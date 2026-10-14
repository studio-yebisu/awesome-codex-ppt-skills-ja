#!/usr/bin/env python3
"""Collect objective release facts for one SlidePoise page reconstruction.

Visual acceptance is never produced here. The script only verifies that required
host-Agent visual-review records exist and that deterministic artifacts are mutually
consistent and structurally valid.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from raster_decisions import illustration_decision_errors


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def content_hash(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def accepted_review(path: Path, stage: str, required_artifacts: tuple[Path, ...] = ()) -> tuple[bool, str | None]:
    record = load(path)
    if record.get("reviewer") != "host_agent_visual_reasoning":
        return False, "visual review is not attributed to host_agent_visual_reasoning"
    if record.get("stage") != stage:
        return False, f"visual review stage must be {stage!r}"
    if record.get("decision") != "accepted":
        return False, f"visual review decision is {record.get('decision')!r}"
    if record.get("material_issues"):
        return False, "visual review still contains material issues"
    observations = record.get("observations", [])
    if not isinstance(observations, list) or not observations or not all(isinstance(item, str) and item.strip() for item in observations):
        return False, "visual review needs concrete host-authored observations"
    bindings = {}
    for item in record.get("reviewed_artifacts", []):
        if not isinstance(item, dict) or not item.get("path"):
            return False, "reviewed_artifacts must bind paths to SHA-256 hashes"
        artifact = Path(item["path"])
        if not artifact.is_absolute():
            artifact = path.parent / artifact
        artifact = artifact.resolve()
        if not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest() != item.get("sha256"):
            return False, f"review artifact missing or changed since inspection: {artifact}"
        bindings[artifact] = item
    for artifact in required_artifacts:
        if artifact.resolve() not in bindings:
            return False, f"visual review does not bind current artifact: {artifact}"
    return True, None


def render_binding_checks(pptx: Path, render: Path, slide_number: int) -> list[dict]:
    """Verify render provenance independently of the host's review record."""
    sidecar = render.with_suffix(".source.json")
    if not sidecar.is_file():
        return [{"reason": "render_source_binding_missing", "path": str(sidecar)}]
    try:
        binding = load(sidecar)
        if not isinstance(binding, dict):
            raise ValueError("Render source binding must be an object")
        errors = []
        for key, expected in (("source_sha256", hashlib.sha256(pptx.read_bytes()).hexdigest()),
                              ("render_sha256", hashlib.sha256(render.read_bytes()).hexdigest()),
                              ("slide_number", slide_number)):
            if binding.get(key) != expected:
                errors.append({"reason": "render_source_binding_mismatch", "field": key})
        text = binding.get("rendered_text")
        if text is not None:
            if not isinstance(text, dict) or not isinstance(text.get("path"), str) or not text["path"]:
                raise ValueError("Rendered-text binding must name its evidence file")
            path = sidecar.parent / text["path"]
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != text.get("sha256"):
                errors.append({"reason": "rendered_text_evidence_missing_or_changed"})
        return errors
    except (OSError, ValueError, TypeError, KeyError) as error:
        return [{"reason": "render_source_binding_invalid", "detail": str(error)}]




def pptx_frame_checks(pptx_path: Path, config: dict) -> list[dict]:
    errors: list[dict] = []
    frame = config["design"]["frame"]
    with zipfile.ZipFile(pptx_path) as archive:
        names = set(archive.namelist())
        if "ppt/slides/slide1.xml" not in names:
            return [{"reason": "pptx_missing_slide1"}]
        slide_xml = archive.read("ppt/slides/slide1.xml").decode("utf-8", errors="ignore")
        master_names = sorted(name for name in names if name.startswith("ppt/slideMasters/slideMaster") and name.endswith(".xml"))
        layout_names = sorted(name for name in names if name.startswith("ppt/slideLayouts/slideLayout") and name.endswith(".xml"))
        if (frame["header"].get("enabled") or frame["footer"].get("enabled")) and not (master_names and layout_names):
            errors.append({"reason": "required_slide_master_or_layout_missing"})
            return errors
        inherited_xml = "\n".join(archive.read(name).decode("utf-8", errors="ignore") for name in [*master_names, *layout_names])
        if frame["header"].get("enabled") and "SC_MASTER_HEADER_LEFT" not in inherited_xml:
            errors.append({"reason": "inherited_header_content_missing"})
        if frame["footer"].get("enabled") and "SC_MASTER_FOOTER_LEFT" not in inherited_xml:
            errors.append({"reason": "inherited_footer_content_missing"})
        if frame["footer"].get("enabled") and frame["footer"].get("slide_number", {}).get("enabled"):
            if "sldNum" not in inherited_xml:
                errors.append({"reason": "native_slide_number_field_missing_from_master_layout"})
        if "SC_MASTER_HEADER_LEFT" in slide_xml or "SC_MASTER_FOOTER_LEFT" in slide_xml:
            errors.append({"reason": "frame_was_emitted_as_per_slide_objects_instead_of_inherited_master_layout_content"})
    return errors


