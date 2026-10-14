#!/usr/bin/env python3
"""Collect structural facts from a host-Agent-authored semantic map.

The script deliberately does not judge whether the map visually represents the slide
well. That judgement belongs to the host Agent's measurement review.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image


def box(record: dict[str, Any]) -> list[float] | None:
    if record.get("kind") in {"icon", "icon_slot"} and record.get("slot_bbox_hint"):
        value = record.get("slot_bbox_hint")
    else:
        value = record.get("bbox_hint") or record.get("bbox")
    return [float(v) for v in value] if isinstance(value, list) and len(value) == 4 else None



def norm_hex(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip().upper()
    if text == "NONE":
        return "NONE"
    if len(text) == 4 and text.startswith("#"):
        text = "#" + "".join(ch * 2 for ch in text[1:])
    if len(text) == 7 and text.startswith("#") and all(ch in "0123456789ABCDEF" for ch in text[1:]):
        return text
    return None


def resolved_token_style(config: dict[str, Any], entity: dict[str, Any], surface: bool = False) -> dict[str, Any]:
    if surface:
        record = entity.get("slot_surface") or {}
        name = record.get("style_token") or entity.get("style_token") or (entity.get("style_hint") or {}).get("style_token")
    else:
        name = entity.get("style_token") or (entity.get("style_hint") or {}).get("style_token")
    return dict(config.get("design", {}).get("semantic_style_tokens", {}).get(name, {}) or {}) if name else {}



def contained(child: list[float], parent: list[float], tolerance: float = 1.0) -> bool:
    cx, cy, cw, ch = child
    px, py, pw, ph = parent
    return cx >= px - tolerance and cy >= py - tolerance and cx + cw <= px + pw + tolerance and cy + ch <= py + ph + tolerance


def overlaps(first: list[float], second: list[float], tolerance: float = 0.5) -> bool:
    ax, ay, aw, ah = first
    bx, by, bw, bh = second
    return min(ax + aw, bx + bw) - max(ax, bx) > tolerance and min(ay + ah, by + bh) - max(ay, by) > tolerance


def selected_asset_catalog(handoff: dict[str, Any]) -> dict[str, dict[str, Any]]:
    catalog = {}
    for item in handoff.get("selected_assets", []) or []:
        asset = item.get("internal", item)
        if asset.get("asset_id"):
            catalog[str(asset["asset_id"])] = asset
    return catalog


def remix_icon_variant_errors(entities: list[dict[str, Any]], handoff: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    catalog = selected_asset_catalog(handoff)
    group_variants: dict[str, set[str]] = {}
    group_members: dict[str, list[str]] = {}
    for entity in entities:
        if entity.get("kind") not in {"icon", "icon_slot"}:
            continue
        asset_id = str(entity.get("upstream_asset_id") or "")
        asset = catalog.get(asset_id, {})
        if str(asset.get("provider") or "") != "Remix Icon":
            continue
        identifier = str(entity.get("id") or "")
        variant = str(entity.get("icon_variant") or "")
        if variant not in {"line", "fill"}:
            errors.append({"entity": identifier, "reason": "remix_icon_requires_line_or_fill_variant"})
            continue
        if str(asset.get("style_variant") or "") != variant:
            errors.append({"entity": identifier, "reason": "remix_icon_variant_does_not_match_selected_asset", "icon_variant": variant, "asset_id": asset_id, "asset_variant": asset.get("style_variant")})
        pair_ids = {str(value) for value in asset.get("pair_asset_ids", []) or []}
        if len(pair_ids) != 2 or not pair_ids.issubset(catalog):
            errors.append({"entity": identifier, "reason": "remix_icon_handoff_must_retain_complete_line_fill_pair", "pair_asset_ids": sorted(pair_ids)})
        review = entity.get("icon_variant_review") or {}
        evaluated = {str(value) for value in review.get("evaluated_asset_ids", []) or []}
        observations = [str(value).strip() for value in review.get("observations", []) or [] if str(value).strip()]
        if review.get("stage") != "post_generation_visual_review":
            errors.append({"entity": identifier, "reason": "remix_icon_variant_review_must_follow_generation_review"})
        if review.get("reviewed_by") != "host_agent_visual_reasoning":
            errors.append({"entity": identifier, "reason": "remix_icon_variant_requires_host_visual_review"})
        if not str(review.get("decision") or "").strip() or not observations:
            errors.append({"entity": identifier, "reason": "remix_icon_variant_review_requires_decision_and_visual_observations"})
        if pair_ids and not pair_ids.issubset(evaluated):
            errors.append({"entity": identifier, "reason": "remix_icon_variant_review_must_compare_both_pair_assets", "required": sorted(pair_ids), "evaluated": sorted(evaluated)})
        group = str(entity.get("icon_treatment_group") or "")
        if group:
            group_variants.setdefault(group, set()).add(variant)
            group_members.setdefault(group, []).append(identifier)
    for group, variants in group_variants.items():
        if len(variants) > 1:
            errors.append({"reason": "remix_icon_peer_group_mixes_line_and_fill", "icon_treatment_group": group, "variants": sorted(variants), "member_ids": group_members[group]})
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--semantic-map", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--upstream-handoff", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--approvals", type=Path, help="Optional legacy decision history. It does not gate semantic evidence.")
    args = parser.parse_args()
    semantic = json.loads(args.semantic_map.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))
    handoff = json.loads(args.upstream_handoff.read_text(encoding="utf-8")) if args.upstream_handoff else {}
    width, height = Image.open(args.image).size
    errors: list[dict[str, Any]] = []
    entities = semantic.get("entities", [])
    groups = semantic.get("groups", [])
    ids = [str(item.get("id", "")) for item in [*entities, *groups]]
    duplicates = sorted({identifier for identifier in ids if identifier and ids.count(identifier) > 1})
    if duplicates:
        errors.append({"reason": "duplicate_semantic_ids", "ids": duplicates})
    if any(not identifier for identifier in ids):
        errors.append({"reason": "missing_semantic_id"})

    lookup = {str(item["id"]): item for item in [*entities, *groups] if item.get("id")}
    entity_lookup = {str(item["id"]): item for item in entities if item.get("id")}
    text_style_policies = config.get("design", {}).get("text_reconstruction", {}).get("text_style_policies", {})
    for item in [*entities, *groups]:
        item_box = box(item)
        if item_box is None:
            errors.append({"entity": item.get("id"), "reason": "missing_bbox_hint"})
            continue
        x, y, w, h = item_box
        if w <= 0 or h <= 0 or x < -1 or y < -1 or x + w > width + 1 or y + h > height + 1:
            errors.append({"entity": item.get("id"), "reason": "bbox_outside_generation_canvas", "bbox": item_box, "canvas": [width, height]})

    text_entities = [entity for entity in entities if entity.get("kind") == "text"]
    typography_groups: dict[str, list[dict[str, Any]]] = {}
    icon_treatment_groups: dict[str, list[dict[str, Any]]] = {}
    non_emitting = {"measurement_evidence", "owned_content", "non_authoritative_glyph"}
    for entity in entities:
        if entity.get("kind") == "connector" or str(entity.get("reconstruction_significance") or "independent_object") in non_emitting:
            continue
        geometry_policy = str(entity.get("geometry_policy") or "")
        if geometry_policy not in {"agent_logical", "opencv_visible"}:
            errors.append({
                "entity": entity.get("id"),
                "reason": "emitting_entity_requires_agent_selected_geometry_policy",
                "allowed": ["agent_logical", "opencv_visible"],
            })
    for entity in entities:
        significance = str(entity.get("reconstruction_significance") or "independent_object")
        if significance in non_emitting:
            continue
        if not isinstance(entity.get("z"), (int, float)):
            errors.append({"entity": entity.get("id"), "reason": "emitting_entity_requires_agent_authored_z_order"})
        kind = str(entity.get("kind") or "")
        if kind in {"shape", "novel_visual"}:
            if not str(entity.get("shape") or "").strip():
                if kind == "shape":
                    errors.append({"entity": entity.get("id"), "reason": "shape_requires_explicit_geometry_type"})
            hint = dict(entity.get("style_hint", {}) or {})
            if not (entity.get("style_token") or hint.get("style_token") or hint.get("style_authority") in {"agent_visual_observation", "profile_policy", "profile_token", "user_exact"}):
                errors.append({"entity": entity.get("id"), "reason": f"{kind}_requires_explicit_style_authority"})
        if kind == "image" and entity.get("raster_fit") not in {"contain", "fill"}:
            errors.append({"entity": entity.get("id"), "reason": "image_requires_agent_authored_raster_fit", "allowed": ["contain", "fill"]})
        if entity.get("sam_candidate_index") is not None and (
            not isinstance(entity.get("sam_candidate_index"), int)
            or isinstance(entity.get("sam_candidate_index"), bool)
            or int(entity["sam_candidate_index"]) < 0
        ):
            errors.append({"entity": entity.get("id"), "reason": "sam_candidate_index_must_be_a_nonnegative_integer"})
    for entity in text_entities:
        style_role = str(entity.get("text_style_role") or "").strip()
        if not style_role:
            errors.append({"entity": entity.get("id"), "reason": "text_requires_text_style_role"})
        elif style_role not in text_style_policies:
            errors.append({"entity": entity.get("id"), "reason": "unknown_text_style_role", "text_style_role": style_role})

        typography_group = str(entity.get("typography_group") or "").strip()
        if not typography_group:
            errors.append({"entity": entity.get("id"), "reason": "text_requires_typography_group"})
        else:
            typography_groups.setdefault(typography_group, []).append(entity)

        hint = dict(entity.get("style_hint", {}) or {})
        target_size = hint.get("target_font_size_px")
        if not isinstance(target_size, (int, float)) or float(target_size) <= 0:
            errors.append({"entity": entity.get("id"), "reason": "text_requires_agent_authored_target_font_size_px"})
        authority = str(hint.get("style_authority") or "")
        allowed_authorities = {"user_exact", "agent_visual_observation", "profile_token", "profile_policy"}
        if authority not in allowed_authorities:
            errors.append({"entity": entity.get("id"), "reason": "text_requires_explicit_style_authority", "allowed": sorted(allowed_authorities)})
        if authority == "profile_token" and not (entity.get("style_token") or hint.get("style_token")):
            errors.append({"entity": entity.get("id"), "reason": "profile_token_authority_requires_style_token"})
        if authority in {"user_exact", "agent_visual_observation"} and not (hint.get("observed_foreground_color") or hint.get("color")):
            errors.append({"entity": entity.get("id"), "reason": "visual_color_authority_requires_authored_color"})

    for typography_group, members in typography_groups.items():
        style_roles = {str(member.get("text_style_role") or "").strip() for member in members}
        if len(style_roles) > 1:
            errors.append({
                "reason": "typography_group_mixes_text_style_roles",
                "typography_group": typography_group,
                "member_ids": [member.get("id") for member in members],
                "text_style_roles": sorted(style_roles),
            })
        target_sizes = {float((member.get("style_hint") or {}).get("target_font_size_px")) for member in members if isinstance((member.get("style_hint") or {}).get("target_font_size_px"), (int, float))}
        if len(target_sizes) > 1:
            errors.append({
                "reason": "typography_group_mixes_target_font_sizes",
                "typography_group": typography_group,
                "member_ids": [member.get("id") for member in members],
                "target_font_sizes_px": sorted(target_sizes),
            })

    for entity in entities:
        if entity.get("kind") in {"icon", "icon_slot"}:
            slot = entity.get("slot_bbox_hint")
            if not (isinstance(slot, list) and len(slot) == 4):
                errors.append({"entity": entity.get("id"), "reason": "icon_requires_explicit_slot_bbox_hint"})
            treatment_group = str(entity.get("icon_treatment_group") or "").strip()
            if not treatment_group:
                errors.append({"entity": entity.get("id"), "reason": "icon_requires_icon_treatment_group"})
            else:
                icon_treatment_groups.setdefault(treatment_group, []).append(entity)
            treatment = entity.get("slot_surface")
            if not isinstance(treatment, dict) or not isinstance(treatment.get("visible"), bool):
                errors.append({"entity": entity.get("id"), "reason": "icon_requires_explicit_slot_surface_visibility"})
            elif treatment.get("visible"):
                surface_shape = str(treatment.get("shape") or "")
                if not surface_shape:
                    errors.append({"entity": entity.get("id"), "reason": "visible_icon_slot_surface_requires_explicit_shape"})
                if surface_shape not in {"rectangle", "rounded_rectangle", "rounded_rect", "ellipse"}:
                    errors.append({"entity": entity.get("id"), "reason": "unsupported_icon_slot_surface_shape", "shape": surface_shape})
                if surface_shape in {"rounded_rectangle", "rounded_rect"}:
                    if not treatment.get("shape_intent"):
                        errors.append({"entity": entity.get("id"), "reason": "rounded_icon_slot_surface_requires_shape_intent"})
                    radius = treatment.get("corner_radius_px")
                    if not isinstance(radius, (int, float)) or float(radius) < 0:
                        errors.append({"entity": entity.get("id"), "reason": "rounded_icon_slot_surface_requires_nonnegative_corner_radius_px"})
            inset = (entity.get("style_hint") or {}).get("icon_inset_fraction")
            if not isinstance(inset, (int, float)) or not (0 <= float(inset) < 0.5):
                errors.append({"entity": entity.get("id"), "reason": "icon_requires_agent_authored_icon_inset_fraction"})

    allowed_icon_treatments = {str(item.get("id")) for item in ((config.get("resolved_profile", {}).get("hard_rules", {}).get("icons", {}).get("proxy_treatments", [])) or []) if item.get("id")}
    for treatment_group, members in icon_treatment_groups.items():
        treatments = {str(member.get("icon_treatment") or "").strip() for member in members}
        if "" in treatments:
            errors.append({"reason": "icon_treatment_group_requires_explicit_treatment", "icon_treatment_group": treatment_group, "member_ids": [member.get("id") for member in members]})
            treatments.discard("")
        unknown = sorted(treatments - allowed_icon_treatments) if allowed_icon_treatments else []
        if unknown:
            errors.append({"reason": "unknown_icon_treatment", "icon_treatment_group": treatment_group, "treatments": unknown, "allowed": sorted(allowed_icon_treatments)})
        if len(treatments) > 1:
            errors.append({"reason": "icon_treatment_group_mixes_treatments", "icon_treatment_group": treatment_group, "member_ids": [member.get("id") for member in members], "treatments": sorted(treatments)})
    errors.extend(remix_icon_variant_errors(entities, handoff))

    # Fidelity invariant: a meaningful visible entity may not silently disappear.
    known_ids = {str(item.get("id")) for item in entities if item.get("id")}
    for entity in entities:
        significance = str(entity.get("reconstruction_significance") or "independent_object")
        if significance not in non_emitting:
            continue
        if significance == "measurement_evidence":
            if entity.get("meaningful_visible") is not False:
                errors.append({"entity": entity.get("id"), "reason": "measurement_evidence_must_be_explicitly_nonmeaningful_visible"})
            continue
        owner = str(entity.get("render_owner") or "")
        if not owner or owner == str(entity.get("id")) or owner not in known_ids:
            errors.append({"entity": entity.get("id"), "reason": "non_emitting_meaningful_entity_requires_distinct_render_owner", "render_owner": owner or None})

    profile = config.get("resolved_profile", {}) or {}
    hard_rules = profile.get("hard_rules", {}) or {}
    typography_rules = hard_rules.get("typography", {}) or {}
    icon_rules = hard_rules.get("icons", {}) or {}
    asset_rules = hard_rules.get("asset_vocabulary", {}) or {}
    if str(asset_rules.get("mode") or "open").lower() == "closed":
        selected_asset_ids = {str(item.get("asset_id")) for item in handoff.get("selected_assets", []) if item.get("asset_id")}
        allowed_raster_roles = {str(value) for value in asset_rules.get("allowed_non_asset_raster_roles", []) or []}
        novel_policy = asset_rules.get("novel_illustrations", {}) or {}
        novel_mode = str(novel_policy.get("mode") or "none").lower()
        for entity in entities:
            kind = str(entity.get("kind") or "")
            source_class = str(entity.get("visual_source_class") or "")
            if kind == "image" and source_class == "novel_illustration":
                if novel_mode in {"none", "forbidden", "off"}:
                    errors.append({"entity": entity.get("id"), "reason": "profile_forbids_novel_illustration"})
                if entity.get("upstream_asset_id"):
                    errors.append({"entity": entity.get("id"), "reason": "novel_illustration_must_not_claim_upstream_asset_id"})
                continue
            if kind == "novel_visual":
                errors.append({"entity": entity.get("id"), "reason": "closed_asset_vocabulary_forbids_unmapped_novel_visual_use_image_novel_illustration_for_raster_illustrations"})
            elif kind in {"icon", "icon_slot", "image"}:
                upstream = str(entity.get("upstream_asset_id") or "")
                role = str(entity.get("role") or "")
                if not upstream and kind == "image" and role in allowed_raster_roles:
                    continue
                if not upstream:
                    errors.append({"entity": entity.get("id"), "reason": "closed_asset_vocabulary_requires_upstream_asset_id_or_novel_illustration_class", "kind": kind})
                elif selected_asset_ids and upstream not in selected_asset_ids:
                    errors.append({"entity": entity.get("id"), "reason": "closed_asset_vocabulary_references_unselected_asset", "upstream_asset_id": upstream})
                elif not selected_asset_ids and args.upstream_handoff:
                    errors.append({"entity": entity.get("id"), "reason": "closed_asset_vocabulary_has_no_selected_assets_in_handoff", "upstream_asset_id": upstream})
    if profile.get("profile_id"):
        allowed_text_colors = {norm_hex(value) for value in typography_rules.get("ordinary_text_colors", [])}
        allowed_text_colors.discard(None)
        allowed_colored_tokens = set(typography_rules.get("allowed_colored_text_style_tokens", []))
        resolved_style = config.get("design", {}).get("style", {})
        allowed_fonts = {str(resolved_style.get("display_font", "")), str(resolved_style.get("body_font", ""))} - {""}
        if typography_rules.get("font_family_policy") == "agent_observed":
            allowed_fonts = set()
        for entity in entities:
            if entity.get("kind") == "text":
                hint = dict(entity.get("style_hint", {}) or {})
                if typography_rules.get("italics_allowed") is False and bool(hint.get("italic")):
                    errors.append({"entity": entity.get("id"), "reason": "profile_forbids_italics", "profile": profile.get("profile_id")})
                family = hint.get("font_family")
                if family and allowed_fonts and str(family) not in allowed_fonts:
                    errors.append({"entity": entity.get("id"), "reason": "profile_unapproved_powerpoint_font", "font_family": family, "allowed": sorted(allowed_fonts)})
                token_name = entity.get("style_token") or hint.get("style_token")
                token_style = resolved_token_style(config, entity)
                color = norm_hex(token_style.get("text_color") or token_style.get("color") or hint.get("observed_foreground_color") or hint.get("color"))
                style_role = str(entity.get("text_style_role") or "default")
                policy = text_style_policies.get(style_role, text_style_policies.get("default", {})) or {}
                policy_color = norm_hex(policy.get("color"))
                color_is_policy_authorized = bool(color and policy_color and color == policy_color)
                if color and allowed_text_colors and color not in allowed_text_colors and token_name not in allowed_colored_tokens and not color_is_policy_authorized:
                    errors.append({"entity": entity.get("id"), "reason": "profile_disallows_ordinary_text_color", "color": color, "style_token": token_name, "text_style_role": style_role, "allowed": sorted(allowed_text_colors)})
                if typography_rules.get("tracking_allowed") is False:
                    tracking = hint.get("tracking", hint.get("char_spacing", hint.get("character_spacing")))
                    if tracking not in {None, 0, 0.0, "0", "0.0"}:
                        errors.append({"entity": entity.get("id"), "reason": "profile_forbids_tracking", "tracking": tracking})

            if entity.get("kind") in {"icon", "icon_slot"}:
                treatments = {str(item.get("id")): item for item in icon_rules.get("proxy_treatments", []) if isinstance(item, dict) and item.get("id")}
                selected_treatment = treatments.get(str(entity.get("icon_treatment") or ""), {})
                surface = dict(entity.get("slot_surface", {}) or {})
                if surface.get("visible"):
                    geometry_policy = dict(icon_rules.get("surface_geometry_policy", {}) or {})
                    allowed_shapes = set(geometry_policy.get("allowed_visible_shapes", []) or [])
                    surface_shape = str(surface.get("shape", "rectangle"))
                    if allowed_shapes and surface_shape not in allowed_shapes and not surface.get("user_explicit_geometry_override"):
                        errors.append({"entity": entity.get("id"), "reason": "profile_disallows_icon_surface_shape", "shape": surface_shape, "allowed": sorted(allowed_shapes)})
                    surface_token = resolved_token_style(config, entity, surface=True)
                    surface_hint = dict(surface.get("style_hint", {}) or {})
                    fill = norm_hex(surface_hint.get("fill") or surface_token.get("fill"))
                    stroke = norm_hex(surface_hint.get("stroke") or surface_hint.get("border") or surface_token.get("stroke") or surface_token.get("border"))
                    if geometry_policy.get("decorative_outline_allowed") is False and stroke not in {None, "NONE"}:
                        errors.append({"entity": entity.get("id"), "reason": "profile_icon_surface_forbids_decorative_outline", "stroke": stroke})
                    allowed_surfaces = {norm_hex(value) for value in icon_rules.get("allowed_surface_colors", []) or []}
                    per_treatment = {norm_hex(value) for value in selected_treatment.get("allowed_surface_colors", []) or []}
                    per_treatment.discard(None)
                    if per_treatment:
                        allowed_surfaces = per_treatment
                    allowed_surfaces.discard(None)
                    if fill and allowed_surfaces and fill not in allowed_surfaces:
                        errors.append({"entity": entity.get("id"), "reason": "profile_disallows_icon_surface_fill", "fill": fill, "allowed": sorted(allowed_surfaces)})

    component_library = config["libraries"]["components"]
    components_by_id = {}
    for value in component_library.get("catalogs", [component_library.get("catalog")]):
        if not value:
            continue
        catalog = json.loads(Path(value).read_text(encoding="utf-8"))
        for record in (catalog.get("items") or {}).values():
            identifier = str(record.get("id", ""))
            if identifier in components_by_id:
                raise ValueError(f"Duplicate component ID across selected sets: {identifier}")
            if identifier:
                components_by_id[identifier] = record
    for entity in entities:
        component_id = entity.get("component_id")
        if component_id is None:
            continue
        record = components_by_id.get(str(component_id))
        if record is None:
            errors.append({"entity": entity.get("id"), "reason": "unknown_component_id", "component_id": component_id})
            continue
        if entity.get("kind") not in {"chart", "table"}:
            errors.append({"entity": entity.get("id"), "reason": "component_id_requires_chart_or_table_entity", "component_id": component_id, "kind": entity.get("kind")})
        elif record.get("kind") != entity.get("kind"):
            errors.append({"entity": entity.get("id"), "reason": "component_kind_mismatch", "component_id": component_id, "component_kind": record.get("kind"), "entity_kind": entity.get("kind")})

    for entity in entities:
        if entity.get("kind") == "connector":
            continue
        parent_id = entity.get("parent_id") or entity.get("parent")
        if not parent_id or entity.get("allow_parent_bleed") is True:
            continue
        parent = lookup.get(str(parent_id))
        child_box = box(entity)
        parent_box = box(parent) if parent else None
        if parent_box is None:
            errors.append({"entity": entity.get("id"), "reason": "missing_parent", "parent": parent_id})
        elif child_box and not contained(child_box, parent_box):
            errors.append({"entity": entity.get("id"), "reason": "explicit_parent_containment_violation", "parent": parent_id, "child_bbox": child_box, "parent_bbox": parent_box})

    rounding = config.get("design", {}).get("shape_geometry", {}).get("rounding", {})
    allowed_intents = set(rounding.get("intent_values", []))
    for entity in entities:
        shape = str(entity.get("shape") or "")
        if shape not in {"rounded_rectangle", "rounded_rect"}:
            continue
        intent = str(entity.get("shape_intent") or "")
        radius = entity.get("corner_radius_px")
        if not intent or (allowed_intents and intent not in allowed_intents):
            errors.append({"entity": entity.get("id"), "reason": "rounded_rectangle_requires_explicit_shape_intent", "intent": intent})
            continue
        if not isinstance(radius, (int, float)) or float(radius) < 0:
            errors.append({"entity": entity.get("id"), "reason": "rounded_rectangle_requires_nonnegative_corner_radius_px"})
            continue
    constraints = semantic.get("layout_constraints", {}) or {}
    non_overlap_pairs = constraints.get("non_overlap_pairs", []) or []
    seen_pairs: set[tuple[str, str]] = set()
    for raw_pair in non_overlap_pairs:
        if not isinstance(raw_pair, list) or len(raw_pair) != 2:
            errors.append({"reason": "non_overlap_pair_must_have_two_ids", "pair": raw_pair})
            continue
        left, right = map(str, raw_pair)
        pair = tuple(sorted((left, right)))
        if left == right or left not in entity_lookup or right not in entity_lookup:
            errors.append({"reason": "non_overlap_pair_must_reference_two_semantic_entities", "pair": raw_pair})
            continue
        if pair in seen_pairs:
            errors.append({"reason": "duplicate_non_overlap_pair", "pair": raw_pair})
            continue
        seen_pairs.add(pair)
        left_box, right_box = box(lookup[left]), box(lookup[right])
        if left_box and right_box and overlaps(left_box, right_box):
            errors.append({"reason": "declared_non_overlap_pair_overlaps_in_logical_map", "pair": raw_pair, "left_bbox": left_box, "right_bbox": right_box})

    allowed_families = set(config.get("design", {}).get("connectors", {}).get("allowed_families", []))
    for entity in entities:
        if entity.get("kind") != "connector":
            continue
        intent = entity.get("connector_intent") or {}
        if intent.get("semantic_topology_verified") is not True:
            errors.append({"entity": entity.get("id"), "reason": "connector_semantic_topology_must_be_explicitly_verified"})
        if intent.get("visual_route_reviewed") is not True:
            errors.append({"entity": entity.get("id"), "reason": "connector_route_must_be_visually_reviewed_by_host_agent"})
        if not str(intent.get("visual_route_decision") or "").strip():
            errors.append({"entity": entity.get("id"), "reason": "connector_visual_route_decision_missing"})
        family = str(intent.get("connector_family") or "")
        sources = list(intent.get("source_entities") or [])
        targets = list(intent.get("target_entities") or [])
        source_sides = list(intent.get("source_attachment_sides") or [])
        target_sides = list(intent.get("target_attachment_sides") or [])
        source_fractions = list(intent.get("source_attachment_fractions") or [])
        target_fractions = list(intent.get("target_attachment_fractions") or [])
        if family not in allowed_families:
            errors.append({"entity": entity.get("id"), "reason": "unsupported_connector_family", "family": family})
        if not sources or not targets:
            errors.append({"entity": entity.get("id"), "reason": "missing_connector_endpoints"})
        if any(str(value) not in lookup for value in [*sources, *targets]):
            errors.append({"entity": entity.get("id"), "reason": "connector_references_unknown_owner"})
        if len(source_sides) != len(sources) or len(target_sides) != len(targets):
            errors.append({"entity": entity.get("id"), "reason": "connector_side_cardinality_mismatch"})
        if len(source_fractions) != len(sources) or len(target_fractions) != len(targets):
            errors.append({"entity": entity.get("id"), "reason": "connector_fraction_cardinality_mismatch"})
        if any(not (0.0 <= float(value) <= 1.0) for value in [*source_fractions, *target_fractions]):
            errors.append({"entity": entity.get("id"), "reason": "connector_attachment_fraction_out_of_range"})
        if family in {"direct_flow", "orthogonal_dependency", "annotation_leader"} and (len(sources) != 1 or len(targets) != 1):
            errors.append({"entity": entity.get("id"), "reason": "one_to_one_family_has_non_one_to_one_endpoints"})
        if family == "merge_split" and len(sources) == 1 and len(targets) == 1:
            errors.append({"entity": entity.get("id"), "reason": "merge_split_requires_multiple_sources_or_targets"})
        if family in {"grouping_bracket", "grouping_brace"} and not intent.get("grouping_side"):
            errors.append({"entity": entity.get("id"), "reason": "grouping_family_requires_grouping_side"})
        route_mode = str(intent.get("route_mode") or "")
        allowed_route_modes = {"minimal_orthogonal", "authored_waypoints", "authored_geometry"}
        if route_mode not in allowed_route_modes:
            errors.append({"entity": entity.get("id"), "reason": "connector_requires_explicit_route_mode", "allowed": sorted(allowed_route_modes)})
        route_waypoints = list((entity.get("visual_constraints") or {}).get("route_waypoints_px") or [])
        if route_mode == "authored_waypoints" and not route_waypoints:
            errors.append({"entity": entity.get("id"), "reason": "authored_waypoints_route_requires_waypoints"})
        shared = len(sources) > 1 or len(targets) > 1
        if shared and intent.get("junction_hint") is None:
            errors.append({"entity": entity.get("id"), "reason": "shared_connector_requires_agent_authored_junction_hint"})
        if shared and route_mode != "minimal_orthogonal":
            errors.append({"entity": entity.get("id"), "reason": "shared_connector_route_mode_must_delegate_minimal_orthogonal_legs"})
        if intent.get("grouping_depth_px") is not None and float(intent.get("grouping_depth_px")) <= 0:
            errors.append({"entity": entity.get("id"), "reason": "grouping_depth_px_must_be_positive"})
        if family in {"grouping_bracket", "grouping_brace"} and intent.get("grouping_depth_px") is None:
            errors.append({"entity": entity.get("id"), "reason": "grouping_connector_requires_agent_authored_depth"})
        if family in {"grouping_bracket", "grouping_brace"} and route_mode != "authored_geometry":
            errors.append({"entity": entity.get("id"), "reason": "grouping_connector_route_mode_must_be_authored_geometry"})
        if family not in {"grouping_bracket", "grouping_brace"} and route_mode == "authored_geometry":
            errors.append({"entity": entity.get("id"), "reason": "authored_geometry_route_mode_is_for_grouping_connectors"})
        if intent.get("junction_style") not in {None, "none", "filled_circle"}:
            errors.append({"entity": entity.get("id"), "reason": "unsupported_junction_style", "value": intent.get("junction_style")})
        if intent.get("junction_style") is None:
            errors.append({"entity": entity.get("id"), "reason": "connector_requires_explicit_junction_style"})
        if intent.get("junction_diameter_px") is not None and float(intent.get("junction_diameter_px")) <= 0:
            errors.append({"entity": entity.get("id"), "reason": "junction_diameter_px_must_be_positive"})
        if intent.get("junction_style") == "filled_circle" and intent.get("junction_diameter_px") is None:
            errors.append({"entity": entity.get("id"), "reason": "filled_junction_requires_agent_authored_diameter"})
        arrowhead = (entity.get("visual_constraints") or {}).get("arrowhead_treatment")
        if arrowhead not in {"none", "triangle_at_target", "open_arrow_at_target"}:
            errors.append({"entity": entity.get("id"), "reason": "connector_requires_explicit_arrowhead_treatment", "allowed": ["none", "triangle_at_target", "open_arrow_at_target"]})
        if intent.get("directed") is False and arrowhead != "none":
            errors.append({"entity": entity.get("id"), "reason": "undirected_connector_cannot_have_target_arrowhead"})

    serialized = args.semantic_map.read_text(encoding="utf-8").lower()
    if "fixture://" in serialized:
        errors.append({"reason": "fixture_reference_forbidden_in_release_semantic_map"})

    report = {
        "evidence_type": "objective_semantic_map_structure",
        "image_size_px": [width, height],
        "entity_count": len(entities),
        "group_count": len(groups),
        "blocking_facts": errors,
        "agent_interpretation_required": True,
        "note": "No semantic or visual verdict is produced. A host-Agent reviewer must inspect the image, map, profile, and these facts together.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not errors else 2)


if __name__ == "__main__":
    main()
