#!/usr/bin/env python3
"""Generate the public qiaomu-bento-ppt product-introduction deck JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "qiaomu-bento-ppt-intro.json"

W, H = 1280, 720
INK = "#101115"
PAPER = "#F3EEE5"
CORAL = "#FF6B4A"
LIME = "#D9F06B"
BLUE = "#5B7CFF"
MUTED = "#A8A49D"
WHITE = "#FFFFFF"
FONT = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif"


def text(
    element_id: str,
    x: float,
    y: float,
    w: float,
    h: float,
    html: str,
    font_size: float,
    color: str,
    *,
    weight: int = 500,
    align: str = "left",
    valign: str = "top",
    line_height: float = 1.1,
    rotation: float = 0,
    opacity: float = 1,
    letter_spacing: float | None = None,
    fx: dict[str, Any] | None = None,
    link: str | None = None,
    role: str | None = None,
) -> dict[str, Any]:
    element: dict[str, Any] = {
        "id": element_id,
        "type": "text",
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "rotation": rotation,
        "opacity": opacity,
        "html": html,
        "fontSize": max(font_size, 18),
        "fontFamily": FONT,
        "fontWeight": weight,
        "color": color,
        "align": align,
        "valign": valign,
        "lineHeight": line_height,
    }
    if letter_spacing is not None:
        element["letterSpacing"] = letter_spacing
    if fx:
        element["fx"] = fx
    if link:
        element["link"] = link
    if role:
        element["role"] = role
    return element


def shape(
    element_id: str,
    kind: str,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    *,
    stroke: str = "transparent",
    stroke_width: float = 0,
    radius: float = 0,
    rotation: float = 0,
    opacity: float = 1,
    gradient: dict[str, Any] | None = None,
    shadow: dict[str, Any] | list[dict[str, Any]] | None = None,
    fx: dict[str, Any] | None = None,
    link: str | None = None,
    d: str | None = None,
    path_box: list[float] | None = None,
    line_end: str | None = None,
) -> dict[str, Any]:
    element: dict[str, Any] = {
        "id": element_id,
        "type": "shape",
        "shape": kind,
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "rotation": rotation,
        "opacity": opacity,
        "fill": fill,
        "stroke": stroke,
        "strokeWidth": stroke_width,
        "radius": radius,
    }
    if gradient:
        element["fillGradient"] = gradient
    if shadow:
        element["shadow"] = shadow
    if fx:
        element["fx"] = fx
    if link:
        element["link"] = link
    if d is not None:
        element["d"] = d
    if path_box is not None:
        element["pathBox"] = path_box
    if line_end:
        element["lineEnd"] = line_end
    return element


def pill(element_id: str, x: float, y: float, w: float, label: str, fill: str, color: str) -> list[dict[str, Any]]:
    return [
        shape(f"{element_id}-bg", "rect", x, y, w, 38, fill, radius=19),
        text(element_id, x, y + 1, w, 36, label, 15, color, weight=750, align="center", valign="middle", letter_spacing=0.8),
    ]


def footer(slide_no: str, *, light: bool = False) -> list[dict[str, Any]]:
    color = INK if light else PAPER
    return [
        text("brand-mark", 72, 34, 260, 32, "qiaomu / bento ppt", 15, color, weight=750, letter_spacing=1.1),
        text("page-chip", 1120, 34, 88, 32, slide_no, 15, color, weight=750, align="right", letter_spacing=1.2),
    ]


def slide(
    slide_id: str,
    background: str,
    elements: list[dict[str, Any]],
    notes: str,
    *,
    transition: str = "morph",
    name: str | None = None,
    state_of: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": slide_id,
        "background": background,
        "transition": transition,
        "elements": elements,
        "notes": notes,
    }
    if name:
        result["name"] = name
    if state_of:
        result["stateOf"] = state_of
    return result


def build() -> dict[str, Any]:
    soft_shadow = {"x": 0, "y": 18, "blur": 32, "color": "rgba(0,0,0,0.24)"}
    paper_shadow = {"x": 0, "y": 14, "blur": 30, "color": "rgba(16,17,21,0.16)"}

    s1 = slide(
        "s1-cover",
        INK,
        [
            shape("cover-orb", "ellipse", 930, 72, 270, 270, CORAL, opacity=0.95, shadow={"x": 0, "y": 0, "blur": 60, "color": "rgba(255,107,74,0.35)"}),
            shape("cover-ring", "ellipse", 982, 124, 166, 166, "transparent", stroke=LIME, stroke_width=3),
            shape("motion-dot", "ellipse", 1016, 222, 26, 26, LIME, fx={"loop": {"type": "motion-path", "path": "M0 0 C80 -96 168 -96 230 0 C168 96 80 96 0 0", "duration": 9}}),
            *footer("01 / 07"),
            text("hero-kicker", 72, 126, 500, 40, "AGENT SKILL · PRODUCT DECK", 18, LIME, weight=800, letter_spacing=2.2, fx={"enter": "fade-up", "order": 0}),
            text("hero-word", 72, 188, 790, 260, "不是一堆<br><b>静态文字页。</b>", 96, PAPER, weight=550, line_height=0.98, fx={"enter": "fade-up", "order": 1}, role="title"),
            text("hero-sub", 76, 474, 720, 82, "是一份会动、会验证、可以直接交付的 deck。", 28, MUTED, weight=500, line_height=1.35, fx={"enter": "fade-up", "order": 2}),
            shape("tile-plan", "rect", 840, 426, 150, 92, PAPER, radius=20, rotation=-6, shadow=soft_shadow, fx={"enter": "slide-left", "order": 3}),
            text("tile-plan-label", 840, 440, 150, 60, "PLAN", 24, INK, weight=850, align="center", valign="middle", rotation=-6),
            shape("tile-author", "rect", 1008, 388, 170, 104, BLUE, radius=22, rotation=5, shadow=soft_shadow, fx={"enter": "slide-left", "order": 4}),
            text("tile-author-label", 1008, 408, 170, 60, "AUTHOR", 23, WHITE, weight=850, align="center", valign="middle", rotation=5),
            shape("tile-gate", "rect", 922, 526, 152, 94, LIME, radius=20, rotation=4, shadow=soft_shadow, fx={"enter": "slide-up", "order": 5}),
            text("tile-gate-label", 922, 543, 152, 60, "GATE", 24, INK, weight=850, align="center", valign="middle", rotation=4),
        ],
        "开场先打破对 AI PPT 的预期：这不是一个帮你写 bullet 的 prompt，而是一条能生成真实、可编辑、可演示文件的工作流。",
        transition="none",
        name="Cover",
    )

    s2 = slide(
        "s2-flip",
        PAPER,
        [
            *footer("02 / 07", light=True),
            text("hero-kicker", 72, 112, 500, 38, "THE DEFAULT FAILURE", 17, CORAL, weight=800, letter_spacing=2),
            text("hero-word", 72, 164, 500, 160, "AI PPT<br><b>的惯性：写满。</b>", 62, INK, weight=520, line_height=1.02),
            text("wall-copy", 76, 360, 470, 180, "观点一、观点二、观点三……<br>信息没有主次，每一页都像文档截图。", 23, "#6F6B65", weight=450, line_height=1.55),
            shape("result-panel", "rect", 650, 116, 558, 500, INK, radius=34, shadow=paper_shadow),
            text("result-kicker", 700, 164, 420, 32, "THE WORKING RESULT", 16, LIME, weight=800, letter_spacing=1.8),
            text("result-title", 700, 214, 420, 150, "第一屏<br><b>就能工作。</b>", 62, PAPER, weight=520, line_height=1.02),
            text("result-copy", 700, 398, 400, 90, "可编辑 · 可演示 · 可保存<br>一个文件，直接交付。", 24, MUTED, weight=520, line_height=1.45),
            shape("tile-plan", "rect", 1048, 520, 100, 58, CORAL, radius=15, rotation=0),
            text("tile-plan-label", 1048, 520, 100, 58, "DECK", 16, WHITE, weight=850, align="center", valign="middle", rotation=0),
        ],
        "成品的标准不是“文字生成了”，而是用户打开第一屏就能编辑、演示和保存。这也是乔木 skill 的成品线。",
        name="The flip",
    )

    connector = shape(
        "pipeline-path",
        "path",
        132,
        330,
        1016,
        70,
        "transparent",
        stroke="rgba(243,238,229,0.32)",
        stroke_width=3,
        d="M0 35 C180 5 270 65 430 35 C600 5 720 65 1016 35",
        path_box=[0, 0, 1016, 70],
        fx={"loop": {"type": "dash-march", "distance": 24, "duration": 1.8}},
    )
    s3_elements: list[dict[str, Any]] = [
        *footer("03 / 07"),
        text("hero-kicker", 72, 112, 500, 38, "ONE SENTENCE → ONE FILE", 17, LIME, weight=800, letter_spacing=2),
        text("hero-word", 72, 160, 980, 90, "从一句话，到一个文件。", 62, PAPER, weight=620),
        connector,
    ]
    stages = [
        ("brief", "BRIEF", "说清目标", PAPER, INK),
        ("plan", "PLAN", "先定叙事", CORAL, WHITE),
        ("author", "AUTHOR", "映射能力", BLUE, WHITE),
        ("gate", "GATE", "验证交付", LIME, INK),
        ("deck", ".BENTO", "打开就用", PAPER, INK),
    ]
    for index, (key, title_label, sub_label, fill, color) in enumerate(stages):
        x = 88 + index * 238
        s3_elements.extend([
            shape(f"stage-{key}", "rect", x, 288, 184, 150, fill, radius=28, shadow=soft_shadow),
            text(f"stage-{key}-title", x, 320, 184, 50, title_label, 24, color, weight=900, align="center", valign="middle", letter_spacing=1.2),
            text(f"stage-{key}-sub", x + 18, 382, 148, 28, sub_label, 16, color, weight=650, align="center", opacity=0.78),
        ])
    s3_elements.extend([
        text("pipeline-foot", 72, 536, 800, 72, "proposal-first 不是多一步。<br><b>它是防止平庸成品的第一道 gate。</b>", 25, MUTED, weight=500, line_height=1.4),
        shape("tile-author", "rect", 1050, 535, 120, 72, BLUE, radius=18, rotation=0),
        text("tile-author-label", 1050, 535, 120, 72, "FLOW", 19, WHITE, weight=850, align="center", valign="middle", rotation=0),
    ])
    s3 = slide(
        "s3-flow",
        INK,
        s3_elements,
        "这条路径的核心是：先用可审阅的 plan 解决叙事，再用 bento 原生能力 author，最后用确定性 gate 交付文件。",
        name="Workflow",
    )

    s4 = slide(
        "s4-map",
        PAPER,
        [
            *footer("04 / 07", light=True),
            text("hero-kicker", 72, 104, 540, 36, "CONTENT → NATIVE CAPABILITY", 17, CORAL, weight=800, letter_spacing=2),
            text("hero-word", 72, 150, 900, 86, "内容不是 bullet 的原料。", 58, INK, weight=650),
            shape("map-a", "rect", 72, 270, 548, 164, INK, radius=30),
            text("map-a-title", 108, 300, 210, 48, "数字", 30, PAPER, weight=800),
            text("map-a-arrow", 310, 300, 72, 48, "→", 32, CORAL, weight=800, align="center"),
            text("map-a-value", 390, 300, 190, 48, "CHART", 27, LIME, weight=900, align="right", letter_spacing=1.5),
            text("map-a-sub", 108, 366, 420, 34, "趋势 · 量级 · 占比", 18, MUTED, weight=600),
            shape("map-b", "rect", 660, 270, 548, 164, BLUE, radius=30),
            text("map-b-title", 696, 300, 210, 48, "对比", 30, WHITE, weight=800),
            text("map-b-arrow", 898, 300, 72, 48, "→", 32, LIME, weight=800, align="center"),
            text("map-b-value", 978, 300, 190, 48, "TABLE", 27, WHITE, weight=900, align="right", letter_spacing=1.5),
            text("map-b-sub", 696, 366, 420, 34, "规格 · 价格 · 选项", 18, "rgba(255,255,255,0.72)", weight=600),
            shape("map-c", "rect", 72, 464, 548, 164, CORAL, radius=30),
            text("map-c-title", 108, 494, 210, 48, "变化", 30, WHITE, weight=800),
            text("map-c-arrow", 310, 494, 72, 48, "→", 32, INK, weight=800, align="center"),
            text("map-c-value", 390, 494, 190, 48, "MORPH", 27, WHITE, weight=900, align="right", letter_spacing=1.5),
            text("map-c-sub", 108, 560, 420, 34, "前后 · 步骤 · 聚焦", 18, "rgba(255,255,255,0.75)", weight=600),
            shape("map-d", "rect", 660, 464, 548, 164, LIME, radius=30),
            text("map-d-title", 696, 494, 210, 48, "深度", 30, INK, weight=800),
            text("map-d-arrow", 898, 494, 72, 48, "→", 32, BLUE, weight=800, align="center"),
            text("map-d-value", 978, 494, 190, 48, "STATE", 27, INK, weight=900, align="right", letter_spacing=1.5),
            text("map-d-sub", 696, 560, 420, 34, "展开 · 交互 · 不打断", 18, "rgba(16,17,21,0.66)", weight=650),
        ],
        "同一种表达不应该对付所有内容。数字应该成为图表，规格应该成为表格，变化应该用 morph，次级深度放进 state。",
        name="Capability map",
    )

    proof_table = {
        "id": "proof-table",
        "type": "table",
        "x": 640,
        "y": 216,
        "w": 568,
        "h": 366,
        "rotation": 0,
        "opacity": 1,
        "header": True,
        "columns": [{"w": 1.25}, {"w": 1.7}, {"w": 0.8}],
        "rows": [
            {"cells": [{"html": "GATE"}, {"html": "EVIDENCE"}, {"html": "RESULT", "align": "right"}]},
            {"cells": [{"html": "Route"}, {"html": "14 trigger cases"}, {"html": "PASS", "align": "right", "bold": True}]},
            {"cells": [{"html": "Standalone"}, {"html": "bundled shell"}, {"html": "TRUE", "align": "right", "bold": True}]},
            {"cells": [{"html": "Identity"}, {"html": "new + edit paths"}, {"html": "PASS", "align": "right", "bold": True}]},
            {"cells": [{"html": "Remote"}, {"html": "clean npx install"}, {"html": "PASS", "align": "right", "bold": True}]},
        ],
        "style": {
            "headerBg": CORAL,
            "headerColor": WHITE,
            "zebra": "rgba(243,238,229,0.06)",
            "borderColor": "rgba(243,238,229,0.14)",
            "borderWidth": 1,
            "cellPadX": 20,
            "cellPadY": 15,
            "fontSize": 18,
            "fontFamily": FONT,
            "color": PAPER,
            "radius": 20,
        },
    }
    s5 = slide(
        "s5-proof",
        INK,
        [
            *footer("05 / 07"),
            text("proof-kicker", 72, 106, 520, 38, "EVIDENCE, NOT PROMISES", 17, LIME, weight=800, letter_spacing=2),
            text("proof-title", 72, 154, 500, 150, "不是承诺。<br><b>是通过的门禁。</b>", 58, PAPER, weight=540, line_height=1.05),
            text("proof-number", 72, 344, 320, 120, "14/14", 94, CORAL, weight=900, fx={"countUp": True, "enter": "fade-up", "order": 0}),
            text("proof-label", 78, 468, 380, 40, "TRIGGER ROUTES PASSED", 16, MUTED, weight=800, letter_spacing=1.6),
            text("proof-copy", 76, 544, 470, 70, "脚本负责机械正确；<br>真实浏览器负责视觉正确。", 22, PAPER, weight=500, line_height=1.4),
            proof_table,
        ],
        "所有公开声明都要回到证据。路由、独立性、文档身份和远程安装已经有确定性证据；视觉效果则必须用真实浏览器验收。",
        transition="fade",
        name="Evidence",
    )

    s6 = slide(
        "s6-file",
        PAPER,
        [
            *footer("06 / 07", light=True),
            text("file-kicker", 72, 104, 480, 36, "THE FILE IS THE PRODUCT", 17, CORAL, weight=800, letter_spacing=2),
            text("file-title", 72, 150, 720, 80, "一个文件，就是交付。", 58, INK, weight=650),
            shape("file-card", "rect", 170, 278, 940, 280, INK, radius=38, shadow=paper_shadow, link="s6-detail"),
            shape("file-fold", "triangle", 968, 278, 142, 122, PAPER, rotation=90, opacity=0.94, link="s6-detail"),
            text("file-ext", 226, 326, 650, 100, ".bento.html", 74, PAPER, weight=850, valign="middle", link="s6-detail"),
            text("file-hint", 230, 446, 660, 38, "CLICK TO OPEN THE CONTRACT", 16, LIME, weight=800, letter_spacing=1.8, link="s6-detail"),
            *pill("file-edit", 226, 500, 132, "EDIT", CORAL, WHITE),
            *pill("file-present", 374, 500, 150, "PRESENT", BLUE, WHITE),
            *pill("file-save", 540, 500, 132, "SAVE", LIME, INK),
            text("file-foot", 948, 594, 260, 32, "data + runtime + editor", 16, "#6F6B65", weight=700, align="right", letter_spacing=0.6),
        ],
        "一份 bento deck 不需要一个另外的 app 去打开。文件本身已经包含数据、运行时和编辑器。点击文件卡可展开内部契约。",
        name="One file",
    )

    s6_state = slide(
        "s6-detail",
        INK,
        [
            *footer("06 / DETAIL"),
            text("file-kicker", 72, 104, 480, 36, "INSIDE THE FILE", 17, LIME, weight=800, letter_spacing=2),
            text("file-title", 72, 150, 780, 80, "文件内部，是三层契约。", 56, PAPER, weight=650),
            shape("file-card", "rect", 72, 276, 1136, 310, "#191B21", radius=34, stroke="rgba(243,238,229,0.13)", stroke_width=1, link="s6-file"),
            shape("detail-data", "rect", 112, 324, 316, 214, CORAL, radius=28, link="s6-file"),
            text("detail-data-title", 144, 354, 250, 56, "DATA", 30, WHITE, weight=900, letter_spacing=1.5, link="s6-file"),
            text("detail-data-copy", 144, 426, 250, 80, "plaintext JSON<br>stable docId", 21, WHITE, weight=550, line_height=1.4, link="s6-file"),
            shape("detail-runtime", "rect", 482, 324, 316, 214, BLUE, radius=28, link="s6-file"),
            text("detail-runtime-title", 514, 354, 250, 56, "RUNTIME", 30, WHITE, weight=900, letter_spacing=1.5, link="s6-file"),
            text("detail-runtime-copy", 514, 426, 250, 80, "viewer + motion<br>works offline", 21, WHITE, weight=550, line_height=1.4, link="s6-file"),
            shape("detail-editor", "rect", 852, 324, 316, 214, LIME, radius=28, link="s6-file"),
            text("detail-editor-title", 884, 354, 250, 56, "EDITOR", 30, INK, weight=900, letter_spacing=1.5, link="s6-file"),
            text("detail-editor-copy", 884, 426, 250, 80, "open + edit + save<br>inside the file", 21, INK, weight=600, line_height=1.4, link="s6-file"),
            text("detail-close", 964, 616, 244, 30, "CLICK ANY CARD TO RETURN", 14, MUTED, weight=750, align="right", letter_spacing=0.8, link="s6-file"),
        ],
        "这个 state 不占用线性叙事的篇幅，但需要的观众可以主动展开。Data 保持可读，runtime 保证离线演示，editor 让文件可以自己编辑自己。",
        name="Inside the file",
        state_of="s6-file",
    )

    s7 = slide(
        "s7-cta",
        CORAL,
        [
            *footer("07 / 07", light=True),
            shape("cta-orb", "ellipse", 930, 90, 250, 250, LIME, opacity=0.92, shadow={"x": 0, "y": 0, "blur": 60, "color": "rgba(217,240,107,0.35)"}),
            shape("cta-ring", "ellipse", 982, 142, 146, 146, "transparent", stroke=INK, stroke_width=3),
            text("cta-kicker", 72, 118, 500, 38, "INSTALL · SAY IT · SHIP IT", 17, INK, weight=850, letter_spacing=2),
            text("cta-title", 72, 174, 900, 170, "一行安装。<br><b>一句话开做。</b>", 78, WHITE, weight=560, line_height=1.02),
            shape("cta-code-bg", "rect", 72, 404, 1010, 92, INK, radius=24, shadow=soft_shadow),
            text("cta-code", 108, 418, 938, 64, "npx skills add joeseesun/qiaomu-bento-ppt", 26, LIME, weight=750, valign="middle", letter_spacing=0.15),
            text("cta-prompt", 76, 548, 900, 54, "“把这份报告做成 12 页离线 bento 演示文稿。”", 25, INK, weight=650),
            text("cta-url", 76, 622, 720, 36, "github.com/joeseesun/qiaomu-bento-ppt", 18, "rgba(16,17,21,0.66)", weight=750, letter_spacing=0.4),
            shape("tile-gate", "rect", 1040, 552, 126, 76, LIME, radius=20, rotation=-4, shadow=soft_shadow),
            text("tile-gate-label", 1040, 552, 126, 76, "SHIP", 20, INK, weight=900, align="center", valign="middle", rotation=-4),
        ],
        "收束时不再重复功能清单。只给两个行动：一行安装，一句自然语言开始。",
        transition="zoom",
        name="Install",
    )

    return {
        "format": "bento/slides",
        "version": 1,
        "docId": "7c8c3dd9-39d7-4e0c-8d88-188594a5046d",
        "title": "qiaomu-bento-ppt — 从资料到会动的单文件 deck",
        "meta": {
            "author": "向阳乔木",
            "company": "Qiaomu AI",
            "subject": "qiaomu-bento-ppt product introduction",
            "keywords": "bento, agent skill, presentation, qiaomu",
        },
        "size": {"width": W, "height": H},
        "theme": {
            "background": INK,
            "color": PAPER,
            "accent": CORAL,
            "fontFamily": FONT,
            "chartPalette": [CORAL, BLUE, LIME, PAPER],
        },
        "present": {"slideNumber": False, "controls": False, "progress": False},
        "slides": [s1, s2, s3, s4, s5, s6, s6_state, s7],
        "modified": "2026-07-26T00:00:00Z",
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
