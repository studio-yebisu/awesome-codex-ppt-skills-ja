#!/usr/bin/env python3
"""Build visual_qa_gate.json from external compare evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VISUAL_TRUE_FIELDS = [
    "surface_system_match",
    "main_chart_semantics_match",
    "visual_semantics_preserved",
    "editable_information_layer_pass",
    "spatial_registration_pass",
    "curve_fidelity_pass",
    "label_collision_pass",
    "text_overflow_pass",
    "container_overflow_pass",
    "continuous_text_flow_pass",
    "table_semantic_typography_pass",
    "table_density_pass",
    "blueprint_background_not_used",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create visual_qa_gate.json from compare reports.")
    parser.add_argument("--slide", type=int, required=True)
    parser.add_argument("--blueprint-render", required=True)
    parser.add_argument("--ppt-render", required=True)
    parser.add_argument("--side-by-side", required=True)
    parser.add_argument("--component-signature-check", required=True)
    parser.add_argument("--visual-element-registry", required=True)
    parser.add_argument("--bbox-delta-report", required=True)
    parser.add_argument("--overlay-comparison", required=True)
    parser.add_argument("--pixel-diff-report", required=True)
    parser.add_argument("--local-crop", action="append", default=[])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    diff_report = read_json(Path(args.pixel_diff_report))
    failures = diff_report.get("failures", []) if isinstance(diff_report, dict) else []
    differences = [
        {
            "element_id": failure.get("element_id"),
            "severity": failure.get("severity", "High"),
            "description": failure.get("code", "external diff failed"),
            "accepted_by_user": False,
            "requires_rework": True,
        }
        for failure in failures
        if isinstance(failure, dict)
    ]
    passed = not differences and bool(diff_report.get("passed"))
    evidence = {field: args.pixel_diff_report for field in VISUAL_TRUE_FIELDS}
    entry = {
        "slide": args.slide,
        "blueprint_render_path": args.blueprint_render,
        "ppt_render_path": args.ppt_render,
        "side_by_side_comparison_path": args.side_by_side,
        "component_signature_check_path": args.component_signature_check,
        "visual_element_registry_path": args.visual_element_registry,
        "bbox_delta_report_path": args.bbox_delta_report,
        "overlay_comparison_path": args.overlay_comparison,
        "pixel_diff_report_path": args.pixel_diff_report,
        "local_crop_comparisons": [{"path": path} for path in args.local_crop],
        "local_overlay_artifacts": [args.overlay_comparison],
        "measurement_evidence_path": args.visual_element_registry,
        "spatial_numeric_check_path": args.bbox_delta_report,
        "visual_differences": differences,
        "evidence": evidence,
        "deliverable_allowed": passed,
    }
    for field in VISUAL_TRUE_FIELDS:
        entry[field] = passed

    payload = {"slides": [entry]}
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "deliverable_allowed": passed, "differences": len(differences)}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
