#!/usr/bin/env python3
"""Compile resolved SlidePoise decisions into one authoritative image-generation handoff.

This script does not design the slide or judge visual quality. It only prevents the
host Agent from dropping resolved content, profile rules, design constraints,
resource obligations, or canvas geometry on the first image-generation call.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from component_preview import ensure_preview

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime/src"))
from slidepoise.canvas import validate_derived_canvas
from slidepoise.artifacts import file_hash, write_json
from slidepoise.reference_retrieval import validate_host_selection
from slidepoise.resource_catalogs import selected_records


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False)


def build_style_context(config: dict[str, Any]) -> dict[str, Any]:
    """Capture resolved visual decisions without choosing or judging them."""
    profile = config.get("resolved_profile", {})
    guidance_keys = ("hard_rules", "visual_principles", "writing_principles", "reasoning_principles",
                     "anti_patterns", "asset_policy", "modes", "review_questions")
    return json.loads(json.dumps({
        "profile": {key: profile.get(key) for key in ("profile_id", "name", "purpose")},
        "style_agency": profile.get("style_agency", {}),
        "design": config.get("design", {}),
        "frame": config.get("design", {}).get("frame", {}),
        "canvas": config.get("derived", {}).get("generation_region_px"),
        "guidance": {key: profile[key] for key in guidance_keys if key in profile},
    }))


def require_object(record: dict[str, Any], key: str, *, owner: str) -> Any:
    if key not in record:
        raise SystemExit(f"{owner} is missing required field: {key}")
    return record[key]


def augment_profile_core_references(
    profile: dict[str, Any],
    resources: dict[str, Any],
    libraries: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Ensure an active profile's always-on visual precedents reach the first image call.

    This is generic profile machinery: profiles nominate reference IDs; the catalog
    supplies their canonical files. It does not choose slide-specific references.
    """
    result = json.loads(json.dumps(resources))
    if "reference_retrieval" in result:
        try:
            validate_host_selection(result, (libraries or {}).get("visual_references"))
        except (OSError, ValueError) as error:
            raise SystemExit(str(error)) from error
        return result
    required = list(profile.get("always_attach_visual_references") or [])
    if not required:
        return result
    library = (libraries or {}).get("visual_references") or {}
    by_id = {}
    ambiguous = set()
    for catalog_path, catalog, record in selected_records(library):
        identifier = record["id"]
        if identifier in by_id:
            ambiguous.add(identifier)
        by_id[identifier] = (catalog_path, record)
        if record.get("resource_id"):
            by_id[record["resource_id"]] = (catalog_path, record)
    for identifier in ambiguous:
        by_id.pop(identifier, None)
    selected = list(result.get("selected_visual_references") or [])
    selected_ids = {str(item.get("id")) for item in selected}
    for ref_id in required:
        ref_id = str(ref_id)
        if ref_id in selected_ids:
            continue
        if ref_id not in by_id:
            if "sources" in library:
                continue  # Explicit resource deselection overrides an older profile priority.
            raise SystemExit(f"Profile requires missing visual reference catalog id: {ref_id}")
        catalog_path, record = by_id[ref_id]
        canonical = catalog_path.parent / str(record.get("path") or record["id"])
        if not canonical.is_file():
            raise SystemExit(f"Profile visual reference file is missing: {canonical}")
        selected.append({
            "id": record["id"],
            **({"resource_id": record["resource_id"]} if record.get("resource_id") else {}),
            "canonical_file": str(canonical.resolve()),
            "reason": f"Always-on visual precedent required by profile {profile.get('profile_id')}: {record.get('description', '')}",
            "source": "profile_core_reference",
        })
        selected_ids.add(ref_id)
    result["selected_visual_references"] = selected
    return result




