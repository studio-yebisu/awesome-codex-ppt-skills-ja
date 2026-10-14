"""Mechanical reconstruction-contract checks.

This module intentionally checks only facts that can be established without visual
judgement. It never decides whether a slide, alignment, connector route, or layout
*looks* good. Those decisions belong to the host Agent's visual review.
"""

from __future__ import annotations

import math
from typing import Any


class ConstructorConformanceError(ValueError):
    """Raised before rendering when a deterministic contract requirement is broken."""


def _owner_box(
    identifier: str,
    entity_by_id: dict[str, dict[str, Any]],
    group_by_id: dict[str, dict[str, Any]],
) -> list[float] | None:
    entity = entity_by_id.get(identifier)
    if entity:
        box = entity.get("measurement", {}).get("layout_bbox", {}).get("px")
        return list(box) if box else None
    group = group_by_id.get(identifier)
    box = group.get("bbox_hint") if group else None
    return list(box) if box else None


def _on_named_side(anchor: list[float], box: list[float], side: str, tolerance: float = 3.0) -> bool:
    x, y, width, height = map(float, box)
    ax, ay = map(float, anchor)
    side = str(side or "").lower()
    if side == "left":
        return abs(ax - x) <= tolerance and y - tolerance <= ay <= y + height + tolerance
    if side == "right":
        return abs(ax - (x + width)) <= tolerance and y - tolerance <= ay <= y + height + tolerance
    if side == "top":
        return abs(ay - y) <= tolerance and x - tolerance <= ax <= x + width + tolerance
    if side == "bottom":
        return abs(ay - (y + height)) <= tolerance and x - tolerance <= ax <= x + width + tolerance
    return False


def _departure_matches_side(dx: float, dy: float, side: str, eps: float = 0.01) -> bool:
    side = str(side or "").lower()
    if side == "right":
        return abs(dy) <= eps and dx > eps
    if side == "left":
        return abs(dy) <= eps and dx < -eps
    if side == "bottom":
        return abs(dx) <= eps and dy > eps
    if side == "top":
        return abs(dx) <= eps and dy < -eps
    return False


def _arrival_matches_side(dx: float, dy: float, side: str, eps: float = 0.01) -> bool:
    """Check the direction of the final segment as it enters a target boundary."""
    side = str(side or "").lower()
    if side == "left":
        return abs(dy) <= eps and dx > eps
    if side == "right":
        return abs(dy) <= eps and dx < -eps
    if side == "top":
        return abs(dx) <= eps and dy > eps
    if side == "bottom":
        return abs(dx) <= eps and dy < -eps
    return False


def _transform_box(box: list[float], scale_xy: list[float], offset_y: int) -> list[float]:
    return [
        float(box[0]) * float(scale_xy[0]),
        float(box[1]) * float(scale_xy[1]) + float(offset_y),
        float(box[2]) * float(scale_xy[0]),
        float(box[3]) * float(scale_xy[1]),
    ]


def _contained(child: list[float], parent: list[float], tolerance: float = 1.5) -> bool:
    cx, cy, cw, ch = map(float, child)
    px, py, pw, ph = map(float, parent)
    return (
        cx >= px - tolerance
        and cy >= py - tolerance
        and cx + cw <= px + pw + tolerance
        and cy + ch <= py + ph + tolerance
    )


def _boxes_overlap(first: list[float], second: list[float], tolerance: float = 0.5) -> bool:
    ax, ay, aw, ah = map(float, first)
    bx, by, bw, bh = map(float, second)
    return min(ax + aw, bx + bw) - max(ax, bx) > tolerance and min(ay + ah, by + bh) - max(ay, by) > tolerance


