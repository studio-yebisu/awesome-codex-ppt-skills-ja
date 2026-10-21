#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageChops, ImageStat


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
GENERATED_IMAGE_BACKENDS = {"codex_builtin_imagegen"}


def read_json(path: Path | None, fallback: object) -> object:
    if not path or not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8-sig"))


def slide_pngs(preview_dir: Path | None) -> list[Path]:
    if not preview_dir or not preview_dir.exists():
        return []
    return sorted(p for p in preview_dir.glob("slide_*.png") if p.is_file())


def image_hash(path: Path) -> str:
    img = Image.open(path).convert("RGB").resize((64, 36), Image.Resampling.LANCZOS)
    return hashlib.sha256(img.tobytes()).hexdigest()


def region_activity(img: Image.Image, box: tuple[int, int, int, int]) -> float:
    region = img.crop(box).convert("RGB")
    if region.width <= 0 or region.height <= 0:
        return 0.0
    quantized = region.quantize(colors=12)
    colors = quantized.getcolors(maxcolors=region.width * region.height) or []
    if not colors:
        return 0.0
    dominant = max(count for count, _ in colors)
    palette_activity = 1.0 - dominant / float(region.width * region.height)
    edges = ImageChops.difference(region, Image.new("RGB", region.size, region.resize((1, 1)).getpixel((0, 0)))).convert("L")
    edge_stat = ImageStat.Stat(edges)
    edge_activity = min(1.0, edge_stat.mean[0] / 48.0)
    return round(max(palette_activity, edge_activity), 4)


def visual_stats(paths: list[Path]) -> dict:
    if not paths:
        return {"available": False}
    hashes = [image_hash(p) for p in paths]
    lumas = []
    bbox_ratios = []
    color_counts = []
    balance = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        small = img.resize((320, 180), Image.Resampling.LANCZOS)
        left_activity = region_activity(small, (0, 0, 198, 180))
        right_activity = region_activity(small, (198, 0, 320, 180))
        balance.append(
            {
                "slide_png": str(path),
                "left_activity": left_activity,
                "right_activity": right_activity,
                "right_underused": right_activity < 0.035 and left_activity > 0.08,
            }
        )
        stat = ImageStat.Stat(small.convert("L"))
        lumas.append(stat.mean[0])
        bg = Image.new("RGB", small.size, small.getpixel((0, 0)))
        diff = ImageChops.difference(small, bg).convert("L")
        bbox = diff.point(lambda v: 255 if v > 9 else 0).getbbox()
        if bbox:
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            bbox_ratios.append(area / (small.width * small.height))
        else:
            bbox_ratios.append(0)
        palette = small.quantize(colors=16)
        color_counts.append(len(palette.getcolors(maxcolors=512) or []))
    return {
        "available": True,
        "count": len(paths),
        "unique_hashes": len(set(hashes)),
        "avg_luminance": round(statistics.mean(lumas), 2),
        "avg_non_background_ratio": round(statistics.mean(bbox_ratios), 3),
        "avg_palette_count": round(statistics.mean(color_counts), 2),
        "region_balance": balance,
        "right_underused_count": sum(1 for item in balance if item["right_underused"]),
    }


def pptx_stats(path: Path | None) -> dict:
    if not path or not path.exists():
        return {"available": False}
    stats = {
        "available": True,
        "slide_count": 0,
        "text_runs": 0,
        "fonts": set(),
        "charts": 0,
        "pictures": 0,
        "round_rects": 0,
        "shapes_per_slide": [],
        "slide_xml_hashes": [],
        "texts": [],
    }
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            [n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=lambda n: int(re.search(r"slide(\d+)\.xml", n).group(1)),
        )
        stats["slide_count"] = len(slide_names)
        stats["charts"] = len([n for n in zf.namelist() if n.startswith("ppt/charts/chart") and n.endswith(".xml")])
        for name in slide_names:
            data = zf.read(name)
            stats["slide_xml_hashes"].append(hashlib.sha256(data).hexdigest())
            root = ET.fromstring(data)
            texts = root.findall(".//a:t", NS)
            text_values = [t.text for t in texts if t.text]
            stats["text_runs"] += len(text_values)
            stats["texts"].extend(text_values)
            stats["pictures"] += len(root.findall(".//p:pic", NS))
            stats["round_rects"] += data.count(b"roundRect")
            shape_count = data.count(b"<p:sp>") + data.count(b"<p:pic>") + data.count(b"<p:graphicFrame>")
            stats["shapes_per_slide"].append(shape_count)
            for latin in root.findall(".//a:latin", NS):
                typeface = latin.attrib.get("typeface")
                if typeface and not typeface.startswith("+"):
                    stats["fonts"].add(typeface)
            for ea in root.findall(".//a:ea", NS):
                typeface = ea.attrib.get("typeface")
                if typeface and not typeface.startswith("+"):
                    stats["fonts"].add(typeface)
    stats["fonts"] = sorted(stats["fonts"])
    return stats


