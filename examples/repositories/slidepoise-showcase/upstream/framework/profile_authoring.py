"""User-owned guidance profile authoring shared by Agents and the Console."""
from __future__ import annotations

import copy
import re
import tempfile
from pathlib import Path

from .paths import data_home
from .profiles import canonical_profile_id, active_profile_id, profile_record
from .storage import read, revision, update, write


KINDS = {
    "visual_references": {".png", ".jpg", ".jpeg", ".webp"},
}


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")
    if not result or len(result) > 60:
        raise ValueError("Use a short profile name with letters or numbers")
    return result


def create_profile(name: str, *, profile_id: str | None = None, based_on: str | None = None, purpose: str = "") -> dict:
    based_on = canonical_profile_id(based_on or active_profile_id())
    identifier = slug(profile_id or name)
    root = data_home() / "profiles" / identifier
    if root.exists():
        raise FileExistsError(f"Profile already exists: {identifier}")
    # Older custom locations join the same shared catalogs before their selection is copied.
    from .shared_resource_migration import migrate_shared_resources
    migrate_shared_resources(data_home())
    source = Path(profile_record(based_on)["root"])
    profile = read(source / "profile.json", {})
    from .design import merge
    configured = read(data_home() / "config.json", {}).get("user_design_overrides", {}).get(based_on, {})
    profile["design_overrides"] = merge(profile.get("design_overrides", {}), configured)
    profile.update({"profile_id": identifier, "name": name.strip(), "purpose": purpose.strip() or f"A user-authored presentation style based on {based_on}."})
    profile["origin"] = {"type": "user_authored", "based_on": based_on}
    root.parent.mkdir(parents=True, exist_ok=True)
    # Keep the copy invisible to profile discovery until its identity is distinct.
    with tempfile.TemporaryDirectory(prefix="profile-create-", dir=data_home()) as directory:
        staged = Path(directory) / "profile"
        staged.mkdir()
        write(staged / "profile.json", profile)
        staged.rename(root)
    return profile_record(identifier)


def apply_profile_values(profile_id: str, profile: dict, values: dict) -> dict:
    """Validate a profile edit without writing any files."""
    if not isinstance(values, dict) or any(not re.fullmatch(r"[a-z][a-z0-9_]*", key) for key in values):
        raise ValueError("Profile fields must use lower-case names")
    if {"profile_id", "schema_version"} & set(values):
        raise ValueError("Profile identity and schema version cannot be changed here")
    result = copy.deepcopy(profile)
    for key, value in values.items():
        if key in {"name", "purpose"} and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{key} must be meaningful text")
        result[key] = copy.deepcopy(value)
    if "library_sets" in values or "library_items" in values:
        from .library_sets import validate_selection
        validate_selection(result)
    result["profile_id"] = profile_id
    return result


def update_profile(profile_id: str, values: dict, expected: str) -> dict:
    profile_id = canonical_profile_id(profile_id)
    path = Path(profile_record(profile_id)["path"])
    update(path, lambda profile: apply_profile_values(profile_id, profile, values), expected=expected, default={})
    return profile_record(profile_id)


def profile_payload(profile_id: str) -> dict:
    record = profile_record(profile_id)
    return {**record, "revision": revision(Path(record["path"]))}


def add_resource(profile_id: str, kind: str, source: Path, *, name: str, description: str,
                 tags: list[str] | None = None, source_url: str = "", license_name: str = "",
                 source_type: str = "unknown", source_page: str = "") -> dict:
    if kind not in KINDS:
        raise ValueError("Unknown resource kind")
    source = source.expanduser().resolve()
    if not source.is_file() or source.suffix.lower() not in KINDS[kind]:
        raise ValueError(f"Unsupported {kind} file")
    if source_type not in {"unknown", "published_document", "user_private_document", "generated_image"}:
        raise ValueError("Choose a known reference origin")
    if tags is not None and (not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags)):
        raise ValueError("Reference tags must be a list of strings")
    from . import library_sets
    profile_id = canonical_profile_id(profile_id)
    record = profile_record(profile_id)
    profile = record["profile"]
    set_ids = library_sets.profile_set_ids(profile, kind)
    local = [set_id for set_id in set_ids if library_sets.set_record(set_id).get("source") == "local"]
    if local:
        set_id = local[0]
    else:
        stem = f"{profile_id}-references"
        candidate = stem
        suffix = 2
        existing = {item["id"] for item in library_sets.list_sets()}
        while candidate in existing:
            candidate = f"{stem}-{suffix}"
            suffix += 1
        set_id = library_sets.create_set(candidate, kind, f"References first collected for {record['name']}")["id"]
    added = library_sets.add_resource(set_id, source, name=name, description=description, tags=tags,
                                     source_url=source_url, license_name=license_name,
                                     source_type=source_type, source_page=source_page)
    def select(document):
        chosen = document.setdefault("library_sets", {}).setdefault(kind, [])
        if set_id not in chosen:
            chosen.append(set_id)
        subset = document.get("library_items", {}).get(kind, {}).get(set_id)
        if subset is not None and added["id"] not in subset:
            subset.append(added["id"])
        return document
    update(Path(record["path"]), select, default={})
    return {**added, "profile": profile_id, "kind": kind}
