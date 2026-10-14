import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from audit_chart_geometry import audit, template
from build_chart_image import render
from PIL import Image, ImageChops
from render_deck import sha256


@pytest.fixture
def chart_case(tmp_path):
    spec = json.loads((Path(__file__).resolve().parents[1] / "examples/page-spec.example.json").read_text(encoding="utf-8"))
    slide = spec["slides"][0]
    slide["elements"].append({"id": "bars", "kind": "chart", "role": "evidence", "native_intent": "native",
                              "source_ref": "table-1", "confirmation_status": "source-verified",
                              "data": {"chart_type": "bar", "categories": ["A", "B", "C"],
                                       "series": [{"name": "change", "values": [3.2, -5.5, 0]}], "unit": "%"}})
    path = tmp_path / "page-spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    image = tmp_path / slide["image_file"]
    image.parent.mkdir()
    Image.new("RGBA", (1200, 675), (12, 34, 56, 123)).save(image)
    observed = template(path, spec)
    observed["charts"][0].update(status="complete", axis=[{"value": -6, "pixel": 200}, {"value": 4, "pixel": 700}],
                                 bars=[{"category": "A", "start": 500, "end": 660},
                                       {"category": "B", "start": 500, "end": 225},
                                       {"category": "C", "start": 500, "end": 500}])
    observation = tmp_path / "geometry.json"
    observation.write_text(json.dumps(observed), encoding="utf-8")
    return path, spec, observation, observed, image


def test_geometry_rejects_wrong_length_despite_correct_source_values(chart_case):
    path, _, observation, observed, _ = chart_case
    assert audit(path, observation)["status"] == "pass"
    observed["charts"][0]["bars"][0]["end"] = 600
    observation.write_text(json.dumps(observed), encoding="utf-8")
    result = audit(path, observation)
    assert result["status"] == "fail"
    assert result["failed"][0]["value"] == 3.2
    assert result["failed"][0]["max_error_px"] == 60


@pytest.mark.parametrize("mutation", ["zero", "direction", "pending", "missing", "stale-image", "stale-spec", "duplicate", "nan", "unknown"])
def test_geometry_missing_invalid_or_stale_cannot_pass(chart_case, mutation):
    path, spec, observation, observed, image = chart_case
    entry = observed["charts"][0]
    if mutation == "zero":
        entry["bars"][0]["start"] = 480
    elif mutation == "direction":
        entry["bars"][1]["end"] = 775
    elif mutation == "pending":
        entry["status"] = "pending"
    elif mutation == "missing":
        observed["charts"] = []
    elif mutation == "stale-image":
        Image.new("RGB", (1200, 675), "white").save(image)
    elif mutation == "stale-spec":
        spec["content_version"] = "changed"
        path.write_text(json.dumps(spec), encoding="utf-8")
    elif mutation == "duplicate":
        observed["charts"].append(copy.deepcopy(entry))
    elif mutation == "nan":
        entry["bars"][0]["end"] = float("nan")
    else:
        entry["element_id"] = "invented"
    observation.write_text(json.dumps(observed), encoding="utf-8")
    if mutation in ("stale-image", "stale-spec", "duplicate", "nan", "unknown"):
        with pytest.raises(ValueError):
            audit(path, observation)
    else:
        assert audit(path, observation)["status"] in ("fail", "incomplete")


def test_column_upward_axis_is_checked_from_its_observed_anchors(chart_case):
    path, spec, observation, observed, _ = chart_case
    spec["slides"][0]["elements"][-1]["data"]["chart_type"] = "column"
    path.write_text(json.dumps(spec), encoding="utf-8")
    observed["page_spec_sha256"] = sha256(path)
    observed["charts"][0].update(axis=[{"value": -6, "pixel": 600}, {"value": 4, "pixel": 100}],
                                  bars=[{"category": "A", "start": 300, "end": 140},
                                        {"category": "B", "start": 300, "end": 575},
                                        {"category": "C", "start": 300, "end": 300}])
    observation.write_text(json.dumps(observed), encoding="utf-8")
    assert audit(path, observation)["status"] == "pass"


def layout_for(chart_case):
    path, spec, _, _, image = chart_case
    layout = {"slide_id": spec["slides"][0]["id"], "element_id": "bars", "region": [100, 100, 850, 450],
              "plot": [150, 30, 600, 330], "axis_min": -8, "axis_max": 5, "ticks": [-8, -4, 0, 5],
              "font_size": 20, "decimals": 1, "signed": True, "suffix": "%", "source_sha256": sha256(image)}
    layout_path = path.parent / "layout.json"
    layout_path.write_text(json.dumps(layout), encoding="utf-8")
    return layout_path, layout


def test_precise_replacement_preserves_all_pixels_outside_region(chart_case):
    path, _, _, _, image = chart_case
    layout_path, layout = layout_for(chart_case)
    output = path.parent / "fixed.png"
    original_hash = sha256(image)
    report = render(path, layout_path, output, replace_region=True)
    assert sha256(image) == original_hash
    assert report["construction_geometry"][1]["end"] < report["construction_geometry"][1]["start"]
    with Image.open(image) as before, Image.open(output) as after:
        x, y, w, h = layout["region"]
        restored = after.copy()
        restored.paste(before.crop((x, y, x + w, y + h)), (x, y))
        assert ImageChops.difference(before, restored).getbbox() is None
        assert before.getpixel((x + 1, y + 1)) != after.getpixel((x + 1, y + 1))


