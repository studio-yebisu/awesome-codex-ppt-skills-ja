#!/usr/bin/env python3
"""Download an Agent-selected exact remote asset into a run cache with provenance."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--asset-id", required=True)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--license", default="unknown, verify before external publication")
    args = parser.parse_args()
    parsed = urllib.parse.urlparse(args.url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit("Remote assets require an explicit HTTPS URL selected by the Agent")
    request = urllib.request.Request(args.url, headers={"User-Agent": "SlidePoise/0.3 exact-asset-fetch"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(20 * 1024 * 1024 + 1)
        content_type = response.headers.get_content_type()
    if len(data) > 20 * 1024 * 1024:
        raise SystemExit("Remote asset exceeds the 20 MB run-cache limit")
    suffix = Path(parsed.path).suffix.lower() or mimetypes.guess_extension(content_type) or ".bin"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / f"{args.asset_id}{suffix}"
    target.write_bytes(data)
    provenance = {
        "asset_id": args.asset_id,
        "canonical_file": str(target.resolve()),
        "source_name": args.source_name,
        "source_url": args.url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "license": args.license,
        "sha256": hashlib.sha256(data).hexdigest(),
        "persistence": "run_cache_only",
        "selection_authority": "host_agent"
    }
    target.with_suffix(target.suffix + ".provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
