#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches
from pptx.util import Pt


ACCENT = RGBColor(37, 99, 235)
INK = RGBColor(17, 24, 39)
MUTED = RGBColor(71, 85, 105)
LINE = RGBColor(214, 222, 232)


def polish_shape(shape, is_title: bool = False) -> None:
    if not getattr(shape, "has_text_frame", False):
        return
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            run.font.name = "Microsoft YaHei UI"
            if run.font.size is None:
                run.font.size = Pt(27 if is_title else 17)
            elif is_title and run.font.size.pt < 24:
                run.font.size = Pt(27)
            elif not is_title and 9 < run.font.size.pt < 15:
                run.font.size = Pt(15)
            if run.font.size and run.font.size.pt > 9:
                run.font.color.rgb = INK if is_title else MUTED
            if is_title:
                run.font.bold = True


def add_deck_structure(slide, idx: int, total: int, width, height) -> None:
    left = Inches(0.58)
    right = width - Inches(0.58)
    top = Inches(0.95)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, right - left, Pt(0.7))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE
    line.line.color.rgb = LINE
    if idx % 4 == 0:
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.0), Inches(0.0), Inches(0.08), height)
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT
        bar.line.color.rgb = ACCENT
    footer = slide.shapes.add_textbox(width - Inches(1.35), height - Inches(0.42), Inches(0.75), Inches(0.18))
    footer.text = f"{idx + 1:02d}/{total:02d}"
    for p in footer.text_frame.paragraphs:
        for r in p.runs:
            r.font.name = "Aptos"
            r.font.size = Pt(8)
            r.font.color.rgb = MUTED


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--change-plan", type=Path)
    parser.add_argument("--change-log", type=Path)
    args = parser.parse_args()
    if not args.input.exists():
        raise FileNotFoundError(args.input)
    prs = Presentation(str(args.input))
    title_y_threshold = Inches(1.15)
    for idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            is_title = getattr(shape, "top", 0) < title_y_threshold and getattr(shape, "has_text_frame", False)
            polish_shape(shape, is_title=is_title)
        add_deck_structure(slide, idx, len(prs.slides), prs.slide_width, prs.slide_height)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(args.output)
    design_dna = {
        "typography": {"heading": "Microsoft YaHei UI", "body": "Microsoft YaHei UI", "number": "Aptos"},
        "grid": {"safe_margin": "0.58in", "title_axis": "top"},
        "palette": ["F7F8FA", "111827", "2563EB", "D6DEE8"],
        "change_policy": "visual polish only; core meaning preserved",
    }
    (args.output.parent.parent / "design_dna.json").write_text(json.dumps(design_dna, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.change_plan:
        args.change_plan.write_text("# Change Plan\n\n- Scope: full deck visual polish.\n- Core content: preserved.\n- Facts/data: unchanged.\n- Typography, color hierarchy, stable guide lines, and footer rhythm are normalized.\n- Output: edited_final.pptx.\n", encoding="utf-8")
    if args.change_log:
        args.change_log.write_text("# Change Log\n\n- Applied Chinese-first font normalization to editable text runs.\n- Added restrained deck structure using accent hairlines and stable page numbers.\n- Preserved slide order, text meaning, pictures, charts, and data.\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
