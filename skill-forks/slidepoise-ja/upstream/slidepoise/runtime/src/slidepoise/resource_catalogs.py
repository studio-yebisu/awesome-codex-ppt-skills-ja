"""Resolve shared resource selections without copying or caching asset catalogs."""
from __future__ import annotations

import copy
import json
from pathlib import Path

KINDS = ("visual_references", "icons", "components")


def resolve_libraries(profile: dict, sets_root: Path, *, session: dict | None = None,
                      legacy_visual_catalog: Path | None = None) -> tuple[dict, dict]:
    session = session or {}
    index = json.loads((sets_root / "catalog.json").read_text()).get("items", {})
    selected = copy.deepcopy(profile.get("library_sets", {}))
    subsets = copy.deepcopy(profile.get("library_items", {}))
    for field, target in (("library_sets", selected), ("library_items", subsets)):
        override = session.get(field)
        if override is not None:
            if not isinstance(override, dict) or set(override) - set(KINDS):
                raise ValueError(f"{field} must contain only known resource kinds")
            target.update(copy.deepcopy(override))
    context = {"root": str(sets_root.resolve()), "selected": selected, "items": subsets, "records": {}}
    libraries = {}
    for kind in KINDS:
        identifiers = selected.get(kind, [])
        if not isinstance(identifiers, list) or any(not isinstance(value, str) for value in identifiers):
            raise ValueError(f"library_sets.{kind} must be a list of set ids")
        choices = subsets.get(kind, {})
        if not isinstance(choices, dict):
            raise ValueError(f"library_items.{kind} must be an object")
        if set(choices) - set(identifiers):
            # A session can deselect a set without inheriting its profile subset.
            if kind in (session.get("library_sets") or {}) and kind not in (session.get("library_items") or {}):
                choices = {key: value for key, value in choices.items() if key in identifiers}
                subsets[kind] = choices
            else:
                raise ValueError(f"library_items.{kind} refers to an unselected set")
        sources, providers = [], []
        for set_id in identifiers:
            record = copy.deepcopy(index.get(set_id))
            if record is None or record.get("kind") != kind:
                raise ValueError(f"Unknown or wrong resource type for library set {set_id}")
            record["root"] = str((sets_root / record.get("root", "")).resolve())
            context["records"][set_id] = record
            if record.get("source") == "remote":
                if set_id in choices:
                    raise ValueError(f"Remote library set {set_id} cannot select local item ids")
                if record.get("provider"):
                    providers.append(record["provider"])
                continue
            catalog = Path(record["root"]) / "catalog.json"
            source = {"set_id": set_id, "catalog": str(catalog), "root": record["root"]}
            if set_id in choices:
                items = choices[set_id]
                if not isinstance(items, list) or any(not isinstance(value, str) for value in items):
                    raise ValueError(f"library_items.{kind}.{set_id} must be a list of item ids")
                raw = json.loads(catalog.read_text()).get("items", {})
                known = {str(item.get("id") or key) for key, item in raw.items()}
                if set(items) - known:
                    raise ValueError(f"Unknown selected item in library set {set_id}")
                source["item_ids"] = list(dict.fromkeys(items))
            sources.append(source)
        if kind == "visual_references" and kind not in selected and legacy_visual_catalog is not None:
            sources.append({"catalog": str(legacy_visual_catalog.resolve()), "root": str(legacy_visual_catalog.parent.resolve())})
        catalogs = [source["catalog"] for source in sources]
        libraries[kind] = {"sources": sources, "catalogs": catalogs,
                           "catalog": catalogs[0] if catalogs else None,
                           "set_ids": list(identifiers), "providers": providers}
    return libraries, context


def catalog_sources(library: dict) -> list[dict]:
    if "sources" in library:
        return copy.deepcopy(library["sources"])
    values = library.get("catalogs", [library.get("catalog")])
    return [{"catalog": value} for value in values if value]


def selected_records(library: dict):
    """Yield fresh records, their catalogs and catalog metadata within the selection."""
    for source in catalog_sources(library):
        path = Path(source["catalog"]).expanduser().resolve()
        catalog = json.loads(path.read_text())
        allowed = source.get("item_ids")
        for key, raw in catalog.get("items", {}).items():
            identifier = str(raw.get("id") or key)
            if allowed is not None and identifier not in allowed:
                continue
            record = {**raw, "id": identifier}
            if source.get("set_id"):
                record.update(set_id=source["set_id"], resource_id=f"{source['set_id']}:{identifier}")
            yield path, catalog, record


def scope_reference_records(records: list[dict], sources: list[dict]) -> list[dict]:
    """Filter and qualify indexed reference records using their source catalogs."""
    by_path = {str(Path(source["catalog"]).expanduser().resolve()): source for source in sources}
    result = []
    for record in records:
        source = by_path.get(record["catalog_path"])
        if source is None:
            continue
        if source.get("item_ids") is not None and record["id"] not in source["item_ids"]:
            continue
        if source.get("set_id"):
            record = {**record, "set_id": source["set_id"], "resource_id": f"{source['set_id']}:{record['id']}"}
        result.append(record)
    return result
