#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rebuild the repository posters with a cleaner layout and real PPT thumbnails."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "assets" / "gallery"
POSTERS = ROOT / "assets" / "posters"
POSTERS.mkdir(parents=True, exist_ok=True)

REPO_NAME = "Paper2ScholarSlides"
REPO_URL = "https://github.com/ficooooo/Paper2ScholarSlides"

INTRO_SHORT = "将综述初稿、论文资料与既有模板整理为结构清楚、图表可溯、公式可讲、页面可复核的学术汇报。"
SUBTITLE = "学术综述与科研汇报 PPT 构建 Skill"
CHIPS = ["Review-to-Deck", "Figure Notes", "Layout QA"]
FEATURES = [
    ("综述重构", "把章节材料改写为真正适合口头汇报的页面叙事。", "#2B6CB0"),
    ("图表可讲", "关键图不只展示，还保留来源、作用与读图重点。", "#1F8A70"),
    ("公式可读", "变量、物理意义与适用边界可同步进入讲解。", "#D97706"),
    ("导出核查", "统一检查溢出、遮挡、低清与错误占位文本。", "#D64550"),
]
WORKFLOW = ["Sources", "Structure", "Slides", "QA"]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    return ImageFont.truetype(path, size)


def rgb(color: str) -> tuple[int, int, int]:
    return ImageColor.getrgb(color)


def rgba(color: str, alpha: int) -> tuple[int, int, int, int]:
    r, g, b = rgb(color)
    return (r, g, b, alpha)


def gradient(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
    width, height = size
    canvas = Image.new("RGBA", size)
    t = rgb(top)
    b = rgb(bottom)
    px = canvas.load()
    for y in range(height):
        ratio = y / max(1, height - 1)
        c = tuple(int(t[i] * (1 - ratio) + b[i] * ratio) for i in range(3)) + (255,)
        for x in range(width):
            px[x, y] = c
    return canvas


def add_bg_shapes(base: Image.Image) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = base.size
    draw.ellipse((w - 720, -120, w + 160, 560), fill=rgba("#CFE3FF", 56))
    draw.ellipse((-180, h - 540, 520, h + 120), fill=rgba("#DCEAF9", 80))
    draw.rounded_rectangle((w - 980, h - 280, w - 120, h - 120), radius=72, fill=rgba("#FFFFFF", 120))
    overlay = overlay.filter(ImageFilter.GaussianBlur(20))
    base.alpha_composite(overlay)


def rounded_panel(
    base: Image.Image,
    box: tuple[int, int, int, int],
    fill: str = "#FFFFFF",
    outline: str = "#D7E4F1",
    radius: int = 30,
    shadow: bool = True,
) -> None:
    x1, y1, x2, y2 = box
    if shadow:
        shadow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow_layer)
        sdraw.rounded_rectangle((x1 + 8, y1 + 12, x2 + 8, y2 + 12), radius=radius, fill=(8, 28, 52, 22))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(14))
        base.alpha_composite(shadow_layer)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    use_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            trial = current + ch
            width = draw.textbbox((0, 0), trial, font=use_font)[2]
            if width <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    use_font: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_gap: int = 8,
) -> int:
    x, y = xy
    h = 0
    for line in wrap_text(draw, text, use_font, max_width):
        draw.text((x, y + h), line, font=use_font, fill=fill)
        bbox = draw.textbbox((0, 0), line if line else "A", font=use_font)
        h += (bbox[3] - bbox[1]) + line_gap
    return h


def fit_contain(img: Image.Image, target: tuple[int, int], background: str = "#FFFFFF", padding: int = 0) -> Image.Image:
    tw, th = target
    iw = max(1, tw - padding * 2)
    ih = max(1, th - padding * 2)
    src_ratio = img.width / img.height
    dst_ratio = iw / ih
    if src_ratio > dst_ratio:
        nw = iw
        nh = int(iw / src_ratio)
    else:
        nh = ih
        nw = int(ih * src_ratio)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (tw, th), background)
    x = (tw - nw) // 2
    y = (th - nh) // 2
    canvas.paste(resized, (x, y))
    return canvas


