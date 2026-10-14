#!/usr/bin/env python3
"""Validate a PradaSlides design-system.json contract."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
TONE_KEYS = {"background", "surface", "text", "muted", "line"}


def contrast_ratio(first: str, second: str) -> float:
    """Return WCAG relative-luminance contrast for two validated #RRGGBB values."""
    def luminance(value: str) -> float:
        channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def validate(value: Any) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not isinstance(value, dict):
        return [Diagnostic("error", "DESIGN_ROOT", "Root must be a JSON object")]
    if value.get("schema_version") != "1.2":
        diagnostics.append(Diagnostic("error", "DESIGN_SCHEMA", "schema_version must be '1.2'", "schema_version"))
    if not str(value.get("name", "")).strip():
        diagnostics.append(Diagnostic("error", "DESIGN_NAME", "name is required", "name"))

    direction = value.get("direction")
    if not isinstance(direction, dict):
        diagnostics.append(Diagnostic("error", "DESIGN_DIRECTION", "direction must be an object", "direction"))
    else:
        for key in ("communication_mode", "visual_cluster"):
            if not str(direction.get(key, "")).strip():
                diagnostics.append(Diagnostic("error", "DESIGN_DIRECTION_FIELD", f"{key} is required", f"direction.{key}"))
        character = direction.get("character")
        if not isinstance(character, list) or not 3 <= len(character) <= 5:
            diagnostics.append(Diagnostic("error", "DESIGN_CHARACTER", "character must contain 3–5 terms", "direction.character"))
        if not isinstance(direction.get("avoid"), list) or not direction.get("avoid"):
            diagnostics.append(Diagnostic("error", "DESIGN_AVOID", "direction.avoid must be a non-empty array", "direction.avoid"))

    art_direction = value.get("art_direction")
    if not isinstance(art_direction, dict):
        diagnostics.append(Diagnostic("error", "DESIGN_ART_DIRECTION", "art_direction must be an object", "art_direction"))
    else:
        thesis = str(art_direction.get("visual_thesis", "")).strip()
        if len(thesis.split()) < 8:
            diagnostics.append(Diagnostic("error", "DESIGN_ART_THESIS", "art_direction.visual_thesis must explain the intended visual character", "art_direction.visual_thesis"))
        scope = art_direction.get("reference_scope")
        if not isinstance(scope, dict):
            diagnostics.append(Diagnostic("error", "DESIGN_ART_REFERENCE", "art_direction.reference_scope must be an object", "art_direction.reference_scope"))
        else:
            for key in ("selected_cluster", "quality_floor", "anti_copy"):
                if not str(scope.get(key, "")).strip():
                    diagnostics.append(Diagnostic("error", "DESIGN_ART_REFERENCE_FIELD", f"reference_scope.{key} is required", f"art_direction.reference_scope.{key}"))
        for group, keys in {
            "material_language": ("background", "surface", "depth"),
            "edge_language": ("primary", "secondary", "overlap_policy"),
        }.items():
            item = art_direction.get(group)
            if not isinstance(item, dict):
                diagnostics.append(Diagnostic("error", "DESIGN_ART_GROUP", f"art_direction.{group} must be an object", f"art_direction.{group}"))
                continue
            for key in keys:
                if not str(item.get(key, "")).strip():
                    diagnostics.append(Diagnostic("error", "DESIGN_ART_GROUP_FIELD", f"{group}.{key} is required", f"art_direction.{group}.{key}"))
        image_system = art_direction.get("image_system")
        if not isinstance(image_system, dict):
            diagnostics.append(Diagnostic("error", "DESIGN_ART_IMAGE", "art_direction.image_system must be an object", "art_direction.image_system"))
        else:
            roles = image_system.get("roles")
            treatments = image_system.get("treatments")
            if not isinstance(roles, list) or not 3 <= len(roles) <= 8 or not all(str(item).strip() for item in roles):
                diagnostics.append(Diagnostic("error", "DESIGN_ART_IMAGE_ROLES", "image_system.roles must contain 3–8 non-empty roles", "art_direction.image_system.roles"))
            if not isinstance(treatments, list) or not 2 <= len(treatments) <= 8 or not all(str(item).strip() for item in treatments):
                diagnostics.append(Diagnostic("error", "DESIGN_ART_IMAGE_TREATMENTS", "image_system.treatments must contain 2–8 non-empty treatments", "art_direction.image_system.treatments"))
            for key in ("reuse_policy", "factual_visual_policy"):
                if not str(image_system.get(key, "")).strip():
                    diagnostics.append(Diagnostic("error", "DESIGN_ART_IMAGE_FIELD", f"image_system.{key} is required", f"art_direction.image_system.{key}"))
        strategy = art_direction.get("native_raster_strategy")
        if not isinstance(strategy, dict):
            diagnostics.append(Diagnostic("error", "DESIGN_ART_NATIVE_RASTER", "art_direction.native_raster_strategy must be an object", "art_direction.native_raster_strategy"))
        else:
            for key in ("native", "raster", "prohibited"):
                items = strategy.get(key)
                if not isinstance(items, list) or not items or not all(str(item).strip() for item in items):
                    diagnostics.append(Diagnostic("error", "DESIGN_ART_NATIVE_RASTER_FIELD", f"native_raster_strategy.{key} must be a non-empty array", f"art_direction.native_raster_strategy.{key}"))
        families = art_direction.get("slide_families")
        if not isinstance(families, list) or not 3 <= len(families) <= 8:
            diagnostics.append(Diagnostic("error", "DESIGN_ART_FAMILIES", "art_direction.slide_families must contain 3–8 families", "art_direction.slide_families"))
        elif isinstance(families, list):
            family_ids: set[str] = set()
            for index, family in enumerate(families):
                location = f"art_direction.slide_families[{index}]"
                if not isinstance(family, dict):
                    diagnostics.append(Diagnostic("error", "DESIGN_ART_FAMILY", "slide family must be an object", location))
                    continue
                for key in ("id", "purpose", "macro_composition", "image_occupation", "tone"):
                    if not str(family.get(key, "")).strip():
                        diagnostics.append(Diagnostic("error", "DESIGN_ART_FAMILY_FIELD", f"slide family {key} is required", f"{location}.{key}"))
                family_id = str(family.get("id", "")).strip()
                if family_id and family_id in family_ids:
                    diagnostics.append(Diagnostic("error", "DESIGN_ART_FAMILY_DUP", f"duplicate slide family id {family_id!r}", f"{location}.id"))
                family_ids.add(family_id)

    canvas = value.get("canvas")
    if not isinstance(canvas, dict):
        diagnostics.append(Diagnostic("error", "DESIGN_CANVAS", "canvas must be an object", "canvas"))
    else:
        for key in ("width_px", "height_px", "safe_margin_px", "columns", "gutter_px", "baseline_px"):
            number = canvas.get(key)
            if not isinstance(number, int) or number <= 0:
                diagnostics.append(Diagnostic("error", "DESIGN_CANVAS_VALUE", f"{key} must be a positive integer", f"canvas.{key}"))
        if isinstance(canvas.get("safe_margin_px"), int) and isinstance(canvas.get("width_px"), int):
            if canvas["safe_margin_px"] * 2 >= canvas["width_px"]:
                diagnostics.append(Diagnostic("error", "DESIGN_MARGIN", "safe margins consume the canvas", "canvas.safe_margin_px"))

    typography = value.get("typography")
    if not isinstance(typography, dict):
        diagnostics.append(Diagnostic("error", "DESIGN_TYPE", "typography must be an object", "typography"))
    else:
        for key in ("display_family", "body_family", "mono_family", "fallback_policy"):
            if not str(typography.get(key, "")).strip():
                diagnostics.append(Diagnostic("error", "DESIGN_TYPE_FIELD", f"{key} is required", f"typography.{key}"))
        selection = typography.get("selection")
        if selection is not None:
            if not isinstance(selection, dict):
                diagnostics.append(Diagnostic("error", "DESIGN_TYPE_SELECTION", "typography.selection must be an object", "typography.selection"))
            else:
                for key in ("category_prior", "product_archetype", "positioning", "audience", "proof_density", "interaction_model", "rationale"):
                    if not str(selection.get(key, "")).strip():
                        diagnostics.append(Diagnostic("error", "DESIGN_TYPE_SELECTION_FIELD", f"{key} is required", f"typography.selection.{key}"))
                personality = selection.get("personality")
                if not isinstance(personality, list) or not 3 <= len(personality) <= 5 or not all(str(item).strip() for item in personality):
                    diagnostics.append(Diagnostic("error", "DESIGN_TYPE_PERSONALITY", "typography.selection.personality must contain 3–5 terms", "typography.selection.personality"))
                rationale = str(selection.get("rationale", ""))
                if rationale and len(rationale.split()) < 12:
                    diagnostics.append(Diagnostic("error", "DESIGN_TYPE_RATIONALE", "typography.selection.rationale must connect product and audience to the type system", "typography.selection.rationale"))
        sizes = typography.get("sizes_px")
        if not isinstance(sizes, dict):
            diagnostics.append(Diagnostic("error", "DESIGN_TYPE_SIZE", "sizes_px must be an object", "typography.sizes_px"))
        else:
            minimums = {"hero": 64, "headline": 44, "subhead": 28, "body": 22, "caption": 15, "micro": 11}
            for key, minimum in minimums.items():
                number = sizes.get(key)
                if not isinstance(number, (int, float)) or number < minimum:
                    diagnostics.append(Diagnostic("error", "DESIGN_TYPE_MIN", f"{key} must be at least {minimum}px", f"typography.sizes_px.{key}"))
            ordered = [sizes.get(key, 0) for key in ("hero", "headline", "subhead", "body", "caption", "micro")]
            if any(left <= right for left, right in zip(ordered, ordered[1:])):
                diagnostics.append(Diagnostic("error", "DESIGN_TYPE_ORDER", "Type scale must descend from hero to micro", "typography.sizes_px"))

    color = value.get("color")
    if not isinstance(color, dict):
        diagnostics.append(Diagnostic("error", "DESIGN_COLOR", "color must be an object", "color"))
    else:
        for key in ("accent", "positive", "warning", "negative"):
            if not HEX.match(str(color.get(key, ""))):
                diagnostics.append(Diagnostic("error", "DESIGN_COLOR_HEX", f"{key} must be #RRGGBB", f"color.{key}"))
        tones = color.get("tones")
        if not isinstance(tones, dict) or not {"light", "dark"}.issubset(tones):
            diagnostics.append(Diagnostic("error", "DESIGN_TONES", "tones must include light and dark", "color.tones"))
        elif isinstance(tones, dict):
            for tone, palette in tones.items():
                if not isinstance(palette, dict) or not TONE_KEYS.issubset(palette):
                    diagnostics.append(Diagnostic("error", "DESIGN_TONE_FIELDS", f"Tone {tone} must define {sorted(TONE_KEYS)}", f"color.tones.{tone}"))
                    continue
                for key in TONE_KEYS:
                    if not HEX.match(str(palette.get(key, ""))):
                        diagnostics.append(Diagnostic("error", "DESIGN_TONE_HEX", f"{tone}.{key} must be #RRGGBB", f"color.tones.{tone}.{key}"))
                if all(HEX.match(str(palette.get(key, ""))) for key in TONE_KEYS):
                    for surface_key in ("background", "surface"):
                        ratio = contrast_ratio(str(palette["text"]), str(palette[surface_key]))
                        if ratio < 4.5:
                            diagnostics.append(Diagnostic("error", "DESIGN_TEXT_CONTRAST", f"{tone}.text contrast against {surface_key} is {ratio:.2f}:1; require at least 4.5:1", f"color.tones.{tone}.{surface_key}"))
                        muted_ratio = contrast_ratio(str(palette["muted"]), str(palette[surface_key]))
                        if muted_ratio < 3.0:
                            diagnostics.append(Diagnostic("error", "DESIGN_MUTED_CONTRAST", f"{tone}.muted contrast against {surface_key} is {muted_ratio:.2f}:1; require at least 3:1", f"color.tones.{tone}.{surface_key}"))

    furniture = value.get("furniture")
    if not isinstance(furniture, dict):
        diagnostics.append(Diagnostic("error", "DESIGN_FURNITURE", "furniture must be an object", "furniture"))
    else:
        if not isinstance(furniture.get("default_enabled"), list):
            diagnostics.append(Diagnostic("error", "DESIGN_FURNITURE_DEFAULT", "default_enabled must be an array", "furniture.default_enabled"))
        maximum = furniture.get("max_decorative_motifs_per_slide")
        if not isinstance(maximum, int) or not 0 <= maximum <= 3:
            diagnostics.append(Diagnostic("error", "DESIGN_MOTIF_MAX", "max_decorative_motifs_per_slide must be 0–3", "furniture.max_decorative_motifs_per_slide"))

    rhythm = value.get("rhythm")
    if not isinstance(rhythm, dict):
        diagnostics.append(Diagnostic("error", "DESIGN_RHYTHM", "rhythm must be an object", "rhythm"))
    else:
        integer_ranges = {
            "min_distinct_topologies_per_10_slides": (3, 8),
            "max_consecutive_same_topology": (1, 3),
            "max_consecutive_same_tone": (1, 5),
            "min_tone_shifts_per_10_slides": (1, 6),
        }
        for key, (low, high) in integer_ranges.items():
            number = rhythm.get(key)
            if not isinstance(number, int) or not low <= number <= high:
                diagnostics.append(Diagnostic("error", "DESIGN_RHYTHM_VALUE", f"{key} must be {low}–{high}", f"rhythm.{key}"))
        ratio = rhythm.get("max_card_grid_ratio")
        if not isinstance(ratio, (int, float)) or not 0 <= ratio <= 0.5:
            diagnostics.append(Diagnostic("error", "DESIGN_CARD_RATIO", "max_card_grid_ratio must be between 0 and 0.5", "rhythm.max_card_grid_ratio"))

    floor = value.get("quality_floor")
    required_floor = {"thumbnail_test", "squint_test", "evidence_scale", "contrast", "copy_fit", "reference_floor", "target_runtime"}
    if not isinstance(floor, dict) or not required_floor.issubset(floor):
        diagnostics.append(Diagnostic("error", "DESIGN_FLOOR", f"quality_floor must define {sorted(required_floor)}", "quality_floor"))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design_system", type=Path)
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        value = load_json(args.design_system)
    except ValueError as exc:
        return emit_report("design system validation", [Diagnostic("error", "DESIGN_JSON", str(exc))], json_output=args.json_output)
    return emit_report(
        "design system validation",
        validate(value),
        json_output=args.json_output,
        extra={"file": str(args.design_system.resolve())},
    )


if __name__ == "__main__":
    raise SystemExit(main())
