#!/usr/bin/env python3
"""Resolve SlidePoise base config, one external profile, and explicit session overrides.

Profiles select shared external resource catalogs. Session
design_overrides may only change keys that already exist in the resolved design.
No visual judgement is performed here.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime/src"))
from slidepoise.canvas import derive_canvas
from slidepoise.generation import resolve_preferences
from slidepoise.resource_catalogs import resolve_libraries


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


PROFILE_OWNED_MAPS = {"semantic_style_tokens"}
DENSITY_ALIASES = {
    "moderately_dense_consulting": "balanced",
    "moderately dense consulting-slide": "balanced",
    "balanced_consulting": "balanced",
    "consulting_balanced": "balanced",
    "editorial_balanced": "balanced",
    "dense_consulting": "information_rich",
    "consulting_dense": "information_rich",
    "high_consulting": "information_rich",
    "consulting_sparse": "spacious",
    "moderate": "balanced",
    "dense": "information_rich",
}


def merge_profile(
    base: dict,
    overlay: dict,
    path: tuple[str, ...] = (),
    *,
    replace_profile_owned_maps: bool = True,
) -> None:
    """Merge a profile while replacing vocabularies that belong to that profile.

    Structural configuration is inherited. Named visual token vocabularies are
    profile-owned and therefore replace the base map as one coherent set.
    """
    for key, value in overlay.items():
        current_path = (*path, key)
        if replace_profile_owned_maps and key in PROFILE_OWNED_MAPS and isinstance(value, dict):
            base[key] = copy.deepcopy(value)
            continue
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge_profile(
                base[key],
                value,
                current_path,
                replace_profile_owned_maps=replace_profile_owned_maps,
            )
        else:
            base[key] = copy.deepcopy(value)


def merge_existing(base: dict, override: dict, path: str = "design") -> None:
    """Apply temporary exact session overrides without inventing config structure."""
    if not isinstance(override, dict):
        raise SystemExit("design_overrides must be an object")
    for key, value in override.items():
        if key not in base:
            raise SystemExit(f"Unknown design override key: {path}.{key}")
        if value is None:
            continue
        if isinstance(base[key], dict):
            if not isinstance(value, dict):
                raise SystemExit(f"Design override {path}.{key} must be an object")
            merge_existing(base[key], value, f"{path}.{key}")
        else:
            base[key] = value


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve one SlidePoise session from base config, selected profile, and explicit overrides.")
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--profiles-root", type=Path)
    parser.add_argument("--session", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cfg = copy.deepcopy(load(args.base))
    session = load(args.session) if args.session and args.session.exists() else {}
    frozen_path = args.session.parent / "work/session-defaults.json" if args.session else None
    frozen = load(frozen_path) if frozen_path and frozen_path.is_file() else {}
    if frozen:
        cfg = copy.deepcopy(frozen["base_config"])
    allowed_top = {
        "slide_role", "density", "palette", "profile", "guidance_profile",
        "generation_model", "image_generation", "header", "footer", "remote_sources", "external_icon_fetch", "measurement", "design_overrides", "library_sets", "library_items",
    }
    unknown = sorted(set(session) - allowed_top)
    if unknown:
        raise SystemExit(f"Unsupported session override keys: {unknown}")

    requested_profile = session.get("profile")
    legacy_profile = session.get("guidance_profile")
    if requested_profile is not None and legacy_profile is not None and str(requested_profile) != str(legacy_profile):
        raise SystemExit("profile and legacy guidance_profile overrides disagree")
    profile_id = str(requested_profile or legacy_profile or cfg.get("design", {}).get("profile", ""))
    repository_root = Path(__file__).resolve().parents[2]
    installed_root = Path(os.environ.get("SLIDEPOISE_HOME", Path.home() / ".slidepoise")) / "profiles"
    profiles_root = Path(frozen.get("profiles_root") or args.profiles_root or (installed_root if installed_root.is_dir() else repository_root / "profiles")).expanduser().resolve()
    aliases_path = profiles_root / "aliases.json"
    aliases = load(aliases_path) if aliases_path.is_file() else {}
    requested_id = profile_id
    if not frozen and not (profiles_root / profile_id / "profile.json").is_file():
        profile_id = aliases.get(profile_id, profile_id)
    profile_path = profiles_root / profile_id / "profile.json"
    if frozen and not profile_path.is_file():
        # Keep the captured design while locating its renamed reference directory.
        profile_path = profiles_root / aliases.get(profile_id, profile_id) / "profile.json"
    if frozen and profile_id not in frozen["profiles"]:
        raise SystemExit("Profile was not captured for this session. Explicitly update session defaults first.")
    if not frozen and not profile_path.is_file():
        available = sorted(path.parent.name for path in profiles_root.glob("*/profile.json"))
        raise SystemExit(f"Unknown external profile {profile_id!r}. Available profiles: {available}")
    profile = copy.deepcopy(frozen["profiles"][profile_id]) if frozen else load(profile_path)
    if str(profile.get("profile_id")) != profile_id:
        raise SystemExit(f"Profile id mismatch: registry={profile_id!r}, file={profile.get('profile_id')!r}")
    overlay = profile.get("design_overrides", {})
    if not isinstance(overlay, dict):
        raise SystemExit("profile.design_overrides must be an object")
    merge_profile(cfg["design"], overlay)
    if requested_id != profile_id:
        merge_profile(cfg["design"], cfg.get("user_design_overrides", {}).get(requested_id, {}), replace_profile_owned_maps=False)
    merge_profile(
        cfg["design"],
        cfg.get("user_design_overrides", {}).get(profile_id, {}),
        replace_profile_owned_maps=False,
    )
    configured_density = str(cfg["design"].get("style", {}).get("density", "balanced"))
    cfg["design"]["style"]["density"] = DENSITY_ALIASES.get(configured_density, configured_density)
    cfg["design"]["profile"] = profile_id
    cfg["design"]["profile_hard_rules"] = copy.deepcopy(profile.get("hard_rules", {}))
    cfg["resolved_profile"] = profile
    profile_root = profile_path.parent
    locations = cfg.get("library_locations", {}).get(profile_id, cfg.get("library_locations", {}).get(requested_id, {}))
    visual_root = Path(locations["visual_references"]).expanduser().resolve() if "visual_references" in locations else (profile_root / "libraries" / "visual_references").resolve()
    if not visual_root.exists():
        for old, new in aliases.items():
            old_root = profiles_root / old
            if visual_root.is_relative_to(old_root):
                visual_root = profiles_root / new / visual_root.relative_to(old_root)
                break
    # Explicit profile roots use their sibling shared store, keeping source checkouts
    # independent of whichever libraries happen to be installed on this machine.
    library_sets_root = profiles_root.parent / "library-sets"
    if not (library_sets_root / "catalog.json").is_file():
        library_sets_root = repository_root / "library-sets"
    # Design is captured for a presentation. Resource choices and catalogs remain live.
    resource_profile = load(profile_path) if profile_path.is_file() else profile
    try:
        cfg["libraries"], cfg["library_sets"] = resolve_libraries(
            resource_profile, library_sets_root, session=session,
            legacy_visual_catalog=visual_root / "catalog.json")
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
    for source in cfg.get("remote_sources", {}).values():
        source["enabled"] = False
    for provider in cfg["libraries"]["icons"]["providers"]:
        if provider in cfg.get("remote_sources", {}):
            cfg["remote_sources"][provider]["enabled"] = True
    cfg["design"]["resource_catalogs"] = copy.deepcopy(cfg["libraries"])

    if session.get("slide_role") is not None:
        cfg["scope"]["current_slide_role"] = session["slide_role"]
    if session.get("generation_model") is not None:
        cfg["generation"]["default_model"] = str(session["generation_model"])
    try:
        generation_overrides = session.get("image_generation")
        if session.get("generation_model") is not None and isinstance(generation_overrides, (dict, type(None))):
            generation_overrides = {"model": str(session["generation_model"]), **(generation_overrides or {})}
        cfg["generation"]["preferences"] = resolve_preferences(cfg["generation"], generation_overrides)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    if session.get("density") is not None:
        density = str(session["density"])
        density_profiles = cfg.get("design", {}).get("density_profiles", {})
        density = DENSITY_ALIASES.get(density, density)
        if density not in density_profiles:
            raise SystemExit(f"Unknown density profile: {density}")
        cfg["design"]["style"]["density"] = density
    if session.get("palette") is not None:
        palette = session["palette"]
        if not isinstance(palette, list) or not palette:
            raise SystemExit("palette override must be a non-empty list of colors")
        cfg["design"]["style"]["accent_colors"] = palette
    if session.get("design_overrides"):
        merge_existing(cfg["design"], session["design_overrides"])

    header_override = session.get("header") or {}
    footer_override = session.get("footer") or {}
    remote_source_overrides = session.get("remote_sources") or {}
    legacy_icon_override = session.get("external_icon_fetch") or {}
    measurement_override = session.get("measurement") or {}
    allowed_header = {"enabled", "height_px", "left_text", "right_text"}
    allowed_footer = {"enabled", "height_px", "left_text", "center_text", "slide_number"}
    if set(header_override) - allowed_header:
        raise SystemExit(f"Unsupported header override keys: {sorted(set(header_override)-allowed_header)}")
    if set(footer_override) - allowed_footer:
        raise SystemExit(f"Unsupported footer override keys: {sorted(set(footer_override)-allowed_footer)}")
    allowed_remote_sources = {"remix_icon", "wikimedia_commons"}
    if set(remote_source_overrides) - allowed_remote_sources:
        raise SystemExit(f"Unsupported remote source overrides: {sorted(set(remote_source_overrides) - allowed_remote_sources)}")
    for source_id, source_override in remote_source_overrides.items():
        if not isinstance(source_override, dict) or set(source_override) - {"enabled"}:
            raise SystemExit(f"Only remote_sources.{source_id}.enabled may be overridden per session")
        if source_override.get("enabled") is not None and not isinstance(source_override["enabled"], bool):
            raise SystemExit(f"remote_sources.{source_id}.enabled must be boolean or null")
    if set(legacy_icon_override) - {"enabled"}:
        raise SystemExit("Only legacy external_icon_fetch.enabled may be overridden per session")
    legacy_enabled = legacy_icon_override.get("enabled")
    if legacy_enabled is not None and not isinstance(legacy_enabled, bool):
        raise SystemExit("legacy external_icon_fetch.enabled must be boolean or null")
    remix_enabled = remote_source_overrides.get("remix_icon", {}).get("enabled")
    if legacy_enabled is not None and remix_enabled is not None and legacy_enabled != remix_enabled:
        raise SystemExit("legacy external_icon_fetch.enabled and remote_sources.remix_icon.enabled disagree")
    if set(measurement_override) - {"segmentation"}:
        raise SystemExit("Only measurement.segmentation may be overridden per session")
    segmentation_override = measurement_override.get("segmentation") or {}
    allowed_segmentation = {"mode", "checkpoint", "model_config", "device"}
    if set(segmentation_override) - allowed_segmentation:
        raise SystemExit(f"Unsupported measurement.segmentation keys: {sorted(set(segmentation_override) - allowed_segmentation)}")

    header = cfg["design"]["frame"]["header"]
    footer = cfg["design"]["frame"]["footer"]
    for key in ("enabled", "height_px", "left_text", "right_text"):
        if header_override.get(key) is not None:
            header[key] = header_override[key]
    for key in ("enabled", "height_px", "left_text", "center_text"):
        if footer_override.get(key) is not None:
            footer[key] = footer_override[key]
    if "slide_number" in footer_override:
        slide_number = footer_override["slide_number"] or {}
        if set(slide_number) - {"enabled"}:
            raise SystemExit("Only footer.slide_number.enabled may be overridden")
        if slide_number.get("enabled") is not None:
            footer["slide_number"]["enabled"] = bool(slide_number["enabled"])
    for source_id, source_override in remote_source_overrides.items():
        if source_override.get("enabled") is not None:
            cfg["remote_sources"][source_id]["enabled"] = source_override["enabled"]
    if legacy_icon_override.get("enabled") is not None:
        cfg["remote_sources"]["remix_icon"]["enabled"] = legacy_enabled
    segmentation = cfg["measurement"]["segmentation"]
    for key in allowed_segmentation:
        if segmentation_override.get(key) is not None:
            segmentation[key] = segmentation_override[key]
    if segmentation.get("mode") not in {"auto", "never", "required"}:
        raise SystemExit("measurement.segmentation.mode must be auto, never, or required")
    if segmentation.get("device") not in {"auto", "cpu", "mps", "cuda"}:
        raise SystemExit("measurement.segmentation.device must be auto, cpu, mps, or cuda")

    try:
        canvas = derive_canvas(cfg["design"])
    except ValueError as error:
        raise SystemExit(str(error)) from error

    density = str(cfg.get("design", {}).get("style", {}).get("density", "balanced"))
    density_profiles = cfg.get("design", {}).get("density_profiles", {})
    density = DENSITY_ALIASES.get(density, density)
    if density not in density_profiles:
        raise SystemExit(f"Resolved density profile has no packaged guidance: {density}")
    cfg["design"]["style"]["density"] = density

    cfg["derived"] = {
        **canvas,
        "profile_id": profile_id,
        "profile_path": str(profile_path),
        "profiles_root": str(profiles_root),
        "profile_name": profile.get("name"),
        "profile_visual_reference_priorities": profile.get("visual_reference_priorities", {}),
        "density_profile": density,
        "density_guidance": density_profiles[density],
        "resolution_precedence": [
            "base_config",
            "external_profile",
            "session_overrides",
            "explicit_slide_intent",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(cfg["derived"], indent=2))


if __name__ == "__main__":
    main()
