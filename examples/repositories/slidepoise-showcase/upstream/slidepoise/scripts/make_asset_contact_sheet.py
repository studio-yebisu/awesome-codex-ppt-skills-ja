#!/usr/bin/env python3
"""Create the SlidePoise generation context sheet or resource review sheet.

The full-resource sheet can be inspected in conversation and passed to the image
model. It covers visual references, component previews, retrieved assets, and user
uploads. The script never chooses resources or changes artwork.
"""
from __future__ import annotations

import argparse
import io
import json
import textwrap
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from resvg_py import svg_to_bytes
from inspect_asset import svg_dimensions


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
        Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf'),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def _svg_to_image(path: Path, size: int) -> Image.Image | None:
    try:
        width, height = svg_dimensions(path)
        if not width or not height:
            return None
        scale = size / max(width, height)
        output_width, output_height = max(1, round(width * scale)), max(1, round(height * scale))
    except (ValueError, OSError, SyntaxError, OverflowError):
        return None
    try:
        data = svg_to_bytes(svg_path=str(path), width=output_width, height=output_height)
        return Image.open(io.BytesIO(data)).convert('RGBA')
    except (ValueError, OSError):
        return None


def _load_preview(path: Path, size: int) -> Image.Image | None:
    if not path.is_file():
        return None
    if path.suffix.lower() == '.svg':
        return _svg_to_image(path, size)
    try:
        return Image.open(path).convert('RGBA')
    except Exception:
        return None


