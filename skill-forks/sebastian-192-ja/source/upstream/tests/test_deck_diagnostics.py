import io
import json
from pathlib import Path

import deck_diagnostics
import init_deck
import pytest
import run_deck
from test_run_deck import review_fixture, save

pytest_plugins = ["test_run_deck"]


@pytest.fixture(autouse=True)
def known_environment(monkeypatch):
    monkeypatch.setattr(deck_diagnostics, "renderer_environment", lambda backend="auto": {
        "requested": backend, "available": {"powerpoint": True, "libreoffice": False}, "ready": True})


def source_bytes(job):
    return {str(p): p.read_bytes() for p in job.parent.rglob("*") if p.is_file()}


def test_initializer_generates_portable_job_without_approving_or_overwriting_inputs(pipeline_case):
    job, _, spec, _, _ = pipeline_case
    spec["slides"][0]["image_status"] = "pending"
    save(job.parent / "page-spec.json", spec)
    before = source_bytes(job)
    result = init_deck.initialize(job.parent, "editable", "powerpoint", 320, "generated-job.json")
    assert result["status"] == "blocked"
    assert result["created_job"] == str(job.parent / "generated-job.json")
    assert any(a["kind"] == "image_approval" and a["page_number"] == 1 for a in result["actions"])
    for path, value in before.items():
        assert Path(path).read_bytes() == value
    config = run_deck.read(job.parent / "generated-job.json")
    assert config["scene"] == "scene.json" and config["page_spec"] == "page-spec.json"
    with pytest.raises(FileExistsError):
        init_deck.initialize(job.parent, "editable", output="generated-job.json")
    with pytest.raises(FileExistsError):
        init_deck.initialize(job.parent, output="page-spec.json")


def test_preflight_collects_all_missing_pages_and_is_read_only(pipeline_case):
    job, work, spec, _, _ = pipeline_case
    for slide in spec["slides"]:
        (job.parent / slide["image_file"]).unlink()
    before = source_bytes(job)
    result = deck_diagnostics.preflight(job, work)
    missing = [a for a in result["actions"] if a["kind"] == "missing_image"]
    assert [a["page_number"] for a in missing] == [1, 2]
    assert all(Path(a["file"]).is_absolute() and a["slide_id"] for a in missing)
    assert source_bytes(job) == before and not work.exists()


def test_missing_environment_is_explicit_without_changing_inputs(pipeline_case, monkeypatch):
    job, work, _, _, _ = pipeline_case
    before = source_bytes(job)
    monkeypatch.setattr(deck_diagnostics, "renderer_environment", lambda _backend: {"ready": False})
    result = deck_diagnostics.preflight(job, work)
    assert result["status"] == "blocked"
    assert result["actions"][0]["kind"] == "renderer_environment"
    assert source_bytes(job) == before and not work.exists()
    assert deck_diagnostics.preflight(job, work, check_renderer=False)["status"] == "ready"


def test_preflight_reports_stale_notes_and_preserves_foreign_workspace(pipeline_case):
    job, work, _, scene, _ = pipeline_case
    scene["slides"][0]["speaker_notes"] = "changed"
    save(job.parent / "scene.json", scene)
    work.mkdir()
    precious = work / "precious.txt"
    precious.write_text("preserve", encoding="utf-8")
    result = deck_diagnostics.preflight(job, work)
    assert result["status"] == "blocked"
    assert any("讲稿" in a["message"] for a in result["actions"])
    assert any(a["kind"] == "workspace" for a in result["actions"])
    assert precious.read_text(encoding="utf-8") == "preserve" and not (work / "owner.json").exists()


def test_chinese_tasks_locate_pages_and_current_files_and_do_not_auto_pass(pipeline_case):
    job, work, _, _, _ = pipeline_case
    first = run_deck.run(job, work)
    assert first["status_label"] == "等待审阅"
    assert all(v >= 0 for v in first["timings_seconds"].values())
    assert set(first["timings_seconds"]) == {"validate", "build", "render", "evaluate"}
    visual = next(a for a in first["actions"] if a["kind"] == "visual_review")
    assert visual["slide_id"] == "s01" and visual["page_number"] == 1
    assert Path(visual["file"]).is_file() and Path(visual["rendered"]).is_file()
    assert "第 1 页" in (work / "summary.md").read_text(encoding="utf-8")
    assert "_timing_started" not in json.dumps(first)
    review_fixture(pipeline_case)
    assert run_deck.run(job, work)["status"] == "complete"
    assert not run_deck.read(work / "summary.json")["actions"]


def test_stopped_summary_does_not_claim_checks_all_passed(pipeline_case):
    job, work, _, _, _ = pipeline_case
    result = run_deck.run(job, work, stop_after="build")
    assert result["status"] == "stopped"
    text = (work / "summary.md").read_text(encoding="utf-8")
    assert "尚未完成全部交付检查" in text and "本次声明的检查全部通过" not in text


@pytest.mark.parametrize("output", ["../escape.json", "/outside.json"])
def test_initializer_rejects_unsafe_job_paths(pipeline_case, output):
    job, _, _, _, _ = pipeline_case
    with pytest.raises(ValueError):
        init_deck.initialize(job.parent, output=output)


def test_legacy_console_output_remains_valid_json_with_unencodable_characters(monkeypatch):
    class LegacyConsole(io.StringIO):
        @property
        def encoding(self):
            return "ascii"

    stream = LegacyConsole()
    monkeypatch.setattr(deck_diagnostics.sys, "stdout", stream)
    result = {"status_label": "等待审阅", "detail": "emoji \U0001f603"}
    deck_diagnostics.print_result(result)
    assert json.loads(stream.getvalue()) == result


def test_utf8_bom_job_is_accepted_by_preflight_and_runner(pipeline_case):
    job, work, _, _, _ = pipeline_case
    job.write_text(job.read_text(encoding="utf-8"), encoding="utf-8-sig")
    assert deck_diagnostics.preflight(job, work)["status"] == "ready"
    assert run_deck.run(job, work, stop_after="build")["status"] == "stopped"
