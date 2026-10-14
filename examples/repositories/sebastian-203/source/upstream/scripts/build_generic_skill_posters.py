#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build landscape and portrait posters for the generic academic PPT skill."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "assets" / "gallery"
POSTERS = ROOT / "assets" / "posters"
POSTERS.mkdir(parents=True, exist_ok=True)

LANDSCAPE_BG_SRC = Path(
    r"C:\Users\admin\.codex\generated_images\019d8eea-707c-7123-8a1e-1c75abd38755\ig_0eb913ec45cc8bc50169faf788c2048198b2713f89a5426c35.png"
)
PORTRAIT_BG_SRC = Path(
    r"C:\Users\admin\.codex\generated_images\019d8eea-707c-7123-8a1e-1c75abd38755\ig_0eb913ec45cc8bc50169faf7df96b88198a145273a68d9e29f.png"
)

LANDSCAPE_BG = POSTERS / "paper2scholarslides-image2-landscape-bg.png"
PORTRAIT_BG = POSTERS / "paper2scholarslides-image2-portrait-bg.png"

REPO_NAME = "Paper2ScholarSlides"
REPO_URL = "https://github.com/ficooooo/Paper2ScholarSlides"
TAGLINE_EN = "A polished skill for turning research material into rigorous academic slide decks."
INTRO_CN = (
    "面向学术综述、课程汇报与科研展示的幻灯片生成技能。"
    "它将论文资料、文稿与模板整理为结构清晰、图表来源明确、公式可解释、"
    "版式可复核的研究型 PPT 成果，适用于课程展示、课题组组会、开题答辩与文献综述汇报。"
)

CHIPS = ["Academic Decks", "Citation-aware", "Figure Notes", "Formula Meaning", "Layout QA"]

FEATURES = [
    (
        "Rebuild the argument",
        "把原始文稿改写为真正适合汇报的页面叙事，而不是把综述目录逐条搬上幻灯片。",
        "#1F5F9C",
    ),
    (
        "Explain figures and formulas",
        "图表不是装饰，公式也不是摆设；关键页面要补上读图要点、变量含义与工程解释。",
        "#187C73",
    ),
    (
        "Stay editable and verifiable",
        "强调模板保真、原生组件可编辑以及导出后的版式检查，减少最终交付风险。",
        "#D46E1C",
    ),
]

USES = ["Course reviews", "Lab seminars", "Thesis defenses", "Survey talks"]

OUTPUTS = [
    "Deck preview",
    "Figure pack",
    "Poster assets",
    "Reusable workflow",
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    return ImageFont.truetype(path, size)


def rgb(color: str) -> tuple[int, int, int]:
    return ImageColor.getrgb(color)


def rgba(color: str, alpha: int) -> tuple[int, int, int, int]:
    r, g, b = rgb(color)
    return (r, g, b, alpha)


def ensure_backgrounds() -> tuple[Path, Path]:
    shutil.copy2(LANDSCAPE_BG_SRC, LANDSCAPE_BG)
    shutil.copy2(PORTRAIT_BG_SRC, PORTRAIT_BG)
    return LANDSCAPE_BG, PORTRAIT_BG


def fit_cover(img: Image.Image, target: tuple[int, int]) -> Image.Image:
    tw, th = target
    sr = img.width / img.height
    tr = tw / th
    if sr > tr:
        nh = th
        nw = int(th * sr)
    else:
        nw = tw
        nh = int(tw / sr)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def fit_contain(img: Image.Image, target: tuple[int, int], background: str = "#FFFFFF", padding: int = 0) -> Image.Image:
    tw, th = target
    iw = max(1, tw - padding * 2)
    ih = max(1, th - padding * 2)
    sr = img.width / img.height
    tr = iw / ih
    if sr > tr:
        nw = iw
        nh = int(iw / sr)
    else:
        nh = ih
        nw = int(ih * sr)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (tw, th), background)
    x = (tw - nw) // 2
    y = (th - nh) // 2
    canvas.paste(resized, (x, y))
    return canvas


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
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
    h = 0
    for line in wrap_text(draw, text, font, max_width):
        draw.text((x, y + h), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line if line else "A", font=font)
        h += (bbox[3] - bbox[1]) + line_gap
    return h


def rounded_panel(base: Image.Image, box: tuple[int, int, int, int], fill: str, outline: str, radius: int = 28, shadow: bool = True) -> None:
    x1, y1, x2, y2 = box
    if shadow:
        shadow_img = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow_img)
        sd.rounded_rectangle((x1 + 8, y1 + 12, x2 + 8, y2 + 12), radius=radius, fill=(6, 28, 52, 28))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(14))
        base.alpha_composite(shadow_img)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def draw_chip_row(draw: ImageDraw.ImageDraw, x: int, y: int, labels: list[str]) -> None:
    cursor = x
    font = load_font(18, bold=True)
    for label in labels:
        w = draw.textbbox((0, 0), label, font=font)[2] + 34
        draw.rounded_rectangle((cursor, y, cursor + w, y + 38), radius=16, fill="#ECF4FF")
        draw.text((cursor + 17, y + 9), label, font=font, fill="#143D66")
        cursor += w + 12


