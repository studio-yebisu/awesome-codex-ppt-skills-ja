from __future__ import annotations

import hashlib
import json
import shutil
import copy
from datetime import datetime
from pathlib import Path
from typing import Any

from .paths import BUNDLED_LIBRARY_SETS_ROOT, BUNDLED_PROFILES_ROOT, DEFAULT_CONFIG, SESSION_TEMPLATE, active_profiles_root, data_home, settings_path


LIBRARY_KINDS = {"visual_references", "icons", "components"}
PROFILE_ID_ALIASES = json.loads((BUNDLED_PROFILES_ROOT / "aliases.json").read_text(encoding="utf-8"))


def canonical_profile_id(profile_id: str) -> str:
    # An explicitly installed profile takes precedence over a retired bundle name.
    if (active_profiles_root() / profile_id / "profile.json").is_file():
        return profile_id
    return PROFILE_ID_ALIASES.get(profile_id, profile_id)


def merge_known_values(base: Any, configured: Any) -> Any:
    """Add new defaults while preserving configured and legacy values verbatim."""
    if isinstance(base, dict) and isinstance(configured, dict):
        merged = copy.deepcopy(configured)
        for key, value in base.items():
            merged[key] = merge_known_values(value, configured[key]) if key in configured else copy.deepcopy(value)
        return merged
    return copy.deepcopy(configured)


def migrate_config(source: Path, destination: Path, archive_root: Path) -> bool:
    bundled = read_json(source, {}) or {}
    current = read_json(destination, {}) or {}
    legacy_single_slide = (
        isinstance(current.get("scope"), dict)
        and current["scope"].get("mode") == "single_slide"
        and bundled.get("scope", {}).get("mode") == "adaptive_presentation"
    )
    migrated = merge_known_values(bundled, current)
    adapter = migrated.get("generation", {}).get("host_adapter", {})
    if adapter.get("mode") == "host_native_or_delegated_image_generation":
        adapter["mode"] = "agent_discovered_or_manual"
        for key in ("chatgpt", "codex", "unsupported_host_policy"):
            adapter.pop(key, None)
    if legacy_single_slide:
        # Scope is a retired runtime contract, not a user presentation preference.
        migrated["scope"]["mode"] = "adaptive_presentation"
    legacy_icons = current.get("external_icon_fetch") or {}
    if isinstance(legacy_icons, dict) and legacy_icons.get("enabled") is not None:
        migrated["remote_sources"]["remix_icon"]["enabled"] = bool(legacy_icons["enabled"])
    for field in ("user_design_overrides", "library_locations"):
        values = migrated.get(field)
        if isinstance(values, dict):
            for legacy_id, current_id in PROFILE_ID_ALIASES.items():
                if (active_profiles_root() / legacy_id / "profile.json").is_file():
                    continue
                if legacy_id in values and current_id not in values:
                    values[current_id] = values.pop(legacy_id)
    for locations in migrated.get("library_locations", {}).values():
        for kind, location in locations.items():
            path = Path(location).expanduser().resolve()
            if path.exists():
                continue
            for old, new in PROFILE_ID_ALIASES.items():
                old_root = active_profiles_root() / old
                if path.is_relative_to(old_root):
                    locations[kind] = str(active_profiles_root() / new / path.relative_to(old_root))
                    break
    design = migrated.get("design")
    if isinstance(design, dict) and design.get("profile") in PROFILE_ID_ALIASES:
        design["profile"] = canonical_profile_id(design["profile"])
    migrated["schema_version"] = bundled["schema_version"]
    if migrated == current:
        return False
    archive_root.mkdir(parents=True, exist_ok=True)
    backup = archive_root / f"config-before-{bundled['schema_version']}.json"
    if backup.exists():
        suffix = 2
        while (archive_root / f"config-before-{bundled['schema_version']}-{suffix}.json").exists():
            suffix += 1
        backup = archive_root / f"config-before-{bundled['schema_version']}-{suffix}.json"
    shutil.copy2(destination, backup)
    write_json(destination, migrated)
    return True