def header_band(base: Image.Image, height: int) -> None:
    draw = ImageDraw.Draw(base)
    draw.rectangle((0, 0, base.width, height), fill="#153F67")


def draw_chip(draw: ImageDraw.ImageDraw, x: int, y: int, label: str) -> int:
    use_font = font(20, bold=True)
    tw = draw.textbbox((0, 0), label, font=use_font)[2]
    w = tw + 36
    draw.rounded_rectangle((x, y, x + w, y + 38), radius=18, fill="#F2F6FB")
    draw.text((x + 18, y + 8), label, font=use_font, fill="#183F66")
    return w


def feature_card(
    base: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    accent: str,
) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D7E4F1", radius=28, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 46, y1 + 46), radius=8, fill=accent)
    draw.text((x1 + 60, y1 + 14), title, font=font(24, bold=True), fill="#123B61")
    draw_wrapped(draw, (x1 + 18, y1 + 66), body, font(18), "#33485A", x2 - x1 - 36, 6)


def preview_panel(
    base: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    subtitle: str,
    image_path: Path,
) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D7E4F1", radius=30, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + 24, y1 + 18), title, font=font(30, bold=True), fill="#123B61")
    draw.text((x1 + 24, y1 + 58), subtitle, font=font(18), fill="#60768C")
    img = Image.open(image_path).convert("RGB")
    inner_w = x2 - x1 - 48
    inner_h = y2 - y1 - 112
    fit = fit_contain(img, (inner_w, inner_h), padding=10)
    mask = Image.new("L", (inner_w, inner_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, inner_w - 1, inner_h - 1), radius=24, fill=255)
    base.paste(fit, (x1 + 24, y1 + 92), mask)


def workflow_panel(base: Image.Image, box: tuple[int, int, int, int]) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D7E4F1", radius=28, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + 22, y1 + 18), "Workflow | 工作流", font=font(28, bold=True), fill="#123B61")
    colors = ["#2B6CB0", "#1F8A70", "#D97706", "#D64550"]
    total = x2 - x1 - 44
    node_w = 128
    gap = (total - node_w * len(WORKFLOW)) // (len(WORKFLOW) - 1)
    y = y1 + 96
    for idx, label in enumerate(WORKFLOW):
        bx1 = x1 + 22 + idx * (node_w + gap)
        bx2 = bx1 + node_w
        draw.rounded_rectangle((bx1, y, bx2, y + 58), radius=18, fill="#FBFDFF", outline=colors[idx], width=2)
        tw = draw.textbbox((0, 0), label, font=font(20, bold=True))[2]
        draw.text((bx1 + (node_w - tw) / 2, y + 16), label, font=font(20, bold=True), fill=colors[idx])
        if idx < len(WORKFLOW) - 1:
            ax1 = bx2 + 12
            ax2 = bx2 + gap - 14
            ay = y + 29
            draw.line((ax1, ay, ax2, ay), fill="#7CBAD2", width=4)
            draw.polygon([(ax2, ay), (ax2 - 12, ay - 7), (ax2 - 12, ay + 7)], fill="#7CBAD2")


def bullet_panel(
    base: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    bullets: list[str],
) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D7E4F1", radius=28, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + 22, y1 + 18), title, font=font(28, bold=True), fill="#123B61")
    for idx, line in enumerate(bullets):
        yy = y1 + 78 + idx * 44
        draw.rounded_rectangle((x1 + 22, yy + 8, x1 + 36, yy + 22), radius=4, fill="#2B6CB0")
        draw.text((x1 + 50, yy), line, font=font(20), fill="#33485A")


