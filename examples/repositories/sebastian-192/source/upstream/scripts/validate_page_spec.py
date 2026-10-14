#!/usr/bin/env python3
"""Validate the semantic page specification used between image and Scene stages."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from json_io import read_json
from jsonschema import Draft202012Validator
from PIL import Image, ImageOps

SCHEMA = Path(__file__).resolve().parents[1] / "references" / "page-spec.schema.json"


def _finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Page Spec numbers must be finite")
    if isinstance(value, dict):
        for item in value.values():
            _finite(item)
    if isinstance(value, list):
        for item in value:
            _finite(item)


def _relative_path(base: Path, value: str) -> Path:
    path = Path(value)
    root = base.resolve()
    resolved = (root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(root):
        raise ValueError(f"Image path must stay inside Page Spec directory: {value}")
    return resolved


def validate_page_spec(
    spec: dict, base: Path, require_images: bool = False, strict: bool = False
) -> dict:
    _finite(spec)
    schema = read_json(SCHEMA)
    errors = list(Draft202012Validator(schema).iter_errors(spec))
    if errors:
        error = errors[0]
        location = "/".join(str(p) for p in error.absolute_path) or "root"
        raise ValueError(f"Page Spec schema at {location}: {error.message}")

    for reference in spec["style"].get("tokens", {}).get("reference_images", []):
        path = _relative_path(base, reference)
        if not path.is_file():
            raise ValueError(f"Missing style reference image: {reference}")
        with Image.open(path) as image:
            image.verify()

    width, height = spec["canvas"]["width"], spec["canvas"]["height"]
    slide_ids, page_numbers, element_count, unresolved = set(), set(), 0, 0
    image_paths = set()
    for expected_page, slide in enumerate(spec["slides"], start=1):
        if slide["id"] in slide_ids:
            raise ValueError(f"Duplicate slide id: {slide['id']}")
        slide_ids.add(slide["id"])
        page_number = slide["page_number"]
        if page_number in page_numbers:
            raise ValueError(f"Duplicate page number: {page_number}")
        page_numbers.add(page_number)
        if page_number != expected_page:
            raise ValueError(
                f"Page numbers must be consecutive and ordered; expected {expected_page}, "
                f"got {page_number}"
            )

        image_path = _relative_path(base, slide["image_file"])
        if image_path in image_paths:
            raise ValueError(f"Duplicate image path: {slide['image_file']}")
        image_paths.add(image_path)
        if require_images:
            if slide["image_status"] != "approved":
                raise ValueError(f"Slide not approved: {slide['id']}")
            if not image_path.is_file():
                raise ValueError(f"Missing approved slide image: {slide['image_file']}")
            with Image.open(image_path) as image:
                if image.format not in ("PNG", "JPEG"):
                    raise ValueError(
                        f"Approved slide image must be PNG or JPEG: {slide['image_file']}"
                    )
                image.verify()
            with Image.open(image_path) as image:
                image_width, image_height = ImageOps.exif_transpose(image).size
                # Allow one pixel of rounding in either dimension, not a crop.
                ratio = width / height
                if abs(image_width - image_height * ratio) > max(1.0, ratio) + 1e-6:
                    raise ValueError(f"Image aspect ratio differs from canvas: {slide['image_file']}")

        element_ids = set()
        for element in slide["elements"]:
            element_count += 1
            if element["confirmation_status"] == "unresolved":
                unresolved += 1
            if element["id"] in element_ids:
                raise ValueError(
                    f"Duplicate element id: {slide['id']}/{element['id']}"
                )
            element_ids.add(element["id"])
            if "bbox_hint" in element:
                x, y, w, h = element["bbox_hint"]
                if x + w > width + 1e-6 or y + h > height + 1e-6:
                    raise ValueError(
                        f"bbox_hint outside canvas: {slide['id']}/{element['id']}"
                    )

    if strict and unresolved:
        raise ValueError(f"Page Spec contains {unresolved} unresolved elements")
    return {
        "slides": len(spec["slides"]),
        "elements": element_count,
        "unresolved": unresolved,
    }


def load_page_spec(path: Path, require_images: bool = False, strict: bool = False):
    spec = read_json(path)
    result = validate_page_spec(spec, path.resolve().parent, require_images, strict)
    return spec, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_spec", type=Path)
    parser.add_argument("--require-images", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    _, result = load_page_spec(args.page_spec, args.require_images, args.strict)
    print(
        f"Page Spec valid: {result['slides']} slides, "
        f"{result['elements']} semantic elements, {result['unresolved']} unresolved"
    )


if __name__ == "__main__":
    main()
