"""Build a reconstruction contract from measured semantic entities."""

from __future__ import annotations

from slidepoise.canvas import reconstruction_geometry

from pathlib import Path
from typing import Any


def _asset_catalog(handoff: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {}
    for item in handoff.get("selected_assets", []):
        internal = item.get("internal", item)
        if internal.get("asset_id"):
            result[internal["asset_id"]] = internal
    return result




def _resolve_asset(entity: dict[str, Any], handoff: dict[str, Any]) -> dict[str, Any]:
    catalog = _asset_catalog(handoff)
    requested = entity.get("upstream_asset_id")
    if requested not in catalog:
        raise ValueError(
            f"Entity {entity['id']} has no exact Agent-selected upstream asset mapping. "
            "Semantic mapping must choose from the assets retained in the generation handoff."
        )
    selected = catalog[requested]
    path = selected.get("canonical_file")
    if not path or not Path(path).is_file():
        raise FileNotFoundError(f"Canonical asset for {entity['id']} is unavailable: {path}")
    asset_kind = "icon_slot" if entity["kind"] in {"icon", "icon_slot"} else "project_image"
    if "preserve_canonical_color" in selected:
        preserve_canonical_color = bool(selected["preserve_canonical_color"])
    else:
        preserve_canonical_color = bool(selected.get("user_required", False) or selected.get("require_exact_identity", False))
    return {
        "entity_id": entity["id"],
        "selected_asset_id": selected["asset_id"],
        "selected_asset_path": selected["canonical_file"],
        "asset_kind": asset_kind,
        "selection_mode": selected.get("selection_mode", "exact_agent_selected_asset"),
        "target_bbox_source_px": entity["measurement"]["layout_bbox"]["px"],
        "preserve_aspect_ratio": True,
        "fit": "contain",
        "alignment": "center",
        "alternative_candidates": selected.get("alternative_candidates", []),
        "asset_source": selected.get("source") or selected.get("asset_source") or selected.get("selection_mode"),
        "intrinsic_aspect_ratio": selected.get("intrinsic_aspect_ratio"),
        "user_required": bool(selected.get("user_required", False)),
        "preserve_canonical_color": preserve_canonical_color,
        "treatment_recolorable": bool(selected.get("treatment_recolorable", False)),
        "recolor_mode": selected.get("recolor_mode"),
        "source_provider": selected.get("provider"),
        "source_provider_version": selected.get("provider_version"),
        "source_license": selected.get("license"),
        "style_pair_id": selected.get("style_pair_id"),
        "style_variant": selected.get("style_variant"),
        "pair_asset_ids": selected.get("pair_asset_ids", []),
        "variant_visual_review": entity.get("icon_variant_review"),
    }


def _connector_plan(entity: dict[str, Any], connector_config: dict[str, Any]) -> dict[str, Any]:
    """Bind Agent-authored connector semantics to measured endpoint evidence."""
    intent = entity.get("connector_intent") or {}
    if intent.get("semantic_topology_verified") is not True:
        raise ValueError(f"Connector {entity['id']} semantic topology was not explicitly verified")
    visual = entity.get("visual_constraints") or {}
    family = str(intent.get("connector_family") or "")
    if not family:
        raise ValueError(f"Connector {entity['id']} is missing host-Agent-authored connector_family")
    allowed = set(connector_config.get("allowed_families", []))
    if allowed and family not in allowed:
        raise ValueError(f"Connector {entity['id']} uses unsupported family {family!r}")
    starts = [list(point) for point in visual.get("start_anchors_px", [])]
    ends = [list(point) for point in visual.get("end_anchors_px", [])]
    sources = list(intent.get("source_entities") or [])
    targets = list(intent.get("target_entities") or [])
    if len(starts) != len(sources) or len(ends) != len(targets):
        raise ValueError(f"Connector {entity['id']} endpoint/anchor cardinality mismatch")
    measured_junctions = [list(point) for point in visual.get("junctions_px", [])]
    explicit_junction = intent.get("junction_hint")
    junctions = [list(map(float, explicit_junction))] if explicit_junction is not None else []
    arrowhead_treatment = visual.get("arrowhead_treatment")
    if arrowhead_treatment not in {"none", "triangle_at_target", "open_arrow_at_target"}:
        raise ValueError(f"Connector {entity['id']} requires an explicit arrowhead_treatment")
    junction_treatment = intent.get("junction_style")
    if junction_treatment not in {"none", "filled_circle"}:
        raise ValueError(f"Connector {entity['id']} requires an explicit junction_style")
    if junction_treatment == "filled_circle" and intent.get("junction_diameter_px") is None:
        raise ValueError(f"Connector {entity['id']} filled junction requires junction_diameter_px")
    return {
        "entity_id": entity["id"],
        "relationship_intent": intent,
        "approximate_start_anchors_px": starts,
        "approximate_end_anchors_px": ends,
        "junction_positions_px": junctions,
        "measured_junction_evidence_px": measured_junctions,
        "stroke_style": visual.get("stroke_style", entity.get("style_hint", {})),
        "arrowhead_treatment": arrowhead_treatment,
        "arrowhead": dict(visual.get("arrowhead") or {}),
        "junction_treatment": junction_treatment,
        "junction_diameter_px": (float(intent["junction_diameter_px"]) if intent.get("junction_diameter_px") is not None else None),
        "grouping_depth_px": (float(intent["grouping_depth_px"]) if intent.get("grouping_depth_px") is not None else None),
        "routing_corridor_px": visual.get("routing_corridor_px"),
        "route_waypoints_px": [list(map(float, point)) for point in visual.get("route_waypoints_px", [])],
        "route_mode": str(intent.get("route_mode") or ""),
        "route_visual_review": {
            "reviewed": intent.get("visual_route_reviewed") is True,
            "decision": intent.get("visual_route_decision"),
            "review_artifact": intent.get("visual_route_review_artifact")
        },
        "endpoint_ownership_audit": [
            *[
                {"endpoint": endpoint, "role": "source", "side": side}
                for endpoint, side in zip(sources, intent.get("source_attachment_sides", []))
            ],
            *[
                {"endpoint": endpoint, "role": "target", "side": side}
                for endpoint, side in zip(targets, intent.get("target_attachment_sides", []))
            ],
        ],
        "source_attachment_sides": list(intent.get("source_attachment_sides", [])),
        "target_attachment_sides": list(intent.get("target_attachment_sides", [])),
        "connector_family": family,
    }


def build_reconstruction_contract(
    measured_scene: dict[str, Any],
    design: dict[str, Any],
) -> dict[str, Any]:
    """Bind fresh measured evidence to the resolved design and Agent reasoning."""
    handoff = measured_scene.get("upstream_handoff", {})
    speaker_notes = handoff.get("speaker_notes", [])
    if not isinstance(speaker_notes, list) or any(not isinstance(note, str) for note in speaker_notes):
        raise ValueError("handoff.speaker_notes must be an array of strings")
    from .coverage import content_obligation_errors
    coverage_errors = content_obligation_errors(measured_scene.get("entities", []), handoff, measured_scene.get("groups", []))
    if coverage_errors:
        raise ValueError(f"Unfulfilled content obligations: {coverage_errors}")
    source = measured_scene["source"]
    geometry = reconstruction_geometry(design, [source["width_px"], source["height_px"]])
    # Full-slide geometry and frame heights come only from the resolved config.
    # Session overrides must already have been resolved before reconstruction.
    frame = dict(design.get("frame", {}))
    header = dict(frame.get("header", {})); footer = dict(frame.get("footer", {}))

    # Frame geometry is resolved config authority; handoff may change content only.
    frame_content = dict(handoff.get("frame_content", {}))
    header_content = dict(frame_content.get("header", {})); footer_content = dict(frame_content.get("footer", {}))
    for key in ("left_text", "right_text"):
        if key in header_content: header[key] = header_content[key]
    for key in ("left_text", "center_text"):
        if key in footer_content: footer[key] = footer_content[key]
    slide_number = frame_content.get("slide_number", handoff.get("slide_number", 1))
    frame_configuration = {**frame, "header": header, "footer": footer, "slide_number": int(slide_number or 1)}

    units=[]; assets=[]; connectors=[]
    connector_configuration = design.get("connectors", {})
    for entity in measured_scene.get("entities", []):
        kind=entity["kind"]
        significance=entity.get("reconstruction_significance", "independent_object")
        emits=significance not in {"measurement_evidence", "owned_content", "non_authoritative_glyph"}
        units.append({
            "id": entity["id"], "semantic_kind": kind, "semantic_role": entity.get("role"),
            "selected_route": entity["reconstruction_route"], "node_class": "reconstruction_unit" if emits else "measurement_evidence",
            "emits_ppt_object": emits, "render_owner": entity.get("render_owner", entity["id"]),
            "bbox_px": entity["measurement"]["layout_bbox"]["px"],
            "component_id": entity.get("component_id"),
        })
        if emits and (kind in {"icon","icon_slot"} or (kind=="image" and entity.get("upstream_asset_id"))):
            assets.append(_resolve_asset(entity, handoff))
        if emits and kind=="connector":
            connectors.append(_connector_plan(entity, connector_configuration))

    emitting_ids = {str(unit["id"]) for unit in units if unit.get("emits_ppt_object")}
    for unit in units:
        if unit.get("emits_ppt_object"):
            continue
        source_entity = next((item for item in measured_scene.get("entities", []) if str(item.get("id")) == str(unit.get("id"))), {})
        significance = str(source_entity.get("reconstruction_significance") or "measurement_evidence")
        if significance == "measurement_evidence":
            if source_entity.get("meaningful_visible") is not False:
                raise ValueError(f"Non-emitting measurement evidence {unit['id']} must be explicitly marked meaningful_visible=false")
            continue
        owner = str(unit.get("render_owner") or "")
        if not owner or owner == str(unit.get("id")) or owner not in emitting_ids:
            raise ValueError(f"Meaningful non-emitting entity {unit['id']} has no emitted reconstruction owner: {owner!r}")

    return {
        "schema_version":"2.0.0",
        "source_scene_evidence": source.get("path") or source.get("image"),
        **geometry,
        "frame_configuration": frame_configuration,
        **({"speaker_notes": list(speaker_notes)} if speaker_notes else {}),
        "content_obligations": handoff.get("content_obligations", []),
        "reconstruction_units": units,
        "canonical_asset_mappings": assets,
        "connector_reconstruction_plans": connectors,
        "connector_configuration": connector_configuration,
        "z_order_relations": [r for r in measured_scene.get("relationships", []) if r.get("type")=="stacking" and r.get("back") and r.get("front")],
        "fitted_text_contracts": [],
        "layout_constraints": measured_scene.get("layout_constraints", {}),
        "evidence_policy": {
            "pixel_evidence_emits_objects": False,
            "generated_icon_glyphs_emit_objects": False,
            "meaningful_visible_entity_must_emit_or_have_emitted_owner": True,
            "accepted_target_geometry_frozen": True,
        },
    }
