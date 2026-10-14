"""Resolve one substantive canvas from the authored full slide and master frame."""
from __future__ import annotations

import math


def pixel_integer(value, field, *, minimum=0):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value != int(value) or value < minimum:
        raise ValueError(f"{field} must be an integer of at least {minimum} pixels")
    return int(value)


def derive_canvas(design: dict, *, fallback_dimensions=None) -> dict:
    full = design.get("full_slide_px", fallback_dimensions)
    if not isinstance(full, (list, tuple)) or len(full) != 2:
        raise ValueError("design.full_slide_px requires width and height")
    width, height = [pixel_integer(value, "design.full_slide_px", minimum=1) for value in full]
    frame = design.get("frame", {})
    if not isinstance(frame, dict):
        raise ValueError("design.frame must be an object")
    heights = {}
    for area in ("header", "footer"):
        settings = frame.get(area, {})
        if not isinstance(settings, dict):
            raise ValueError(f"design.frame.{area} must be an object")
        enabled = settings.get("enabled", True)
        if not isinstance(enabled, bool):
            raise ValueError(f"design.frame.{area}.enabled must be boolean")
        pixels = pixel_integer(settings.get("height_px", 0), f"design.frame.{area}.height_px")
        heights[area] = pixels if enabled else 0
    substantive_height = height - heights["header"] - heights["footer"]
    if substantive_height <= 0:
        raise ValueError("header/footer heights leave no substantive generation region")
    return {"generation_region_px": [width, substantive_height], "generation_offset_y_px": heights["header"],
            "generation_aspect_ratio": round(width / substantive_height, 6),
            "header_height_px": heights["header"], "footer_height_px": heights["footer"]}


def validate_derived_canvas(config: dict, *, required=False) -> dict:
    expected = derive_canvas(config.get("design", {}))
    derived = config.get("derived")
    if derived is None and not required:
        return expected
    if not isinstance(derived, dict):
        raise ValueError("Resolved config.derived must contain the derived canvas")
    for key, value in expected.items():
        if key not in derived or derived[key] != value:
            raise ValueError(f"Resolved config.derived.{key} disagrees with design.frame. Rerun resolve_config.py")
    return expected


def validate_source_aspect(source_dimensions, region_dimensions):
    """Allow one source-pixel rounding error, never a different canvas shape."""
    width, height = [pixel_integer(value, "measured source dimensions", minimum=1) for value in source_dimensions]
    expected_height = width * region_dimensions[1] / region_dimensions[0]
    if abs(height - expected_height) > 1:
        raise ValueError("Accepted source aspect ratio differs from the substantive generation canvas. "
                         "Use normalize_generation_canvas.py with a host-reviewed crop or regenerate before measurement. "
                         "Reconstruction cannot stretch a full-slide image into the content-only region.")


def reconstruction_geometry(design, source_dimensions):
    source = [pixel_integer(value, "measured source dimensions", minimum=1) for value in source_dimensions]
    canvas = derive_canvas(design, fallback_dimensions=source)
    region = canvas["generation_region_px"]
    validate_source_aspect(source, region)
    return {"full_slide_dimensions_px": list(design.get("full_slide_px", source)),
            "generation_region": {"offset_y_px": canvas["generation_offset_y_px"], "dimensions_px": region},
            "coordinate_transform_to_full_slide": {"scale_xy": [region[0] / source[0], region[1] / source[1]],
                                                   "translation_px": [0, canvas["generation_offset_y_px"]]}}
