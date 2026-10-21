#!/usr/bin/env python3
"""
HTML Compiler

Compiles HTML presentation projects to SVG, PNG, browser PNG, PDF, PPTX,
or overview grid image.
Mirrors the typst_compiler.py interface for consistency.

Pipeline:
  1. Assemble: merge index-template.html + content HTML -> index.html (inlines CSS)
  2. HTML to SVG: browser DOM-layout conversion -> per-slide SVGs
  3. SVG to PNG: browser rendering -> output/pngs
  4. HTML to browser PNG: direct Chromium screenshots -> output/browser_pngs
  5. PNG to overview: stitched grid image for LLM review
  6. SVG to PDF: Chromium vector printing -> output/slides.pdf
  7. SVG to PPTX: editable DrawingML shapes with rasterized math -> output/slides.pptx

Usage:
    python3 html_compiler.py <project_path> --all
    python3 html_compiler.py <project_path> --format png
    python3 html_compiler.py <project_path> --format browser-png
    python3 html_compiler.py <project_path> --format pdf
    python3 html_compiler.py <project_path> --format pptx
    python3 html_compiler.py <project_path> --format overview
    python3 html_compiler.py <project_path> --entry demo.html   # Template dev
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from math import ceil
from urllib.parse import unquote, urlsplit

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from runtime_environment import runtime_environment_fingerprint  # noqa: E402

DEFAULT_CANVAS_WIDTH = 1280
DEFAULT_CANVAS_HEIGHT = 720
CANVAS_PROP_RE = re.compile(
    r"--(?P<base>slide|page|canvas|poster-page)-(?P<dim>width|height)\s*:\s*"
    r"(?P<value>\d+(?:\.\d+)?)\s*(?:px)?\b",
    re.IGNORECASE,
)
HTML_LOCAL_REF_RE = re.compile(
    r"\b(?:src|href|poster)\s*=\s*([\"'])(.*?)\1",
    re.IGNORECASE | re.DOTALL,
)
CSS_URL_RE = re.compile(r"url\(\s*([\"']?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMPORT_QUOTED_RE = re.compile(
    r"@import\s+([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL
)


class _SlideNotesParser(HTMLParser):
    """Collect canonical ``data-notes`` values from slide sections."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.notes: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() != "section":
            return
        attr_map = {
            str(name).lower(): value if value is not None else ""
            for name, value in attrs
        }
        if "slide" not in attr_map.get("class", "").split():
            return
        self.notes.append(attr_map.get("data-notes", "").strip())