def make_landscape() -> Path:
    size = (2400, 1350)
    base = gradient(size, "#F5FAFD", "#EDF4FB")
    add_bg_shapes(base)
    header_band(base, 250)
    draw = ImageDraw.Draw(base)

    draw.text((78, 56), REPO_NAME, font=font(76, bold=True), fill="#FFFFFF")
    draw.text((82, 146), SUBTITLE, font=font(28, bold=True), fill="#D9E7F5")
    draw.text((82, 184), INTRO_SHORT, font=font(22), fill="#E6F0F8")

    chip_x = 82
    for label in CHIPS:
        w = draw_chip(draw, chip_x, 212, label)
        chip_x += w + 14

    preview_panel(
        base,
        (760, 308, 2332, 934),
        "真实课堂 PPT 缩略图",
        "精选页面完整展示，不裁切页面，不保留校徽。",
        GALLERY / "paper2scholarslides-ppt-preview-clean.png",
    )

    feature_positions = [
        (62, 308, 700, 446),
        (62, 466, 700, 604),
        (62, 624, 700, 762),
        (62, 782, 700, 920),
    ]
    for box, item in zip(feature_positions, FEATURES):
        feature_card(base, box, *item)

    workflow_panel(base, (62, 954, 1266, 1246))
    preview_panel(
        base,
        (1292, 954, 1790, 1246),
        "页面细节",
        "结构页、建模页、控制页局部示例。",
        GALLERY / "paper2scholarslides-ppt-preview-strip.png",
    )
    preview_panel(
        base,
        (1816, 954, 2332, 1246),
        "Figure Assets",
        "流程图、控制框图与学术线图资源。",
        GALLERY / "academic-figures-overview.png",
    )

    footer = "GitHub  " + REPO_URL
    draw.text((78, 1284), footer, font=font(18), fill="#5F748A")

    out = POSTERS / "academic-review-decksmith-poster-landscape.png"
    base.convert("RGB").save(out, quality=96)
    return out


def make_portrait() -> Path:
    size = (1440, 2048)
    base = gradient(size, "#F5FAFD", "#EEF4FA")
    add_bg_shapes(base)
    header_band(base, 250)
    draw = ImageDraw.Draw(base)

    draw.text((74, 56), REPO_NAME, font=font(64, bold=True), fill="#FFFFFF")
    draw.text((78, 134), SUBTITLE, font=font(26, bold=True), fill="#D9E7F5")
    draw.text((78, 172), "面向课程汇报、组会展示与专题综述的研究型幻灯片整理技能。", font=font(20), fill="#E6F0F8")

    chip_x = 78
    for label in CHIPS:
        w = draw_chip(draw, chip_x, 210, label)
        chip_x += w + 12

    preview_panel(
        base,
        (58, 296, 1382, 1126),
        "真实课堂 PPT 缩略图",
        "保留真实页面质感，同时去除校徽干扰。",
        GALLERY / "paper2scholarslides-ppt-preview-clean.png",
    )

    feature_card(base, (58, 1160, 690, 1300), *FEATURES[0])
    feature_card(base, (750, 1160, 1382, 1300), *FEATURES[1])
    feature_card(base, (58, 1324, 690, 1464), *FEATURES[2])
    feature_card(base, (750, 1324, 1382, 1464), *FEATURES[3])

    preview_panel(
        base,
        (58, 1496, 690, 1912),
        "页面细节",
        "三张代表页的局部示例。",
        GALLERY / "paper2scholarslides-ppt-preview-strip.png",
    )
    preview_panel(
        base,
        (750, 1496, 1382, 1912),
        "Figure Assets",
        "控制框图、流程图、曲线图与矩阵图。",
        GALLERY / "academic-figures-overview.png",
    )

    draw.text((62, 1978), REPO_URL, font=font(18), fill="#5F748A")

    out = POSTERS / "academic-review-decksmith-poster-portrait.png"
    base.convert("RGB").save(out, quality=96)
    return out


def main() -> None:
    landscape = make_landscape()
    portrait = make_portrait()
    print(landscape)
    print(portrait)


if __name__ == "__main__":
    main()
