#!/usr/bin/env python3
"""Validate a PradaSlides brief.json contract."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


TASK_MODES = {
    "new",
    "redesign",
    "fill-template",
    "enhance-existing",
    "critique",
    "plan-only",
}
INTENTS = {
    "portfolio",
    "work-results",
    "business-proposal",
    "sales",
    "investor-pitch",
    "strategy-decision",
    "research-technical",
    "teaching-workshop",
    "keynote-launch",
    "report-async",
    "template-system",
}
DELIVERY_MODES = {"speaking", "hybrid", "reading"}
EDITABILITY = {
    "native-required",
    "native-preferred",
    "source-editable",
    "raster-acceptable",
    "not-required",
}
BRAND_STATUS = {"none", "provided", "derive", "preserve"}
ASPECT_RATIOS = {"16:9", "4:3", "A4-landscape", "A4-portrait", "custom"}


def is_nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_dict(
    parent: dict[str, Any], key: str, diagnostics: list[Diagnostic]
) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        diagnostics.append(Diagnostic("error", "BRIEF_TYPE", f"'{key}' must be an object", key))
        return {}
    return value


def validate(data: Any) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not isinstance(data, dict):
        return [Diagnostic("error", "BRIEF_ROOT", "Root must be a JSON object")]

    for key in ("schema_version", "project", "task_mode", "primary_intent"):
        if not is_nonempty(data.get(key)):
            diagnostics.append(Diagnostic("error", "BRIEF_REQUIRED", f"Missing non-empty '{key}'", key))

    if data.get("schema_version") != "1.0":
        diagnostics.append(Diagnostic("warning", "BRIEF_SCHEMA", "Expected schema_version '1.0'", "schema_version"))
    if data.get("task_mode") not in TASK_MODES:
        diagnostics.append(Diagnostic("error", "BRIEF_TASK_MODE", f"Unknown task_mode: {data.get('task_mode')!r}", "task_mode"))
    if data.get("primary_intent") not in INTENTS:
        diagnostics.append(Diagnostic("error", "BRIEF_INTENT", f"Unknown primary_intent: {data.get('primary_intent')!r}", "primary_intent"))
    secondary = data.get("secondary_intent")
    if secondary is not None and secondary not in INTENTS:
        diagnostics.append(Diagnostic("error", "BRIEF_SECONDARY", f"Unknown secondary_intent: {secondary!r}", "secondary_intent"))
    if secondary and secondary == data.get("primary_intent"):
        diagnostics.append(Diagnostic("warning", "BRIEF_DUP_INTENT", "Secondary intent duplicates primary intent", "secondary_intent"))

    audience = require_dict(data, "audience", diagnostics)
    for key in ("who", "context", "prior_state", "desired_state"):
        if not is_nonempty(audience.get(key)):
            diagnostics.append(Diagnostic("error", "BRIEF_AUDIENCE", f"Audience '{key}' is required", f"audience.{key}"))
    objections = audience.get("objections", [])
    if not isinstance(objections, list) or not all(isinstance(item, str) for item in objections):
        diagnostics.append(Diagnostic("error", "BRIEF_OBJECTIONS", "audience.objections must be an array of strings", "audience.objections"))

    for key in ("communication_job", "central_takeaway", "final_action"):
        if not is_nonempty(data.get(key)):
            diagnostics.append(Diagnostic("error", "BRIEF_STRATEGY", f"'{key}' is required", key))
    job = str(data.get("communication_job", ""))
    if len(job.split()) < 10:
        diagnostics.append(Diagnostic("warning", "BRIEF_JOB_THIN", "Communication job is unusually short; include audience, change, and reason", "communication_job"))

    delivery = require_dict(data, "delivery", diagnostics)
    if delivery.get("mode") not in DELIVERY_MODES:
        diagnostics.append(Diagnostic("error", "BRIEF_DELIVERY_MODE", f"Unknown delivery mode: {delivery.get('mode')!r}", "delivery.mode"))
    duration = delivery.get("duration_minutes")
    if duration is not None and (not isinstance(duration, (int, float)) or duration <= 0):
        diagnostics.append(Diagnostic("error", "BRIEF_DURATION", "duration_minutes must be positive or null", "delivery.duration_minutes"))
    count = delivery.get("slide_count_target")
    if count is not None and (not isinstance(count, int) or isinstance(count, bool) or count <= 0):
        diagnostics.append(Diagnostic("error", "BRIEF_SLIDE_COUNT", "slide_count_target must be a positive integer or null", "delivery.slide_count_target"))
    if delivery.get("aspect_ratio") not in ASPECT_RATIOS:
        diagnostics.append(Diagnostic("error", "BRIEF_ASPECT", f"Unknown aspect_ratio: {delivery.get('aspect_ratio')!r}", "delivery.aspect_ratio"))
    if not is_nonempty(delivery.get("language")):
        diagnostics.append(Diagnostic("error", "BRIEF_LANGUAGE", "delivery.language is required", "delivery.language"))
    formats = delivery.get("output_formats")
    if not isinstance(formats, list) or not formats or not all(is_nonempty(item) for item in formats):
        diagnostics.append(Diagnostic("error", "BRIEF_OUTPUT", "output_formats must be a non-empty array of strings", "delivery.output_formats"))
    if delivery.get("editability") not in EDITABILITY:
        diagnostics.append(Diagnostic("error", "BRIEF_EDITABILITY", f"Unknown editability: {delivery.get('editability')!r}", "delivery.editability"))

    brand = require_dict(data, "brand", diagnostics)
    if brand.get("status") not in BRAND_STATUS:
        diagnostics.append(Diagnostic("error", "BRIEF_BRAND", f"Unknown brand status: {brand.get('status')!r}", "brand.status"))
    for key in ("assets", "constraints"):
        if not isinstance(brand.get(key), list):
            diagnostics.append(Diagnostic("error", "BRIEF_BRAND_LIST", f"brand.{key} must be an array", f"brand.{key}"))

    source_policy = require_dict(data, "source_policy", diagnostics)
    if not isinstance(source_policy.get("research_allowed"), bool):
        diagnostics.append(Diagnostic("error", "BRIEF_RESEARCH", "source_policy.research_allowed must be boolean", "source_policy.research_allowed"))

    for key in ("invariants", "assumptions", "open_questions"):
        if not isinstance(data.get(key), list):
            diagnostics.append(Diagnostic("error", "BRIEF_LIST", f"'{key}' must be an array", key))

    if data.get("task_mode") in {"fill-template", "enhance-existing"} and not data.get("invariants"):
        diagnostics.append(Diagnostic("warning", "BRIEF_INVARIANTS", "Existing-deck route has no invariants; record what must remain unchanged", "invariants"))
    if data.get("open_questions"):
        diagnostics.append(Diagnostic("warning", "BRIEF_OPEN", "Open questions remain; confirm none materially changes the route or argument", "open_questions"))
    if delivery.get("editability") == "native-required" and formats and "pptx" not in {str(x).lower() for x in formats}:
        diagnostics.append(Diagnostic("warning", "BRIEF_NATIVE_FORMAT", "Native editability is required but PPTX is not requested", "delivery.output_formats"))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        data = load_json(args.brief)
    except ValueError as exc:
        return emit_report("brief validation", [Diagnostic("error", "BRIEF_JSON", str(exc))], json_output=args.json_output)
    return emit_report(
        "brief validation",
        validate(data),
        json_output=args.json_output,
        extra={"file": str(Path(args.brief).resolve())},
    )


if __name__ == "__main__":
    raise SystemExit(main())
