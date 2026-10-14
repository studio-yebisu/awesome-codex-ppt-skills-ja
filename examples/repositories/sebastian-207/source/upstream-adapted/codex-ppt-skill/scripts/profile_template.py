#!/usr/bin/env python3
"""
Purpose: Generate template_profile.md and template_profile.json for a PPTX template.
Input: A .pptx path and an output directory.
Output: template_profile.md/json containing size, layouts, placeholders, theme colors, fonts.
Failure behavior: Exit non-zero on unreadable PPTX; never modify source files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from html import unescape
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from inspect_pptx import inspect_pptx  # noqa: E402


def _read(zipf: zipfile.ZipFile, name: str) -> str:
    return zipf.read(name).decode("utf-8", errors="replace")


def _theme_colors_and_fonts(path: Path) -> tuple[list[str], list[str]]:
    colors: set[str] = set()
    fonts: set[str] = set()
    with zipfile.ZipFile(path) as zipf:
        for name in zipf.namelist():
            if name.startswith("ppt/theme/") and name.endswith(".xml"):
                xml = _read(zipf, name)
                colors.update(re.findall(r"<a:srgbClr[^>]*val=\"([0-9A-Fa-f]{6})\"", xml))
                fonts.update(unescape(v) for v in re.findall(r"typeface=\"([^\"]+)\"", xml) if v.strip())
    return sorted(colors), sorted(fonts)


def build_profile(path: Path) -> dict[str, object]:
    info = inspect_pptx(path)
    colors, fonts = _theme_colors_and_fonts(path)
    return {
        "source_path": str(path),
        "slide_count": info["slide_count"],
        "slide_size": info["slide_size"],
        "has_master_or_layouts": bool(info["has_masters"] or info["has_layouts"]),
        "layouts": info["layouts"],
        "theme_colors": colors,
        "fonts": fonts,
        "notes": [
            "Prefer existing layouts and placeholders.",
            "Do not overlay arbitrary text boxes unless no suitable placeholder exists.",
            "Use layout name or layout_id hints in slides_plan.json when possible.",
        ],
    }


def write_markdown(profile: dict[str, object], output: Path) -> None:
    layouts = profile.get("layouts", [])
    lines = [
        "# Template Profile",
        "",
        f"- Source: `{profile['source_path']}`",
        f"- Slide count: {profile['slide_count']}",
        f"- Slide size: `{profile['slide_size']}`",
        f"- Has master/layouts: {profile['has_master_or_layouts']}",
        f"- Theme colors: {', '.join(profile.get('theme_colors', [])) or 'unknown'}",
        f"- Fonts: {', '.join(profile.get('fonts', [])) or 'unknown'}",
        "",
        "## Layouts",
        "",
    ]
    for layout in layouts:
        lines.append(f"- `{layout.get('name')}`: {layout.get('placeholder_count')} placeholders ({layout.get('part')})")
    lines.extend(
        [
            "",
            "## Usage Rules",
            "",
            "- Prefer existing layouts and placeholders.",
            "- Use `[HINT: layout_name]` or `layout_id` in `slides_plan.json`.",
            "- Record limitations if placeholders are missing or too restrictive.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--outdir", "-o", type=Path, default=Path("."))
    args = parser.parse_args()

    try:
        profile = build_profile(args.pptx)
        args.outdir.mkdir(parents=True, exist_ok=True)
        (args.outdir / "template_profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_markdown(profile, args.outdir / "template_profile.md")
    except Exception as exc:
        print(f"profile_template failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
