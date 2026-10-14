#!/usr/bin/env python3
"""Fetch one official Remix Icon line/fill pair into a run cache."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SAFE_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
REPOSITORY = "Remix-Design/RemixIcon"
DEFAULT_VERSION = "4.9.0"
TREE_URL = "https://api.github.com/repos/{repository}/git/trees/v{version}?recursive=1"
RAW_URL = "https://raw.githubusercontent.com/{repository}/v{version}/{path}"
LICENSE_URL = "https://github.com/Remix-Design/RemixIcon/blob/v{version}/License"


def request(url: str) -> bytes:
    headers = {"User-Agent": "SlidePoise Remix Icon fetcher", "Accept": "application/vnd.github+json"}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        return response.read()


def validate_svg(data: bytes) -> list[float]:
    root = ET.fromstring(data.decode("utf-8"))
    if root.tag.split("}")[-1].lower() != "svg" or not root.attrib.get("viewBox"):
        raise ValueError("file is not a viewBox SVG")
    for element in root.iter():
        local = element.tag.split("}")[-1].lower()
        if local in {"script", "foreignobject"}:
            raise ValueError(f"unsafe SVG element: {local}")
        for key, value in element.attrib.items():
            attr = key.split("}")[-1].lower()
            lowered = str(value).strip().lower()
            if attr.startswith("on") or lowered.startswith(("javascript:", "data:")):
                raise ValueError("active SVG content is not allowed")
    values = [float(value) for value in root.attrib["viewBox"].replace(",", " ").split()]
    if len(values) != 4 or values[2:] != [24.0, 24.0]:
        raise ValueError(f"unexpected Remix Icon viewBox: {root.attrib['viewBox']}")
    return values


def locate_pair(name: str, version: str) -> dict[str, str]:
    url = TREE_URL.format(repository=REPOSITORY, version=version)
    tree = json.loads(request(url).decode("utf-8"))
    if tree.get("truncated"):
        raise ValueError("official repository tree response was truncated")
    result = {}
    for variant in ("line", "fill"):
        suffix = f"/{name}-{variant}.svg"
        matches = [item["path"] for item in tree.get("tree", []) if item.get("type") == "blob" and str(item.get("path", "")).startswith("icons/") and str(item.get("path", "")).endswith(suffix)]
        if len(matches) != 1:
            raise ValueError(f"Expected one official {name}-{variant}.svg, found {len(matches)}")
        result[variant] = matches[0]
    if Path(result["line"]).parent != Path(result["fill"]).parent:
        raise ValueError("line/fill candidates do not share one official Remix Icon category")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Official Remix Icon base name without -line or -fill")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--version")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    source = ((config.get("remote_sources") or {}).get("remix_icon") or {})
    if not source.get("enabled"):
        raise SystemExit("Remix Icon retrieval is disabled in the resolved config")
    name = args.name.strip().lower()
    version = str(args.version or source.get("provider_version") or DEFAULT_VERSION).strip()
    if not SAFE_NAME.fullmatch(name):
        raise SystemExit("Remix Icon name must contain lowercase letters, digits, and hyphens only")
    if not SAFE_VERSION.fullmatch(version):
        raise SystemExit("Remix Icon version must use major.minor.patch")
    paths = locate_pair(name, version)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pair_id = f"remix-{name}"
    asset_ids = [f"{pair_id}-line", f"{pair_id}-fill"]
    assets = []
    for variant, repository_path in paths.items():
        url = RAW_URL.format(repository=REPOSITORY, version=version, path=urllib.parse.quote(repository_path, safe="/"))
        data = request(url)
        validate_svg(data)
        output = args.output_dir / f"{pair_id}-{variant}.svg"
        output.write_bytes(data)
        asset = {
            "asset_id": f"{pair_id}-{variant}",
            "canonical_file": str(output.resolve()),
            "source_url": url,
            "source_repository_path": repository_path,
            "provider": "Remix Icon",
            "provider_version": version,
            "license": "Remix Icon License v1.0",
            "license_url": LICENSE_URL.format(version=version),
            "attribution_notice": "This project uses icons from Remix Icon (https://remixicon.com), licensed under the Remix Icon License v1.0.",
            "style_variant": variant,
            "style_pair_id": pair_id,
            "pair_asset_ids": asset_ids,
            "intrinsic_aspect_ratio": 1.0,
            "treatment_recolorable": True,
            "recolor_mode": "fill_all",
            "preserve_canonical_color": False,
            "sha256": hashlib.sha256(data).hexdigest(),
            "persistence": "run_cache_only",
            "selection_status": "candidate_pending_post_generation_visual_review",
        }
        output.with_suffix(".provenance.json").write_text(json.dumps(asset, indent=2) + "\n", encoding="utf-8")
        assets.append(asset)
    pair = {
        "pair_id": pair_id,
        "semantic_icon_name": name,
        "provider": "Remix Icon",
        "provider_version": version,
        "category": Path(paths["line"]).parent.name,
        "candidates": assets,
        "selection_owner": "host_agent_post_generation_visual_review",
    }
    manifest = args.output_dir / f"{pair_id}.pair.json"
    manifest.write_text(json.dumps(pair, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pair_manifest": str(manifest.resolve()), **pair}, indent=2))


if __name__ == "__main__":
    main()
