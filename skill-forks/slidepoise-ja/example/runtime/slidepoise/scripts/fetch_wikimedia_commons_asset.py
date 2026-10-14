#!/usr/bin/env python3
"""Fetch one host-Agent-selected Wikimedia Commons file with provenance."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def clean(value: Any) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(str((value or {}).get("value") or ""))).strip()


def request(url: str, accept: str = "*/*") -> tuple[bytes, str]:
    headers = {"User-Agent": "SlidePoise (https://github.com/henryhyw/slidepoise; media retrieval)", "Accept": accept}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        data = response.read(20 * 1024 * 1024 + 1)
        return data, response.headers.get_content_type()


def validate_svg(data: bytes) -> None:
    root = ET.fromstring(data.decode("utf-8"))
    if root.tag.split("}")[-1].lower() != "svg" or not root.attrib.get("viewBox"):
        raise ValueError("Commons SVG must contain an SVG root and viewBox")
    for element in root.iter():
        local = element.tag.split("}")[-1].lower()
        if local in {"script", "foreignobject"}:
            raise ValueError(f"unsafe SVG element: {local}")
        for key, value in element.attrib.items():
            if key.split("}")[-1].lower().startswith("on") or str(value).strip().lower().startswith(("javascript:", "data:")):
                raise ValueError("active SVG content is not allowed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--file-title", required=True)
    parser.add_argument("--asset-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", args.asset_id):
        raise SystemExit("Asset ID must start with a letter or number and contain only letters, numbers, dots, underscores or hyphens")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    source = ((config.get("remote_sources") or {}).get("wikimedia_commons") or {})
    if not source.get("enabled"):
        raise SystemExit("Wikimedia Commons retrieval is disabled in the resolved config")
    title = args.file_title if args.file_title.startswith("File:") else f"File:{args.file_title}"
    params = {
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url|mime|size|extmetadata",
        "format": "json",
        "formatversion": "2",
    }
    api_url = str(source.get("api_url") or "https://commons.wikimedia.org/w/api.php") + "?" + urllib.parse.urlencode(params)
    metadata_bytes, _ = request(api_url, "application/json")
    metadata_payload = json.loads(metadata_bytes.decode("utf-8"))
    if metadata_payload.get("error"):
        raise SystemExit(f"Wikimedia Commons lookup failed: {metadata_payload['error'].get('info', metadata_payload['error'])}")
    page = ((metadata_payload.get("query") or {}).get("pages") or [{}])[0]
    if page.get("missing") is True or not page.get("imageinfo"):
        raise SystemExit(f"Wikimedia Commons file not found: {title}")
    info = page["imageinfo"][0]
    mime = str(info.get("mime") or "")
    if mime not in set(source.get("allowed_media_types") or []):
        raise SystemExit(f"Wikimedia Commons media type is not enabled: {mime}")
    metadata = info.get("extmetadata") or {}
    license_name = clean(metadata.get("LicenseShortName")) or clean(metadata.get("UsageTerms"))
    license_url = clean(metadata.get("LicenseUrl"))
    if source.get("require_license_metadata") and not license_name:
        raise SystemExit("Selected Commons file has no machine-readable license metadata")
    data, content_type = request(str(info["url"]), mime)
    if len(data) > 20 * 1024 * 1024:
        raise SystemExit("Wikimedia Commons asset exceeds the 20 MB run-cache limit")
    if mime == "image/svg+xml":
        validate_svg(data)
        suffix = ".svg"
    elif mime == "image/png":
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise SystemExit("Downloaded Commons asset is not a valid PNG")
        suffix = ".png"
    else:
        raise SystemExit(f"Unsupported Commons media type: {content_type}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / f"{args.asset_id}{suffix}"
    target.write_bytes(data)
    provenance = {
        "asset_id": args.asset_id,
        "canonical_file": str(target.resolve()),
        "provider": "Wikimedia Commons",
        "file_title": title,
        "source_url": info.get("descriptionurl"),
        "download_url": info.get("url"),
        "artist": clean(metadata.get("Artist")),
        "credit": clean(metadata.get("Credit")),
        "license": license_name,
        "license_url": license_url,
        "attribution_required": clean(metadata.get("AttributionRequired")),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "persistence": "run_cache_only",
        "selection_authority": "host_agent",
        "selection_status": "selected_after_identity_license_and_visual_review",
    }
    target.with_suffix(target.suffix + ".provenance.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(provenance, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
