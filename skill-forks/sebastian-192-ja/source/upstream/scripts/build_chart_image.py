#!/usr/bin/env python3
"""Draw precise grouped bar/column references, optionally replace an authorized page region."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

from audit_chart_geometry import chart_series, number
from json_io import read_json
from overlay_text import FONT_CANDIDATES, load_font, parse_color
from PIL import Image, ImageDraw, ImageOps
from render_deck import sha256
from validate_page_spec import _relative_path, load_page_spec


def protected_paths(spec_path, layout_path, spec):
    return {spec_path.resolve(), layout_path.resolve(),
            *[_relative_path(spec_path.parent, s["image_file"]) for s in spec["slides"]],
            *[_relative_path(spec_path.parent, p) for p in spec["style"].get("tokens", {}).get("reference_images", [])]}


def render(spec_path, layout_path, output, replace_region=False):
    spec_path, output = spec_path.resolve(), output.resolve()
    spec, _ = load_page_spec(spec_path)
    layout = read_json(layout_path)
    slide = next((s for s in spec["slides"] if s["id"] == layout["slide_id"]), None)
    element = next((e for e in slide["elements"] if e["id"] == layout["element_id"]), None) if slide else None
    if not element or element["kind"] != "chart":
        raise ValueError("Layout must select an existing chart element")
    data, categories, series = chart_series(element)
    values = [v for item in series for v in item["values"]]
    source = _relative_path(spec_path.parent, slide["image_file"])
    if output in protected_paths(spec_path, layout_path, spec):
        raise ValueError("Write a new image; do not overwrite the source page")
    if output.suffix.lower() != ".png":
        raise ValueError("Use PNG output to preserve pixels outside the replaced region")
    region = layout["region"]
    if len(region) != 4 or any(isinstance(x, bool) or not isinstance(x, int) for x in region):
        raise ValueError("Region must be integer [x,y,width,height]")
    x, y, width, height = region
    if min(x, y) < 0 or min(width, height) <= 0 or max(width, height) > 16384:
        raise ValueError("Invalid region bounds")
    px, py, pw, ph = (number(v) for v in layout["plot"])
    if min(px, py) < 0 or min(pw, ph) <= 0 or px + pw >= width or py + ph >= height:
        raise ValueError("Plot must fit inside region with space for labels/ticks")
    lo, hi = number(layout["axis_min"]), number(layout["axis_max"])
    if lo >= hi or lo > min(0, *values) or hi < max(0, *values):
        raise ValueError("Axis must include zero and every source value")
    colors = {key: parse_color(layout.get(key, default)) for key, default in (
        ("background", "#FFFFFF"), ("positive_color", "#9582DE"), ("negative_color", "#B8A8E2"),
        ("text_color", "#242638"), ("grid_color", "#DED9EF"))}
    font_size = layout.get("font_size", 24)
    if isinstance(font_size, bool) or not isinstance(font_size, int) or font_size <= 0:
        raise ValueError("Font size must be a positive integer")
    font = load_font(font_size, [layout.get("font"), *FONT_CANDIDATES])
    series_colors = layout.get("series_colors", ["#9582DE", "#488AB8", "#C9774B", "#408569"])
    if not isinstance(series_colors, list) or len(series_colors) < len(series):
        raise ValueError("Supply a color for every series")
    series_colors = [parse_color(c) for c in series_colors]
    image = Image.new("RGB", (width, height), colors["background"])
    draw = ImageDraw.Draw(image)

    def text(position, value, anchor):
        bounds = draw.textbbox(position, value, font=font, anchor=anchor)
        if bounds[0] < 0 or bounds[1] < 0 or bounds[2] > width or bounds[3] > height:
            raise ValueError(f"Label overflows region: {value}; enlarge region or adjust plot/font")
        draw.text(position, value, font=font, fill=colors["text_color"], anchor=anchor)

    horizontal = data["chart_type"] == "bar"
    scale = (pw if horizontal else -ph) / (hi - lo)
    zero = px - lo * scale if horizontal else py + ph - lo * scale
    for tick in layout.get("ticks", [lo, 0, hi]):
        tick = number(tick)
        if not lo <= tick <= hi:
            raise ValueError("Tick outside axis")
        position = zero + tick * scale
        if horizontal:
            draw.line((position, py, position, py + ph), fill=colors["grid_color"], width=1)
            text((position, py + ph + 8), f"{tick:g}", "mt")
        else:
            draw.line((px, position, px + pw, position), fill=colors["grid_color"], width=1)
            text((px - 12, position), f"{tick:g}", "rm")
    if horizontal:
        draw.line((zero, py, zero, py + ph), fill=colors["text_color"], width=1)
    else:
        draw.line((px, zero, px + pw, zero), fill=colors["text_color"], width=1)
    step = (ph if horizontal else pw) / len(categories)
    slot = step * 0.8 / len(series)
    thickness = number(layout.get("bar_thickness", slot * 0.7))
    if not 0 < thickness < slot:
        raise ValueError("Bar thickness must be smaller than its series slot")
    decimals = layout.get("decimals", 2)
    if isinstance(decimals, bool) or not isinstance(decimals, int) or not 0 <= decimals <= 8:
        raise ValueError("Decimals must be an integer between 0 and 8")
    geometry = []
    if len(series) > 1:
        lx, ly = layout.get("legend_position", [px, 8])
        lx, ly = number(lx), number(ly)
        if ly + font_size + 7 >= py:
            raise ValueError("Legend must fit above the plot")
        for index, item in enumerate(series):
            text((lx, ly), item["name"], "lt")
            tw = draw.textlength(item["name"], font=font)
            draw.line((lx, ly + font_size + 3, lx + tw, ly + font_size + 3), fill=series_colors[index], width=4)
            lx += tw + 30
    for index, category in enumerate(categories):
        center = (py if horizontal else px) + step * (index + 0.5)
        if layout.get("show_categories", True):
            text((px - 12, center) if horizontal else (center, py + ph + 12), category, "rm" if horizontal else "mt")
        for series_index, item in enumerate(series):
            value = item["values"][index]
            cross = center + (series_index - (len(series) - 1) / 2) * slot
            end = zero + value * scale
            color = series_colors[series_index] if len(series) > 1 else colors["positive_color" if value >= 0 else "negative_color"]
            if value:
                box = ((min(zero, end), cross - thickness / 2, max(zero, end), cross + thickness / 2)
                       if horizontal else (cross - thickness / 2, min(zero, end), cross + thickness / 2, max(zero, end)))
                draw.rectangle(box, fill=color)
            label = format(value, ("+" if layout.get("signed", False) else "") + f".{decimals}f") + layout.get("suffix", "")
            if horizontal:
                text((end + 8, cross) if value >= 0 else (end - 8, cross), label, "lm" if value >= 0 else "rm")
            else:
                text((cross, end - 8) if value >= 0 else (cross, end + 8), label, "mb" if value >= 0 else "mt")
            offset = (x if horizontal else y) if replace_region else 0
            geometry.append({"category": category, **({"series": item["name"]} if len(series) > 1 else {}),
                             "start": offset + zero, "end": offset + end,
                             "cross_center": ((y if horizontal else x) if replace_region else 0) + cross})
    source_hash = None
    if replace_region:
        if layout.get("source_sha256") != sha256(source):
            raise ValueError("Replacement source hash is missing or stale")
        source_hash = sha256(source)
        with Image.open(source) as opened:
            page = ImageOps.exif_transpose(opened).convert("RGBA")
        if x + width > page.width or y + height > page.height:
            raise ValueError("Replacement region outside source page")
        page.paste(image, (x, y))
        image = page
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, staged = tempfile.mkstemp(suffix=".png", dir=output.parent)
    os.close(fd)
    try:
        image.save(staged)
        os.replace(staged, output)
    finally:
        Path(staged).unlink(missing_ok=True)
    return {"output": str(output), "output_sha256": sha256(output), "page_spec_sha256": sha256(spec_path),
            "layout_sha256": sha256(layout_path), "source_sha256": source_hash,
            "region": region, "coordinate_space": "page" if replace_region else "region", "construction_geometry": geometry,
            "note": "Construction coordinates are not independent visual observations. Inspect the output before approval."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_spec", type=Path)
    parser.add_argument("layout", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--replace-region", action="store_true", help="Modify only the specified rectangle; respect host image-edit permissions")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        if args.report:
            spec, _ = load_page_spec(args.page_spec)
            if args.report.resolve() in protected_paths(args.page_spec.resolve(), args.layout, spec) | {args.output.resolve()}:
                raise ValueError("Report must not overwrite source inputs or the generated image")
        report = render(args.page_spec, args.layout, args.output, args.replace_region)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=True))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, f"build_chart_image: {error}\n")


if __name__ == "__main__":
    main()
