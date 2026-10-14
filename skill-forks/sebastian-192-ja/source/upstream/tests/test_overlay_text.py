import json
import subprocess
import sys
from pathlib import Path

import overlay_text
import pytest
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "overlay_text.py"


def find_test_font() -> str:
    for candidate in (
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ):
        if Path(candidate).exists():
            return candidate
    pytest.skip("no system font available")


def find_cjk_font():
    for candidate in (
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ):
        if Path(candidate).exists():
            return candidate
    return None


def run_overlay(spec_path: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(spec_path), *extra],
        capture_output=True,
        text=True,
        check=False,
    )


def write_spec(tmp_path: Path, spec: dict) -> Path:
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    return spec_path


def test_renders_text_on_background(tmp_path):
    Image.new("RGB", (800, 450), "#FFFFFF").save(tmp_path / "bg.png")
    spec = {
        "pages": [
            {
                "background": "bg.png",
                "output": "out/01.png",
                "texts": [
                    {
                        "text": "Hello PPT",
                        "x": 0.1,
                        "y": 0.1,
                        "w": 0.8,
                        "h": 0.3,
                        "font_size": 64,
                        "color": "#000000",
                        "align": "center",
                        "valign": "center",
                    }
                ],
            }
        ]
    }
    proc = run_overlay(write_spec(tmp_path, spec), "--font", find_test_font())
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["pages"] == 1
    output = tmp_path / "out" / "01.png"
    assert output.is_file()
    with Image.open(output) as image:
        assert image.size == (800, 450)
        region = image.crop((80, 45, 720, 180))
        assert len(region.getcolors(maxcolors=100000)) > 1


def test_solid_color_page(tmp_path):
    spec = {
        "pages": [
            {
                "background": "#10233A",
                "width": 640,
                "height": 360,
                "output": "01.png",
                "texts": [
                    {
                        "text": "12",
                        "x": 0.8,
                        "y": 0.9,
                        "w": 0.15,
                        "h": 0.08,
                        "font_size": 24,
                        "color": "#FFFFFF",
                    }
                ],
            }
        ]
    }
    proc = run_overlay(write_spec(tmp_path, spec), "--font", find_test_font())
    assert proc.returncode == 0, proc.stderr
    with Image.open(tmp_path / "01.png") as image:
        assert image.size == (640, 360)
        assert image.getpixel((5, 5)) == (16, 35, 58)


def test_wrap_text_breaks_long_lines():
    image = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(find_test_font(), 20)
    text = "the quick brown fox jumps over the lazy dog"
    lines = overlay_text.wrap_text(draw, text, font, 120)
    assert len(lines) > 1
    assert " ".join(lines).split() == text.split()
    for line in lines:
        assert draw.textlength(line, font=font) <= 120


def test_renders_chinese_text(tmp_path):
    cjk_font = find_cjk_font()
    if cjk_font is None:
        pytest.skip("no CJK font available")
    Image.new("RGB", (800, 450), "#FFFFFF").save(tmp_path / "bg.png")
    spec = {
        "pages": [
            {
                "background": "bg.png",
                "output": "01.png",
                "texts": [
                    {
                        "text": "核心结论：增长 32%",
                        "x": 0.08,
                        "y": 0.36,
                        "w": 0.84,
                        "h": 0.2,
                        "font_size": 64,
                        "color": "#10233A",
                        "align": "center",
                        "valign": "center",
                        "bold": True,
                    }
                ],
            }
        ]
    }
    proc = run_overlay(write_spec(tmp_path, spec), "--font", cjk_font)
    assert proc.returncode == 0, proc.stderr
    with Image.open(tmp_path / "01.png") as image:
        region = image.crop((64, 162, 736, 252))
        assert len(region.getcolors(maxcolors=100000)) > 1


