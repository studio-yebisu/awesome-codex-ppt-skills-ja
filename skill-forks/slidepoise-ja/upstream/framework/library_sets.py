"""Shared resources selected by guidance profiles and the Console."""
from __future__ import annotations

from pathlib import Path
import re
import shutil
import uuid
from typing import Any

from .paths import active_library_sets_root, installed_library_sets_root, BUNDLED_LIBRARY_SETS_ROOT
from .storage import locked, read, revision, update


SET_KINDS = {"visual_references", "icons", "components"}
RESOURCE_SUFFIXES = {
    "visual_references": {".png", ".jpg", ".jpeg", ".webp"},
    "icons": {".svg", ".png"},
    "components": {".json", ".svg", ".png", ".pptx"},
}
SOURCE_TYPES = {"unknown", "published_document", "user_private_document", "generated_image"}


def _ensure_installed() -> Path:
    """Keep all mutations outside the bundled package, including before setup."""
    root = installed_library_sets_root()
    with locked(root.parent / ".library-sets-install"):
        if not (root / "catalog.json").is_file():
            root.mkdir(parents=True, exist_ok=True)
            # Install the index last so concurrent readers see a complete set tree.
            source_files = [path for path in BUNDLED_LIBRARY_SETS_ROOT.rglob("*") if path.is_file()]
            source_files.sort(key=lambda path: path == BUNDLED_LIBRARY_SETS_ROOT / "catalog.json")
            for source in source_files:
                target = root / source.relative_to(BUNDLED_LIBRARY_SETS_ROOT)
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
    return root


def catalog_path() -> Path:
    return active_library_sets_root() / "catalog.json"


def list_sets(kind: str | None = None) -> list[dict[str, Any]]:
    payload = read(catalog_path(), {"items": {}})
    values = payload.get("items", {}).values()
    result = []
    for raw in values:
        item = dict(raw)
        if kind and item.get("kind") != kind:
            continue
        item["id"] = str(item["id"])
        item["root"] = str((active_library_sets_root() / item.get("root", "")).resolve())
        result.append(item)
    return sorted(result, key=lambda item: (item.get("kind", ""), item.get("name", "")))


def set_record(set_id: str) -> dict[str, Any]:
    for item in list_sets():
        if item["id"] == set_id:
            return item
    raise FileNotFoundError(f"Unknown library set: {set_id}")


def set_catalog(set_id: str) -> tuple[Path, dict[str, Any]]:
    record = set_record(set_id)
    if record.get("source") == "remote":
        return catalog_path(), {"items": {}}
    path = Path(record["root"]) / "catalog.json"
    return path, read(path, {"items": {}})


