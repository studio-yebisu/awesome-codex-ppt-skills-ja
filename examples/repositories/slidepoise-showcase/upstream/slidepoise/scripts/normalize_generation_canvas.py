#!/usr/bin/env python3
"""Apply an explicit host-Agent crop and fit it to the resolved generation canvas.

This script never discovers unwanted chrome or decides what should be cropped. The host
Agent must visually inspect the candidate and provide the crop rectangle. The script
then performs deterministic, aspect-preserving geometry only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime/src"))
from slidepoise.canvas import validate_derived_canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--crop", nargs=4, type=int, metavar=("X", "Y", "W", "H"))
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    try:
        target_w, target_h = validate_derived_canvas(cfg)["generation_region_px"]
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    image = Image.open(args.input).convert("RGB")
    if args.crop:
        x, y, w, h = args.crop
        if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > image.width or y + h > image.height:
            raise SystemExit("crop rectangle is outside the source image")
        image = image.crop((x, y, x + w, y + h))

    scale = min(target_w / image.width, target_h / image.height)
    resized = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), cfg.get("design", {}).get("style", {}).get("background", "#FFFFFF"))
    left = (target_w - resized.width) // 2
    top = (target_h - resized.height) // 2
    canvas.paste(resized, (left, top))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output)
    print(json.dumps({
        "output": str(args.output.resolve()),
        "target_px": [target_w, target_h],
        "source_after_crop_px": list(image.size),
        "placed_px": [left, top, resized.width, resized.height],
        "note": "Crop choice came from host-Agent visual reasoning; this script only normalized geometry."
    }, indent=2))


if __name__ == "__main__":
    main()
