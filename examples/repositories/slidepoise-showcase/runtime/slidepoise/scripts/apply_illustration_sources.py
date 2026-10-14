#!/usr/bin/env python3
"""Attach inspected illustration files without changing their canvas placement."""

from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import sys

from raster_decisions import illustration_decisions

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime" / "scripts"))
from raster_sources import validate_canvas, validate_source


def apply_sources(semantic: dict, mapping: dict) -> tuple[dict, list[str]]:
    result = copy.deepcopy(semantic)
    selected = {str(e["id"]): e for e, d in illustration_decisions(result) if d["action"] == "refine"}
    updated = []
    for record in mapping.get("items", []):
        entity_id = str(record["entity_id"])
        if entity_id in updated:
            raise ValueError("Illustration mapping contains duplicate entity IDs")
        if entity_id not in selected:
            raise ValueError("Illustration mapping includes objects not selected by the host")
        entity = selected[entity_id]
        if entity.get("geometry_policy") != "agent_logical":
            raise ValueError(f"{entity_id}: illustration registration requires an agent_logical canvas")
        path = Path(record["refined_raster"]).expanduser().resolve()
        contract = record["raster_source"]
        facts = validate_source(path, contract)
        box = entity.get("bbox_hint") or entity.get("bbox")
        if box != contract.get("source_bbox_px"):
            raise ValueError(f"{entity_id}: source placement changed after preparation")
        background = entity["raster_decision"].get("background", "preserve")
        if contract.get("background") != background:
            raise ValueError(f"{entity_id}: background requirement changed after preparation")
        validate_canvas(facts["canvas_dimensions_px"], box[2:])
        entity["raster_source_override"] = str(path)
        entity["raster_source"] = copy.deepcopy(contract)
        # The full source canvas includes intentional transparent margins. Its
        # registered extent is the authored canvas, never the tight alpha bounds.
        entity["raster_fit"] = "fill"
        entity["illustration_refinement_status"] = "refined"
        updated.append(entity_id)
    return result, updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semantic-map", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result, updated = apply_sources(json.loads(args.semantic_map.read_text()), json.loads(args.mapping.read_text()))
    for entity in result.get("entities", []):
        if entity.get("raster_source_override"):
            original_path = Path(entity["raster_source_override"])
            if not original_path.is_absolute():
                original_path = args.semantic_map.resolve().parent / original_path
            entity["raster_source_override"] = Path(os.path.relpath(original_path.resolve(), args.output.resolve().parent)).as_posix()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"updated_entity_ids": updated, "output": str(args.output.resolve())}, indent=2))


if __name__ == "__main__":
    main()
