#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_MARKERS = [
    "cover",
    "closing",
    "vision",
    "hook",
    "concept",
    "abstract",
    "scenario",
    "case",
    "story",
    "product",
    "system",
    "capability",
    "process",
    "workflow",
    "architecture",
]

NOT_NEEDED_MARKERS = ["agenda", "toc", "contents", "目录", "table", "checklist", "policy", "法规", "清单"]


def read_json(path: Path | None, fallback: Any) -> Any:
    if not path or not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_text(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(x).strip() for x in value if str(x).strip())
    return str(value or "").strip()


def slide_id(slide: dict[str, Any], idx: int) -> str:
    return str(slide.get("slide_id") or slide.get("id") or f"slide_{idx + 1:02d}")


def layout_of(slide: dict[str, Any], idx: int, total: int) -> str:
    raw = str(
        slide.get("layout_archetype")
        or slide.get("layout")
        or slide.get("layout_family")
        or slide.get("slide_type")
        or ""
    ).lower()
    if raw:
        return raw
    if idx == 0:
        return "cover-hero"
    if idx == total - 1:
        return "closing-echo"
    return "text-visual-60-40"


def core_message(slide: dict[str, Any]) -> str:
    for key in ("core_message", "key_message", "purpose", "subtitle", "body", "points", "speaker_notes_seed"):
        value = clean_text(slide.get(key))
        if value:
            return value[:180]
    return clean_text(slide.get("title"))[:180]


def infer_visual_need(slide: dict[str, Any], idx: int, total: int) -> str:
    explicit = slide.get("visual_need")
    if explicit in {"required", "optional", "not_needed"}:
        return explicit
    haystack = " ".join(
        [
            layout_of(slide, idx, total),
            clean_text(slide.get("title")),
            clean_text(slide.get("purpose")),
            clean_text(slide.get("key_message")),
        ]
    ).lower()
    if idx == 0 or idx == total - 1 or any(marker in haystack for marker in REQUIRED_MARKERS):
        return "required"
    if any(marker in haystack for marker in NOT_NEEDED_MARKERS):
        return "not_needed"
    if "chart" in haystack or "data" in haystack or "数据" in haystack:
        return "optional"
    return "optional"


def choose_asset_type(slide: dict[str, Any], layout: str, need: str, idx: int, total: int) -> str:
    existing = slide.get("asset_type")
    if existing:
        return str(existing)
    text = f"{layout} {clean_text(slide.get('title'))} {clean_text(slide.get('purpose'))}".lower()
    if need == "not_needed":
        return "none"
    if idx == 0 or "cover" in layout:
        return "cover_hero"
    if "closing" in layout or "vision" in text:
        return "closing_vision"
    if "chart" in layout or "data" in text or "数据" in text:
        return "data_chart"
    if "process" in layout or "workflow" in text or "流程" in text:
        return "process_diagram"
    if "case" in layout or "story" in text or "案例" in text:
        return "scene_illustration"
    if "system" in text or "architecture" in text or "能力" in text:
        return "system_illustration"
    return "concept_illustration"


def choose_slot(layout: str, asset_type: str, idx: int, total: int) -> dict[str, str]:
    if idx == 0 or "cover" in layout:
        return {
            "image_slot": "cover_hero",
            "aspect_ratio": "16:9",
            "integration_treatment": "masked editorial crop",
            "intended_composition": "Large visual field on the right or full canvas edge, with a quiet native-text safe zone on the left.",
        }
    if "closing" in layout or asset_type == "closing_vision":
        return {
            "image_slot": "cover_hero",
            "aspect_ratio": "16:9",
            "integration_treatment": "full-bleed hero",
            "intended_composition": "Closing visual echoes the cover motif while leaving a quiet native-text zone.",
        }
    if "visual-text" in layout:
        return {
            "image_slot": "left_40",
            "aspect_ratio": "16:10",
            "integration_treatment": "60/40 split",
            "intended_composition": "Visual sits on the left as evidence or scene; native explanation remains on the right.",
        }
    if "chart" in layout or asset_type == "data_chart":
        return {
            "image_slot": "chart_sidecar",
            "aspect_ratio": "4:3",
            "integration_treatment": "chart-with-insight sidecar",
            "intended_composition": "Native chart remains editable; generated visual only supports context or metaphor.",
        }
    if "image-grid" in layout or asset_type == "image_grid":
        return {
            "image_slot": "image_grid",
            "aspect_ratio": "16:10",
            "integration_treatment": "image grid",
            "intended_composition": "All visuals in the grid share the same crop, scale, margins, and line weight.",
        }
    if "statement" in layout:
        return {
            "image_slot": "top_strip",
            "aspect_ratio": "21:9",
            "integration_treatment": "tinted monochrome treatment",
            "intended_composition": "Wide restrained strip supports the statement without competing with the headline.",
        }
    return {
        "image_slot": "right_40",
        "aspect_ratio": "16:10",
        "integration_treatment": "60/40 split",
        "intended_composition": "Visual sits on the right 40 percent as a semantic explanation panel; native text stays left.",
    }


def style_summary(spec: dict[str, Any], reference_board: dict[str, Any]) -> str:
    pieces = []
    if spec.get("style_id"):
        pieces.append(f"style_id={spec['style_id']}")
    if spec.get("style"):
        pieces.append(f"style={spec['style']}")
    dna = reference_board.get("design_dna") if isinstance(reference_board, dict) else None
    if isinstance(dna, dict):
        palette = dna.get("palette") or []
        if palette:
            pieces.append("palette=" + ", ".join(map(str, palette[:4])))
        treatment = dna.get("image_treatment") or []
        if treatment:
            pieces.append("image_treatment=" + ", ".join(map(str, treatment[:2])))
    return "; ".join(pieces) or "professional Chinese PPT style with restrained palette, strong hierarchy, and clear grid"


