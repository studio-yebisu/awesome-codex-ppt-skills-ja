#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REFERENCE_LIBRARY = [
    {
        "id": "zh-finished-swiss-grid-systems",
        "tags": ["business", "grid", "analysis", "swiss", "clean"],
        "palette": ["F7F4EA", "111111", "D43F2A", "D3CCB8"],
        "typography": {"heading": "DengXian / Microsoft YaHei UI", "body": "Microsoft YaHei UI"},
        "grid": {"columns": 12, "axis": "left", "safe_margin": "strong"},
        "spacing": {"density": "medium", "rhythm": "strict"},
        "layout_rhythm": ["cover low density", "content medium density", "data with insight", "quiet closing"],
        "image_treatment": ["masked editorial crop", "tinted monochrome treatment"],
        "chart_treatment": ["comparison-bar", "trend-line"],
    },
    {
        "id": "zh-finished-global-ai-capital-2026",
        "tags": ["business", "data", "technology", "capital"],
        "palette": ["F5F7FA", "121826", "1D4ED8", "D6DFEA"],
        "typography": {"heading": "Microsoft YaHei UI", "body": "Microsoft YaHei UI"},
        "grid": {"columns": 12, "axis": "left"},
        "spacing": {"density": "medium-high"},
        "layout_rhythm": ["insight pages", "chart hero", "kpi row"],
        "image_treatment": ["atmospheric background with overlay"],
        "chart_treatment": ["chart-with-insight", "kpi-cards"],
    },
    {
        "id": "zh-finished-brutalist-ai-newspaper-2026",
        "tags": ["editorial", "bold", "news", "high-contrast"],
        "palette": ["F4F1EA", "111111", "C2410C", "D7CCB9"],
        "typography": {"heading": "DengXian / Microsoft YaHei UI", "body": "Microsoft YaHei UI"},
        "grid": {"columns": 12, "axis": "asymmetric-left"},
        "spacing": {"density": "low-to-medium"},
        "layout_rhythm": ["statement hero", "quote editorial", "strong divider"],
        "image_treatment": ["full-bleed hero", "masked editorial crop"],
        "chart_treatment": ["minimal annotated charts"],
    },
    {
        "id": "zh-template-thu",
        "tags": ["academic", "university", "template", "formal"],
        "palette": ["FAFAF7", "1C1917", "8A3B12", "D8CEC0"],
        "typography": {"heading": "Microsoft YaHei UI / SimSun", "body": "Microsoft YaHei UI / SimSun"},
        "grid": {"columns": 12, "axis": "template-placeholder"},
        "spacing": {"density": "medium"},
        "layout_rhythm": ["formal cover", "section divider", "content with evidence"],
        "image_treatment": ["restrained crop"],
        "chart_treatment": ["formal comparison-bar"],
    },
    {
        "id": "zh-finished-home-design-trends-2026",
        "tags": ["warm", "education", "lifestyle", "friendly"],
        "palette": ["F7FBF5", "1F2933", "2F855A", "CFE0CF"],
        "typography": {"heading": "Microsoft YaHei UI", "body": "Microsoft YaHei UI"},
        "grid": {"columns": 12, "axis": "soft-left"},
        "spacing": {"density": "medium", "whitespace": "generous"},
        "layout_rhythm": ["low-density cover", "visual explanation", "three point summary"],
        "image_treatment": ["soft editorial crop", "image grid"],
        "chart_treatment": ["progress", "timeline"],
    },
]


def select_refs(topic: str, style: str) -> tuple[dict, dict, dict]:
    text = f"{topic} {style}".lower()
    scored = []
    for ref in REFERENCE_LIBRARY:
        score = sum(1 for tag in ref["tags"] if tag in text)
        if any(word in text for word in ["高校", "学术", "课件", "教师", "education", "academic"]) and "academic" in ref["tags"]:
            score += 3
        if any(word in text for word in ["数据", "经营", "季度", "复盘", "data"]) and "data" in ref["tags"]:
            score += 3
        if any(word in text for word in ["商务", "产业链", "趋势", "analysis", "business"]) and "business" in ref["tags"]:
            score += 3
        if any(word in text for word in ["产品", "发布", "高端", "editorial", "bold"]) and "editorial" in ref["tags"]:
            score += 2
        scored.append((score, ref["id"], ref))
    scored.sort(reverse=True)
    primary = scored[0][2]
    typography = scored[1][2] if len(scored) > 1 else primary
    layout = next((r for _, _, r in scored if "data" in r["tags"] or "grid" in r["tags"]), primary)
    return primary, typography, layout


def write_montage(board: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1500, 760), "white")
    draw = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.truetype("msyh.ttc", 36)
        body_font = ImageFont.truetype("msyh.ttc", 24)
        small_font = ImageFont.truetype("msyh.ttc", 18)
    except Exception:
        title_font = body_font = small_font = ImageFont.load_default()
    draw.text((60, 48), "Reference Board", fill=(20, 20, 20), font=title_font)
    labels = [
        ("Primary", board["primary_reference"]),
        ("Typography", board["typography_reference"]),
        ("Layout / Chart", board["layout_or_chart_reference"]),
    ]
    x = 60
    for i, (label, ref) in enumerate(labels):
        y = 128 + i * 182
        draw.rounded_rectangle((x, y, 1420, y + 138), radius=10, outline=(210, 210, 210), fill=(248, 248, 246), width=2)
        draw.text((x + 28, y + 22), label, fill=(90, 90, 90), font=small_font)
        draw.text((x + 28, y + 56), ref, fill=(20, 20, 20), font=body_font)
        palette = board["design_dna"]["palette"]
        for j, color in enumerate(palette):
            c = color if color.startswith("#") else f"#{color}"
            draw.rectangle((x + 980 + j * 80, y + 40, x + 1038 + j * 80, y + 98), fill=c, outline=(180, 180, 180))
    img.save(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="")
    parser.add_argument("--style", default="")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    primary, typo, layout = select_refs(args.topic, args.style)
    board = {
        "primary_reference": primary["id"],
        "typography_reference": typo["id"],
        "layout_or_chart_reference": layout["id"],
        "why_selected": [
            f"Primary reference matches topic/style cues: {args.topic} {args.style}".strip(),
            "Typography reference provides Chinese-first hierarchy and readable projection sizes.",
            "Layout/chart reference provides grid, density, and data treatment discipline.",
        ],
        "design_dna": {
            "palette": primary["palette"],
            "typography": typo["typography"],
            "grid": primary["grid"],
            "spacing": primary["spacing"],
            "layout_rhythm": primary["layout_rhythm"],
            "image_treatment": primary["image_treatment"],
            "chart_treatment": layout["chart_treatment"],
        },
        "must_not_copy": [
            "Do not copy source text.",
            "Do not copy logos or brand marks.",
            "Do not copy protected images.",
            "Do not reproduce page layouts one-to-one.",
        ],
        "adaptation_notes": [
            "Use palette as semantic roles, not literal branding.",
            "Use typography scale and grid rhythm to guide original slides.",
            "Adapt chart treatment to the new topic and data.",
        ],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "reference_board.json").write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# Reference Board", ""]
    for key in ["primary_reference", "typography_reference", "layout_or_chart_reference"]:
        md.append(f"- `{key}`: `{board[key]}`")
    md.extend(["", "## Design DNA", "", json.dumps(board["design_dna"], ensure_ascii=False, indent=2), "", "## Must Not Copy", ""])
    md.extend(f"- {item}" for item in board["must_not_copy"])
    (args.output_dir / "reference_board.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    write_montage(board, args.output_dir / "reference_board_montage.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
