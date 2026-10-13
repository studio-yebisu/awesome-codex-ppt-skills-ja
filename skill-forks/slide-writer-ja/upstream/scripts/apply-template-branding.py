#!/usr/bin/env python3
"""
apply-template-branding.py — 一次性把标题、主题样式、logo 写回 HTML 模板。

用法：
    python3 scripts/apply-template-branding.py <html-file> --title <title>
    python3 scripts/apply-template-branding.py <html-file> --title <title> --speaker <speaker>
    python3 scripts/apply-template-branding.py <html-file> --title <title> --speaker <speaker> --theme-id <theme-id>
    python3 scripts/apply-template-branding.py <html-file> --title <title> --theme-id <theme-id>
    python3 scripts/apply-template-branding.py <html-file> --title <title> --theme-id <theme-id> \
        [--primary-id <primary-id> --primary-alt <primary-alt>] \
        [--secondary-id <secondary-id> --secondary-alt <secondary-alt>]

默认：
    - theme-id = ant-group
    - logo 跟随 theme-id 自动推断
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
LOGO_DIR = ROOT_DIR / "themes" / "logos"
TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
THEME_STYLE_RE = re.compile(r"<!-- %%THEME_STYLE%% -->")
LOGO_BLOCK_RE = re.compile(
    r'<div id="globalLogoGroup" class="logo-group-(?:single|dual)"[^>]*>.*?</div>',
    re.DOTALL,
)
DEFAULT_THEME_LOGOS: dict[str, dict[str, str]] = {
    "ant-group": {
        "primary_id": "ant-group",
        "primary_alt": "蚂蚁集团",
        "secondary_id": "alipay",
        "secondary_alt": "支付宝",
    },
    "bytedance": {
        "primary_id": "bytedance",
        "primary_alt": "字节跳动",
    },
    "meituan": {
        "primary_id": "meituan",
        "primary_alt": "美团",
    },
    "jd": {
        "primary_id": "jd",
        "primary_alt": "京东",
    },
    "baidu": {
        "primary_id": "baidu",
        "primary_alt": "百度",
    },
    "huawei": {
        "primary_id": "huawei",
        "primary_alt": "华为",
    },
    "xiaomi": {
        "primary_id": "xiaomi",
        "primary_alt": "小米",
    },
    "netease": {
        "primary_id": "netease",
        "primary_alt": "网易",
    },
    "didi": {
        "primary_id": "didi",
        "primary_alt": "滴滴",
    },
    "microsoft": {
        "primary_id": "microsoft",
        "primary_alt": "Microsoft",
    },
    "google": {
        "primary_id": "google",
        "primary_alt": "Google",
    },
    "apple": {
        "primary_id": "apple",
        "primary_alt": "Apple",
    },
    "tencent": {
        "primary_id": "tencent",
        "primary_alt": "腾讯",
    },
    "alibaba": {
        "primary_id": "alibaba",
        "primary_alt": "阿里巴巴",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply title, theme style and logo branding to a local HTML file."
    )
    parser.add_argument("html_file", help="要替换 branding 的 HTML 文件")
    parser.add_argument("--title", required=True, help="演讲主题")
    parser.add_argument("--speaker", help="演讲者")
    parser.add_argument(
        "--theme-id",
        default="ant-group",
        help="主题 ID，对应 themes/<theme-id>.md，默认 ant-group",
    )
    parser.add_argument("--primary-id", help="主 logo 的品牌 ID，例如 ant-group")
    parser.add_argument("--primary-alt", help="主 logo 的 alt 文案，例如 蚂蚁集团")
    parser.add_argument("--secondary-id", help="副 logo 的品牌 ID，例如 alipay")
    parser.add_argument("--secondary-alt", help="副 logo 的 alt 文案，例如 支付宝")
    args = parser.parse_args()

    defaults = DEFAULT_THEME_LOGOS.get(args.theme_id, {"primary_id": args.theme_id})

    if not args.primary_id:
        args.primary_id = defaults["primary_id"]
        args.primary_alt = args.primary_alt or defaults.get("primary_alt") or args.primary_id
        if args.secondary_id is None:
            args.secondary_id = defaults.get("secondary_id")
        if args.secondary_alt is None:
            args.secondary_alt = defaults.get("secondary_alt")
    elif not args.primary_alt:
        args.primary_alt = args.primary_id

    return args


def build_title(title: str, speaker: str | None) -> str:
    return f"{title} — {speaker}" if speaker else title


def load_theme_style(theme_id: str) -> str:
    if theme_id == "ant-group":
        return "<!-- %%THEME_STYLE%% -->"

    theme_path = ROOT_DIR / "themes" / f"{theme_id}.md"
    if not theme_path.exists():
        raise FileNotFoundError(f"theme file not found: {theme_path}")

    content = theme_path.read_text(encoding="utf-8")
    match = re.search(r"## CSS\s+```css\n(.*?)\n```", content, re.DOTALL)
    if not match:
        raise ValueError(f"CSS block not found in theme file: {theme_path}")

    css = match.group(1).strip()
    return f"<style>\n{css}\n</style>"


def read_logo_data_uri(brand_id: str, variant: str) -> str | None:
    path = LOGO_DIR / f"{brand_id}-{variant}.txt"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip() or None


def render_logo_img(css_class: str, src: str, alt: str, style: str | None = None) -> str:
    style_attr = f' style="{html.escape(style, quote=True)}"' if style else ""
    return (
        f'    <img class="{css_class}" src="{html.escape(src, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}"{style_attr}>'
    )


def render_logo_pair(brand_id: str, alt: str) -> list[str] | None:
    color_src = read_logo_data_uri(brand_id, "color")
    if not color_src:
        return None

    white_src = read_logo_data_uri(brand_id, "white")
    lines = [render_logo_img("logo-light", color_src, alt)]
    if white_src:
        lines.append(render_logo_img("logo-dark", white_src, alt))
    else:
        lines.append(
            render_logo_img(
                "logo-dark",
                color_src,
                alt,
                style="filter:brightness(0) invert(1);",
            )
        )
    return lines


def render_hidden_logo_group() -> str:
    return '<div id="globalLogoGroup" class="logo-group-single" style="display:none;"></div>'


def build_logo_block(
    primary_id: str,
    primary_alt: str,
    secondary_id: str | None = None,
    secondary_alt: str | None = None,
) -> tuple[str, list[str]]:
    warnings: list[str] = []

    primary_pair = render_logo_pair(primary_id, primary_alt)
    if not primary_pair:
        warnings.append(
            f"WARNING: missing required color logo: themes/logos/{primary_id}-color.txt; logo block hidden"
        )
        return render_hidden_logo_group(), warnings

    if secondary_id:
        secondary_pair = render_logo_pair(secondary_id, secondary_alt or secondary_id)
        if secondary_pair:
            lines = ['<div id="globalLogoGroup" class="logo-group-dual">']
            lines.extend(primary_pair)
            lines.append('    <span class="logo-divider"></span>')
            lines.extend(secondary_pair)
            lines.append("</div>")
            return "\n".join(lines), warnings

        warnings.append(
            f"WARNING: missing secondary color logo: themes/logos/{secondary_id}-color.txt; fallback to primary only"
        )

    lines = ['<div id="globalLogoGroup" class="logo-group-single">']
    lines.extend(primary_pair)
    lines.append("</div>")
    return "\n".join(lines), warnings


def main() -> int:
    args = parse_args()
    html_path = Path(args.html_file)
    if not html_path.is_absolute():
        html_path = ROOT_DIR / html_path
    if not html_path.exists():
        print(f"ERROR: file not found: {html_path}", file=sys.stderr)
        return 1

    html_text = html_path.read_text(encoding="utf-8")

    if not TITLE_RE.search(html_text):
        print("ERROR: <title> tag not found", file=sys.stderr)
        return 1
    if not THEME_STYLE_RE.search(html_text):
        print("ERROR: <!-- %%THEME_STYLE%% --> placeholder not found", file=sys.stderr)
        return 1

    final_title = build_title(args.title, args.speaker)
    theme_style = load_theme_style(args.theme_id)
    logo_block, warnings = build_logo_block(
        primary_id=args.primary_id,
        primary_alt=args.primary_alt,
        secondary_id=args.secondary_id,
        secondary_alt=args.secondary_alt,
    )

    updated = TITLE_RE.sub(f"<title>{final_title}</title>", html_text, count=1)
    updated = THEME_STYLE_RE.sub(theme_style, updated, count=1)
    if not LOGO_BLOCK_RE.search(updated):
        print("ERROR: #globalLogoGroup block not found", file=sys.stderr)
        return 1
    updated = LOGO_BLOCK_RE.sub(logo_block, updated, count=1)
    html_path.write_text(updated, encoding="utf-8")

    print(f"Updated branding in {html_path}")
    print(f"title: {final_title}")
    print(f"theme: {args.theme_id}")
    print(f"primary logo: {args.primary_id}")
    if args.secondary_id:
        print(f"secondary logo: {args.secondary_id}")
    for warning in warnings:
        print(warning, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
