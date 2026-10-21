#!/usr/bin/env python3
"""Deprecated diagnostic HTML-to-PPTX pipeline.

Converts an assembled HTML presentation to PPTX via SVG intermediary.

For standard delivery, use ``html_compiler.py <project> --all --include-pptx``.
This legacy command does not produce the synchronized build receipt.

Pipeline steps:
  1. (Optional) Run assemble.py to merge template + content -> index.html
  2. Run browser_dom_to_svg.mjs to convert index.html -> per-slide SVG files
  3. Run svg_to_pptx (create_pptx_with_native_svg) to convert SVGs -> PPTX
  4. Run browser_svg_to_png.mjs to convert SVGs -> PNGs for visual verification

Usage:
    # From assembled index.html:
    python3 html_to_pptx.py <index.html> -o <output_dir>

    # From index-template + content (auto-assemble, inlines CSS):
    python3 html_to_pptx.py --template <index-template.html> --content <content.html> -o <output_dir>

    # Minimal (just input, output defaults to same directory):
    python3 html_to_pptx.py examples/sample/index.html
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Ensure scripts directory is on sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))


def run_assemble(template: Path, content: Path, output: Path) -> Path:
    """Run assemble.py to merge template + content."""
    assemble_script = SCRIPTS_DIR / "assemble.py"
    if not assemble_script.exists():
        print(f"Error: assemble.py not found at {assemble_script}")
        raise RuntimeError(f"assemble.py not found at {assemble_script}")

    cmd = [
        sys.executable, str(assemble_script),
        str(template), str(content),
        "-o", str(output),
    ]
    print(f"\n{'='*60}")
    print(f"Step 1: Assembling HTML")
    print(f"  Template: {template}")
    print(f"  Content:  {content}")
    print(f"  Output:   {output}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error assembling HTML: {result.stderr}")
        raise RuntimeError(result.stderr.strip() or "HTML assembly failed")
    print(result.stdout.strip())
    return output


def run_html_to_svg(input_html: Path, output_dir: Path) -> Path:
    """Run browser_dom_to_svg.mjs to convert HTML to per-slide SVGs."""
    html_to_svg_script = SCRIPTS_DIR / "html_to_svg" / "browser_dom_to_svg.mjs"
    if not html_to_svg_script.exists():
        print(f"Error: browser_dom_to_svg.mjs not found at {html_to_svg_script}")
        raise RuntimeError(f"browser_dom_to_svg.mjs not found at {html_to_svg_script}")

    cmd = [
        "node", str(html_to_svg_script),
        str(input_html),
        "-o", str(output_dir),
    ]
    print(f"\n{'='*60}")
    print(f"Step 2: Converting HTML to SVG (browser DOM)")
    print(f"  Input:  {input_html}")
    print(f"  Output: {output_dir}/")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error converting HTML to SVG:")
        print(result.stderr)
        raise RuntimeError(result.stderr.strip() or "HTML to SVG conversion failed")
    print(result.stdout.strip())
    return output_dir


def run_svg_to_pptx(svg_dir: Path, output_pptx: Path) -> Path:
    """Convert SVGs to PPTX using svg_to_pptx package."""
    print(f"\n{'='*60}")
    print(f"Step 3: Converting SVG to PPTX")
    print(f"  SVG dir:  {svg_dir}/")
    print(f"  Output:   {output_pptx}")
    print(f"{'='*60}")

    try:
        from svg_to_pptx import create_pptx_with_native_svg
    except ImportError as e:
        print(f"Error importing svg_to_pptx: {e}")
        print("Make sure python-pptx is installed: pip install python-pptx")
        raise RuntimeError("svg_to_pptx import failed") from e

    # Find all SVG files in the directory
    svg_files = sorted(svg_dir.glob("*.svg"))
    if not svg_files:
        print(f"Error: No SVG files found in {svg_dir}")
        raise RuntimeError(f"No SVG files found in {svg_dir}")

    print(f"  Found {len(svg_files)} SVG files")

    # Create output directory
    output_pptx.parent.mkdir(parents=True, exist_ok=True)

    # Use native shapes mode to convert SVG elements into DrawingML shapes.
    # This produces higher-quality output with editable text and scalable graphics.
    success = create_pptx_with_native_svg(
        svg_files=svg_files,
        output_path=output_pptx,
        canvas_format=None,  # Auto-detect from SVG viewBox
        verbose=True,
        transition='fade',
        transition_duration=0.4,
        use_compat_mode=False,  # Skip PNG compatibility (no svglib needed)
        use_native_shapes=True,  # Use native DrawingML shapes
        animation=None,  # No animation for simplicity
    )

    if success and output_pptx.is_file() and output_pptx.stat().st_size > 0:
        print(f"  PPTX created: {output_pptx} ({output_pptx.stat().st_size:,} bytes)")
    else:
        raise RuntimeError("PPTX creation did not produce a non-empty file")

    return output_pptx


def run_svg_to_png(svg_dir: Path, png_dir: Path) -> Path:
    """Convert SVGs to PNGs using Chromium."""
    svg_to_png_script = SCRIPTS_DIR / "html_to_svg" / "browser_svg_to_png.mjs"
    if not svg_to_png_script.exists():
        raise RuntimeError(f"browser_svg_to_png.mjs not found at {svg_to_png_script}")

    cmd = [
        "node", str(svg_to_png_script),
        str(svg_dir),
        "-o", str(png_dir),
        "--scale", "2",
    ]
    print(f"\n{'='*60}")
    print(f"Step 4: Converting SVG to PNG (visual verification)")
    print(f"  SVG dir:  {svg_dir}/")
    print(f"  PNG dir:  {png_dir}/")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "SVG to PNG conversion failed")
    if not any(png_dir.glob("*.png")):
        raise RuntimeError("SVG to PNG conversion produced no PNG files")
    print(result.stdout.strip())

    return png_dir


def main():
    parser = argparse.ArgumentParser(
        description="HTML to PPTX Pipeline - Convert HTML presentations to PowerPoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # From pre-assembled index.html:
    python3 html_to_pptx.py examples/sample/index.html -o output/

    # From template + content (auto-assemble):
    python3 html_to_pptx.py --template templates/minimal.html \\
                            --content examples/sample/content.html \\
                            -o output/

    # Skip PNG generation:
    python3 html_to_pptx.py examples/sample/index.html --no-png
        """,
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="Path to assembled index.html file",
    )
    parser.add_argument(
        "--template",
        help="Path to template HTML file (for auto-assembly)",
    )
    parser.add_argument(
        "--content",
        help="Path to content HTML file (for auto-assembly)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: same directory as input)",
    )
    parser.add_argument(
        "--no-png",
        action="store_true",
        help="Skip PNG generation step",
    )
    parser.add_argument(
        "--no-pptx",
        action="store_true",
        help="Skip PPTX generation step (SVGs only)",
    )

    args = parser.parse_args()

    # Determine input file
    assemble_inputs: tuple[Path, Path] | None = None
    if args.template and args.content:
        # Auto-assemble mode
        template = Path(args.template).resolve()
        content = Path(args.content).resolve()
        if not template.exists():
            print(f"Error: Template not found: {template}")
            sys.exit(1)
        if not content.exists():
            print(f"Error: Content not found: {content}")
            sys.exit(1)

        # Determine output directory
        if args.output:
            output_dir = Path(args.output).resolve()
        else:
            output_dir = content.parent / "output"

        output_dir.mkdir(parents=True, exist_ok=True)
        input_html = output_dir / "index.html"

        assemble_inputs = (template, content)

    elif args.input:
        input_html = Path(args.input).resolve()
        if not input_html.exists():
            print(f"Error: Input file not found: {input_html}")
            sys.exit(1)

        if args.output:
            output_dir = Path(args.output).resolve()
        else:
            output_dir = input_html.parent / "output"

        output_dir.mkdir(parents=True, exist_ok=True)

    else:
        parser.print_help()
        sys.exit(1)

    try:
        if assemble_inputs is not None:
            run_assemble(*assemble_inputs, input_html)
        # Step 2: HTML to SVG
        svg_dir = output_dir / "svg_output"
        run_html_to_svg(input_html, svg_dir)

        # Step 3: SVG to PPTX
        if not args.no_pptx:
            pptx_path = output_dir / "presentation.pptx"
            run_svg_to_pptx(svg_dir, pptx_path)

        # Step 4: SVG to PNG
        if not args.no_png:
            png_dir = output_dir / "pngs"
            run_svg_to_png(svg_dir, png_dir)
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Summary
    print(f"\n{'='*60}")
    print(f"Diagnostic pipeline complete!")
    print(f"{'='*60}")
    print(f"  Output directory: {output_dir}/")
    print(f"  SVGs:  {svg_dir}/")
    if not args.no_pptx:
        print(f"  PPTX:  {output_dir / 'presentation.pptx'}")
    if not args.no_png:
        print(f"  PNGs:  {output_dir / 'pngs/'}")


if __name__ == "__main__":
    main()
