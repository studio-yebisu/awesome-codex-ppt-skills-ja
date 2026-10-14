#!/usr/bin/env python3
"""Run dependency-free smoke tests for PradaSlides contracts and validators."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from lint_deck_plan import validate as lint_plan
from resolve_capabilities import resolve as resolve_capabilities
from resolve_capabilities import validate_profile
from scaffold_presenter import create_deck as create_presenter_deck
from validate_asset_manifest import validate as validate_assets
from validate_brief import validate as validate_brief
from validate_design_system import validate as validate_design_system
from validate_layout_manifest import validate as validate_layout_manifest
from validate_reference_benchmark import validate as validate_reference_benchmark
from validate_source_ledger import validate as validate_ledger
from validate_visual_generation_plan import validate as validate_generation_plan


def valid_brief(intent: str) -> dict:
    return {
        "schema_version": "1.0",
        "project": f"Smoke test: {intent}",
        "task_mode": "new",
        "primary_intent": intent,
        "secondary_intent": None,
        "audience": {
            "who": "A defined review audience",
            "context": "A scheduled review",
            "prior_state": "Aware of the topic but not aligned",
            "desired_state": "Aligned on the central takeaway and next action",
            "decision_authority": "Review owner",
            "objections": ["Evidence quality", "Implementation effort"],
        },
        "communication_job": (
            "By the end, the review audience should support the proposed next action "
            "because the evidence resolves the most important uncertainty."
        ),
        "central_takeaway": "The evidence supports a bounded next action.",
        "final_action": "Confirm the next action and owner",
        "delivery": {
            "mode": "hybrid",
            "duration_minutes": 10,
            "slide_count_target": 3,
            "aspect_ratio": "16:9",
            "language": "en",
            "output_formats": ["pptx"],
            "editability": "native-preferred",
        },
        "brand": {"status": "none", "assets": [], "constraints": []},
        "source_policy": {
            "research_allowed": True,
            "citations": "visible-for-key-claims",
            "confidentiality": "test",
        },
        "invariants": [],
        "assumptions": [],
        "open_questions": [],
    }


def valid_ledger() -> dict:
    return {
        "schema_version": "1.0",
        "sources": [
            {
                "id": "S01",
                "kind": "supplied-file",
                "title": "Verified test source",
                "uri_or_path": "sources/test.pdf",
                "publisher_or_owner": "Test owner",
                "date": "2026-07-22",
                "retrieved": None,
                "location": "p. 1",
                "supports": ["C01"],
                "status": "verified",
                "license_or_permission": "test fixture",
                "notes": "",
            }
        ],
        "claims": [
            {
                "id": "C01",
                "text": "The supplied evidence resolves the primary uncertainty.",
                "class": "supplied-fact",
                "source_ids": ["S01"],
                "status": "verified",
                "slide_ids": ["P02"],
            }
        ],
    }


def valid_plan(brief: dict) -> dict:
    return {
        "schema_version": "1.1",
        "project": brief["project"],
        "communication_job": brief["communication_job"],
        "design_direction": {
            "name": "Measured clarity",
            "communication_mode": "hybrid",
            "visual_cluster": "corporate-editorial",
            "character": ["clear", "credible", "specific"],
            "grid": "12-column",
            "type": "Large claim titles and neutral sans body",
            "palette": "Warm white, charcoal, cobalt accent",
            "media": "Native chart and one source visual",
            "topology_rhythm": "stage to axis to stage with two tone shifts",
            "reference_quality_floor": "Decisive scale, inspectable evidence, and clear visual rhythm",
        },
        "slides": [
            {
                "id": "P01",
                "role": "cover",
                "journey_phase": "orientation",
                "job": "Frame the review",
                "audience_question": "What are we deciding?",
                "title": "A bounded next action for the key uncertainty",
                "claim": None,
                "evidence_ids": [],
                "visual_role": "Establish context",
                "visual_form": "Single contextual visual",
                "layout_family": "cover-hero",
                "layout_id": "hero-decision",
                "topology": "stage",
                "tone": "dark",
                "emphasis": "decision headline",
                "slot_budget": {"headline_lines": 2, "body_words": 0, "peer_items": 1, "media": 1},
                "density": "speaking",
                "transition": "Start with the evidence.",
                "speaker_notes_purpose": "Set the scope",
                "source_ids": [],
                "asset_ids": [],
                "media_plan": None,
            },
            {
                "id": "P02",
                "role": "content",
                "journey_phase": "proof",
                "job": "Resolve the uncertainty",
                "audience_question": "What does the evidence show?",
                "title": "The supplied evidence resolves the primary uncertainty",
                "claim": "The supplied evidence resolves the primary uncertainty.",
                "evidence_ids": ["C01"],
                "visual_role": "Show the decisive evidence",
                "visual_form": "Annotated comparison",
                "layout_family": "evidence-led",
                "layout_id": "ranked-evidence-axis",
                "topology": "axis",
                "tone": "light",
                "emphasis": "decisive evidence",
                "slot_budget": {"headline_lines": 2, "body_words": 24, "peer_items": 4, "media": 0},
                "density": "hybrid",
                "transition": "Convert the finding into a next step.",
                "speaker_notes_purpose": "Explain the source boundary",
                "source_ids": ["S01"],
                "asset_ids": [],
                "media_plan": None,
            },
            {
                "id": "P03",
                "role": "closing",
                "journey_phase": "decision",
                "job": "Secure the next action",
                "audience_question": "What should happen next?",
                "title": "Confirm the next action and owner",
                "claim": None,
                "evidence_ids": [],
                "visual_role": "Make ownership visible",
                "visual_form": "Action and owner lockup",
                "layout_family": "decision-close",
                "layout_id": "decision-lock",
                "topology": "stage",
                "tone": "dark",
                "emphasis": "next action",
                "slot_budget": {"headline_lines": 2, "body_words": 18, "peer_items": 3, "media": 0},
                "density": "speaking",
                "transition": "Move to discussion.",
                "speaker_notes_purpose": "State the ask",
                "source_ids": [],
                "asset_ids": [],
                "media_plan": None,
            },
        ],
    }


def valid_asset_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "root": "assets",
        "assets": [
            {
                "id": "A01",
                "path": "assets/test.png",
                "kind": "image",
                "sha256": "0" * 64,
                "bytes": 1024,
                "duplicate_of": None,
                "filename_hint": "product",
                "technical": {
                    "width": 1600,
                    "height": 900,
                    "aspect": 1.7778,
                    "orientation": "landscape",
                },
                "semantic": {
                    "review_status": "reviewed",
                    "role": "product-evidence",
                    "subject": "Test product",
                    "context": "Test fixture",
                    "message": "The product state supports the slide claim",
                    "focal_point": "center",
                    "directionality": "neutral",
                    "text_safe_regions": ["left"],
                    "protected_regions": ["center"],
                    "crop_tolerance": "low",
                    "quality": "good",
                    "rights": "owned",
                    "attribution": "",
                    "sensitivity": "none",
                    "alt_text": "Test product interface in its completed state",
                },
                "placement": {
                    "recommended": "contained on the right",
                    "avoid": ["cropping the focal product"],
                    "journey_phases": ["proof"],
                    "slide_candidates": ["P02"],
                },
            }
        ],
    }


def valid_generation_plan() -> dict:
    return {
        "schema_version": "1.0",
        "capability_status": "available",
        "decision": "use",
        "decision_reason": "A unique conceptual cover hero improves entry without replacing evidence.",
        "budget": {"image_candidates": 2, "final_unique_images": 1, "video_candidates": 0},
        "operations": [
            {
                "id": "IMG-P01-01",
                "slide_ids": ["P01"],
                "purpose": "Create the cover hero",
                "use_case": "stylized-concept",
                "asset_type": "full-bleed cover",
                "narrative_job": "express one controlled path through complexity",
                "composition": "16:9 with left text-safe space",
                "difference_from_other_visuals": "Conceptual only; later slides use native evidence",
                "prompt": "Create an original abstract operational-flow sculpture with no text.",
                "constraints": ["no text", "no logo", "no UI"],
                "avoid": ["stock office", "flowchart boxes"],
                "expected_output": "assets/generated/P01-hero.png",
                "review": {
                    "required": True,
                    "reviewer": "vision-capable agent",
                    "checks": ["prompt adherence", "crop", "artifacts", "distinctness"],
                },
                "fallback": "native typographic hero",
                "provenance": {
                    "provider": "test generator",
                    "model": "test",
                    "created_at": "2026-07-22T00:00:00Z",
                    "prompt_saved": True,
                },
                "status": "reviewed",
            }
        ],
    }


def valid_reference_benchmark() -> dict:
    criteria = []
    floors = {
        "identity": 8.5,
        "hierarchy": 8.7,
        "typography": 8.4,
        "composition": 8.6,
        "media": 8.4,
        "proof": 8.7,
        "rhythm": 8.5,
        "runtime": 8.5,
        "accessibility": 8.0,
        "originality": 8.5,
        "materiality": 8.3,
        "native-fidelity": 8.5,
    }
    for criterion_id, floor in floors.items():
        criteria.append(
            {
                "id": criterion_id,
                "score": floor + 0.2,
                "floor": floor,
                "status": "pass",
                "rationale": "Rendered fixture meets the declared floor.",
                "evidence": ["renders/slide-montage.png"],
            }
        )
    return {
        "schema_version": "1.0",
        "candidate": "HTML smoke fixture",
        "target_runtime": "html",
        "status": "final",
        "review": {
            "reviewer": "smoke-test reviewer",
            "method": "fixture render review",
            "reviewed_at": "2026-07-22T12:00:00Z",
        },
        "reference_policy": {
            "mode": "principles-not-layouts",
            "references": [
                {
                    "id": "R01",
                    "path": "references/example.png",
                    "cluster": "corporate-clean",
                    "usage": "quality-floor",
                    "transferable_principle": "Use decisive hierarchy and inspectable proof.",
                    "avoid": "Do not copy the original layout or assets.",
                }
            ],
        },
        "criteria": criteria,
        "render_evidence": {
            "entrypoint": "presenter/index.html",
            "slide_count": 3,
            "slide_montage": "renders/slide-montage.png",
            "console_capture": "renders/presenter-console.png",
            "browser_qa": "qa/html-presenter.json",
            "viewport": "1600x900 slides; 1900x854 console",
        },
        "blockers": [],
        "repairs": ["Repaired one title wrap after render review."],
    }


def errors(diagnostics: list) -> list:
    return [item for item in diagnostics if item.severity == "error"]


def main() -> int:
    failures: list[str] = []
    starter_dir = Path(__file__).resolve().parents[1] / "assets" / "starter"
    starter_profile = json.loads((starter_dir / "capability-profile.json").read_text(encoding="utf-8"))
    design_system = json.loads((starter_dir / "design-system.json").read_text(encoding="utf-8"))
    layout_manifest = json.loads((starter_dir / "layout-manifest.json").read_text(encoding="utf-8"))
    starter_reference_benchmark = json.loads((starter_dir / "reference-benchmark.json").read_text(encoding="utf-8"))
    if errors(validate_design_system(design_system)):
        failures.append("starter design system was rejected")
    typography_selection = design_system.get("typography", {}).get("selection")
    if not isinstance(typography_selection, dict) or not typography_selection.get("rationale"):
        failures.append("starter design system omitted product-specific typography selection")
    art_direction = design_system.get("art_direction")
    if not isinstance(art_direction, dict) or not art_direction.get("visual_thesis"):
        failures.append("starter design system omitted executable art direction")
    invalid_art_direction = copy.deepcopy(design_system)
    invalid_art_direction["art_direction"].pop("native_raster_strategy")
    if not errors(validate_design_system(invalid_art_direction)):
        failures.append("design system accepted a missing native/raster strategy")
    invalid_typography = copy.deepcopy(design_system)
    invalid_typography["typography"]["selection"]["rationale"] = "Modern clean"
    if not errors(validate_design_system(invalid_typography)):
        failures.append("design system accepted a non-specific typography rationale")
    invalid_contrast = copy.deepcopy(design_system)
    invalid_contrast["color"]["tones"]["light"]["text"] = invalid_contrast["color"]["tones"]["light"]["background"]
    if not errors(validate_design_system(invalid_contrast)):
        failures.append("design system accepted unreadable text/background colors")
    if errors(validate_layout_manifest(layout_manifest)):
        failures.append("starter layout manifest was rejected")
    if validate_profile(starter_profile):
        failures.append("starter capability profile was rejected")
    if errors(validate_reference_benchmark(starter_reference_benchmark, False)):
        failures.append("starter reference benchmark was rejected")
    scaffold_deck = create_presenter_deck(valid_plan(valid_brief("business-proposal")), design_system)
    if not scaffold_deck.get("slides") or any(
        "prada-composition" not in str(slide.get("html", ""))
        for slide in scaffold_deck.get("slides", [])
    ):
        failures.append("HTML scaffold omitted topology composition regions")
    composition_css = (
        Path(__file__).resolve().parents[1] / "assets" / "html-presenter" / "deck.css"
    ).read_text(encoding="utf-8")
    required_topology_selectors = {
        f".topology-{topology}"
        for topology in ("stage", "split", "spine", "axis", "matrix", "stack", "network", "mosaic", "field", "frame")
    }
    if any(selector not in composition_css for selector in required_topology_selectors):
        failures.append("HTML starter CSS omitted one or more topology silhouettes")
    presenter_runtime = Path(__file__).resolve().parents[1] / "assets" / "html-presenter"
    presenter_css = (presenter_runtime / "presenter.css").read_text(encoding="utf-8")
    presenter_js = (presenter_runtime / "presenter.js").read_text(encoding="utf-8")
    html_qa = (Path(__file__).resolve().parent / "qa_html_presenter.mjs").read_text(encoding="utf-8")
    if not all(token in presenter_css for token in (".stage-scaler", "position: absolute", "left: 50%", "top: 50%", "translate(-50%, -50%) scale(.05)")):
        failures.append("HTML stage scaler is not explicitly center-positioned")
    if not all(token in presenter_js for token in ("translate(-50%, -50%) scale(${scale})", "ResizeObserver", "viewportObserver.observe(dom.viewport)")):
        failures.append("HTML stage scaler transform can drift beneath console panels")
    if not all(token in html_qa for token in ("HTML_TEXT_SAFE_AREA", "HTML_TEXT_COLLISION", "HTML_TEXT_OBSTRUCTION", "edgeUnsafe", "textCollisions", "textObstructions")):
        failures.append("HTML QA omitted hard text-safe-area, collision, or layout-obstruction gates")
    for viewport_width, viewport_height in ((1026, 686), (744, 580), (1336, 724), (1600, 900)):
        scale = min(viewport_width / 1600, viewport_height / 900)
        left = (viewport_width - 1600 * scale) / 2
        top = (viewport_height - 900 * scale) / 2
        if left < -0.01 or top < -0.01:
            failures.append("centered HTML stage-fit calculation exceeded a representative viewport")
            break
    text_only = resolve_capabilities(starter_profile, valid_brief("business-proposal"))
    if text_only["operating_mode"] != "text-only":
        failures.append("text-only capability mode resolved incorrectly")

    multimodal_profile = copy.deepcopy(starter_profile)
    for item in multimodal_profile["capabilities"]:
        if item["id"] in {
            "image_understanding",
            "image_generation",
            "native_pptx_authoring",
            "slide_rendering",
            "pptx_roundtrip",
        }:
            item["status"] = "available"
            item["provider"] = "test provider"
    multimodal = resolve_capabilities(multimodal_profile, valid_brief("business-proposal"))
    if multimodal["operating_mode"] != "multimodal" or multimodal["artifact_route"] != "native-pptx":
        failures.append("multimodal native-PPTX route resolved incorrectly")

    multi_profile = copy.deepcopy(multimodal_profile)
    next(item for item in multi_profile["capabilities"] if item["id"] == "web_slide_authoring")["status"] = "available"
    next(item for item in multi_profile["capabilities"] if item["id"] == "web_slide_authoring")["provider"] = "test HTML runtime"
    multi_brief = valid_brief("business-proposal")
    multi_brief["delivery"]["output_formats"] = ["html", "pptx", "pdf"]
    multi = resolve_capabilities(multi_profile, multi_brief)
    if multi["artifact_route"] != "multi-output" or set(multi["artifact_routes"]) != {"native-pptx", "web-slides", "pdf-export"}:
        failures.append("multi-output HTML/PPTX/PDF route resolved incorrectly")

    delegated_profile = copy.deepcopy(starter_profile)
    delegated_item = next(
        item for item in delegated_profile["capabilities"] if item["id"] == "image_understanding"
    )
    delegated_item["status"] = "delegated"
    delegated_item["provider"] = "separate vision model"
    delegated = resolve_capabilities(delegated_profile, valid_brief("portfolio"))
    if delegated["operating_mode"] != "orchestrated-multimodel":
        failures.append("delegated multimodel route resolved incorrectly")

    generation_only_profile = copy.deepcopy(starter_profile)
    generated_item = next(
        item for item in generation_only_profile["capabilities"] if item["id"] == "image_generation"
    )
    generated_item["status"] = "available"
    generated_item["provider"] = "test image generator"
    generation_only = resolve_capabilities(generation_only_profile, valid_brief("portfolio"))
    if not any("external visual review" in gate for gate in generation_only["blocking_gates"]):
        failures.append("generation-without-vision review gate was not enforced")
    if generation_only["creative_route"]["opportunity_audit"] != "required":
        failures.append("generation opportunity audit was not activated")

    generation_plan = valid_generation_plan()
    if errors(validate_generation_plan(generation_plan, True)):
        failures.append("valid visual generation plan was rejected")
    reference_benchmark = valid_reference_benchmark()
    if errors(validate_reference_benchmark(reference_benchmark, True)):
        failures.append("valid final reference benchmark was rejected")
    native_pptx_benchmark = valid_reference_benchmark()
    native_pptx_benchmark["candidate"] = "Native PPTX smoke fixture"
    native_pptx_benchmark["target_runtime"] = "native-pptx"
    native_pptx_benchmark["render_evidence"] = {
        "pptx_file": "deck/final.pptx",
        "slide_count": 3,
        "slide_montage": "renders/slide-montage.png",
        "package_inspection": "qa/pptx-package.json",
        "viewport": "16:9 render at 1920x1080",
    }
    if errors(validate_reference_benchmark(native_pptx_benchmark, True)):
        failures.append("valid native-PPTX reference benchmark was rejected")
    missing_evidence_root = Path("__pradaslides_missing_evidence__")
    draft_evidence_benchmark = valid_reference_benchmark()
    draft_evidence_benchmark["status"] = "draft"
    draft_evidence_benchmark["reference_policy"]["references"][0]["path"] = "https://example.com/reference.png"
    draft_evidence_diagnostics = validate_reference_benchmark(
        draft_evidence_benchmark, False, missing_evidence_root
    )
    if errors(draft_evidence_diagnostics):
        failures.append("draft benchmark with pending render evidence was rejected")
    if not any(item.code == "REFBENCH_RENDER_PATH" for item in draft_evidence_diagnostics):
        failures.append("draft benchmark did not report pending render evidence")
    final_missing_benchmark = valid_reference_benchmark()
    final_missing_benchmark["reference_policy"]["references"][0]["path"] = "https://example.com/reference.png"
    final_missing_diagnostics = validate_reference_benchmark(final_missing_benchmark, False, missing_evidence_root)
    if not errors(final_missing_diagnostics):
        failures.append("final benchmark with missing render evidence was accepted")
    coverage_benchmark = valid_reference_benchmark()
    coverage_benchmark["render_evidence"]["slide_count"] = 1
    coverage_benchmark["coverage"] = {
        "mode": "one-slide-per-reference",
        "mappings": [{"reference_id": "R01", "slide_id": "P01", "response": "Original HTML composition translates the specific reference principle into visible geometry.", "status": "pass"}],
    }
    if errors(validate_reference_benchmark(coverage_benchmark, True)):
        failures.append("valid one-slide-per-reference coverage was rejected")

    ledger = valid_ledger()
    if errors(validate_ledger(ledger)):
        failures.append("valid source ledger was rejected")
    asset_manifest = valid_asset_manifest()
    if errors(validate_assets(asset_manifest, Path("asset-manifest.json"), True, False)):
        failures.append("valid reviewed asset manifest was rejected")

    for intent in ("business-proposal", "portfolio", "research-technical"):
        brief = valid_brief(intent)
        plan = valid_plan(brief)
        if errors(validate_brief(brief)):
            failures.append(f"valid {intent} brief was rejected")
        plan_diagnostics, _ = lint_plan(
            plan,
            brief,
            ledger,
            None,
            design_system,
            layout_manifest,
            True,
        )
        if errors(plan_diagnostics):
            failures.append(f"valid {intent} deck plan was rejected")

    media_brief = valid_brief("portfolio")
    media_plan = valid_plan(media_brief)
    media_plan["slides"][1]["asset_ids"] = ["A01"]
    media_plan["slides"][1]["layout_id"] = "artifact-proof-frame"
    media_plan["slides"][1]["topology"] = "frame"
    media_plan["slides"][1]["visual_form"] = "Contained interface proof with native annotation"
    media_plan["slides"][1]["slot_budget"]["media"] = 1
    media_plan["slides"][1]["media_plan"] = {
        "purpose": "Show the product state that supports the claim",
        "treatment": "contained image with native annotation",
        "placement": "right half",
        "crop_mode": "contain",
        "focal_anchor": "center",
        "text_safe_region": "left",
        "fallback": "same image without annotation",
        "alt_text": "Test product interface in its completed state",
    }
    media_diagnostics, _ = lint_plan(
        media_plan,
        media_brief,
        ledger,
        asset_manifest,
        design_system,
        layout_manifest,
        True,
    )
    if errors(media_diagnostics):
        failures.append("valid asset-backed deck plan was rejected")

    multi_assets = copy.deepcopy(asset_manifest)
    logo_asset = copy.deepcopy(multi_assets["assets"][0])
    logo_asset["id"] = "A02"
    logo_asset["path"] = "assets/test-logo.svg"
    logo_asset["semantic"]["role"] = "logo"
    logo_asset["semantic"]["crop_tolerance"] = "none"
    logo_asset["semantic"]["alt_text"] = "Test wordmark"
    multi_assets["assets"].append(logo_asset)
    multi_plan = copy.deepcopy(media_plan)
    multi_plan["slides"][1]["asset_ids"] = ["A01", "A02"]
    multi_plan["slides"][1]["media_plan"]["asset_treatments"] = [
        {
            "asset_id": "A01",
            "treatment": "contained evidence image",
            "placement": "right half",
            "crop_mode": "contain",
            "focal_anchor": "center",
            "text_safe_region": "left",
            "fallback": "same image",
            "alt_text": "Test product interface in its completed state",
        },
        {
            "asset_id": "A02",
            "treatment": "unaltered logo",
            "placement": "top left",
            "crop_mode": "contain",
            "focal_anchor": "center",
            "text_safe_region": "own clear-space box",
            "fallback": "text wordmark",
            "alt_text": "Test wordmark",
        },
    ]
    multi_diagnostics, _ = lint_plan(multi_plan, media_brief, ledger, multi_assets, design_system, layout_manifest, True)
    if errors(multi_diagnostics):
        failures.append("valid per-asset media treatments were rejected")
    bad_multi_plan = copy.deepcopy(multi_plan)
    bad_multi_plan["slides"][1]["media_plan"].pop("asset_treatments")
    bad_multi_diagnostics, _ = lint_plan(bad_multi_plan, media_brief, ledger, multi_assets, design_system, layout_manifest, True)
    if not errors(bad_multi_diagnostics):
        failures.append("strict multi-asset plan without per-asset treatments was accepted")

    bad_brief = valid_brief("portfolio")
    bad_brief["audience"]["who"] = ""
    if not errors(validate_brief(bad_brief)):
        failures.append("invalid brief was accepted")

    bad_ledger = valid_ledger()
    bad_ledger["claims"][0]["source_ids"] = ["S99"]
    if not errors(validate_ledger(bad_ledger)):
        failures.append("ledger with missing source was accepted")

    bad_assets = valid_asset_manifest()
    bad_assets["assets"][0]["semantic"]["review_status"] = "pending"
    if not errors(validate_assets(bad_assets, Path("asset-manifest.json"), True, False)):
        failures.append("pending asset review was accepted")

    brief = valid_brief("business-proposal")
    bad_plan = valid_plan(brief)
    bad_plan["slides"][1]["title"] = "TODO add title"
    diagnostics, _ = lint_plan(
        bad_plan,
        brief,
        ledger,
        None,
        design_system,
        layout_manifest,
        True,
    )
    if not errors(diagnostics):
        failures.append("plan with placeholder title was accepted")

    bad_generation = valid_generation_plan()
    bad_generation["decision"] = "skip"
    bad_generation["decision_reason"] = ""
    bad_generation["operations"] = []
    if not errors(validate_generation_plan(bad_generation, True)):
        failures.append("unexplained generation skip was accepted")

    bad_benchmark = valid_reference_benchmark()
    bad_benchmark["criteria"][0]["score"] = 4.0
    if not errors(validate_reference_benchmark(bad_benchmark, True)):
        failures.append("reference benchmark below its floor was accepted")
    bad_coverage = copy.deepcopy(coverage_benchmark)
    bad_coverage["coverage"]["mappings"] = []
    if not errors(validate_reference_benchmark(bad_coverage, True)):
        failures.append("empty every-reference coverage was accepted")
    short_coverage = copy.deepcopy(coverage_benchmark)
    short_coverage["coverage"]["mappings"][0]["response"] = "Generic response"
    if not errors(validate_reference_benchmark(short_coverage, True)):
        failures.append("underspecified exhaustive coverage response was accepted")
    duplicate_coverage = copy.deepcopy(coverage_benchmark)
    second_reference = copy.deepcopy(duplicate_coverage["reference_policy"]["references"][0])
    second_reference["id"] = "R02"
    duplicate_coverage["reference_policy"]["references"].append(second_reference)
    duplicate_coverage["render_evidence"]["slide_count"] = 2
    duplicate_coverage["coverage"]["mappings"].append(
        {
            "reference_id": "R02",
            "slide_id": "P02",
            "response": duplicate_coverage["coverage"]["mappings"][0]["response"],
            "status": "pass",
        }
    )
    if not errors(validate_reference_benchmark(duplicate_coverage, True)):
        failures.append("duplicate exhaustive coverage responses were accepted")

    bad_topology = valid_plan(brief)
    bad_topology["slides"][1]["topology"] = "stage"
    diagnostics, _ = lint_plan(
        bad_topology,
        brief,
        ledger,
        None,
        design_system,
        layout_manifest,
        True,
    )
    if not errors(diagnostics):
        failures.append("layout/topology mismatch was accepted")

    if failures:
        print("PradaSlides self-test: FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("PradaSlides self-test: PASSED")
    print("  - valid briefs/plans: business-proposal, portfolio, research-technical")
    print("  - valid reviewed media manifest, asset-backed plan, and per-asset treatments accepted")
    print("  - text-only, multimodal, delegated-model, multi-output, and generation-without-vision routes accepted")
    print("  - design-system, topology registry, strict visual floor, generation plan, reference benchmark, and corpus coverage accepted")
    print("  - HTML scaffold composition regions and ten topology silhouettes present")
    print("  - centered stage scaler fits representative short and narrow presenter viewports")
    print("  - hard rendered text-safe-area, collision, and layout-obstruction gates present")
    print("  - invalid brief, provenance, media-review, multi-asset treatment, placeholder, generation-skip, reference-floor, empty/weak/duplicate coverage, and topology cases rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
