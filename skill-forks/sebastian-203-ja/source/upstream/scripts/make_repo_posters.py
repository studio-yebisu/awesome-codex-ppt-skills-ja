#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate polished project posters for the repository."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
GALLERY = ASSETS / "gallery"
POSTERS = ASSETS / "posters"
POSTERS.mkdir(parents=True, exist_ok=True)

REPO_NAME = "Paper2ScholarSlides"
DEFAULT_URL = "https://github.com/ficooooo/Paper2ScholarSlides"
INTRO = (
    "面向学术综述与研究汇报的幻灯片构建技能。它将论文资料、综述初稿与既有模板整理为"
    "结构清晰、图表来源明确、公式可解释、版式可复核的研究型 PPT 资产，适用于课程汇报、"
    "组会交流、开题答辩与专题综述展示。"
)
CHIPS = ["综述重构", "图表说明", "公式解读", "模板保真", "导出校验"]

FEATURES = [
    (
        "结构不是堆章节",
        "按“背景—问题—方法—建模—控制—应用”重组内容，让综述页序真正服务于讲述逻辑。",
        "#2B6CB0",
    ),
    (
        "图片必须可追溯",
        "区分文献原图、重绘示意、原生表格与展示性配图，避免整套幻灯片视觉来源混乱。",
        "#1F8A70",
    ),
    (
        "公式需要可读性",
        "关键公式不仅展示，还补充变量、物理含义、适用边界和与图表的对应关系。",
        "#D97706",
    ),
    (
        "交付前做导出核查",
        "统一导出 PNG 逐页检查溢出、遮挡、低清晰度、占位文本和引用说明缺失问题。",
        "#D64550",
    ),
]

WORKFLOW = ["资料输入", "论证重构", "图表处理", "PPT 成稿", "导出校验"]

ASSET_LINES = [
    "SKILL.md：通用综述转汇报规则",
    "README：项目概览与上手方式",
    "Gallery：真实 PPT 预览与图件总览",
    "Posters：横版与竖版项目海报",
    "Scripts：可重复生成海报与展示图",
]

USE_CASES = ["课程综述汇报", "课题组组会", "博士生预答辩", "文献综述展示"]


def git_remote_url() -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        url = result.stdout.strip().removesuffix(".git")
        if "Paper2ScholarSlides" in url:
            return "https://github.com/ficooooo/Paper2ScholarSlides"
        if "Academic-Review-Decksmith" in url:
            return "https://github.com/ficooooo/Paper2ScholarSlides"
        return url or DEFAULT_URL
    except Exception:
        return DEFAULT_URL


REPO_URL = git_remote_url()


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    return ImageFont.truetype(path, size)


def hex_rgba(color: str, alpha: int) -> tuple[int, int, int, int]:
    r, g, b = ImageColor.getrgb(color)
    return (r, g, b, alpha)


def vertical_gradient(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
    width, height = size
    img = Image.new("RGBA", size)
    top_rgb = ImageColor.getrgb(top)
    bottom_rgb = ImageColor.getrgb(bottom)
    pixels = img.load()
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(int(top_rgb[i] * (1 - ratio) + bottom_rgb[i] * ratio) for i in range(3)) + (255,)
        for x in range(width):
            pixels[x, y] = color
    return img


def add_soft_shapes(base: Image.Image) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = base.size
    draw.ellipse((w - 700, -160, w + 260, 700), fill=hex_rgba("#8FD3FF", 28))
    draw.ellipse((-260, h - 520, 480, h + 180), fill=hex_rgba("#CFE5FF", 34))
    draw.rounded_rectangle((w - 980, h - 250, w - 140, h - 90), radius=72, fill=hex_rgba("#F2F7FF", 180))
    overlay = overlay.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(overlay)


def rounded_panel(
    base: Image.Image,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int, int] | str = "#FFFFFF",
    outline: tuple[int, int, int, int] | str = "#D7E4F1",
    radius: int = 32,
    shadow: bool = True,
) -> None:
    x1, y1, x2, y2 = box
    if shadow:
        shadow_img = Image.new("RGBA", base.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_draw.rounded_rectangle(
            (x1 + 10, y1 + 14, x2 + 10, y2 + 14),
            radius=radius,
            fill=(8, 28, 52, 28),
        )
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(16))
        base.alpha_composite(shadow_img)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
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
            width = draw.textbbox((0, 0), trial, font=font)[2]
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
    font: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_gap: int = 8,
) -> int:
    x, y = xy
    height = 0
    for line in wrap_text(draw, text, font, max_width):
        draw.text((x, y + height), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y + height), line if line else "A", font=font)
        height += (bbox[3] - bbox[1]) + line_gap
    return height


