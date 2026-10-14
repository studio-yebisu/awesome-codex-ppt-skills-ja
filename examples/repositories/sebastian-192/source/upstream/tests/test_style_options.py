import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image
from validate_style_options import validate_style_options


@pytest.fixture
def choices(tmp_path):
    pages = ["s01", "s02", "s03"]
    options = []
    for number in range(1, 5):
        name = f"option-{number}.png"
        Image.new("RGB", (160, 90), (number * 40, 20, 60)).save(tmp_path / name)
        options.append({"option": number, "file": name, "slide_ids": pages[:]})
    return {"version": "1.0", "total_pages": 3, "representative_pages": pages, "options": options}


def test_four_current_candidates_pass(choices, tmp_path):
    result = validate_style_options(choices, tmp_path)
    assert len(result["options"]) == 4
    assert result["representative_pages"] == ["s01", "s02", "s03"]
    assert "required" in result["visual_review"]


@pytest.mark.parametrize("size", [(90, 160), (160, 160), (240, 90)])
def test_rejects_vertical_strip_and_wrong_canvas(choices, tmp_path, size):
    Image.new("RGB", size, "red").save(tmp_path / choices["options"][0]["file"])
    with pytest.raises(ValueError, match="landscape overview"):
        validate_style_options(choices, tmp_path)


@pytest.mark.parametrize("count", [3, 5, 7])
def test_drafts_cannot_be_extra_candidates(choices, tmp_path, count):
    choices["options"] = [copy.deepcopy(choices["options"][i % 4]) for i in range(count)]
    with pytest.raises(ValueError, match="Exactly four"):
        validate_style_options(choices, tmp_path)


@pytest.mark.parametrize("mutation", ["number", "order", "missing_page", "path", "pixels", "missing_file", "traversal"])
def test_invalid_candidates_rejected(choices, tmp_path, mutation):
    first, second = choices["options"][:2]
    if mutation == "number":
        second["option"] = 1
    elif mutation == "order":
        second["slide_ids"].reverse()
    elif mutation == "missing_page":
        second["slide_ids"].pop()
    elif mutation == "path":
        second["file"] = first["file"]
    elif mutation == "pixels":
        (tmp_path / second["file"]).write_bytes((tmp_path / first["file"]).read_bytes())
    elif mutation == "missing_file":
        second["file"] = "missing.png"
    elif mutation == "traversal":
        second["file"] = "../outside.png"
    with pytest.raises(ValueError):
        validate_style_options(choices, tmp_path)


@pytest.mark.parametrize("total,representatives,valid", [(1, 1, True), (3, 2, False), (8, 8, True), (12, 6, True), (12, 3, False)])
def test_representative_page_coverage(choices, tmp_path, total, representatives, valid):
    choices["total_pages"] = total
    pages = [f"s{i}" for i in range(representatives)]
    choices["representative_pages"] = pages
    for option in choices["options"]:
        option["slide_ids"] = pages[:]
    if valid:
        assert len(validate_style_options(choices, tmp_path)["options"]) == 4
    else:
        with pytest.raises(ValueError, match="representative pages"):
            validate_style_options(choices, tmp_path)


def test_cli_from_other_directory_and_pixel_rounding(choices, tmp_path):
    Image.new("RGB", (1672, 941), "red").save(tmp_path / choices["options"][0]["file"])
    path = tmp_path / "choices.json"
    path.write_text(json.dumps(choices), encoding="utf-8")
    script = Path(__file__).resolve().parents[1] / "scripts/validate_style_options.py"
    result = subprocess.run([sys.executable, str(script), str(path)], cwd=tmp_path.parent, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert len(json.loads(result.stdout)["options"]) == 4
