"""Translate explicit Console choices into the existing design configuration."""
from __future__ import annotations

import copy
import re
import subprocess
import sys
import tempfile
from contextlib import ExitStack
from pathlib import Path

from .paths import DEFAULT_CONFIG, SKILL_ROOT, active_profiles_root, data_home
from .profiles import canonical_profile_id, active_profile_id, list_profiles
from .library_sets import list_sets, profile_set_ids
from .storage import ConflictError, locked, read, revision, update, write


FONTS = ["Arial", "Helvetica Neue", "Georgia", "Times New Roman", "Aptos", "Calibri", "Courier New", "Segoe Print", "PingFang SC", "Songti SC"]
DENSITIES = {"spacious": "Spacious", "balanced": "Balanced", "information_rich": "Information-rich"}


def merge(base, overlay):
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge(base[key], value)
        else:
            base[key] = copy.deepcopy(value)
    return base


def resolve_default(profile=None):
    profile = profile or active_profile_id()
    with tempfile.TemporaryDirectory(prefix="slidepoise-style-") as temporary:
        root = Path(temporary)
        write(root / "session.json", {"profile": profile})
        config = data_home() / "config.json"
        result = subprocess.run([sys.executable, str(SKILL_ROOT / "scripts/resolve_config.py"), "--base",
                                 str(config if config.exists() else DEFAULT_CONFIG), "--profiles-root", str(active_profiles_root()),
                                 "--session", str(root / "session.json"), "--output", str(root / "resolved.json")],
                                text=True, capture_output=True)
        if result.returncode:
            raise ValueError(result.stderr or result.stdout)
        return read(root / "resolved.json")


def presentation_values(cfg):
    design = cfg["design"]
    style = design["style"]
    colors = style.get("accent_colors", [])
    tokens = design.get("semantic_style_tokens", {})
    return {"profile": design["profile"], "display_font": style["display_font"], "body_font": style["body_font"],
            "density": style.get("density", "balanced"), "background": style.get("background", "#FFFFFF"),
            "primary": colors[0] if colors else "#171717", "secondary": colors[1] if len(colors) > 1 else "#777777",
            "highlight": colors[2] if len(colors) > 2 else "#AAAAAA",
            "surface": tokens.get("muted_panel", {}).get("fill", "#F5F5F5"),
            "text": tokens.get("primary_text", {}).get("color", "#171717"),
            "icon_treatment": style.get("icon_treatment", "agent_decides")}


def design_patch(cfg, values):
    allowed = {"display_font", "body_font", "density", "primary", "secondary", "highlight", "surface", "text", "background", "icon_treatment"}
    if set(values) - allowed:
        raise ValueError("Unknown design setting")
    design = copy.deepcopy(cfg["design"])
    patch = {}
    def put(path, value):
        cursor = patch
        parts = path.split(".")
        for part in parts[:-1]:
            cursor = cursor.setdefault(part, {})
        cursor[parts[-1]] = value
    for role in ("display", "body"):
        field = role + "_font"
        if field not in values:
            continue
        font = values[field].strip()
        if not font or len(font) > 100 or any(ch in font for ch in "<>\n\r"):
            raise ValueError("Enter a valid typeface name")
        put("style." + field, font)
        if role == "display":
            put("title.font_family", font)
        old = design["style"][field]
        for group, policy in design.get("text_reconstruction", {}).get("text_style_policies", {}).items():
            display_role = group in {"slide_title", "heading_large"}
            if display_role == (role == "display") and policy.get("font_family", old) == old:
                put(f"text_reconstruction.text_style_policies.{group}.font_family", font)
        for name, token in design.get("semantic_style_tokens", {}).items():
            if role == "body" and token.get("font_family") == old:
                put(f"semantic_style_tokens.{name}.font_family", font)
    if "density" in values:
        if values["density"] not in cfg["design"]["density_profiles"]:
            raise ValueError("Unknown information density")
        put("style.density", values["density"])
    if "icon_treatment" in values:
        if values["icon_treatment"] not in {"agent_decides", "plain", "tinted_surface"}:
            raise ValueError("Unknown icon treatment")
        put("style.icon_treatment", values["icon_treatment"])
    colors = list(design["style"].get("accent_colors", []))
    for key in ("primary", "secondary", "highlight", "surface", "text", "background"):
        if key not in values:
            continue
        color = values[key]
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise ValueError("Colors must be six-digit hex values")
        if key in ("primary", "secondary", "highlight"):
            i = ("primary", "secondary", "highlight").index(key)
            while len(colors) <= i:
                colors.append(color)
            old = colors[i]
            colors[i] = color
            # Keep existing exact color tokens aligned with this explicit palette edit.
            def recolor(node, path=""):
                for name, value in node.items():
                    current = f"{path}.{name}" if path else name
                    if isinstance(value, dict):
                        recolor(value, current)
                    elif isinstance(value, str) and value.lower() == old.lower() and ("color" in name or name in {"fill", "stroke"}):
                        put(current, color)
            recolor(design)
        elif key == "surface":
            put("semantic_style_tokens.muted_panel.fill", color)
        elif key == "text":
            put("semantic_style_tokens.primary_text.color", color)
            put("title.color", color)
            for group in design.get("text_reconstruction", {}).get("text_style_policies", {}):
                put(f"text_reconstruction.text_style_policies.{group}.color", color)
        else:
            put("style.background", color)
    if any(key in values for key in ("primary", "secondary", "highlight")):
        put("style.accent_colors", colors)
    return patch


