# -*- coding: utf-8 -*-

"""

PPT Pipeline Design System

DesignHub (Fraternity Pen Pivot) + projection-optimized

聚合 McKinsey/PPTAgent/html-ppt-skill/pptx 四大来源

"""

from dataclasses import dataclass, field

from typing import Optional

from pptx.dml.color import RGBColor

from pptx.util import Pt, Inches, Emu





# ============================================================

# Design System — the single source of truth for all visual decisions

# ============================================================



@dataclass

class DesignSystem:

    """Container for all design decisions: colors, fonts, spacing, decor."""

    name: str



    # Background

    bg: RGBColor

    bg_soft: RGBColor       # 装饰区用

    bg_alt: RGBColor         # 备用背景



    # Text — projection requires ≥4.5:1 contrast

    text_title: RGBColor     # 标题

    text_body: RGBColor      # 正文

    text_dim: RGBColor       # 辅助文字

    text_light: RGBColor     # dark-background text (reversed)



    # Brand colors

    primary: RGBColor        # 主色

    secondary: RGBColor      # 辅色

    accent: RGBColor         # 点缀色



    # Semantic colors

    good: RGBColor           # 正面/生命

    warn: RGBColor           # 警示

    bad: RGBColor            # 负面/紧急



    # Fonts

    font_title: str = 'Microsoft YaHei'

    font_body: str = 'Microsoft YaHei'

    font_accent: str = 'Microsoft YaHei'



    # Slide dimensions (16:9 default, 13.333 × 7.5 inches)

    slide_width: Emu = Inches(13.333)

    slide_height: Emu = Inches(7.5)



    # Margins (projection-safe)

    margin_left: Emu = Inches(0.67)

    margin_right: Emu = Inches(0.67)

    margin_top: Emu = Inches(0.45)

    margin_bottom: Emu = Inches(0.45)



    # Decor

    left_bar_width: Emu = Inches(0.10)

    top_line_height: Emu = Inches(0.04)

    bottom_box_height: Emu = Inches(1.0)

    accent_bar_color: Optional[RGBColor] = None  # defaults to primary

    section_number_enabled: bool = True





# ============================================================

# Projection font sizes — 16:9 at typical viewing distance

# ============================================================



FONT_SIZES = {

    'hero':           Pt(66),    # 封面大标题

    'page_title':     Pt(48),    # 页面主标题

    'section_title':  Pt(40),    # 章节标题

    'subtitle':       Pt(36),    # 副标题

    'body':           Pt(32),    # 正文（投影最小安全尺寸）

    'body_small':     Pt(28),    # 小正文

    'caption':        Pt(22),    # 说明文字

    'footer':         Pt(14),    # 页脚/页码

    'data_big':       Pt(84),    # 大数字

    'data_mid':       Pt(60),    # 中数字

    'quote':          Pt(36),    # 引用

}





# ============================================================

# Theme presets

# ============================================================



# ★ DesignHub · 温暖希望系

# Background: warm cream; Primary: warm red; Secondary: life green; Accent: hope gold

# Target: student/public audience, projection, emotional storytelling

THEME_DESIGNHUB_WARM = DesignSystem(

    name='DesignHub · 温暖希望',

    bg=RGBColor(0xFD, 0xF8, 0xF5),

    bg_soft=RGBColor(0xF5, 0xF1, 0xE8),

    bg_alt=RGBColor(0xF0, 0xEE, 0xE6),

    text_title=RGBColor(0x8A, 0x1A, 0x1A),

    text_body=RGBColor(0x2D, 0x2D, 0x2D),

    text_dim=RGBColor(0x66, 0x66, 0x66),

    text_light=RGBColor(0xFF, 0xFF, 0xFF),

    primary=RGBColor(0xE6, 0x00, 0x12),

    secondary=RGBColor(0x4A, 0x9B, 0x5E),

    accent=RGBColor(0xF5, 0xA6, 0x23),

    good=RGBColor(0x3F, 0x7D, 0x4F),

    warn=RGBColor(0xB0, 0x7A, 0x1F),

    bad=RGBColor(0x8A, 0x1A, 0x1A),

)



