#!/usr/bin/env python3
"""Resolve model/tool/runtime capabilities into a conservative execution plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID_STATUS = {"available", "unavailable", "unknown", "delegated"}
KNOWN_IDS = {
    "text_reasoning",
    "image_understanding",
    "video_understanding",
    "image_generation",
    "image_editing",
    "video_generation",
    "web_research",
    "code_execution",
    "filesystem",
    "native_pptx_authoring",
    "web_slide_authoring",
    "slide_rendering",
    "pptx_roundtrip",
    "video_keyframe_extraction",
    "pdf_rasterization",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def validate_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if profile.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    entries = profile.get("capabilities")
    if not isinstance(entries, list):
        return errors + ["capabilities must be an array"]
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"capabilities[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        cid = entry.get("id")
        if not isinstance(cid, str) or not cid:
            errors.append(f"{prefix}.id is required")
        elif cid in seen:
            errors.append(f"duplicate capability id: {cid}")
        else:
            seen.add(cid)
        if entry.get("status") not in VALID_STATUS:
            errors.append(f"{prefix}.status must be one of {sorted(VALID_STATUS)}")
        if entry.get("status") == "delegated" and not entry.get("provider"):
            errors.append(f"{prefix}.provider is required for delegated status")
    missing = sorted(KNOWN_IDS - seen)
    if missing:
        errors.append("missing required capability ids: " + ", ".join(missing))
    return errors


def merge_local_scan(profile: dict[str, Any], scan: dict[str, Any]) -> None:
    entries = {item["id"]: item for item in profile["capabilities"]}

    def detected(cid: str, available: bool, provider: str) -> None:
        entry = entries[cid]
        if entry["status"] != "unknown":
            return
        entry["status"] = "available" if available else "unavailable"
        entry["provider"] = provider if available else None

    exe = scan["executables"]
    py = scan["python_modules"]
    node = scan["node_packages"]
    detected(
        "code_execution",
        exe["python"]["available"] or exe["node"]["available"],
        "local Python/Node",
    )
    detected("filesystem", True, "local filesystem")
    detected(
        "native_pptx_authoring",
        py["python-pptx"]["available"]
        or node["pptxgenjs"]["available"]
        or node["@oai/artifact-tool"]["available"],
        "python-pptx/PptxGenJS/artifact-tool",
    )
    detected(
        "web_slide_authoring",
        exe["node"]["available"],
        "local Node.js fixed-stage HTML",
    )
    detected(
        "slide_rendering",
        exe["powerpoint"]["available"] or exe["libreoffice"]["available"],
        "Microsoft PowerPoint/LibreOffice",
    )
    detected("pptx_roundtrip", exe["powerpoint"]["available"], "Microsoft PowerPoint")
    detected(
        "video_keyframe_extraction",
        exe["ffmpeg"]["available"] and exe["ffprobe"]["available"],
        "ffmpeg/ffprobe",
    )
    detected("pdf_rasterization", exe["pdftoppm"]["available"], "pdftoppm")


def resolve(profile: dict[str, Any], brief: dict[str, Any] | None = None) -> dict[str, Any]:
    caps = {item["id"]: item for item in profile["capabilities"]}
    separate = bool(profile.get("separate_tools_allowed"))

    def usable(cid: str) -> bool:
        status = caps[cid]["status"]
        return status == "available" or (status == "delegated" and separate)

    vision = usable("image_understanding")
    generation = usable("image_generation") or usable("video_generation")
    delegated = any(item["status"] == "delegated" for item in caps.values())
    if delegated and separate:
        mode = "orchestrated-multimodel"
    elif vision:
        mode = "multimodal" if generation else "text-plus-vision"
    elif generation:
        mode = "text-plus-generation"
    else:
        mode = "text-only"

    formats: list[str] = []
    if brief:
        formats = brief.get("delivery", {}).get("output_formats", []) or []
    wants_pptx = "pptx" in formats
    wants_web = any(value in formats for value in ("html", "web", "slidev"))
    wants_preview = "html-preview" in formats
    wants_pdf = "pdf" in formats
    artifact_routes: list[str] = []
    if wants_pptx and usable("native_pptx_authoring"):
        artifact_routes.append("native-pptx")
    if wants_web and usable("web_slide_authoring"):
        artifact_routes.append("web-slides")
    if wants_preview and usable("slide_rendering") and (
        not wants_pptx or usable("native_pptx_authoring")
    ):
        artifact_routes.append("pptx-render-preview")
    if wants_pdf and usable("slide_rendering") and artifact_routes:
        artifact_routes.append("pdf-export")
    if not formats:
        if usable("native_pptx_authoring"):
            artifact_routes.append("native-pptx")
        elif usable("web_slide_authoring"):
            artifact_routes.append("web-slides")
    artifact_route = (
        "plan-only"
        if not artifact_routes
        else (artifact_routes[0] if len(artifact_routes) == 1 else "multi-output")
    )

    warnings: list[str] = []
    gates: list[str] = []
    if not usable("text_reasoning"):
        warnings.append("No usable text reasoning capability; deck strategy cannot proceed.")
    if not vision:
        warnings.append("Asset semantics require a human or delegated vision reviewer.")
    if generation and not vision:
        gates.append("Generated media must pass external visual review before final use.")
    if not usable("video_understanding"):
        if usable("video_keyframe_extraction") and vision:
            warnings.append("Video review is keyframe-only unless transcript/audio review is added.")
        else:
            warnings.append("Video meaning must come from a user summary or delegated reviewer.")
    if artifact_route != "plan-only" and not usable("slide_rendering"):
        gates.append("Final artifact requires external render review.")
    if wants_pptx and "native-pptx" not in artifact_routes:
        warnings.append("Requested PPTX cannot be produced natively with verified capabilities.")
    if wants_web and "web-slides" not in artifact_routes:
        warnings.append("Requested web slides cannot be produced with verified capabilities.")
    if wants_preview and "pptx-render-preview" not in artifact_routes:
        warnings.append("Requested HTML presenter preview requires final slide renders.")
    if wants_pdf and "pdf-export" not in artifact_routes:
        warnings.append("Requested PDF requires a rendered artifact route or external export.")
    if wants_pptx and not usable("pptx_roundtrip"):
        warnings.append("PowerPoint round-trip compatibility is unverified.")

    media_route = {
        "input_review": (
            "direct-vision"
            if vision
            else "technical-inventory-plus-human-or-delegated-semantic-review"
        ),
        "video_review": (
            "direct-video-understanding"
            if usable("video_understanding")
            else (
                "keyframes-plus-transcript"
                if usable("video_keyframe_extraction") and vision
                else "user-summary-and-static-fallback"
            )
        ),
        "image_creation": (
            "generate-and-vision-review"
            if usable("image_generation") and vision
            else (
                "generate-then-external-review"
                if usable("image_generation")
                else "supplied-or-native-visuals"
            )
        ),
        "video_creation": (
            "generate-with-review-and-static-fallback"
            if usable("video_generation")
            else "no-generated-video"
        ),
    }
    intent = str(brief.get("primary_intent", "")) if isinstance(brief, dict) else ""
    generation_jobs_by_intent = {
        "portfolio": ["original section treatment", "supporting conceptual visual that does not replace real work"],
        "work-results": ["cover hero or contextual scene; keep result evidence native"],
        "business-proposal": ["cover hero", "conceptual mechanism visual"],
        "sales": ["cover hero", "product-in-context concept"],
        "investor-pitch": ["vision hero", "product or market context concept"],
        "strategy-decision": ["cover hero", "future-state concept"],
        "research-technical": ["explanatory illustration with native labels"],
        "teaching-workshop": ["concept illustration or memorable example scene"],
        "keynote-launch": ["cover hero", "section hero", "product concept"],
        "report-async": ["optional section or context visual"],
        "template-system": ["style-validation hero asset"],
    }
    image_generation = usable("image_generation")
    video_generation = usable("video_generation")
    creative_route = {
        "opportunity_audit": "required",
        "visual_generation_plan": "visual-generation-plan.json",
        "image_generation": (
            "active-with-agent-review"
            if image_generation and vision
            else (
                "draft-only-external-review"
                if image_generation
                else "unavailable-use-supplied-or-native"
            )
        ),
        "video_generation": (
            "active-only-when-motion-is-essential"
            if video_generation
            else "unavailable-or-not-selected"
        ),
        "recommended_jobs": generation_jobs_by_intent.get(
            intent, ["evaluate one distinctive hero, context, or explanatory visual"]
        ),
        "default_budget": {
            "image_candidates": 2 if image_generation else 0,
            "final_unique_images": 1 if image_generation else 0,
            "video_candidates": 1 if video_generation else 0,
        },
        "distinctness_rule": "one primary generated asset per unique slide job; do not reuse a hero as repeated proof",
        "review": "vision-agent" if image_generation and vision else "human-or-delegated-required",
    }
    qa_route = {
        "structural": "local" if usable("code_execution") else "host-or-manual",
        "render": "local" if usable("slide_rendering") else "external-required",
        "visual_inspection": "agent" if vision else "human-or-delegated-required",
        "pptx_roundtrip": "verified-route" if usable("pptx_roundtrip") else "unverified",
    }
    return {
        "schema_version": "1.0",
        "operating_mode": mode,
        "artifact_route": artifact_route,
        "artifact_routes": artifact_routes,
        "requested_formats": formats,
        "media_route": media_route,
        "creative_route": creative_route,
        "qa_route": qa_route,
        "blocking_gates": gates,
        "warnings": warnings,
        "capability_snapshot": {
            cid: {"status": item["status"], "provider": item.get("provider")}
            for cid, item in sorted(caps.items())
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--brief", type=Path)
    parser.add_argument("--scan-local", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    profile = load_json(args.profile)
    errors = validate_profile(profile)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.scan_local:
        from capability_scan import build_report

        merge_local_scan(profile, build_report())
    brief = load_json(args.brief) if args.brief else None
    plan = resolve(profile, brief)
    rendered = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Execution plan written: {args.output.resolve()}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