@pytest.mark.parametrize("mutation", ["stale", "outside", "axis", "label-overflow", "overwrite"])
def test_fallback_rejects_invalid_replacement_without_modifying_existing_file(chart_case, mutation):
    path, _, _, _, image = chart_case
    layout_path, layout = layout_for(chart_case)
    output = path.parent / "existing.png"
    output.write_bytes(b"existing")
    if mutation == "stale":
        layout["source_sha256"] = "stale"
    elif mutation == "outside":
        layout["region"][0] = 1000
    elif mutation == "axis":
        layout["axis_min"] = -1
    elif mutation == "label-overflow":
        layout["font_size"] = 500
    else:
        output = image
    layout_path.write_text(json.dumps(layout), encoding="utf-8")
    original = output.read_bytes()
    with pytest.raises(ValueError):
        render(path, layout_path, output, replace_region=True)
    assert output.read_bytes() == original


@pytest.mark.parametrize("orientation", ["bar", "column"])
def test_grouped_geometry_distinguishes_series_and_measures_real_pixels(chart_case, orientation):
    path, spec, observation, _, _ = chart_case
    data = spec["slides"][0]["elements"][-1]["data"]
    data.update(chart_type=orientation, categories=["A", "B"])
    data["series"] = [{"name": "Before", "values": [3, -2]}, {"name": "After", "values": [4, 0]}]
    path.write_text(json.dumps(spec), encoding="utf-8")
    layout_path, layout = layout_for(chart_case)
    layout.update(plot=[130, 65, 560, 270], axis_min=-4, axis_max=6, ticks=[-4, 0, 6],
                  decimals=0, signed=False, suffix="", series_colors=["#ff0000", "#0000ff"])
    layout_path.write_text(json.dumps(layout), encoding="utf-8")
    output = path.parent / "grouped.png"
    report = render(path, layout_path, output)
    spec["slides"][0]["image_file"] = output.name
    path.write_text(json.dumps(spec), encoding="utf-8")
    observations = template(path, spec)
    entry = observations["charts"][0]
    entry["status"] = "complete"
    # Independently fixed axis coordinates from the configured region and scale.
    entry["axis"] = ([{"value": -4, "pixel": 130}, {"value": 6, "pixel": 690}] if orientation == "bar"
                     else [{"value": -4, "pixel": 335}, {"value": 6, "pixel": 65}])
    zero = 354 if orientation == "bar" else 227
    with Image.open(output) as image:
        for index, bar in enumerate(entry["bars"]):
            cross = round(report["construction_geometry"][index]["cross_center"])
            color = (255, 0, 0) if bar["series"] == "Before" else (0, 0, 255)
            pixels = [p for p in range(850 if orientation == "bar" else 450)
                      if image.getpixel((p, cross) if orientation == "bar" else (cross, p)) == color]
            value = data["series"][index % 2]["values"][index // 2]
            bar["start"] = zero
            bar["end"] = (max(pixels) if (value > 0) == (orientation == "bar") else min(pixels)) if value else zero
    observation.write_text(json.dumps(observations), encoding="utf-8")
    assert audit(path, observation)["status"] == "pass"
    entry["bars"][0]["end"] = zero  # Correct values cannot hide a missing real bar.
    observation.write_text(json.dumps(observations), encoding="utf-8")
    assert audit(path, observation)["status"] == "fail"
    entry["bars"][0]["series"] = "After"
    observation.write_text(json.dumps(observations), encoding="utf-8")
    with pytest.raises(ValueError, match="category and series"):
        audit(path, observation)


@pytest.mark.parametrize("mutation", ["duplicate-series", "stacked", "axis-direction", "color-shortage", "nan-value"])
def test_grouped_invalid_data_and_axes_are_rejected(chart_case, mutation):
    path, spec, observation, observed, _ = chart_case
    data = spec["slides"][0]["elements"][-1]["data"]
    if mutation == "axis-direction":
        observed["charts"][0]["axis"] = [{"value": -6, "pixel": 700}, {"value": 4, "pixel": 200}]
        observation.write_text(json.dumps(observed), encoding="utf-8")
        with pytest.raises(ValueError, match="direction"):
            audit(path, observation)
        return
    if mutation == "duplicate-series":
        data["series"].append(copy.deepcopy(data["series"][0]))
    elif mutation == "stacked":
        data["stacked"] = True
    elif mutation == "nan-value":
        data["series"][0]["values"][0] = float("nan")
    else:
        data["series"].append({"name": "Other", "values": [1, 2, 3]})
    path.write_text(json.dumps(spec), encoding="utf-8")
    layout_path, layout = layout_for(chart_case)
    if mutation == "color-shortage":
        layout["series_colors"] = ["#ff0000"]
        layout_path.write_text(json.dumps(layout), encoding="utf-8")
    with pytest.raises(ValueError):
        render(path, layout_path, path.parent / "invalid.png")


def test_chart_report_cannot_overwrite_input_before_rendering(chart_case):
    path, _, _, _, image = chart_case
    layout_path, _ = layout_for(chart_case)
    output = path.parent / "new.png"
    original = image.read_bytes()
    result = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/build_chart_image.py"),
                             str(path), str(layout_path), str(output), "--report", str(image)],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "Report must not overwrite" in result.stderr
    assert not output.exists()
    assert image.read_bytes() == original
