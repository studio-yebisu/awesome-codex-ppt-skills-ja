#!/usr/bin/env python3
"""Crop specified regions and apply supplied masks; this is not an OCR/segmentation model."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

from json_io import read_json
from PIL import Image, ImageChops, ImageOps
from scene import asset_path


def extract(spec_path: Path, output_dir: Path) -> dict:
    spec_path, output_dir = spec_path.resolve(), output_dir.resolve()
    spec = read_json(spec_path)
    base = spec_path.parent
    source = asset_path(base, spec["source"])
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert("RGBA")
    regions = spec.get("regions")
    if not isinstance(regions, list) or not regions:
        raise ValueError("regions must be a non-empty list")
    prepared, ids = [], set()
    inputs = {source, spec_path}
    for region in regions:
        eid = region["id"]
        if (
            not isinstance(eid, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", eid)
            or eid.casefold() in ids
        ):
            raise ValueError("Region IDs must be unique portable filenames")
        ids.add(eid.casefold())
        box = region["box"]
        if len(box) != 4 or any(
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not math.isfinite(v)
            for v in box
        ):
            raise ValueError(f"{eid}: box must be finite [x, y, width, height] pixels")
        x, y, w, h = box
        if (
            min(x, y) < 0
            or min(w, h) <= 0
            or x + w > image.width
            or y + h > image.height
        ):
            raise ValueError(f"{eid}: crop outside source image")
        actual = (math.floor(x), math.floor(y), math.ceil(x + w), math.ceil(y + h))
        cropped = image.crop(actual)
        mask_path = None
        if region.get("mask"):
            mask_path = asset_path(base, region["mask"])
            inputs.add(mask_path)
            with Image.open(mask_path) as opened:
                mask = ImageOps.exif_transpose(opened).convert("L")
            if mask.size != image.size:
                raise ValueError(f"{eid}: mask must match full source dimensions")
            cropped.putalpha(
                ImageChops.multiply(cropped.getchannel("A"), mask.crop(actual))
            )
        target = output_dir / f"{eid}.png"
        prepared.append(
            (
                target,
                cropped,
                {
                    "id": eid,
                    "path": target.name,
                    "source_box": [
                        actual[0],
                        actual[1],
                        actual[2] - actual[0],
                        actual[3] - actual[1],
                    ],
                    "mask": region.get("mask"),
                    "method": "masked-crop" if mask_path else "crop",
                    "source": spec["source"],
                    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                },
            )
        )
    manifest_path = output_dir / "assets.json"
    targets = [p[0] for p in prepared] + [manifest_path]
    if any(p in inputs or p.exists() for p in targets):
        raise ValueError(
            "Extraction output exists or overlaps input; choose a fresh output directory"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for target, cropped, record in prepared:
        cropped.save(target, "PNG")
        record["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        record["has_transparency"] = cropped.getchannel("A").getextrema()[0] < 255
        records.append(record)
    report = {
        "source_size": list(image.size),
        "assets": records,
        "note": "Crops do not remove occluders or reconstruct hidden pixels. Inspect every asset.",
    }
    manifest_path.write_text(
        json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    try:
        report = extract(args.spec, args.output_dir)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, f"extract_assets: {error}\n")
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