def draw_feature_card(base: Image.Image, box: tuple[int, int, int, int], title: str, body: str, accent: str) -> None:
    rounded_panel(base, box, fill="#FFFFFF", outline="#D4E2F0", radius=26, shadow=True)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 46, y1 + 46), radius=8, fill=accent)
    draw.text((x1 + 62, y1 + 16), title, font=load_font(21, bold=True), fill="#123A60")
    draw_wrapped(draw, (x1 + 18, y1 + 60), body, load_font(17), "#334454", x2 - x1 - 36, 6)


def draw_bullets(draw: ImageDraw.ImageDraw, x: int, y: int, items: list[str], color: str, font_size: int = 18, step: int = 30) -> None:
    font = load_font(font_size)
    for idx, item in enumerate(items):
        yy = y + idx * step
        draw.rounded_rectangle((x, yy + 7, x + 12, yy + 19), radius=4, fill=color)
        draw.text((x + 22, yy), item, font=font, fill="#2D4154")


def poster_landscape(bg_path: Path) -> Path:
    bg = Image.open(bg_path).convert("RGB")
    canvas = fit_cover(bg, (2400, 1350)).convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((56, 60, 1210, 1290), radius=42, fill=rgba("#F7FBFF", 208))
    od.rounded_rectangle((1260, 86, 2328, 720), radius=42, fill=rgba("#FFFFFF", 224))
    od.rounded_rectangle((1260, 758, 1792, 1240), radius=34, fill=rgba("#FFFFFF", 222))
    od.rounded_rectangle((1830, 758, 2328, 1240), radius=34, fill=rgba("#F9FCFF", 228))
    overlay = overlay.filter(ImageFilter.GaussianBlur(2))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)

    draw.text((104, 104), REPO_NAME, font=load_font(72, bold=True), fill="#0E3658")
    draw_wrapped(draw, (108, 206), TAGLINE_EN, load_font(23), "#567086", 980, 6)
    intro_h = draw_wrapped(draw, (108, 276), INTRO_CN, load_font(24), "#304355", 980, 8)

    draw.text((108, 412 + intro_h), "GitHub", font=load_font(18, bold=True), fill="#768AA0")
    draw.rounded_rectangle((108, 444 + intro_h, 760, 494 + intro_h), radius=18, fill="#E9F2FE")
    draw.text((132, 458 + intro_h), REPO_URL, font=load_font(18), fill="#174B75")
    draw_chip_row(draw, 108, 530 + intro_h, CHIPS)

    preview = fit_contain(Image.open(GALLERY / "snake-robot-demo-overview.png").convert("RGB"), (1000, 430), padding=12)
    rounded_panel(canvas, (1288, 112, 2300, 680), fill="#FFFFFF", outline="#D7E4F0", radius=34, shadow=False)
    draw.text((1320, 138), "Preview", font=load_font(28, bold=True), fill="#123A60")
    draw.text((1320, 176), "Generic academic deck overview", font=load_font(18), fill="#5B7288")
    mask = Image.new("L", (1000, 430), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 999, 429), radius=24, fill=255)
    canvas.paste(preview, (1294, 220), mask)

    card_y = 690 if intro_h < 130 else 720
    cards = [
        (104, card_y, 590, card_y + 190),
        (616, card_y, 1102, card_y + 190),
        (104, card_y + 220, 1102, card_y + 410),
    ]
    for box, feature in zip(cards, FEATURES):
        draw_feature_card(canvas, box, *feature)

    rounded_panel(canvas, (1288, 780, 1772, 1240), fill="#FFFFFF", outline="#D7E4F0", radius=30, shadow=False)
    draw.text((1318, 812), "Best For", font=load_font(28, bold=True), fill="#123A60")
    draw_bullets(draw, 1320, 866, USES, "#1F5F9C", font_size=21, step=42)

    fig = fit_contain(Image.open(GALLERY / "academic-figures-overview.png").convert("RGB"), (432, 178), padding=10)
    mask2 = Image.new("L", (432, 178), 0)
    ImageDraw.Draw(mask2).rounded_rectangle((0, 0, 431, 177), radius=18, fill=255)
    canvas.paste(fig, (1314, 1020), mask2)

    rounded_panel(canvas, (1802, 780, 2328, 1240), fill="#FFFFFF", outline="#D7E4F0", radius=30, shadow=False)
    draw.text((1834, 812), "What It Produces", font=load_font(28, bold=True), fill="#123A60")
    draw_bullets(draw, 1838, 868, OUTPUTS, "#D46E1C", font_size=21, step=42)
    banner = fit_contain(Image.open(GALLERY / "project-overview.png").convert("RGB"), (450, 154), padding=8)
    mask3 = Image.new("L", (450, 154), 0)
    ImageDraw.Draw(mask3).rounded_rectangle((0, 0, 449, 153), radius=18, fill=255)
    canvas.paste(banner, (1838, 1030), mask3)

    out = POSTERS / "paper2scholarslides-generic-poster-landscape.png"
    canvas.convert("RGB").save(out, quality=96)
    return out


