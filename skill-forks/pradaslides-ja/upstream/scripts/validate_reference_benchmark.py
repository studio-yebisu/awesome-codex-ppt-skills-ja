#!/usr/bin/env python3
"""Validate reference-relative benchmark evidence and quality floors."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


REQUIRED_CRITERIA = {
    "identity",
    "hierarchy",
    "typography",
    "composition",
    "media",
    "proof",
    "rhythm",
    "runtime",
    "accessibility",
    "originality",
    "materiality",
    "native-fidelity",
}
VALID_STATUS = {"draft", "final"}
CRITERION_STATUS = {"pass", "fail", "not-applicable"}
TARGET_RUNTIMES = {"html", "web-slides", "slidev", "native-pptx"}
COVERAGE_MODES = {"cluster-sampled", "mapped-all-references", "one-slide-per-reference"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: Any, require_final: bool, root: Path | None = None) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    reference_ids: set[str] = set()
    coverage_mode: str | None = None
    coverage_slide_ids: list[str] = []
    if not isinstance(data, dict):
        return [Diagnostic("error", "REFBENCH_ROOT", "Root must be a JSON object")]
    if data.get("schema_version") != "1.0":
        diagnostics.append(Diagnostic("error", "REFBENCH_SCHEMA", "schema_version must be '1.0'", "schema_version"))
    if not nonempty(data.get("candidate")):
        diagnostics.append(Diagnostic("error", "REFBENCH_CANDIDATE", "candidate is required", "candidate"))
    if data.get("target_runtime") not in TARGET_RUNTIMES:
        diagnostics.append(Diagnostic("error", "REFBENCH_RUNTIME", f"target_runtime must be one of {sorted(TARGET_RUNTIMES)}", "target_runtime"))
    status = data.get("status")
    if status not in VALID_STATUS:
        diagnostics.append(Diagnostic("error", "REFBENCH_STATUS", f"status must be one of {sorted(VALID_STATUS)}", "status"))
    if require_final and status != "final":
        diagnostics.append(Diagnostic("error", "REFBENCH_NOT_FINAL", "Final validation requires status 'final'", "status"))
    missing_evidence_severity = "error" if require_final or status == "final" else "warning"

    review = data.get("review")
    if not isinstance(review, dict):
        diagnostics.append(Diagnostic("error", "REFBENCH_REVIEW", "review must be an object", "review"))
    else:
        for key in ("reviewer", "method", "reviewed_at"):
            if not nonempty(review.get(key)):
                diagnostics.append(Diagnostic("error", "REFBENCH_REVIEW_FIELD", f"review.{key} is required", f"review.{key}"))
        if require_final and str(review.get("reviewer", "")).strip().casefold() in {"pending", "unknown", "unreviewed"}:
            diagnostics.append(Diagnostic("error", "REFBENCH_REVIEW_PENDING", "Final benchmark requires a resolved reviewer", "review.reviewer"))

    policy = data.get("reference_policy")
    if not isinstance(policy, dict):
        diagnostics.append(Diagnostic("error", "REFBENCH_POLICY", "reference_policy must be an object", "reference_policy"))
    else:
        if policy.get("mode") != "principles-not-layouts":
            diagnostics.append(Diagnostic("error", "REFBENCH_COPY_POLICY", "reference_policy.mode must be 'principles-not-layouts'", "reference_policy.mode"))
        references = policy.get("references")
        if not isinstance(references, list) or not references:
            diagnostics.append(Diagnostic("error", "REFBENCH_REFERENCES", "At least one reference mapping is required", "reference_policy.references"))
        else:
            seen: set[str] = set()
            for index, item in enumerate(references):
                loc = f"reference_policy.references[{index}]"
                if not isinstance(item, dict):
                    diagnostics.append(Diagnostic("error", "REFBENCH_REFERENCE", "Reference mapping must be an object", loc))
                    continue
                rid = item.get("id")
                if not nonempty(rid):
                    diagnostics.append(Diagnostic("error", "REFBENCH_REFERENCE_ID", "Reference id is required", f"{loc}.id"))
                elif rid in seen:
                    diagnostics.append(Diagnostic("error", "REFBENCH_REFERENCE_DUP", f"Duplicate reference id {rid!r}", f"{loc}.id"))
                else:
                    seen.add(rid)
                    reference_ids.add(rid)
                for key in ("path", "cluster", "transferable_principle", "avoid"):
                    if not nonempty(item.get(key)):
                        diagnostics.append(Diagnostic("error", "REFBENCH_REFERENCE_FIELD", f"{key} is required", f"{loc}.{key}"))
                reference_path = item.get("path")
                if root and nonempty(reference_path) and "://" not in reference_path and not (root / reference_path).resolve().is_file():
                    diagnostics.append(Diagnostic(missing_evidence_severity, "REFBENCH_REFERENCE_PATH", f"Reference file does not exist: {reference_path}", f"{loc}.path"))
                if item.get("usage") not in {"selected", "quality-floor", "not-applicable"}:
                    diagnostics.append(Diagnostic("error", "REFBENCH_REFERENCE_USE", "usage must be selected, quality-floor, or not-applicable", f"{loc}.usage"))

    coverage = data.get("coverage")
    if coverage is not None:
        if not isinstance(coverage, dict):
            diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE", "coverage must be an object", "coverage"))
        else:
            coverage_mode = coverage.get("mode")
            if coverage_mode not in COVERAGE_MODES:
                diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_MODE", f"coverage.mode must be one of {sorted(COVERAGE_MODES)}", "coverage.mode"))
            mappings = coverage.get("mappings")
            if not isinstance(mappings, list) or not mappings:
                diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_MAPPINGS", "coverage.mappings must be a non-empty array", "coverage.mappings"))
            else:
                mapped_references: set[str] = set()
                mapped_slides: set[str] = set()
                mapped_responses: set[str] = set()
                for index, item in enumerate(mappings):
                    loc = f"coverage.mappings[{index}]"
                    if not isinstance(item, dict):
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_MAPPING", "Coverage mapping must be an object", loc))
                        continue
                    reference_id = item.get("reference_id")
                    slide_id = item.get("slide_id")
                    if not nonempty(reference_id):
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_REFERENCE", "reference_id is required", f"{loc}.reference_id"))
                    elif reference_id not in reference_ids:
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_UNKNOWN", f"Unknown reference_id {reference_id!r}", f"{loc}.reference_id"))
                    elif reference_id in mapped_references:
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_DUP_REFERENCE", f"Reference {reference_id!r} is mapped more than once", f"{loc}.reference_id"))
                    else:
                        mapped_references.add(reference_id)
                    if not nonempty(slide_id) or not re.fullmatch(r"P\d{2,}", str(slide_id)):
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_SLIDE", "slide_id must match P01, P02, ...", f"{loc}.slide_id"))
                    else:
                        coverage_slide_ids.append(str(slide_id))
                        if coverage_mode == "one-slide-per-reference" and slide_id in mapped_slides:
                            diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_DUP_SLIDE", f"Slide {slide_id!r} maps more than one reference", f"{loc}.slide_id"))
                        mapped_slides.add(str(slide_id))
                    response = item.get("response")
                    if not nonempty(response):
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_RESPONSE", "response is required", f"{loc}.response"))
                    elif coverage_mode in {"mapped-all-references", "one-slide-per-reference"}:
                        normalized_response = re.sub(r"\s+", " ", str(response).strip().lower())
                        if len(re.findall(r"\b\w+\b", normalized_response)) < 8:
                            diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_RESPONSE_DETAIL", "Exhaustive coverage response must contain at least eight words", f"{loc}.response"))
                        if normalized_response in mapped_responses:
                            diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_DUP_RESPONSE", "Exhaustive coverage responses must be individually specific", f"{loc}.response"))
                        mapped_responses.add(normalized_response)
                    if item.get("status") not in {"pass", "fail"}:
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_STATUS", "status must be pass or fail", f"{loc}.status"))
                    elif require_final and item.get("status") != "pass":
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_NOT_PASS", "Final coverage mappings must pass", f"{loc}.status"))
                if coverage_mode in {"mapped-all-references", "one-slide-per-reference"}:
                    missing_references = sorted(reference_ids - mapped_references)
                    if missing_references:
                        diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_MISSING", "Unmapped references: " + ", ".join(missing_references), "coverage.mappings"))

    criteria = data.get("criteria")
    found: set[str] = set()
    if not isinstance(criteria, list):
        diagnostics.append(Diagnostic("error", "REFBENCH_CRITERIA", "criteria must be an array", "criteria"))
    else:
        for index, item in enumerate(criteria):
            loc = f"criteria[{index}]"
            if not isinstance(item, dict):
                diagnostics.append(Diagnostic("error", "REFBENCH_CRITERION", "Criterion must be an object", loc))
                continue
            cid = item.get("id")
            if not nonempty(cid):
                diagnostics.append(Diagnostic("error", "REFBENCH_CRITERION_ID", "Criterion id is required", f"{loc}.id"))
                continue
            if cid in found:
                diagnostics.append(Diagnostic("error", "REFBENCH_CRITERION_DUP", f"Duplicate criterion {cid!r}", f"{loc}.id"))
            found.add(cid)
            score = item.get("score")
            floor = item.get("floor")
            if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 10:
                diagnostics.append(Diagnostic("error", "REFBENCH_SCORE", "score must be between 0 and 10", f"{loc}.score"))
            if not isinstance(floor, (int, float)) or isinstance(floor, bool) or not 0 <= floor <= 10:
                diagnostics.append(Diagnostic("error", "REFBENCH_FLOOR", "floor must be between 0 and 10", f"{loc}.floor"))
            criterion_status = item.get("status")
            if criterion_status not in CRITERION_STATUS:
                diagnostics.append(Diagnostic("error", "REFBENCH_CRITERION_STATUS", f"status must be one of {sorted(CRITERION_STATUS)}", f"{loc}.status"))
            if not nonempty(item.get("rationale")):
                diagnostics.append(Diagnostic("error", "REFBENCH_RATIONALE", "rationale is required", f"{loc}.rationale"))
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not evidence or not all(nonempty(value) for value in evidence):
                diagnostics.append(Diagnostic("error", "REFBENCH_EVIDENCE", "evidence must contain at least one path or test identifier", f"{loc}.evidence"))
            elif root:
                for evidence_index, value in enumerate(evidence):
                    if "://" not in value and not (root / value).resolve().exists():
                        diagnostics.append(Diagnostic(missing_evidence_severity, "REFBENCH_EVIDENCE_PATH", f"Evidence path does not exist: {value}", f"{loc}.evidence[{evidence_index}]"))
            if require_final and criterion_status != "not-applicable":
                if isinstance(score, (int, float)) and isinstance(floor, (int, float)) and score < floor:
                    diagnostics.append(Diagnostic("error", "REFBENCH_FLOOR_FAIL", f"Criterion {cid!r} score {score} is below floor {floor}", loc))
                if criterion_status != "pass":
                    diagnostics.append(Diagnostic("error", "REFBENCH_NOT_PASS", f"Criterion {cid!r} must pass for final delivery", f"{loc}.status"))
        missing = sorted(REQUIRED_CRITERIA - found)
        if missing:
            diagnostics.append(Diagnostic("error", "REFBENCH_CRITERIA_MISSING", "Missing criteria: " + ", ".join(missing), "criteria"))

    render = data.get("render_evidence")
    if not isinstance(render, dict):
        diagnostics.append(Diagnostic("error", "REFBENCH_RENDER", "render_evidence must be an object", "render_evidence"))
    else:
        native_pptx = data.get("target_runtime") == "native-pptx"
        required_render_fields = (
            ("pptx_file", "slide_montage", "package_inspection", "viewport")
            if native_pptx
            else ("entrypoint", "slide_montage", "console_capture", "browser_qa", "viewport")
        )
        file_render_fields = (
            ("pptx_file", "slide_montage", "package_inspection")
            if native_pptx
            else ("entrypoint", "slide_montage", "console_capture", "browser_qa")
        )
        for key in required_render_fields:
            if not nonempty(render.get(key)):
                diagnostics.append(Diagnostic("error", "REFBENCH_RENDER_FIELD", f"render_evidence.{key} is required", f"render_evidence.{key}"))
        if root:
            for key in file_render_fields:
                value = render.get(key)
                if nonempty(value) and "://" not in value and not (root / value).resolve().is_file():
                    diagnostics.append(Diagnostic(missing_evidence_severity, "REFBENCH_RENDER_PATH", f"Render evidence does not exist: {value}", f"render_evidence.{key}"))
        count = render.get("slide_count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            diagnostics.append(Diagnostic("error", "REFBENCH_SLIDE_COUNT", "render_evidence.slide_count must be a positive integer", "render_evidence.slide_count"))
        elif coverage_slide_ids:
            invalid_slides = sorted({slide_id for slide_id in coverage_slide_ids if int(slide_id[1:]) > count})
            if invalid_slides:
                diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_RANGE", "Coverage slide IDs exceed render slide_count: " + ", ".join(invalid_slides), "coverage.mappings"))
            if coverage_mode == "one-slide-per-reference" and len(set(coverage_slide_ids)) != len(reference_ids):
                diagnostics.append(Diagnostic("error", "REFBENCH_COVERAGE_ONE_TO_ONE", "one-slide-per-reference requires one unique slide for every reference", "coverage.mappings"))

    blockers = data.get("blockers")
    if not isinstance(blockers, list):
        diagnostics.append(Diagnostic("error", "REFBENCH_BLOCKERS", "blockers must be an array", "blockers"))
    elif require_final and blockers:
        diagnostics.append(Diagnostic("error", "REFBENCH_BLOCKED", "Final benchmark cannot contain unresolved blockers", "blockers"))
    repairs = data.get("repairs")
    if not isinstance(repairs, list):
        diagnostics.append(Diagnostic("error", "REFBENCH_REPAIRS", "repairs must be an array", "repairs"))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmark", type=Path)
    parser.add_argument("--require-final", action="store_true")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()
    diagnostics = validate(load_json(args.benchmark), args.require_final, args.benchmark.resolve().parent)
    return emit_report("reference benchmark validation", diagnostics, json_output=args.json_output)


if __name__ == "__main__":
    raise SystemExit(main())
