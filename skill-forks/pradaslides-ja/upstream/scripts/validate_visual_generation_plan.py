#!/usr/bin/env python3
"""Validate a PradaSlides visual-generation-plan.json contract."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


DECISIONS = {"pending", "use", "skip", "unavailable", "delegated"}
CAPABILITY_STATUS = {"available", "unavailable", "unknown", "delegated"}
OP_STATUS = {"planned", "generated", "needs-visual-review", "reviewed", "rejected", "fallback-used"}
OP_ID = re.compile(r"^(IMG|VID)-P\d{2,}-\d{2,}$")


def validate(plan: Any, require_resolved: bool = False) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not isinstance(plan, dict):
        return [Diagnostic("error", "GEN_ROOT", "Root must be a JSON object")]
    if plan.get("schema_version") != "1.0":
        diagnostics.append(Diagnostic("error", "GEN_SCHEMA", "schema_version must be '1.0'", "schema_version"))
    capability = plan.get("capability_status")
    if capability not in CAPABILITY_STATUS:
        diagnostics.append(Diagnostic("error", "GEN_CAPABILITY", f"Unknown capability_status {capability!r}", "capability_status"))
    decision = plan.get("decision")
    if decision not in DECISIONS:
        diagnostics.append(Diagnostic("error", "GEN_DECISION", f"Unknown decision {decision!r}", "decision"))
    if require_resolved and decision == "pending":
        diagnostics.append(Diagnostic("error", "GEN_PENDING", "Generation opportunity audit is unresolved", "decision"))

    reason = str(plan.get("decision_reason", "")).strip()
    if decision in {"skip", "unavailable"} and not reason:
        diagnostics.append(Diagnostic("error", "GEN_REASON", f"decision_reason is required for {decision}", "decision_reason"))
    if decision == "unavailable" and capability not in {"unavailable", "unknown"}:
        diagnostics.append(Diagnostic("warning", "GEN_CAP_MISMATCH", "Generation is marked unavailable despite a usable capability status", "capability_status"))
    if decision == "delegated" and capability != "delegated":
        diagnostics.append(Diagnostic("warning", "GEN_DELEGATE_MISMATCH", "Delegated decision should use delegated capability_status", "capability_status"))

    budget = plan.get("budget")
    if not isinstance(budget, dict):
        diagnostics.append(Diagnostic("error", "GEN_BUDGET", "budget must be an object", "budget"))
    else:
        for key in ("image_candidates", "final_unique_images", "video_candidates"):
            value = budget.get(key)
            if not isinstance(value, int) or value < 0:
                diagnostics.append(Diagnostic("error", "GEN_BUDGET_VALUE", f"{key} must be a non-negative integer", f"budget.{key}"))
        if isinstance(budget.get("final_unique_images"), int) and isinstance(budget.get("image_candidates"), int):
            if budget["final_unique_images"] > budget["image_candidates"]:
                diagnostics.append(Diagnostic("error", "GEN_BUDGET_ORDER", "final_unique_images cannot exceed image_candidates", "budget"))

    operations = plan.get("operations")
    if not isinstance(operations, list):
        return diagnostics + [Diagnostic("error", "GEN_OPERATIONS", "operations must be an array", "operations")]
    if decision in {"use", "delegated"} and not operations:
        diagnostics.append(Diagnostic("error", "GEN_NO_OPERATION", f"decision {decision} requires at least one operation", "operations"))
    if decision in {"skip", "unavailable"} and operations:
        diagnostics.append(Diagnostic("warning", "GEN_UNUSED_OPERATION", f"operations exist although decision is {decision}", "operations"))

    seen: set[str] = set()
    output_paths: set[str] = set()
    for index, operation in enumerate(operations):
        loc = f"operations[{index}]"
        if not isinstance(operation, dict):
            diagnostics.append(Diagnostic("error", "GEN_OPERATION_TYPE", "Operation must be an object", loc))
            continue
        op_id = operation.get("id")
        if not isinstance(op_id, str) or not OP_ID.match(op_id):
            diagnostics.append(Diagnostic("error", "GEN_OPERATION_ID", "id must match IMG-P01-01 or VID-P01-01", f"{loc}.id"))
        elif op_id in seen:
            diagnostics.append(Diagnostic("error", "GEN_DUP_ID", f"Duplicate operation id {op_id}", f"{loc}.id"))
        else:
            seen.add(op_id)
        slide_ids = operation.get("slide_ids")
        if not isinstance(slide_ids, list) or not slide_ids or not all(isinstance(item, str) and re.match(r"^P\d{2,}$", item) for item in slide_ids):
            diagnostics.append(Diagnostic("error", "GEN_SLIDES", "slide_ids must contain P01-style IDs", f"{loc}.slide_ids"))
        for key in (
            "purpose",
            "use_case",
            "asset_type",
            "narrative_job",
            "composition",
            "difference_from_other_visuals",
            "prompt",
            "expected_output",
            "fallback",
        ):
            if not str(operation.get(key, "")).strip():
                diagnostics.append(Diagnostic("error", "GEN_REQUIRED", f"{key} is required", f"{loc}.{key}"))
        for key in ("constraints", "avoid"):
            value = operation.get(key)
            if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                diagnostics.append(Diagnostic("error", "GEN_LIST", f"{key} must be an array of non-empty strings", f"{loc}.{key}"))
        expected = str(operation.get("expected_output", "")).strip().casefold()
        if expected:
            if expected in output_paths:
                diagnostics.append(Diagnostic("error", "GEN_OUTPUT_REUSE", "Each operation must have a unique expected_output", f"{loc}.expected_output"))
            output_paths.add(expected)
        review = operation.get("review")
        if not isinstance(review, dict):
            diagnostics.append(Diagnostic("error", "GEN_REVIEW", "review must be an object", f"{loc}.review"))
        else:
            if review.get("required") is not True:
                diagnostics.append(Diagnostic("error", "GEN_REVIEW_REQUIRED", "Generated media requires visual review", f"{loc}.review.required"))
            checks = review.get("checks")
            if not isinstance(checks, list) or not checks:
                diagnostics.append(Diagnostic("error", "GEN_REVIEW_CHECKS", "review.checks must be a non-empty array", f"{loc}.review.checks"))
        provenance = operation.get("provenance")
        if not isinstance(provenance, dict) or not str(provenance.get("provider", "")).strip():
            diagnostics.append(Diagnostic("error", "GEN_PROVENANCE", "provenance.provider is required", f"{loc}.provenance"))
        status = operation.get("status")
        if status not in OP_STATUS:
            diagnostics.append(Diagnostic("error", "GEN_STATUS", f"Unknown status {status!r}", f"{loc}.status"))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--require-resolved", action="store_true")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        value = load_json(args.plan)
    except ValueError as exc:
        return emit_report("visual generation plan validation", [Diagnostic("error", "GEN_JSON", str(exc))], json_output=args.json_output)
    return emit_report(
        "visual generation plan validation",
        validate(value, args.require_resolved),
        json_output=args.json_output,
        extra={"file": str(args.plan.resolve())},
    )


if __name__ == "__main__":
    raise SystemExit(main())
