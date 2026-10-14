#!/usr/bin/env python3
"""Retrieve local slide-reference candidates without selecting or attaching them."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime/src"))
from slidepoise.reference_retrieval import AUTHENTICITY_MODES, read_json, retrieve


def add_retrieval_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--intent", type=Path, help="Per-slide intent with communication job, relationships and role")
    parser.add_argument("--output", type=Path, help="Candidate JSON, with no automatic generation attachment")
    parser.add_argument("--sheet", type=Path, help="Actual candidate thumbnail contact sheet PNG")
    parser.add_argument("--index", type=Path, help="SQLite index, defaults to output filename with .sqlite suffix")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--authenticity", choices=AUTHENTICITY_MODES, default="authentic")
    parser.add_argument("--catalog", type=Path, action="append", default=[], help="Additional explicitly scoped catalog")
    parser.add_argument("--asset-root", type=Path, action="append", default=[], help="Additional allowed private asset root")
    parser.add_argument("--exclude-id", action="append", default=[])
    parser.add_argument("--exclusions", type=Path, help="JSON with ids, canonical_paths, sha256, source_families, source_types")
    parser.add_argument("--include-ineligible", action="store_true", help="Include host-marked retrieval_eligible false records")


def run_retrieval(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not all((args.config, args.intent, args.output, args.sheet)):
        parser.error("Per-slide retrieval requires --config, --intent, --output and --sheet")
    try:
        result = retrieve(args.config, args.intent, args.output, args.sheet, index_path=args.index,
                          extra_catalogs=args.catalog, asset_roots=args.asset_root,
                          exclusions=read_json(args.exclusions) if args.exclusions else None,
                          exclude_ids=args.exclude_id, authenticity=args.authenticity,
                          query=args.query, limit=args.limit, include_ineligible=args.include_ineligible)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({"output": str(args.output.resolve()), "contact_sheet": result["contact_sheet"],
                      "index_path": result["index_path"], "candidate_count": len(result["candidates"]),
                      "omitted_count": len(result["omitted"]), "selection_owner": "host_agent"}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="Resolved session configuration")
    parser.add_argument("--query", default="", help="Optional host-authored terms to widen recall")
    add_retrieval_arguments(parser)
    run_retrieval(parser.parse_args(), parser)


if __name__ == "__main__":
    main()