def typography_checks(semantic: dict, contract: dict, scene: dict) -> list[dict]:
    """Check native text peers against explicit reconstruction ownership."""
    errors: list[dict] = []
    units = {str(unit["id"]): unit for unit in contract.get("reconstruction_units", [])}
    semantic_text = []
    for entity in semantic.get("entities", []):
        if entity.get("kind") != "text":
            continue
        identity = str(entity.get("id"))
        unit = units.get(identity)
        if unit is None:
            errors.append({"entity": identity, "reason": "release_text_missing_reconstruction_unit"})
        if unit is not None and unit.get("emits_ppt_object") is False:
            continue
        semantic_text.append(entity)
    expected_typography_groups: dict[str, list[str]] = {}
    for entity in semantic_text:
        group = str(entity.get("typography_group") or "").strip()
        if not group:
            errors.append({"entity": entity.get("id"), "reason": "release_text_missing_typography_group"})
            continue
        expected_typography_groups.setdefault(group, []).append(str(entity.get("id")))


    text_fit = scene.get("compiler_report", {}).get("text_fitting", {}) or {}
    reported_groups = {str(record.get("typography_group")): record for record in text_fit.get("text_groups", []) if record.get("typography_group")}
    emitted_textboxes = {str(obj.get("id")): obj for obj in scene.get("objects", []) if obj.get("kind") == "textbox"}
    for group, member_ids in expected_typography_groups.items():
        report_group = reported_groups.get(group)
        if report_group is None:
            errors.append({"reason": "typography_group_missing_from_constructor_report", "typography_group": group, "member_ids": member_ids})
            continue
        reported_member_ids = [str(value) for value in report_group.get("member_ids", [])]
        if set(reported_member_ids) != set(member_ids):
            errors.append({
                "reason": "typography_group_membership_changed_during_reconstruction",
                "typography_group": group,
                "semantic_member_ids": sorted(member_ids),
                "reported_member_ids": sorted(reported_member_ids),
            })
        emitted_sizes = []
        emitted_members = []
        for member_id in member_ids:
            textbox = emitted_textboxes.get(member_id)
            if textbox is None:
                errors.append({"entity": member_id, "reason": "emitting_textbox_missing_from_scene"})
                continue
            value = textbox.get("style", {}).get("font_size_pt")
            if isinstance(value, (int, float)):
                emitted_sizes.append(float(value))
                emitted_members.append(member_id)
        if len(emitted_sizes) >= 2 and max(emitted_sizes) - min(emitted_sizes) > 1e-6:
            errors.append({
                "reason": "typography_group_emitted_multiple_font_sizes",
                "typography_group": group,
                "member_ids": emitted_members,
                "font_sizes_pt": emitted_sizes,
            })
        shared_size = report_group.get("shared_font_size_pt")
        if isinstance(shared_size, (int, float)):
            mismatched = [member_id for member_id in emitted_members if abs(float(emitted_textboxes[member_id].get("style", {}).get("font_size_pt")) - float(shared_size)) > 1e-6]
            if mismatched:
                errors.append({
                    "reason": "typography_group_scene_size_differs_from_constructor_report",
                    "typography_group": group,
                    "shared_font_size_pt": shared_size,
                    "member_ids": mismatched,
                })
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("config", "generated_image", "semantic_map", "measured_scene", "contract", "constructor_scene", "pptx", "generation_review", "measurement_review", "reconstruction_review", "output"):
        parser.add_argument(f"--{name.replace('_','-')}", dest=name, type=Path, required=True)
    parser.add_argument("--approvals", type=Path, help="Optional legacy decision history. It does not gate release evidence.")
    parser.add_argument("--render", type=Path, required=False, help="Persist the inspected PPTX render so review freshness can be checked at release.")
    parser.add_argument("--slide-number", type=int, default=1, help="One-based page in the supplied PowerPoint that produced the inspected render.")
    args = parser.parse_args()
    errors: list[dict] = []
    config = load(args.config)
    stage_artifacts = {
        "generation": (args.generated_image,),
        "measurement": (args.generated_image, args.semantic_map, args.measured_scene, args.measured_scene.parent / "debug_overlay.png"),
        "reconstruction": (args.generated_image, args.measured_scene, args.contract, args.constructor_scene, args.pptx) + ((args.render,) if args.render else ()),
    }
    if args.render is None:
        errors.append({"reason": "persisted_pptx_render_required_for_review_freshness"})
    for stage, path in (("generation", args.generation_review), ("measurement", args.measurement_review), ("reconstruction", args.reconstruction_review)):
        ok, reason = accepted_review(path, stage, stage_artifacts[stage])
        if not ok:
            errors.append({"reason": "visual_review_not_accepted", "stage": stage, "detail": reason})
    generation_review = load(args.generation_review)
    candidate_index = generation_review.get("candidate_index")
    if not isinstance(candidate_index, int):
        errors.append({"reason": "generation_review_missing_candidate_index"})
    elif candidate_index < 1:
        errors.append({"reason": "generation_candidate_index_must_be_positive", "candidate_index": candidate_index})

    measured = load(args.measured_scene)
    contract = load(args.contract)
    scene = load(args.constructor_scene)
    semantic = load(args.semantic_map)
    approvals = load(args.approvals) if args.approvals and args.approvals.is_file() else {}
    bindings = scene.get("compiler_report", {}).get("input_bindings", {}) or {}
    expected_bindings = {
        "measured_scene_sha256": content_hash(measured),
        "reconstruction_contract_sha256": content_hash(contract),
        "resolved_design_sha256": content_hash(config.get("design", {})),
    }
    for key, expected in expected_bindings.items():
        if bindings.get(key) != expected:
            errors.append({"reason": "constructor_scene_input_binding_mismatch", "binding": key})
    errors.extend({"reason": "illustration_decision_invalid", "detail": message} for message in illustration_decision_errors(semantic, approvals))

    errors.extend(typography_checks(semantic, contract, scene))
    if not args.generated_image.is_file() or not args.pptx.is_file():
        errors.append({"reason": "release_artifact_missing"})
    if args.render is not None and not args.render.is_file():
        errors.append({"reason": "declared_render_artifact_missing"})
    if args.render is not None and args.render.is_file() and args.pptx.is_file():
        errors.extend(render_binding_checks(args.pptx, args.render, args.slide_number))
    if not measured.get("runtime", {}).get("opencv"):
        errors.append({"reason": "OpenCV_measurement_missing"})
    local_norm = measured.get("runtime", {}).get("local_geometry_normalization", {}) or {}
    if local_norm.get("mode") != "agent_authored_only":
        errors.append({"reason": "agent_authored_geometry_correction_report_missing"})
    expected_adjustments = semantic.get("geometry_adjustments", []) or []
    actual_adjustments = local_norm.get("adjustments", []) or []
    fields = ("entity_id", "before_bbox_px", "after_bbox_px", "reviewed_by", "reason")
    if [{key: item.get(key) for key in fields} for item in actual_adjustments] != [{key: item.get(key) for key in fields} for item in expected_adjustments]:
        errors.append({"reason": "geometry_corrections_differ_from_host_decisions"})
    if "fixture://" in args.measured_scene.read_text(encoding="utf-8").lower():
        errors.append({"reason": "fixture_measurement_forbidden"})

    frame = scene.get("frame", {})
    resolved_frame = config["design"]["frame"]
    for area in ("header", "footer"):
        for key in ("enabled", "height_px", "implementation"):
            if frame.get(area, {}).get(key) != resolved_frame.get(area, {}).get(key):
                errors.append({"reason": "frame_configuration_mismatch", "area": area, "field": key})
    errors.extend(pptx_frame_checks(args.pptx, config))

    try:
        with zipfile.ZipFile(args.pptx) as archive:
            if "[Content_Types].xml" not in archive.namelist():
                errors.append({"reason": "invalid_pptx_package"})
    except zipfile.BadZipFile:
        errors.append({"reason": "invalid_pptx_package"})

    report = {
        "evidence_type": "objective_release_facts",
        "blocking_facts": errors,
        "agent_release_decision_required": True,
        "visual_acceptance_source": "host-Agent visual reasoning, optionally strengthened by independent visual reviewers",
        "mechanical_evidence_scope": "artifact freshness, config consistency, master-frame facts, package structure, typography-group consistency, and raster-decision structure. No release verdict is produced",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not errors else 2)


if __name__ == "__main__":
    main()
