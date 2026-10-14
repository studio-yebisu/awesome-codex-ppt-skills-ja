#!/usr/bin/env python3
"""List a profile's visual references and selected shared Library Sets."""
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
    repository = Path(__file__).resolve().parents[2] / "profiles"
    return installed if installed.is_dir() else repository


def default_sets_root() -> Path:
    installed = Path(os.environ.get("SLIDEPOISE_HOME", Path.home() / ".slidepoise")) / "library-sets"
    repository = Path(__file__).resolve().parents[2] / "library-sets"
    return installed if (installed / "catalog.json").is_file() else repository


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["all", *KINDS], default="all")
    parser.add_argument("--profile")
    parser.add_argument("--config", type=Path, help="Resolved session configuration used by generation")
    parser.add_argument("--profiles-root", type=Path, default=default_profiles_root())
    parser.add_argument("--library-sets-root", type=Path, default=default_sets_root())
    parser.add_argument("--query", default="")
    from retrieve_references import add_retrieval_arguments, run_retrieval
    add_retrieval_arguments(parser)
    args = parser.parse_args()
    if args.intent:
        if args.kind not in ("all", "visual_references"):
            parser.error("Per-slide reference retrieval requires --kind visual_references or all")
        run_retrieval(args, parser)
        return

    selected = KINDS if args.kind == "all" else (args.kind,)
    output: dict[str, list[dict]] = {}
    cfg = json.loads(args.config.read_text()) if args.config else None
    if cfg:
        profile = cfg["resolved_profile"]
        args.profile = profile["profile_id"]
        libraries = cfg.get("libraries", {})
        set_index = cfg.get("library_sets", {}).get("records", {})
    else:
        if not args.profile:
            parser.error("Use --config for a session, or --profile to browse a shared profile")
        profile = json.loads((args.profiles_root / args.profile / "profile.json").read_text(encoding="utf-8"))
        base_path = args.profiles_root.parent / "config.json"
        base = json.loads(base_path.read_text()) if base_path.is_file() else {}
        location = base.get("library_locations", {}).get(args.profile, {}).get("visual_references")
        legacy = (Path(location) if location else args.profiles_root / args.profile / "libraries/visual_references") / "catalog.json"
        try:
            libraries, context = resolve_libraries(profile, args.library_sets_root, legacy_visual_catalog=legacy)
        except (ValueError, OSError) as error:
            parser.error(str(error))
        set_index = context["records"]
    for kind in selected:
        library = libraries.get(kind, {})
        records = []
        for set_id in library.get("set_ids", []):
            record = set_index.get(set_id, {})
            if record.get("source") == "remote":
                if cfg and not cfg.get("remote_sources", {}).get(record.get("provider"), {}).get("enabled"):
                    continue
                records.append({"set_id": set_id, "name": record.get("name"), "source": "remote", "provider": record.get("provider")})
        for catalog_path, catalog, item in selected_records(library):
            haystack = " ".join([str(item.get("resource_id", item.get("id", ""))), str(item.get("name", "")), str(item.get("description", "")), " ".join(map(str, item.get("tags", []) or []))]).lower()
            terms = [term for term in args.query.lower().split() if term]
            if terms and not all(term in haystack for term in terms):
                continue
            record = dict(item)
            asset_path = catalog_path.parent / str(item.get("preview_path") or item.get("path") or item.get("definition_path") or "")
            record["absolute_path"] = str(asset_path.resolve()) if asset_path.is_file() else None
            record["profile_id"] = args.profile
            records.append(record)
        output[kind] = records
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