def _contain(image: Image.Image, width: int, height: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    x = (width - copy.width) // 2
    y = (height - copy.height) // 2
    canvas.alpha_composite(copy, (x, y))
    return canvas


def _asset_path(record: dict[str, Any]) -> Path | None:
    internal = record.get('internal') if isinstance(record.get('internal'), dict) else record
    value = None
    if isinstance(internal, dict):
        value = internal.get('canonical_file') or internal.get('preview_file')
    return Path(str(value)).expanduser().resolve() if value else None


def _catalog_items(path: Path) -> dict[str, dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}
    items = payload.get('items') or {}
    if isinstance(items, dict):
        return {str(key): dict(value) for key, value in items.items() if isinstance(value, dict)}
    if isinstance(items, list):
        return {str(value.get('id')): dict(value) for value in items if isinstance(value, dict) and value.get('id')}
    return {}


def collect_resource_review_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    root = Path(__file__).resolve().parents[1]
    ref_catalog = _catalog_items(root / 'assets' / 'visual_references' / 'catalog.json')
    component_catalog = _catalog_items(root / 'assets' / 'components' / 'catalog.json')
    for index, record in enumerate(payload.get('selected_visual_references') or [], start=1):
        ref_id = str(record.get('id') or '')
        catalog = ref_catalog.get(ref_id) or next((value for value in ref_catalog.values() if str(value.get('id')) == ref_id), {})
        file_value = record.get('canonical_file')
        if not file_value and catalog.get('path'):
            file_value = root / 'assets' / 'visual_references' / str(catalog.get('path'))
        items.append({
            'asset_id': ref_id or f'visual-reference-{index}',
            'contact_sheet_label': f'R{index:02d}',
            'canonical_file': str(file_value) if file_value else None,
            'role': f"Visual reference. {record.get('reason') or catalog.get('description') or ref_id or 'Selected precedent'}",
        })
    for index, record in enumerate(payload.get('selected_components') or [], start=1):
        component_id = str(record.get('component_id') or '')
        catalog = component_catalog.get(component_id) or next((value for value in component_catalog.values() if str(value.get('id')) == component_id), {})
        file_value = record.get('preview_file')
        if not file_value and catalog.get('preview_path'):
            file_value = root / 'assets' / 'components' / str(catalog.get('preview_path'))
        items.append({
            'asset_id': component_id or f'component-{index}',
            'contact_sheet_label': f'C{index:02d}',
            'canonical_file': str(file_value) if file_value else None,
            'role': f"Component precedent. {record.get('reason') or catalog.get('description') or component_id or 'Selected component'}",
        })
    for index, record in enumerate(payload.get('selected_assets') or [], start=1):
        copy = dict(record)
        copy['contact_sheet_label'] = f'A{index:02d}'
        source = ('User upload' if record.get('source') == 'current_chat_upload' else
                  'Required asset' if record.get('user_required') or record.get('required_for_slide') else 'Selected asset')
        copy['role'] = f"{source}. {record.get('role') or record.get('asset_id') or 'Asset'}"
        items.append(copy)
    return items


def _style_header(width: int, context: dict[str, Any], direction: Any = None) -> Image.Image:
    """Typeset the supplied style snapshot. This is a review board, never a slide design."""
    style = context.get('design', {}).get('style', {})
    agency = context.get('style_agency', {})
    profile = context.get('profile', {})
    modes = {'specified': 'Defined', 'guided': 'Starting point', 'agent_decides': 'Open',
             'agent_decides_from_references': 'From references', 'agent_decides_within_profile': 'Open within the profile'}
    lines = []
    y = 24
    measure = ImageDraw.Draw(Image.new('RGB', (1, 1)))

    def add(text, size=18, bold=False, color='#424247'):
        nonlocal y
        font = _font(size, bold)
        # Wrap by measured glyph width, including content without spaces.
        line = ''
        for char in str(text):
            if char == '\n' or (line and measure.textlength(line + char, font=font) > width - 64):
                lines.append((line, y, font, color))
                y += size + 9
                line = ''
            if char != '\n':
                line += char
        if line:
            lines.append((line, y, font, color))
            y += size + 9
        y += 6

    add('STYLE & ASSETS', 16, True, '#77777D')
    add(profile.get('name') or 'Visual direction', 30, True, '#202024')
    if profile.get('purpose'):
        add(profile['purpose'])
    add('Palette  /  ' + modes.get(agency.get('palette'), 'Guided'))
    swatches = []
    colors = list(style.get('accent_colors') or [])
    if style.get('background'):
        colors.append(style['background'])
    x = 32
    for color in dict.fromkeys(colors):
        if x + 126 > width - 32:
            x = 32
            y += 60
        swatches.append((x, y, color))
        x += 126
    if swatches:
        y += 66
    add(f"Typography  /  {style.get('display_font') or 'Open'} + {style.get('body_font') or 'Open'}  /  {modes.get(agency.get('typography'), 'Guided')}")
    density = str(style.get('density') or 'Open').replace('_', ' ')
    add(f"Density  /  {density}  /  {modes.get(agency.get('density'), 'Guided')}")
    treatment = str(style.get('icon_treatment') or 'agent_decides').replace('_', ' ')
    add(f"Icons  /  {treatment}  /  {modes.get(agency.get('icon_treatment'), 'Guided')}")

    def describe(value, prefix=''):
        if isinstance(value, dict):
            for key, item in value.items():
                describe(item, str(key).replace('_', ' ').capitalize() + '  /  ')
        elif isinstance(value, list):
            for item in value:
                describe(item, prefix)
        elif value is not None and value != '':
            add(prefix + str(value))
    if direction:
        y += 6
        add('Direction for this slide', 20, True)
        describe(direction)
    add('Style samples and reference material, not slide content or a prescribed layout.', 15, color='#77777D')
    y += 10
    add('REFERENCES & ASSETS', 16, True, '#77777D')
    canvas = Image.new('RGB', (width, y + 8), '#F6F6F8')
    draw = ImageDraw.Draw(canvas)
    for line, top, font, color in lines:
        draw.text((32, top), line, font=font, fill=color)
    for left, top, color in swatches:
        draw.rounded_rectangle((left, top, left + 106, top + 28), radius=5, fill=color, outline='#D0D0D5')
        draw.text((left, top + 33), color, font=_font(14), fill='#505058')
    return canvas


def build_contact_sheet(
    assets: list[dict[str, Any]],
    output: Path,
    *,
    columns: int = 4,
    style_context: dict[str, Any] | None = None,
    style_direction: Any = None,
) -> dict[str, Any]:
    output = output.resolve()
    cell_w, cell_h = 330, 260
    preview_size = 150
    margin = 24
    columns = max(1, min(columns, max(1, len(assets))))
    rows = max(0 if style_context else 1, (len(assets) + columns - 1) // columns)
    width = margin * 2 + max(3 if style_context else 1, columns) * cell_w
    header = _style_header(width, style_context, style_direction) if style_context else None
    offset = header.height if header else 0
    canvas = Image.new('RGB', (width, offset + margin * 2 + rows * cell_h), 'white')
    if header:
        canvas.paste(header, (0, 0))
    draw = ImageDraw.Draw(canvas)
    label_font = _font(18, bold=True)
    role_font = _font(14, bold=False)
    skipped: list[str] = []
    rendered = 0
    labels: dict[str, str] = {}

    for index, asset in enumerate(assets):
        asset_id = str(asset.get('asset_id') or f'asset-{index+1}')
        label = str(asset.get('contact_sheet_label') or f'A{index+1:02d}')
        labels[asset_id] = label
        row, col = divmod(index, columns)
        left = margin + col * cell_w
        top = offset + margin + row * cell_h
        draw.rectangle((left, top, left + cell_w - 10, top + cell_h - 10), outline=(220, 220, 220), width=1)
        draw.text((left + 12, top + 10), label, fill='black', font=label_font)
        role = str(asset.get('role') or asset_id)
        role_lines = textwrap.wrap(role, width=38)[:2] or [role]
        for line_index, line in enumerate(role_lines):
            draw.text((left + 12, top + 38 + line_index * 18), line, fill=(70, 70, 70), font=role_font)

        path = _asset_path(asset)
        preview = _load_preview(path, preview_size) if path else None
        if preview is None:
            if path and path.suffix.lower() == '.svg':
                raise RuntimeError(f'Unable to render real SVG preview for {asset_id}: {path}. Install CairoSVG or an SVG renderer; do not substitute an SVG placeholder.')
            skipped.append(asset_id)
            draw.text((left + 24, top + 118), 'visual preview unavailable', fill=(120, 120, 120), font=role_font)
            continue
        fitted = _contain(preview, cell_w - 40, preview_size)
        canvas.paste(fitted, (left + 15, top + 82), fitted)
        rendered += 1


    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return {
        'path': str(output),
        'asset_count': len(assets),
        'rendered_preview_count': rendered,
        'skipped_preview_asset_ids': skipped,
        'labels': labels,
        'includes_style_context': bool(style_context),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--resources', type=Path, required=True, help='resource-selection JSON containing selected_assets')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--columns', type=int, default=4)
    parser.add_argument('--review-all-resources', action='store_true', help='Include selected references, component previews, retrieved/packaged assets, and user uploads in the generation context sheet')
    args = parser.parse_args()
    payload = json.loads(args.resources.read_text(encoding='utf-8'))
    assets = collect_resource_review_items(payload) if args.review_all_resources else list(payload.get('selected_assets') or [])
    result = build_contact_sheet(assets, args.output, columns=args.columns)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
