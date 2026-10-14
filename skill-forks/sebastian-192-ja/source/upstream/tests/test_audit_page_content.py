import json
import subprocess
import sys
from pathlib import Path

import audit_page_content
import pytest
from PIL import Image


def make_spec(tmp_path):
    source = json.loads((Path(__file__).resolve().parents[1] / "examples/page-spec.example.json").read_text(encoding="utf-8"))
    slide = source["slides"][0]
    slide["required_visible_values"] = ["增长 32%"]
    slide["image_status"] = "generated"
    image = tmp_path / slide["image_file"]
    image.parent.mkdir()
    Image.new("RGB", (160, 90), "white").save(image)
    path = tmp_path / "page-spec.json"
    path.write_text(json.dumps(source, ensure_ascii=False), encoding="utf-8")
    return path, source


def test_detects_missing_numeric_and_stale_transcription(tmp_path):
    path, spec = make_spec(tmp_path)
    slide = spec["slides"][0]
    observation = audit_page_content.template(path, [slide])
    observation["slides"][0].update(status="complete", observed_text="让数字服务真正走进田间\n以可信、易用的数字服务连接农户与产业资源\n增长 23%")
    report = audit_page_content.audit(path, [slide], observation)
    assert report["issues"] == 1
    assert report["slides"][0]["findings"][0]["missing_numbers"] == ["32%"]
    observation["slides"][0]["observed_text"] = observation["slides"][0]["observed_text"].replace("23%", "32%")
    assert audit_page_content.audit(path, [slide], observation)["pass"]
    Image.new("RGB", (160, 90), "black").save(tmp_path / slide["image_file"])
    with pytest.raises(ValueError, match="hash changed"):
        audit_page_content.audit(path, [slide], observation)


def test_partial_observation_cannot_pass_strict_gate(tmp_path):
    path, spec = make_spec(tmp_path)
    observation = audit_page_content.template(path, spec["slides"])
    report = audit_page_content.audit(path, spec["slides"], observation)
    assert not report["pass"]
    assert report["incomplete"] == 1
    assert all(finding["status"] == "needs_review" for finding in report["slides"][0]["findings"])


def test_chinese_adjacent_numbers_and_units():
    assert audit_page_content.numbers("增长32%，达到1,200万；单价12.5元") == ["32%", "1,200", "12.5"]
    assert audit_page_content.compact_number("1,200") == audit_page_content.compact_number("1200")


def test_cli_creates_transcription_template(tmp_path):
    path, _ = make_spec(tmp_path)
    target = tmp_path / "observations.json"
    script = Path(__file__).resolve().parents[1] / "scripts/audit_page_content.py"
    result = subprocess.run([sys.executable, str(script), str(path), str(target), "--init", "--slide", "s01"],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    observation = json.loads(target.read_text(encoding="utf-8"))
    assert len(observation["slides"][0]["image_sha256"]) == 64
