"""Rebuild the evidence panel from the preserved before and current page PNGs.

This only lays out existing renders; it does not generate or retouch slide content.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

CASE = Path(__file__).resolve().parents[1]
AREA = CASE / 'source/imagegen-repair'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    left_path = AREA / 'slide-03-before.png'
    right_path = CASE / 'render/slide-03.png'
    left = Image.open(left_path).convert('RGB')
    right = Image.open(right_path).convert('RGB')
    right_size = right.size
    if right.size != left.size:
        right = right.resize(left.size, Image.Resampling.LANCZOS)
    panel = Image.new('RGB', (left.width * 2, left.height + 32), 'white')
    panel.paste(left, (0, 32))
    panel.paste(right, (left.width, 32))
    draw = ImageDraw.Draw(panel)
    font = ImageFont.truetype('arial.ttf', 20)
    draw.text((12, 4), 'BEFORE', fill='#182631', font=font)
    draw.text((left.width + 12, 4), 'AFTER — CURRENT POWERPOINT RENDER', fill='#182631', font=font)
    result = AREA / 'before-after-page-03.png'
    panel.save(result)
    record = {
        'left': left_path.relative_to(CASE).as_posix(),
        'left_sha256': sha(left_path),
        'right': right_path.relative_to(CASE).as_posix(),
        'right_sha256': sha(right_path),
        'comparison': result.relative_to(CASE).as_posix(),
        'comparison_sha256': sha(result),
        'composition': 'Preserved before pixels on the left; current PowerPoint render on the right, resized only to the left dimensions; 32px label row added.',
        'left_dimensions': list(left.size),
        'right_original_dimensions': list(right_size),
        'right_display_dimensions': list(right.size),
        'generator': 'source/build_repair_comparison.py',
        'slide_content_modified': False,
    }
    (AREA / 'comparison.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record, ensure_ascii=False))

if __name__ == '__main__':
    main()
