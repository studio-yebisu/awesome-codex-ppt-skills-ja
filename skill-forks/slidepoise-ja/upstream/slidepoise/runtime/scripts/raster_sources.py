"""File and canvas facts for raster artwork. These are not visual judgements."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

from PIL import Image


def image_facts(path: Path) -> dict:
    with Image.open(path) as source:
        source.load()
        alpha = source.convert("RGBA").getchannel("A")
        histogram = alpha.histogram()
        bounds = alpha.getbbox()
        return {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "canvas_dimensions_px": list(source.size),
            "alpha": {
                "transparent_pixels": histogram[0],
                "partial_pixels": sum(histogram[1:255]),
                "opaque_pixels": histogram[255],
                "visible_bbox_px": (
                    [bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1]] if bounds else None
                ),
            },
        }


def validate_background(facts: dict, background: str) -> None:
    if background not in {"preserve", "transparent"}:
        raise ValueError("Raster background must be preserve or transparent")
    if facts["alpha"]["visible_bbox_px"] is None:
        raise ValueError("Raster artwork is fully transparent")
    if background == "transparent" and facts["alpha"]["transparent_pixels"] == 0:
        raise ValueError(
            "Transparent artwork requires actual transparent pixels. A solid image or painted checkerboard cannot be used."
        )


def validate_canvas(dimensions: list, expected: list) -> None:
    if (
        len(dimensions) != 2
        or len(expected) != 2
        or any(
            isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0
            for v in [*dimensions, *expected]
        )
    ):
        raise ValueError("Raster canvas dimensions must be positive finite numbers")
    # Allow only whole-pixel rounding of a uniform scale. Never squeeze artwork.
    w, h = dimensions
    ew, eh = expected
    if abs(w * eh - h * ew) > max(ew, eh):
        raise ValueError(
            "Returned raster canvas changed aspect ratio. Inspect its placement and explicitly select a matching canvas crop before applying it."
        )


def validate_source(path: Path, contract: dict) -> dict:
    facts = image_facts(path)
    if facts["sha256"] != contract.get("sha256"):
        raise ValueError("Raster source changed after inspection")
    if facts["canvas_dimensions_px"] != contract.get("canvas_dimensions_px"):
        raise ValueError("Raster source canvas does not match its recorded dimensions")
    validate_background(facts, contract.get("background", "preserve"))
    return facts


def safe_entity_id(value: str) -> str:
    if not value or value in {".", ".."} or any(c in value for c in "/\\\0"):
        raise ValueError("Entity ID must be a safe filename")
    return value
