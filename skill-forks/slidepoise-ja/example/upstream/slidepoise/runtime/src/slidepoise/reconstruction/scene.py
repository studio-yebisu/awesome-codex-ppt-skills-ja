"""Compile measured scene evidence and the reconstruction contract into a constructor scene."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from slidepoise.canvas import reconstruction_geometry

from slidepoise.reconstruction.conformance import validate_contract_consumption
from slidepoise.reconstruction.text_fit import (
    finalize_fitted_text_entities,
    fit_text_entities,
    resolve_text_style_policy,
)


def _content_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

def _transform_box(box: list[int], scale_xy: list[float], offset_y: int) -> list[int]:
    scale_x, scale_y = scale_xy
    return [round(box[0] * scale_x), round(box[1] * scale_y + offset_y), round(box[2] * scale_x), round(box[3] * scale_y)]


def _transform_point(point: list[float], scale_xy: list[float], offset_y: int, translation_px: tuple[float, float] = (0, 0)) -> list[float]:
    return [(point[0] + translation_px[0]) * scale_xy[0], (point[1] + translation_px[1]) * scale_xy[1] + offset_y]


def _transform_contours(
    contours: list[list[list[float]]], scale_xy: list[float], offset_y: int,
    translation_px: list[float] = (0, 0),
) -> list[list[list[float]]]:
    """Move OpenCV's source-image contour coordinates into scene coordinates.

    OpenCV returns absolute points in the accepted target image. Constructor scenes
    use full-slide coordinates after the generation-region transform. Keeping those
    coordinate spaces explicit prevents a renderer from guessing point ownership
    from a point's numeric value.
    """
    return [
        [_transform_point([float(x) + translation_px[0], float(y) + translation_px[1]], scale_xy, offset_y) for x, y in contour]
        for contour in contours
    ]


def _entity_box(entity: dict[str, Any] | None) -> list[float] | None:
    if not entity:
        return None
    measurement = entity.get("measurement", {})
    return measurement.get("layout_bbox", {}).get("px") or entity.get("bbox_hint")


def _resolved_entity_style(entity: dict[str, Any], design: dict[str, Any]) -> dict[str, Any]:
    """Merge an explicit semantic style token with Agent-authored style evidence.

    This is deterministic token application, not a visual judgement. A semantic token
    is used only when the semantic map explicitly assigns it. Agent-authored style_hint
    fields may override token defaults for the current slide.
    """
    hint = dict(entity.get("style_hint", {}) or {})
    token = entity.get("style_token") or hint.get("style_token")
    token_style = dict(design.get("semantic_style_tokens", {}).get(token, {}) or {}) if token else {}
    token_style.pop("text_color", None)
    token_style.pop("font_weight", None)
    token_style.pop("glyph_color", None)
    token_style.update({k: v for k, v in hint.items() if k != "style_token"})
    return token_style





def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _component_catalog(design: dict[str, Any]) -> tuple[Path, dict[str, dict[str, Any]]]:
    library = design.get("resource_catalogs", {}).get("components", {})
    configured = [value for value in library.get("catalogs", [library.get("catalog")]) if value]
    if not configured:
        raise ValueError("Resolved design has no selected-profile component catalog")
    by_id = {}
    for value in configured:
        path = Path(str(value)).expanduser().resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        for raw in (payload.get("items") or {}).values():
            identifier = str(raw.get("id", ""))
            if identifier in by_id:
                raise ValueError(f"Duplicate component ID across selected sets: {identifier}")
            record = copy.deepcopy(raw)
            if not record.get("path") and payload.get("native_source"):
                record["path"] = payload["native_source"]
            if str(record.get("path", "")).lower().endswith(".pptx") and not record.get("preview_path"):
                record["preview_path"] = str(Path(record["path"]).with_suffix(f".slide-{int(record.get('native_source_slide_number', 1))}.preview.png"))
            for key in ("path", "preview_path"):
                if record.get(key):
                    record[key] = str((path.parent / record[key]).resolve())
            if identifier:
                by_id[identifier] = record
    return path, by_id


def _component_record(component_id: Any, expected_kind: str, design: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if not component_id:
        return None, None
    catalog_path, by_id = _component_catalog(design)
    record = by_id.get(str(component_id))
    if record is None:
        raise ValueError(f"Unknown component_id {component_id!r}")
    if record.get("kind") != expected_kind:
        raise ValueError(f"Component {component_id!r} is {record.get('kind')!r}, not {expected_kind!r}")
    donor = catalog_path.parent / str(record.get("path") or "")
    preview = catalog_path.parent / str(record.get("preview_path") or "")
    if not donor.is_file() or not preview.is_file():
        raise FileNotFoundError(f"Component {component_id!r} is missing its native donor or preview")
    reference = {
        "component_id": str(component_id),
        "native_donor_path": str(donor.resolve()),
        "native_source_slide_number": int(record.get("native_source_slide_number", 1)),
        "preview_path": str(preview.resolve()),
        "grammar": copy.deepcopy(record.get("grammar") or {}),
        "adaptation_rules": list(record.get("adaptation_rules") or []),
    }
    return record, reference


def _resolve_icon_group_treatments(entities: list[dict[str, Any]], design: dict[str, Any]) -> dict[str, dict[str, Any]]:
    icon_rules = dict(design.get("profile_hard_rules", {}).get("icons", {}) or {})
    treatments = {str(item.get("id")): item for item in (icon_rules.get("proxy_treatments") or []) if item.get("id")}
    groups: dict[str, str] = {}
    for entity in entities:
        if entity.get("kind") not in {"icon", "icon_slot"}:
            continue
        group = str(entity.get("icon_treatment_group") or "").strip()
        treatment_id = str(entity.get("icon_treatment") or "").strip()
        if not group or not treatment_id:
            raise ValueError(f"Icon {entity.get('id')} requires icon_treatment_group and icon_treatment")
        if treatment_id not in treatments:
            raise ValueError(f"Icon {entity.get('id')} uses unknown icon treatment {treatment_id!r}")
        prior = groups.setdefault(group, treatment_id)
        if prior != treatment_id:
            raise ValueError(f"Icon treatment group {group!r} mixes {prior!r} and {treatment_id!r}")
    return {group: treatments[treatment_id] for group, treatment_id in groups.items()}

def _round_rect_adjustment(entity: dict[str, Any], transformed_box: list[int], design: dict[str, Any], scale_xy: list[float]) -> tuple[float, int]:
    """Resolve an Agent-observed corner radius into a PowerPoint round-rect adjustment.

    The Agent owns shape intent and observed radius. The runtime only applies the
    technical PowerPoint radius limit and converts the result into the DrawingML
    adjustment used by PowerPoint's editable roundRect preset.
    """
    policy = design.get("shape_geometry", {}).get("rounding", {})
    intent = str(entity.get("shape_intent") or "")
    if not intent:
        raise ValueError(f"Rounded rectangle {entity.get('id')} is missing host-Agent shape_intent")
    raw_radius = entity.get("corner_radius_px")
    if not isinstance(raw_radius, (int, float)) or float(raw_radius) < 0:
        raise ValueError(f"Rounded rectangle {entity.get('id')} requires nonnegative corner_radius_px")
    radius = float(raw_radius) * min(float(scale_xy[0]), float(scale_xy[1]))
    short_side = max(1.0, min(float(transformed_box[2]), float(transformed_box[3])))
    allowed = set(policy.get("intent_values", []))
    if allowed and intent not in allowed:
        raise ValueError(f"Rounded rectangle {entity.get('id')} uses unsupported shape_intent {intent!r}")
    radius = min(radius, short_side * 0.5)
    adjustment = max(0, min(50000, round(radius / short_side * 100000)))
    return radius, adjustment

def _semantic_owner_box(identifier: str, entity_by_id: dict[str, Any], group_by_id: dict[str, Any]) -> list[float] | None:
    entity = entity_by_id.get(identifier)
    if entity:
        return _entity_box(entity)
    group = group_by_id.get(identifier)
    if group and group.get("bbox_hint"):
        return group["bbox_hint"]
    return None


def _union_owner_boxes(ids: list[str], entity_by_id: dict[str, Any], group_by_id: dict[str, Any]) -> list[float] | None:
    boxes=[_semantic_owner_box(i,entity_by_id,group_by_id) for i in ids]
    boxes=[b for b in boxes if b]
    if not boxes: return None
    x=min(float(b[0]) for b in boxes); y=min(float(b[1]) for b in boxes)
    r=max(float(b[0])+float(b[2]) for b in boxes); bot=max(float(b[1])+float(b[3]) for b in boxes)
    return [x,y,r-x,bot-y]


def _project_anchor_to_owner_boundary(
    anchor: list[float],
    owner_box: list[float] | None,
    reference: list[float] | None = None,
    side: str | None = None,
) -> list[float]:
    if not owner_box:
        return anchor
    x, y, w, h = [float(value) for value in owner_box]
    hint_x, hint_y = float(anchor[0]), float(anchor[1])
    side = (side or "").lower()
    if side == "left":
        return [x, min(max(hint_y, y), y + h)]
    if side == "right":
        return [x + w, min(max(hint_y, y), y + h)]
    if side == "top":
        return [min(max(hint_x, x), x + w), y]
    if side == "bottom":
        return [min(max(hint_x, x), x + w), y + h]

    cx = x + w / 2.0
    cy = y + h / 2.0
    if reference:
        dx = float(reference[0]) - cx
        dy = float(reference[1]) - cy
    else:
        dx = hint_x - cx
        dy = hint_y - cy
    if abs(dx) >= abs(dy):
        px = x + w if dx >= 0 else x
        py = min(max(hint_y, y), y + h)
    else:
        px = min(max(hint_x, x), x + w)
        py = y + h if dy >= 0 else y
    return [px, py]

def _anchor_on_owner_side(box: list[float], side: str, fraction: float) -> list[float]:
    x, y, width, height = map(float, box)
    fraction = max(0.0, min(1.0, float(fraction)))
    side = str(side).lower()
    if side == "left":
        return [x, y + height * fraction]
    if side == "right":
        return [x + width, y + height * fraction]
    if side == "top":
        return [x + width * fraction, y]
    if side == "bottom":
        return [x + width * fraction, y + height]
    raise ValueError(f"Unsupported connector attachment side {side!r}")


def _semantic_connector_points(plan: dict[str, Any], entity_by_id: dict[str, Any], group_by_id: dict[str, Any]) -> tuple[list[list[float]], list[list[float]], list[list[float]]]:
    """Resolve exact endpoint ports from Agent-authored semantic owners/sides/fractions.

    OpenCV/raster anchor hints are evidence only. Once semantic endpoint ownership is
    audited, owner geometry plus the authored side/fraction becomes placement authority.
    Owner geometry plus authored side/fraction is placement authority, so native
    connector endpoints remain stable even when the generated raster path was wrong.
    """
    intent = plan.get("relationship_intent", {})
    sources = list(intent.get("source_entities") or [])
    targets = list(intent.get("target_entities") or [])
    source_sides = list(intent.get("source_attachment_sides") or [])
    target_sides = list(intent.get("target_attachment_sides") or [])
    source_fractions = list(intent.get("source_attachment_fractions") or [])
    target_fractions = list(intent.get("target_attachment_fractions") or [])
    if len(source_sides) != len(sources) or len(target_sides) != len(targets):
        raise ValueError(f"Connector {plan.get('entity_id')} attachment-side cardinality mismatch")
    if len(source_fractions) != len(sources) or len(target_fractions) != len(targets):
        raise ValueError(f"Connector {plan.get('entity_id')} attachment-fraction cardinality mismatch")

    snapped_sources: list[list[float]] = []
    for identifier, side, fraction in zip(sources, source_sides, source_fractions):
        owner = _semantic_owner_box(str(identifier), entity_by_id, group_by_id)
        if owner is None:
            raise ValueError(f"Connector {plan.get('entity_id')} source owner has no geometry: {identifier}")
        snapped_sources.append(_anchor_on_owner_side(owner, str(side), float(fraction)))

    snapped_targets: list[list[float]] = []
    for identifier, side, fraction in zip(targets, target_sides, target_fractions):
        owner = _semantic_owner_box(str(identifier), entity_by_id, group_by_id)
        if owner is None:
            raise ValueError(f"Connector {plan.get('entity_id')} target owner has no geometry: {identifier}")
        snapped_targets.append(_anchor_on_owner_side(owner, str(side), float(fraction)))

    explicit_hint = intent.get("junction_hint")
    if explicit_hint is not None:
        junctions = [list(map(float, explicit_hint))]
    else:
        junctions = []
    return snapped_sources, snapped_targets, junctions


def _axis_for_side(side: str | None) -> str | None:
    side = str(side or "").lower()
    if side in {"left", "right"}:
        return "horizontal"
    if side in {"top", "bottom"}:
        return "vertical"
    return None


def _remove_redundant_route_points(points: list[list[float]]) -> list[list[float]]:
    unique: list[list[float]] = []
    for point in points:
        p = [float(point[0]), float(point[1])]
        if unique and abs(p[0] - unique[-1][0]) < 0.01 and abs(p[1] - unique[-1][1]) < 0.01:
            continue
        unique.append(p)
    if len(unique) <= 2:
        return unique
    changed = True
    while changed and len(unique) > 2:
        changed = False
        result = [unique[0]]
        for index in range(1, len(unique) - 1):
            prev = result[-1]
            cur = unique[index]
            nxt = unique[index + 1]
            collinear_vertical = abs(prev[0] - cur[0]) < 0.01 and abs(cur[0] - nxt[0]) < 0.01
            collinear_horizontal = abs(prev[1] - cur[1]) < 0.01 and abs(cur[1] - nxt[1]) < 0.01
            if collinear_vertical or collinear_horizontal:
                changed = True
                continue
            result.append(cur)
        result.append(unique[-1])
        unique = result
    return unique


def _minimal_orthogonal_route(
    start: list[float],
    end: list[float],
    *,
    start_side: str | None = None,
    end_side: str | None = None,
    forced_points: list[list[float]] | None = None,
) -> list[list[float]]:
    """Return the least-bend orthogonal route that respects endpoint-side semantics.

    Semantic endpoint sides constrain the first and final segment axes. Explicit
    forced points are reserved for Agent-audited routing corridors / semantic
    junctions; otherwise raster detours are discarded.
    """
    start = [float(start[0]), float(start[1])]
    end = [float(end[0]), float(end[1])]
    start_axis = _axis_for_side(start_side)
    end_axis = _axis_for_side(end_side)
    if forced_points:
        return _remove_redundant_route_points([start, *forced_points, end])

    same_x = abs(start[0] - end[0]) < 0.01
    same_y = abs(start[1] - end[1]) < 0.01
    if same_x and (start_axis in {None, "vertical"}) and (end_axis in {None, "vertical"}):
        return [start, end]
    if same_y and (start_axis in {None, "horizontal"}) and (end_axis in {None, "horizontal"}):
        return [start, end]

    # One-bend L routes. Each candidate is accepted only when its first and
    # final segment axes agree with the audited endpoint sides.
    candidates = [
        [start, [end[0], start[1]], end],  # horizontal then vertical
        [start, [start[0], end[1]], end],  # vertical then horizontal
    ]
    for candidate in candidates:
        candidate = _remove_redundant_route_points(candidate)
        if len(candidate) < 2:
            continue
        first = candidate[1]
        last_prev = candidate[-2]
        first_axis = "horizontal" if abs(first[1] - start[1]) < 0.01 else "vertical"
        last_axis = "horizontal" if abs(end[1] - last_prev[1]) < 0.01 else "vertical"
        if start_axis not in {None, first_axis}:
            continue
        if end_axis not in {None, last_axis}:
            continue
        return candidate

    # Matching endpoint axes may require a two-bend dogleg. Put the middle
    # corridor halfway between endpoints unless the Agent supplies a semantic
    # corridor/junction explicitly.
    if start_axis == end_axis == "horizontal":
        mid_x = (start[0] + end[0]) / 2.0
        return _remove_redundant_route_points([start, [mid_x, start[1]], [mid_x, end[1]], end])
    if start_axis == end_axis == "vertical":
        mid_y = (start[1] + end[1]) / 2.0
        return _remove_redundant_route_points([start, [start[0], mid_y], [end[0], mid_y], end])

    # If one endpoint has no side constraint, choose the one-bend route that
    # satisfies the constrained endpoint. The host Agent explicitly delegates
    # this minimal route compilation through route_mode.
    if start_axis == "horizontal" or end_axis == "vertical":
        return _remove_redundant_route_points([start, [end[0], start[1]], end])
    if start_axis == "vertical" or end_axis == "horizontal":
        return _remove_redundant_route_points([start, [start[0], end[1]], end])
    return _remove_redundant_route_points([start, [end[0], start[1]], end])


def _connector_routes(
    plan: dict[str, Any],
    source_points: list[list[float]],
    target_points: list[list[float]],
    junction_points: list[list[float]],
) -> tuple[list[list[list[float]]], list[list[list[float]]]]:
    source_sides = list(plan.get("source_attachment_sides") or [])
    target_sides = list(plan.get("target_attachment_sides") or [])
    family=str(plan.get("connector_family") or "direct_flow")
    if family in {"grouping_bracket", "grouping_brace"}:
        if plan.get("route_mode") != "authored_geometry":
            raise ValueError(f"Grouping connector {plan['entity_id']} requires authored_geometry route mode")
        return [], []
    shared = len(source_points) > 1 or len(target_points) > 1
    route_mode = str(plan.get("route_mode") or "")
    if route_mode not in {"minimal_orthogonal", "authored_waypoints"}:
        raise ValueError(f"Connector {plan['entity_id']} requires an explicit route_mode")
    if shared:
        if route_mode != "minimal_orthogonal":
            raise ValueError(f"Shared connector {plan['entity_id']} requires minimal_orthogonal route mode")
        if not junction_points:
            raise ValueError(f"Shared connector {plan['entity_id']} requires an Agent-audited semantic junction")
        junction = junction_points[0]
        source_routes = [
            _minimal_orthogonal_route(
                source,
                junction,
                start_side=source_sides[index] if index < len(source_sides) else None,
            )
            for index, source in enumerate(source_points)
        ]
        target_routes = [
            _minimal_orthogonal_route(
                junction,
                target,
                end_side=target_sides[index] if index < len(target_sides) else None,
            )
            for index, target in enumerate(target_points)
        ]
        return source_routes, target_routes

    if len(source_points) == 1 and len(target_points) == 1:
        if not plan.get("route_visual_review", {}).get("reviewed"):
            raise ValueError(f"Connector {plan['entity_id']} requires a host-Agent visual route review")
        forced = list(plan.get("route_waypoints_px") or []) or None
        if route_mode == "authored_waypoints" and not forced:
            raise ValueError(f"Connector {plan['entity_id']} authored_waypoints route has no waypoints")
        route = _minimal_orthogonal_route(
            source_points[0],
            target_points[0],
            start_side=source_sides[0] if source_sides else None,
            end_side=target_sides[0] if target_sides else None,
            forced_points=forced,
        )
        return [], [route]
    return [], []

def _svg_ratio(path: Path) -> float:
    text = path.read_text(encoding="utf-8", errors="ignore")[:6000]
    match = re.search(r"viewBox=[\"']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)", text)
    if match and float(match.group(2)):
        return float(match.group(1)) / float(match.group(2))
    return 1.0


def _image_ratio(path: Path) -> float:
    if path.suffix.lower() == ".svg":
        return _svg_ratio(path)
    from PIL import Image

    with Image.open(path) as image:
        return image.width / image.height if image.height else 1.0


def _contain(box: list[int], ratio: float, inset_fraction: float = 0.14) -> list[int]:
    x, y, width, height = box
    available_width = width * (1 - 2 * inset_fraction)
    available_height = height * (1 - 2 * inset_fraction)
    final_width = min(available_width, available_height * ratio)
    final_height = final_width / ratio
    return [round(x + (width - final_width) / 2), round(y + (height - final_height) / 2), round(final_width), round(final_height)]


def _text_style(entity: dict[str, Any], fitted: dict[str, Any] | None, design: dict[str, Any], scale_y: float = 1.0) -> dict[str, Any]:
    hint = entity.get("style_hint", {})
    defaults = design.get("style", {})
    role_policy = resolve_text_style_policy(entity, design)
    family = hint.get("font_family") or role_policy.get("font_family") or defaults.get("body_font", "Arial")
    if fitted is None:
        raise ValueError(f"Text entity {entity.get('id')} has no finalized Agent-targeted fit record")
    size_px = float(fitted["font_size_px"])
    insets = fitted.get("insets_px", {})
    return {
        "font_family": fitted.get("font_family", family),
        "font_size_px": size_px * scale_y,
        "font_size_pt": fitted.get("font_size_pt"),
        "font_weight": "bold" if fitted.get("bold") else "regular",
        "italic": bool(fitted.get("italic", False)),
        "char_spacing_px": float(hint.get("char_spacing_px", 0)) * scale_y,
        "color": fitted.get("color", hint.get("color", "#111111")),
        "alignment": fitted.get("alignment", hint.get("alignment", "left")),
        "vertical_alignment": fitted.get("vertical_alignment", "top"),
        "margins_px": [insets.get("left", 0) * scale_y, insets.get("top", 0) * scale_y, insets.get("right", 0) * scale_y, insets.get("bottom", 0) * scale_y],
        "line_spacing_multiple": fitted.get("line_spacing", 1.0),
        "paragraph_spacing_px": fitted.get("paragraph_space_after_px", 0),
        "autofit": "none",
        "outer_geometry_is_fixed": True,
    }


def _apply_explicit_z_order(objects: list[dict[str, Any]], relations: list[dict[str, Any]]) -> None:
    """Validate the Agent-authored layer order without rewriting it."""
    by_id = {item["id"]: item for item in objects}
    usable = [item for item in relations if item.get("back") in by_id and item.get("front") in by_id]
    conflicts = [
        f"{relation['back']} behind {relation['front']}"
        for relation in usable
        if by_id[relation["front"]]["z"] <= by_id[relation["back"]]["z"]
    ]
    if conflicts:
        raise ValueError(
            "Agent-authored z values conflict with explicit stacking relationships: "
            + ", ".join(conflicts)
        )


def build_reconstruction_scene(
    *,
    measured_scene: dict[str, Any],
    contract: dict[str, Any],
    design: dict[str, Any],
    slide_id: str,
) -> dict[str, Any]:
    speaker_notes = contract.get("speaker_notes", [])
    if not isinstance(speaker_notes, list) or any(not isinstance(note, str) for note in speaker_notes):
        raise ValueError("contract.speaker_notes must be an array of strings")
    geometry = reconstruction_geometry(design, [measured_scene["source"]["width_px"], measured_scene["source"]["height_px"]])
    for key, expected in geometry.items():
        if contract.get(key) != expected:
            raise ValueError(f"Reconstruction contract {key} disagrees with the current source and resolved frame. Rebuild the contract.")
    dimensions = list(contract.get("full_slide_dimensions_px") or [measured_scene["source"]["width_px"], measured_scene["source"]["height_px"]])
    transform = contract.get("coordinate_transform_to_full_slide", {})
    offset_y = int((transform.get("translation_px") or transform.get("full_slide_offset_px") or [0, 0])[1])
    scale_xy = [float(value) for value in transform.get("scale_xy", [1, 1])]
    asset_mappings = {mapping["entity_id"]: mapping for mapping in contract.get("canonical_asset_mappings", [])}
    connector_plans = {plan["entity_id"]: plan for plan in contract.get("connector_reconstruction_plans", [])}
    connector_configuration = contract.get("connector_configuration", design.get("connectors", {}))
    working_scene = copy.deepcopy(measured_scene)
    units = {unit["id"]: unit for unit in contract.get("reconstruction_units", [])}
    emitting_entities = [entity for entity in working_scene["entities"] if units.get(entity["id"], {}).get("emits_ppt_object") is not False]
    icon_group_treatments = _resolve_icon_group_treatments(emitting_entities, design)
    text_overrides = dict(contract.get("text_bbox_overrides", {}))
    for entity in working_scene.get("entities", []):
        if entity.get("kind") == "text" and entity.get("id") in text_overrides:
            entity.setdefault("measurement", {}).setdefault("layout_bbox", {})["px"] = list(text_overrides[entity["id"]])
            entity["bbox_hint"] = list(text_overrides[entity["id"]])
    entity_by_id = {entity["id"]: entity for entity in working_scene.get("entities", [])}
    group_by_id = {group["id"]: group for group in working_scene.get("groups", [])}
    fitted_text = {record["id"]: record for record in contract.get("fitted_text_contracts", [])}
    if not fitted_text:
        fitted_text, _ = fit_text_entities(emitting_entities, design)
    # The renderer's 40/3-inch canvas is exactly 960 points (12,192,000 EMU).
    points_per_px = scale_xy[1] * 960 / dimensions[0]
    text_policy = design.get("text_reconstruction", {})
    fitted_text, text_fit_report = finalize_fitted_text_entities(
        emitting_entities,
        design,
        fitted_text,
        points_per_px=points_per_px,
        quantization_step_pt=float(text_policy.get("font_size_quantization_pt", 0.5)),
        technical_minimum_pt=float(text_policy.get("technical_font_size_step_pt", 0.5)),
    )
    units = {unit["id"]: unit for unit in contract.get("reconstruction_units", [])}
    objects: list[dict[str, Any]] = []
    for entity in working_scene["entities"]:
        entity_id = entity["id"]
        unit = units.get(entity_id)
        if unit and unit.get("emits_ppt_object") is False:
            continue
        kind = entity["kind"]
        box = _transform_box(entity["measurement"]["layout_bbox"]["px"], scale_xy, offset_y)
        if not isinstance(entity.get("z"), (int, float)):
            raise ValueError(f"Emitting entity {entity_id} requires host-Agent-authored z order")
        z = float(entity["z"])
        if kind == "text":
            objects.append({
                "id": entity_id,
                "kind": "textbox",
                "bbox_px": box,
                "text": fitted_text.get(entity_id, {}).get("authored_text", entity.get("authored_text", entity.get("text", ""))),
                "style": _text_style(entity, fitted_text.get(entity_id), design, scale_xy[1]),
                "paragraphs": fitted_text.get(entity_id, {}).get("authored_text", entity.get("authored_text", entity.get("text", ""))).split("\n"),
                "bullet_style": entity.get("bullet_style"),
                "semantic_role": entity.get("role"),
                "parent_id": entity.get("parent_id") or entity.get("parent"),
                "allow_boundary_crossing": entity.get("allow_boundary_crossing") is True,
                "z": z,
            })
        elif kind in {"icon", "icon_slot"}:
            mapping = asset_mappings.get(entity_id)
            if not mapping:
                raise ValueError(f"Icon entity {entity_id} has no canonical asset mapping")
            path = Path(mapping.get("selected_asset_path", ""))
            if not path.exists():
                raise FileNotFoundError(f"Canonical asset for {entity_id} does not exist: {path}")
            current_slot = entity["measurement"]["layout_bbox"]["px"]
            slot = _transform_box(current_slot, scale_xy, offset_y)
            selected_asset_id = str(mapping.get("selected_asset_id", ""))
            entity_hint = dict(entity.get("style_hint", {}) or {})
            slot_surface = dict(entity.get("slot_surface", {}) or {})
            token_name = slot_surface.get("style_token") or entity.get("style_token") or entity_hint.get("style_token")
            token_style = dict(design.get("semantic_style_tokens", {}).get(token_name, {}) or {}) if token_name else {}

            # The logical slot always exists for spacing/measurement. A visible slot
            # surface/frame is emitted only when the host Agent observed one in the
            # accepted generated image. Filled and outline-only treatments are both
            # supported; there is no automatic pictogram background.
            surface_visible = bool(slot_surface.get("visible", bool(slot_surface)))
            if surface_visible:
                surface_hint = dict(slot_surface.get("style_hint", {}) or {})
                surface_shape = str(slot_surface.get("shape", "rectangle"))
                surface_style = {
                    "fill": surface_hint.get("fill", token_style.get("fill", "none")),
                    "stroke": surface_hint.get("stroke", surface_hint.get("border", token_style.get("border", token_style.get("stroke", "none")))),
                    "stroke_width_px": surface_hint.get("stroke_width_px", token_style.get("stroke_width_px", 1)),
                }
                surface_object = {
                    "id": f"{entity_id}.icon_slot_surface",
                    "kind": "shape",
                    "shape": surface_shape,
                    "bbox_px": slot,
                    "style": surface_style,
                    "semantic_role": "icon_slot_surface",
                    "z": z - 1,
                }
                if surface_shape in {"rounded_rectangle", "rounded_rect"}:
                    surface_object["shape"] = "rounded_rectangle"
                    surface_geometry = {
                        "id": f"{entity_id}.icon_slot_surface",
                        "shape_intent": slot_surface.get("shape_intent", "ordinary_container"),
                        "corner_radius_px": slot_surface.get("corner_radius_px", 0),
                        "user_explicit_geometry_override": slot_surface.get("user_explicit_geometry_override", False),
                    }
                    radius_px, adjustment = _round_rect_adjustment(surface_geometry, slot, design, scale_xy)
                    surface_object["corner_radius_px"] = round(radius_px, 3)
                    surface_object["round_rect_adjustment"] = adjustment
                    surface_object["shape_intent"] = surface_geometry["shape_intent"]
                objects.append(surface_object)

            treatment_group = str(entity.get("icon_treatment_group"))
            treatment = icon_group_treatments[treatment_group]
            if not bool(mapping.get("treatment_recolorable")):
                raise ValueError(
                    f"Icon {entity_id} belongs to treatment group {treatment_group!r} but its selected asset is not declared treatment-recolorable"
                )
            glyph_color = treatment.get("glyph_color", treatment.get("glyph"))
            glyph_gradient = treatment.get("glyph_gradient")
            if "icon_inset_fraction" not in entity_hint:
                raise ValueError(f"Icon {entity.get('id')} requires host-Agent-authored icon_inset_fraction")
            inset_fraction = float(entity_hint["icon_inset_fraction"])
            objects.append({
                "id": entity_id,
                "kind": "image",
                "bbox_px": _contain(slot, _image_ratio(path), inset_fraction),
                "source_path": str(path.resolve()),
                "recolor": glyph_color,
                "recolor_gradient": glyph_gradient,
                "recolor_mode": mapping.get("recolor_mode"),
                "icon_treatment_group": treatment_group,
                "icon_treatment": treatment.get("id"),
                "selected_asset_id": selected_asset_id,
                "fit": "contain",
                "preserve_aspect_ratio": True,
                "semantic_role": entity.get("role"),
                "z": z,
            })
        elif kind == "image":
            image = entity["measurement"].get("image_object", {})
            mapping = asset_mappings.get(entity_id)
            source = mapping.get("selected_asset_path") if mapping else image.get("screenshot_crop_absolute")
            if source:
                source_path = Path(source)
                if not source_path.is_file():
                    raise FileNotFoundError(f"Raster source for {entity_id} does not exist: {source_path}")
                source_hash = None if mapping else image.get("raster_source_facts", {}).get("sha256")
                if source_hash and hashlib.sha256(source_path.read_bytes()).hexdigest() != source_hash:
                    raise ValueError(f"Raster source for {entity_id} changed after measurement")
                fit_mode = "contain" if mapping else str(image.get("crop_mode", "fill"))
                target_box = _contain(box, _image_ratio(source_path), 0) if (mapping or fit_mode == "contain") else box
                objects.append({
                    "id": entity_id,
                    "kind": "image",
                    "bbox_px": target_box,
                    "source_path": str(source_path.resolve()),
                    **({"source_sha256": source_hash} if source_hash else {}),
                    "selected_asset_id": mapping.get("selected_asset_id") if mapping else None,
                    "fit": fit_mode,
                    "preserve_aspect_ratio": True,
                    "semantic_role": entity.get("role"),
                    "z": z,
                })
        elif kind == "connector":
            plan = connector_plans.get(entity_id)
            if plan:
                stroke_style = dict(plan.get("stroke_style", {}))
                configured_stroke = connector_configuration.get("stroke", {})
                # The accepted image/Agent-authored style evidence is authoritative for
                # connector appearance unless no local style was supplied. Configuration
                # provides defaults, not a forced recoloring of every relationship.
                stroke_style.setdefault("color", stroke_style.get("stroke", configured_stroke.get("color", "#222222")))
                stroke_style.setdefault("width_px", stroke_style.get("stroke_width_px", configured_stroke.get("width_px", 3)))
                stroke_style.setdefault("dash", configured_stroke.get("dash", "solid"))
                arrowhead_config = {"powerpoint_size": "med", **connector_configuration.get("arrowhead", {}), **plan.get("arrowhead", {})}
                stroke_style["width_px"] = max(0.5, float(stroke_style.get("width_px", configured_stroke.get("width_px", 3))))
                source_points, target_points, junction_points = _semantic_connector_points(plan, entity_by_id, group_by_id)
                source_routes, target_routes = _connector_routes(plan, source_points, target_points, junction_points)
                objects.append({
                    "id": entity_id,
                    "kind": "connector_graph",
                    "sources_px": [_transform_point(point, scale_xy, offset_y) for point in source_points],
                    "targets_px": [_transform_point(point, scale_xy, offset_y) for point in target_points],
                    "junctions_px": [_transform_point(point, scale_xy, offset_y) for point in junction_points],
                    "route": plan.get("connector_family", "direct_flow"),
                    "style": stroke_style,
                    "arrowhead_treatment": plan["arrowhead_treatment"],
                    "arrowhead": arrowhead_config,
                    "junction_style": {"style": plan["junction_treatment"], "diameter_px": plan.get("junction_diameter_px")},
                    "routing_constraints": connector_configuration.get("routing", {}),
                    "route_visual_review": plan.get("route_visual_review", {}),
                    "semantic_intent": plan["relationship_intent"],
                    "connector_family": plan.get("connector_family", "direct_flow"),
                    "grouping_side": plan.get("relationship_intent", {}).get("grouping_side"),
                    "grouping_depth_px": plan.get("grouping_depth_px"),
                    "grouping_bbox_px": (_transform_box(_union_owner_boxes(plan.get("relationship_intent", {}).get("source_entities", []), entity_by_id, group_by_id), scale_xy, offset_y) if _union_owner_boxes(plan.get("relationship_intent", {}).get("source_entities", []), entity_by_id, group_by_id) else None),
                    "source_attachment_sides": list(plan.get("source_attachment_sides") or []),
                    "target_attachment_sides": list(plan.get("target_attachment_sides") or []),
                    "source_routes_px": [
                        [_transform_point(point, scale_xy, offset_y) for point in route]
                        for route in source_routes
                    ],
                    "target_routes_px": [
                        [_transform_point(point, scale_xy, offset_y) for point in route]
                        for route in target_routes
                    ],
                    "source_path_representations": [
                        "native_connector" if len(route) == 2 else "editable_freeform" for route in source_routes
                    ],
                    "target_path_representations": [
                        "native_connector" if len(route) == 2 else "editable_freeform" for route in target_routes
                    ],
                    "z": z,
                })
        elif kind == "table":
            component_record, component_reference = _component_record(entity.get("component_id"), "table", design)
            actual_structure = dict(entity.get("structure") or entity.get("table_structure") or {})
            defaults = dict((component_record or {}).get("constructor_defaults") or {})
            structure = _deep_merge(defaults.get("table_structure", {}), actual_structure)
            # Cell pixel measurements belong to the same source canvas as the
            # table bounds. Office-point margins already have physical units.
            for row in structure.get("rows", []):
                for cell in row:
                    if isinstance(cell, dict) and "margin_px" in cell:
                        margin = cell["margin_px"]
                        if isinstance(margin, (int, float)) and not isinstance(margin, bool):
                            margin = [margin] * 4
                        if (not isinstance(margin, list) or len(margin) != 4
                                or any(isinstance(v, bool) or not isinstance(v, (int, float))
                                       or v < 0 for v in margin)):
                            raise ValueError("Table cell margin_px must contain four nonnegative pixel values")
                        cell["margin_px"] = [v * scale_xy[1 if i % 2 == 0 else 0]
                                             for i, v in enumerate(margin)]
            table_style = _deep_merge(defaults.get("table_style", {}), actual_structure.get("table_style", {}))
            if table_style:
                structure["table_style"] = table_style
            objects.append({
                "id": entity_id, "kind": "table", "bbox_px": box, "structure": structure,
                "style": _resolved_entity_style(entity, design), "component_id": entity.get("component_id"),
                "component_reference": component_reference, "z": z,
            })
        elif kind == "chart":
            component_record, component_reference = _component_record(entity.get("component_id"), "chart", design)
            defaults = dict((component_record or {}).get("constructor_defaults") or {})
            chart_structure = _deep_merge(defaults.get("chart_structure", {}), dict(entity.get("chart_structure") or {}))
            data_defaults = design.get("data_visualization", {})
            if not chart_structure.get("colors"):
                default_colors = data_defaults.get("default_series_colors", [])
                if default_colors:
                    chart_structure["colors"] = list(default_colors)
            chart_structure.setdefault("title_font_family", data_defaults.get("chart_title_font", design.get("style", {}).get("display_font", "Georgia")))
            chart_structure.setdefault("data_font_family", data_defaults.get("data_font", design.get("style", {}).get("body_font", "Arial")))
            if chart_structure.get("show_value_gridlines") is True and not chart_structure.get("gridline_color") and data_defaults.get("gridline_color"):
                chart_structure["gridline_color"] = data_defaults.get("gridline_color")
            objects.append({
                "id": entity_id, "kind": "chart", "bbox_px": box, "structure": chart_structure,
                "style": _resolved_entity_style(entity, design), "component_id": entity.get("component_id"),
                "component_reference": component_reference, "z": z,
            })
        elif kind == "novel_visual":
            commands = []
            for command in entity.get("path_commands_px", []):
                item = {"op": command["op"]}
                for key in ("point", "control1", "control2"):
                    if key in command:
                        item[key] = _transform_point(command[key], scale_xy, offset_y, entity["measurement"].get("layout_translation_px", [0, 0]))
                commands.append(item)
            contours = _transform_contours(entity["measurement"].get("contours_px", []), scale_xy, offset_y, entity["measurement"].get("layout_translation_px", [0, 0]))
            if not commands and not contours:
                raise ValueError(f"Novel visual {entity_id} has no authored path or measured contour evidence")
            objects.append({
                "id": entity_id,
                "kind": "freeform",
                "bbox_px": box,
                "path_commands_px": commands,
                "contours_px": contours,
                "coordinates": "absolute",
                "style": _resolved_entity_style(entity, design),
                "z": z,
            })
        else:
            shape = entity.get("shape")
            if not shape:
                raise ValueError(f"Shape entity {entity_id} requires an explicit shape")
            shape = {"rounded_rect": "rounded_rectangle", "circle": "ellipse"}.get(shape, shape)
            if shape in {"rectangle", "line", "parallelogram", "trapezoid", "ellipse", "rounded_rectangle"}:
                shape_object = {"id": entity_id, "kind": "shape", "shape": shape, "bbox_px": box, "style": _resolved_entity_style(entity, design), "allow_text_crossing": entity.get("allow_text_crossing") is True, "structural_boundary": entity.get("structural_boundary") is True, "z": z}
                if shape == "rounded_rectangle":
                    radius_px, adjustment = _round_rect_adjustment(entity, box, design, scale_xy)
                    shape_object["corner_radius_px"] = round(radius_px, 3)
                    shape_object["round_rect_adjustment"] = adjustment
                    shape_object["shape_intent"] = entity.get("shape_intent")
                objects.append(shape_object)
            else:
                commands = []
                for command in entity.get("path_commands_px", []):
                    item = {"op": command["op"]}
                    for key in ("point", "control1", "control2"):
                        if key in command:
                            item[key] = _transform_point(command[key], scale_xy, offset_y, entity["measurement"].get("layout_translation_px", [0, 0]))
                    commands.append(item)
                contours = _transform_contours(entity["measurement"].get("contours_px", []), scale_xy, offset_y, entity["measurement"].get("layout_translation_px", [0, 0]))
                objects.append({"id": entity_id, "kind": "freeform", "bbox_px": box, "path_commands_px": commands, "contours_px": contours, "coordinates": "absolute", "style": _resolved_entity_style(entity, design), "z": z})
    _apply_explicit_z_order(objects, contract.get("z_order_relations", []))
    source_by_entity = {
        entity["id"]: entity.get("authoritative_source_path")
        for entity in measured_scene.get("entities", [])
        if entity.get("authoritative_source_path")
    }
    for item in objects:
        source_path = source_by_entity.get(item["id"])
        if source_path:
            item["source_references"] = [{"authoritative_source_path": source_path}]
    objects = sorted(objects, key=lambda item: item["z"])
    conformance = validate_contract_consumption(
        measured_scene=working_scene,
        contract=contract,
        objects=objects,
        scale_xy=scale_xy,
        offset_y=offset_y,
    )
    sources = []
    source_image = measured_scene.get("source", {}).get("path") or measured_scene.get("source", {}).get("image_path")
    if source_image:
        sources.append(f"Generated target visual: {source_image}")
    for mapping in contract.get("canonical_asset_mappings", []):
        asset_path = mapping.get("selected_asset_path")
        asset_id = mapping.get("selected_asset_id")
        if asset_path:
            sources.append(f"Canonical asset {asset_id}: {asset_path}")
    for entity_id, source_path in sorted(source_by_entity.items()):
        sources.append(f"Object {entity_id}: authoritative source {source_path}")
    for item in objects:
        reference = item.get("component_reference")
        if reference:
            sources.append(
                f"Component {reference['component_id']}: native donor {reference['native_donor_path']} slide {reference['native_source_slide_number']}"
            )
    return {
        "schema_version": "1.0.0",
        "slide_id": slide_id,
        "dimensions_px": dimensions,
        "background": design.get("style", {}).get("background", "#FFFFFF"),
        "design_config_id": design.get("config_id"),
        "objects": objects,
        "frame": contract.get("frame_configuration", {}),
        "sources": list(dict.fromkeys(sources)),
        **({"speaker_notes": list(speaker_notes)} if speaker_notes else {}),
        "compiler_report": {
            "measured_entity_count": len(measured_scene["entities"]),
            "emitted_object_count": len(objects),
            "evidence_objects_emitted": 0,
            "measurement": {
                "engine": "OpenCV",
                "opencv": measured_scene.get("runtime", {}).get("opencv"),
            },
            "connector_graph_count": sum(item["kind"] == "connector_graph" for item in objects),
            "canonical_asset_count": sum(item["kind"] == "image" and bool(item.get("semantic_role")) for item in objects),
            "text_fitting": text_fit_report,
            "local_geometry_normalization": measured_scene.get("runtime", {}).get("local_geometry_normalization", {}),
            "text_bbox_override_count": len(text_overrides),
            "contract_conformance": conformance,
            "input_bindings": {
                "measured_scene_sha256": _content_hash(measured_scene),
                "reconstruction_contract_sha256": _content_hash(contract),
                "resolved_design_sha256": _content_hash(design),
            },
        },
    }
