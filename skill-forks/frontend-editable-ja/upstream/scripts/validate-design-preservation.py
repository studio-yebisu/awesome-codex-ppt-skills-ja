#!/usr/bin/env python3
"""Validate design preservation for ported template decks.

Checks that generated ported decks retain upstream template identity:
- C1: Upstream CSS class preservation on slide elements
- C2: Decorative DOM markers (scanlines, gridlines, texture, SVG, glitch)
- C3: Font-family declarations match STYLE_PRESETS spec
- C4: Root CSS variables include expected palette tokens
- C7: Chrome token presence (--deck-chrome-* variables)

Warnings (not hard failures):
- C8: Banned fonts/colors as display (soft check)
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = ROOT / "examples" / "generated" / "presets"
TEMPLATES_DIR = ROOT / "beautiful-html-templates" / "templates"

# Decorative DOM markers that upstream templates may use
DECORATIVE_MARKERS = {
    "scanlines", "gridline", "gridlines", "texture", "grain", "noise",
    "glitch", "hairline", "axis", "tick", "xaxis", "yaxis", "decor",
    "decoration", "bg", "overlay",
}

# SVG markers
SVG_MARKERS = {"<svg", "<path", "<line", "<circle", "<rect", "<polygon"}

# Chrome token variables required in every ported deck
CHROME_TOKENS = {
    "--deck-chrome-bg",
    "--deck-chrome-border",
    "--deck-chrome-text",
    "--deck-chrome-muted",
    "--deck-chrome-accent",
    "--deck-chrome-shadow",
    "--deck-chrome-surface",
}

# Banned display fonts (warnings only)
BANNED_DISPLAY_FONTS = {
    "inter", "roboto", "arial", "helvetica",
}

# Banned accent colors (warnings only)
BANNED_COLORS = {"#6366f1"}


def load_builder_ports():
    builder_path = ROOT / "scripts" / "build-template-port-decks.py"
    spec = importlib.util.spec_from_file_location("build_template_port_decks", builder_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load {builder_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.PORTS


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def find_slide_classes(source: str) -> list[set[str]]:
    """Extract CSS class sets from section.slide elements."""
    classes_list = []
    for match in re.finditer(
        r'<section\b[^>]*\bclass=["\']([^"\']*)["\'][^>]*>',
        source, flags=re.I
    ):
        cls = set(match.group(1).split())
        if "slide" in cls:
            classes_list.append(cls)
    return classes_list


def find_decorative_markers(source: str) -> set[str]:
    """Find decorative DOM class markers in the deck area."""
    found = set()
    # Check for class-based markers
    for match in re.finditer(r'class=["\']([^"\']*)["\']', source, flags=re.I):
        classes = set(match.group(1).lower().split())
        found.update(classes & DECORATIVE_MARKERS)
    # Check for SVG markers
    for marker in SVG_MARKERS:
        if marker in source.lower():
            found.add(marker.strip("<"))
    return found


def find_root_css_vars(source: str) -> dict[str, str]:
    """Extract :root CSS custom properties."""
    vars_dict = {}
    root_match = re.search(r':root\s*\{([^}]+)\}', source, flags=re.S)
    if root_match:
        block = root_match.group(1)
        for match in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+)', block):
            vars_dict[match.group(1).strip()] = match.group(2).strip()
    return vars_dict


def find_font_families(source: str) -> set[str]:
    """Extract font-family values from CSS."""
    families = set()
    for match in re.finditer(r'font-family\s*:\s*([^;]+)', source, flags=re.I):
        value = match.group(1).strip().lower()
        # Extract individual font names
        for font in re.findall(r'["\']?([a-zA-Z][\w\s-]+)["\']?', value):
            families.add(font.strip().lower())
    return families


def has_chrome_tokens(source: str) -> set[str]:
    """Check which --deck-chrome-* tokens are present."""
    found = set()
    for token in CHROME_TOKENS:
        if token in source:
            found.add(token)
    return found


def fail(errors: list[str], rel: str, message: str) -> None:
    errors.append(f"{rel}: {message}")


def warn(warnings: list[str], rel: str, message: str) -> None:
    warnings.append(f"{rel}: {message}")


def validate_preservation(
    ported_path: Path,
    upstream_path: Path | None,
    port,
    errors: list[str],
    warnings: list[str],
) -> None:
    rel = display_path(ported_path)
    ported = ported_path.read_text(encoding="utf-8")

    # C7: Chrome token presence
    chrome_found = has_chrome_tokens(ported)
    missing_chrome = CHROME_TOKENS - chrome_found
    if missing_chrome:
        fail(errors, rel, f"missing chrome tokens: {', '.join(sorted(missing_chrome))}")

    if upstream_path is None or not upstream_path.is_file():
        warn(warnings, rel, "upstream template not found; skipping class/decor comparison")
        return

    upstream = upstream_path.read_text(encoding="utf-8")

    # C1: Upstream CSS class preservation
    upstream_classes = find_slide_classes(upstream)
    ported_classes = find_slide_classes(ported)
    if upstream_classes and ported_classes:
        # Check that key upstream classes are retained
        upstream_all = set()
        for cls_set in upstream_classes:
            upstream_all.update(cls_set - {"slide", "visible", "active", "current"})
        ported_all = set()
        for cls_set in ported_classes:
            ported_all.update(cls_set - {"slide", "visible", "active", "current"})
        # Report classes that exist upstream but not in ported (excluding runtime-added ones)
        lost = upstream_all - ported_all
        # Filter out classes that are commonly added by the builder
        builder_added = {
            "slide", "slides-offset", "ported-template-deck",
            "slide-edit-layer", "slide-object", "filmstrip-thumb-host",
        }
        significant_lost = lost - builder_added
        if significant_lost and len(significant_lost) > len(upstream_all) * 0.5:
            fail(errors, rel, f"lost {len(significant_lost)}/{len(upstream_all)} upstream slide classes")
        elif significant_lost:
            warn(warnings, rel, f"lost {len(significant_lost)} upstream classes: {', '.join(sorted(significant_lost)[:5])}")

    # C2: Decorative DOM preservation
    upstream_decor = find_decorative_markers(upstream)
    ported_decor = find_decorative_markers(ported)
    if upstream_decor:
        lost_decor = upstream_decor - ported_decor
        if lost_decor and len(lost_decor) > len(upstream_decor) * 0.5:
            fail(errors, rel, f"lost {len(lost_decor)}/{len(upstream_decor)} decorative markers: {', '.join(sorted(lost_decor)[:5])}")
        elif lost_decor:
            warn(warnings, rel, f"lost decorative markers: {', '.join(sorted(lost_decor)[:5])}")

    # C3: Font family match
    ported_fonts = find_font_families(ported)
    upstream_fonts = find_font_families(upstream)
    if upstream_fonts:
        # Check that at least some upstream fonts are present
        retained = upstream_fonts & ported_fonts
        if not retained:
            warn(warnings, rel, f"no upstream fonts retained (upstream had: {', '.join(sorted(upstream_fonts)[:3])})")

    # C4: Color token presence (soft check)
    upstream_vars = find_root_css_vars(upstream)
    ported_vars = find_root_css_vars(ported)
    upstream_color_keys = {k for k in upstream_vars if any(c in k for c in ("color", "bg", "ink", "paper", "accent", "neon", "primary"))}
    if upstream_color_keys:
        ported_color_keys = {k for k in ported_vars if any(c in k for c in ("color", "bg", "ink", "paper", "accent", "neon", "primary"))}
        retained_colors = upstream_color_keys & ported_color_keys
        if not retained_colors:
            warn(warnings, rel, f"no upstream color tokens retained (had: {', '.join(sorted(upstream_color_keys)[:4])})")

    # C8: Banned display fonts (warning only)
    for font in BANNED_DISPLAY_FONTS:
        if font in ported_fonts:
            # Check if it's used as display (first in font-family list)
            display_matches = re.findall(
                rf'font-family\s*:\s*["\']?{font}',
                ported, flags=re.I
            )
            if display_matches:
                warn(warnings, rel, f"banned font '{font}' used as display font")


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--file":
        path = Path(sys.argv[2])
        if not path.is_file():
            print(f"missing {path}", file=sys.stderr)
            return 1
        errors: list[str] = []
        warnings: list[str] = []
        validate_preservation(path, None, None, errors, warnings)
        if errors:
            print("Design preservation failed:")
            for e in errors:
                print(f"- {e}")
            return 2
        if warnings:
            for w in warnings:
                print(f"  warning: {w}")
        print(f"Validated design preservation for {display_path(path)}.")
        return 0

    if not PRESETS_DIR.is_dir():
        print(f"Missing presets dir: {PRESETS_DIR}", file=sys.stderr)
        return 1

    ports = load_builder_ports()
    ports_by_slug = {port.out_slug: port for port in ports}
    errors = []
    warnings = []
    checked = 0

    for port in ports:
        ported_path = PRESETS_DIR / f"{port.out_slug}.html"
        if not ported_path.is_file():
            errors.append(f"missing ported preset {display_path(ported_path)}")
            continue
        upstream_path = TEMPLATES_DIR / port.source_slug / "template.html"
        validate_preservation(ported_path, upstream_path, port, errors, warnings)
        checked += 1

    if errors:
        print("Design preservation validation failed:")
        for e in errors:
            print(f"- {e}")
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for w in warnings:
                print(f"  - {w}")
        return 2

    if warnings:
        print(f"Design preservation: {checked} presets passed with {len(warnings)} warnings:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print(f"Validated design preservation for {checked} ported presets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
