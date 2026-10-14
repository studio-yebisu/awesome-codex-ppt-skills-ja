#!/usr/bin/env python3
"""Measure one host-Agent-authored semantic map against an accepted slide image.

OpenCV supplies deterministic pixel evidence only: geometry, contours, color evidence,
text ink, and raster crops. Semantic meaning, object ownership, visual peer groups,
connector intent, and every visual-quality judgement remain host-Agent decisions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import quote

import cv2
import numpy as np
from PIL import Image

from sam_optional import attempt as attempt_sam
from raster_sources import image_facts, validate_background, validate_canvas, validate_source

KIND_ROUTE = {
    "text": "native_text",
    "shape": "native_shape",
    "table": "native_table",
    "chart": "native_chart",
    "icon": "canonical_svg",
    "icon_slot": "canonical_svg",
    "connector": "native_connector_graph",
    "image": "screenshot_crop",
    "novel_visual": "fitted_freeform",
}

OVERLAY_COLORS = {
    "text": (36, 112, 214),
    "shape": (90, 160, 60),
    "icon": (255, 135, 30),
    "icon_slot": (255, 135, 30),
    "connector": (187, 102, 219),
    "image": (170, 120, 70),
    "table": (30, 155, 180),
    "chart": (120, 80, 180),
    "novel_visual": (140, 140, 140),
}


def load_json(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def get_box(record: dict[str, Any]) -> list[int]:
    if record.get("kind") in {"icon", "icon_slot"} and record.get("slot_bbox_hint"):
        box = record.get("slot_bbox_hint")
    else:
        box = record.get("bbox_hint") or record.get("bbox")
    if not (isinstance(box, list) and len(box) == 4):
        raise ValueError(f"{record.get('id')}: missing bbox_hint")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not np.isfinite(value) for value in box) or min(box[2:]) <= 0:
        raise ValueError(f"{record.get('id')}: bbox must contain finite numbers and positive dimensions")
    return [int(round(float(value))) for value in box]


def get_search_box(record: dict[str, Any]) -> list[int]:
    """Keep the pixel search window independent from native layout allocation."""
    if "search_bbox_hint" not in record:
        return get_box(record)
    return get_box({"id": record.get("id"), "bbox_hint": record["search_bbox_hint"]})


def clamp_box(box: list[int], width: int, height: int) -> list[int]:
    x, y, box_width, box_height = box
    right, bottom = min(width, x + box_width), min(height, y + box_height)
    x, y = max(0, x), max(0, y)
    if right <= x or bottom <= y:
        raise ValueError("bbox has no pixels inside the source canvas")
    return [x, y, right - x, bottom - y]


def rgb_hex(rgb: np.ndarray | list[float]) -> str:
    values = tuple(int(max(0, min(255, value))) for value in rgb)
    return "#%02X%02X%02X" % values


def border_pixels(crop: np.ndarray) -> np.ndarray:
    if crop.size == 0:
        return np.zeros((0, 3), dtype=np.uint8)
    return np.concatenate([crop[0, :, :], crop[-1, :, :], crop[:, 0, :], crop[:, -1, :]], axis=0)


def color_evidence(crop: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    """Estimate local background/foreground pixel colors without judging fidelity."""
    if crop.size == 0:
        return np.zeros(crop.shape[:2], dtype=np.uint8), {
            "background": "#FFFFFF",
            "foreground": "#111111",
            "foreground_fraction": 0.0,
        }

    border = border_pixels(crop).astype(np.float32)
    background = np.median(border, axis=0) if len(border) else np.array([255, 255, 255], dtype=np.float32)
    difference = np.linalg.norm(crop.astype(np.float32) - background.reshape(1, 1, 3), axis=2)
    threshold = max(20.0, float(np.percentile(difference, 70)) * 0.35)
    mask = (difference > threshold).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    foreground_pixels = crop[mask > 0]
    foreground = np.median(foreground_pixels, axis=0) if len(foreground_pixels) else np.array([17, 17, 17])
    fraction = float((mask > 0).mean())
    return mask, {
        "background": rgb_hex(background),
        "foreground": rgb_hex(foreground),
        "foreground_fraction": round(fraction, 4),
    }


def visible_bbox(mask: np.ndarray, origin: list[int]) -> list[int]:
    ys, xs = np.where(mask > 0)
    if not len(xs):
        return origin
    x, y, _, _ = origin
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    return [x + x0, y + y0, x1 - x0 + 1, y1 - y0 + 1]


def contour_evidence(mask: np.ndarray, origin: list[int]) -> list[list[list[int]]]:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    origin_x, origin_y, _, _ = origin
    output: list[list[list[int]]] = []
    for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:8]:
        if cv2.contourArea(contour) < 4:
            continue
        epsilon = max(1.0, 0.01 * cv2.arcLength(contour, True))
        polygon = cv2.approxPolyDP(contour, epsilon, True).reshape(-1, 2)
        output.append([[int(px + origin_x), int(py + origin_y)] for px, py in polygon])
    return output


def text_geometry(mask: np.ndarray, box: list[int], image_width: int) -> dict[str, Any]:
    """Measure text ink as evidence; logical textbox allocation remains Agent-authored."""
    count, _labels, stats, _centroids = cv2.connectedComponentsWithStats((mask > 0).astype(np.uint8), 8)
    components: list[list[int]] = []
    for index in range(1, count):
        x, y, width, height, area = [int(value) for value in stats[index]]
        if area >= 3 and height >= 2:
            components.append([x, y, width, height, area])
    components.sort(key=lambda record: (record[1], record[0]))

    lines: list[dict[str, Any]] = []
    for component in components:
        center_y = component[1] + component[3] / 2
        for line in lines:
            if abs(center_y - line["center_y"]) <= max(3, line["height"] * 0.55):
                line["items"].append(component)
                items = line["items"]
                line["center_y"] = sum(value[1] + value[3] / 2 for value in items) / len(items)
                line["height"] = max(value[3] for value in items)
                break
        else:
            lines.append({"center_y": center_y, "height": component[3], "items": [component]})

    origin_x, origin_y, _, _ = box
    line_boxes: list[list[int]] = []
    for line in lines:
        items = line["items"]
        left = min(value[0] for value in items)
        top = min(value[1] for value in items)
        right = max(value[0] + value[2] for value in items)
        bottom = max(value[1] + value[3] for value in items)
        line_boxes.append([origin_x + left, origin_y + top, right - left, bottom - top])

    heights = [record[3] for record in line_boxes if record[3] > 0]
    median_ink_height = float(np.median(heights)) if heights else 0.0
    estimated_points = median_ink_height * 72.0 * (13.333333 / max(1, image_width)) if median_ink_height else None
    return {
        "line_boxes_px": line_boxes,
        "line_count_evidence": len(line_boxes),
        "median_ink_height_px": round(median_ink_height, 2),
        "estimated_font_size_pt": round(estimated_points, 2) if estimated_points else None,
    }


def owner_box(identifier: str, entities: dict[str, dict[str, Any]], groups: dict[str, dict[str, Any]]) -> list[int]:
    record = entities.get(identifier) or groups.get(identifier)
    if not record:
        raise ValueError(f"connector owner not found: {identifier}")
    return get_box(record)


def attachment_point(box: list[int], side: str, fraction: float) -> list[float]:
    x, y, width, height = [float(value) for value in box]
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
    raise ValueError(f"unsupported attachment side: {side}")


def junction_evidence(starts: list[list[float]], ends: list[list[float]], intent: dict[str, Any]) -> list[list[float]]:
    """Return a measured/suggested merge-split junction as non-authoritative evidence."""
    if str(intent.get("connector_family") or "") != "merge_split":
        return []
    if intent.get("junction_hint") is not None:
        return [list(map(float, intent["junction_hint"]))]
    if not starts or not ends:
        return []
    points = [*starts, *ends]
    sides = [*(intent.get("source_attachment_sides") or []), *(intent.get("target_attachment_sides") or [])]
    if sides and all(side in {"left", "right"} for side in sides):
        return [[(min(point[0] for point in points) + max(point[0] for point in points)) / 2.0, sum(point[1] for point in points) / len(points)]]
    if sides and all(side in {"top", "bottom"} for side in sides):
        return [[sum(point[0] for point in points) / len(points), (min(point[1] for point in points) + max(point[1] for point in points)) / 2.0]]
    return [[sum(point[0] for point in points) / len(points), sum(point[1] for point in points) / len(points)]]


def measured_layout_box(kind: str, hint_box: list[int], visible: list[int], entity: dict[str, Any]) -> list[int]:
    """Apply the geometry authority already selected by the host Agent."""
    significance = str(entity.get("reconstruction_significance") or "independent_object")
    if kind == "connector" or significance in {"measurement_evidence", "owned_content", "non_authoritative_glyph"}:
        return hint_box
    policy = str(entity.get("geometry_policy") or "").lower()
    if policy == "agent_logical":
        return hint_box
    if policy == "opencv_visible":
        return visible
    raise ValueError(
        f"Entity {entity.get('id')!r} requires geometry_policy agent_logical or opencv_visible. "
        "Measurement cannot infer visual authority from entity kind."
    )




def normalize_local_geometry(
    measured: list[dict[str, Any]],
    semantic: dict[str, Any],
    config: dict[str, Any],
    canvas_size: tuple[int, int] | None = None,
) -> dict[str, Any]:
    """Apply only explicit host-reviewed measurement corrections, atomically.

    No proximity clustering, peer discovery, or automatic target selection happens
    here. The host Agent owns the correction magnitude and reason.
    """
    policy = (config.get("measurement", {}) or {}).get("local_geometry_normalization", {}) or {}
    enabled = policy.get("enabled", True)
    decisions = semantic.get("geometry_adjustments", []) or []
    if not enabled and decisions:
        raise ValueError("geometry adjustments supplied while local corrections are disabled")
    by_id = {str(item["id"]): item for item in measured}
    proposed = {}
    for decision in decisions:
        entity_id = str(decision.get("entity_id", ""))
        if entity_id not in by_id or entity_id in proposed:
            raise ValueError(f"{entity_id}: unknown or duplicate geometry adjustment")
        if decision.get("reviewed_by") != "host_agent_visual_reasoning" or not str(decision.get("reason", "")).strip():
            raise ValueError(f"{entity_id}: geometry adjustment needs a host visual decision")
        before = list(map(float, by_id[entity_id]["measurement"]["layout_bbox"]["px"]))
        expected = decision.get("before_bbox_px")
        after = decision.get("after_bbox_px")
        if not isinstance(expected, list) or len(expected) != 4 or not np.allclose(expected, before, atol=1e-6, rtol=0):
            raise ValueError(f"{entity_id}: stale geometry decision, remeasure and review")
        if not isinstance(after, list) or len(after) != 4:
            raise ValueError(f"{entity_id}: after_bbox_px must contain four values")
        after = list(map(float, after))
        if not all(np.isfinite(after)) or after[2:] != before[2:]:
            raise ValueError(f"{entity_id}: local correction cannot resize or use nonfinite coordinates")
        if min(after[:2]) < 0:
            raise ValueError(f"{entity_id}: correction cannot move the object outside the canvas")
        if canvas_size and (after[0] + after[2] > canvas_size[0] or after[1] + after[3] > canvas_size[1]):
            raise ValueError(f"{entity_id}: correction cannot move the object outside the canvas")
        proposed[entity_id] = {
            "entity_id": entity_id,
            "before_bbox_px": before,
            "after_bbox_px": after,
            "delta_px": [after[0] - before[0], after[1] - before[1]],
            "reviewed_by": decision["reviewed_by"],
            "reason": decision["reason"],
        }
    # Validate all decisions before mutating any measured object.
    for entity_id, decision in proposed.items():
        by_id[entity_id]["measurement"]["layout_bbox"]["px"] = decision["after_bbox_px"]
        by_id[entity_id]["measurement"]["layout_translation_px"] = decision["delta_px"]
    return {
        "enabled": enabled,
        "mode": "agent_authored_only",
        "adjustment_count": len(proposed),
        "adjustments": list(proposed.values()),
        "policy": "Exact host-reviewed corrections only. No automatic alignment or programmatic magnitude verdict.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--semantic-map", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--upstream-handoff")
    parser.add_argument("--config", required=True)
    parser.add_argument("--sam", choices=["auto", "never", "required"], help=argparse.SUPPRESS)
    args = parser.parse_args()

    image_path = Path(args.image).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "crops").mkdir(exist_ok=True)

    rgb = np.array(Image.open(image_path).convert("RGB"))
    image_height, image_width = rgb.shape[:2]
    semantic = load_json(args.semantic_map)
    handoff = load_json(args.upstream_handoff)
    config = load_json(args.config)
    identifiers = [record.get("id") for record in [*semantic.get("entities", []), *semantic.get("groups", [])]]
    if any(not isinstance(value, str) or not value.strip() for value in identifiers) or len(set(identifiers)) != len(identifiers):
        raise ValueError("Semantic entity and group IDs must be nonempty and unique")
    entity_lookup = {entity["id"]: entity for entity in semantic.get("entities", [])}
    group_lookup = {group["id"]: group for group in semantic.get("groups", [])}
    sam_results, segmentation_report = attempt_sam(
        rgb,
        semantic.get("entities", []),
        config,
        mode_override=args.sam,
    )

    measured: list[dict[str, Any]] = []
    debug = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    masks_dir = output_dir / "masks"
    masks_dir.mkdir(exist_ok=True)
    for entity in semantic.get("entities", []):
        item = json.loads(json.dumps(entity))
        filename_id = quote(str(entity["id"]), safe="")
        logical_box = clamp_box(get_box(entity), image_width, image_height)
        box = clamp_box(get_search_box(entity), image_width, image_height)
        x, y, box_width, box_height = box
        crop = rgb[y : y + box_height, x : x + box_width]
        opencv_mask, colors = color_evidence(crop)
        sam_record = sam_results.get(str(entity["id"]))
        mask = opencv_mask
        mask_source = "opencv"
        sam_candidate_paths: list[str] = []
        if sam_record is not None:
            for index, candidate in enumerate(sam_record["candidate_masks"]):
                candidate_path = masks_dir / f"{filename_id}-sam2-candidate-{index}.png"
                cv2.imwrite(str(candidate_path), candidate * 255)
                sam_candidate_paths.append(str(candidate_path.relative_to(output_dir)))
            selected_index = entity.get("sam_candidate_index")
            if selected_index is not None:
                if not isinstance(selected_index, int) or isinstance(selected_index, bool):
                    raise ValueError(f"{entity['id']}: sam_candidate_index must be an integer")
                if selected_index < 0 or selected_index >= len(sam_record["candidate_masks"]):
                    raise ValueError(f"{entity['id']}: sam_candidate_index is outside the generated candidate range")
                sam_full = sam_record["candidate_masks"][selected_index]
                mask = (sam_full[y : y + box_height, x : x + box_width] > 0).astype(np.uint8) * 255
                mask_source = "sam2"
                segmentation_report["selected_entity_ids"].append(str(entity["id"]))
        kind = entity.get("kind", "shape")
        visible = visible_bbox(mask, box)
        layout = measured_layout_box(kind, logical_box, visible, entity)
        measurement: dict[str, Any] = {
            "layout_bbox": {"px": layout},
            "search_bbox": {"px": box},
            "visible_bbox": {"px": visible},
            "color_evidence": colors,
            "contours_px": contour_evidence(mask, box),
            "mask_source": mask_source,
        }
        if sam_record is not None:
            measurement["sam2"] = {
                "candidate_scores": [round(value, 5) for value in sam_record["candidate_scores"]],
                "prompt_time_sec": round(sam_record["prompt_time_sec"], 4),
                "candidate_masks": sam_candidate_paths,
                "selected_candidate_index": entity.get("sam_candidate_index"),
                "selection_basis": "A SAM candidate contributes only when the host Agent records sam_candidate_index after visual inspection.",
            }

        if kind == "text":
            measurement["text_geometry"] = text_geometry(mask, box, image_width)
            measurement["text_color_evidence"] = {
                "background": colors["background"],
                "foreground": colors["foreground"],
            }

        if kind in {"image", "novel_visual"}:
            crop_path = output_dir / "crops" / f"{filename_id}.png"
            cx, cy, cw, ch = layout
            Image.fromarray(rgb[cy:cy + ch, cx:cx + cw]).save(crop_path)
            measurement["source_crop_bbox"] = {"px": list(layout)}
            override = entity.get("raster_source_override") if kind == "image" else None
            if (entity.get("raster_decision") or {}).get("action") == "reuse_original":
                override = None
            if override:
                override_path = Path(str(override)).expanduser()
                if not override_path.is_absolute():
                    override_path = Path(args.semantic_map).resolve().parent / override_path
                override_path = override_path.resolve()
                if not override_path.is_file():
                    raise FileNotFoundError(f"{entity['id']}: raster_source_override is missing: {override_path}")
                source_contract = entity.get("raster_source")
                if source_contract:
                    facts = validate_source(override_path, source_contract)
                    if source_contract.get("source_image_sha256") != hashlib.sha256(image_path.read_bytes()).hexdigest():
                        raise ValueError(f"{entity['id']}: illustration was prepared against a different slide image")
                    if list(layout) != source_contract.get("source_bbox_px"):
                        raise ValueError(f"{entity['id']}: measured canvas changed after illustration preparation")
                    validate_canvas(facts["canvas_dimensions_px"], list(layout)[2:])
                else:
                    facts = image_facts(override_path)
                validate_background(facts, (entity.get("raster_decision") or {}).get("background", "preserve"))
                measurement["image_object"] = {
                    "screenshot_crop_absolute": str(override_path),
                    "original_slide_crop_absolute": str(crop_path),
                    "crop_mode": str(entity.get("raster_fit") or "contain"),
                    "source_kind": "refined_raster_override",
                    "raster_source_facts": facts,
                }
            else:
                measurement["image_object"] = {
                    "screenshot_crop_absolute": str(crop_path),
                    "crop_mode": str(entity.get("raster_fit") or "fill"),
                    "source_kind": "accepted_slide_crop",
                }

        if kind == "connector":
            intent = item.get("connector_intent") or {}
            authored_visual = dict(item.get("visual_constraints") or {})
            sources = list(intent.get("source_entities") or [])
            targets = list(intent.get("target_entities") or [])
            source_sides = list(intent.get("source_attachment_sides") or [])
            target_sides = list(intent.get("target_attachment_sides") or [])
            source_fractions = list(intent.get("source_attachment_fractions") or [])
            target_fractions = list(intent.get("target_attachment_fractions") or [])
            if len(source_sides) != len(sources) or len(target_sides) != len(targets):
                raise ValueError(f"{item['id']}: attachment side count must match semantic endpoints")
            if len(source_fractions) != len(sources) or len(target_fractions) != len(targets):
                raise ValueError(f"{item['id']}: attachment fraction count must match semantic endpoints")
            starts = [
                attachment_point(owner_box(identifier, entity_lookup, group_lookup), source_sides[index], source_fractions[index])
                for index, identifier in enumerate(sources)
            ]
            ends = [
                attachment_point(owner_box(identifier, entity_lookup, group_lookup), target_sides[index], target_fractions[index])
                for index, identifier in enumerate(targets)
            ]
            family = str(intent.get("connector_family") or "")
            if not family:
                raise ValueError(f"{item['id']}: host Agent must author connector_family")
            item["visual_constraints"] = {
                **authored_visual,
                "start_anchors_px": starts,
                "end_anchors_px": ends,
                "junctions_px": junction_evidence(starts, ends, intent),
                "routing_corridor_px": authored_visual.get("routing_corridor_px", intent.get("routing_corridor_px")),
                "stroke_style": authored_visual.get("stroke_style", item.get("style_hint", {})),
                "arrowhead_treatment": authored_visual.get("arrowhead_treatment"),
                "junction_treatment": intent.get("junction_style"),
            }

        item["measurement"] = measurement
        item["reconstruction_route"] = item.get("reconstruction_route") or KIND_ROUTE.get(kind, "native_shape")
        measured.append(item)

    normalization_report = normalize_local_geometry(measured, semantic, config, (image_width, image_height))

    # Draw after host-authored geometry adjustments. The overlay distinguishes the
    # search area OpenCV inspected, the visible-pixel evidence it found, and the
    # layout geometry the constructor will actually consume. It reports evidence
    # only. It never selects which geometry is visually correct.
    for item in measured:
        measurement = item["measurement"]
        search = [round(value) for value in measurement["search_bbox"]["px"]]
        visible = [round(value) for value in measurement["visible_bbox"]["px"]]
        layout = [round(value) for value in measurement["layout_bbox"]["px"]]
        overlay_color = OVERLAY_COLORS.get(item.get("kind"), (80, 80, 80))
        sx, sy, sw, sh = search
        vx, vy, vw, vh = visible
        lx, ly, lw, lh = layout
        cv2.rectangle(debug, (sx, sy), (sx + sw, sy + sh), (110, 110, 110), 1, cv2.LINE_AA)
        cv2.rectangle(debug, (vx, vy), (vx + vw, vy + vh), (0, 215, 255), 1, cv2.LINE_AA)
        cv2.rectangle(debug, (lx, ly), (lx + lw, ly + lh), overlay_color, 2, cv2.LINE_AA)
        cv2.putText(
            debug,
            str(item["id"]),
            (lx, max(14, ly - 4)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            overlay_color,
            1,
            cv2.LINE_AA,
        )
        for line in measurement.get("text_geometry", {}).get("line_boxes_px", []):
            tx, ty, tw, th = [round(value) for value in line]
            cv2.rectangle(debug, (tx, ty), (tx + tw, ty + th), (255, 180, 0), 1, cv2.LINE_AA)

    cv2.putText(
        debug,
        "gray: search  yellow: visible evidence  color: emitted layout  blue: text line evidence",
        (12, 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.42,
        (35, 35, 35),
        1,
        cv2.LINE_AA,
    )

    debug_path = output_dir / "debug_overlay.png"
    cv2.imwrite(str(debug_path), debug)
    result = {
        "schema_version": "3.0.0",
        "source": {
            "image": str(image_path),
            "path": str(image_path),
            "width_px": image_width,
            "height_px": image_height,
        },
        "runtime": {
            "opencv": cv2.__version__,
            "segmentation": segmentation_report,
            "local_geometry_normalization": normalization_report,
        },
        "entities": measured,
        "groups": semantic.get("groups", []),
        "relationships": semantic.get("relationships", []),
        "layout_constraints": semantic.get("layout_constraints", {}),
        "upstream_handoff": handoff,
    }
    (output_dir / "slide_entities.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    optional_report = ""
    if segmentation_report["mode"] != "never":
        optional_report = (
            f"- Experimental segmentation masks contributed: {len(segmentation_report['selected_entity_ids'])}\n"
            f"- Segmentation execution: {segmentation_report['executed']}, "
            f"skip reason: {segmentation_report['skip_reason']}\n"
        )
    (output_dir / "report.md").write_text(
        "# Measurement report\n\n"
        f"- Image: `{image_path}`\n"
        f"- Size: {image_width} x {image_height}\n"
        f"- Entities measured: {len(measured)}\n"
        f"- OpenCV: {cv2.__version__}\n"
        f"{optional_report}"
        f"- Host-authored geometry adjustments: {normalization_report['adjustment_count']}\n\n"
        "This report records deterministic pixel evidence and any explicit host-authored geometry adjustments. Visual acceptance belongs to the host Agent.\n",
        encoding="utf-8",
    )
    print(json.dumps({"entities": len(measured), "opencv": cv2.__version__, "debug_overlay": str(debug_path)}, indent=2))


if __name__ == "__main__":
    main()
