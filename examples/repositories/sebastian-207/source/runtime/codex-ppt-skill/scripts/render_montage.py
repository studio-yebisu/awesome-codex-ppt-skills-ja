#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def slide_paths(input_dir: Path) -> list[Path]:
    paths = sorted(input_dir.glob("slide_*.png"))
    if not paths:
        paths = sorted(input_dir.glob("*.png"))
    return [p for p in paths if p.name.lower() != "montage.png"]


def build_montage(paths: list[Path], output: Path, thumb_w: int = 480) -> None:
    if not paths:
        raise FileNotFoundError("no slide PNG files found")
    thumbs = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        ratio = img.height / img.width
        thumb_h = int(thumb_w * ratio)
        img = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        thumbs.append((path, img))
    cols = min(3, max(1, math.ceil(math.sqrt(len(thumbs)))))
    rows = math.ceil(len(thumbs) / cols)
    gutter = 28
    label_h = 28
    cell_h = max(img.height for _, img in thumbs) + label_h
    canvas = Image.new("RGB", (cols * thumb_w + (cols + 1) * gutter, rows * cell_h + (rows + 1) * gutter), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    for i, (path, img) in enumerate(thumbs):
        row = i // cols
        col = i % cols
        x = gutter + col * (thumb_w + gutter)
        y = gutter + row * (cell_h + gutter)
        canvas.paste(img, (x, y + label_h))
        draw.text((x, y), path.stem, fill=(80, 80, 80), font=font)
        draw.rectangle((x, y + label_h, x + img.width - 1, y + label_h + img.height - 1), outline=(210, 210, 210), width=1)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--thumb-width", type=int, default=480)
    args = parser.parse_args()
    build_montage(slide_paths(args.input_dir), args.output, args.thumb_width)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