# ★ DesignHub · 专业信任系

# Background: pure white; Primary: professional red; Secondary: trust blue

# Target: professional audience, institutional, formal

THEME_DESIGNHUB_PRO = DesignSystem(

    name='DesignHub · 专业信任',

    bg=RGBColor(0xFF, 0xFF, 0xFF),

    bg_soft=RGBColor(0xF4, 0xF6, 0xFA),

    bg_alt=RGBColor(0xEB, 0xEE, 0xF3),

    text_title=RGBColor(0x1A, 0x3A, 0x7A),

    text_body=RGBColor(0x1A, 0x1A, 0x2E),

    text_dim=RGBColor(0x4A, 0x55, 0x68),

    text_light=RGBColor(0xFF, 0xFF, 0xFF),

    primary=RGBColor(0xE6, 0x00, 0x12),

    secondary=RGBColor(0x2E, 0x5C, 0x8A),

    accent=RGBColor(0x4A, 0x9B, 0x5E),

    good=RGBColor(0x3F, 0x7D, 0x4F),

    warn=RGBColor(0xB0, 0x7A, 0x1F),

    bad=RGBColor(0x8A, 0x1A, 0x1A),

)



# ★ 投影优化默认 · academic-paper × Primary

# Balanced for projection: slightly warm bg, high contrast, dark blue titles

THEME_PROJECTION = DesignSystem(

    name='投影优化默认',

    bg=RGBColor(0xFD, 0xFC, 0xF8),

    bg_soft=RGBColor(0xF5, 0xF1, 0xE8),

    bg_alt=RGBColor(0xF0, 0xEE, 0xE6),

    text_title=RGBColor(0x1A, 0x3A, 0x7A),

    text_body=RGBColor(0x33, 0x33, 0x33),

    text_dim=RGBColor(0x70, 0x70, 0x70),

    text_light=RGBColor(0xFD, 0xFC, 0xF8),

    primary=RGBColor(0x1A, 0x3A, 0x7A),

    secondary=RGBColor(0xE6, 0x00, 0x12),

    accent=RGBColor(0x5C, 0x4A, 0x3E),

    good=RGBColor(0x3F, 0x7D, 0x4F),

    warn=RGBColor(0xB0, 0x7A, 0x1F),

    bad=RGBColor(0x8A, 0x1A, 0x1A),

)





# Registry — English keys + Chinese aliases

_THEMES = {

    'designhub_warm': THEME_DESIGNHUB_WARM,

    'designhub_pro': THEME_DESIGNHUB_PRO,

    'projection': THEME_PROJECTION,

    # Chinese aliases

    'DesignHub·温暖希望': THEME_DESIGNHUB_WARM,

    'DesignHub·专业信任': THEME_DESIGNHUB_PRO,

    '投影优化默认': THEME_PROJECTION,

    '温暖希望': THEME_DESIGNHUB_WARM,

    '专业信任': THEME_DESIGNHUB_PRO,

}





def load_theme(name: str) -> DesignSystem:

    """Load a theme by name.



    Args:

        name: Theme key or display name (case-insensitive, spaces optional).

              Examples: 'designhub_warm', 'DesignHub · 温暖希望', 'projection'



    Returns:

        DesignSystem dataclass with all colors, fonts, and spacing.



    Raises:

        KeyError: Theme not found.

    """

    # Normalize: strip spaces, dots, underscores, lower

    norm = name.lower().replace(' ', '').replace('_', '').replace('·', '')

    # Direct match

    if norm in _THEMES:

        return _THEMES[norm]

    # Try original name

    if name in _THEMES:

        return _THEMES[name]

    # Fuzzy: check if any key contains or is contained by normalized input

    for k, v in _THEMES.items():

        knorm = k.lower().replace(' ', '').replace('_', '').replace('·', '')

        if norm in knorm or knorm in norm:

            return v

    raise KeyError(

        f'Theme "{name}" not found. Available keys: {list(_THEMES.keys())}'

    )





def list_themes() -> list[str]:

    """List available theme display names."""

    seen = set()

    return [t.name for t in _THEMES.values() if not (t.name in seen or seen.add(t.name))]

