#!/usr/bin/env python3
"""Inspect a packaged or current-chat visual asset for deterministic placement metadata.

This utility reports file type, intrinsic dimensions when available, and aspect ratio.
It does not decide whether the asset is visually appropriate; selection belongs to the host Agent.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


def svg_dimensions(path: Path) -> tuple[float | None, float | None]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if viewbox:
        parts = [float(v) for v in re.split(r"[ ,]+", viewbox.strip()) if v]
        if len(parts) == 4 and parts[2] > 0 and parts[3] > 0:
            return parts[2], parts[3]
    def numeric(value: str | None) -> float | None:
        if not value:
            return None
        match = re.match(r"\s*([0-9.]+)", value)
        return float(match.group(1)) if match else None
    return numeric(root.attrib.get("width")), numeric(root.attrib.get("height"))


def inspect(path: Path) -> dict:
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    suffix = path.suffix.lower()
    width = height = None
    kind = "unknown"
    if suffix == ".svg":
        kind = "svg"
        width, height = svg_dimensions(path)
    else:
        try:
            with Image.open(path) as im:
                width, height = map(float, im.size)
                kind = im.format.lower() if im.format else suffix.lstrip(".")
        except Exception:
            kind = suffix.lstrip(".") or "unknown"
    ratio = (width / height) if width and height and height > 0 else None
    return {
        "path": str(path),
        "kind": kind,
        "intrinsic_width": width,
        "intrinsic_height": height,
        "intrinsic_aspect_ratio": round(ratio, 6) if ratio else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inspect(args.asset)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