def build_prompt(spec: dict[str, Any], reference_board: dict[str, Any], slide: dict[str, Any], asset: dict[str, Any]) -> str:
    binding = asset["semantic_binding"]
    title = binding["slide_title"]
    core = binding["core_message"]
    style = style_summary(spec, reference_board)
    return "\n".join(
        [
            "Generate one raster visual asset for a PowerPoint slide.",
            "",
            f"Slide title: {title}",
            f"Slide core message: {core}",
            f"Visual role: {binding['visual_role']}",
            f"Layout archetype: {binding['layout_archetype']}",
            f"Image slot: {asset['image_slot']}",
            f"Aspect ratio: {asset['aspect_ratio']}",
            f"Integration treatment: {asset['integration_treatment']}",
            f"Intended composition: {binding['intended_composition']}",
            f"Deck style: {style}",
            "",
            "Create a page-specific visual that explains or supports this exact slide message.",
            "Do not create a generic background, seed image, wallpaper, unrelated technology scene, or decorative filler.",
            "No slide title, no body copy, no key numbers, no chart conclusion, no page chrome, no logo, no watermark.",
            "Keep the composition clean enough for native editable PowerPoint text to sit beside or over it.",
            "Use a professional Chinese presentation aesthetic: readable hierarchy, restrained colors, deliberate whitespace, and no AI-template purple-blue glow.",
        ]
    )


def normalize_assets(
    run_dir: Path,
    spec: dict[str, Any],
    slides_plan: dict[str, Any],
    asset_plan: dict[str, Any],
    reference_board: dict[str, Any],
) -> dict[str, Any]:
    slides = slides_plan.get("slides", [])
    total = len(slides)
    raw_assets = asset_plan.get("assets") or asset_plan.get("slides") or []
    existing = {str(item.get("slide_id")): dict(item) for item in raw_assets if item.get("slide_id")}
    brief_dir = run_dir / "visual_briefs"
    brief_dir.mkdir(parents=True, exist_ok=True)
    normalized = []
    for idx, slide in enumerate(slides):
        sid = slide_id(slide, idx)
        layout = layout_of(slide, idx, total)
        need = existing.get(sid, {}).get("visual_need") or infer_visual_need(slide, idx, total)
        asset_type = existing.get(sid, {}).get("asset_type") or choose_asset_type(slide, layout, need, idx, total)
        slot = choose_slot(layout, asset_type, idx, total)
        item = {
            "slide_id": sid,
            "visual_need": need,
            "asset_type": asset_type,
            "generation_required": need == "required" and asset_type not in {"data_chart", "none"},
            "reason": existing.get(sid, {}).get("reason")
            or ("This slide needs a page-specific visual to carry its message." if need == "required" else "Native layout can carry the slide; generated visual is optional."),
            "must_not_skip": need == "required",
            "fallback_allowed": need != "required",
            "status": "not_needed" if need == "not_needed" else "planned",
            **slot,
        }
        item.update(existing.get(sid, {}))
        item.setdefault("image_slot", slot["image_slot"])
        item.setdefault("aspect_ratio", slot["aspect_ratio"])
        item.setdefault("integration_treatment", slot["integration_treatment"])
        if item["visual_need"] == "required" and item.get("asset_type") not in {"data_chart", "screenshot", "user_asset", "none"}:
            item["generation_required"] = True
            item["must_not_skip"] = True
        binding = dict(item.get("semantic_binding") or {})
        binding.update(
            {
                "bound_to_slide": True,
                "slide_title": binding.get("slide_title") or clean_text(slide.get("title")) or sid,
                "core_message": binding.get("core_message") or core_message(slide),
                "visual_role": binding.get("visual_role") or clean_text(slide.get("visual_role")) or item["asset_type"],
                "layout_archetype": binding.get("layout_archetype") or layout,
                "intended_composition": binding.get("intended_composition") or item["intended_composition"],
            }
        )
        binding["visual_brief"] = (
            binding.get("visual_brief")
            or f"Create a visual for '{binding['slide_title']}' that makes this message tangible: {binding['core_message']}"
        )
        item["semantic_binding"] = binding
        if item.get("generation_required"):
            prompt = build_prompt(spec, reference_board, slide, item)
            prompt_path = brief_dir / f"{sid}_image_prompt.md"
            prompt_path.write_text(prompt + "\n", encoding="utf-8")
            item["prompt_path"] = str(prompt_path)
        normalized.append(item)
    return {
        **asset_plan,
        "minimum_is_not_maximum": True,
        "semantic_visual_briefs": True,
        "assets": normalized,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=Path("."))
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--slides-plan", type=Path, required=True)
    parser.add_argument("--asset-plan", type=Path, required=True)
    parser.add_argument("--reference-board", type=Path)
    args = parser.parse_args()

    spec = read_json(args.spec, {})
    slides_plan = read_json(args.slides_plan, {"slides": []})
    asset_plan = read_json(args.asset_plan, {"assets": []})
    reference_board = read_json(args.reference_board, {})
    normalized = normalize_assets(args.run_dir, spec, slides_plan, asset_plan, reference_board)
    write_json(args.asset_plan, normalized)
    required = sum(1 for item in normalized["assets"] if item.get("visual_need") == "required")
    prompts = sum(1 for item in normalized["assets"] if item.get("prompt_path"))
    print(f"visual briefs written: {len(normalized['assets'])} slides, {required} required, {prompts} prompt files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
