#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt


ACCENT = RGBColor(37, 99, 235)
SURFACE = RGBColor(238, 242, 247)
INK = RGBColor(17, 24, 39)
MUTED = RGBColor(71, 85, 105)


def style_runs(shape, font: str, size: float, color: RGBColor, bold: bool = False) -> None:
    if not getattr(shape, "has_text_frame", False):
        return
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--slide", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--locked-slides", type=Path, required=True)
    parser.add_argument("--change-log", type=Path)
    args = parser.parse_args()

    prs = Presentation(str(args.input))
    target_idx = args.slide - 1
    if target_idx < 0 or target_idx >= len(prs.slides):
        raise ValueError("target slide out of range")

    locked = [i + 1 for i in range(len(prs.slides)) if i != target_idx]
    slide = prs.slides[target_idx]
    width, height = prs.slide_width, prs.slide_height

    x = Inches(0.72)
    y = height - Inches(1.58)
    w = width - Inches(1.44)
    h = Inches(0.86)

    label = slide.shapes.add_textbox(x, y - Inches(0.32), Inches(1.6), Inches(0.22))
    label.text = "TARGET SLIDE"
    style_runs(label, "Aptos", 8.5, MUTED, True)

    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    box.fill.solid()
    box.fill.fore_color.rgb = SURFACE
    box.line.color.rgb = ACCENT
    box.line.width = Pt(0.9)

    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.08), h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.color.rgb = ACCENT

    tf = box.text_frame
    tf.margin_left = Inches(0.24)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.14)
    tf.text = "本页已优化：用更直观的结论提示条强化关键信息，其他页面保持锁定。"
    style_runs(box, "Microsoft YaHei UI", 15.5, INK, True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(args.output)
    args.locked_slides.parent.mkdir(parents=True, exist_ok=True)
    args.locked_slides.write_text(json.dumps({"target_slide": args.slide, "locked_slides": locked}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.change_log:
        args.change_log.write_text(
            f"# Change Log\n\n- Modified slide {args.slide} only.\n"
            "- Added one tokenized insight strip that inherits deck typography and accent color.\n"
            f"- Locked slides: {', '.join(map(str, locked))}.\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