def test_multiline_text_renders_multiple_rows(tmp_path):
    font = find_test_font()
    Image.new("RGB", (800, 450), "#FFFFFF").save(tmp_path / "bg.png")
    spec = {
        "pages": [
            {
                "background": "bg.png",
                "output": "01.png",
                "texts": [
                    {
                        "text": "line one\nline two\nline three",
                        "x": 0.1,
                        "y": 0.1,
                        "w": 0.8,
                        "h": 0.5,
                        "font_size": 48,
                        "color": "#000000",
                    }
                ],
            }
        ]
    }
    proc = run_overlay(write_spec(tmp_path, spec), "--font", font)
    assert proc.returncode == 0, proc.stderr
    with Image.open(tmp_path / "01.png") as image:
        # three rows of ~48px text at spacing 1.25 -> dark pixels span > 150px vertically
        rows = [
            y
            for y in range(45, 300)
            if any(image.getpixel((x, y)) != (255, 255, 255) for x in range(80, 720))
        ]
        assert rows
        assert rows[-1] - rows[0] > 100


def test_rejects_invalid_color(tmp_path):
    spec = {
        "pages": [
            {
                "background": "#FFFFFF",
                "width": 640,
                "height": 360,
                "output": "01.png",
                "texts": [
                    {"text": "x", "x": 0.1, "y": 0.1, "w": 0.5, "h": 0.2, "color": "#XYZ"}
                ],
            }
        ]
    }
    proc = run_overlay(write_spec(tmp_path, spec))
    assert proc.returncode != 0
    assert "color" in proc.stderr


def test_rejects_box_outside_page(tmp_path):
    spec = {
        "pages": [
            {
                "background": "#FFFFFF",
                "width": 640,
                "height": 360,
                "output": "01.png",
                "texts": [
                    {"text": "x", "x": 0.9, "y": 0.1, "w": 0.5, "h": 0.2}
                ],
            }
        ]
    }
    proc = run_overlay(write_spec(tmp_path, spec))
    assert proc.returncode != 0
    assert "exceeds" in proc.stderr


def test_rejects_missing_text_field(tmp_path):
    spec = {"pages": [{"background": "#FFFFFF", "width": 640, "height": 360, "output": "01.png", "texts": [{"x": 0.1, "y": 0.1, "w": 0.5, "h": 0.2}]}]}
    proc = run_overlay(write_spec(tmp_path, spec))
    assert proc.returncode != 0
    assert "text" in proc.stderr


def test_rejects_vertical_overflow_without_writing_page(tmp_path):
    spec = {"pages": [{"background": "#FFFFFF", "width": 640, "height": 360,
                       "output": "01.png", "texts": [{"text": "long line\nsecond line", "x": 0.1,
                       "y": 0.1, "w": 0.8, "h": 0.05, "font_size": 48}]}]}
    proc = run_overlay(write_spec(tmp_path, spec), "--font", find_test_font())
    assert proc.returncode != 0
    assert "overflows its box" in proc.stderr
    assert not (tmp_path / "01.png").exists()


def test_defaults_apply_across_pages(tmp_path):
    font = find_test_font()
    Image.new("RGB", (800, 450), "#F0F0F0").save(tmp_path / "bg.png")
    spec = {
        "defaults": {"color": "#FF0000", "font_size": 40, "align": "center", "valign": "center"},
        "pages": [
            {
                "background": "bg.png",
                "output": "01.png",
                "texts": [{"text": "RED", "x": 0.2, "y": 0.4, "w": 0.6, "h": 0.2}],
            }
        ],
    }
    proc = run_overlay(write_spec(tmp_path, spec), "--font", font)
    assert proc.returncode == 0, proc.stderr
    with Image.open(tmp_path / "01.png") as image:
        colors = image.crop((160, 180, 640, 270)).getcolors(maxcolors=100000)
        reds = [count for count, color in colors if color[0] > 180 and color[1] < 90 and color[2] < 90]
        assert reds, f"expected red text pixels, got {colors[:5]}"
