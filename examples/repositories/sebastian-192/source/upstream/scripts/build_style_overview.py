#!/usr/bin/env python3
"""Locally arrange existing slide images or explicit crops into a thumbnail grid."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from json_io import read_json
from overlay_text import FONT_CANDIDATES, load_font
from PIL import Image, ImageDraw, ImageOps


def build_overview(spec_path: Path, output: Path, overwrite: bool = False) -> dict:
    spec_path, output = spec_path.resolve(), output.resolve()
    spec = read_json(spec_path)
    if not isinstance(spec, dict):
        raise TypeError("Overview specification must be an object")
    slides = spec.get("slides")
    if not isinstance(slides, list) or not 1 <= len(slides) <= 8:
        raise ValueError("Provide 1-8 existing slide images or explicit crops")
    width, height = spec.get("width", 1600), spec.get("height", 900)
    if any(type(v) is not int or not 480 <= v <= 4096 for v in (width, height)) or width <= height:
        raise ValueError("Canvas must be landscape, with integer dimensions between 480 and 4096")
    aspect = spec.get("slide_aspect_ratio", [16, 9])
    if (not isinstance(aspect, list) or len(aspect) != 2
            or any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in aspect)):
        raise ValueError("slide_aspect_ratio must contain two positive finite numbers")
    ratio = aspect[0] / aspect[1]
    if not 0.2 <= ratio <= 5:
        raise ValueError("slide_aspect_ratio must be between 1:5 and 5:1")
    if output.suffix.lower() != ".png":
        raise ValueError("Output must be a PNG file")
    if output == spec_path:
        raise ValueError("Output must not overwrite the specification")
    if output.exists() and not overwrite:
        raise ValueError("Output exists; choose a new filename or use --overwrite")
    images = []
    for slide in slides:
        if not isinstance(slide, dict) or not isinstance(slide.get("file"), str):
            raise TypeError("Each slide needs a file path")
        relative = Path(slide["file"])
        path = (spec_path.parent / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(spec_path.parent):
            raise ValueError("Images must stay inside the specification directory")
        if path == output:
            raise ValueError("Output must not overwrite a source image")
        with Image.open(path) as opened:
            image = ImageOps.exif_transpose(opened).convert("RGBA")
        if "box" in slide:
            box = slide["box"]
            if not isinstance(box, list) or len(box) != 4 or any(type(v) is not int for v in box):
                raise ValueError("Crop box must be four integers: x, y, width, height")
            x, y, w, h = box
            if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > image.width or y + h > image.height:
                raise ValueError("Crop box is outside the source image")
            image = image.crop((x, y, x + w, y + h))
        images.append(image)
    columns = 1 if len(images) == 1 else 2 if len(images) <= 4 else 3 if len(images) <= 6 else 4
    rows = math.ceil(len(images) / columns)
    scale = min(width / 1600, height / 900)
    margin, gap, header, label_h = [max(1, round(v * scale)) for v in (48, 36, 96, 30)]
    cell_w = (width - 2 * margin - (columns - 1) * gap) // columns
    cell_h = (height - header - margin - (rows - 1) * gap) // rows - label_h
    tile_w = min(cell_w, int(cell_h * ratio))
    tile_h = round(tile_w / ratio)
    left = (width - columns * tile_w - (columns - 1) * gap) // 2
    canvas = Image.new("RGB", (width, height), "#EBEDF0")
    draw = ImageDraw.Draw(canvas)
    fonts = [spec.get("font"), *FONT_CANDIDATES]
    title_font = load_font(max(12, round(32 * scale)), fonts)
    label_font = load_font(max(10, round(22 * scale)), fonts)
    title = str(spec.get("title", ""))
    if draw.textbbox((0, 0), title, font=title_font)[2] > width - 2 * margin:
        raise ValueError("Overview title is too wide; shorten it")
    draw.text((margin, round(24 * scale)), title, font=title_font, fill="#263444")
    tiles = []
    for index, (slide, image) in enumerate(zip(slides, images)):
        x = left + (index % columns) * (tile_w + gap)
        y = header + (index // columns) * (tile_h + label_h + gap)
        draw.rectangle((x, y, x + tile_w - 1, y + tile_h - 1), fill="white")
        fitted = ImageOps.contain(image, (tile_w, tile_h), Image.Resampling.LANCZOS)
        px, py = x + (tile_w - fitted.width) // 2, y + (tile_h - fitted.height) // 2
        canvas.paste(fitted, (px, py), fitted)
        draw.rectangle((x, y, x + tile_w - 1, y + tile_h - 1), outline="#BCC5CF")
        label = str(slide.get("label", f"{index + 1:02d}"))
        if draw.textbbox((0, 0), label, font=label_font)[2] > tile_w:
            raise ValueError("Thumbnail label is too wide")
        draw.text((x, y + tile_h + max(1, round(3 * scale))), label, font=label_font, fill="#364658")
        tiles.append({"label": label, "box": [x, y, tile_w, tile_h], "source": slide["file"]})
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return {"output": str(output), "pixels": [width, height], "tiles": tiles, "image_generation_calls": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        result = build_overview(args.spec, args.output, args.overwrite)
    except (TypeError, ValueError, OSError) as error:
        parser.exit(2, f"build_style_overview: {error}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
