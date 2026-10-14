#!/usr/bin/env python3
"""Collect objective shared catalog, selection and asset-path facts."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime/src"))
from slidepoise.resource_catalogs import KINDS, resolve_libraries, selected_records


def default_profiles_root() -> Path:
    installed = Path(os.environ.get("SLIDEPOISE_HOME", Path.home() / ".slidepoise")) / "profiles"
    return installed if installed.is_dir() else Path(__file__).resolve().parents[2] / "profiles"


def inspect_catalog(path: Path, label: str, errors: list[str], *, legacy: bool = False, check_unregistered: bool = False) -> None:
    if not path.is_file():
        errors.append(f"{label}: missing catalog")
        return
    data = json.loads(path.read_text())
    items = data.get("items", {})
    if not isinstance(items, dict):
        errors.append(f"{label}: items must be an object")
        return
    seen, registered = set(), set()
    root = path.parent.resolve()
    for key, record in items.items():
        identifier = str(record.get("id") or "")
        if not identifier or identifier in seen:
            errors.append(f"{label}:{key}: missing or duplicate id")
        seen.add(identifier)
        for field in ("path", "preview_path", "definition_path", "source_document_path"):
            relative = record.get(field)
            if not relative:
                continue
            target = (root / str(relative)).resolve()
            if not target.is_relative_to(root):
                errors.append(f"{label}:{key}: asset escapes its library {relative}")
            elif not target.is_file():
                errors.append(f"{label}:{key}: missing asset {relative}")
            else:
                registered.add(target)
    if legacy or check_unregistered:
        for target in root.rglob("*"):
            if (target.is_file() and target not in (path, path.with_suffix(".json.lock"))
                    and not target.name.startswith(".") and target.resolve() not in registered
                    and (legacy or target.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"})):
                errors.append(f"{label}: unregistered asset {target.relative_to(root).as_posix()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles-root", type=Path, default=default_profiles_root())
    parser.add_argument("--profile")
    parser.add_argument("--library-sets-root", type=Path)
    args = parser.parse_args()
    errors, counts = [], {}
    profile_dirs = [args.profiles_root / args.profile] if args.profile else sorted(path.parent for path in args.profiles_root.glob("*/profile.json"))
    if not args.profiles_root.is_dir():
        errors.append(f"profiles folder missing: {args.profiles_root}")
    elif not profile_dirs:
        errors.append(f"no profiles found in: {args.profiles_root}")
    sets_root = args.library_sets_root or args.profiles_root.parent / "library-sets"
    if args.library_sets_root is None and not (sets_root / "catalog.json").is_file():
        sets_root = Path(__file__).resolve().parents[2] / "library-sets"
    set_index = {}
    if (sets_root / "catalog.json").is_file():
        set_index = json.loads((sets_root / "catalog.json").read_text()).get("items", {})
    else:
        errors.append(f"library sets catalog missing: {sets_root / 'catalog.json'}")
    base_path = args.profiles_root.parent / "config.json"
    base = json.loads(base_path.read_text()) if base_path.is_file() else {}
    for profile_dir in profile_dirs:
        path = profile_dir / "profile.json"
        if not path.is_file():
            errors.append(f"missing profile: {path}")
            continue
        profile = json.loads(path.read_text())
        profile_id = str(profile.get("profile_id") or profile_dir.name)
        configured = base.get("library_locations", {}).get(profile_id, {}).get("visual_references")
        legacy = (Path(configured) if configured else profile_dir / "libraries/visual_references") / "catalog.json"
        if "visual_references" not in profile.get("library_sets", {}):
            inspect_catalog(legacy, f"{profile_id}:visual_references", errors, legacy=True)
        try:
            libraries, context = resolve_libraries(profile, sets_root, legacy_visual_catalog=legacy)
            counts[profile_id] = {kind: len(list(selected_records(libraries[kind]))) for kind in KINDS}
            counts[profile_id].update({f"{kind.removesuffix('s')}_sets": len(context["selected"].get(kind, [])) for kind in KINDS})
        except (ValueError, OSError, TypeError) as error:
            errors.append(f"{profile_id}: {error}")
    for set_id, record in set_index.items():
        if record.get("source") == "local":
            inspect_catalog(sets_root / record.get("root", "") / "catalog.json", f"library-set:{set_id}", errors,
                            check_unregistered=record.get("kind") == "visual_references")
    print(json.dumps({"evidence_type": "objective_catalog_structure", "agent_interpretation_required": True,
                      "counts": counts, "blocking_facts": errors,
                      "notice": "No overall verdict is produced. The host Agent still judges relevance, style, and visual quality."}, indent=2))
    raise SystemExit(0 if not errors else 2)


if __name__ == "__main__":
    main()
