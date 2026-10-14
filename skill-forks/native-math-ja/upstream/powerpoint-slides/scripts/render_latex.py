#!/usr/bin/env python3
"""Batch LaTeX formula renderer: JSON → transparent PNG (or SVG) images.

Usage:
  python render_latex.py formulas.json output_dir/                  # PNG @ 600 DPI (default)
  python render_latex.py formulas.json output_dir/ --dpi 900        # PNG @ custom DPI
  python render_latex.py formulas.json output_dir/ --format svg     # SVG (needs ghostscript)

Input JSON: [{"id": "f01", "latex": "E=mc^2", "mode": "display", "fg_color": "1A1A2E", "scale": 1.0}, ...]
Output: output_dir/f01.png (or .svg), ... + output_dir/manifest.json
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

LATEX_TEMPLATE = r"""\documentclass[border=2pt]{{standalone}}
\usepackage{{amsmath,amssymb,amsthm,mathtools,stmaryrd}}
\usepackage{{xcolor}}
\definecolor{{positive}}{{HTML}}{{0173B2}}
\definecolor{{negative}}{{HTML}}{{DE8F05}}
\definecolor{{emphasis}}{{HTML}}{{029E73}}
\definecolor{{neutral}}{{gray}}{{0.55}}
\definecolor{{fgcolor}}{{HTML}}{{{fg_color}}}
\begin{{document}}
\color{{fgcolor}}
{content}
\end{{document}}
"""

DEFAULT_DPI = 600


def _has_ghostscript() -> bool:
    """Check if ghostscript is available (needed by dvisvgm --pdf)."""
    for cmd in ("gs", "gswin64c", "gswin32c"):
        try:
            subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return False


def _compile_to_cropped_pdf(formula: dict, tmpdir: str) -> tuple[str | None, str | None]:
    """Compile LaTeX to cropped PDF. Returns (cropped_pdf_path, error_msg)."""
    fid = formula["id"]
    latex = formula["latex"]
    mode = formula.get("mode", "display")
    fg = formula.get("fg_color", "1A1A2E")

    if mode == "inline":
        content = f"${latex}$"
    elif mode == "paragraph":
        content = latex  # raw LaTeX — caller handles math mode, minipage, etc.
    else:
        content = f"\\[ {latex} \\]"
    tex_src = LATEX_TEMPLATE.format(fg_color=fg, content=content)

    tex_path = os.path.join(tmpdir, f"{fid}.tex")
    pdf_path = os.path.join(tmpdir, f"{fid}.pdf")
    cropped_path = os.path.join(tmpdir, f"{fid}-crop.pdf")

    with open(tex_path, "w") as f:
        f.write(tex_src)

    r = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
        capture_output=True, text=True, timeout=30,
    )
    if not os.path.exists(pdf_path):
        tail = (r.stderr or r.stdout or "")[-500:]
        return None, f"xelatex failed: {tail}"

    r2 = subprocess.run(
        ["pdfcrop", pdf_path, cropped_path],
        capture_output=True, text=True, timeout=15,
    )
    if r2.returncode != 0 or not os.path.exists(cropped_path):
        cropped_path = pdf_path
    return cropped_path, None


def _render_png(fid: str, cropped_pdf: str, outdir: Path, tmpdir: str, dpi: int) -> dict:
    """Convert cropped PDF to transparent PNG."""
    png_prefix = os.path.join(tmpdir, f"{fid}-out")
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), "-singlefile", cropped_pdf, png_prefix],
        capture_output=True, timeout=15,
    )
    tmp_png = f"{png_prefix}.png"
    if not os.path.exists(tmp_png):
        return {"id": fid, "error": "pdftoppm failed to produce PNG"}

    final = outdir / f"{fid}.png"
    if Image:
        img = Image.open(tmp_png).convert("RGBA")
        pixels = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                if r > 240 and g > 240 and b > 240:
                    pixels[x, y] = (r, g, b, 0)
        img.save(str(final))
    else:
        import shutil
        shutil.copy2(tmp_png, str(final))
        w, h = 0, 0

    return {"id": fid, "file": str(final), "format": "png", "width_px": w, "height_px": h, "dpi": dpi}


def _render_svg(fid: str, cropped_pdf: str, outdir: Path) -> dict:
    """Convert cropped PDF to SVG via dvisvgm."""
    final = outdir / f"{fid}.svg"
    r = subprocess.run(
        ["dvisvgm", "--pdf", "--no-fonts", "--exact-bbox", cropped_pdf, "-o", str(final)],
        capture_output=True, text=True, timeout=15,
    )
    if r.returncode != 0 or not final.exists():
        return {"id": fid, "error": f"dvisvgm failed: {(r.stderr or r.stdout or '')[-300:]}"}

    # Extract dimensions from SVG viewBox or width/height attributes
    svg_text = final.read_text()[:2000]
    w_pt, h_pt = 0.0, 0.0
    # Try width="...pt" height="...pt"
    wm = re.search(r'width="([0-9.]+)pt"', svg_text)
    hm = re.search(r'height="([0-9.]+)pt"', svg_text)
    if wm and hm:
        w_pt, h_pt = float(wm.group(1)), float(hm.group(1))
    else:
        # Try viewBox
        vb = re.search(r'viewBox="[0-9.\-]+ [0-9.\-]+ ([0-9.]+) ([0-9.]+)"', svg_text)
        if vb:
            w_pt, h_pt = float(vb.group(1)), float(vb.group(2))

    return {"id": fid, "file": str(final), "format": "svg", "width_pt": w_pt, "height_pt": h_pt}


def render_one(formula: dict, outdir: Path, tmpdir: str, fmt: str, dpi: int) -> dict:
    """Render a single formula. Returns manifest entry."""
    fid = formula["id"]
    render_mode = formula.get("render", "auto")
    mode = formula.get("mode", "display")

    # Auto-resolve: paragraph → image, else → omml
    if render_mode == "auto":
        render_mode = "image" if mode == "paragraph" else "omml"

    if render_mode == "omml":
        return {"id": fid, "render": "omml", "latex": formula["latex"]}

    ext = "svg" if fmt == "svg" else "png"

    # Incremental: skip if already rendered
    final = outdir / f"{fid}.{ext}"
    if final.exists():
        if ext == "png" and Image:
            img = Image.open(str(final))
            w, h = img.size
            return {"id": fid, "file": str(final), "format": "png", "width_px": w, "height_px": h, "dpi": dpi}
        elif ext == "svg":
            svg_text = final.read_text()[:2000]
            wm = re.search(r'width="([0-9.]+)pt"', svg_text)
            hm = re.search(r'height="([0-9.]+)pt"', svg_text)
            w_pt = float(wm.group(1)) if wm else 0.0
            h_pt = float(hm.group(1)) if hm else 0.0
            return {"id": fid, "file": str(final), "format": "svg", "width_pt": w_pt, "height_pt": h_pt}
        return {"id": fid, "file": str(final), "format": ext}

    cropped_pdf, err = _compile_to_cropped_pdf(formula, tmpdir)
    if err:
        return {"id": fid, "error": err}

    if fmt == "svg":
        return _render_svg(fid, cropped_pdf, outdir)
    return _render_png(fid, cropped_pdf, outdir, tmpdir, dpi)


def main():
    parser = argparse.ArgumentParser(description="Batch LaTeX formula renderer")
    parser.add_argument("formulas", help="Path to formulas.json")
    parser.add_argument("outdir", help="Output directory")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI, help=f"PNG resolution (default: {DEFAULT_DPI})")
    parser.add_argument("--format", choices=["png", "svg"], default="png", dest="fmt",
                        help="Output format (default: png). SVG requires ghostscript.")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.fmt == "svg" and not _has_ghostscript():
        print("WARNING: ghostscript not found, falling back to PNG", file=sys.stderr)
        args.fmt = "png"

    with open(args.formulas) as f:
        formulas = json.load(f)

    manifest = {}
    errors = []

    with tempfile.TemporaryDirectory(prefix="render_latex_") as tmpdir:
        for formula in formulas:
            result = render_one(formula, outdir, tmpdir, args.fmt, args.dpi)
            fid = result.pop("id")
            if "error" in result:
                errors.append(f"  {fid}: {result['error']}")
            manifest[fid] = result

    manifest_path = outdir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Rendered {len(formulas) - len(errors)}/{len(formulas)} formulas → {outdir}/ ({args.fmt}@{args.dpi}dpi)")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
