#!/usr/bin/env python3
"""Deterministically overlay accurate text onto background images to produce slide pages."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from json_io import read_json
from PIL import Image, ImageDraw, ImageFont, ImageOps

DEFAULTS = {
    "font_size": 48,
    "color": "#333333",
    "align": "left",
    "valign": "top",
    "line_spacing": 1.25,
    "bold": False,
}
FONT_CANDIDATES = (
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "DejaVuSans.ttf",
)
def fail(message: str) -> None:
    raise SystemExit(f"overlay_text: {message}")
def parse_color(value: object) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        fail(f"invalid color {value!r}; expected #RRGGBB")
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))
def load_font(size: int, candidates: list[str]) -> ImageFont.FreeTypeFont:
    for candidate in candidates:
        if not candidate:
            continue
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    fail('no usable TrueType font found; pass --font PATH or set "font" in the spec')
def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for char in paragraph:
            trial = current + char
            if not current or draw.textlength(trial, font=font) <= max_width:
                current = trial
            elif " " in current[1:]:
                cut = current.rfind(" ", 1)
                lines.append(current[:cut].rstrip())
                current = current[cut + 1 :] + char
            else:
                lines.append(current)
                current = char
        lines.append(current)
    return lines
def merged_settings(element: dict, defaults: dict) -> dict:
    if "text" not in element:
        fail('text element is missing required field "text"')
    settings = {**DEFAULTS, **defaults, **element}
    for key in ("x", "y", "w", "h"):
        if key not in settings:
            fail(f"text element is missing required field {key!r}")
        settings[key] = float(settings[key])
    x, y, w, h = settings["x"], settings["y"], settings["w"], settings["h"]
    if not (0 <= x <= 1 and 0 <= y <= 1):
        fail(f"x/y must be within [0, 1]; got x={x}, y={y}")
    if w <= 0 or h <= 0:
        fail(f"w/h must be positive; got w={w}, h={h}")
    if x + w > 1.000001 or y + h > 1.000001:
        fail(f"text box exceeds the page: x+w={x + w:.3f}, y+h={y + h:.3f}")
    if settings["align"] not in ("left", "center", "right"):
        fail(f"align must be left/center/right; got {settings['align']!r}")
    if settings["valign"] not in ("top", "center", "bottom"):
        fail(f"valign must be top/center/bottom; got {settings['valign']!r}")
    settings["font_size"] = int(settings["font_size"])
    if settings["font_size"] <= 0:
        fail(f"font_size must be positive; got {settings['font_size']}")
    settings["color_rgb"] = parse_color(settings["color"])
    settings["line_spacing"] = float(settings["line_spacing"])
    return settings
def render_page(page: dict, spec_dir: Path, defaults: dict, cli_font: str) -> Path:
    for key in ("background", "output", "texts"):
        if key not in page:
            fail(f'each page needs "{key}"')
    background = page["background"]
    if isinstance(background, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", background):
        if "width" not in page or "height" not in page:
            fail('solid-color pages need "width" and "height" in pixels')
        image = Image.new("RGB", (int(page["width"]), int(page["height"])), background)
    else:
        if not isinstance(background, str):
            fail(f'"background" must be a path or #RRGGBB color; got {background!r}')
        source = spec_dir / background
        if not source.is_file():
            fail(f"background image not found: {source}")
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened).convert("RGBA")
    draw = ImageDraw.Draw(image)
    page_width, page_height = image.size
    for element in page["texts"]:
        settings = merged_settings(element, defaults)
        font = load_font(
            settings["font_size"],
            [
                element.get("font"),
                page.get("font"),
                defaults.get("font"),
                cli_font,
                *FONT_CANDIDATES,
            ],
        )
        box_left = settings["x"] * page_width
        box_top = settings["y"] * page_height
        box_width = settings["w"] * page_width
        box_height = settings["h"] * page_height
        lines = wrap_text(draw, str(settings["text"]), font, box_width)
        if any(draw.textlength(line, font=font) > box_width + 1 for line in lines):
            fail(f"text overflows its width on {page['output']}; increase the box or reduce font size")
        line_height = settings["font_size"] * settings["line_spacing"]
        stroke_width = 1 if settings["bold"] else 0
        visible_height = max(
            index * line_height + draw.textbbox((0, 0), line or " ", font=font, anchor="la", stroke_width=stroke_width)[3]
            for index, line in enumerate(lines)
        )
        if visible_height > box_height + 1:
            fail(
                f"text overflows its box on {page['output']}: "
                f"{visible_height:.0f}px > {box_height:.0f}px; "
                "increase the box or reduce font size"
            )
        if settings["valign"] == "center":
            top = box_top + (box_height - visible_height) / 2
        elif settings["valign"] == "bottom":
            top = box_top + box_height - visible_height
        else:
            top = box_top
        top = max(top, box_top)
        x, anchor = {
            "left": (box_left, "la"),
            "center": (box_left + box_width / 2, "ma"),
            "right": (box_left + box_width, "ra"),
        }[settings["align"]]
        y = top
        for line in lines:
            draw.text(
                (x, y),
                line,
                font=font,
                fill=settings["color_rgb"],
                anchor=anchor,
                stroke_width=stroke_width,
                stroke_fill=settings["color_rgb"],
            )
            y += line_height
    output = spec_dir / page["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in (".jpg", ".jpeg"):
        image.convert("RGB").save(output, "JPEG", quality=95)
    else:
        image.save(output)
    return output
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="JSON spec describing pages and text boxes")
    parser.add_argument("--font", default="", help="Fallback TrueType/OpenType font path or name")
    args = parser.parse_args()
    if not args.spec.is_file():
        fail(f"spec file not found: {args.spec}")
    try:
        spec = read_json(args.spec)
    except json.JSONDecodeError as error:
        fail(f"invalid JSON in {args.spec}: {error}")
    defaults = spec.get("defaults", {})
    pages = spec.get("pages")
    if not isinstance(pages, list) or not pages:
        fail('spec must contain a non-empty "pages" list')
    spec_dir = args.spec.resolve().parent
    outputs = [render_page(page, spec_dir, defaults, args.font) for page in pages]
    print(
        json.dumps(
            {"pages": len(outputs), "outputs": [str(path) for path in outputs]},
            ensure_ascii=False,
            indent=2,
        )
    )
if __name__ == "__main__":
    main()
