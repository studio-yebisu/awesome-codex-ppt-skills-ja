#!/usr/bin/env python3
"""Collect objective framework configuration preflight facts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime/src"))
from slidepoise.canvas import validate_derived_canvas
from slidepoise.generation import resolve_preferences

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    errors: list[str] = []
    facts: list[str] = []

    if cfg.get("scope", {}).get("mode") != "adaptive_presentation":
        errors.append("scope.mode must be adaptive_presentation")
    forbidden = {"connector_registry", "google_drive", "sharepoint", "mcp"}
    for key in forbidden:
        if key in cfg:
            errors.append(f"external library dependency is not supported: {key}")
    if cfg.get("measurement", {}).get("engine") != "OpenCV":
        errors.append("measurement.engine must be OpenCV")
    segmentation = cfg.get("measurement", {}).get("segmentation", {}) or {}
    if segmentation.get("mode") not in {"auto", "never", "required"}:
        errors.append("measurement.segmentation.mode must be auto, never, or required")
    if segmentation.get("provider") != "sam2":
        errors.append("measurement.segmentation.provider must be sam2")
    if segmentation.get("device") not in {"auto", "cpu", "mps", "cuda"}:
        errors.append("measurement.segmentation.device must be auto, cpu, mps, or cuda")
    if not isinstance(segmentation.get("eligible_roles"), list) or not segmentation.get("eligible_roles"):
        errors.append("measurement.segmentation.eligible_roles must be a non-empty array")

    generation = cfg.get("generation", {})
    try:
        resolve_preferences(generation)
    except ValueError as error:
        errors.append(str(error))
    host_adapter = generation.get("host_adapter", {}) or {}
    if host_adapter.get("mode") not in {"agent_discovered_or_manual", "host_native_or_delegated_image_generation"}:
        errors.append("generation.host_adapter.mode must use Agent-discovered or manual image generation")
    if not isinstance(host_adapter.get("max_prompt_chars"), int) or host_adapter.get("max_prompt_chars") < 1:
        errors.append("generation.host_adapter.max_prompt_chars must be a positive integer")
    if generation.get("initial_candidates_per_slide") != 1:
        errors.append("generation.initial_candidates_per_slide must be 1")
    refinement = generation.get("illustration_refinement", {}) or {}
    if refinement.get("enabled_by_default") is not True:
        errors.append("generation.illustration_refinement.enabled_by_default must be true")
    if not isinstance(refinement.get("ask_user_when_material_choice_or_extra_cost_is_unresolved"), bool):
        errors.append("generation.illustration_refinement ask-user policy must be boolean")
    if refinement.get("trigger_visual_source_class") != "novel_illustration":
        errors.append("generation.illustration_refinement.trigger_visual_source_class must be novel_illustration")

    design = cfg.get("design", {})
    if not str(design.get("profile") or "").strip():
        errors.append("design.profile must name a default external profile")

    try:
        validate_derived_canvas(cfg)
    except ValueError as error:
        errors.append(str(error))
    frame = design.get("frame", {})
    for area in ("header", "footer"):
        record = frame.get(area, {})
        if record.get("implementation") != "slide_master_inherited_content":
            errors.append(f"{area}.implementation must be slide_master_inherited_content")
    if frame.get("footer", {}).get("slide_number", {}).get("implementation") != "native_slide_number_field_on_master":
        errors.append("footer slide number must use native_slide_number_field_on_master")

    local_norm = cfg.get("measurement", {}).get("local_geometry_normalization", {})
    if not isinstance(local_norm.get("enabled"), bool):
        errors.append("measurement.local_geometry_normalization.enabled must be boolean")
    if local_norm.get("mode", "agent_authored_only") != "agent_authored_only":
        errors.append("local geometry corrections must use agent_authored_only mode")

    library_policy = cfg.get("library_policy", {})
    max_refs = library_policy.get("maximum_visual_references_per_generation")
    if not isinstance(max_refs, int) or max_refs < 0 or max_refs > 6:
        errors.append("library_policy.maximum_visual_references_per_generation must be an integer from 0 to 6")
    max_assets = library_policy.get("maximum_optional_assets_per_generation")
    if not isinstance(max_assets, int) or max_assets < 1 or max_assets > 24:
        errors.append("library_policy.maximum_optional_assets_per_generation must be an integer from 1 to 24")

    deprecated_generation_keys = {
        "attach_selected_visual_references", "attach_exact_user_assets", "render_selected_icons_in_candidate",
        "candidate_review_required", "generated_canvas_excludes_master_frame",
    }
    for key in sorted(deprecated_generation_keys):
        if key in generation:
            errors.append(f"deprecated no-op generation config key must be removed: generation.{key}")
    if "selection_owner" in library_policy:
        errors.append("deprecated no-op config key must be removed: library_policy.selection_owner")

    text_config = design.get("text_reconstruction", {})
    if "semantic_role_policies" in text_config:
        errors.append("text_reconstruction.semantic_role_policies is deprecated; use text_style_policies")
    policies = text_config.get("text_style_policies", {})
    if not isinstance(policies, dict) or "default" not in policies:
        errors.append("text_reconstruction.text_style_policies.default is required")

    deprecated_noop_paths = {
        "design.icon_slots.fit": design.get("icon_slots", {}).get("fit"),
        "design.icon_slots.alignment": design.get("icon_slots", {}).get("alignment"),
        "design.icon_slots.allow_stretch": design.get("icon_slots", {}).get("allow_stretch"),
        "design.icon_slots.minimum_inset_px": design.get("icon_slots", {}).get("minimum_inset_px"),
        "design.icon_slots.preserve_canonical_color_for_brand_assets": design.get("icon_slots", {}).get("preserve_canonical_color_for_brand_assets"),
        "design.text_reconstruction.maximize_peer_font_size": text_config.get("maximize_peer_font_size"),
        "design.text_reconstruction.peer_group_authority": text_config.get("peer_group_authority"),
        "design.connectors.routing.minimum_bend_spacing_px": design.get("connectors", {}).get("routing", {}).get("minimum_bend_spacing_px"),
        "design.connectors.routing.prefer_axis_aligned_segments": design.get("connectors", {}).get("routing", {}).get("prefer_axis_aligned_segments"),
        "design.connectors.routing.terminal_approach_must_be_straight": design.get("connectors", {}).get("routing", {}).get("terminal_approach_must_be_straight"),
        "design.connectors.routing.route_selection_priority": design.get("connectors", {}).get("routing", {}).get("route_selection_priority"),
        "design.connectors.routing.source_departure_axis_from_attachment_side": design.get("connectors", {}).get("routing", {}).get("source_departure_axis_from_attachment_side"),
        "design.connectors.routing.target_terminal_axis_from_attachment_side": design.get("connectors", {}).get("routing", {}).get("target_terminal_axis_from_attachment_side"),
        "design.connectors.routing.arrowhead_orientation_from_final_segment": design.get("connectors", {}).get("routing", {}).get("arrowhead_orientation_from_final_segment"),
    }
    for path, value in deprecated_noop_paths.items():
        if value is not None:
            errors.append(f"deprecated no-op config key must be removed: {path}")

    families = set(design.get("connectors", {}).get("allowed_families", []))
    if not families:
        errors.append("design.connectors.allowed_families must contain at least one framework-supported family")

    remote_sources = cfg.get("remote_sources", {})
    required_remote_sources = {"remix_icon", "wikimedia_commons", "shared_policy"}
    missing_remote_sources = sorted(required_remote_sources - set(remote_sources))
    if missing_remote_sources:
        errors.append(f"remote_sources is missing required entries: {missing_remote_sources}")
    for source_id in ("remix_icon", "wikimedia_commons"):
        source = remote_sources.get(source_id, {})
        if source.get("enabled") and not str(source.get("provider", "")).strip():
            errors.append(f"enabled remote source must name its provider: {source_id}")
        if source.get("enabled") not in {True, False}:
            errors.append(f"remote_sources.{source_id}.enabled must be boolean")

    selected_icon_sets = cfg.get("library_sets", {}).get("selected", {}).get("icons", []) or []
    records = cfg.get("library_sets", {}).get("records", {}) or {}
    for set_id in selected_icon_sets:
        record = records.get(set_id, {}) or {}
        provider = record.get("provider")
        if record.get("source") == "remote" and provider and remote_sources.get(provider, {}).get("enabled") is False:
            facts.append(f"selected remote icon Library Set is disabled for this run: {set_id} ({provider})")

    remix = remote_sources.get("remix_icon", {})
    if remix:
        if remix.get("pair_styles") != ["line", "fill"]:
            errors.append("Remix Icon external fetch must retain the line/fill pair")
        if "{version}" not in str(remix.get("repository_tree_url", "")):
            errors.append("Remix Icon repository_tree_url must contain {version}")
        raw_template = str(remix.get("raw_url_template", ""))
        if "{version}" not in raw_template or "{repository_path}" not in raw_template:
            errors.append("Remix Icon raw_url_template must contain {version} and {repository_path}")
        if remix.get("selection_stage") != "post_generation_visual_review":
            errors.append("Remix Icon variant selection must occur during post_generation_visual_review")
        if remix.get("selection_owner") != "host_agent_visual_reasoning":
            errors.append("Remix Icon variant selection must belong to host_agent_visual_reasoning")

    commons = remote_sources.get("wikimedia_commons", {})
    if commons and (commons.get("require_file_page") is not True or commons.get("require_license_metadata") is not True):
        errors.append("Wikimedia Commons retrieval must require a file page and license metadata")

    reviews = cfg.get("agent_reviews", {})
    if reviews.get("mode") not in {"disabled", "use_when_host_supports_subagents"}:
        errors.append("agent_reviews.mode must be disabled or use_when_host_supports_subagents")
    if int(reviews.get("ordinary_checkpoint_revision_rounds", -1)) != 1:
        errors.append("ordinary Agent review checkpoints must use exactly one correction round")
    if reviews.get("reviewer_write_access") is not False:
        errors.append("independent Agent reviewers must remain read-only")

    report = {
        "evidence_type": "objective_config_structure",
        "blocking_facts": errors,
        "configuration_facts": facts,
        "agent_interpretation_required": True,
        "config": str(args.config.resolve()),
        "notice": "No overall verdict is produced. The host Agent must interpret these facts together with the profile and current task."
    }
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not errors else 2)


if __name__ == "__main__":
    main()