def _structural_boundary_collisions(objects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Report text boxes that cross emitted divider or rule shapes.

    The host explicitly marks structural boundaries. We check allocated boxes
    against that declaration without interpreting a decorative line as a divider
    or claiming that a textbox allocation equals its rendered ink.
    """
    textboxes = [
        item for item in objects
        if item.get("kind") == "textbox" and item.get("bbox_px") and item.get("allow_boundary_crossing") is not True
    ]
    separators = [item for item in objects
                  if item.get("kind") == "shape" and item.get("bbox_px")
                  and item.get("structural_boundary") is True
                  and item.get("allow_text_crossing") is not True]

    collisions: list[dict[str, Any]] = []
    for textbox in textboxes:
        for separator in separators:
            if _boxes_overlap(list(textbox["bbox_px"]), list(separator["bbox_px"])):
                collisions.append({
                    "text": str(textbox.get("id")),
                    "separator": str(separator.get("id")),
                    "text_bbox_px": list(textbox["bbox_px"]),
                    "separator_bbox_px": list(separator["bbox_px"]),
                })
    return collisions


def _chart_structure_failures(objects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Check chart facts that must survive semantic reconstruction."""
    supported = {"area", "bar", "column", "doughnut", "line", "pie", "scatter"}
    failures: list[dict[str, Any]] = []
    for item in objects:
        if item.get("kind") != "chart":
            continue
        structure = item.get("structure") or {}
        chart_type = str(structure.get("type") or "")
        categories = structure.get("categories") or []
        series = structure.get("series") or []
        if chart_type not in supported:
            failures.append({"chart": str(item.get("id")), "reason": "chart_type_must_be_explicit", "type": chart_type})
            continue
        if chart_type != "scatter" and not categories:
            failures.append({"chart": str(item.get("id")), "reason": "chart_categories_missing"})
        for index, record in enumerate(series):
            values = record.get("values") or []
            if chart_type != "scatter" and len(values) != len(categories):
                failures.append({
                    "chart": str(item.get("id")),
                    "reason": "chart_series_category_length_mismatch",
                    "series_index": index,
                    "categories": len(categories),
                    "values": len(values),
                })
    return failures


def _segment_crosses_box(start: list[float], end: list[float], box: list[float]) -> bool:
    """Intersect a line with the strict interior of an allocated text rectangle."""
    x, y, width, height = map(float, box)
    if width <= 0 or height <= 0:
        return False
    low, high = 0.0, 1.0
    for origin, delta, lower, upper in (
        (float(start[0]), float(end[0]) - float(start[0]), x + 0.01, x + width - 0.01),
        (float(start[1]), float(end[1]) - float(start[1]), y + 0.01, y + height - 0.01),
    ):
        if abs(delta) < 1e-9:
            if not lower < origin < upper:
                return False
            continue
        a, b = sorted(((lower - origin) / delta, (upper - origin) / delta))
        low, high = max(low, a), min(high, b)
        if low >= high:
            return False
    return low < high


def _connector_text_intersections(objects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Report crossings as review evidence, including labels that mask a shaft.

    Text allocation is not text ink. An intentional line label can intersect its
    route, so these facts do not block rendering or decide visual suitability.
    """
    textboxes = [item for item in objects if item.get("kind") == "textbox" and item.get("bbox_px")]
    findings = []
    for connector in objects:
        if connector.get("kind") != "connector_graph":
            continue
        for textbox in textboxes:
            segments = []
            for kind in ("source_routes_px", "target_routes_px"):
                for route_index, route in enumerate(connector.get(kind, [])):
                    for segment_index, (start, end) in enumerate(zip(route, route[1:])):
                        if _segment_crosses_box(start, end, textbox["bbox_px"]):
                            segments.append({"route_set": kind, "route_index": route_index,
                                             "segment_index": segment_index, "start_px": start, "end_px": end})
            if segments:
                findings.append({"connector": connector["id"], "text": textbox["id"],
                                 "text_bbox_px": textbox["bbox_px"], "segments": segments})
    return findings


def _bend_count(points: list[list[float]]) -> int:
    if len(points) < 3:
        return 0
    bends = 0
    previous_axis: str | None = None
    for first, second in zip(points, points[1:]):
        dx = float(second[0]) - float(first[0])
        dy = float(second[1]) - float(first[1])
        if abs(dx) < 0.01 and abs(dy) < 0.01:
            continue
        if abs(dx) < 0.01:
            axis = "vertical"
        elif abs(dy) < 0.01:
            axis = "horizontal"
        else:
            axis = "diagonal"
        if previous_axis is not None and axis != previous_axis:
            bends += 1
        previous_axis = axis
    return bends


def validate_contract_consumption(
    *,
    measured_scene: dict[str, Any],
    contract: dict[str, Any],
    objects: list[dict[str, Any]],
    scale_xy: list[float],
    offset_y: int,
) -> dict[str, Any]:
    """Verify that the deterministic constructor consumed the authored contract.

    This function checks identity, containment of explicit endpoints, asset coverage,
    route cardinality, and route direction. It deliberately does *not* score visual
    quality, alignment beauty, bend aesthetics, hierarchy, spacing, or color fidelity.
    """
    object_ids = [str(item["id"]) for item in objects]
    duplicates = sorted({identifier for identifier in object_ids if object_ids.count(identifier) > 1})
    by_id = {str(item["id"]): item for item in objects}
    entity_by_id = {str(entity["id"]): entity for entity in measured_scene.get("entities", [])}
    group_by_id = {str(group["id"]): group for group in measured_scene.get("groups", [])}

    non_emitting = {
        str(unit["id"])
        for unit in contract.get("reconstruction_units", [])
        if unit.get("emits_ppt_object") is False
    }
    text_ids = {
        str(entity["id"])
        for entity in measured_scene.get("entities", [])
        if entity.get("kind") == "text" and str(entity["id"]) not in non_emitting
    }
    emitted_text_ids = {str(item["id"]) for item in objects if item.get("kind") == "textbox"}

    asset_ids = {str(item["entity_id"]) for item in contract.get("canonical_asset_mappings", [])}
    icon_asset_ids = {
        str(item["entity_id"])
        for item in contract.get("canonical_asset_mappings", [])
        if item.get("asset_kind", "icon_slot") == "icon_slot"
    }
    emitted_asset_ids = {
        str(item["id"])
        for item in objects
        if item.get("kind") == "image" and item.get("selected_asset_id")
    }
    asset_mapping_by_id = {
        str(item["entity_id"]): item for item in contract.get("canonical_asset_mappings", [])
    }
    icon_surface_expected_ids = {
        identifier
        for identifier in icon_asset_ids
        if bool((entity_by_id.get(identifier, {}).get("slot_surface") or {}).get("visible", bool(entity_by_id.get(identifier, {}).get("slot_surface"))))
    }
    missing_icon_surfaces = sorted(
        identifier for identifier in icon_surface_expected_ids if f"{identifier}.icon_slot_surface" not in by_id
    )
    unexpected_icon_surfaces = sorted(
        identifier for identifier in icon_asset_ids - icon_surface_expected_ids if f"{identifier}.icon_slot_surface" in by_id
    )
    icon_containment_failures: list[dict[str, Any]] = []
    for identifier in sorted(icon_asset_ids & emitted_asset_ids):
        glyph = by_id.get(identifier)
        source_slot = _owner_box(identifier, entity_by_id, group_by_id)
        if not glyph or not source_slot:
            continue
        sx, sy, sw, sh = map(float, _transform_box(source_slot, scale_xy, offset_y))
        gx, gy, gw, gh = map(float, glyph["bbox_px"])
        if gx < sx - 0.01 or gy < sy - 0.01 or gx + gw > sx + sw + 0.01 or gy + gh > sy + sh + 0.01:
            icon_containment_failures.append({"entity": identifier, "reason": "canonical_asset_outside_slot"})

    connector_ids = {str(item["entity_id"]) for item in contract.get("connector_reconstruction_plans", [])}
    emitted_connector_ids = {str(item["id"]) for item in objects if item.get("kind") == "connector_graph"}

    text_parent_failures: list[dict[str, Any]] = []
    for entity_id in sorted(text_ids):
        entity = entity_by_id.get(entity_id, {})
        if entity.get("allow_parent_bleed") is True:
            continue
        parent_id = entity.get("parent_id") or entity.get("parent")
        if not parent_id:
            continue
        parent_box = _owner_box(str(parent_id), entity_by_id, group_by_id)
        emitted_box = by_id.get(entity_id, {}).get("bbox_px")
        if parent_box is None:
            text_parent_failures.append({"entity": entity_id, "reason": "missing_parent_geometry", "parent": parent_id})
            continue
        if emitted_box and not _contained(emitted_box, _transform_box(parent_box, scale_xy, offset_y)):
            text_parent_failures.append({
                "entity": entity_id,
                "reason": "emitted_text_outside_semantic_parent",
                "parent": parent_id,
                "text_bbox_px": emitted_box,
                "parent_bbox_px": _transform_box(parent_box, scale_xy, offset_y),
            })
    declared_overlap_failures: list[dict[str, Any]] = []

    def constraint_box(identifier: str) -> list[float] | None:
        if identifier in icon_asset_ids:
            source_slot = _owner_box(identifier, entity_by_id, group_by_id)
            if source_slot:
                return _transform_box(source_slot, scale_xy, offset_y)
        item = by_id.get(identifier)
        return list(item.get("bbox_px")) if item and item.get("bbox_px") else None

    for raw_pair in (contract.get("layout_constraints", {}) or {}).get("non_overlap_pairs", []) or []:
        if not isinstance(raw_pair, list) or len(raw_pair) != 2:
            continue
        left, right = map(str, raw_pair)
        left_box = constraint_box(left)
        right_box = constraint_box(right)
        if not left_box or not right_box:
            declared_overlap_failures.append({"pair": raw_pair, "reason": "declared_non_overlap_object_missing_after_reconstruction"})
            continue
        if left_box and right_box and _boxes_overlap(left_box, right_box):
            declared_overlap_failures.append({"pair": raw_pair, "reason": "declared_non_overlap_pair_intersects_after_reconstruction", "left_bbox_px": left_box, "right_bbox_px": right_box})

    connector_config = contract.get("connector_configuration", {})
    allowed_families = set(connector_config.get("allowed_families", []))
    max_bends = int(connector_config.get("routing", {}).get("maximum_ordinary_bends", 2))
    min_terminal = float(connector_config.get("arrowhead", {}).get("minimum_clear_segment_px", 0))

    endpoint_failures: list[dict[str, Any]] = []
    topology_failures: list[dict[str, Any]] = []
    direction_failures: list[dict[str, Any]] = []
    bend_limit_failures: list[dict[str, Any]] = []
    terminal_length_failures: list[dict[str, Any]] = []

    for plan in contract.get("connector_reconstruction_plans", []):
        connector_id = str(plan["entity_id"])
        intent = plan.get("relationship_intent", {})
        family = str(plan.get("connector_family") or intent.get("connector_family") or "direct_flow")
        sources = [str(value) for value in intent.get("source_entities", [])]
        targets = [str(value) for value in intent.get("target_entities", [])]
        source_sides = [str(value).lower() for value in plan.get("source_attachment_sides", [])]
        target_sides = [str(value).lower() for value in plan.get("target_attachment_sides", [])]

        if allowed_families and family not in allowed_families:
            topology_failures.append({"connector": connector_id, "reason": "connector_family_not_allowed", "family": family})
        if not sources or not targets:
            topology_failures.append({"connector": connector_id, "reason": "missing_semantic_endpoint"})
            continue
        if len(source_sides) != len(sources) or len(target_sides) != len(targets):
            topology_failures.append({"connector": connector_id, "reason": "attachment_side_cardinality_mismatch"})

        emitted = by_id.get(connector_id, {})
        starts = [list(value) for value in emitted.get("sources_px", [])]
        ends = [list(value) for value in emitted.get("targets_px", [])]
        junctions = [list(value) for value in emitted.get("junctions_px", [])]
        if len(starts) != len(sources) or len(ends) != len(targets):
            topology_failures.append({
                "connector": connector_id,
                "reason": "compiled_anchor_cardinality_mismatch",
                "source_count": len(sources),
                "source_anchor_count": len(starts),
                "target_count": len(targets),
                "target_anchor_count": len(ends),
            })

        grouping = family in {"grouping_bracket", "grouping_brace"}
        shared = len(sources) > 1 or len(targets) > 1
        if family == "merge_split" and shared and not junctions:
            topology_failures.append({"connector": connector_id, "reason": "merge_split_missing_junction"})
        if grouping and not plan.get("relationship_intent", {}).get("grouping_side"):
            topology_failures.append({"connector": connector_id, "reason": "grouping_connector_missing_grouping_side"})

        for index, (source_id, anchor) in enumerate(zip(sources, starts)):
            box = _owner_box(source_id, entity_by_id, group_by_id)
            side = source_sides[index] if index < len(source_sides) else ""
            transformed_box = _transform_box(box, scale_xy, offset_y) if box is not None else None
            if transformed_box is None:
                endpoint_failures.append({"connector": connector_id, "endpoint": source_id, "reason": "missing_source_owner_box"})
            elif not _on_named_side(anchor, transformed_box, side):
                endpoint_failures.append({"connector": connector_id, "endpoint": source_id, "reason": "compiled_source_anchor_not_on_authored_side", "side": side, "anchor": anchor, "owner_box": transformed_box})

        for index, (target_id, anchor) in enumerate(zip(targets, ends)):
            box = _owner_box(target_id, entity_by_id, group_by_id)
            side = target_sides[index] if index < len(target_sides) else ""
            transformed_box = _transform_box(box, scale_xy, offset_y) if box is not None else None
            if transformed_box is None:
                endpoint_failures.append({"connector": connector_id, "endpoint": target_id, "reason": "missing_target_owner_box"})
            elif not _on_named_side(anchor, transformed_box, side):
                endpoint_failures.append({"connector": connector_id, "endpoint": target_id, "reason": "compiled_target_anchor_not_on_authored_side", "side": side, "anchor": anchor, "owner_box": transformed_box})
        if grouping:
            if emitted and not emitted.get("grouping_bbox_px"):
                topology_failures.append({"connector": connector_id, "reason": "grouping_connector_missing_grouping_bbox"})
            continue

        source_routes = emitted.get("source_routes_px", [])
        target_routes = emitted.get("target_routes_px", [])
        if len(source_routes) not in {0, len(sources)}:
            topology_failures.append({"connector": connector_id, "reason": "source_route_cardinality_mismatch"})
        if len(target_routes) != len(targets):
            topology_failures.append({"connector": connector_id, "reason": "target_route_cardinality_mismatch"})

        for index, route in enumerate(source_routes):
            if len(route) < 2:
                topology_failures.append({"connector": connector_id, "reason": "source_route_too_short", "index": index})
                continue
            dx = float(route[1][0]) - float(route[0][0])
            dy = float(route[1][1]) - float(route[0][1])
            side = source_sides[index] if index < len(source_sides) else ""
            if not _departure_matches_side(dx, dy, side):
                direction_failures.append({"connector": connector_id, "endpoint_role": "source", "index": index, "side": side, "vector": [dx, dy]})

        # A one-to-one graph is represented as one target route from source to target.
        # Validate its departure side as well as its terminal side.
        if len(sources) == 1 and len(targets) == 1 and not source_routes and len(target_routes) == 1 and len(target_routes[0]) >= 2:
            route = target_routes[0]
            dx = float(route[1][0]) - float(route[0][0])
            dy = float(route[1][1]) - float(route[0][1])
            side = source_sides[0] if source_sides else ""
            if not _departure_matches_side(dx, dy, side):
                direction_failures.append({"connector": connector_id, "endpoint_role": "source", "index": 0, "side": side, "vector": [dx, dy]})

        for index, route in enumerate(target_routes):
            if len(route) < 2:
                topology_failures.append({"connector": connector_id, "reason": "target_route_too_short", "index": index})
                continue
            dx = float(route[-1][0]) - float(route[-2][0])
            dy = float(route[-1][1]) - float(route[-2][1])
            side = target_sides[index] if index < len(target_sides) else ""
            if not _arrival_matches_side(dx, dy, side):
                direction_failures.append({"connector": connector_id, "endpoint_role": "target", "index": index, "side": side, "vector": [dx, dy]})
            if min_terminal > 0:
                terminal_length = math.hypot(dx, dy)
                if terminal_length + 1e-6 < min_terminal:
                    terminal_length_failures.append({"connector": connector_id, "target_index": index, "terminal_length_px": round(terminal_length, 3), "minimum_px": min_terminal})
            if plan.get("route_mode") == "minimal_orthogonal" and family in {"direct_flow", "orthogonal_dependency"} and len(sources) == 1 and len(targets) == 1:
                bends = _bend_count(route)
                if bends > max_bends:
                    bend_limit_failures.append({"connector": connector_id, "bends": bends, "maximum": max_bends})

    failures = {
        "missing_emitting_entities": sorted(str(unit["id"]) for unit in contract.get("reconstruction_units", []) if unit.get("emits_ppt_object") and str(unit["id"]) not in by_id),
        "duplicate_object_ids": duplicates,
        "missing_text_entities": sorted(text_ids - emitted_text_ids),
        "text_parent_containment": text_parent_failures,
        "missing_canonical_assets": sorted(asset_ids - emitted_asset_ids),
        "missing_icon_slot_surfaces": missing_icon_surfaces,
        "unexpected_icon_slot_surfaces": unexpected_icon_surfaces,
        "icon_glyphs_outside_slots": icon_containment_failures,
        "declared_non_overlap_constraints": declared_overlap_failures,
        "structural_boundary_collisions": _structural_boundary_collisions(objects),
        "chart_structure_contract": _chart_structure_failures(objects),
        "missing_connector_graphs": sorted(connector_ids - emitted_connector_ids),
        "connector_endpoint_contract": endpoint_failures,
        "connector_topology_contract": topology_failures,
        "connector_direction_contract": direction_failures,
        "connector_bend_limit": bend_limit_failures,
        "connector_terminal_length": terminal_length_failures,
    }
    failures = {key: value for key, value in failures.items() if value}
    report = {
        "evidence_type": "objective_constructor_contract_consumption",
        "coordinate_transform": {"scale_xy": scale_xy, "offset_y_px": offset_y},
        "required_counts": {
            "text_entities": len(text_ids),
            "canonical_assets": len(asset_ids),
            "icon_slot_surfaces": len(icon_surface_expected_ids),
            "connector_graphs": len(connector_ids),
        },
        "emitted_counts": {
            "text_entities": len(text_ids & emitted_text_ids),
            "canonical_assets": len(asset_ids & emitted_asset_ids),
            "icon_slot_surfaces": len(icon_surface_expected_ids) - len(missing_icon_surfaces),
            "connector_graphs": len(connector_ids & emitted_connector_ids),
        },
        "blocking_facts": failures,
        "visual_review_facts": {"connector_text_intersections": _connector_text_intersections(objects)},
        "agent_interpretation_required": True,
        "note": "No quality or reconstruction verdict is produced. Visual reasoning remains external.",
    }
    if failures:
        raise ConstructorConformanceError(f"Constructor contract coverage failed: {failures}")
    return report


def validate_backend_capabilities(scene: dict[str, Any], supported_kinds: set[str]) -> dict[str, Any]:
    required = {item["kind"] for item in scene.get("objects", [])}
    unsupported = sorted(required - supported_kinds)
    if unsupported:
        raise ConstructorConformanceError(
            f"The selected constructor backend does not support these required routes: {unsupported}"
        )
    return {
        "evidence_type": "objective_backend_capability_facts",
        "blocking_facts": [],
        "required_kinds": sorted(required),
        "supported_kinds": sorted(supported_kinds),
        "agent_interpretation_required": True,
    }
