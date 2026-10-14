#!/usr/bin/env python3
"""Prepare individual illustration sources and review contact sheets."""

from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from raster_decisions import illustration_decisions

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime" / "scripts"))
from raster_sources import image_facts, safe_entity_id


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def checked_crop_box(box, width, height):
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or int(v) != v for v in box):
        raise ValueError("Illustration crop coordinates must be finite whole pixels")
    x, y, w, h = map(int, box)
    if min(x, y) < 0 or min(w, h) <= 0 or x + w > width or y + h > height:
        raise ValueError("Illustration crop must lie inside the source image")
    return [x, y, w, h]


def fit_slot(cell, ratio):
    x, y, w, h = cell
    fw = min(w, h * ratio)
    fh = fw / ratio
    return [round(x + (w - fw) / 2), round(y + (h - fh) / 2), round(fw), round(fh)]


def choose_layout(ratios, W, H, margin, gutter):
    n = len(ratios)
    best = None
    for cols in range(1, min(4, n) + 1):
        rows = math.ceil(n / cols)
        cell_w = (W - 2 * margin - (cols - 1) * gutter) / cols
        cell_h = (H - 2 * margin - (rows - 1) * gutter) / rows
        if cell_w <= 1 or cell_h <= 1:
            continue
        slots = []
        area = 0.0
        for i, r in enumerate(ratios):
            row = i // cols
            col = i % cols
            cell = [margin + col * (cell_w + gutter), margin + row * (cell_h + gutter), cell_w, cell_h]
            slot = fit_slot(cell, max(0.05, float(r)))
            slots.append(slot)
            area += slot[2] * slot[3]
        score = area - rows * cols * 0.01
        if best is None or score > best[0]:
            best = (score, slots, cols, rows)
    if best is None:
        raise ValueError("Unable to lay out illustration board")
    return best[1], best[2], best[3]


