#!/usr/bin/env python3
"""Lint a PradaSlides deck-plan.json for narrative and production readiness."""

from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


SLIDE_ID = re.compile(r"^P\d{2,}$")
ROLES = {"cover", "section", "content", "pause", "closing", "appendix"}
PHASES = {"attention", "orientation", "tension", "insight", "proof", "resolution", "decision", "retention"}
DENSITIES = {"speaking", "hybrid", "reading"}
PLACEHOLDERS = re.compile(r"\b(todo|tbd|lorem ipsum|add title|sample text|placeholder|xx%|x/xx)\b", re.I)
TOPICAL_TITLES = re.compile(r"^(overview|introduction|agenda|background|problem|solution|our process|market overview|results|conclusion|summary)$", re.I)
TITLE_LIMIT = {"speaking": 16, "hybrid": 20, "reading": 24}


def words(value: Any) -> int:
    return len(str(value or "").split())


def validate(
    plan: Any,
    brief: Any | None,
    ledger: Any | None,
    asset_manifest: Any | None = None,
    design_system: Any | None = None,
    layout_manifest: Any | None = None,
    strict_visual: bool = False,
) -> tuple[list[Diagnostic], dict[str, Any]]:
    diagnostics: list[Diagnostic] = []
    stats: dict[str, Any] = {}
    if not isinstance(plan, dict):
        return [Diagnostic("error", "PLAN_ROOT", "Root must be a JSON object")], stats
    slides = plan.get("slides")
    if not isinstance(slides, list) or not slides:
        return [Diagnostic("error", "PLAN_SLIDES", "slides must be a non-empty array", "slides")], stats
    if not str(plan.get("communication_job", "")).strip():
        diagnostics.append(Diagnostic("error", "PLAN_JOB", "communication_job is required", "communication_job"))
    if not isinstance(plan.get("design_direction"), dict):
        diagnostics.append(Diagnostic("error", "PLAN_DESIGN", "design_direction must be an object", "design_direction"))

    known_claims = set()
    known_sources = set()
    if isinstance(ledger, dict):
        known_claims = {item.get("id") for item in ledger.get("claims", []) if isinstance(item, dict)}
        known_sources = {item.get("id") for item in ledger.get("sources", []) if isinstance(item, dict)}

    known_assets: dict[str, dict[str, Any]] = {}
    if isinstance(asset_manifest, dict):
        known_assets = {
            item.get("id"): item
            for item in asset_manifest.get("assets", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
    asset_usage: Counter[str] = Counter()

    known_layouts: dict[str, dict[str, Any]] = {}
    known_topologies: set[str] = set()
    allow_custom_layouts = False
    if isinstance(layout_manifest, dict):
        known_layouts = {
            item.get("id"): item
            for item in layout_manifest.get("layouts", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        known_topologies = {
            item.get("id")
            for item in layout_manifest.get("topologies", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        allow_custom_layouts = bool(layout_manifest.get("allow_custom_layouts"))

    seen_ids: set[str] = set()
    titles: list[str] = []
    layouts: list[str] = []
    visual_forms: list[str] = []
    roles: list[str] = []
    phases: list[str] = []
    topologies: list[str] = []
    tones: list[str] = []
    card_grid_count = 0
    for index, slide in enumerate(slides):
        loc = f"slides[{index}]"
        if not isinstance(slide, dict):
            diagnostics.append(Diagnostic("error", "PLAN_SLIDE_TYPE", "Slide must be an object", loc))
            continue
        slide_id = slide.get("id")
        if not isinstance(slide_id, str) or not SLIDE_ID.match(slide_id):
            diagnostics.append(Diagnostic("error", "PLAN_SLIDE_ID", "id must match P01, P02, ...", f"{loc}.id"))
            slide_id = loc
        elif slide_id in seen_ids:
            diagnostics.append(Diagnostic("error", "PLAN_DUP_ID", f"Duplicate slide id {slide_id}", f"{loc}.id"))
        seen_ids.add(str(slide_id))

        role = slide.get("role")
        roles.append(str(role))
        if role not in ROLES:
            diagnostics.append(Diagnostic("error", "PLAN_ROLE", f"Unknown role {role!r}", f"{loc}.role"))
        phase = slide.get("journey_phase")
        phases.append(str(phase))
        if phase not in PHASES:
            diagnostics.append(Diagnostic("error", "PLAN_PHASE", f"Unknown journey phase {phase!r}", f"{loc}.journey_phase"))
        density = slide.get("density")
        if density not in DENSITIES:
            diagnostics.append(Diagnostic("error", "PLAN_DENSITY", f"Unknown density {density!r}", f"{loc}.density"))

        for key in ("job", "title", "visual_role", "visual_form", "layout_family"):
            if not str(slide.get(key, "")).strip():
                diagnostics.append(Diagnostic("error", "PLAN_REQUIRED", f"'{key}' is required", f"{loc}.{key}"))
        title = str(slide.get("title", "")).strip()
        titles.append(title)
        layouts.append(str(slide.get("layout_family", "")))
        visual_forms.append(str(slide.get("visual_form", "")))
        topology = str(slide.get("topology", "")).strip()
        layout_id = str(slide.get("layout_id", "")).strip()
        tone = str(slide.get("tone", "")).strip()
        topologies.append(topology)
        tones.append(tone)
        if re.search(r"\b(card|cards|grid|tiles)\b", f"{layout_id} {slide.get('visual_form', '')}", re.I):
            card_grid_count += 1

        if isinstance(layout_manifest, dict):
            if not topology:
                diagnostics.append(Diagnostic("error", "PLAN_TOPOLOGY", "topology is required when a layout manifest is used", f"{loc}.topology"))
            elif topology not in known_topologies:
                diagnostics.append(Diagnostic("error", "PLAN_UNKNOWN_TOPOLOGY", f"Unknown topology {topology!r}", f"{loc}.topology"))
            if not layout_id:
                diagnostics.append(Diagnostic("error", "PLAN_LAYOUT_ID", "layout_id is required when a layout manifest is used", f"{loc}.layout_id"))
            elif layout_id in known_layouts:
                layout = known_layouts[layout_id]
                if topology and layout.get("topology") != topology:
                    diagnostics.append(Diagnostic("error", "PLAN_LAYOUT_TOPOLOGY", f"Layout {layout_id} uses topology {layout.get('topology')!r}, not {topology!r}", f"{loc}.topology"))
                if role and role not in layout.get("roles", []):
                    diagnostics.append(Diagnostic("error", "PLAN_LAYOUT_ROLE", f"Layout {layout_id} does not support role {role!r}", f"{loc}.layout_id"))
                if density and density not in layout.get("density", []):
                    diagnostics.append(Diagnostic("error", "PLAN_LAYOUT_DENSITY", f"Layout {layout_id} does not support density {density!r}", f"{loc}.density"))
                if tone and tone not in layout.get("tones", []):
                    diagnostics.append(Diagnostic("error", "PLAN_LAYOUT_TONE", f"Layout {layout_id} does not support tone {tone!r}", f"{loc}.tone"))
                planned_assets = slide.get("asset_ids", []) if isinstance(slide.get("asset_ids"), list) else []
                media_asset_count = 0
                for planned_asset in planned_assets:
                    semantic = known_assets.get(planned_asset, {}).get("semantic", {}) if known_assets else {}
                    asset_role = semantic.get("role") if isinstance(semantic, dict) else None
                    if asset_role not in {"logo", "icon", "texture-background"}:
                        media_asset_count += 1
                if media_asset_count > int(layout.get("media_slots", 0)):
                    diagnostics.append(Diagnostic("error", "PLAN_LAYOUT_MEDIA", f"Layout {layout_id} supports {layout.get('media_slots', 0)} primary media slot(s); logo/icon furniture is excluded", f"{loc}.asset_ids"))
            elif allow_custom_layouts and layout_id.startswith("custom-"):
                if not str(slide.get("layout_rationale", "")).strip():
                    diagnostics.append(Diagnostic("error", "PLAN_CUSTOM_LAYOUT", "Custom layout requires layout_rationale", f"{loc}.layout_rationale"))
            elif layout_id:
                diagnostics.append(Diagnostic("error", "PLAN_UNKNOWN_LAYOUT", f"Unknown layout_id {layout_id!r}", f"{loc}.layout_id"))
            if not tone:
                diagnostics.append(Diagnostic("error", "PLAN_TONE", "tone is required", f"{loc}.tone"))
            if not str(slide.get("emphasis", "")).strip():
                diagnostics.append(Diagnostic("error", "PLAN_EMPHASIS", "emphasis must name the primary focal object or region", f"{loc}.emphasis"))
            budget = slide.get("slot_budget")
            if not isinstance(budget, dict):
                diagnostics.append(Diagnostic("error", "PLAN_SLOT_BUDGET", "slot_budget must be an object", f"{loc}.slot_budget"))
            else:
                for key in ("headline_lines", "body_words", "peer_items", "media"):
                    value = budget.get(key)
                    if not isinstance(value, int) or value < 0:
                        diagnostics.append(Diagnostic("error", "PLAN_SLOT_VALUE", f"slot_budget.{key} must be a non-negative integer", f"{loc}.slot_budget.{key}"))
        if PLACEHOLDERS.search(title):
            diagnostics.append(Diagnostic("error", "PLAN_PLACEHOLDER", "Title contains placeholder text", f"{loc}.title"))
        if role == "content" and TOPICAL_TITLES.match(title):
            diagnostics.append(Diagnostic("warning", "PLAN_TOPIC_TITLE", "Content title is topical rather than a takeaway claim", f"{loc}.title"))
        limit = TITLE_LIMIT.get(str(density), 20)
        if words(title) > limit:
            diagnostics.append(Diagnostic("warning", "PLAN_TITLE_LONG", f"Title has {words(title)} words; target ≤{limit} for {density} mode", f"{loc}.title"))

        evidence = slide.get("evidence_ids", [])
        source_ids = slide.get("source_ids", [])
        if not isinstance(evidence, list):
            diagnostics.append(Diagnostic("error", "PLAN_EVIDENCE_TYPE", "evidence_ids must be an array", f"{loc}.evidence_ids"))
            evidence = []
        if not isinstance(source_ids, list):
            diagnostics.append(Diagnostic("error", "PLAN_SOURCE_TYPE", "source_ids must be an array", f"{loc}.source_ids"))
            source_ids = []
        if role == "content":
            for key in ("audience_question", "claim", "transition", "speaker_notes_purpose"):
                if not str(slide.get(key, "")).strip():
                    diagnostics.append(Diagnostic("error", "PLAN_CONTENT_REQUIRED", f"Content slide requires '{key}'", f"{loc}.{key}"))
            if not evidence:
                diagnostics.append(Diagnostic("error", "PLAN_NO_EVIDENCE", "Content slide requires at least one evidence/claim ID", f"{loc}.evidence_ids"))
            claim = str(slide.get("claim", ""))
            if PLACEHOLDERS.search(claim):
                diagnostics.append(Diagnostic("error", "PLAN_CLAIM_PLACEHOLDER", "Claim contains placeholder text", f"{loc}.claim"))
        if known_claims:
            missing = sorted(set(evidence) - known_claims)
            if missing:
                diagnostics.append(Diagnostic("error", "PLAN_UNKNOWN_CLAIM", "Unknown evidence IDs: " + ", ".join(missing), f"{loc}.evidence_ids"))
        if known_sources:
            missing = sorted(set(source_ids) - known_sources)
            if missing:
                diagnostics.append(Diagnostic("error", "PLAN_UNKNOWN_SOURCE", "Unknown source IDs: " + ", ".join(missing), f"{loc}.source_ids"))

        asset_ids = slide.get("asset_ids", [])
        media_plan = slide.get("media_plan")
        if not isinstance(asset_ids, list) or not all(isinstance(item, str) for item in asset_ids):
            diagnostics.append(Diagnostic("error", "PLAN_ASSET_TYPE", "asset_ids must be an array of strings", f"{loc}.asset_ids"))
            asset_ids = []
        for asset_id in asset_ids:
            asset_usage[asset_id] += 1
        if known_assets:
            missing_assets = sorted(set(asset_ids) - set(known_assets))
            if missing_assets:
                diagnostics.append(Diagnostic("error", "PLAN_UNKNOWN_ASSET", "Unknown asset IDs: " + ", ".join(missing_assets), f"{loc}.asset_ids"))
            for asset_id in set(asset_ids) & set(known_assets):
                asset = known_assets[asset_id]
                semantic = asset.get("semantic", {}) if isinstance(asset.get("semantic"), dict) else {}
                status = semantic.get("review_status")
                if status != "reviewed":
                    diagnostics.append(Diagnostic("error", "PLAN_ASSET_UNREVIEWED", f"Used asset {asset_id} has review_status {status!r}", f"{loc}.asset_ids"))
                if semantic.get("role") in {"unclassified", "exclude"}:
                    diagnostics.append(Diagnostic("error", "PLAN_ASSET_ROLE", f"Used asset {asset_id} has unusable role {semantic.get('role')!r}", f"{loc}.asset_ids"))
                if str(semantic.get("rights", "")).strip().casefold() in {"", "unknown"}:
                    diagnostics.append(Diagnostic("error", "PLAN_ASSET_RIGHTS", f"Used asset {asset_id} has unresolved rights", f"{loc}.asset_ids"))
        if asset_ids:
            if not isinstance(media_plan, dict):
                diagnostics.append(Diagnostic("error", "PLAN_MEDIA_PLAN", "Slides with asset_ids require a media_plan object", f"{loc}.media_plan"))
            else:
                for key in ("purpose", "treatment", "placement", "crop_mode", "focal_anchor", "text_safe_region", "fallback", "alt_text"):
                    if not str(media_plan.get(key, "")).strip():
                        diagnostics.append(Diagnostic("error", "PLAN_MEDIA_FIELD", f"media_plan requires '{key}'", f"{loc}.media_plan.{key}"))
                treatments = media_plan.get("asset_treatments")
                if strict_visual and len(asset_ids) > 1 and not isinstance(treatments, list):
                    diagnostics.append(Diagnostic("error", "PLAN_MEDIA_TREATMENTS", "Strict multi-asset slides require media_plan.asset_treatments", f"{loc}.media_plan.asset_treatments"))
                treatment_records: list[dict[str, Any]] = []
                if treatments is not None:
                    if not isinstance(treatments, list) or not all(isinstance(item, dict) for item in treatments):
                        diagnostics.append(Diagnostic("error", "PLAN_MEDIA_TREATMENTS_TYPE", "asset_treatments must be an array of objects", f"{loc}.media_plan.asset_treatments"))
                    else:
                        treatment_records = treatments
                        treatment_ids = [str(item.get("asset_id", "")) for item in treatments]
                        duplicates = sorted({item for item, count in Counter(treatment_ids).items() if item and count > 1})
                        if duplicates:
                            diagnostics.append(Diagnostic("error", "PLAN_MEDIA_TREATMENTS_DUP", "Duplicate asset treatments: " + ", ".join(duplicates), f"{loc}.media_plan.asset_treatments"))
                        if strict_visual and len(asset_ids) > 1:
                            missing_treatments = sorted(set(asset_ids) - set(treatment_ids))
                            extra_treatments = sorted(set(treatment_ids) - set(asset_ids))
                            if missing_treatments:
                                diagnostics.append(Diagnostic("error", "PLAN_MEDIA_TREATMENTS_MISSING", "Missing per-asset treatments: " + ", ".join(missing_treatments), f"{loc}.media_plan.asset_treatments"))
                            if extra_treatments:
                                diagnostics.append(Diagnostic("error", "PLAN_MEDIA_TREATMENTS_EXTRA", "Treatments reference assets not used on this slide: " + ", ".join(extra_treatments), f"{loc}.media_plan.asset_treatments"))
                        for treatment_index, treatment in enumerate(treatments):
                            treatment_loc = f"{loc}.media_plan.asset_treatments[{treatment_index}]"
                            for key in ("asset_id", "treatment", "placement", "crop_mode", "focal_anchor", "text_safe_region", "fallback", "alt_text"):
                                if not str(treatment.get(key, "")).strip():
                                    diagnostics.append(Diagnostic("error", "PLAN_MEDIA_TREATMENT_FIELD", f"asset treatment requires '{key}'", f"{treatment_loc}.{key}"))
                if not treatment_records and len(asset_ids) == 1:
                    treatment_records = [{"asset_id": asset_ids[0], **media_plan}]
                for treatment_index, treatment in enumerate(treatment_records):
                    asset_id = str(treatment.get("asset_id", ""))
                    asset = known_assets.get(asset_id, {})
                    semantic = asset.get("semantic", {}) if isinstance(asset.get("semantic"), dict) else {}
                    crop_mode = str(treatment.get("crop_mode", "")).strip().casefold()
                    role = str(semantic.get("role", "")).strip().casefold()
                    crop_tolerance = str(semantic.get("crop_tolerance", "")).strip().casefold()
                    treatment_loc = f"{loc}.media_plan.asset_treatments[{treatment_index}]" if treatments is not None else f"{loc}.media_plan"
                    if role == "logo" and crop_mode not in {"contain", "none"}:
                        diagnostics.append(Diagnostic("error", "PLAN_LOGO_CROP", f"Logo {asset_id} must use contain or none crop mode", f"{treatment_loc}.crop_mode"))
                    if crop_tolerance == "none" and crop_mode not in {"contain", "none"}:
                        diagnostics.append(Diagnostic("error", "PLAN_MEDIA_CROP", f"Asset {asset_id} has crop_tolerance 'none' and cannot use {crop_mode!r}", f"{treatment_loc}.crop_mode"))
        elif media_plan is not None:
            diagnostics.append(Diagnostic("warning", "PLAN_MEDIA_UNUSED", "media_plan exists but asset_ids is empty", f"{loc}.media_plan"))

    title_counts = Counter(title.casefold() for title in titles if title)
    for title, count in title_counts.items():
        if count > 1:
            diagnostics.append(Diagnostic("warning", "PLAN_DUP_TITLE", f"Title repeated {count} times: {title}"))

    def longest_run(items: list[str]) -> tuple[str, int]:
        best_item, best_count, current_item, current_count = "", 0, "", 0
        for item in items:
            if item and item == current_item:
                current_count += 1
            else:
                current_item, current_count = item, 1
            if current_count > best_count:
                best_item, best_count = current_item, current_count
        return best_item, best_count

    layout, layout_run = longest_run(layouts)
    if layout_run >= 4:
        diagnostics.append(Diagnostic("warning", "PLAN_LAYOUT_RUN", f"Layout family '{layout}' repeats for {layout_run} consecutive slides; verify rhythm"))
    form, form_run = longest_run(visual_forms)
    if form_run >= 4:
        diagnostics.append(Diagnostic("warning", "PLAN_VISUAL_RUN", f"Visual form '{form}' repeats for {form_run} consecutive slides"))

    topology, topology_run = longest_run(topologies)
    tone, tone_run = longest_run(tones)
    if isinstance(design_system, dict):
        severity = "error" if strict_visual else "warning"
        rhythm = design_system.get("rhythm", {}) if isinstance(design_system.get("rhythm"), dict) else {}
        min_per_ten = int(rhythm.get("min_distinct_topologies_per_10_slides", 5))
        required_topologies = min(len(slides), max(1, math.ceil(len(slides) * min_per_ten / 10)))
        actual_topologies = len({item for item in topologies if item})
        if actual_topologies < required_topologies:
            diagnostics.append(Diagnostic(severity, "PLAN_TOPOLOGY_VARIETY", f"Deck uses {actual_topologies} distinct topologies; quality floor requires {required_topologies} for {len(slides)} slides", "slides"))
        max_topology_run = int(rhythm.get("max_consecutive_same_topology", 2))
        if topology_run > max_topology_run:
            diagnostics.append(Diagnostic(severity, "PLAN_TOPOLOGY_RUN", f"Topology '{topology}' repeats {topology_run} times; floor allows {max_topology_run}", "slides"))
        max_tone_run = int(rhythm.get("max_consecutive_same_tone", 3))
        if tone_run > max_tone_run:
            diagnostics.append(Diagnostic(severity, "PLAN_TONE_RUN", f"Tone '{tone}' repeats {tone_run} times; floor allows {max_tone_run}", "slides"))
        shifts = sum(1 for left, right in zip(tones, tones[1:]) if left and right and left != right)
        min_shifts_per_ten = int(rhythm.get("min_tone_shifts_per_10_slides", 2))
        required_shifts = min(max(0, len(slides) - 1), math.ceil(len(slides) * min_shifts_per_ten / 10))
        if shifts < required_shifts:
            diagnostics.append(Diagnostic(severity, "PLAN_TONE_RHYTHM", f"Deck has {shifts} tone shift(s); floor requires {required_shifts}", "slides"))
        max_card_ratio = float(rhythm.get("max_card_grid_ratio", 0.25))
        if slides and card_grid_count / len(slides) > max_card_ratio:
            diagnostics.append(Diagnostic(severity, "PLAN_CARD_RATIO", f"Card/grid layouts occupy {card_grid_count}/{len(slides)} slides; floor allows {max_card_ratio:.0%}", "slides"))

    if not any(role == "cover" for role in roles):
        diagnostics.append(Diagnostic("warning", "PLAN_NO_COVER", "No cover slide is defined"))
    if not any(role == "closing" for role in roles):
        diagnostics.append(Diagnostic("warning", "PLAN_NO_CLOSE", "No closing slide is defined"))
    if "decision" not in phases and isinstance(brief, dict) and brief.get("primary_intent") in {"business-proposal", "sales", "investor-pitch", "strategy-decision"}:
        diagnostics.append(Diagnostic("warning", "PLAN_NO_DECISION", "Decision-oriented intent has no slide in the decision phase"))

    if isinstance(brief, dict):
        if brief.get("communication_job") and brief.get("communication_job") != plan.get("communication_job"):
            diagnostics.append(Diagnostic("error", "PLAN_JOB_MISMATCH", "communication_job differs from brief.json", "communication_job"))
        target = brief.get("delivery", {}).get("slide_count_target") if isinstance(brief.get("delivery"), dict) else None
        if isinstance(target, int) and target > 0 and abs(len(slides) - target) > max(2, round(target * 0.2)):
            diagnostics.append(Diagnostic("warning", "PLAN_COUNT", f"Plan has {len(slides)} slides versus target {target}"))

    for asset_id, count in asset_usage.items():
        if count <= 1:
            continue
        role = ""
        if asset_id in known_assets:
            semantic = known_assets[asset_id].get("semantic", {})
            if isinstance(semantic, dict):
                role = str(semantic.get("role", ""))
        if role not in {"logo", "icon", "texture-background"}:
            diagnostics.append(Diagnostic("warning", "PLAN_ASSET_REUSE", f"Asset {asset_id} is used on {count} slides; verify repetition is intentional"))

    stats = {
        "slide_count": len(slides),
        "role_counts": dict(Counter(roles)),
        "phase_counts": dict(Counter(phases)),
        "unique_layout_families": len({item for item in layouts if item}),
        "unique_visual_forms": len({item for item in visual_forms if item}),
        "used_asset_count": len(asset_usage),
        "distinct_topologies": len({item for item in topologies if item}),
        "tone_shifts": sum(1 for left, right in zip(tones, tones[1:]) if left and right and left != right),
        "card_grid_count": card_grid_count,
    }
    return diagnostics, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan")
    parser.add_argument("--brief")
    parser.add_argument("--source-ledger")
    parser.add_argument("--asset-manifest")
    parser.add_argument("--design-system")
    parser.add_argument("--layout-manifest")
    parser.add_argument("--strict-visual", action="store_true")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        plan = load_json(args.plan)
        brief = load_json(args.brief) if args.brief else None
        ledger = load_json(args.source_ledger) if args.source_ledger else None
        asset_manifest = load_json(args.asset_manifest) if args.asset_manifest else None
        design_system = load_json(args.design_system) if args.design_system else None
        layout_manifest = load_json(args.layout_manifest) if args.layout_manifest else None
    except ValueError as exc:
        return emit_report("deck plan lint", [Diagnostic("error", "PLAN_JSON", str(exc))], json_output=args.json_output)
    diagnostics, stats = validate(
        plan,
        brief,
        ledger,
        asset_manifest,
        design_system,
        layout_manifest,
        args.strict_visual,
    )
    return emit_report(
        "deck plan lint",
        diagnostics,
        json_output=args.json_output,
        extra={"file": str(Path(args.plan).resolve()), "stats": stats},
    )


if __name__ == "__main__":
    raise SystemExit(main())