def collect_slide_notes(content_html: Path, svg_files: list[Path]) -> dict[str, str]:
    """Map source ``data-notes`` to exported SVG stems in slide order.

    ``data-notes`` is the HTML skill's canonical narration source.  Enforcing
    the same roster here prevents a successful PPTX export that silently loses
    notes or attaches them to the wrong slide.
    """
    parser = _SlideNotesParser()
    try:
        parser.feed(content_html.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as error:
        raise RuntimeError(f"cannot read PPTX speaker notes from {content_html}: {error}") from error

    if len(parser.notes) != len(svg_files):
        raise RuntimeError(
            "PPTX notes roster does not match the SVG export: "
            f"{len(parser.notes)} source slide(s), {len(svg_files)} SVG slide(s)"
        )
    missing = [index for index, note in enumerate(parser.notes, 1) if not note]
    if missing:
        raise RuntimeError(
            "PPTX export requires non-empty data-notes on every slide; "
            f"missing on slide(s) {missing}"
        )
    return {
        svg_file.stem: parser.notes[index]
        for index, svg_file in enumerate(svg_files)
    }


def sha256_file(path: Path) -> str:
    """Return a stable SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_directory(path: Path) -> str:
    """Hash a directory from relative paths and file bytes."""
    digest = hashlib.sha256()
    for child in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256_file(child)))
    return digest.hexdigest()


def collect_local_dependencies(project_path: Path, source_paths: list[Path]) -> list[Path]:
    """Resolve the project-contained HTML/CSS dependency closure safely."""
    dependencies: set[Path] = set()
    project_root = project_path.resolve()
    pending = [path.resolve() for path in source_paths]
    scanned: set[Path] = set()

    def references_for(source: Path, text: str) -> list[str]:
        if source.suffix.lower() == ".css":
            references = [match.group(2).strip() for match in CSS_URL_RE.finditer(text)]
            references.extend(
                match.group(2).strip() for match in CSS_IMPORT_QUOTED_RE.finditer(text)
            )
            return references
        return [match.group(2).strip() for match in HTML_LOCAL_REF_RE.finditer(text)]

    while pending:
        source = pending.pop()
        if source in scanned:
            continue
        try:
            source.relative_to(project_root)
        except ValueError as error:
            raise RuntimeError(f"source dependency escapes the project: {source}") from error
        scanned.add(source)
        text = source.read_text(encoding="utf-8")
        for reference in references_for(source, text):
            if not reference or reference.startswith("#") or reference.startswith("//"):
                continue
            parsed = urlsplit(reference)
            if parsed.scheme in {"blob", "data", "http", "https", "mailto", "javascript", "tel"}:
                continue
            clean = unquote(parsed.path)
            if not clean:
                continue
            dependency = (source.parent / clean).resolve()
            try:
                dependency.relative_to(project_root)
            except ValueError as error:
                raise RuntimeError(
                    f"local dependency escapes the project: {reference!r} in {source.name}"
                ) from error
            if not dependency.is_file():
                raise RuntimeError(
                    f"referenced local dependency is missing: {reference!r} in {source.name}"
                )
            if dependency not in dependencies:
                dependencies.add(dependency)
                if dependency.suffix.lower() == ".css":
                    pending.append(dependency)
    return sorted(dependencies)


def managed_publish_targets(project_path: Path) -> set[Path]:
    """Return canonical paths that the compiler owns and may never be overridden."""
    output_dir = project_path / "output"
    return {
        path.resolve() for path in {
            project_path / "index.html",
            output_dir / "svgs",
            output_dir / "pngs",
            output_dir / "browser_pngs",
            output_dir / "overview.png",
            output_dir / "slides.pdf",
            output_dir / "slides.pptx",
            output_dir / "dom-audit.json",
            output_dir / "render-fidelity.json",
            output_dir / "compile-manifest.json",
        }
    }


def normalize_publish_targets(project_path: Path, targets: dict[str, Path]) -> dict[str, Path]:
    """Resolve publish targets and reject collisions before rendering starts."""
    normalized = {name: path.expanduser().resolve() for name, path in targets.items()}
    items = list(normalized.items())
    for index, (left_name, left_path) in enumerate(items):
        for right_name, right_path in items[index + 1:]:
            try:
                left_path.relative_to(right_path)
                overlap = True
            except ValueError:
                try:
                    right_path.relative_to(left_path)
                    overlap = True
                except ValueError:
                    overlap = False
            if overlap:
                raise RuntimeError(
                    "publish targets must be disjoint; collision between "
                    f"{left_name} ({left_path}) and {right_name} ({right_path})"
                )
    return normalized


def resolve_output_target(
    project_path: Path, output_path: str | None, default: Path,
) -> Path:
    """Resolve a custom --output and keep compiler-owned locations exclusive."""
    if not output_path:
        return default.resolve()
    target = Path(output_path).expanduser().resolve()
    for managed in managed_publish_targets(project_path.resolve()):
        try:
            target.relative_to(managed)
            overlap = True
        except ValueError:
            try:
                managed.relative_to(target)
                overlap = True
            except ValueError:
                overlap = False
        if overlap:
            raise RuntimeError(
                f"--output cannot overlap compiler-managed artifact: {target} / {managed}"
            )
    return target


def remove_generated_path(path: Path) -> None:
    """Remove one exact compiler-managed path."""
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)


def publish_atomically(pairs: list[tuple[Path, Path]], token: str) -> None:
    """Publish staged paths as one rollback-capable transaction."""
    published: list[tuple[Path, Path | None]] = []
    try:
        for staged, target in pairs:
            if not staged.exists():
                raise RuntimeError(f"staged artifact is missing: {staged}")
            target.parent.mkdir(parents=True, exist_ok=True)
            backup = target.with_name(f".{target.name}.backup-{token}")
            remove_generated_path(backup)
            if target.exists():
                os.replace(target, backup)
                saved: Path | None = backup
            else:
                saved = None
            try:
                os.replace(staged, target)
            except Exception:
                if saved is not None and saved.exists():
                    os.replace(saved, target)
                raise
            published.append((target, saved))
    except Exception:
        for target, backup in reversed(published):
            remove_generated_path(target)
            if backup is not None and backup.exists():
                os.replace(backup, target)
        raise
    else:
        for _, backup in published:
            if backup is not None:
                remove_generated_path(backup)


def slide_numbers(paths: list[Path]) -> list[int]:
    numbers: list[int] = []
    for path in paths:
        match = re.search(r"(\d+)$", path.stem)
        if not match:
            raise RuntimeError(f"slide artifact has no numeric suffix: {path.name}")
        numbers.append(int(match.group(1)))
    return numbers


def verify_slide_roster(paths: list[Path], label: str) -> list[int]:
    if not paths:
        raise RuntimeError(f"{label} produced zero slides")
    numbers = slide_numbers(paths)
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        raise RuntimeError(
            f"{label} slide roster is not contiguous: found {numbers}, expected {expected}"
        )
    return numbers


def verify_svg_canvas(svg_files: list[Path], width: int, height: int) -> None:
    expected = [0.0, 0.0, float(width), float(height)]
    for path in svg_files:
        root = ET.parse(path).getroot()
        raw = root.attrib.get("viewBox", "")
        try:
            actual = [float(value) for value in raw.replace(",", " ").split()]
        except ValueError as error:
            raise RuntimeError(f"{path.name} has an invalid viewBox: {raw!r}") from error
        if len(actual) != 4 or any(abs(a - b) > 0.01 for a, b in zip(actual, expected)):
            raise RuntimeError(
                f"{path.name} canvas {raw!r} does not match {width}x{height}"
            )


def verify_png_set(
    png_dir: Path,
    expected_numbers: list[int],
    width: int,
    height: int,
    scale: float,
    label: str,
) -> list[Path]:
    try:
        from PIL import Image
    except ImportError as error:
        raise RuntimeError("Pillow is required to verify PNG output") from error

    files = sorted(
        png_dir.glob("slide_*.png"),
        key=lambda path: slide_numbers([path])[0],
    )
    numbers = verify_slide_roster(files, label)
    if numbers != expected_numbers:
        raise RuntimeError(
            f"{label} roster {numbers} does not match SVG roster {expected_numbers}"
        )
    expected_size = (round(width * scale), round(height * scale))
    for path in files:
        with Image.open(path) as image:
            if image.size != expected_size:
                raise RuntimeError(
                    f"{path.name} is {image.size[0]}x{image.size[1]}, "
                    f"expected {expected_size[0]}x{expected_size[1]}"
                )
    return files


def step_browser_dom_audit(
    index_html: Path,
    output_path: Path,
    width: int = DEFAULT_CANVAS_WIDTH,
    height: int = DEFAULT_CANVAS_HEIGHT,
    timeout: int = 120_000,
) -> dict:
    """Measure the settled browser DOM and return its quality receipt.

    Exit code 2 means the audit completed and found deterministic blockers.  It
    is not a renderer crash: compilation continues so complete visual evidence
    can be published alongside a non-passing manifest.
    """
    script = SCRIPTS_DIR / "html_to_svg" / "browser_dom_audit.mjs"
    if not script.exists():
        raise RuntimeError(f"browser DOM audit not found at {script}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "node", str(script), str(index_html), "-o", str(output_path),
        "--width", str(width), "--height", str(height), "--timeout", str(timeout),
    ]
    print(f"Auditing settled browser DOM (canvas={width}x{height}, timeout={timeout}ms) ...")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode not in (0, 2):
        detail = result.stderr.strip() or result.stdout.strip() or "unknown browser audit error"
        raise RuntimeError(f"browser DOM audit failed: {detail}")
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError("browser DOM audit produced no receipt")
    try:
        receipt = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"browser DOM audit produced invalid JSON: {error}") from error
    if receipt.get("schema") != "seaslides.browser-dom-audit":
        raise RuntimeError("browser DOM audit returned an unsupported receipt schema")
    summary = receipt.get("summary", {})
    blocker_count = summary.get("blockerCount")
    review_count = summary.get("reviewCount")
    if not isinstance(blocker_count, int) or not isinstance(review_count, int):
        raise RuntimeError("browser DOM audit receipt is missing issue counts")
    print(
        f"  DOM audit: {summary.get('slideCount', 0)} slide(s), "
        f"{blocker_count} blocker(s), {review_count} review item(s)"
    )
    return receipt


def compare_render_routes(
    svg_png_dir: Path,
    browser_png_dir: Path,
    output_path: Path,
) -> dict:
    """Record browser-vs-SVG raster drift as review evidence, never a blocker."""
    try:
        from PIL import Image, ImageChops, ImageStat
    except ImportError as error:
        raise RuntimeError("Pillow is required to compare PNG render routes") from error

    svg_files = sorted(svg_png_dir.glob("slide_*.png"), key=lambda path: slide_numbers([path])[0])
    browser_files = sorted(
        browser_png_dir.glob("slide_*.png"), key=lambda path: slide_numbers([path])[0]
    )
    svg_numbers = verify_slide_roster(svg_files, "SVG-route fidelity input")
    browser_numbers = verify_slide_roster(browser_files, "browser fidelity input")
    if svg_numbers != browser_numbers:
        raise RuntimeError(
            f"render fidelity rosters differ: SVG {svg_numbers}, browser {browser_numbers}"
        )

    rows = []
    for number, svg_path, browser_path in zip(svg_numbers, svg_files, browser_files):
        with Image.open(svg_path).convert("RGB") as svg_image, Image.open(browser_path).convert("RGB") as browser_image:
            if svg_image.size != browser_image.size:
                raise RuntimeError(
                    f"render fidelity canvas mismatch on slide {number}: "
                    f"{svg_image.size} != {browser_image.size}"
                )
            difference = ImageChops.difference(svg_image, browser_image)
            mean_abs = sum(ImageStat.Stat(difference).mean) / 3
            bands = difference.split()
            maximum = ImageChops.lighter(ImageChops.lighter(bands[0], bands[1]), bands[2])
            histogram = maximum.histogram()
            pixel_count = svg_image.width * svg_image.height
            changed_ratio = sum(histogram[9:]) / pixel_count
            threshold_mask = maximum.point(lambda value: 255 if value > 8 else 0)
            bbox = threshold_mask.getbbox()
            review = mean_abs > 10 or changed_ratio > 0.15
            rows.append({
                "slide": number,
                "mean_abs": round(mean_abs, 4),
                "changed_ratio_gt8": round(changed_ratio, 6),
                "changed_bbox_gt8": list(bbox) if bbox else None,
                "status": "review" if review else "pass",
            })

    review_slides = [row["slide"] for row in rows if row["status"] == "review"]
    receipt = {
        "schema": "seaslides.html-render-fidelity/v1",
        "status": "review" if review_slides else "pass",
        "policy": {
            "severity": "review-only",
            "mean_abs_review_above": 10,
            "changed_ratio_gt8_review_above": 0.15,
        },
        "slide_count": len(rows),
        "review_slides": review_slides,
        "slides": rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"  Render fidelity: {len(rows)} slide(s), {len(review_slides)} review item(s)")
    return receipt


def artifact_record(path: Path, root: Path) -> dict:
    record = {
        "path": str(path.relative_to(root)) if path.is_relative_to(root) else str(path),
        "kind": "directory" if path.is_dir() else "file",
    }
    if path.is_dir():
        files = sorted(item for item in path.rglob("*") if item.is_file())
        record.update({"file_count": len(files), "sha256": sha256_directory(path)})
    else:
        record.update({"bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return record


# ============================================================
def list_svg_files(svg_dir: Path) -> list[Path]:
    """Return slide SVGs in natural filename order, excluding hidden files."""
    return sorted(
        (
            path
            for path in svg_dir.glob("*.svg")
            if not path.name.startswith(".")
        ),
        key=lambda path: [
            int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", path.name)
        ],
    )


def infer_canvas_size(
    project_path: Path,
    explicit_width: int | None = None,
    explicit_height: int | None = None,
) -> tuple[int, int, str]:
    """Infer the browser canvas size used for rendering slides.

    The HTML templates primarily use viewport units (`100vw`/`100vh`).  The
    browser viewport is therefore the authoritative slide canvas for SVG/PNG
    export.  Projects can declare the intended canvas through CSS custom
    properties, which keeps the value close to the template and avoids passing
    per-project flags through batch scripts.
    """

    if explicit_width is not None or explicit_height is not None:
        if explicit_width is None or explicit_height is None:
            print("Error: --width and --height must be provided together")
            sys.exit(1)
        return explicit_width, explicit_height, "cli"

    for name in ("template.css", "index-template.html", "index.html"):
        path = project_path / name
        if not path.exists():
            continue
        props: dict[str, dict[str, float]] = {}
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in CANVAS_PROP_RE.finditer(text):
            base = match.group("base").lower()
            dim = match.group("dim").lower()
            value = float(match.group("value"))
            props.setdefault(base, {})[dim] = value

        for base in ("slide", "page", "canvas", "poster-page"):
            dims = props.get(base)
            if not dims or "width" not in dims or "height" not in dims:
                continue
            width = max(1, round(dims["width"]))
            height = max(1, round(dims["height"]))
            return width, height, f"{name}:--{base}-width/height"

    return DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT, "default 16:9"


def step_assemble(template: Path, content: Path, output: Path) -> Path:
    """Merge index-template.html + content HTML into a standalone index.html."""
    assemble_script = SCRIPTS_DIR / "assemble.py"
    if not assemble_script.exists():
        print(f"Error: assemble.py not found at {assemble_script}")
        sys.exit(1)

    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(assemble_script), str(template), str(content), "-o", str(output)]

    print(f"Assembling HTML ...")
    print(f"  Template: {template}")
    print(f"  Content:  {content}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error assembling HTML:\n{result.stderr}")
        sys.exit(1)
    print(f"  -> {output} ({output.stat().st_size:,} bytes)")
    return output


def step_html_to_svg(
    input_html: Path,
    svg_dir: Path,
    width: int = DEFAULT_CANVAS_WIDTH,
    height: int = DEFAULT_CANVAS_HEIGHT,
    timeout: int = 120_000,
) -> Path:
    """Convert assembled HTML to per-slide SVGs."""
    html_to_svg_script = SCRIPTS_DIR / "html_to_svg" / "browser_dom_to_svg.mjs"
    if not html_to_svg_script.exists():
        print(f"Error: HTML to SVG renderer not found at {html_to_svg_script}")
        sys.exit(1)

    svg_dir.mkdir(parents=True, exist_ok=True)
    for existing in svg_dir.glob("*.svg"):
        existing.unlink(missing_ok=True)
    cmd = [
        "node", str(html_to_svg_script),
        str(input_html), "-o", str(svg_dir),
        "--width", str(width),
        "--height", str(height),
        "--timeout", str(timeout),
    ]

    print(f"Converting HTML to SVG (browser DOM, canvas={width}x{height}, timeout={timeout}ms) ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error converting HTML to SVG:\n{result.stderr}")
        sys.exit(1)

    # Print the SVG output lines (filtering noise)
    for line in result.stdout.strip().splitlines():
        if line.strip().startswith("->") or line.startswith("Done!") or line.startswith("Found"):
            print(f"  {line.strip()}")

    svg_count = len(list_svg_files(svg_dir))
    if svg_count == 0:
        print("Error: HTML renderer returned success but produced zero SVG slides")
        sys.exit(1)
    print(f"  {svg_count} SVGs -> {svg_dir}/")
    return svg_dir


def check_svg_images_embedded(svg_dir: Path) -> None:
    """Fail fast if exported SVGs contain external image references."""
    external_refs: list[str] = []
    image_count = 0

    for svg_path in list_svg_files(svg_dir):
        try:
            root = ET.parse(svg_path).getroot()
        except ET.ParseError as error:
            print(f"Error parsing SVG {svg_path}: {error}")
            sys.exit(1)

        for image in root.iter():
            if not image.tag.endswith("image"):
                continue
            image_count += 1
            href = (
                image.attrib.get("href")
                or image.attrib.get("{http://www.w3.org/1999/xlink}href")
                or ""
            )
            if not href.startswith("data:"):
                external_refs.append(f"{svg_path}: {href or '<missing href>'}")

    if external_refs:
        print("Error: SVG image references must be embedded data URIs.")
        for ref in external_refs[:20]:
            print(f"  {ref}")
        if len(external_refs) > 20:
            print(f"  ... and {len(external_refs) - 20} more")
        sys.exit(1)

    if image_count:
        print(f"  SVG image check: {image_count} embedded image(s), 0 external refs")


def step_svg_to_png_browser(
    svg_dir: Path,
    png_dir: Path,
    ppi: float = 2.0,
    width: int = DEFAULT_CANVAS_WIDTH,
    height: int = DEFAULT_CANVAS_HEIGHT,
    timeout: int = 120_000,
) -> Path:
    """Convert SVGs to individual PNGs using Chromium."""
    browser_svg_to_png_script = SCRIPTS_DIR / "html_to_svg" / "browser_svg_to_png.mjs"
    if not browser_svg_to_png_script.exists():
        print(f"Error: browser_svg_to_png.mjs not found at {browser_svg_to_png_script}")
        sys.exit(1)

    png_dir.mkdir(parents=True, exist_ok=True)
    for existing in png_dir.glob("*.png"):
        existing.unlink(missing_ok=True)
    cmd = [
        "node", str(browser_svg_to_png_script),
        str(svg_dir), "-o", str(png_dir),
        "--width", str(width),
        "--height", str(height),
        "--scale", str(ppi),
        "--timeout", str(timeout),
    ]

    print(f"Converting SVG to PNG with browser (scale={ppi}, timeout={timeout}ms) ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error converting SVG to PNG with browser:\n{result.stderr}")
        sys.exit(1)

    for line in result.stdout.strip().splitlines():
        if line.strip().startswith("->") or line.startswith("Done!"):
            print(f"  {line.strip()}")

    if not list(png_dir.glob("slide_*.png")):
        print("Error: SVG renderer returned success but produced zero PNG slides")
        sys.exit(1)
    print(f"  PNGs -> {png_dir}/")
    return png_dir


def step_html_to_png_browser(
    index_html: Path,
    png_dir: Path,
    ppi: float = 2.0,
    width: int = DEFAULT_CANVAS_WIDTH,
    height: int = DEFAULT_CANVAS_HEIGHT,
    timeout: int = 120_000,
) -> Path:
    """Capture assembled HTML slides directly to PNGs using Chromium."""
    browser_html_to_png_script = SCRIPTS_DIR / "html_to_svg" / "browser_html_to_png.mjs"
    if not browser_html_to_png_script.exists():
        print(f"Error: browser_html_to_png.mjs not found at {browser_html_to_png_script}")
        sys.exit(1)

    png_dir.mkdir(parents=True, exist_ok=True)
    for existing in png_dir.glob("*.png"):
        existing.unlink(missing_ok=True)
    cmd = [
        "node", str(browser_html_to_png_script),
        str(index_html), "-o", str(png_dir),
        "--width", str(width),
        "--height", str(height),
        "--scale", str(ppi),
        "--timeout", str(timeout),
    ]

    print(f"Capturing HTML to browser PNG with Chromium (canvas={width}x{height}, scale={ppi}, timeout={timeout}ms) ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error capturing HTML to browser PNG:\n{result.stderr}")
        sys.exit(1)

    for line in result.stdout.strip().splitlines():
        if line.strip().startswith("->") or line.startswith("Done!"):
            print(f"  {line.strip()}")

    if not list(png_dir.glob("slide_*.png")):
        print("Error: browser renderer returned success but produced zero PNG slides")
        sys.exit(1)
    print(f"  Browser PNGs -> {png_dir}/")
    return png_dir


def step_png_to_overview(png_dir: Path, overview_path: Path,
                         max_width: int = 2000, max_height: int = 2000) -> Path:
    """Generate overview grid from existing PNG files."""
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow is required for browser overview generation. Install with: pip install Pillow")
        sys.exit(1)

    png_files = sorted(png_dir.glob("*.png"))
    if not png_files:
        print(f"Error: No PNG files found in {png_dir}")
        sys.exit(1)

    images = [Image.open(path).convert("RGB") for path in png_files]
    slide_w, slide_h = images[0].size

    best = None
    for cols in range(1, len(images) + 1):
        rows = ceil(len(images) / cols)
        scale = min(max_width / (cols * slide_w), max_height / (rows * slide_h), 1.0)
        area = (cols * slide_w * scale) * (rows * slide_h * scale)
        if best is None or area > best[0]:
            best = (area, cols, rows, scale)

    _, cols, rows, scale = best
    thumb_w = max(1, int(slide_w * scale))
    thumb_h = max(1, int(slide_h * scale))
    gap = max(4, int(8 * scale))
    canvas_w = cols * thumb_w + (cols - 1) * gap
    canvas_h = rows * thumb_h + (rows - 1) * gap
    overview = Image.new("RGB", (canvas_w, canvas_h), (200, 200, 200))

    for index, image in enumerate(images):
        row = index // cols
        col = index % cols
        thumb = image.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        overview.paste(thumb, (col * (thumb_w + gap), row * (thumb_h + gap)))

    overview_path.parent.mkdir(parents=True, exist_ok=True)
    if overview_path.is_dir():
        shutil.rmtree(overview_path)
    overview.save(overview_path)
    for image in images:
        image.close()
    print(f"  Overview -> {overview_path} ({overview_path.stat().st_size:,} bytes)")
    return overview_path


def step_svg_to_pptx(
    svg_dir: Path,
    pptx_path: Path,
    *,
    content_html: Path | None = None,
) -> Path:
    """Convert SVGs to editable PPTX shapes (MathJax remains raster images)."""
    print(f"Converting SVG to PPTX ...")

    try:
        from svg_to_pptx import create_pptx_with_native_svg
    except ImportError as e:
        print(f"Error importing svg_to_pptx: {e}")
        print("Make sure python-pptx is installed: pip install python-pptx")
        sys.exit(1)

    svg_files = list_svg_files(svg_dir)
    if not svg_files:
        print(f"Error: No SVG files found in {svg_dir}")
        sys.exit(1)

    notes = collect_slide_notes(content_html, svg_files) if content_html else None

    pptx_path.parent.mkdir(parents=True, exist_ok=True)

    success = create_pptx_with_native_svg(
        svg_files=svg_files,
        output_path=pptx_path,
        canvas_format=None,
        verbose=True,
        transition='fade',
        transition_duration=0.4,
        use_compat_mode=False,
        use_native_shapes=True,
        notes=notes,
        enable_notes=True,
        animation=None,
    )

    if success and pptx_path.exists() and pptx_path.stat().st_size > 0:
        print(f"  PPTX -> {pptx_path} ({pptx_path.stat().st_size:,} bytes)")
    else:
        remove_generated_path(pptx_path)
        print("Error: PPTX creation did not publish a new non-empty file")
        sys.exit(1)

    return pptx_path


def step_svg_to_pdf_browser(
    svg_dir: Path,
    pdf_path: Path,
    width: int = DEFAULT_CANVAS_WIDTH,
    height: int = DEFAULT_CANVAS_HEIGHT,
    timeout: int = 120_000,
) -> Path:
    """Combine per-slide SVGs into a vector PDF using Chromium."""
    browser_svg_to_pdf_script = SCRIPTS_DIR / "html_to_svg" / "browser_svg_to_pdf.mjs"
    if not browser_svg_to_pdf_script.exists():
        print(f"Error: browser_svg_to_pdf.mjs not found at {browser_svg_to_pdf_script}")
        sys.exit(1)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "node", str(browser_svg_to_pdf_script),
        str(svg_dir), "-o", str(pdf_path),
        "--width", str(width),
        "--height", str(height),
        "--timeout", str(timeout),
    ]

    print(f"Converting SVG to vector PDF with Chromium (canvas={width}x{height}, timeout={timeout}ms) ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error converting SVG to PDF with Chromium:\n{result.stderr}")
        sys.exit(1)

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        print("Error: PDF renderer returned success but produced no non-empty PDF")
        sys.exit(1)

    for line in result.stdout.strip().splitlines():
        if line.strip().startswith("->") or line.startswith("Done!"):
            print(f"  {line.strip()}")

    print(f"  PDF -> {pdf_path} ({pdf_path.stat().st_size:,} bytes)")
    return pdf_path


# ============================================================
# Project compilation
# ============================================================

def compile_project(
    project_path: Path,
    output_format: str = "all",
    output_path: str = None,
    ppi: float = 2.0,
    max_width: int = 2000,
    max_height: int = 2000,
    browser_timeout: int = 120_000,
    width: int | None = None,
    height: int | None = None,
    entry: str = "content.html",
    include_pptx: bool = False,
) -> dict:
    """
    Compile an HTML presentation project.

    The project directory must contain:
      - index-template.html  (the HTML shell with {{CONTENT}} placeholder)
      - <entry>              (content HTML, default: content.html)
      - template.css         (presentation styling, inlined by assembler)

    Args:
        project_path: Project directory
        output_format: 'svg', 'png', 'browser_png', 'pdf', 'pptx',
            'overview', or 'all'
        output_path: Custom output path (single format only)
        ppi: Pixels per inch for PNG output
        max_width: Max overview image width
        max_height: Max overview image height
        browser_timeout: Browser operation timeout for browser-backed rendering
        entry: Content HTML filename (default: content.html)

    Returns:
        Dictionary mapping format names to output paths
    """
    project_path = project_path.resolve()
    template_html = project_path / "index-template.html"
    content_html = (project_path / entry).resolve()
    try:
        entry = content_html.relative_to(project_path).as_posix()
    except ValueError as error:
        raise RuntimeError(f"entry must stay inside the project: {entry}") from error

    if not template_html.exists():
        print(f"Error: index-template.html not found in {project_path}")
        sys.exit(1)
    if not content_html.exists():
        print(f"Error: {entry} not found in {project_path}")
        sys.exit(1)

    output_dir = project_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    canvas_width, canvas_height, canvas_source = infer_canvas_size(project_path, width, height)
    print(f"Canvas: {canvas_width}x{canvas_height} ({canvas_source})")

    # Determine which formats to produce
    if output_format == "all":
        formats = ["svg", "png", "browser_png", "overview", "pdf"]
        if include_pptx:
            formats.append("pptx")
    else:
        formats = [output_format]

    # Validate every eventual publication location before creating staging
    # output or invoking a renderer.  This prevents --output from replacing a
    # receipt, assembled entrypoint, or another managed artifact.
    custom_format = formats[0] if output_path and len(formats) == 1 else None
    def planned_target(name: str, default: Path) -> Path:
        return resolve_output_target(project_path, output_path, default) if name == custom_format else default

    planned_targets = {
        "index": project_path / "index.html",
        "svg": planned_target("svg", output_dir / "svgs"),
        "dom_audit": output_dir / "dom-audit.json",
        "manifest": output_dir / "compile-manifest.json",
    }
    if "png" in formats:
        planned_targets["png"] = planned_target("png", output_dir / "pngs")
    if "browser_png" in formats:
        planned_targets["browser_png"] = planned_target("browser_png", output_dir / "browser_pngs")
    if "overview" in formats:
        planned_targets["overview"] = planned_target("overview", output_dir / "overview.png")
        if "png" not in formats:
            planned_targets["png_dependency"] = output_dir / "pngs"
    if "pdf" in formats:
        planned_targets["pdf"] = planned_target("pdf", output_dir / "slides.pdf")
    if "pptx" in formats:
        planned_targets["pptx"] = planned_target("pptx", output_dir / "slides.pptx")
    if "png" in formats and "browser_png" in formats:
        planned_targets["render_fidelity"] = output_dir / "render-fidelity.json"
    normalize_publish_targets(project_path, planned_targets)

    token = uuid.uuid4().hex[:12]
    staging_dir = output_dir / f".staging-{token}"
    staged_index = project_path / f".index-{token}.html"
    staging_dir.mkdir(parents=True, exist_ok=False)
    staged_artifacts: dict[str, tuple[Path, Path]] = {}
    results: dict[str, str] = {}

    def register(name: str, staged: Path, target: Path, *, visible: bool = True) -> None:
        staged_artifacts[name] = (staged, target)
        if visible:
            results[name] = str(target)

    try:
        # Build everything away from the last known-good output.  A failed
        # renderer must never erase or partially replace the prior delivery.
        step_assemble(template_html, content_html, staged_index)

        staged_svg_dir = staging_dir / "svgs"
        step_html_to_svg(
            staged_index,
            staged_svg_dir,
            width=canvas_width,
            height=canvas_height,
            timeout=browser_timeout,
        )
        check_svg_images_embedded(staged_svg_dir)
        svg_files = list_svg_files(staged_svg_dir)
        svg_numbers = verify_slide_roster(svg_files, "SVG export")
        verify_svg_canvas(svg_files, canvas_width, canvas_height)
        svg_target = planned_targets["svg"]
        register("svg", staged_svg_dir, svg_target)

        staged_dom_audit = staging_dir / "dom-audit.json"
        dom_audit = step_browser_dom_audit(
            staged_index,
            staged_dom_audit,
            width=canvas_width,
            height=canvas_height,
            timeout=browser_timeout,
        )
        if dom_audit.get("summary", {}).get("slideCount") != len(svg_numbers):
            raise RuntimeError(
                "browser DOM audit page count does not match the SVG export roster"
            )
        register("dom_audit", staged_dom_audit, output_dir / "dom-audit.json")
        dom_blocker_count = dom_audit["summary"]["blockerCount"]

        staged_png_dir: Path | None = None
        staged_browser_png_dir: Path | None = None
        for fmt in formats:
            if fmt == "svg":
                continue
            if fmt == "png":
                staged_png_dir = staging_dir / "pngs"
                target = planned_targets["png"]
                step_svg_to_png_browser(
                    staged_svg_dir,
                    staged_png_dir,
                    ppi=ppi,
                    width=canvas_width,
                    height=canvas_height,
                    timeout=browser_timeout,
                )
                verify_png_set(
                    staged_png_dir,
                    svg_numbers,
                    canvas_width,
                    canvas_height,
                    ppi,
                    "SVG-route PNG export",
                )
                register("png", staged_png_dir, target)
            elif fmt == "browser_png":
                staged = staging_dir / "browser_pngs"
                staged_browser_png_dir = staged
                target = planned_targets["browser_png"]
                step_html_to_png_browser(
                    staged_index,
                    staged,
                    ppi=ppi,
                    width=canvas_width,
                    height=canvas_height,
                    timeout=browser_timeout,
                )
                verify_png_set(
                    staged,
                    svg_numbers,
                    canvas_width,
                    canvas_height,
                    ppi,
                    "browser PNG export",
                )
                register("browser_png", staged, target)
            elif fmt == "overview":
                target = planned_targets["overview"]
                if staged_png_dir is None:
                    staged_png_dir = staging_dir / "pngs"
                    step_svg_to_png_browser(
                        staged_svg_dir,
                        staged_png_dir,
                        ppi=ppi,
                        width=canvas_width,
                        height=canvas_height,
                        timeout=browser_timeout,
                    )
                    verify_png_set(
                        staged_png_dir,
                        svg_numbers,
                        canvas_width,
                        canvas_height,
                        ppi,
                        "overview PNG dependency",
                    )
                    register(
                        "png_dependency",
                        staged_png_dir,
                        output_dir / "pngs",
                        visible=False,
                    )
                staged = staging_dir / "overview.png"
                step_png_to_overview(
                    staged_png_dir,
                    staged,
                    max_width=max_width,
                    max_height=max_height,
                )
                if not staged.exists() or staged.stat().st_size == 0:
                    raise RuntimeError("overview generation produced no non-empty file")
                register("overview", staged, target)
            elif fmt == "pdf":
                staged = staging_dir / "slides.pdf"
                target = planned_targets["pdf"]
                step_svg_to_pdf_browser(
                    staged_svg_dir,
                    staged,
                    width=canvas_width,
                    height=canvas_height,
                    timeout=browser_timeout,
                )
                register("pdf", staged, target)
            elif fmt == "pptx":
                staged = staging_dir / "slides.pptx"
                target = planned_targets["pptx"]
                step_svg_to_pptx(staged_svg_dir, staged, content_html=content_html)
                register("pptx", staged, target)

        render_fidelity = None
        if staged_png_dir is not None and staged_browser_png_dir is not None:
            staged_fidelity = staging_dir / "render-fidelity.json"
            render_fidelity = compare_render_routes(
                staged_png_dir,
                staged_browser_png_dir,
                staged_fidelity,
            )
            register(
                "render_fidelity",
                staged_fidelity,
                output_dir / "render-fidelity.json",
            )

        input_paths = [template_html, content_html]
        css_path = project_path / "template.css"
        if css_path.exists():
            input_paths.append(css_path)
        input_paths = sorted(set(input_paths + collect_local_dependencies(project_path, input_paths)))

        toolchain_paths = {
            SCRIPTS_DIR / "html_compiler.py",
            SCRIPTS_DIR / "runtime_environment.py",
            SCRIPTS_DIR / "assemble.py",
            SCRIPTS_DIR / "runtime" / "deck_runtime.js",
            SCRIPTS_DIR / "html_to_svg" / "browser_dom_to_svg.mjs",
            SCRIPTS_DIR / "html_to_svg" / "browser_dom_audit.mjs",
            SCRIPTS_DIR / "html_to_svg" / "chart_renderer.mjs",
            SCRIPTS_DIR / "html_to_svg" / "package.json",
            SCRIPTS_DIR / "html_to_svg" / "package-lock.json",
            SCRIPTS_DIR.parent / "requirements.txt",
        }
        if staged_png_dir is not None:
            toolchain_paths.add(SCRIPTS_DIR / "html_to_svg" / "browser_svg_to_png.mjs")
        if staged_browser_png_dir is not None:
            toolchain_paths.add(SCRIPTS_DIR / "html_to_svg" / "browser_html_to_png.mjs")
        if "pdf" in staged_artifacts:
            toolchain_paths.add(SCRIPTS_DIR / "html_to_svg" / "browser_svg_to_pdf.mjs")
        if "pptx" in staged_artifacts:
            toolchain_paths.add(SCRIPTS_DIR / "svg_to_pptx.py")
            # ``step_svg_to_pptx`` imports the package API, not just the legacy
            # wrapper above.  Fingerprint the implementation and its SVG
            # finalization helpers so a changed converter cannot inherit a
            # seemingly current delivery receipt.
            toolchain_paths.update(
                path for path in (SCRIPTS_DIR / "svg_to_pptx").rglob("*.py")
                if path.is_file()
            )
            toolchain_paths.update(
                path for path in (SCRIPTS_DIR / "svg_finalize").rglob("*.py")
                if path.is_file()
            )

        artifact_rows = []
        for name, (staged, target) in staged_artifacts.items():
            row = artifact_record(staged, staging_dir)
            row["name"] = name
            row["path"] = (
                str(target.relative_to(project_path))
                if target.is_relative_to(project_path)
                else str(target)
            )
            artifact_rows.append(row)

        manifest = {
            "schema": "seaslides-html-compile/v1",
            "status": "blocker" if dom_blocker_count else "pass",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "entry": entry,
            "format": output_format,
            "requested_formats": formats,
            "canvas": {
                "width": canvas_width,
                "height": canvas_height,
                "source": canvas_source,
                "png_scale": ppi,
            },
            "slide_count": len(svg_numbers),
            "quality": {
                "dom_audit": dom_audit["summary"],
                "render_fidelity": {
                    "status": render_fidelity["status"],
                    "review_slides": render_fidelity["review_slides"],
                } if render_fidelity else None,
            },
            "inputs": [
                {
                    "path": str(path.relative_to(project_path)),
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
                for path in input_paths
            ],
            "toolchain": [
                {
                    # Use one canonical namespace for every build dependency,
                    # including files such as requirements.txt that live at
                    # the skill root rather than under scripts/.
                    "path": path.relative_to(SKILL_ROOT).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
                for path in sorted(toolchain_paths)
                if path.is_file()
            ],
            "runtime_environment": runtime_environment_fingerprint(),
            "assembled_index_sha256": sha256_file(staged_index),
            "artifacts": artifact_rows,
        }
        staged_manifest = staging_dir / "compile-manifest.json"
        staged_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        publish_pairs = [(staged_index, project_path / "index.html")]
        publish_pairs.extend(staged_artifacts.values())
        publish_pairs.append((staged_manifest, output_dir / "compile-manifest.json"))
        normalize_publish_targets(
            project_path,
            {f"publish_{index}": target for index, (_staged, target) in enumerate(publish_pairs)},
        )
        publish_atomically(publish_pairs, token)
    finally:
        staged_index.unlink(missing_ok=True)
        if staging_dir.exists():
            shutil.rmtree(staging_dir)

    # Summary
    print(f"\n{'='*60}")
    print(f"Compilation complete!")
    print(f"{'='*60}")
    print(f"  Project:  {project_path}")
    print(f"  Output:   {output_dir}/")
    for fmt, path in results.items():
        print(f"  {fmt:>8s}: {path}")

    if dom_blocker_count:
        raise RuntimeError(
            f"DOM quality gate found {dom_blocker_count} blocker(s); complete artifacts "
            "were published with status='blocker' for visual diagnosis"
        )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Compile HTML presentation projects to SVG, PNG, browser PNG, PDF, PPTX, or overview grid",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 html_compiler.py ./my-project --all                # SVG + PNG + browser_png + overview + PDF
  python3 html_compiler.py ./my-project --format png
  python3 html_compiler.py ./my-project --format browser-png # Direct browser screenshots
  python3 html_compiler.py ./my-project --format pdf         # Vector PDF
  python3 html_compiler.py ./my-project --all --include-pptx # Delivery build + PPTX receipt
  python3 html_compiler.py ./my-project --format pptx        # Diagnostic/non-standard single-format export
  python3 html_compiler.py ./my-project --format overview
  python3 html_compiler.py ./my-project --entry demo.html    # Template development
        """,
    )

    parser.add_argument(
        "project_path",
        help="Path to the project directory containing index-template.html + content HTML",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["svg", "png", "browser-png", "pdf", "pptx", "overview", "all"],
        default="all",
        help="Output format (default: all = svg + png + browser_png + overview + pdf; single formats are diagnostic/non-standard for delivery)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Custom output path (for single format only)",
        default=None,
    )
    parser.add_argument(
        "--ppi",
        type=float,
        default=2.0,
        help="Pixels per inch for PNG output (default: 2.0 = retina)",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=2000,
        help="Max overview image width in pixels (default: 2000)",
    )
    parser.add_argument(
        "--max-height",
        type=int,
        default=2000,
        help="Max overview image height in pixels (default: 2000)",
    )
    parser.add_argument(
        "--browser-timeout",
        type=int,
        default=120_000,
        help="Browser operation timeout for HTML/SVG rendering in ms (default: 120000)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Browser canvas width in pixels. Overrides CSS --slide-width/height metadata.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Browser canvas height in pixels. Overrides CSS --slide-width/height metadata.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Compile the synchronized SVG, PNG, browser_png, overview, and PDF build (add --include-pptx for delivery)",
    )
    parser.add_argument(
        "--include-pptx",
        action="store_true",
        help="Include PPTX in the same atomic --all build and delivery receipt",
    )
    parser.add_argument(
        "--entry",
        default="content.html",
        help="Content HTML filename (default: content.html). Use --entry demo.html for template dev.",
    )
    args = parser.parse_args()

    if args.all and args.format != "all":
        parser.error("--all cannot be combined with an explicit --format")
    if args.include_pptx and not (args.all or args.format == "all"):
        parser.error("--include-pptx requires --all or --format all")
    if args.output and (args.all or args.format == "all"):
        parser.error("--output is only valid for a single output format")
    if args.ppi <= 0:
        parser.error("--ppi must be greater than zero")
    if args.browser_timeout <= 0:
        parser.error("--browser-timeout must be greater than zero")
    if (args.width is None) != (args.height is None):
        parser.error("--width and --height must be provided together")
    if args.width is not None and (args.width <= 0 or args.height <= 0):
        parser.error("--width and --height must be greater than zero")

    project_path = Path(args.project_path).expanduser().resolve()
    if not project_path.exists():
        print(f"Error: Project directory not found: {project_path}")
        sys.exit(1)

    output_format = "all" if args.all else args.format.replace("-", "_")
    try:
        results = compile_project(
            project_path, output_format, args.output, args.ppi,
            max_width=args.max_width, max_height=args.max_height,
            browser_timeout=args.browser_timeout,
            width=args.width,
            height=args.height,
            entry=args.entry,
            include_pptx=args.include_pptx,
        )
    except (OSError, RuntimeError, ET.ParseError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    if len(results) > 1:
        print(f"\nAll {len(results)} format(s) compiled successfully!")


if __name__ == "__main__":
    main()