def poster_portrait(bg_path: Path) -> Path:
    bg = Image.open(bg_path).convert("RGB")
    canvas = fit_cover(bg, (1800, 2600)).convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((68, 64, 1732, 548), radius=40, fill=rgba("#F8FBFF", 216))
    od.rounded_rectangle((68, 590, 1732, 1478), radius=40, fill=rgba("#FFFFFF", 224))
    od.rounded_rectangle((68, 1516, 810, 2320), radius=34, fill=rgba("#FFFFFF", 220))
    od.rounded_rectangle((844, 1516, 1732, 2320), radius=34, fill=rgba("#F9FCFF", 226))
    overlay = overlay.filter(ImageFilter.GaussianBlur(2))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)

    draw.text((112, 110), REPO_NAME, font=load_font(66, bold=True), fill="#0E3658")
    draw_wrapped(draw, (116, 206), TAGLINE_EN, load_font(24), "#587086", 1440, 6)
    intro_h = draw_wrapped(draw, (116, 274), INTRO_CN, load_font(26), "#304355", 1440, 10)
    draw.text((116, 388 + intro_h), "GitHub", font=load_font(19, bold=True), fill="#768AA0")
    draw.rounded_rectangle((116, 424 + intro_h, 872, 478 + intro_h), radius=18, fill="#E9F2FE")
    draw.text((142, 440 + intro_h), REPO_URL, font=load_font(20), fill="#174B75")
    draw_chip_row(draw, 116, 506 + intro_h, ["Academic PPT", "Narrative", "Visual Notes", "QA"])

    rounded_panel(canvas, (96, 620, 1704, 1452), fill="#FFFFFF", outline="#D7E4F0", radius=34, shadow=False)
    draw.text((132, 652), "Preview", font=load_font(30, bold=True), fill="#123A60")
    draw.text((132, 694), "Generic academic deck overview and workflow banner", font=load_font(20), fill="#5B7288")
    preview = fit_contain(Image.open(GALLERY / "snake-robot-demo-overview.png").convert("RGB"), (1548, 420), padding=16)
    mask = Image.new("L", (1548, 420), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 1547, 419), radius=24, fill=255)
    canvas.paste(preview, (126, 744), mask)
    banner = fit_contain(Image.open(GALLERY / "project-overview.png").convert("RGB"), (1548, 214), padding=12)
    maskb = Image.new("L", (1548, 214), 0)
    ImageDraw.Draw(maskb).rounded_rectangle((0, 0, 1547, 213), radius=24, fill=255)
    canvas.paste(banner, (126, 1198), maskb)

    for idx, (title, body, accent) in enumerate(FEATURES):
        y = 1560 + idx * 218
        draw_feature_card(canvas, (96, y, 780, y + 180), title, body, accent)

    rounded_panel(canvas, (868, 1560, 1704, 1966), fill="#FFFFFF", outline="#D7E4F0", radius=30, shadow=False)
    draw.text((904, 1592), "Figure Assets", font=load_font(28, bold=True), fill="#123A60")
    figure = fit_contain(Image.open(GALLERY / "academic-figures-overview.png").convert("RGB"), (742, 236), padding=12)
    mask2 = Image.new("L", (742, 236), 0)
    ImageDraw.Draw(mask2).rounded_rectangle((0, 0, 741, 235), radius=20, fill=255)
    canvas.paste(figure, (912, 1648), mask2)
    draw.text((908, 1902), "Reusable charts, diagrams, and figure logic panels", font=load_font(18), fill="#5B7288")

    rounded_panel(canvas, (868, 2002, 1704, 2320), fill="#FFFFFF", outline="#D7E4F0", radius=30, shadow=False)
    draw.text((904, 2034), "Best For", font=load_font(28, bold=True), fill="#123A60")
    draw_bullets(draw, 908, 2088, USES, "#1F5F9C", font_size=21, step=42)
    draw.text((904, 2262), "Output: clean decks, figure notes, and reusable poster assets", font=load_font(18), fill="#5B7288")

    out = POSTERS / "paper2scholarslides-generic-poster-portrait.png"
    canvas.convert("RGB").save(out, quality=96)
    return out


def main() -> None:
    landscape_bg, portrait_bg = ensure_backgrounds()
    landscape = poster_landscape(landscape_bg)
    portrait = poster_portrait(portrait_bg)
    print(landscape)
    print(portrait)


if __name__ == "__main__":
    main()
