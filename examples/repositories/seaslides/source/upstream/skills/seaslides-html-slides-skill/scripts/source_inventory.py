#!/usr/bin/env python3
"""Build a Markdown inventory of source text and images for HTML slides.

Usage:
    python3 source_inventory.py <sources_dir>

The report is written to stdout for prompt embedding. Source files are never
modified.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from analyze_images import analyze_images  # noqa: E402


IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp",
    ".tiff", ".tif",
}
MARKDOWN_EXTENSIONS = {".md", ".markdown"}
PDF_EXTENSIONS = {".pdf"}
TEMPORARY_SUFFIXES = (".tmp", ".temp", ".partial", ".part")


def is_inventory_file(path: Path, sources_dir: Path) -> bool:
    """Return whether a path is a visible, durable source input."""
    try:
        path.resolve(strict=True).relative_to(sources_dir.resolve())
    except (OSError, ValueError):
        return False
    return (
        path.is_file()
        and not path.name.endswith(".receipt.json")
        and not path.name.endswith(TEMPORARY_SUFFIXES)
        and not path.name.startswith("~$")
        and not any(part.startswith(".") for part in path.relative_to(sources_dir).parts)
    )


def inventory_paths(sources_dir: Path) -> tuple[list[Path], list[str]]:
    """List safe source files and report links that resolve outside sources/."""
    files: list[Path] = []
    warnings: list[str] = []
    for path in sources_dir.rglob("*"):
        try:
            path.resolve(strict=True).relative_to(sources_dir.resolve())
        except (OSError, ValueError):
            if path.is_symlink():
                warnings.append(
                    f"- Skipped symlink outside `sources/`: `sources/{path.relative_to(sources_dir)}`"
                )
            continue
        if is_inventory_file(path, sources_dir):
            files.append(path)
    return sorted(files), warnings


def html_layout_hint(path: str, orientation: str) -> str:
    """Return guidance without assuming theme-specific class names."""
    kind = orientation.lower()
    quoted_path = f"sources/{path}"
    if "portrait" in kind:
        role = "portrait media in a theme-defined split or side-column layout"
    elif "ultra" in kind or "wide" in kind:
        role = "full-width banner, hero media, or CSS background with a safe crop"
    elif "standard" in kind:
        role = "landscape media in a theme-defined split or media panel"
    else:
        role = "contained media, card illustration, or balanced split layout"
    return f"Use `{quoted_path}` as {role}; keep sizing/cropping in `template.css`."


def build_inventory(sources_dir: Path) -> str:
    """Return a complete Markdown inventory, or an empty string for no files."""
    files, path_warnings = inventory_paths(sources_dir)
    if not files and not path_warnings:
        return ""

    markdown_files: list[tuple[Path, Path]] = []
    image_files: list[tuple[Path, Path]] = []
    pdf_files: list[tuple[Path, Path]] = []
    other_files: list[tuple[Path, Path]] = []

    for path in files:
        relative = path.relative_to(sources_dir)
        suffix = path.suffix.lower()
        if suffix in MARKDOWN_EXTENSIONS:
            markdown_files.append((path, relative))
        elif suffix in IMAGE_EXTENSIONS:
            image_files.append((path, relative))
        elif suffix in PDF_EXTENSIONS:
            pdf_files.append((path, relative))
        else:
            other_files.append((path, relative))

    sections: list[str] = []
    inventory = ["## Source File Inventory"]
    groups = (
        ("Markdown Files", markdown_files),
        ("Image Files", image_files),
        ("PDF Files", pdf_files),
        ("Other Files", other_files),
    )
    for heading, group in groups:
        if group:
            inventory.append(f"\n### {heading}")
            inventory.extend(f"- `sources/{relative}`" for _, relative in group)
    sections.append("\n".join(inventory))

    source_content = []
    read_warnings = list(path_warnings)
    for source_path, relative in markdown_files:
        try:
            content = source_path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError as error:
            read_warnings.append(f"- Could not read `sources/{relative}`: {error}")
            continue
        if content:
            source_content.append(f"### Source: {relative}\n\n{content}")
    if source_content:
        sections.append("## Source Content\n\n" + "\n\n---\n\n".join(source_content))
    if read_warnings:
        sections.append("## Source Read Warnings\n\n" + "\n".join(read_warnings))

    if image_files:
        analyzed = {
            str(record["filename"]): record
            for record in analyze_images(str(sources_dir), recursive=True)
        }
        rows = [
            "## Source Images",
            "",
            "Use local paths from the assembled project. Apply layout and crop "
            "behavior through documented theme classes.",
            "",
            "| Image | Path | Size | Orientation | HTML layout guidance |",
            "|---|---|---:|---|---|",
        ]
        for _, relative in image_files:
            relative_text = str(relative)
            record = analyzed.get(relative_text)
            if record:
                size = f"{record['width']}x{record['height']}"
                orientation = str(record["layout_hint"])
            else:
                size = "unknown"
                orientation = "unknown"
            hint = html_layout_hint(relative_text, orientation)
            rows.append(
                f"| {relative.stem} | `sources/{relative}` | {size} | "
                f"{orientation.lower()} | {hint} |"
            )
        sections.append("\n".join(rows))

    return "\n\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a source inventory with HTML layout guidance"
    )
    parser.add_argument("sources_dir", help="Path to the sources directory")
    args = parser.parse_args()

    sources_dir = Path(args.sources_dir).expanduser().resolve()
    if not sources_dir.is_dir():
        print(f"Error: Directory not found: {sources_dir}", file=sys.stderr)
        return 1

    report = build_inventory(sources_dir)
    if report:
        print(report)
    else:
        print("No source files found.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
