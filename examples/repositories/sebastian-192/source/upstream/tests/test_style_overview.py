import json

import pytest
from build_style_overview import build_overview
from PIL import Image


@pytest.fixture
def overview_spec(tmp_path):
    # A misplaced vertical strip with real gutters: crops must be explicit.
    strip = Image.new("RGB", (160, 300), "black")
    colors = ["red", "green", "blue"]
    slides = []
    for index, color in enumerate(colors):
        strip.paste(Image.new("RGB", (160, 90), color), (0, index * 100))
        slides.append({"file": "strip.png", "box": [0, index * 100, 160, 90]})
    strip.save(tmp_path / "strip.png")
    path = tmp_path / "overview.json"
    path.write_text(json.dumps({"title": "Option 1", "slides": slides}), encoding="utf-8")
    return path


def test_three_crops_form_grid_without_changing_pixels_or_sources(overview_spec):
    original = (overview_spec.parent / "strip.png").read_bytes()
    result = build_overview(overview_spec, overview_spec.with_suffix(".png"))
    assert result["image_generation_calls"] == 0
    assert len(result["tiles"]) == 3
    first, second, third = [item["box"] for item in result["tiles"]]
    assert first[1] == second[1] and first[0] == third[0]
    assert second[0] > first[0] and third[1] > first[1]
    with Image.open(result["output"]) as image:
        assert image.size == (1600, 900)
        for (x, y, w, h), color in zip([first, second, third], [(255, 0, 0), (0, 128, 0), (0, 0, 255)]):
            assert image.getpixel((x + w // 2, y + h // 2)) == color
        assert image.getpixel((second[0] + second[2] // 2, third[1] + third[3] // 2)) == (235, 237, 240)
    assert (overview_spec.parent / "strip.png").read_bytes() == original


@pytest.mark.parametrize("mutation", ["outside", "overwrite_source", "existing", "traversal"])
def test_invalid_crop_or_overwrite_rejected(overview_spec, mutation):
    spec = json.loads(overview_spec.read_text())
    output = overview_spec.with_suffix(".png")
    if mutation == "outside":
        spec["slides"][0]["box"] = [0, 0, 999, 90]
    elif mutation == "traversal":
        spec["slides"][0]["file"] = "../strip.png"
    elif mutation == "overwrite_source":
        output = overview_spec.parent / "strip.png"
    elif mutation == "existing":
        output.write_bytes(b"previous")
    overview_spec.write_text(json.dumps(spec), encoding="utf-8")
    with pytest.raises(ValueError):
        build_overview(overview_spec, output, overwrite=mutation == "overwrite_source")
    if mutation == "existing":
        assert output.read_bytes() == b"previous"


@pytest.mark.parametrize("count", [1, 2, 6, 8])
def test_layout_count_and_bounds(overview_spec, count):
    spec = json.loads(overview_spec.read_text())
    spec["slides"] = [spec["slides"][0]] * count
    spec["slide_aspect_ratio"] = [4, 3]
    overview_spec.write_text(json.dumps(spec), encoding="utf-8")
    result = build_overview(overview_spec, overview_spec.with_suffix(".png"))
    assert len(result["tiles"]) == count
    for tile in result["tiles"]:
        x, y, w, h = tile["box"]
        assert 0 <= x < x + w <= 1600
        assert 0 <= y < y + h < 900
        assert w / h == pytest.approx(4 / 3, abs=0.01)
