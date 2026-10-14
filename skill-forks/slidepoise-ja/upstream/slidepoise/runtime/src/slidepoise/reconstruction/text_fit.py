"""Office-safe fitting and joint normalization for native textboxes."""

from __future__ import annotations

import re
import math
import shutil
import subprocess
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from PIL import ImageFont

FONT_PATHS = {
    ("Arial", False, False): (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ),
    ("Arial", True, False): (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
    ("Arial", False, True): (
        "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
        "C:/Windows/Fonts/ariali.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    ),
    ("Arial", True, True): (
        "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
        "C:/Windows/Fonts/arialbi.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-BoldItalic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
    ),
    ("Georgia", False, False): (
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "C:/Windows/Fonts/georgia.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ),
    ("Georgia", True, False): (
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "C:/Windows/Fonts/georgiab.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ),
    ("Georgia", False, True): (
        "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
        "C:/Windows/Fonts/georgiai.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    ),
    ("Georgia", True, True): (
        "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf",
        "C:/Windows/Fonts/georgiaz.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-BoldItalic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf",
    ),
}

def _authored_text(entity: dict[str, Any]) -> str:
    text = str(entity.get("authored_text") or entity.get("source_text") or entity.get("text") or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if (
        entity.get("preserve_explicit_breaks", entity.get("text_structure", {}).get("preserve_explicit_breaks", True))
        or int(entity.get("paragraphs", 1) or 1) > 1
    ):
        return "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")).strip()
    paragraphs = [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n\s*\n", text)]
    return "\n".join(part for part in paragraphs if part)


@lru_cache(maxsize=128)
def _font_path(family: str, bold: bool, italic: bool) -> str | None:
    """Resolve requested font metrics before using the configured fallback family."""
    direct = FONT_PATHS.get((family, bold, italic), ())
    match = next((candidate for candidate in direct if Path(candidate).exists()), None)
    if match:
        return match

    suffix = (" Bold" if bold else "") + (" Italic" if italic else "")
    for extension in ("ttf", "ttc"):
        local = Path("/System/Library/Fonts/Supplemental") / f"{family}{suffix}.{extension}"
        if local.is_file():
            return str(local)

    fc_match = shutil.which("fc-match")
    if fc_match:
        styles = []
        if bold:
            styles.append("Bold")
        if italic:
            styles.append("Italic")
        query = family + (f":style={' '.join(styles)}" if styles else "")
        result = subprocess.run([fc_match, "-f", "%{file}", query], text=True, capture_output=True, check=False)
        candidate = result.stdout.strip()
        if candidate and Path(candidate).is_file():
            return candidate

    fallback = FONT_PATHS.get(("Arial", bold, italic), ()) + FONT_PATHS[("Arial", False, False)]
    return next((candidate for candidate in fallback if Path(candidate).exists()), None)


def _load_font(family: str, bold: bool, italic: bool, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = _font_path(family, bold, italic)
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


CJK = "\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF\U00020000-\U0002FA1F"
WRAP_TOKENS = re.compile(rf"\s+|[{CJK}]|[^{CJK}\s]+")
LINE_END_PROHIBITED = set("（［｛〈《「『【〔〖〘〚‘“")
LINE_START_PROHIBITED = set("，。！？、；：）］｝〉》」』】〕〗〙〛’”")


def _wrap(text: str, font: ImageFont.FreeTypeFont, width_px: float, tracking_px: float = 0) -> list[str]:
    """Supply CJK break opportunities within mixed copy without splitting Latin words.

    This is a fitting estimate. Native rendering remains the authority for actual
    glyph shaping and line layout. Common opening and closing CJK punctuation
    stays with its adjacent content.
    """
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        units: list[str] = []
        for token in WRAP_TOKENS.findall(paragraph):
            if units and not token.isspace() and (token[0] in LINE_START_PROHIBITED or units[-1][-1] in LINE_END_PROHIBITED):
                units[-1] += token
            else:
                units.append(token)
        current = ""
        gap = ""
        for unit in units:
            if unit.isspace():
                gap = " " if current else ""
                continue
            candidate = current + gap + unit
            if not current or font.getlength(candidate) + max(0, len(candidate) - 1) * tracking_px <= width_px:
                current = candidate
            else:
                lines.append(current)
                current = unit
            gap = ""
        lines.append(current)
    return lines or [""]


def resolve_text_style_role(entity: dict[str, Any], design: dict[str, Any]) -> str:
    """Resolve visual text style independently from the entity's semantic meaning."""
    config = design.get("text_reconstruction", {})
    explicit = entity.get("text_style_role")
    if explicit:
        return str(explicit)
    semantic_role = str(entity.get("role", "default"))
    aliases = config.get("legacy_semantic_role_style_aliases", {})
    return str(aliases.get(semantic_role, semantic_role))


def resolve_text_style_policy(entity: dict[str, Any], design: dict[str, Any]) -> dict[str, Any]:
    config = design.get("text_reconstruction", {})
    policies = config.get("text_style_policies", {})
    style_role = resolve_text_style_role(entity, design)
    return policies.get(style_role, policies.get("default", {}))


def require_typography_group(entity: dict[str, Any]) -> str:
    """Return the Agent-authored font-size peer group or fail deterministically."""
    group = str(entity.get("typography_group") or "").strip()
    if not group:
        raise ValueError(
            f"Text entity {entity.get('id')!r} has no typography_group. Every meaningful textbox must declare its "
            "font-size hierarchy/content level; independent per-box fitting is forbidden."
        )
    return group


def _line_spacing(value: Any, entity_id: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"Text {entity_id} line_spacing must be a positive finite number")
    return float(value)


def _base_style(entity: dict[str, Any], design: dict[str, Any]) -> dict[str, Any]:
    """Resolve text styling from explicit semantic authority.

    Visual style choices are authored by the host Agent or an explicit configured
    semantic token. OpenCV color measurement remains evidence for visual review and
    never becomes an implicit reconstruction choice.
    """
    hint = entity.get("style_hint", {})
    style = design.get("style", {})
    policy = resolve_text_style_policy(entity, design)
    token = entity.get("style_token") or hint.get("style_token")
    token_styles = design.get("semantic_style_tokens", {})
    token_style = token_styles.get(token, {}) if token else {}

    family = hint.get("font_family") or token_style.get("font_family") or policy.get("font_family") or style.get("body_font", "Arial")
    weight = hint.get("font_weight", token_style.get("font_weight", policy.get("font_weight", 400)))
    authority = str(hint.get("style_authority") or "").lower()
    observed = hint.get("observed_foreground_color")
    declared = hint.get("color")

    # Fidelity precedence: accepted-target observation is authoritative over a semantic-token default.
    # Tokens provide defaults when the target did not clearly specify a foreground colour.
    if authority in {"user_exact", "agent_visual_observation"} and (observed or declared):
        color = observed or declared
    elif authority == "profile_token" and (token_style.get("text_color") or token_style.get("color")):
        color = token_style.get("text_color") or token_style.get("color")
    elif authority == "profile_policy":
        color = policy.get("color", "#111111")
    elif declared or observed:
        color = declared or observed
    elif token_style.get("text_color") or token_style.get("color"):
        color = token_style.get("text_color") or token_style.get("color")
    else:
        color = policy.get("color", "#111111")

    adjustments = []
    profile_typography = design.get("profile_hard_rules", {}).get("typography", {}) or {}
    allowed_fonts = {str(style.get("display_font", "")), str(style.get("body_font", ""))} - {""}
    if profile_typography.get("font_family_policy") == "agent_observed":
        allowed_fonts = set()
    if allowed_fonts and str(family) not in allowed_fonts:
        requested_family = family
        family = policy.get("font_family") or style.get("body_font", "Arial")
        adjustments.append({"property": "font_family", "requested": requested_family, "resolved": family, "reason": "profile_font_family_policy"})
    italic = bool(hint.get("italic", token_style.get("italic", False)))
    if profile_typography.get("italics_allowed") is False:
        if italic:
            adjustments.append({"property": "italic", "requested": True, "resolved": False, "reason": "profile_italics_policy"})
        italic = False
    allowed_colors = {str(value).upper() for value in profile_typography.get("ordinary_text_colors", [])}
    allowed_colored_tokens = set(profile_typography.get("allowed_colored_text_style_tokens", []))
    token_name = token or hint.get("style_token")
    policy_color = str(policy.get("color", "")).upper()
    color_is_policy_authorized = bool(policy_color and str(color).upper() == policy_color)
    if allowed_colors and str(color).upper() not in allowed_colors and token_name not in allowed_colored_tokens and not color_is_policy_authorized:
        requested_color = color
        color = policy.get("color") or "#000000"
        adjustments.append({"property": "color", "requested": requested_color, "resolved": color, "reason": "profile_text_color_policy"})

    return {
        "family": family or "Arial",
        "bold": weight == "bold" or (isinstance(weight, (int, float)) and weight >= 600),
        "italic": italic,
        "color": color,
        "alignment": hint.get("alignment", token_style.get("alignment", policy.get("alignment", "left"))),
        "vertical_alignment": hint.get("vertical_alignment", token_style.get("vertical_alignment", policy.get("vertical_alignment", "top"))),
        "role_policy": policy,
        "char_spacing_px": float(hint.get("char_spacing_px", 0)),
        "line_spacing": _line_spacing(hint.get("line_spacing", policy.get("line_spacing", 1.1)), entity.get("id", "unknown")),
        "profile_adjustments": adjustments,
    }


def _fits(entity: dict[str, Any], style: dict[str, Any], size_px: float, text_override: str | None = None) -> dict[str, Any] | None:
    _, _, width, height = entity["measurement"]["layout_bbox"]["px"]
    policy = style.get("role_policy", {})
    inset = float(policy.get("inset_px", 2))
    usable_width = max(1.0, width - 2 * inset)
    usable_height = max(1.0, height - 2 * inset)
    scaled = max(4, round(size_px * 4))
    font = _load_font(style["family"], style["bold"], style["italic"], scaled)
    office_width = usable_width * 4 * 0.96
    authored = text_override if text_override is not None else _authored_text(entity)
    if entity.get("bullet_style"):
        authored = "\n".join(f"•  {paragraph}" if paragraph else "" for paragraph in authored.split("\n"))
    tracking = float(style.get("char_spacing_px", 0))
    lines = _wrap(authored, font, office_width, tracking * 4)
    widths = [font.getlength(line or " ") / 4 + max(0, len(line) - 1) * tracking for line in lines]
    line_height = float(style.get("line_spacing", policy.get("line_spacing", 1.1)))
    block_height = len(lines) * size_px * line_height
    if max(widths, default=0) > usable_width * 0.96 or block_height > usable_height * 0.95:
        return None
    return {
        "lines": lines,
        "max_width_px": round(max(widths, default=0), 2),
        "block_height_px": round(block_height, 2),
        "inset_px": inset,
    }


def _floor_step(value: float, step: float) -> float:
    units = value / step
    nearest = round(units)
    # Unit conversions can land microscopically below an exact grid boundary.
    # This tolerance is far smaller than DrawingML's 0.01-point font precision.
    if math.isclose(units, nearest, rel_tol=1e-7, abs_tol=1e-9):
        units = nearest
    return math.floor(units) * step


def finalize_fitted_text_entities(
    entities: list[dict[str, Any]],
    design: dict[str, Any],
    fitted: dict[str, dict[str, Any]],
    *,
    points_per_px: float,
    quantization_step_pt: float = 0.5,
    technical_minimum_pt: float = 0.5,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Revalidate text as semantic peer groups and emit Office-safe sizes.

    Peer typography is a hard visual system constraint. The constructor must not
    silently shrink one peer independently. It first tries the Agent-authored
    allocation box and predicted wrap, then finds the largest shared font size
    that fits the entire peer group. Visual readability remains an Agent decision.
    """
    for name, value in (("points_per_px", points_per_px), ("quantization_step_pt", quantization_step_pt), ("technical_minimum_pt", technical_minimum_pt)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    text_entities = [entity for entity in entities if entity.get("kind") == "text"]
    styles = {entity["id"]: _base_style(entity, design) for entity in text_entities}
    # The host Agent must declare the font-size hierarchy for every textbox.
    # Missing typography_group is an error; there is no implicit per-entity fallback.
    groups: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    missing = [entity for entity in text_entities if entity["id"] not in fitted]
    generated: dict[str, dict[str, Any]] = {}
    if missing:
        generated, _ = fit_text_entities(missing, design)
    for entity in text_entities:
        source = fitted.get(entity["id"], generated.get(entity["id"]))
        if source is None:
            raise ValueError(f"Missing fitted text contract for {entity['id']}")
        group_key = require_typography_group(entity)
        groups[group_key].append((entity, source))

    finalized: dict[str, dict[str, Any]] = {}
    report_groups: list[dict[str, Any]] = []
    for group_key, records in groups.items():
        semantic_role = str(records[0][0].get("role", "default"))
        group_style_roles = {resolve_text_style_role(member, design) for member, _ in records}
        if len(group_style_roles) != 1:
            raise ValueError(
                f"Typography group {group_key!r} mixes text_style_role values: {sorted(group_style_roles)}. "
                "Split different visual hierarchy levels into different typography groups."
            )
        text_style_role = next(iter(group_style_roles))
        policy = resolve_text_style_policy(records[0][0], design)
        for member, source in records:
            styles[member["id"]]["line_spacing"] = _line_spacing(source.get("line_spacing", styles[member["id"]]["line_spacing"]), member["id"])

        raw_targets = [(member.get("style_hint") or {}).get("target_font_size_px") for member, _ in records]
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) for value in raw_targets):
            raise ValueError(f"Typography group {group_key!r} requires one positive Agent-authored target_font_size_px")
        target_sizes = {float(value) for value in raw_targets}
        if len(target_sizes) != 1 or next(iter(target_sizes)) <= 0:
            raise ValueError(f"Typography group {group_key!r} requires one positive Agent-authored target_font_size_px")
        target_px = next(iter(target_sizes))
        # Fitting may reduce an Agent-authored target to prevent overflow. It never
        # enlarges text simply because the allocated box has unused space.
        cap_px = target_px
        target_pt = cap_px * points_per_px
        cap_pt = _floor_step(target_pt, quantization_step_pt)
        floor_pt = max(float(technical_minimum_pt), float(quantization_step_pt))

        # Predicted native wraps from the semantic/text fitting pass are useful
        # layout intent, not literal raster tracing. Materialize them only when
        # they help preserve peer size or readability.
        wrap_candidates: dict[str, list[str]] = {}
        for member, source in records:
            candidates = [_authored_text(member)]
            predicted = source.get("predicted_native_wrap_lines") or []
            if len(predicted) > 1:
                materialized = "\n".join(str(line) for line in predicted)
                if materialized and materialized not in candidates:
                    candidates.append(materialized)
            wrap_candidates[member["id"]] = candidates

        chosen_pt: float | None = None
        chosen_fit: dict[str, dict[str, Any]] = {}
        chosen_text: dict[str, str] = {}
        candidate_pt = cap_pt
        while candidate_pt >= floor_pt - 1e-9:
            fits_all = True
            group_fit: dict[str, dict[str, Any]] = {}
            group_text: dict[str, str] = {}
            for member, _source in records:
                match = None
                match_text = None
                for candidate_text in wrap_candidates[member["id"]]:
                    result = _fits(member, styles[member["id"]], candidate_pt / points_per_px, candidate_text)
                    if result is not None:
                        match = result
                        match_text = candidate_text
                        break
                if match is None:
                    fits_all = False
                    break
                group_fit[member["id"]] = match
                group_text[member["id"]] = match_text or _authored_text(member)
            if fits_all:
                chosen_pt = candidate_pt
                chosen_fit = group_fit
                chosen_text = group_text
                break
            candidate_pt -= quantization_step_pt

        if chosen_pt is None:
            member_ids = [member["id"] for member, _ in records]
            raise ValueError(
                f"Typography peer group {group_key!r} cannot fit at the technical font-size floor "
                f"({floor_pt:g} pt): {member_ids}. Enlarge/reallocate the text boxes, add a justified line break, "
                "or revise wording. Do not independently shrink peers."
            )

        # A different peer size must be represented by a different Agent-authored
        # typography_group; the runtime never splits a declared peer group.
        for member, source in records:
            candidate_px = chosen_pt / points_per_px
            item = dict(source)
            fit = chosen_fit[member["id"]]
            item.update({
                "authored_text": chosen_text[member["id"]],
                "typography_group": group_key,
                "font_size_px": candidate_px,
                "font_size_pt": chosen_pt,
                "predicted_native_wrap_lines": fit["lines"],
                "predicted_max_line_width_px": fit["max_width_px"],
                "predicted_block_height_px": fit["block_height_px"],
                "fit_evidence": "fits_within_agent_authored_allocation",
            })
            finalized[member["id"]] = item

        report_groups.append({
            "typography_group": group_key,
            "semantic_role": semantic_role,
            "text_style_role": text_style_role,
            "member_ids": [member["id"] for member, _ in records],
            "shared_font_size_pt": chosen_pt,
            "shared_font_size_px": round(chosen_pt / points_per_px, 3),
            "agent_target_font_size_px": target_px,
            "explicit_peer_group": len(records) > 1,
            "technical_floor_pt": floor_pt,
            "agent_target_ceiling_pt": cap_pt,
            "agent_target_unquantized_pt": target_pt,
            "quantization_reduction_pt": round(max(0, target_pt - cap_pt), 9),
            "reduced_from_agent_target": chosen_pt < target_pt and not math.isclose(chosen_pt, target_pt, rel_tol=1e-7, abs_tol=1e-9),
            "reduced_for_fit": chosen_pt + 1e-6 < cap_pt,
            "members_not_fitting_target": [member["id"] for member, _ in records if _fits(member, styles[member["id"]], target_px) is None],
            "font_measurement_sources": {member["id"]: _font_path(styles[member["id"]]["family"], styles[member["id"]]["bold"], styles[member["id"]]["italic"]) for member, _ in records},
            "profile_adjustments": {member["id"]: styles[member["id"]]["profile_adjustments"] for member, _ in records if styles[member["id"]]["profile_adjustments"]},
            "overflow_evidence": "no_overflow_detected_by_text_measurement",
        })

    return finalized, {
        "source": "constructor_text_fit_evidence",
        "fitted_textbox_count": len(finalized),
        "quantization_step_pt": quantization_step_pt,
        "all_textboxes_fit_within_allocations": True,
        "peer_typography_preserved": True,
        "text_groups": report_groups,
    }

def _largest_size(entities: list[dict[str, Any]], styles: dict[str, dict[str, Any]], maximum: float, minimum: float) -> tuple[float, dict[str, dict[str, Any]]]:
    """Find the largest size that actually fits every member; never emit a non-fitting fallback."""
    size = float(maximum)
    floor = float(minimum)
    if not math.isfinite(size) or not math.isfinite(floor) or floor <= 0 or size < floor:
        raise ValueError("Text fitting requires finite font-size bounds with maximum >= minimum > 0")
    while size >= floor - 0.001:
        evidence: dict[str, dict[str, Any]] = {}
        for entity in entities:
            fit = _fits(entity, styles[entity["id"]], size)
            if fit is None:
                break
            evidence[entity["id"]] = fit
        else:
            return round(size, 2), evidence
        size -= 0.25
    ids = [entity["id"] for entity in entities]
    raise ValueError(
        f"Text allocation cannot fit at the technical font-size floor ({floor:g}px): {ids}. "
        "The host Agent must revise the logical text region, wording, or peer assignment."
    )


def fit_text_entities(entities: list[dict[str, Any]], design: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Fit authored text by explicit visual peer group and text style role."""
    text_entities = [entity for entity in entities if entity.get("kind") == "text"]
    styles = {entity["id"]: _base_style(entity, design) for entity in text_entities}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entity in text_entities:
        # Font-size peer membership is mandatory and authored by the host Agent.
        # The runtime never silently creates one independent group per textbox.
        group_key = require_typography_group(entity)
        groups[group_key].append(entity)
    fitted: dict[str, dict[str, Any]] = {}
    report_groups: list[dict[str, Any]] = []
    for group_key, members in groups.items():
        semantic_role = str(members[0].get("role", "default"))
        group_style_roles = {resolve_text_style_role(member, design) for member in members}
        if len(group_style_roles) != 1:
            raise ValueError(
                f"Typography group {group_key!r} mixes text_style_role values: {sorted(group_style_roles)}. "
                "Split different visual hierarchy levels into different typography groups."
            )
        text_style_role = next(iter(group_style_roles))
        policy = resolve_text_style_policy(members[0], design)
        _suggested_minimum, suggested_maximum = policy.get("font_size_range_px", [10.0, 20.0])
        size, evidence = _largest_size(members, styles, suggested_maximum, 0.5)
        for member in members:
            style = styles[member["id"]]
            item_evidence = evidence.get(member["id"], {})
            fitted[member["id"]] = {
                "id": member["id"],
                "authored_text": _authored_text(member),
                "typography_group": group_key,
                "font_family": style["family"],
                "font_size_px": size,
                "bold": style["bold"],
                "italic": style["italic"],
                "color": style["color"],
                "alignment": style["alignment"],
                "vertical_alignment": style["vertical_alignment"],
                "line_spacing": style["line_spacing"],
                "paragraph_space_after_px": 0,
                "insets_px": {side: item_evidence.get("inset_px", 0) for side in ("left", "top", "right", "bottom")},
                "predicted_native_wrap_lines": item_evidence.get("lines", []),
                "predicted_max_line_width_px": item_evidence.get("max_width_px"),
                "predicted_block_height_px": item_evidence.get("block_height_px"),
                "autofit": "none",
                "bullet_style": member.get("bullet_style"),
                "office_width_safety_factor": 0.90,
                "office_height_safety_factor": 0.90,
            }
        report_groups.append({
            "typography_group": group_key,
            "semantic_role": semantic_role,
            "text_style_role": text_style_role,
            "member_ids": [member["id"] for member in members],
            "shared_font_size_px": size,
            "font_family": styles[members[0]["id"]]["family"],
            "split": False,
        })
    return fitted, {"text_groups": report_groups, "group_count": len(report_groups), "fitted_textbox_count": len(fitted)}