def read_json(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def list_profiles(root: Path | None = None) -> list[dict[str, Any]]:
    profiles = []
    for path in sorted((root or active_profiles_root()).glob("*/profile.json")):
        payload = read_json(path, {}) or {}
        profile_id = str(payload.get("profile_id") or path.parent.name)
        style = ((payload.get("design_overrides") or {}).get("style") or {})
        accents = list(style.get("accent_colors") or [])
        neutrals = list(style.get("neutral_colors") or [])
        profiles.append({
            "id": profile_id,
            "name": str(payload.get("name") or profile_id),
            "purpose": str(payload.get("purpose") or ""),
            "path": str(path),
            "root": str(path.parent),
            "modes": list((payload.get("modes") or {}).keys()),
            "library_sets": copy.deepcopy(payload.get("library_sets", {"visual_references": [], "icons": [], "components": []})),
            "library_items": copy.deepcopy(payload.get("library_items", {})),
            "style_agency": copy.deepcopy(payload.get("style_agency", {})),
            "preview": {
                "colors": [
                    accents[0] if accents else "#2F2F31",
                    accents[1] if len(accents) > 1 else (neutrals[1] if len(neutrals) > 1 else "#9A9A9F"),
                    str(style.get("background") or (neutrals[-1] if neutrals else "#F1F1F2")),
                ],
                "density": str(style.get("density") or "balanced"),
            },
        })
    return profiles


def active_profile_id() -> str:
    available = list_profiles()
    ids = {item["id"] for item in available}
    requested = canonical_profile_id(str((read_json(settings_path(), {}) or {}).get("active_profile") or "consulting"))
    if requested in ids:
        return requested
    return available[0]["id"] if available else ""


def set_active_profile(profile_id: str) -> dict[str, Any]:
    profile = profile_record(profile_id)
    from .storage import update
    update(settings_path(), lambda settings: {**settings, "active_profile": profile["id"]}, default={})
    return profile


def profile_record(profile_id: str) -> dict[str, Any]:
    profile_id = canonical_profile_id(profile_id)
    for item in list_profiles():
        if item["id"] == profile_id:
            payload = read_json(Path(item["path"]), {}) or {}
            return {**item, "profile": payload}
    raise FileNotFoundError(f"Unknown SlidePoise profile: {profile_id}")


def library_root(profile_id: str, kind: str) -> Path:
    """Compatibility access for a single catalog. Use selected_items for aggregation."""
    profile_id = canonical_profile_id(profile_id)
    if kind not in LIBRARY_KINDS:
        raise ValueError(f"Unknown resource kind {kind}")
    record = profile_record(profile_id)
    from .library_sets import profile_set_ids, set_record
    for set_id in profile_set_ids(record["profile"], kind):
        selected = set_record(set_id)
        if selected.get("source") == "local":
            return Path(selected["root"])
    # Read-only compatibility with old catalogs and captured presentation fixtures.
    configured = read_json(data_home() / "config.json", {}).get("library_locations", {}).get(profile_id, {}).get(kind)
    root = Path(configured).expanduser().resolve() if configured else Path(record["root"]) / "libraries" / kind
    if not root.is_dir():
        raise FileNotFoundError(root)
    return root


def library_catalog(profile_id: str, kind: str) -> tuple[Path, dict[str, Any]]:
    root = library_root(profile_id, kind)
    path = root / "catalog.json"
    return path, read_json(path, {"items": {}}) or {"items": {}}


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_profiles(source: Path, target: Path, previous_manifest: dict[str, str] | None = None, *, manifest_prefix: str = "") -> tuple[dict[str, str], dict[str, int]]:
    manifest: dict[str, str] = {}
    counts = {"installed": 0, "updated": 0, "migrated": 0, "unchanged": 0, "preserved_user_changes": 0}
    previous_manifest = previous_manifest or {}
    target.mkdir(parents=True, exist_ok=True)
    for source_file in sorted(source.rglob("*")):
        if not source_file.is_file():
            continue
        relative = source_file.relative_to(source)
        target_file = target / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        source_hash = hash_file(source_file)
        current_hash = hash_file(target_file) if target_file.is_file() else None
        manifest_key = f"{manifest_prefix}{relative.as_posix()}"
        previous_hash = previous_manifest.get(manifest_key)
        if current_hash is None:
            shutil.copy2(source_file, target_file)
            counts["installed"] += 1
        elif current_hash == source_hash:
            counts["unchanged"] += 1
        elif previous_hash and current_hash == previous_hash:
            shutil.copy2(source_file, target_file)
            counts["updated"] += 1
        else:
            counts["preserved_user_changes"] += 1
        manifest[manifest_key] = source_hash
    return manifest, counts


def migrate_profile_ids(home: Path, previous_manifest: dict[str, str]) -> tuple[dict[str, str], dict[str, int]]:
    """Rename bundled profile identities while preserving every installed file."""
    counts: dict[str, int] = {}
    manifest = dict(previous_manifest)
    for legacy_id, current_id in PROFILE_ID_ALIASES.items():
        legacy = home / "profiles" / legacy_id
        current = home / "profiles" / current_id
        if not legacy.is_dir() or current.exists():
            continue
        source_profile = legacy / "profile.json"
        legacy_profile_key = f"profiles/{legacy_id}/profile.json"
        managed_profile = source_profile.is_file() and manifest.get(legacy_profile_key) == hash_file(source_profile)
        if source_profile.is_file():
            backup = home / "archive" / "profile-id-migration" / legacy_id / "profile.json"
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_profile, backup)
        legacy.rename(current)
        profile = read_json(current / "profile.json", {}) or {}
        profile["profile_id"] = current_id
        write_json(current / "profile.json", profile)
        old_prefix = f"profiles/{legacy_id}/"
        new_prefix = f"profiles/{current_id}/"
        manifest = {(new_prefix + key.removeprefix(old_prefix)) if key.startswith(old_prefix) else key: value
                    for key, value in manifest.items()}
        if managed_profile:
            manifest[f"profiles/{current_id}/profile.json"] = hash_file(current / "profile.json")
        counts["profile_ids_migrated"] = counts.get("profile_ids_migrated", 0) + 1
    return manifest, counts


