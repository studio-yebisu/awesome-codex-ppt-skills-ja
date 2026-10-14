"""Load the portable scene contract and validate geometry and local assets."""

from __future__ import annotations

import math
from pathlib import Path

from json_io import read_json
from jsonschema import Draft202012Validator
from PIL import Image

SCHEMA = Path(__file__).resolve().parents[1] / "references" / "scene.schema.json"


def walk(elements):
    for element in elements:
        yield element
        if element["type"] == "group":
            yield from walk(element["children"])


def asset_path(base: Path, value: str) -> Path:
    """Scene assets are portable, relative, and confined to the scene directory."""
    path = Path(value)
    root = base.resolve()
    resolved = (root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(root):
        raise ValueError(f"Asset must stay inside scene directory: {value}")
    if not resolved.is_file():
        raise ValueError(f"Missing asset: {value}")
    return resolved


def _finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Scene numbers must be finite")
    if isinstance(value, dict):
        for item in value.values():
            _finite(item)
    if isinstance(value, list):
        for item in value:
            _finite(item)


def validate_scene(scene: dict, base: Path) -> list[str]:
    _finite(scene)
    schema = read_json(SCHEMA)
    errors = list(Draft202012Validator(schema).iter_errors(scene))
    if errors:
        error = errors[0]
        location = "/".join(str(p) for p in error.absolute_path) or "root"
        raise ValueError(f"Scene schema at {location}: {error.message}")
    width, height = scene["canvas"]["width"], scene["canvas"]["height"]
    if not 1 <= scene["canvas"].get("width_inches", 13.333333) * height / width <= 56:
        raise ValueError("Calculated slide height must be between 1 and 56 inches")
    slide_ids, warnings = set(), []
    for slide in scene["slides"]:
        if slide["id"] in slide_ids:
            raise ValueError(f"Duplicate slide id: {slide['id']}")
        slide_ids.add(slide["id"])
        if slide.get("source_image"):
            asset_path(base, slide["source_image"])
        ids = set()
        for e in walk(slide["elements"]):
            label = f"{slide['id']}/{e['id']}"
            if e["id"] in ids:
                raise ValueError(f"Duplicate element id: {label}")
            ids.add(e["id"])
            kind = e["type"]
            if kind == "group":
                continue
            if kind == "line":
                if max(e["x1"], e["x2"]) > width or max(e["y1"], e["y2"]) > height:
                    raise ValueError(f"Line outside canvas: {label}")
                if (e["x1"], e["y1"]) == (e["x2"], e["y2"]):
                    raise ValueError(f"Zero-length line: {label}")
            elif e["x"] + e["w"] > width + 1e-6 or e["y"] + e["h"] > height + 1e-6:
                raise ValueError(f"Element outside canvas: {label}")
            if e.get("confidence", 1) < 0.85:
                warnings.append(
                    f"{label}: low-confidence reconstruction; verify source"
                )
            if e.get("rotation", 0):
                warnings.append(f"{label}: rotated extents require rendered review")
            if kind == "image":
                path = asset_path(base, e["path"])
                with Image.open(path) as im:
                    if im.format not in ("PNG", "JPEG"):
                        raise ValueError(f"Use PNG or JPEG assets: {label}")
                    im.verify()
                if (
                    e.get("role") in ("background", "reference")
                    or e["w"] * e["h"] > 0.8 * width * height
                ):
                    warnings.append(
                        f"{label}: large/background raster; check for baked-in elements"
                    )
            if kind == "table":
                cols = len(e["rows"][0])
                if any(len(row) != cols for row in e["rows"]):
                    raise ValueError(f"Ragged table: {label}")
                if "column_widths" in e and len(e["column_widths"]) != cols:
                    raise ValueError(f"Table column widths mismatch: {label}")
            if kind == "shape" and "corner_radius" in e and e["shape"] != "roundRect":
                raise ValueError(f"Corner radius requires roundRect: {label}")
            if kind == "chart":
                if any(len(s["values"]) != len(e["categories"]) for s in e["series"]):
                    raise ValueError(f"Chart categories/values mismatch: {label}")
                axis_options = (
                    "value_axis_min",
                    "value_axis_max",
                    "major_gridlines",
                    "major_gridline_color",
                    "tick_label_color",
                    "category_axis_visible",
                    "value_axis_visible",
                    "category_reverse_order",
                )
                if e["chart_type"] in ("pie", "doughnut") and any(
                    option in e for option in axis_options
                ):
                    raise ValueError(f"Pie/doughnut has no axes: {label}")
                if (
                    "value_axis_min" in e
                    and "value_axis_max" in e
                    and e["value_axis_min"] >= e["value_axis_max"]
                ):
                    raise ValueError(
                        f"Chart value axis minimum must be below maximum: {label}"
                    )
                if e.get("major_gridlines") is False and "major_gridline_color" in e:
                    raise ValueError(f"Hidden chart gridlines cannot have a color: {label}")
                if "data_label_color" in e and not e.get("data_labels", False):
                    raise ValueError(f"Chart data label color requires data_labels: {label}")
                if any(key in e for key in ("data_label_position", "data_label_font_size")) and not e.get("data_labels", False):
                    raise ValueError(f"Chart label styling requires data_labels: {label}")
                if "gap_width" in e and e["chart_type"] not in ("bar", "column"):
                    raise ValueError(f"Gap width requires bar/column: {label}")
                if "hole_size" in e and e["chart_type"] != "doughnut":
                    raise ValueError(f"Hole size requires doughnut: {label}")
                if "first_slice_angle" in e and e["chart_type"] not in ("pie", "doughnut"):
                    raise ValueError(f"Slice angle requires pie/doughnut: {label}")
                if "plot_layout" in e:
                    layout = e["plot_layout"]
                    if layout["x"] + layout["w"] > 1 + 1e-6 or layout["y"] + layout["h"] > 1 + 1e-6:
                        raise ValueError(f"Plot layout outside chart: {label}")
                for series in e["series"]:
                    if "point_colors" in series and len(series["point_colors"]) != len(e["categories"]):
                        raise ValueError(f"Point colors/categories mismatch: {label}")
                    if "invert_if_negative" in series and e["chart_type"] not in ("bar", "column"):
                        raise ValueError(f"Negative fill requires bar/column: {label}")
                if e["chart_type"] in ("pie", "doughnut") and (
                    len(e["series"]) != 1
                    or any(v < 0 for v in e["series"][0]["values"])
                    or sum(e["series"][0]["values"]) <= 0
                ):
                    raise ValueError(
                        f"Pie/doughnut requires one nonnegative, nonzero series: {label}"
                    )
    return warnings


def load_scene(path: Path):
    scene = read_json(path)
    warnings = validate_scene(scene, path.resolve().parent)
    return scene, warnings
