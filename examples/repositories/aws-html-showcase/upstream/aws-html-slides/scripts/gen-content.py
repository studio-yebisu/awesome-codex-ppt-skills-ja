#!/usr/bin/env python3
"""Generate content.md template based on page count and language.

Usage:
    python scripts/gen-content.py <page_count> [output_path] [--lang en|zh]

Examples:
    python scripts/gen-content.py 8
    python scripts/gen-content.py 15 my-project/content.md --lang zh
"""

import sys
import argparse
from pathlib import Path

# --- Language strings ---

HEADER = {
    "en": [
        "# Presentation Title",
        "",
        "> Fill in each slide below. For media, reference files in the `### media` section.",
        "> Supported formats: .png .jpg .gif .mp4 .webm",
        "> One slide can have multiple media files, one per line.",
        ">",
        "> **Media file referencing** — any of these formats work:",
        "> - Paste/drop image directly into this md file (IDE will auto-generate a path)",
        "> - Relative path from current directory: `images/screenshot.png`",
        "> - Absolute path: `/Users/name/Desktop/photo.png`",
        ">",
        "> All referenced media will be automatically copied into the presentation's assets/ folder.",
        ">",
        "> ---",
        ">",
        "> **Chart** (optional): Add `### chart` in any slide. Supported types:",
        ">   `line` | `bar` | `doughnut` | `pie` | `radar` | `polarArea`",
        ">",
        ">   Format:",
        ">   ```",
        ">   ### chart",
        ">   type: bar",
        ">   labels: Q1, Q2, Q3, Q4",
        ">   Revenue ($M): 12, 18, 25, 31",
        ">   Cost ($M): 8, 10, 12, 15",
        ">   ```",
        ">",
        "> **Table** (optional): Add `### table` in any slide, use markdown table syntax:",
        ">   ```",
        ">   ### table",
        ">   | Feature | Basic | Pro |",
        ">   |---------|-------|-----|",
        ">   | Storage | 10GB  | 1TB |",
        ">   ```",
        ">",
        "> **Diagram** (optional): Add `### diagram` in any slide. Flowcharts, sequence,",
        ">   UML/ER, network, mind maps and architecture are drawn as native animated SVG",
        ">   (no install needed; supports flowing request packets and an isometric-3D look).",
        ">   Only `type: aws` (official AWS icons) uses the drawio skill and requires the",
        ">   draw.io desktop CLI (`brew install --cask drawio`).",
        ">   `type:` (optional) one of: `flowchart` | `sequence` | `class` | `er` | `network` | `mindmap` | `arch` | `aws`",
        ">   `animate:` (optional) `flow` (packets, default) | `static` | `none`",
        ">",
        ">   Format:",
        ">   ```",
        ">   ### diagram",
        ">   type: sequence",
        ">   caption: One API request, end to end",
        ">   Client -> API Gateway: POST /orders",
        ">   API Gateway -> Lambda: Invoke",
        ">   Lambda -> DynamoDB: PutItem",
        ">   DynamoDB --> Client: 201 Created",
        ">   ```",
    ],
    "zh": [
        "# 演示文稿标题",
        "",
        "> 请在下方填写每页幻灯片的内容。媒体文件请在 `### media` 区域中引用。",
        "> 支持格式：.png .jpg .gif .mp4 .webm",
        "> 每页可引用多个媒体文件，每行一个。",
        ">",
        "> **媒体文件引用方式**（以下格式均可）：",
        "> - 直接在此 md 文件中粘贴/拖入图片（IDE 会自动生成路径）",
        "> - 相对路径：`images/screenshot.png`",
        "> - 绝对路径：`/Users/name/Desktop/photo.png`",
        ">",
        "> 所有引用的媒体文件会自动复制到演示文稿的 assets/ 目录中。",
        ">",
        "> ---",
        ">",
        "> **图表**（可选）：在任意幻灯片中添加 `### chart`。支持的图表类型：",
        ">   `line`（折线图）| `bar`（柱状图）| `doughnut`（环形图）| `pie`（饼图）| `radar`（雷达图）| `polarArea`（极区图）",
        ">",
        ">   格式：",
        ">   ```",
        ">   ### chart",
        ">   type: bar",
        ">   labels: 一季度, 二季度, 三季度, 四季度",
        ">   营收 (百万): 12, 18, 25, 31",
        ">   成本 (百万): 8, 10, 12, 15",
        ">   ```",
        ">",
        "> **表格**（可选）：在任意幻灯片中添加 `### table`，使用 markdown 表格语法：",
        ">   ```",
        ">   ### table",
        ">   | 功能   | 基础版 | 专业版 |",
        ">   |--------|--------|--------|",
        ">   | 存储   | 10GB   | 1TB    |",
        ">   ```",
        ">",
        "> **图表/架构图**（可选）：在任意幻灯片中添加 `### diagram`。流程图、时序图、",
        ">   UML/ER 图、网络拓扑、思维导图和架构图均以原生动画 SVG 直接绘制在幻灯片中",
        ">   （无需安装任何工具；支持请求包沿连线流动动画和等轴测 3D 架构效果）。",
        ">   仅 `type: aws`（官方 AWS 服务图标）走 drawio skill，需要安装",
        ">   draw.io 桌面版 CLI（`brew install --cask drawio`）。",
        ">   `type:`（可选）取值：`flowchart`（流程图）| `sequence`（时序图）| `class`（类图）| `er`（ER 图）| `network`（网络图）| `mindmap`（思维导图）| `arch`（架构图）| `aws`（AWS 架构图）",
        ">   `animate:`（可选）`flow`（数据包流动，默认）| `static`（仅入场）| `none`",
        ">",
        ">   格式：",
        ">   ```",
        ">   ### diagram",
        ">   type: sequence",
        ">   caption: 一次 API 请求的完整流转",
        ">   客户端 -> API 网关: POST /orders",
        ">   API 网关 -> Lambda: Invoke",
        ">   Lambda -> DynamoDB: PutItem",
        ">   DynamoDB --> 客户端: 201 Created",
        ">   ```",
    ],
}

