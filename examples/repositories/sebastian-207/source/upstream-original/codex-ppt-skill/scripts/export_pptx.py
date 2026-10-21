#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


def find_soffice() -> str | None:
    for name in ("soffice.com", "soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for p in (
        Path("C:/Program Files/LibreOffice/program/soffice.com"),
        Path("C:/Program Files/LibreOffice/program/soffice.exe"),
        Path("C:/Program Files (x86)/LibreOffice/program/soffice.com"),
        Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
    ):
        if p.exists():
            return str(p)
    return None


def pdf_to_pngs(pdf: Path, outdir: Path, prefix: str = "slide") -> list[str]:
    doc = fitz.open(pdf)
    paths: list[str] = []
    for idx, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        out = outdir / f"{prefix}_{idx:02d}.png"
        pix.save(out)
        paths.append(str(out))
    doc.close()
    return paths


def make_montage(pngs: list[str], out: Path) -> None:
    if not pngs:
        return
    thumbs = []
    for p in pngs:
        img = Image.open(p).convert("RGB")
        img.thumbnail((420, 236))
        thumbs.append((p, img.copy()))
        img.close()
    cols = min(3, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * 460, rows * 296), "white")
    draw = ImageDraw.Draw(canvas)
    for i, (p, img) in enumerate(thumbs):
        x = (i % cols) * 460 + 20
        y = (i // cols) * 296 + 20
        canvas.paste(img, (x, y))
        draw.text((x, y + img.height + 8), Path(p).stem, fill=(60, 60, 60))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--outdir", "-o", type=Path, default=Path("preview"))
    parser.add_argument("--pdf-name", default="final.pdf")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"input": str(args.pptx), "outdir": str(args.outdir), "pdf": None, "png": [], "montage": None, "warnings": [], "errors": []}
    if not args.pptx.exists():
        report["errors"].append("PPTX not found.")
    soffice = find_soffice()
    if not soffice:
        report["errors"].append("LibreOffice/soffice not found.")
    if not report["errors"]:
        try:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(args.outdir), str(args.pptx)], check=True, capture_output=True, text=True, timeout=120)
            generated = args.outdir / f"{args.pptx.stem}.pdf"
            target_pdf = args.outdir / args.pdf_name
            if generated.exists():
                if generated.resolve() != target_pdf.resolve():
                    if target_pdf.exists():
                        target_pdf.unlink()
                    generated.rename(target_pdf)
                report["pdf"] = str(target_pdf)
                report["png"] = pdf_to_pngs(target_pdf, args.outdir)
                montage = args.outdir / "montage.png"
                make_montage(report["png"], montage)  # type: ignore[arg-type]
                report["montage"] = str(montage)
            else:
                report["errors"].append("LibreOffice completed but PDF was not found.")
        except Exception as exc:
            report["errors"].append(f"LibreOffice export failed: {exc}")
    report_path = args.report or (args.outdir / "render_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if not report["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
