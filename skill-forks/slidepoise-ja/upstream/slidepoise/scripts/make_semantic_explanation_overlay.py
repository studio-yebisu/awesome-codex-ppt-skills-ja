#!/usr/bin/env python3
"""Render a readable overlay from host-authored entities, groups, and relationships."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

COLORS = {
    "text": (28, 98, 243),
    "icon": (232, 129, 27),
    "icon_slot": (232, 129, 27),
    "image": (146, 104, 35),
    "shape": (62, 154, 80),
    "connector": (187, 67, 150),
    "table": (42, 166, 172),
    "chart": (98, 76, 180),
}
GROUP_COLOR = (74, 74, 74)
RELATION_COLOR = (174, 86, 32)


def bbox(record):
    value = record.get("slot_bbox_hint") or record.get("bbox_hint") or record.get("bbox")
    return [int(round(float(item))) for item in value] if isinstance(value, list) and len(value) == 4 else None


def label(record):
    return str(record.get("display_label") or record.get("semantic_label") or record.get("role") or record.get("id") or "").replace("_", " ")


def tag(canvas, text, origin, color, scale=0.44):
    x, y = origin
    font = cv2.FONT_HERSHEY_SIMPLEX
    (width, height), baseline = cv2.getTextSize(text, font, scale, 1)
    x = max(0, min(x, canvas.shape[1] - width - 10))
    y = max(height + 5, min(y, canvas.shape[0] - baseline - 5))
    cv2.rectangle(canvas, (x, y - height - 5), (x + width + 10, y + baseline + 3), (250, 250, 250), -1)
    cv2.rectangle(canvas, (x, y - height - 5), (x + width + 10, y + baseline + 3), color, 1)
    cv2.putText(canvas, text, (x + 5, y), font, scale, color, 1, cv2.LINE_AA)


def dashed_rect(canvas, box, color, thickness=2, dash=9):
    x, y, width, height = box
    for start in range(x, x + width, dash * 2):
        cv2.line(canvas, (start, y), (min(start + dash, x + width), y), color, thickness)
        cv2.line(canvas, (start, y + height), (min(start + dash, x + width), y + height), color, thickness)
    for start in range(y, y + height, dash * 2):
        cv2.line(canvas, (x, start), (x, min(start + dash, y + height)), color, thickness)
        cv2.line(canvas, (x + width, start), (x + width, min(start + dash, y + height)), color, thickness)


def center(record):
    x, y, width, height = bbox(record)
    return (x + width // 2, y + height // 2)


def endpoints(relationship):
    sources = relationship.get("source_entities") or relationship.get("sources") or relationship.get("source") or relationship.get("from") or []
    targets = relationship.get("target_entities") or relationship.get("targets") or relationship.get("target") or relationship.get("to") or []
    if isinstance(sources, str):
        sources = [sources]
    if isinstance(targets, str):
        targets = [targets]
    return [str(value) for value in sources], [str(value) for value in targets]


def render(image_path: Path, semantic_path: Path, output: Path):
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(image_path)
    semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
    canvas = image.copy()
    wash = np.full_like(canvas, 255)
    canvas = cv2.addWeighted(canvas, 0.82, wash, 0.18, 0)
    entities = [item for item in semantic.get("entities", []) if bbox(item)]
    groups = [item for item in semantic.get("groups", []) if bbox(item)]
    lookup = {str(item["id"]): item for item in [*entities, *groups] if item.get("id")}

    for entity in entities:
        x, y, width, height = bbox(entity)
        color = COLORS.get(str(entity.get("kind")), (85, 85, 85))
        cv2.rectangle(canvas, (x, y), (x + width, y + height), color, 2)
        tag(canvas, f"{entity.get('kind', 'entity')} · {label(entity)}", (x, max(16, y - 4)), color)

    for group in groups:
        x, y, width, height = bbox(group)
        dashed_rect(canvas, [x, y, width, height], GROUP_COLOR)
        semantic_class = str(group.get("semantic_class") or group.get("role") or "semantic group").replace("_", " ")
        tag(canvas, f"GROUP · {label(group)} · {semantic_class}", (x, min(canvas.shape[0] - 8, y + height + 20)), GROUP_COLOR, 0.46)

    relationship_count = 0
    for relationship in semantic.get("relationships", []) or []:
        sources, targets = endpoints(relationship)
        for source in sources:
            for target in targets:
                if source not in lookup or target not in lookup:
                    continue
                start, end = center(lookup[source]), center(lookup[target])
                cv2.arrowedLine(canvas, start, end, RELATION_COLOR, 2, cv2.LINE_AA, tipLength=0.025)
                midpoint = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
                relationship_label = str(relationship.get("display_label") or relationship.get("type") or "relationship").replace("_", " ")
                tag(canvas, relationship_label, midpoint, RELATION_COLOR, 0.42)
                relationship_count += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output), canvas):
        raise RuntimeError(f"Failed to write {output}")
    return {"output": str(output.resolve()), "entities": len(entities), "groups": len(groups), "relationships_rendered": relationship_count, "notice": "Mechanical rendering of host-authored semantics. No semantic discovery or visual acceptance."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--semantic-map", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.image, args.semantic_map, args.output), indent=2))


if __name__ == "__main__":
    main()
