#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build a high-resolution contact sheet from exported PPT slide PNGs."""

from __future__ import annotations

import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SLIDE_DIR = ROOT / "assets" / "posters" / "poster_template_preview_slides"
OUT_PATH = ROOT / "assets" / "gallery" / "poster_template_preview_contact_sheet.png"

COLS = 3
PAGE_W = 2200
PAGE_H = 1238
SCALE = 0.48
THUMB_W = int(PAGE_W * SCALE)
THUMB_H = int(PAGE_H * SCALE)
GAP_X = 38
GAP_Y = 44
LABEL_H = 30
TOP = 24
LEFT = 22
RIGHT = 22
BOTTOM = 24
BG = (255, 255, 255)
TEXT = (54, 63, 74)
SUBTLE = (90, 98, 109)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    return ImageFont.truetype(path, size)


def slide_num(path: Path) -> int:
    m = re.search(r"(\d+)", path.stem)
    return int(m.group(1)) if m else 0


def fit_contain(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    src_ratio = img.width / img.height
    dst_ratio = tw / th
    if src_ratio > dst_ratio:
        nw = tw
        nh = int(tw / src_ratio)
    else:
        nh = th
        nw = int(th * src_ratio)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (tw, th), BG)
    x = (tw - nw) // 2
    y = (th - nh) // 2
    canvas.paste(resized, (x, y))
    return canvas


def main() -> None:
    slides = sorted(SLIDE_DIR.glob("*.PNG"), key=slide_num)
    if not slides:
        raise SystemExit(f"No slide PNGs found in {SLIDE_DIR}")

    rows = math.ceil(len(slides) / COLS)
    width = LEFT + RIGHT + COLS * THUMB_W + (COLS - 1) * GAP_X
    row_h = LABEL_H + THUMB_H
    height = TOP + BOTTOM + rows * row_h + (rows - 1) * GAP_Y
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)

    label_font = load_font(18, bold=False)

    for i, slide in enumerate(slides):
        row = i // COLS
        col = i % COLS
        x = LEFT + col * (THUMB_W + GAP_X)
        y = TOP + row * (row_h + GAP_Y)
        num = slide_num(slide)
        draw.text((x, y), f"Slide {num}", font=label_font, fill=SUBTLE)
        img = Image.open(slide).convert("RGB")
        thumb = fit_contain(img, (THUMB_W, THUMB_H))
        canvas.paste(thumb, (x, y + LABEL_H))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PATH, quality=96)
    print(OUT_PATH)


if __name__ == "__main__":
    main()
