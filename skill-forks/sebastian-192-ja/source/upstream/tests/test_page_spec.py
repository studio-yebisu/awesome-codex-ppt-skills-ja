import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image
from validate_page_spec import load_page_spec, validate_page_spec


@pytest.fixture
def page_spec(tmp_path):
    spec = {
        "version": "1.0",
        "title": "Test deck",
        "content_approved": True,
        "content_version": "outline-v1",
        "content_authorization": "User approved outline v1",
        "canvas": {"width": 1600, "height": 900},
        "style": {
            "decision": "selected",
            "authorization": "User selected option 1",
            "visual_spec": "Clean editorial",
        },
        "slides": [
            {
                "id": "s01",
                "page_number": 1,
                "title": "Accurate title",
                "core_message": "One conclusion",
                "visual_brief": "Title left, image right",
                "image_file": "slides/01.png",
                "image_status": "pending",
                "elements": [
                    {
                        "id": "title",
                        "kind": "text",
                        "role": "heading",
                        "native_intent": "native",
                        "source_ref": "report p1",
                        "confirmation_status": "confirmed",
                        "text": "Accurate title",
                        "bbox_hint": [100, 80, 800, 120],
                    }
                ],
            }
        ],
    }
    path = tmp_path / "page-spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    return path


def test_example_is_valid():
    path = Path(__file__).resolve().parents[1] / "examples/page-spec.example.json"
    _, result = load_page_spec(path)
    assert result == {"slides": 1, "elements": 3, "unresolved": 0}


def test_requires_approval_and_existing_images(page_spec):
    spec, _ = load_page_spec(page_spec)
    spec["slides"][0]["image_status"] = "approved"
    page_spec.write_text(json.dumps(spec), encoding="utf-8")
    with pytest.raises(ValueError, match="Missing approved slide image"):
        load_page_spec(page_spec, require_images=True)
    image = page_spec.parent / "slides/01.png"
    image.parent.mkdir()
    Image.new("RGB", (16, 9), "white").save(image)
    _, result = load_page_spec(page_spec, require_images=True)
    assert result["slides"] == 1


@pytest.mark.parametrize("rotated", [False, True])
def test_approved_image_ratio_allows_pixel_rounding_and_exif(page_spec, rotated):
    spec, _ = load_page_spec(page_spec)
    slide = spec["slides"][0]
    slide.update(image_status="approved", image_file="slides/01.jpg")
    target = page_spec.parent / slide["image_file"]
    target.parent.mkdir()
    exif = Image.Exif()
    if rotated:
        exif[0x0112] = 6
    size = (941, 1672) if rotated else (1672, 941)
    Image.new("RGB", size, "white").save(target, exif=exif)
    assert validate_page_spec(spec, page_spec.parent, require_images=True, strict=True)["slides"] == 1


@pytest.mark.parametrize("mutation", ["approval", "duplicate", "outside", "traversal"])
def test_invalid_page_spec_rejected(page_spec, mutation):
    spec, _ = load_page_spec(page_spec)
    if mutation == "approval":
        spec["content_approved"] = False
    elif mutation == "duplicate":
        spec["slides"][0]["elements"].append(
            copy.deepcopy(spec["slides"][0]["elements"][0])
        )
    elif mutation == "outside":
        spec["slides"][0]["elements"][0]["bbox_hint"] = [1500, 20, 200, 50]
    elif mutation == "traversal":
        spec["slides"][0]["image_file"] = "../outside.png"
    with pytest.raises(ValueError):
        validate_page_spec(spec, page_spec.parent)


def test_cli_from_other_working_directory(page_spec, tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts/validate_page_spec.py"
    result = subprocess.run(
        [sys.executable, str(script), str(page_spec)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "1 slides, 1 semantic elements, 0 unresolved" in result.stdout


def test_strict_rejects_unresolved(page_spec):
    spec, _ = load_page_spec(page_spec)
    spec["slides"][0]["elements"][0]["confirmation_status"] = "unresolved"
    spec["slides"][0]["elements"][0]["confidence"] = 0.5
    assert validate_page_spec(spec, page_spec.parent)["unresolved"] == 1
    with pytest.raises(ValueError, match="1 unresolved"):
        validate_page_spec(spec, page_spec.parent, strict=True)


def test_style_reference_must_exist_inside_task(page_spec):
    spec, _ = load_page_spec(page_spec)
    spec["style"]["tokens"] = {
        "palette": {"background": "#FFFFFF", "text": "#111111", "primary": "#123456", "accent": "#ABCDEF"},
        "typography": {"heading_font": "Arial", "body_font": "Arial", "heading_size": 50, "body_size": 24},
        "layout": {"grid": "two columns", "margin_px": 100, "spacing_px": 24},
        "image_treatment": "soft light", "reference_images": ["styles/selected.png"],
    }
    with pytest.raises(ValueError, match="Missing style reference"):
        validate_page_spec(spec, page_spec.parent)
    target = page_spec.parent / "styles/selected.png"
    target.parent.mkdir()
    Image.new("RGB", (16, 9), "white").save(target)
    assert validate_page_spec(spec, page_spec.parent)["slides"] == 1
    spec["style"]["tokens"]["reference_images"] = ["../outside.png"]
    with pytest.raises(ValueError, match="inside Page Spec directory"):
        validate_page_spec(spec, page_spec.parent)