def catalog_items(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Use stored item IDs, retaining compatibility with historical catalog keys."""
    result = {}
    for key, item in catalog.get("items", {}).items():
        identifier = str(item.get("id") or key)
        if identifier in result:
            raise ValueError(f"Duplicate resource ID {identifier}")
        result[identifier] = item
    return result


def validate_selection(profile: dict[str, Any]) -> None:
    """Reject unknown sets and item IDs before a profile selection is persisted."""
    selections = profile.get("library_sets", {})
    subsets = profile.get("library_items", {})
    if not isinstance(selections, dict) or set(selections) - SET_KINDS:
        raise ValueError("Choose visual reference, icon or component sets")
    if not isinstance(subsets, dict) or set(subsets) - SET_KINDS:
        raise ValueError("Resource selections must be grouped by resource kind")
    records = {record["id"]: record for record in list_sets()}
    for kind, identifiers in selections.items():
        if not isinstance(identifiers, list) or any(not isinstance(value, str) for value in identifiers):
            raise ValueError("Selected Library Sets must be a list of IDs")
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("Select each Library Set only once")
        for identifier in identifiers:
            if identifier not in records or records[identifier].get("kind") != kind:
                raise ValueError(f"Unknown {kind} Library Set {identifier}")
    for kind, sets in subsets.items():
        if not isinstance(sets, dict):
            raise ValueError("Resource selections must be grouped by Library Set")
        for set_id, identifiers in sets.items():
            if set_id not in selections.get(kind, []):
                raise ValueError(f"Resource selection refers to unselected Library Set {set_id}")
            if not isinstance(identifiers, list) or any(not isinstance(value, str) for value in identifiers):
                raise ValueError("Selected resources must be a list of IDs")
            if len(set(identifiers)) != len(identifiers):
                raise ValueError("Select each resource only once")
            if records[set_id].get("source") == "remote":
                raise ValueError("Remote sources are selected as complete Library Sets")
            catalog = set_catalog(set_id)[1]
            unknown = set(identifiers) - set(catalog_items(catalog))
            if unknown:
                raise ValueError(f"Unknown resources in {set_id}: {', '.join(sorted(unknown))}")


def profile_set_ids(profile: dict[str, Any], kind: str) -> list[str]:
    if kind not in SET_KINDS:
        raise ValueError(f"Unknown set kind: {kind}")
    value = profile.get("library_sets", {}).get(kind, [])
    known = {record["id"] for record in list_sets(kind)}
    return [str(item) for item in value if str(item) in known]


def selected_items(profile: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    """Read the current selected items without copying them into a profile."""
    result = []
    subsets = profile.get("library_items", {}).get(kind, {})
    for set_id in profile_set_ids(profile, kind):
        record = set_record(set_id)
        if record.get("source") == "remote":
            continue
        path, catalog = set_catalog(set_id)
        selected = subsets.get(set_id)
        for identifier, raw in catalog_items(catalog).items():
            if selected is not None and identifier not in selected:
                continue
            item = {**raw, "id": identifier, "set_id": set_id,
                    "resource_id": f"{set_id}:{identifier}", "catalog_path": str(path)}
            for key, value in list(item.items()):
                if isinstance(value, str) and value and (key == "path" or key.endswith("_path")) and key != "catalog_path":
                    item[key] = str((path.parent / value).resolve())
            result.append(item)
    return result


def payload() -> dict[str, Any]:
    return {"sets": list_sets(), "revision": revision(catalog_path()), "location": str(active_library_sets_root())}


def update_set_metadata(set_id: str, values: dict[str, Any], expected: str) -> dict[str, Any]:
    _ensure_installed()
    allowed = {"name", "description"}
    if set(values) - allowed:
        raise ValueError("Unsupported library set field")
    def change(document):
        item = document.setdefault("items", {}).get(set_id)
        if item is None:
            raise FileNotFoundError(set_id)
        for key, value in values.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{key} must be meaningful text")
            item[key] = value.strip()
        return document
    update(catalog_path(), change, expected=expected, default={"items": {}})
    return payload()


def create_set(name: str, kind: str, description: str = "") -> dict[str, Any]:
    if kind not in SET_KINDS:
        raise ValueError("Choose visual references, icons or components")
    identifier = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
    if not identifier:
        raise ValueError("Use a meaningful set name")
    root = _ensure_installed()
    folder = root / kind / identifier
    if folder.exists() or any(item["id"] == identifier for item in list_sets()):
        raise FileExistsError(f"Library Set already exists: {identifier}")
    folder.mkdir(parents=True)
    from .storage import write
    write(folder / "catalog.json", {"schema_version": "1.0.0", "items": {}})
    def change(document):
        document.setdefault("items", {})[identifier] = {"id": identifier, "kind": kind, "name": name.strip(), "description": description.strip(), "source": "local", "root": f"{kind}/{identifier}"}
        return document
    update(catalog_path(), change, default={"schema_version": "1.0.0", "items": {}})
    return set_record(identifier)


def add_resource(set_id: str, source: Path, *, name: str, description: str = "", tags: list[str] | None = None,
                 source_url: str = "", license_name: str = "", source_type: str = "unknown",
                 source_page: str = "", provenance: dict[str, Any] | None = None) -> dict[str, Any]:
    _ensure_installed()
    record = set_record(set_id)
    if record.get("source") != "local":
        raise ValueError("Remote Library Sets retrieve assets at run time")
    source = source.expanduser().resolve()
    allowed = RESOURCE_SUFFIXES[record["kind"]]
    if not source.is_file() or source.suffix.lower() not in allowed:
        raise ValueError("Unsupported Library Set resource")
    if record["kind"] == "icons" and not license_name:
        raise ValueError("Persistent icons require license information")
    if source_type not in SOURCE_TYPES:
        raise ValueError("Choose a known resource origin")
    if tags is not None and (not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags)):
        raise ValueError("Resource tags must be a list of strings")
    if provenance is not None and not isinstance(provenance, dict):
        raise ValueError("Resource provenance must be an object")
    path, _catalog = set_catalog(set_id)
    identifier = uuid.uuid4().hex[:12]
    destination = path.parent / f"{identifier}-{source.name}"
    metadata = {}
    if record["kind"] == "components":
        if source.suffix.lower() == ".pptx":
            from pptx import Presentation
            deck = Presentation(source)
            if not len(deck.slides):
                raise ValueError("The PowerPoint has no slides")
            metadata = {"path": destination.name, "preview_path": destination.with_suffix(".preview.png").name,
                        "native_source_slide_number": 1, "resource_form": "native_powerpoint"}
        elif source.suffix.lower() == ".json":
            definition = read(source)
            if not isinstance(definition, dict):
                raise ValueError("Component guidance must be a JSON object")
            metadata = {"definition_path": destination.name, "resource_form": "grammar_only", "grammar": definition}
        else:
            metadata = {"preview_path": destination.name, "resource_form": "visual_precedent"}
    else:
        metadata = {"path": destination.name}
    origin = {"provider": "user_or_agent_added", "source_url": source_url, "license": license_name, **(provenance or {})}
    if record["kind"] == "visual_references":
        origin.update({"source_type": source_type,
                       "source_url": source_url or (source.name if source_type == "user_private_document" else origin.get("source_url", "")),
                       "source_page": source_page or ("Uploaded image" if source_type == "user_private_document" else ""),
                       "generated_reference": True if source_type == "generated_image" else
                           False if source_type in {"published_document", "user_private_document"} else None})
    shutil.copy2(source, destination)
    def change(document):
        document.setdefault("items", {})[identifier] = {"id": identifier, "resource_id": f"{set_id}:{identifier}", "name": name.strip() or source.stem, "description": description.strip(), "tags": tags or [], **metadata, "provenance": origin}
        return document
    update(path, change, default={"schema_version": "1.0.0", "items": {}})
    return {"id": identifier, "resource_id": f"{set_id}:{identifier}", "set_id": set_id, "path": str(destination)}
