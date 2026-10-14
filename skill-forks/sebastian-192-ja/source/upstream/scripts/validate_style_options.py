#!/usr/bin/env python3
"""Validate the four current landscape slide-sorter candidates before selection."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from json_io import read_json
from PIL import Image, ImageOps


def validate_style_options(spec: dict, base: Path) -> dict:
    if not isinstance(spec, dict) or spec.get("version") != "1.0":
        raise ValueError("Style options must be a version 1.0 object")
    total = spec.get("total_pages")
    pages = spec.get("representative_pages")
    if type(total) is not int or total < 1:
        raise ValueError("total_pages must be a positive integer")
    if (
        not isinstance(pages, list)
        or not pages
        or any(not isinstance(page, str) or not page.strip() for page in pages)
        or len(set(pages)) != len(pages)
    ):
        raise ValueError("representative_pages must contain unique, nonempty slide IDs")
    if (total <= 8 and len(pages) != total) or (total > 8 and not 6 <= len(pages) <= 8):
        raise ValueError("Show every page up to 8 pages; otherwise use 6-8 representative pages")
    aspect = spec.get("overview_aspect_ratio", [16, 9])
    if (
        not isinstance(aspect, list)
        or len(aspect) != 2
        or any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in aspect)
        or aspect[0] <= aspect[1]
    ):
        raise ValueError("overview_aspect_ratio must describe a landscape canvas")
    ratio = aspect[0] / aspect[1]
    options = spec.get("options")
    if not isinstance(options, list) or len(options) != 4:
        raise ValueError("Exactly four current options are required; exclude drafts and superseded revisions")
    paths, hashes, results = set(), set(), []
    root = base.resolve()
    for number, option in enumerate(options, 1):
        if not isinstance(option, dict) or type(option.get("option")) is not int or option["option"] != number:
            raise ValueError("Options must be numbered 1, 2, 3, 4 in order, without duplicates")
        if option.get("slide_ids") != pages:
            raise ValueError(f"Option {number}: slide IDs/order differ from the representative pages")
        value = option.get("file")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Option {number}: missing image file")
        path = Path(value)
        resolved = (root / path).resolve()
        if path.is_absolute() or not resolved.is_relative_to(root):
            raise ValueError(f"Option {number}: image must stay inside the options directory")
        if resolved in paths:
            raise ValueError(f"Option {number}: duplicate image path")
        paths.add(resolved)
        if not resolved.is_file():
            raise ValueError(f"Option {number}: missing image {value}")
        with Image.open(resolved) as image:
            if image.format not in ("PNG", "JPEG"):
                raise ValueError(f"Option {number}: use a PNG or JPEG overview")
            image.verify()
        with Image.open(resolved) as image:
            image = ImageOps.exif_transpose(image).convert("RGBA")
            width, height = image.size
            if width <= height or abs(width - height * ratio) > max(1.0, ratio) + 1e-6:
                raise ValueError(f"Option {number}: expected a landscape overview, not a vertical slide strip or wrong canvas ratio")
            digest = hashlib.sha256(str(image.size).encode() + image.tobytes()).hexdigest()
        if digest in hashes:
            raise ValueError(f"Option {number}: duplicate image content is not a distinct option")
        hashes.add(digest)
        results.append({"option": number, "file": value, "pixels": [width, height]})
    return {
        "options": results,
        "representative_pages": pages,
        "visual_review": "required: inspect thumbnail grid, page coverage, content and visual differences",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("choices", type=Path)
    args = parser.parse_args()
    try:
        spec = read_json(args.choices)
        result = validate_style_options(spec, args.choices.resolve().parent)
    except (ValueError, OSError) as error:
        parser.exit(2, f"validate_style_options: {error}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
