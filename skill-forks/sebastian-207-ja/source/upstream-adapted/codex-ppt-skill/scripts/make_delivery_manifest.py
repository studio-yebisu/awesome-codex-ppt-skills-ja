#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--route", required=True)
    parser.add_argument("--backend", default="unknown")
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument("--source-artifact", action="append", default=[])
    parser.add_argument("--output-file", action="append", default=[])
    parser.add_argument("--qa-status", default="unknown")
    parser.add_argument("--editable-level", default="unknown")
    parser.add_argument("--image-status", default="unknown")
    parser.add_argument("--limitation", action="append", default=[])
    parser.add_argument("--known-limitation", action="append", default=[])
    args = parser.parse_args()
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "route": args.route,
        "execution_backend": args.backend,
        "source_artifacts": args.source_artifact,
        "output_files": args.output_file,
        "qa_status": args.qa_status,
        "editable_level": args.editable_level,
        "image_generation_status": args.image_status,
        "known_limitations": args.limitation + args.known_limitation,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