SLIDE_TITLE = {
    "en": {
        "title_heading": "(your title)",
        "title_subtitle": "(your subtitle)",
        "closing_heading": "(Thank You / Q&A)",
        "closing_subtitle": "(closing message or URL)",
        "section_heading": "(heading text)",
        "body_points": ["(point 1)", "(point 2)", "(point 3)"],
        "optional": "(optional)",
        "slide": "Slide",
        "title": "Title",
        "closing": "Closing",
        "section": "Section",
    },
    "zh": {
        "title_heading": "(你的标题)",
        "title_subtitle": "(你的副标题)",
        "closing_heading": "(谢谢 / Q&A)",
        "closing_subtitle": "(结束语或链接)",
        "section_heading": "(标题文字)",
        "body_points": ["(要点 1)", "(要点 2)", "(要点 3)"],
        "optional": "(可选)",
        "slide": "幻灯片",
        "title": "标题页",
        "closing": "结束页",
        "section": "章节",
    },
}


def generate_content_md(page_count: int, lang: str = "en") -> str:
    t = SLIDE_TITLE[lang]
    lines = list(HEADER[lang])
    lines.append("")

    for i in range(1, page_count + 1):
        lines.append("---")
        lines.append("")

        if i == 1:
            lines.append(f"## {t['slide']} {i:02d}: {t['title']}")
            lines.append("type: title")
            lines.append("")
            lines.append("### heading")
            lines.append(t["title_heading"])
            lines.append("")
            lines.append("### subtitle")
            lines.append(t["title_subtitle"])
            lines.append("")
            lines.append("### media")
            lines.append(t["optional"])
        elif i == page_count:
            lines.append(f"## {t['slide']} {i:02d}: {t['closing']}")
            lines.append("type: title")
            lines.append("")
            lines.append("### heading")
            lines.append(t["closing_heading"])
            lines.append("")
            lines.append("### subtitle")
            lines.append(t["closing_subtitle"])
            lines.append("")
            lines.append("### media")
            lines.append(t["optional"])
        else:
            lines.append(f"## {t['slide']} {i:02d}: {t['section']} {i - 1}")
            lines.append("type: content")
            lines.append("")
            lines.append("### heading")
            lines.append(t["section_heading"])
            lines.append("")
            lines.append("### body")
            for pt in t["body_points"]:
                lines.append(f"- {pt}")
            lines.append("")
            lines.append("### media")
            lines.append(t["optional"])

        lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate content.md template")
    parser.add_argument("page_count", type=int, help="Number of slides")
    parser.add_argument("output", nargs="?", default="content.md", help="Output path")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="Language")
    args = parser.parse_args()

    content = generate_content_md(args.page_count, args.lang)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(content, encoding="utf-8")
    print(f"Generated {args.output} with {args.page_count} slides (lang={args.lang})")


if __name__ == "__main__":
    main()