def layout_stats(slides_plan: dict) -> dict:
    slides = slides_plan.get("slides", []) if isinstance(slides_plan, dict) else []
    layouts = [s.get("layout_archetype") or s.get("layout") or s.get("layout_family") or s.get("slide_type") for s in slides]
    layouts = [str(x) for x in layouts if x]
    max_run = 0
    current = None
    run = 0
    for layout in layouts:
        if layout == current:
            run += 1
        else:
            current = layout
            run = 1
        max_run = max(max_run, run)
    return {"layouts": layouts, "unique_layouts": len(set(layouts)), "max_consecutive": max_run}


def has_mandatory_generated_image(asset_plan: dict) -> bool:
    assets = asset_plan.get("assets") or asset_plan.get("slides") or []
    for item in assets:
        if (
            item.get("generation_required") is True
            and item.get("generation_backend") in GENERATED_IMAGE_BACKENDS
            and item.get("status") == "generated"
            and item.get("output_path")
            and Path(str(item.get("output_path"))).exists()
        ):
            return True
    return False


def generated_asset_relevance(asset_plan: dict, slides_plan: dict) -> dict:
    assets = asset_plan.get("assets") or asset_plan.get("slides") or []
    slides = slides_plan.get("slides", []) if isinstance(slides_plan, dict) else []
    slide_lookup = {s.get("slide_id"): s for s in slides}
    generated = []
    issues = []
    sources: dict[str, list[str]] = {}
    for item in assets:
        if not (
            item.get("generation_required") is True
            and item.get("generation_backend") in GENERATED_IMAGE_BACKENDS
            and item.get("status") == "generated"
            and item.get("output_path")
        ):
            continue
        sid = item.get("slide_id")
        generated.append(item)
        source = str(Path(str(item.get("output_path"))).resolve()) if item.get("output_path") else ""
        sources.setdefault(source, []).append(str(sid))
        binding = item.get("semantic_binding") or {}
        slide = slide_lookup.get(sid, {})
        title = str(binding.get("slide_title") or slide.get("title") or "").strip()
        core = str(binding.get("core_message") or slide.get("key_message") or slide.get("purpose") or "").strip()
        prompt_text = ""
        prompt_path = item.get("prompt_path")
        if prompt_path and Path(str(prompt_path)).exists():
            prompt_text = Path(str(prompt_path)).read_text(encoding="utf-8-sig", errors="ignore")
        generic_markers = [
            "mandatory generated-image gate",
            "deck-level image generation requirement",
            "Phase 3 mandatory",
            "seed generated asset",
            "reused for regression",
        ]
        required_fields = {
            "image_slot": item.get("image_slot"),
            "aspect_ratio": item.get("aspect_ratio"),
            "integration_treatment": item.get("integration_treatment"),
        }
        if binding.get("bound_to_slide") is not True:
            issues.append({"slide_id": sid, "reason": "missing bound_to_slide=true"})
        if not title or not core or not str(binding.get("visual_brief") or "").strip():
            issues.append({"slide_id": sid, "reason": "semantic binding incomplete"})
        for field, value in required_fields.items():
            if not str(value or "").strip():
                issues.append({"slide_id": sid, "reason": f"missing required visual brief field: {field}"})
        if str(item.get("asset_type") or "").lower() == "background" and str(item.get("visual_need") or "").lower() == "required":
            issues.append({"slide_id": sid, "reason": "required visual is declared as generic background"})
        if not prompt_text:
            issues.append({"slide_id": sid, "reason": "prompt file missing or empty"})
        elif any(marker.lower() in prompt_text.lower() for marker in generic_markers):
            issues.append({"slide_id": sid, "reason": "prompt is generic gate text"})
        else:
            title_hit = title and (title in prompt_text or title[: max(2, min(6, len(title)))] in prompt_text)
            core_hit = core and (core in prompt_text or core[: max(2, min(8, len(core)))] in prompt_text)
            if not (title_hit or core_hit):
                issues.append({"slide_id": sid, "reason": "prompt does not mention slide title/core message"})
    reused = {source: ids for source, ids in sources.items() if source and len(ids) > 1}
    for source, ids in reused.items():
        issues.append({"slide_id": ",".join(ids), "reason": f"same generated image reused: {source}"})
    return {"generated_count": len(generated), "issues": issues, "reused_sources": reused}


