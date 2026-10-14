#!/usr/bin/env python3
"""Register one returned illustration while preserving its full canvas and alpha."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import sys

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime" / "scripts"))
from raster_sources import image_facts, safe_entity_id, validate_background, validate_canvas


def extract(
    image_path: Path, manifest: dict, entity_id: str | None, output_dir: Path, crop_box: list[int] | None = None
) -> dict:
    items = manifest.get("items", [])
    ids = [str(item["entity_id"]) for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("Illustration manifest contains duplicate entity IDs")
    if entity_id is None and len(items) == 1:
        entity_id = ids[0]
    if entity_id not in ids:
        raise ValueError("Select one illustration with --entity-id. Generate each source crop separately.")
    item = items[ids.index(entity_id)]
    safe_entity_id(entity_id)
    background = item.get("background", "preserve")
    facts = image_facts(image_path)
    validate_background(facts, background)
    with Image.open(image_path) as source:
        image = source.convert("RGBA")
    if crop_box is not None:
        x, y, w, h = crop_box
        if min(x, y) < 0 or min(w, h) <= 0 or x + w > image.width or y + h > image.height:
            raise ValueError("Returned canvas crop must be inside the image")
        image = image.crop((x, y, x + w, y + h))
    else:
        crop_box = [0, 0, image.width, image.height]
    validate_canvas(list(image.size), item["source_bbox_px"][2:])
    alpha = image.getchannel("A")
    if alpha.getbbox() is None or (background == "transparent" and alpha.getextrema()[0] != 0):
        raise ValueError("Selected canvas does not contain the required visible artwork and transparency")
    output_dir.mkdir(parents=True, exist_ok=True)
    encoded = io.BytesIO()
    image.save(encoded, format="PNG")
    payload = encoded.getvalue()
    digest = hashlib.sha256(payload).hexdigest()
    output = output_dir / f"{entity_id}-{digest[:12]}.png"
    if output.resolve() == image_path.resolve():
        raise ValueError("Keep the returned image unchanged. Use a separate output directory.")
    output.write_bytes(payload)
    previews = {}
    for name, color in (("light", "#FAF8F4"), ("dark", "#202630")):
        preview = Image.new("RGBA", image.size, color)
        preview.alpha_composite(image)
        preview_path = output.with_name(f"{output.stem}.on-{name}.png")
        preview.convert("RGB").save(preview_path)
        previews[name] = str(preview_path.resolve())
    contract = {
        **image_facts(output),
        "background": background,
        "source_bbox_px": item["source_bbox_px"],
        "source_image_sha256": manifest["source_image_sha256"],
        "source_crop_sha256": item["source_crop_sha256"],
        "returned_image_sha256": facts["sha256"],
        "output_crop_px": crop_box,
    }
    return {"items": [{"entity_id": entity_id, "refined_raster": str(output.resolve()), "raster_source": contract, "review_previews": previews}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--entity-id")
    parser.add_argument("--crop", type=int, nargs=4, metavar=("X", "Y", "WIDTH", "HEIGHT"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    args = parser.parse_args()
    mapping = extract(args.image, json.loads(args.manifest.read_text()), args.entity_id, args.output_dir, args.crop)
    args.mapping.parent.mkdir(parents=True, exist_ok=True)
    args.mapping.write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(mapping, indent=2))


if __name__ == "__main__":
    main()