def fit_image(img: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    target_w, target_h = target_size
    src_ratio = img.width / img.height
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        new_h = target_h
        new_w = int(target_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(target_w / src_ratio)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def sanitize_real_preview() -> Image.Image:
    img = Image.open(GALLERY / "snake-robot-demo-overview-real.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cols, rows = 3, 9
    cell_w = img.width / cols
    cell_h = img.height / rows
    for row in range(rows):
        for col in range(cols):
            x = int(col * cell_w)
            y = int(row * cell_h)
            draw.rounded_rectangle(
                (x + 18, y + 10, x + 118, y + 34),
                radius=8,
                fill=(255, 255, 255, 245),
            )
            draw.rounded_rectangle(
                (x + 42, y + 34, x + 188, y + 84),
                radius=12,
                fill=(255, 255, 255, 248),
            )
            draw.rounded_rectangle(
                (x + int(cell_w) - 120, y + 36, x + int(cell_w) - 24, y + 66),
                radius=10,
                fill=(255, 255, 255, 238),
            )
    overlay = overlay.filter(ImageFilter.GaussianBlur(1))
    img.alpha_composite(overlay)
    return img


def slide_crop_strip() -> Image.Image:
    preview = sanitize_real_preview()
    cols, rows = 3, 9
    cell_w = preview.width // cols
    cell_h = preview.height // rows
    picks = [1, 14, 20]
    crops: list[Image.Image] = []
    for slide_no in picks:
        idx = slide_no - 1
        row = idx // cols
        col = idx % cols
        x = col * cell_w
        y = row * cell_h
        crop = preview.crop((x + 32, y + 30, x + cell_w - 28, y + cell_h - 30))
        crops.append(crop)
    strip = Image.new("RGBA", (1200, 300), (0, 0, 0, 0))
    x = 0
    for crop in crops:
        frame = Image.new("RGBA", (372, 248), (255, 255, 255, 255))
        fit = fit_image(crop, (348, 224))
        frame_draw = ImageDraw.Draw(frame)
        frame_draw.rounded_rectangle((0, 0, 371, 247), radius=24, fill="#FFFFFF", outline="#D6E1EC", width=2)
        frame.paste(fit, (12, 12))
        frame = frame.filter(ImageFilter.GaussianBlur(0))
        strip.alpha_composite(frame, (x, 26))
        x += 414
    return strip


def add_chip_row(draw: ImageDraw.ImageDraw, x: int, y: int, labels: list[str]) -> None:
    cursor = x
    font = load_font(22, bold=True)
    for label in labels:
        bbox = draw.textbbox((0, 0), label, font=font)
        width = bbox[2] - bbox[0] + 34
        draw.rounded_rectangle((cursor, y, cursor + width, y + 42), radius=18, fill="#EDF5FF")
        draw.text((cursor + 17, y + 8), label, font=font, fill="#133E66")
        cursor += width + 14


def draw_feature_card(base: Image.Image, box: tuple[int, int, int, int], title: str, body: str, accent: str) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D8E4F0", radius=28, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 22, y1 + 22, x1 + 54, y1 + 54), radius=10, fill=accent)
    draw.text((x1 + 70, y1 + 18), title, font=load_font(28, bold=True), fill="#123B61")
    draw_wrapped(draw, (x1 + 24, y1 + 78), body, load_font(21), "#314252", x2 - x1 - 48, 7)


def draw_preview_panel(
    base: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    subtitle: str,
    image: Image.Image,
) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D8E4F0", radius=34, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + 28, y1 + 22), title, font=load_font(30, bold=True), fill="#123B61")
    draw.text((x1 + 28, y1 + 62), subtitle, font=load_font(19), fill="#5C6E80")
    inner = (x1 + 24, y1 + 108, x2 - 24, y2 - 24)
    fitted = fit_image(image, (inner[2] - inner[0], inner[3] - inner[1]))
    mask = Image.new("L", (inner[2] - inner[0], inner[3] - inner[1]), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, mask.width - 1, mask.height - 1), radius=26, fill=255)
    base.paste(fitted, (inner[0], inner[1]), mask)
    shine = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shine_draw = ImageDraw.Draw(shine)
    shine_draw.polygon(
        [
            (inner[0] + 60, inner[1]),
            (inner[0] + 240, inner[1]),
            (inner[0] + 120, inner[3]),
            (inner[0] - 20, inner[3]),
        ],
        fill=(255, 255, 255, 20),
    )
    shine = shine.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(shine)


def draw_text_list(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    items: list[str],
    bullet_color: str,
    font_size: int = 22,
    line_step: int = 40,
) -> None:
    font = load_font(font_size)
    for idx, item in enumerate(items):
        yy = y + idx * line_step
        draw.rounded_rectangle((x, yy + 8, x + 16, yy + 24), radius=5, fill=bullet_color)
        draw.text((x + 28, yy), item, font=font, fill="#304252")


def draw_workflow(base: Image.Image, box: tuple[int, int, int, int]) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D8E4F0", radius=28, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + 24, y1 + 18), "工作流程", font=load_font(28, bold=True), fill="#123B61")
    total_w = x2 - x1 - 48
    step_w = 170
    gap = (total_w - step_w * len(WORKFLOW)) // (len(WORKFLOW) - 1)
    cy = y1 + 102
    for idx, label in enumerate(WORKFLOW):
        bx1 = x1 + 24 + idx * (step_w + gap)
        bx2 = bx1 + step_w
        color = ["#2B6CB0", "#1F8A70", "#D97706", "#D64550", "#123B61"][idx]
        draw.rounded_rectangle((bx1, cy, bx2, cy + 62), radius=18, fill="#F7FAFE", outline=color, width=2)
        tw = draw.textbbox((0, 0), label, font=load_font(22, bold=True))[2]
        draw.text((bx1 + (step_w - tw) / 2, cy + 14), label, font=load_font(22, bold=True), fill=color)
        if idx < len(WORKFLOW) - 1:
            ax1 = bx2 + 10
            ax2 = bx2 + gap - 10
            ay = cy + 31
            draw.line((ax1, ay, ax2, ay), fill="#7CBAD2", width=5)
            draw.polygon([(ax2, ay), (ax2 - 14, ay - 8), (ax2 - 14, ay + 8)], fill="#7CBAD2")


def draw_asset_panel(base: Image.Image, box: tuple[int, int, int, int]) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D8E4F0", radius=28, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + 24, y1 + 18), "仓库内容", font=load_font(28, bold=True), fill="#123B61")
    draw_text_list(draw, x1 + 24, y1 + 78, ASSET_LINES, "#2B6CB0", font_size=20, line_step=40)


def draw_usecase_panel(base: Image.Image, box: tuple[int, int, int, int]) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D8E4F0", radius=28, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + 24, y1 + 18), "适用场景", font=load_font(28, bold=True), fill="#123B61")
    draw_text_list(draw, x1 + 24, y1 + 82, USE_CASES, "#1F8A70", font_size=22, line_step=46)


def landscape_poster() -> Path:
    size = (2400, 1350)
    base = vertical_gradient(size, "#F5F9FD", "#EDF4FB")
    add_soft_shapes(base)
    draw = ImageDraw.Draw(base)

    draw.text((100, 82), REPO_NAME, font=load_font(84, bold=True), fill="#0E3658")
    intro_h = draw_wrapped(draw, (100, 192), INTRO, load_font(26), "#33475A", 860, 8)
    draw.rounded_rectangle((100, 242 + intro_h, 770, 286 + intro_h), radius=16, fill="#EAF3FF")
    draw.text((124, 252 + intro_h), REPO_URL, font=load_font(21), fill="#164A75")
    add_chip_row(draw, 100, 314 + intro_h, CHIPS)

    preview = sanitize_real_preview()
    draw_preview_panel(
        base,
        (980, 72, 2310, 810),
        "真实 PPT 效果预览",
        "使用仓库中的真实汇报预览图，并对校徽区域做统一净化处理",
        preview,
    )

    y0 = 470
    card_w, card_h = 400, 182
    positions = [(100, y0), (530, y0), (100, y0 + 212), (530, y0 + 212)]
    for (x, y), (title, body, accent) in zip(positions, FEATURES):
        draw_feature_card(base, (x, y, x + card_w, y + card_h), title, body, accent)

    draw_preview_panel(
        base,
        (980, 842, 1680, 1266),
        "局部页面放大",
        "从真实预览中截取代表性页面，强调版式与内容密度",
        slide_crop_strip(),
    )
    figure_gallery = Image.open(GALLERY / "academic-figures-overview.png").convert("RGBA")
    draw_preview_panel(
        base,
        (1710, 842, 2310, 1070),
        "图件资源",
        "重绘图、控制框图与学术线图可直接复用",
        figure_gallery,
    )
    draw_usecase_panel(base, (1710, 1096, 2310, 1266))

    draw_workflow(base, (100, 1094, 1460, 1266))
    draw_asset_panel(base, (1490, 1096, 1680, 1266))

    out = POSTERS / "paper2scholarslides-poster-landscape.png"
    base.convert("RGB").save(out, quality=96)
    return out


def portrait_poster() -> Path:
    size = (1800, 2600)
    base = vertical_gradient(size, "#F5F9FD", "#EDF4FB")
    add_soft_shapes(base)
    draw = ImageDraw.Draw(base)

    draw.text((90, 88), REPO_NAME, font=load_font(76, bold=True), fill="#0E3658")
    intro_h = draw_wrapped(draw, (90, 192), INTRO, load_font(28), "#33475A", 1540, 10)
    draw.rounded_rectangle((90, 228 + intro_h, 980, 276 + intro_h), radius=18, fill="#EAF3FF")
    draw.text((116, 240 + intro_h), REPO_URL, font=load_font(22), fill="#164A75")
    add_chip_row(draw, 90, 306 + intro_h, CHIPS)

    preview = sanitize_real_preview()
    draw_preview_panel(
        base,
        (90, 390 + intro_h, 1710, 1500 + intro_h),
        "真实 PPT 效果预览",
        "主视觉选用仓库中的真实课程汇报预览图，校徽区域已做净化处理",
        preview,
    )

    features_y = 1540 + intro_h
    card_w, card_h = 760, 182
    positions = [
        (90, features_y),
        (950, features_y),
        (90, features_y + 212),
        (950, features_y + 212),
    ]
    for (x, y), (title, body, accent) in zip(positions, FEATURES):
        draw_feature_card(base, (x, y, x + card_w, y + card_h), title, body, accent)

    figure_gallery = Image.open(GALLERY / "academic-figures-overview.png").convert("RGBA")
    draw_preview_panel(
        base,
        (90, features_y + 444, 820, features_y + 864),
        "图件资源",
        "用于 README 与报告的学术风格图件预览",
        figure_gallery,
    )
    draw_preview_panel(
        base,
        (860, features_y + 444, 1710, features_y + 864),
        "局部页面放大",
        "从真实预览中提取代表性页面，展示结构页、建模页与控制页",
        slide_crop_strip(),
    )

    footer_y = features_y + 894
    draw_workflow(base, (90, footer_y, 1710, footer_y + 176))
    draw_asset_panel(base, (90, footer_y + 204, 1060, footer_y + 394))
    draw_usecase_panel(base, (1090, footer_y + 204, 1710, footer_y + 394))

    out = POSTERS / "paper2scholarslides-poster-portrait.png"
    base.convert("RGB").save(out, quality=96)
    return out


def save_sanitized_preview() -> Path:
    out = GALLERY / "snake-robot-demo-overview-sanitized.png"
    sanitize_real_preview().convert("RGB").save(out, quality=96)
    return out


def main() -> None:
    sanitized = save_sanitized_preview()
    landscape = landscape_poster()
    portrait = portrait_poster()
    print(sanitized)
    print(landscape)
    print(portrait)


if __name__ == "__main__":
    main()