def retire_managed_files(home: Path, target: Path, previous: dict[str, str], current: dict[str, str],
                         prefix: str, archive: Path, counts: dict[str, int]) -> None:
    """Archive removed bundled files and leave user-modified files in place."""
    retained = set()
    for record in read_json(home / "library-sets/catalog.json", {}).get("items", {}).values():
        migration = record.get("migration", {})
        retained.update(migration.get("legacy_files", []))
        if migration.get("legacy_catalog"):
            retained.add(migration["legacy_catalog"])
    for relative in sorted(set(previous) - set(current)):
        target_file = target / relative.removeprefix(prefix)
        if not target_file.is_file() or str(target_file.resolve()) in retained:
            continue
        if hash_file(target_file) == previous[relative]:
            archived = archive / relative.removeprefix(prefix)
            archived.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target_file), str(archived))
            counts["retired_archived"] = counts.get("retired_archived", 0) + 1
        else:
            counts["preserved_user_changes"] += 1


def initialize_home(source_profiles: Path, *, force: bool = False) -> dict[str, Any]:
    home = data_home()
    home.mkdir(parents=True, exist_ok=True)
    target = home / "profiles"
    from .shared_resource_migration import migrate_shared_resources
    migrated_resources = migrate_shared_resources(home)
    if force and target.exists():
        backup = home / "archive" / "profiles-before-setup"
        if backup.exists():
            raise FileExistsError(f"Backup already exists: {backup}")
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(backup))
    previous_payload = read_json(home / "manifest.json", {}) or {}
    previous_manifest = previous_payload.get("files", {}) if isinstance(previous_payload.get("files", {}), dict) else {}
    previous_manifest, identity_counts = migrate_profile_ids(home, previous_manifest)
    profile_previous = {key: value for key, value in previous_manifest.items() if key.startswith("profiles/")}
    legacy_profile_previous = {f"profiles/{key}": value for key, value in previous_manifest.items() if not key.startswith(("config.json", "session-overrides-template.json", "profiles/", "library-sets/"))}
    profile_previous = {**legacy_profile_previous, **profile_previous}
    manifest, counts = copy_profiles(source_profiles, target, profile_previous, manifest_prefix="profiles/")
    for key, value in identity_counts.items():
        counts[key] = counts.get(key, 0) + value
    retirement_root = home / "archive" / f"retired-bundle-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
    retire_managed_files(home, target, profile_previous, manifest, "profiles/", retirement_root, counts)
    for folder in sorted((path for path in target.rglob("*") if path.is_dir()), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()
    set_previous = {key: value for key, value in previous_manifest.items() if key.startswith("library-sets/")}
    sets_target = home / "library-sets"
    set_manifest, set_counts = copy_profiles(BUNDLED_LIBRARY_SETS_ROOT, sets_target, set_previous, manifest_prefix="library-sets/")
    manifest.update(set_manifest)
    # A user-owned index keeps its existing records and receives newly bundled sets.
    bundled_sets = read_json(BUNDLED_LIBRARY_SETS_ROOT / "catalog.json", {"items": {}})
    installed_index = read_json(sets_target / "catalog.json", {"schema_version": "1.0.0", "items": {}})
    before_index = copy.deepcopy(installed_index)
    for identifier, record in bundled_sets.get("items", {}).items():
        installed_index.setdefault("items", {}).setdefault(identifier, record)
    if installed_index != before_index:
        write_json(sets_target / "catalog.json", installed_index)
    for key, value in set_counts.items():
        counts[key] = counts.get(key, 0) + value
    retire_managed_files(home, sets_target, set_previous, set_manifest, "library-sets/", retirement_root, counts)
    for folder in sorted((path for path in sets_target.rglob("*") if path.is_dir()), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()
    for source, destination in ((DEFAULT_CONFIG, home / "config.json"), (SESSION_TEMPLATE, home / "session-overrides-template.json")):
        relative = destination.relative_to(home).as_posix()
        source_hash = hash_file(source)
        current_hash = hash_file(destination) if destination.is_file() else None
        previous_hash = previous_manifest.get(relative)
        if current_hash is None:
            shutil.copy2(source, destination)
            counts["installed"] += 1
        elif current_hash == source_hash:
            counts["unchanged"] += 1
        elif destination.name == "config.json" and migrate_config(source, destination, home / "archive"):
            counts["migrated"] += 1
        elif previous_hash and current_hash == previous_hash:
            shutil.copy2(source, destination)
            counts["updated"] += 1
        else:
            counts["preserved_user_changes"] += 1
        manifest[relative] = source_hash
    write_json(home / "manifest.json", {"files": manifest, "source": str(source_profiles.resolve())})
    settings = read_json(settings_path(), {}) or {}
    if settings.get("active_profile") in PROFILE_ID_ALIASES and not (target / settings["active_profile"] / "profile.json").is_file():
        settings["active_profile"] = PROFILE_ID_ALIASES[settings["active_profile"]]
    settings.setdefault("active_profile", "consulting")
    write_json(settings_path(), settings)
    for folder in (home / "workspace", home / "cache"):
        folder.mkdir(parents=True, exist_ok=True)
    after_resources = migrate_shared_resources(home)
    return {"home": str(home), "profiles": len(list(target.glob("*/profile.json"))), "active_profile": settings["active_profile"], "files": counts,
            "shared_resources": after_resources if after_resources["migrated"] else migrated_resources}
