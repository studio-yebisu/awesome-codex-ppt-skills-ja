"""Move legacy profile reference catalogs into shared resource storage safely."""
from __future__ import annotations

import copy
import hashlib
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from .storage import locked, read, write


BUNDLED_REFERENCE_IDS = {
    "consulting": "consulting-references",
    "editorial-archive": "editorial-references",
    "monochrome-modern": "monochrome-references",
    "pwc-public": "pwc-public-references",
}


def _qualified(values: Any, set_id: str, identifiers: set[str]) -> Any:
    if isinstance(values, dict):
        return {key: _qualified(value, set_id, identifiers) for key, value in values.items()}
    if isinstance(values, list):
        return [_qualified(value, set_id, identifiers) for value in values]
    return f"{set_id}:{values}" if isinstance(values, str) and values in identifiers else values


def _copy_catalog(source: Path, destination: Path, set_id: str) -> tuple[dict, list[str]]:
    """Copy referenced local files, including provenance outside the old folder."""
    catalog = copy.deepcopy(read(source, {"items": {}}))
    copied: dict[Path, str] = {}
    def relocate(value):
        if isinstance(value, dict):
            return {key: relocate(item) for key, item in value.items()}
        if isinstance(value, list):
            return [relocate(item) for item in value]
        if not isinstance(value, str) or not value or "://" in value or "\n" in value:
            return value
        # Only existing local files are paths. Descriptions and source URLs remain verbatim.
        try:
            path = (source.parent / Path(value).expanduser()).resolve()
            if not path.is_file():
                return value
        except (OSError, ValueError):
            return value
        if path not in copied:
            if path.is_relative_to(source.parent.resolve()):
                relative = path.relative_to(source.parent.resolve())
            else:
                digest = hashlib.sha256(str(path).encode()).hexdigest()[:12]
                relative = Path("sources") / f"{digest}-{path.name}"
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied[path] = relative.as_posix()
        return copied[path]
    catalog = relocate(catalog)
    for key, item in catalog.get("items", {}).items():
        identifier = str(item.get("id") or key)
        item.setdefault("id", identifier)
        item["resource_id"] = f"{set_id}:{identifier}"
    write(destination / "catalog.json", catalog)
    return catalog, [str(path) for path in copied]


def migrate_shared_resources(home: Path) -> dict[str, Any]:
    """Register old catalogs once and preserve their original files for existing runs."""
    home = home.expanduser().resolve()
    with locked(home / ".shared-resources-migration"):
        return _migrate(home)


def _migrate(home: Path) -> dict[str, Any]:
    config_path = home / "config.json"
    config = read(config_path, {}) or {}
    index_path = home / "library-sets/catalog.json"
    index = read(index_path, {"schema_version": "1.0.0", "items": {}})
    original_index = copy.deepcopy(index)
    original_config = copy.deepcopy(config)
    groups: dict[Path, list[tuple[Path, dict, bool]]] = {}
    for path in sorted((home / "profiles").glob("*/profile.json")):
        profile = read(path, {})
        identifier = profile.get("profile_id", path.parent.name)
        configured = config.get("library_locations", {}).get(identifier, {}).get("visual_references")
        # An explicit shared selection, including an empty one, supersedes old files.
        if not configured and "visual_references" in profile.get("library_sets", {}):
            continue
        folder = Path(configured).expanduser() if configured else path.parent / "libraries/visual_references"
        catalog = (folder / "catalog.json").resolve()
        if catalog.is_file():
            groups.setdefault(catalog, []).append((path, profile, bool(configured)))
    if not groups:
        return {"migrated": False, "sets": 0, "profiles": 0}
    known = {item.get("migration", {}).get("legacy_catalog"): identifier
             for identifier, item in index.get("items", {}).items()
             if item.get("migration", {}).get("legacy_catalog")}
    for identifier, record in index.get("items", {}).items():
        if record.get("source") == "local" and record.get("kind") == "visual_references":
            path = (home / "library-sets" / record.get("root", "") / "catalog.json").resolve()
            known.setdefault(str(path), identifier)
    updates: dict[Path, dict] = {}
    pending: list[tuple[Path, Path]] = []
    with tempfile.TemporaryDirectory(prefix="shared-resources-", dir=home) as temporary:
        stage = Path(temporary)
        for catalog, members in groups.items():
            set_id = known.get(str(catalog))
            if set_id:
                record = index["items"][set_id]
                migrated = read(home / "library-sets" / record["root"] / "catalog.json", {"items": {}})
            else:
                owner = next((profile for path, profile, _ in members if catalog.is_relative_to(path.parent.resolve())), members[0][1])
                profile_id = owner.get("profile_id", members[0][0].parent.name)
                stem = BUNDLED_REFERENCE_IDS.get(profile_id, f"{profile_id}-references")
                stem = re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-") or "imported-references"
                set_id = stem
                suffix = 2
                while set_id in index.get("items", {}) or (home / "library-sets/visual_references" / set_id).exists():
                    set_id = f"{stem}-{suffix}"
                    suffix += 1
                staged = stage / set_id
                staged.mkdir()
                migrated, legacy_files = _copy_catalog(catalog, staged, set_id)
                relative = f"visual_references/{set_id}"
                name = str(owner.get("name") or profile_id).strip()
                if not re.search(r"\breferences?$", name, re.IGNORECASE):
                    name += " references"
                index.setdefault("items", {})[set_id] = {
                    "id": set_id, "kind": "visual_references",
                    "name": name,
                    "description": "Shared references imported from an existing profile",
                    "source": "local", "root": relative,
                    "migration": {"legacy_catalog": str(catalog), "legacy_files": legacy_files},
                }
                pending.append((staged, home / "library-sets" / relative))
            identifiers = {str(item.get("id") or key) for key, item in migrated.get("items", {}).items()}
            for path, original, configured in members:
                profile = copy.deepcopy(original)
                profile_id = profile.get("profile_id", path.parent.name)
                selected = profile.setdefault("library_sets", {}).setdefault("visual_references", [])
                if set_id not in selected:
                    selected.append(set_id)
                for field in ("visual_reference_priorities", "always_attach_visual_references"):
                    if field in profile:
                        profile[field] = _qualified(profile[field], set_id, identifiers)
                updates[path] = profile
                if configured:
                    locations = config.get("library_locations", {}).get(profile_id, {})
                    locations.pop("visual_references", None)
                    if not locations:
                        config["library_locations"].pop(profile_id, None)
        backup = home / "archive" / f"shared-resources-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
        backup.mkdir(parents=True)
        for path in [config_path, index_path, *updates]:
            if path.is_file():
                destination = backup / path.relative_to(home)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
        for catalog in groups:
            digest = hashlib.sha256(str(catalog).encode()).hexdigest()[:16]
            shutil.copy2(catalog, backup / f"legacy-catalog-{digest}.json")
        write(backup / "migration.json", {
            "catalogs": [str(path) for path in groups],
            "profiles": [str(path) for path in updates],
            "note": "Original resource files remain available for captured presentations and recovery.",
        })
        for staged, destination in pending:
            destination.parent.mkdir(parents=True, exist_ok=True)
            staged.rename(destination)
        if index != original_index:
            write(index_path, index)
        for path, profile in updates.items():
            write(path, profile)
        if config != original_config:
            write(config_path, config)
    return {"migrated": True, "sets": len(pending), "profiles": len(updates), "backup": str(backup)}