def font(size=24, bold=False):
    candidates = [
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
        Path(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            if bold
            else "/System/Library/Fonts/Supplemental/Arial.ttf"
        ),
    ]
    for p in candidates:
        if p.is_file():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", type=Path, required=True)
    ap.add_argument("--semantic-map", type=Path, required=True)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--board", type=Path, required=True)
    ap.add_argument("--review-board", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--brief", type=Path, required=True)
    args = ap.parse_args()
    semantic = load(args.semantic_map)
    config = load(args.config)
    refcfg = (config.get("generation", {}) or {}).get("illustration_refinement", {}) or {}
    W, H = [int(v) for v in refcfg.get("board_max_size_px", [2048, 2048])]
    margin = int(refcfg.get("board_outer_margin_px", 80))
    gutter = int(refcfg.get("board_gutter_px", 72))
    source = Image.open(args.image).convert("RGBA")
    sw, sh = source.size
    candidates = []
    for e, decision in illustration_decisions(semantic):
        if decision["action"] == "refine":
            if e.get("geometry_policy") != "agent_logical":
                raise ValueError(f"{e.get('id')}: illustration registration requires an agent_logical canvas")
            box = e.get("bbox_hint") or e.get("bbox")
            if not (isinstance(box, list) and len(box) == 4):
                raise SystemExit(f"{e.get('id')}: novel illustration missing bbox_hint")
            safe_entity_id(str(e["id"]))
            box = checked_crop_box(box, sw, sh)
            candidates.append((e, box))
    identifiers = [str(entity["id"]) for entity, _ in candidates]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Illustration candidates contain duplicate entity IDs")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "source-crops").mkdir(exist_ok=True)
    if not candidates:
        manifest = {
            "source_image": str(args.image.resolve()),
            "source_image_sha256": image_facts(args.image)["sha256"],
            "board_dimensions_px": [W, H],
            "candidate_count": 0,
            "items": [],
        }
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, indent=2) + "\n")
        args.brief.parent.mkdir(parents=True, exist_ok=True)
        args.brief.write_text("# No novel illustration refinement candidates\n")
        print(json.dumps({"candidate_count": 0, "manifest": str(args.manifest.resolve())}, indent=2))
        return
    ratios = [b[2] / b[3] for _, b in candidates]
    slots, cols, rows = choose_layout(ratios, W, H, margin, gutter)
    board = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    items = []
    for i, ((e, box), slot) in enumerate(zip(candidates, slots), start=1):
        x, y, bw, bh = box
        crop = source.crop((x, y, x + bw, y + bh))
        crop_path = args.output_dir / "source-crops" / f"{e['id']}.png"
        crop.save(crop_path)
        sx, sy, ssw, ssh = slot
        resized = crop.resize((ssw, ssh), Image.Resampling.LANCZOS)
        board.alpha_composite(resized, (sx, sy))
        background = e["raster_decision"].get("background", "preserve")
        items.append(
            {
                "entity_id": e["id"],
                "label": f"I{i:02d}",
                "semantic_role": e.get("role"),
                "source_bbox_px": box,
                "source_aspect_ratio": round(bw / bh, 6),
                "source_crop": str(crop_path.resolve()),
                "source_crop_sha256": image_facts(crop_path)["sha256"],
                "background": background,
                "board_slot_px": slot,
                "board_slot_normalized": [round(sx / W, 8), round(sy / H, 8), round(ssw / W, 8), round(ssh / H, 8)],
            }
        )
    args.board.parent.mkdir(parents=True, exist_ok=True)
    board.save(args.board)
    review = Image.new("RGBA", board.size, "white")
    review.alpha_composite(board)
    draw = ImageDraw.Draw(review)
    f = font(24, True)
    for item in items:
        x, y, w, h = item["board_slot_px"]
        draw.rectangle((x, y, x + w, y + h), outline=(230, 70, 20), width=3)
        draw.rectangle((x, y, x + 64, y + 34), fill="white")
        draw.text((x + 6, y + 4), item["label"], fill="black", font=f)
    args.review_board.parent.mkdir(parents=True, exist_ok=True)
    review.save(args.review_board)
    manifest = {
        "source_image": str(args.image.resolve()),
        "source_image_sha256": image_facts(args.image)["sha256"],
        "board_dimensions_px": [W, H],
        "layout": {"columns": cols, "rows": rows, "outer_margin_px": margin, "gutter_px": gutter},
        "candidate_count": len(items),
        "items": items,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    profile = config.get("resolved_profile", {}) or {}
    av = (profile.get("hard_rules", {}) or {}).get("asset_vocabulary", {}) or {}
    novel = av.get("novel_illustrations", {}) or {}
    brief = [
        "# Illustration edits",
        "",
        "Edit each source crop separately. The boards are contact sheets for review.",
        "Preserve the approved artwork, intrinsic lettering and its position within the source canvas.",
        "Keep the canvas aspect ratio and existing margins. Do not recenter or enlarge the subject.",
        "Inspect each result at its intended slide size before applying it.",
        "",
        "## Selected artwork",
    ]
    for item in items:
        brief += [
            "",
            f"### {item['entity_id']}",
            f"Source file `{item['source_crop']}`",
            f"Canvas {item['source_bbox_px'][2]} × {item['source_bbox_px'][3]} pixels.",
        ]
        if item["background"] == "transparent":
            brief += [
                "Remove only the slide backdrop. Keep intrinsic paper, photographic backgrounds and soft shadows belonging to the artwork.",
                "Request a PNG or WebP with genuine alpha transparency. Keep partially transparent edges and shadows.",
                "Verify the returned file. A painted checkerboard or an opaque image does not satisfy this request.",
            ]
        else:
            brief += ["Preserve the source background behavior, including any existing transparency."]
    brief += [
        "",
        "## Visual direction",
        novel.get("guidance", ""),
        *[str(v) for v in profile.get("visual_principles", [])],
    ]
    args.brief.parent.mkdir(parents=True, exist_ok=True)
    args.brief.write_text("\n".join(brief) + "\n", encoding="utf-8")
    # Each edit is a separate portable request, so tools and manual exchanges use
    # the same source crop and instructions without attaching unrelated artwork.
    from prepare_generation import file_binding
    import hashlib
    for item in items:
        source = Path(item["source_crop"])
        prompt = "\n".join([
            "Edit the attached illustration while preserving its identity and intrinsic lettering.",
            "Keep the canvas aspect ratio, original margins and placement of the subject.",
            ("Remove only the slide backdrop. Preserve paper, photographic content and soft shadows belonging to the artwork. Return a PNG or WebP with genuine alpha transparency."
             if item["background"] == "transparent" else "Preserve the source background and any existing transparency."),
            novel.get("guidance", ""), *[str(v) for v in profile.get("visual_principles", [])],
        ]) + "\n"
        prompt_path = source.with_suffix('.edit.txt')
        prompt_path.write_text(prompt, encoding='utf-8')
        request = {"schema_version": "1.0", "purpose": "host_illustration_edit_request", "prompt": prompt,
                   "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                   "canvas": {"dimensions_px": item["source_bbox_px"][2:]}, "background": item["background"],
                   "reference_images": [{"id": item["entity_id"], "purpose": "Original illustration to edit", **file_binding(source)}],
                   "input_bindings": {"config": file_binding(args.config), "manifest": file_binding(args.manifest),
                                      "brief": file_binding(prompt_path), "source": file_binding(args.image)}}
        source.with_suffix('.request.json').write_text(json.dumps(request, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(
        json.dumps(
            {
                "candidate_count": len(items),
                "board": str(args.board.resolve()),
                "review_board": str(args.review_board.resolve()),
                "manifest": str(args.manifest.resolve()),
                "brief": str(args.brief.resolve()),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