def score_deck(spec: dict, slides_plan: dict, pptx: dict, visual: dict, asset_plan: dict | None = None) -> tuple[dict, list[dict], list[str]]:
    phase3 = bool(spec.get("phase3_design_system") or spec.get("aesthetic_engine") or slides_plan.get("phase3_design_system"))
    layouts = layout_stats(slides_plan)
    slide_count = pptx.get("slide_count") or visual.get("count") or len(slides_plan.get("slides", []))
    dims = {
        "typography": 8.8 if phase3 else 6.4,
        "visual_hierarchy": 8.8 if phase3 else 6.2,
        "grid_and_alignment": 8.9 if phase3 else 6.0,
        "whitespace_and_density": 8.7 if phase3 else 6.1,
        "color_and_contrast": 8.8 if phase3 else 6.5,
        "layout_suitability": 8.8 if phase3 else 6.2,
        "image_integration": 8.5 if phase3 else 5.8,
        "chart_and_data_design": 8.8 if phase3 else 5.7,
        "cross_slide_consistency_and_rhythm": 8.8 if phase3 else 5.9,
        "originality_anti_ai_slop": 8.7 if phase3 else 5.8,
    }
    issues: list[dict] = []
    failure_modes: list[str] = []

    def issue(mode: str, severity: str, message: str, penalties: dict[str, float]) -> None:
        failure_modes.append(mode)
        issues.append({"mode": mode, "severity": severity, "message": message})
        for key, amount in penalties.items():
            dims[key] = max(0, dims[key] - amount)

    if not visual.get("available"):
        issue("render_missing", "severe", "No rendered slide PNGs were available for visual review.", {k: 4 for k in dims})
    elif visual.get("count", 0) != slide_count and slide_count:
        issue("render_count_mismatch", "major", "Rendered PNG count does not match deck slide count.", {"cross_slide_consistency_and_rhythm": 1.2, "grid_and_alignment": 0.8})

    if pptx.get("available"):
        fonts = pptx.get("fonts", [])
        if len(fonts) > 4:
            issue("typography_fallback", "major", f"Too many font families detected: {fonts}", {"typography": 1.4, "cross_slide_consistency_and_rhythm": 0.7})
        if pptx.get("text_runs", 0) == 0 and not spec.get("route") == "image_first":
            issue("missing_editable_text", "severe", "PPTX has no editable text runs.", {"typography": 2.6, "visual_hierarchy": 2.0})
        visible_text = "\n".join(str(t) for t in pptx.get("texts", []))
        internal_markers = [
            "PAGE-SPECIFIC VISUAL REQUIRED",
            "VISUAL MODEL",
            "EXPLANATION PANEL",
            "ACTION MODEL",
            "HTML DECK",
            "mandatory generated-image gate",
            "deck-level image generation requirement",
        ]
        leaked = [marker for marker in internal_markers if marker.lower() in visible_text.lower()]
        if leaked:
            issue(
                "internal_workflow_text_visible",
                "severe",
                f"Internal workflow labels are visible in slide body: {', '.join(leaked)}",
                {"visual_hierarchy": 2.0, "originality_anti_ai_slop": 2.0, "typography": 1.0},
            )
        if pptx.get("charts", 0) > 0 and not phase3:
            issue("default_chart", "major", "Native chart XML detected without Phase 3 chart treatment metadata.", {"chart_and_data_design": 2.2, "originality_anti_ai_slop": 1.0})
        avg_shapes = statistics.mean(pptx.get("shapes_per_slide") or [0])
        if pptx.get("round_rects", 0) >= max(10, slide_count * 4) and avg_shapes > 10:
            issue("card_soup", "major", "Many rounded rectangles and high shape counts suggest card soup.", {"layout_suitability": 1.6, "originality_anti_ai_slop": 1.6, "whitespace_and_density": 0.8})
        if spec.get("route") == "image_first" and pptx.get("text_runs", 0) < slide_count:
            issue("image_first_low_editability", "minor", "Image-first deck has limited editable text; acceptable only when declared.", {"typography": 0.8})

    if layouts["layouts"]:
        if layouts["max_consecutive"] > 2:
            issue("repetitive_layout", "major", f"Layout repeats {layouts['max_consecutive']} times consecutively.", {"cross_slide_consistency_and_rhythm": 1.5, "layout_suitability": 1.0})
        if slide_count >= 8 and layouts["unique_layouts"] < 5:
            issue("repetitive_layout", "major", "Deck uses too few layout archetypes for its length.", {"cross_slide_consistency_and_rhythm": 1.2})
    elif not phase3:
        issue("layout_plan_missing", "major", "Slides plan does not specify Phase 3 layout archetypes.", {"layout_suitability": 1.2, "grid_and_alignment": 1.0})

    if visual.get("available"):
        if visual.get("unique_hashes", 0) <= 1 and visual.get("count", 0) > 2:
            issue("weak_image_integration", "major", "Rendered pages are visually near-identical.", {"image_integration": 1.4, "cross_slide_consistency_and_rhythm": 1.2})
        ratio = visual.get("avg_non_background_ratio", 0)
        if ratio > 0.82:
            issue("overfill", "major", "Average non-background occupancy is high; pages may be crowded.", {"whitespace_and_density": 1.2, "visual_hierarchy": 0.7})
        if ratio < 0.18 and slide_count > 2:
            issue("underfill", "major", "Average occupancy is very low without clear intentional rhythm.", {"whitespace_and_density": 1.0, "visual_hierarchy": 0.7})
        if visual.get("avg_palette_count", 0) > 15.8 and not phase3:
            issue("gradient_slop", "minor", "High color variety without design-system metadata may indicate decorative slop.", {"color_and_contrast": 0.5, "originality_anti_ai_slop": 0.5})
        right_underused = visual.get("right_underused_count", 0)
        if right_underused >= max(1, slide_count // 3):
            pages = [
                str(i + 1)
                for i, item in enumerate(visual.get("region_balance", []))
                if item.get("right_underused")
            ]
            issue(
                "unintentional_right_blank",
                "major",
                f"Right-side composition is underused on slides {', '.join(pages)}; empty space must carry a visual, insight, chart, or deliberate rhythm.",
                {"layout_suitability": 1.8, "visual_hierarchy": 1.2, "whitespace_and_density": 1.2, "grid_and_alignment": 0.8},
            )

    if asset_plan is not None and not has_mandatory_generated_image(asset_plan):
        issue("mandatory_image_generation_missing", "severe", "Qualified decks must include at least one generated image asset captured into the workspace.", {"image_integration": 3.0, "originality_anti_ai_slop": 1.5, "visual_hierarchy": 0.8})
    if asset_plan is not None:
        relevance = generated_asset_relevance(asset_plan, slides_plan)
        if relevance["issues"]:
            issue(
                "image_not_bound_to_slide_message",
                "severe",
                "Generated images must be prompted from the specific slide title, core message, and visual role; generic or reused gate images are not acceptable.",
                {"image_integration": 3.0, "layout_suitability": 1.0, "originality_anti_ai_slop": 1.4},
            )

    dims = {k: round(max(0, min(10, v)), 1) for k, v in dims.items()}
    return dims, issues, sorted(set(failure_modes))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pptx", type=Path)
    parser.add_argument("--preview-dir", type=Path)
    parser.add_argument("--slides-plan", type=Path)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--reference-board", type=Path)
    parser.add_argument("--asset-plan", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--case-id", default="")
    args = parser.parse_args()

    spec = read_json(args.spec, {}) if args.spec else {}
    slides_plan = read_json(args.slides_plan, {"slides": []}) if args.slides_plan else {"slides": []}
    asset_plan = read_json(args.asset_plan, {}) if args.asset_plan else None
    pptx = pptx_stats(args.pptx)
    paths = slide_pngs(args.preview_dir)
    visual = visual_stats(paths)
    dims, issues, failure_modes = score_deck(spec, slides_plan, pptx, visual, asset_plan)
    score = round(sum(dims.values()), 1)
    severe = any(i["severity"] == "severe" for i in issues)
    required_floor = dims["typography"] >= 8 and dims["visual_hierarchy"] >= 8 and dims["grid_and_alignment"] >= 8 and dims["cross_slide_consistency_and_rhythm"] >= 8
    status = "PASS" if score >= 85 and required_floor and not severe else "FAIL"
    result = {
        "case_id": args.case_id,
        "status": status,
        "score": score,
        "dimensions": dims,
        "failure_modes": failure_modes,
        "issues": issues,
        "pptx_stats": pptx,
        "visual_stats": visual,
        "generated_asset_relevance": generated_asset_relevance(asset_plan, slides_plan) if asset_plan else None,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "annotated_issues").mkdir(exist_ok=True)
    (args.output_dir / "aesthetic_qa_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = [f"# Aesthetic QA Report: {args.case_id or 'deck'}", "", f"Status: `{status}`", f"Score: `{score}`", "", "## Dimensions", ""]
    for key, value in dims.items():
        md.append(f"- `{key}`: {value}/10")
    md.extend(["", "## Failure Modes", ""])
    md.extend([f"- `{mode}`" for mode in failure_modes] or ["- None"])
    md.extend(["", "## Issues", ""])
    md.extend([f"- **{i['severity']}** `{i['mode']}`: {i['message']}" for i in issues] or ["- None"])
    (args.output_dir / "aesthetic_qa_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