def augment_selected_components(
    resources: dict[str, Any],
    profile_id: str | None = None,
    libraries: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve host-Agent-selected component IDs to packaged previews and native donor metadata.

    Components are optional design grammar. This function never chooses a component; it only
    resolves IDs the host Agent already selected so the image-generation handoff cannot lose
    the preview/native-source relationship.
    """
    result = json.loads(json.dumps(resources))
    requested = list(result.get("selected_components") or [])
    if not requested:
        result["selected_components"] = []
        return result
    component_library = (libraries or {}).get("components") or {}
    by_id, origins, ambiguous = {}, {}, set()
    for catalog_path, catalog, raw in selected_records(component_library):
        record = dict(raw)
        if not record.get("path") and catalog.get("native_source"):
            record["path"] = catalog["native_source"]
        identifier = record["id"]
        if identifier in by_id:
            ambiguous.add(identifier)
        by_id[identifier], origins[identifier] = record, catalog_path
        if record.get("resource_id"):
            qualified = record["resource_id"]
            by_id[qualified], origins[qualified] = record, catalog_path
    for identifier in ambiguous:
        by_id.pop(identifier, None)
        origins.pop(identifier, None)
    resolved: list[dict[str, Any]] = []
    for item in requested:
        component_id = str(item.get("resource_id") or item.get("component_id") or item.get("id") or "")
        if not component_id:
            raise SystemExit("Every selected component requires component_id or id")
        record = by_id.get(component_id)
        if record is None:
            raise SystemExit(f"Selected component is not in the packaged component catalog: {component_id}")
        catalog_path = origins[component_id]
        donor_value = str(record.get("path") or "").strip()
        preview_value = str(record.get("preview_path") or "").strip()
        # Older imported records only stored their source path.
        if donor_value.lower().endswith(".pptx") and not preview_value:
            preview_value = str(Path(donor_value).with_suffix(f".slide-{int(record.get('native_source_slide_number', 1))}.preview.png"))
        donor = catalog_path.parent / donor_value if donor_value else None
        preview = catalog_path.parent / preview_value if preview_value else None
        if donor and preview and donor.is_file():
            try:
                ensure_preview(donor, preview, int(record.get("native_source_slide_number", 1)))
            except ValueError as error:
                raise SystemExit(str(error)) from error
        if donor and not preview:
            raise SystemExit(f"Selected component {component_id} must provide both native donor and preview, or neither for grammar-only guidance")
        if donor is not None and not donor.is_file():
            raise SystemExit(f"Selected component native donor is missing: {donor}")
        if preview is not None and not preview.is_file():
            raise SystemExit(f"Selected component preview is missing: {preview}")
        reason = str(item.get("reason") or "").strip()
        if not reason:
            raise SystemExit(f"Selected component {component_id} requires a reason-for-selection")
        merged = json.loads(json.dumps(record))
        merged.update({
            "component_id": component_id,
            "reason": reason,
            "source": "selected_shared_component_set",
        })
        if donor is not None and preview is not None:
            merged["canonical_file"] = str(donor.resolve())
            merged["preview_file"] = str(preview.resolve())
            merged["native_source_slide_number"] = int(record.get("native_source_slide_number", 1))
            merged["native_source_binding"] = {"source_sha256": file_hash(donor), "preview_sha256": file_hash(preview),
                                               "slide_number": merged["native_source_slide_number"]}
            merged["resource_form"] = "native_component" if donor.suffix.lower() == ".pptx" else "visual_precedent"
        elif preview is not None:
            merged["preview_file"] = str(preview.resolve())
            merged["resource_form"] = "visual_precedent"
        else:
            merged["resource_form"] = "grammar_only"
        resolved.append(merged)
    result["selected_components"] = resolved
    return result



def asset_vocabulary_policy(profile: dict[str, Any]) -> dict[str, Any]:
    return dict((profile.get("hard_rules") or {}).get("asset_vocabulary") or {})


def generation_asset_descriptions(profile: dict[str, Any], resources: dict[str, Any]) -> list[dict[str, Any]]:
    policy = asset_vocabulary_policy(profile)
    closed = str(policy.get("mode") or "open").lower() == "closed"
    result: list[dict[str, Any]] = []
    for index, item in enumerate(resources.get("selected_assets") or [], start=1):
        description = str(item.get("generation_description") or item.get("description") or "").strip()
        if closed and not description:
            raise SystemExit(f"Closed asset vocabulary requires generation_description for selected asset {item.get('asset_id')}")
        result.append({
            "asset_id": item.get("asset_id"),
            "contact_sheet_label": f"A{index:02d}",
            "role": item.get("role", "selected asset"),
            "generation_description": description or str(item.get("role") or item.get("asset_id")),
            "intrinsic_aspect_ratio": item.get("intrinsic_aspect_ratio"),
            "require_exact_identity": bool(item.get("require_exact_identity") or item.get("user_required")),
            "required_for_slide": _asset_is_required(item),
            "user_required": bool(item.get("user_required")),
        })
    return result


def _asset_is_required(item: dict[str, Any]) -> bool:
    return bool(item.get("user_required") or item.get("required_for_slide"))


def enforce_resource_budgets(config: dict[str, Any], resources: dict[str, Any]) -> None:
    policy = config.get("library_policy", {}) or {}
    max_refs = int(policy.get("maximum_visual_references_per_generation", 3))
    references = list(resources.get("selected_visual_references") or [])
    if len(references) > max_refs:
        raise SystemExit(f"Selected visual references exceed configured maximum: {len(references)} > {max_refs}")

    max_optional_assets = int(policy.get("maximum_optional_assets_per_generation", 12))
    optional_assets = [item for item in (resources.get("selected_assets") or []) if not _asset_is_required(item)]
    if len(optional_assets) > max_optional_assets:
        raise SystemExit(
            f"Optional selected assets exceed configured maximum: {len(optional_assets)} > {max_optional_assets}. "
            "Narrow retrieval to the most useful assets; user-required assets are exempt."
        )


def validate_resources(intent: dict[str, Any], resources: dict[str, Any]) -> None:
    selected_assets = list(resources.get("selected_assets") or [])
    asset_by_id = {str(item.get("asset_id")): item for item in selected_assets if item.get("asset_id")}
    for item in selected_assets:
        if not item.get("asset_id"):
            raise SystemExit("Every selected asset requires asset_id")
        if not item.get("canonical_file"):
            raise SystemExit(f"Selected asset {item['asset_id']} requires canonical_file")

    for reference in resources.get("selected_visual_references") or []:
        if not reference.get("id") or not reference.get("canonical_file"):
            raise SystemExit("Every selected visual reference requires id and canonical_file")
        if not str(reference.get("reason") or "").strip():
            raise SystemExit(f"Visual reference {reference.get('id')} requires a reason-for-attachment")
        if "full_resolution_attachment" in reference and not isinstance(reference["full_resolution_attachment"], bool):
            raise SystemExit(f"Visual reference {reference['id']} full_resolution_attachment must be boolean")

    for obligation in intent.get("user_required_assets") or []:
        asset_id = str(obligation.get("asset_id") or "")
        if not asset_id:
            raise SystemExit("Every user_required_assets record requires asset_id")
        if obligation.get("require_exact_identity") and asset_id not in asset_by_id:
            raise SystemExit(f"Exact required asset is missing from resource selection: {asset_id}")


def build_contract(config: dict[str, Any], intent: dict[str, Any], resources: dict[str, Any], deck_design: dict | None = None) -> dict[str, Any]:
    design = require_object(config, "design", owner="resolved config")
    derived = require_object(config, "derived", owner="resolved config")
    generation = require_object(config, "generation", owner="resolved config")
    profile = require_object(config, "resolved_profile", owner="resolved config")
    title = require_object(design, "title", owner="resolved design")
    style = require_object(design, "style", owner="resolved design")
    if resources.get("style_context") is not None and resources["style_context"] != build_style_context(config):
        raise SystemExit("Style changed since the context sheet was prepared. Rebuild it before generation so the current style and assets remain bound.")

    for key in (
        "audience_question",
        "dominant_message",
        "required_content",
        "semantic_relationships",
        "hierarchy",
        "visual_obligations",
        "explicit_user_visual_requirements",
    ):
        require_object(intent, key, owner="slide intent")

    resources = augment_profile_core_references(profile, resources, config.get("libraries"))
    resources = augment_selected_components(resources, str(profile.get("profile_id") or ""), config.get("libraries"))
    enforce_resource_budgets(config, resources)
    validate_resources(intent, resources)
    asset_policy = asset_vocabulary_policy(profile)
    asset_descriptions = generation_asset_descriptions(profile, resources)

    try:
        resolved_canvas = validate_derived_canvas(config, required=True)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    canvas = resolved_canvas["generation_region_px"]

    contract = {
        "schema_version": "1.4.0",
        "purpose": "authoritative_first_image_generation_handoff",
        "generation_model_default": generation.get("default_model"),
        "host_generation_adapter": generation.get("host_adapter", {}),
        "generation_budget": {
            "initial_candidates_per_slide": int(generation.get("initial_candidates_per_slide", 1)),
            "revision_guidance": generation.get("revision_guidance"),
        },
        "canvas": {
            "dimensions_px": canvas,
            "aspect_ratio": derived.get("generation_aspect_ratio"),
            "full_slide_offset_y_px": derived.get("generation_offset_y_px"),
            "master_frame_excluded": True,
            "forbidden_frame_content": ["header", "footer", "page number", "master-frame rules or decorations"],
        },
        "communication_intent": json.loads(json.dumps(intent)),
        "user_language": {
            "preserve_user_language_and_wording": True,
            "reader_first": True,
            "new_copy_em_dash": "avoid",
            "new_copy_semicolon": "avoid",
            "new_copy_colon": "use_only_when_materially_clearer",
            "avoid_stock_assistant_phrasing": True,
            "avoid_meta_interface_explanations": True,
            "profile_may_extend_voice": True,
        },
        "non_negotiable_design": {
            "title": title,
            "style": style,
            "text_style_policies": design.get("text_reconstruction", {}).get("text_style_policies", {}),
            "semantic_style_tokens": design.get("semantic_style_tokens", {}),
            "data_visualization": design.get("data_visualization", {}),
            "explicit_user_visual_requirements": intent["explicit_user_visual_requirements"],
            "icon_slot_rule": (
                "For every icon, reserve a visually unambiguous bounded slot that protects its room from surrounding content. "
                "The icon may have no designed surface or may sit on a profile-approved background surface. When there is no designed surface, "
                "a subtle generation-only boundary may mark the slot for localization; that boundary is scaffolding, not a decorative container and is not reconstructed downstream. When the icon sits on a larger colored panel/card and no distinct icon tile is intended, the downstream reconstruction should keep the icon background transparent rather than turning the scaffold into a white box."
            ),
        },
        "profile": {
            "profile_id": profile.get("profile_id"),
            "name": profile.get("name"),
            "purpose": profile.get("purpose"),
            "style_agency": profile.get("style_agency", {}),
            "hard_rules": profile.get("hard_rules", {}),
            "reasoning_principles": profile.get("reasoning_principles", []),
            "visual_principles": profile.get("visual_principles", []),
            "writing_principles": profile.get("writing_principles", []),
            "review_questions": profile.get("review_questions", []),
            "anti_patterns": profile.get("anti_patterns", []),
            "visual_reference_priorities": profile.get("visual_reference_priorities", {}),
            "density_profile": derived.get("density_profile"),
            "density_guidance": derived.get("density_guidance", {}),
            "resolution_precedence": derived.get("resolution_precedence", []),
        },
        "resources": {
            "style_context": resources.get("style_context"),
            "style_direction": resources.get("style_direction", {}),
            "selection_reasoning": resources.get("selection_reasoning", {}),
            "selected_visual_references": resources.get("selected_visual_references", []),
            "selected_assets": resources.get("selected_assets", []),
            "generation_asset_descriptions": asset_descriptions,
            "generation_context_sheet": resources.get("generation_context_sheet"),
            "asset_vocabulary_policy": asset_policy,
            "selected_components": resources.get("selected_components", []),
        },
        "composition_freedom": [
            "Choose the visual composition, grouping structure, exact object placement, connector arrangement, and emphasis system that best communicates the semantic intent.",
            "Do not force a fixed template, grid, card count, chart archetype, component precedent, or one icon treatment when another composition better supports the slide.",
            "Preserve compositional freedom without relaxing resolved design values, profile hard rules, content, asset, or canvas constraints.",
            "Density is a separate user/session control. Apply the selected density inside the profile rather than equating the profile with sparse or dense composition.",
        ],
    }
    if deck_design is not None:
        contract["deck_design"] = deck_design
    return contract


def generation_resource_projection(resources: dict[str, Any]) -> dict[str, Any]:
    """Project selected artwork and its use, keeping selection deliberation with the host."""
    references = [
        {key: item.get(key) for key in ("id", "reason") if item.get(key) is not None}
        for item in resources.get("selected_visual_references", [])
    ]
    components = []
    for item in resources.get("selected_components", []):
        components.append({
            key: value for key, value in item.items()
            if key not in {"canonical_file", "preview_file", "generation_preview", "source", "native_source_slide_number"}
        })
    return {
        "style_direction": resources.get("style_direction", {}),
        "selected_visual_references": references,
        "generation_asset_descriptions": resources.get("generation_asset_descriptions", []),
        "selected_components": components,
    }


def build_brief(contract: dict[str, Any]) -> str:
    """Project visual instructions once, without host workflow or evidence bookkeeping.

    The full contract remains the source record. Compact JSON preserves exact values
    and complete authored content, including fields unknown to this compiler.
    """
    payload = {key: contract[key] for key in (
        "canvas", "communication_intent", "user_language", "composition_freedom",
    )}
    # These requirements already occur verbatim in the complete communication intent.
    duplicated_design_fields = {"explicit_user_visual_requirements"}
    payload["non_negotiable_design"] = {
        key: value for key, value in contract["non_negotiable_design"].items()
        if key not in duplicated_design_fields
    }
    # Agent reasoning, reference selection and review belong in the host's contract.
    host_profile_fields = {
        "reasoning_principles", "review_questions", "visual_reference_priorities", "resolution_precedence",
        "purpose",
    }
    payload["profile"] = {key: value for key, value in contract["profile"].items() if key not in host_profile_fields}
    # The style-context fingerprint duplicates the resolved design and profile below.
    payload["resources"] = generation_resource_projection(contract["resources"])
    if contract.get("deck_design"):
        payload["deck_design"] = contract["deck_design"]["content"]
    instructions = [
        "# SlidePoise image-generation brief",
        "Create one substantive slide image at the canvas dimensions and aspect ratio. "
        "Exclude the Slide Master frame. Do not draw headers, footers, page numbers or master-frame decoration.",
        "Preserve the complete communication intent, facts, qualifications, exact wording, negatives and asset obligations. "
        "Use optional context selectively. Content arrays do not imply a numbered process. Session and explicit user requirements take precedence.",
        "Make the recorded information relationships legible. Keep quantities associated with what they measure and preserve their comparison basis. "
        "Arrows, enclosures, status marks and colour must express only relationships and certainty supported by the intent. "
        "Give content roles distinct emphasis, keep necessary qualifications readable and use the recorded reading context to guide explanatory depth. "
        "Choose the visual form freely unless the user specifies it. Do not invent evidence or repeat a claim merely to fill another text role.",
        "Apply profile hard rules and shared deck roles. For style agency, specified values are exact, guided values preserve character, "
        "and agent_decides or agent_decides_from_references values are fallbacks. Choose composition within these constraints.",
        "USER-FACING LANGUAGE. Preserve user-authored wording. Do not use an em dash in newly authored copy. "
        "Use direct reader-facing language with the recorded writing rules.",
        "Attachments provide the recorded visual vocabulary. Context-sheet arrangement and sample text/data are not slide content. "
        "Adapt useful component grammar to the current information. Use references for style unless factual reuse is explicitly authorized. "
        "Include assets required by the intent or marked required_for_slide. Other supplied assets are candidates to use where they help the content. "
        "When using an asset, preserve its identity and intrinsic proportions. Canonical files are restored in reconstruction. "
        "An empty asset selection does not itself prohibit visual explanation. Respect explicit exclusions and the profile's asset policy. "
        "When that policy closes the asset vocabulary, use only selected identities and profile-authorized novel illustrations. Native presentation geometry remains available.",
        "The following JSON contains each visual decision once.",
        "```json",
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        "```",
        "",
    ]
    return "\n\n".join(instructions)


def validate_prompt_capacity(prompt: str, maximum: int | None) -> None:
    if maximum is None:
        return
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 1:
        raise SystemExit("The host prompt character limit must be a positive integer")
    if len(prompt) > maximum:
        raise SystemExit(
            f"Compiled generation prompt exceeds the host character limit. {len(prompt)} > {maximum}. "
            "No content was truncated. Revise the upstream content or design inputs, or use a host with a larger prompt capacity."
        )


def file_binding(path: Path) -> dict:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"Generation input file is missing. {path}")
    return {"path": str(path), "sha256": file_hash(path)}


def load_deck_design(path: Path) -> dict:
    content = load(path)
    allowed = {"schema_version", "design_id", "purpose", "frame_source", "repeated_roles", "allowed_variations",
               "reference_images", "cross_slide_review_focus"}
    if set(content) - allowed:
        raise SystemExit("Unsupported deck-design fields. Frame values belong in the resolved configuration.")
    if content.get("schema_version") != "1.0" or not isinstance(content.get("design_id"), str) or not content["design_id"].strip():
        raise SystemExit("Deck design requires schema_version 1.0 and a non-empty design_id")
    roles = content.get("repeated_roles")
    if not isinstance(roles, dict) or not roles or any(not isinstance(value, dict) for value in roles.values()):
        raise SystemExit("Deck design repeated_roles must map role names to authored objects")
    for field in ("allowed_variations", "cross_slide_review_focus"):
        if not isinstance(content.get(field), list) or any(not isinstance(value, str) for value in content[field]):
            raise SystemExit(f"Deck design {field} must be an array of authored descriptions")
    for field in ("purpose", "frame_source"):
        if field in content and not isinstance(content[field], str):
            raise SystemExit(f"Deck design {field} must be a string")
    references = content.get("reference_images", [])
    if not isinstance(references, list):
        raise SystemExit("Deck design reference_images must be an array")
    bound_references = []
    ids = set()
    for item in references:
        if not isinstance(item, dict) or any(not isinstance(item.get(key), str) or not item[key].strip() for key in ("id", "path", "purpose")):
            raise SystemExit("Each deck reference requires id, path and purpose strings")
        if item["id"] in ids:
            raise SystemExit(f"Duplicate deck reference id. {item['id']}")
        ids.add(item["id"])
        source = Path(item["path"]).expanduser()
        bound_references.append({"id": item["id"], "purpose": item["purpose"],
                                 **file_binding(source if source.is_absolute() else path.parent / source)})
    return {**file_binding(path), "content": content, "reference_images": bound_references}


def generation_reference_images(contract: dict) -> list[dict]:
    resources = contract["resources"]
    references = []
    sheet = resources.get("generation_context_sheet") or {}
    if sheet.get("path"):
        references.append({"id": "generation-context", "purpose": "Combined style and selected assets", **file_binding(Path(sheet["path"]))})
    representation = (resources.get("asset_vocabulary_policy") or {}).get("generation_representation")
    for field, path_key, identity in (("selected_visual_references", "canonical_file", "id"),
                                      ("selected_components", "preview_file", "component_id"),
                                      ("selected_assets", "canonical_file", "asset_id")):
        for item in resources.get(field, []):
            if field == "selected_components" and item.get("resource_form") == "grammar_only":
                continue
            source = Path(item[path_key])
            attachment = file_binding(source)
            if source.suffix.lower() == ".svg":
                preview = item.get("generation_preview") or {}
                if not preview.get("path") or preview.get("format") != "png":
                    raise SystemExit(f"SVG attachment needs a prepared PNG preview. Run prepare_resource_context.py again. {source}")
                if preview.get("source") != attachment:
                    raise SystemExit(f"SVG preview source changed. Run prepare_resource_context.py again. {source}")
                preview_binding = file_binding(Path(preview["path"]))
                if preview_binding["sha256"] != preview.get("sha256"):
                    raise SystemExit(f"SVG preview changed. Run prepare_resource_context.py again. {preview['path']}")
                attachment = {**preview_binding, "source": attachment}
            if representation == "full_context_sheet" and not (
                    field == "selected_visual_references" and item.get("full_resolution_attachment") is True):
                continue
            references.append({"id": item.get(identity), "purpose": item.get("reason") or item.get("role") or field,
                               **attachment})
    references.extend((contract.get("deck_design") or {}).get("reference_images", []))
    unique = {}
    for item in references:
        unique.setdefault(item["path"], item)
    return list(unique.values())


def build_request(contract: dict, *, inputs: dict[str, Path], max_prompt_chars: int | None = None) -> dict:
    prompt = build_brief(contract)
    validate_prompt_capacity(prompt, max_prompt_chars)
    return {"schema_version": "1.0", "purpose": "host_image_generation_request", "prompt": prompt,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "prompt_character_count": len(prompt), "host_constraints": {"max_prompt_chars": max_prompt_chars},
            "preferred_model": contract["generation_model_default"], "canvas": contract["canvas"],
            "reference_images": generation_reference_images(contract),
            "input_bindings": {name: file_binding(path) for name, path in inputs.items()}}


def verify_request(path: Path) -> dict:
    request = load(path)
    if request.get("schema_version") != "1.0" or request.get("purpose") != "host_image_generation_request":
        raise SystemExit("Unsupported generation request")
    bindings = request.get("input_bindings", {})
    if not {"config", "intent", "resources", "contract", "brief"}.issubset(bindings):
        raise SystemExit("Generation request is missing source bindings")
    for name, record in bindings.items():
        if file_binding(Path(record["path"])) != record:
            raise SystemExit(f"Generation request input changed. Recompile the request. {name}")
    contract = load(Path(bindings["contract"]["path"]))
    deck = load_deck_design(Path(bindings["deck_design"]["path"])) if "deck_design" in bindings else None
    rebuilt = build_contract(load(Path(bindings["config"]["path"])), load(Path(bindings["intent"]["path"])),
                             load(Path(bindings["resources"]["path"])), deck)
    if rebuilt != contract:
        raise SystemExit("Generation contract differs from its source inputs. Recompile the request.")
    expected = build_request(contract, inputs={name: Path(record["path"]) for name, record in bindings.items()},
                             max_prompt_chars=(request.get("host_constraints") or {}).get("max_prompt_chars"))
    if request != expected or Path(bindings["brief"]["path"]).read_text(encoding="utf-8") != expected["prompt"]:
        raise SystemExit("Generation request differs from the compiled brief or attachments. Recompile the request.")
    return request


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    parser.add_argument("--intent", type=Path)
    parser.add_argument("--resources", type=Path)
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--brief", type=Path)
    parser.add_argument("--deck-design", type=Path)
    parser.add_argument("--request", type=Path, help="Defaults to generation-request.json beside the contract")
    parser.add_argument("--max-prompt-chars", type=int, help="Optional host character capacity. Oversized prompts fail without truncation.")
    parser.add_argument("--verify-request", type=Path, help="Verify freshness and emit the exact request for a host adapter")
    parser.add_argument("--approvals", type=Path, help="Optional legacy decision history. It does not gate generation.")
    args = parser.parse_args()
    if args.verify_request:
        if any(getattr(args, key) is not None for key in ("config", "intent", "resources", "contract", "brief", "deck_design", "request", "max_prompt_chars")):
            parser.error("--verify-request does not accept generation input or output options")
        print(dump_json(verify_request(args.verify_request)))
        return
    if any(getattr(args, key) is None for key in ("config", "intent", "resources", "contract", "brief")):
        parser.error("Generation requires --config, --intent, --resources, --contract and --brief")
    config = load(args.config)
    intent = load(args.intent)
    resources = load(args.resources)
    if not resources.get("style_context"):
        raise SystemExit("This resource sheet predates combined style and asset context. Run prepare_resource_context.py before generating.")
    deck_design = load_deck_design(args.deck_design) if args.deck_design else None
    contract = build_contract(config, intent, resources, deck_design)
    asset_policy = contract.get("resources", {}).get("asset_vocabulary_policy", {}) or {}
    representation = str(asset_policy.get("generation_representation") or "").lower()
    if representation == "full_context_sheet":
        context_sheet = contract.get("resources", {}).get("generation_context_sheet") or {}
        context_path = Path(str(context_sheet.get("path") or ""))
        if not context_path.is_file():
            raise SystemExit("Generation context sheet is missing. Run prepare_resource_context.py first.")
    brief = build_brief(contract)
    configured_maximum = ((config.get("generation") or {}).get("host_adapter") or {}).get("max_prompt_chars")
    limits = [value for value in (args.max_prompt_chars, configured_maximum) if value is not None]
    maximum_prompt_chars = min(limits) if limits else None
    validate_prompt_capacity(brief, maximum_prompt_chars)
    request_path = args.request or args.contract.with_name("generation-request.json")
    inputs = {name: getattr(args, name) for name in ("config", "intent", "resources")}
    if args.deck_design:
        inputs["deck_design"] = args.deck_design
    destinations = [path.resolve() for path in (args.contract, args.brief, request_path)]
    if len(set(destinations)) != 3 or set(destinations).intersection(path.resolve() for path in inputs.values()):
        raise SystemExit("Generation outputs must be distinct from each other and from their source inputs")
    generation_reference_images(contract)

    args.contract.parent.mkdir(parents=True, exist_ok=True)
    args.brief.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.contract, contract)
    args.brief.write_text(brief, encoding="utf-8")
    write_json(request_path, build_request(contract, inputs={**inputs, "contract": args.contract, "brief": args.brief},
                                           max_prompt_chars=maximum_prompt_chars))
    print(json.dumps({
        "contract": str(args.contract.resolve()),
        "brief": str(args.brief.resolve()),
        "request": str(request_path.resolve()),
        "profile": contract["profile"]["profile_id"],
        "visual_references": len(contract["resources"]["selected_visual_references"]),
        "assets": len(contract["resources"]["selected_assets"]),
        "components": len(contract["resources"].get("selected_components", [])),
        "canvas": contract["canvas"]["dimensions_px"],
        "prompt_character_count": len(brief),
    }, indent=2))


if __name__ == "__main__":
    main()