def defaults_payload(profile=None):
    cfg = resolve_default(profile)
    selected = next(item for item in list_profiles() if item["id"] == cfg["design"]["profile"])
    from .profiles import profile_record
    profile_payload = profile_record(selected["id"])["profile"]
    return {"values": presentation_values(cfg), "config": cfg, "profiles": list_profiles(), "active_profile": active_profile_id(),
            "fonts": FONTS, "densities": DENSITIES, "revision": revision(data_home() / "config.json"),
            "profile_revision": revision(Path(selected["path"])), "style_agency": profile_payload.get("style_agency", {}),
            "selected_sets": {kind: profile_set_ids(profile_payload, kind) for kind in ("visual_references", "icons", "components")},
            "selected_items": copy.deepcopy(profile_payload.get("library_items", {})),
            "library_sets": list_sets()}


def save_defaults(profile, values, expected, reset=False):
    profile = canonical_profile_id(profile)
    patch = design_patch(resolve_default(profile), values)
    def change(cfg):
        defaults = cfg.setdefault("user_design_overrides", {})
        if reset:
            defaults.pop(profile, None)
        else:
            defaults[profile] = merge(defaults.get(profile, {}), patch)
        return cfg
    update(data_home() / "config.json", change, expected=expected, default=read(DEFAULT_CONFIG))


def save_runtime(values, expected):
    allowed = {"remix_icon", "wikimedia_commons"}
    if set(values) - allowed:
        raise ValueError("Unknown runtime setting")
    def change(cfg):
        for source in ("remix_icon", "wikimedia_commons"):
            if source in values:
                if type(values[source]) is not bool:
                    raise ValueError("Resource switches must be boolean")
                cfg["remote_sources"][source]["enabled"] = values[source]
        return cfg
    update(data_home() / "config.json", change, expected=expected, default=read(DEFAULT_CONFIG))


def save_profile_style(profile, values, profile_values, expected, profile_expected):
    profile = canonical_profile_id(profile)
    """Save one Console edit with both revisions checked before either write."""
    from .profile_authoring import apply_profile_values
    from .profiles import profile_record
    if set(profile_values) - {"style_agency", "library_sets", "library_items"}:
        raise ValueError("Unknown profile style setting")
    modes = {"typography": {"specified", "guided", "agent_decides"},
             "density": {"specified", "guided", "agent_decides"},
             "palette": {"specified", "guided", "agent_decides_from_references"}}
    agency = profile_values.get("style_agency", {})
    if not isinstance(agency, dict) or any(key not in modes or mode not in modes[key] for key, mode in agency.items()):
        raise ValueError("Unknown style flexibility setting")
    config_path = data_home() / "config.json"
    profile_path = Path(profile_record(profile)["path"])
    with ExitStack() as stack:
        for path in sorted((config_path, profile_path)):
            stack.enter_context(locked(path))
        if expected != revision(config_path) or profile_expected != revision(profile_path):
            raise ConflictError("Changed in another window or Agent. Reload before saving your changes.")
        old_profile = profile_path.read_bytes()
        configured = read(config_path, read(DEFAULT_CONFIG))
        original_profile = read(profile_path)
        profile_values = copy.deepcopy(profile_values)
        if "style_agency" in profile_values:
            profile_values["style_agency"] = {**original_profile.get("style_agency", {}), **agency}
        updated_profile = apply_profile_values(profile, original_profile, profile_values)
        patch = design_patch(resolve_default(profile), values)
        defaults = configured.setdefault("user_design_overrides", {})
        defaults[profile] = merge(defaults.get(profile, {}), patch)
        # Stage the rollback bytes before changing the profile. A rejected or
        # failed config write restores the exact original profile revision.
        with tempfile.NamedTemporaryFile(dir=profile_path.parent, delete=False) as backup:
            backup.write(old_profile)
            backup_path = Path(backup.name)
        try:
            write(profile_path, updated_profile)
            try:
                write(config_path, configured)
            except BaseException:
                backup_path.replace(profile_path)
                raise
        finally:
            backup_path.unlink(missing_ok=True)
