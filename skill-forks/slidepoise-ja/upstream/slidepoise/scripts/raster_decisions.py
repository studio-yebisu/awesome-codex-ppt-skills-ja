"""Read host-authored raster choices without judging image quality."""
from __future__ import annotations


def illustration_decisions(semantic: dict) -> list[tuple[dict, dict]]:
    result = []
    for entity in semantic.get("entities", []):
        if entity.get("kind") != "image" or entity.get("visual_source_class") != "novel_illustration" or entity.get("meaningful_visible") is False:
            continue
        decision = entity.get("raster_decision", {})
        action = decision.get("action")
        if action not in {"reuse_original", "refine", "clean_plate", "preserve_composite"}:
            raise ValueError(f"{entity.get('id')}: explicit raster_decision.action required")
        if decision.get("reviewed_by") != "host_agent_visual_reasoning" or not str(decision.get("reason", "")).strip():
            raise ValueError(f"{entity.get('id')}: raster choice needs host visual reasoning")
        if action == "refine" and decision.get("occluding_native_text_ids"):
            raise ValueError(f"{entity.get('id')}: resolve editable text occlusion before isolated refinement")
        if decision.get("background", "preserve") not in {"preserve", "transparent"}:
            raise ValueError(f"{entity.get('id')}: raster background must be preserve or transparent")
        result.append((entity, decision))
    return result


def illustration_decision_errors(semantic: dict, approvals: dict) -> list[str]:
    """Return structural raster-decision errors.

    The approvals argument remains for compatibility with older runs. User approval
    status is optional conversation history and does not control reconstruction.
    """
    try:
        illustration_decisions(semantic)
    except ValueError as exc:
        return [str(exc)]
    return []
