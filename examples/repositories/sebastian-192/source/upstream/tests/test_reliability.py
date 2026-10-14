import copy
import json
import sys
import time

import pytest
import render_environment
import run_deck
from json_io import read_json
from measured_layout import findings
from record_work import aggregate, append, summarize
from render_process import execute, rendering_options, validate_options
from update_data_bindings import page_dependencies

pytest_plugins = ['test_run_deck']


def test_bom_spec_survives_build_render_and_evaluation(pipeline_case):
    job, work, spec, scene, _ = pipeline_case
    for name, value in (("page-spec.json", spec), ("scene.json", scene)):
        (job.parent / name).write_text(json.dumps(value), encoding="utf-8-sig")
    assert run_deck.run(job, work)["status"] == "awaiting_review"
    from test_run_deck import review_fixture
    review_fixture(pipeline_case)
    for name in ("visual-review.json", "content-observations.json"):
        value = read_json(work / name)
        (work / name).write_text(json.dumps(value), encoding="utf-8-sig")
    assert run_deck.run(job, work)["status"] == "complete"


@pytest.mark.parametrize("options", [{"timeout": float('nan')}, {"timeout": 0}, {"retries": True}, {"retries": 3}, {"measure_text": "yes"}])
def test_bad_renderer_options_rejected(options):
    with pytest.raises((ValueError, TypeError)):
        validate_options(**options)


def test_real_hung_helper_is_bounded_and_safe_retry_is_limited(tmp_path):
    marker = tmp_path / "attempts"
    command = [sys.executable, "-c", "import sys,time;from pathlib import Path;p=Path(sys.argv[1]);p.write_text(p.read_text()+'x' if p.exists() else 'x');time.sleep(20)", str(marker)]
    began = time.monotonic()
    with rendering_options(timeout=1, retries=1), pytest.raises(RuntimeError, match="Attempts: 2"):
        execute(command, label="test")
    assert time.monotonic() - began < 12
    assert marker.read_text() == "xx"
    with rendering_options(timeout=1, retries=2), pytest.raises(RuntimeError, match="Attempts: 1"):
        execute(command, label="PowerPoint test", retry_safe=False)
    assert marker.read_text() == "xxx"


def test_command_error_contains_stderr_and_is_not_silently_successful():
    with rendering_options(retries=0), pytest.raises(RuntimeError, match="specific failure"):
        execute([sys.executable, "-c", "import sys;sys.stderr.write('specific failure');sys.exit(4)"], label="test")


def test_font_file_replacement_invalidates_environment_without_manual_refresh(tmp_path, monkeypatch):
    font = tmp_path / "font.ttf"
    font.write_bytes(b"font-a")
    monkeypatch.setattr(render_environment, "font_directories", lambda: [tmp_path])
    before = render_environment.fingerprint()
    font.write_bytes(b"font-b")  # Same length; content replacement still invalidates.
    after = render_environment.fingerprint()
    assert render_environment.environment_key(before, "powerpoint") != render_environment.environment_key(after, "powerpoint")


def test_environment_change_rebuilds_render_and_discards_old_page_review(pipeline_case, monkeypatch):
    job, work, _, _, calls = pipeline_case
    before = {"binaries": {}, "fonts": {"fixture": "v1"}}
    monkeypatch.setattr(run_deck, "fingerprint", lambda: copy.deepcopy(before))
    run_deck.run(job, work)
    from test_run_deck import review_fixture
    review_fixture(pipeline_case)
    assert run_deck.run(job, work)["status"] == "complete"
    before["fonts"]["fixture"] = "v2"
    result = run_deck.run(job, work)
    assert result["rendered_slides"] == ["s01", "s02"]
    assert result["status"] == "awaiting_review"
    assert calls == [[1, 2], [1, 2]]


def test_renderer_component_upgrade_invalidates_cache_even_when_launcher_is_unchanged(tmp_path, monkeypatch):
    launcher = tmp_path / "soffice"
    component = tmp_path / "soffice.bin"
    launcher.write_bytes(b"unchanged launcher")
    component.write_bytes(b"engine v1")
    monkeypatch.setattr(render_environment, "font_directories", list)
    monkeypatch.setattr(render_environment.shutil, "which", lambda name: str(launcher) if name == "soffice" else None)
    before = render_environment.fingerprint()
    component.write_bytes(b"engine v2")
    after = render_environment.fingerprint()
    assert render_environment.environment_key(before, "libreoffice") != render_environment.environment_key(after, "libreoffice")


def binding_contract(case):
    job, _, spec, scene, _ = case
    for index, text in enumerate(("10", "20")):
        spec["slides"][index]["elements"][0]["text"] = text
        scene["slides"][index]["elements"][0]["text"] = text
    run_deck.write(job.parent / "page-spec.json", spec)
    run_deck.write(job.parent / "scene.json", scene)
    contract = {"version": "1.0", "documents": {"page_spec": "page-spec.json", "scene": "scene.json"},
                "inputs": {"a": {"value": 5, "unit": "count", "source_ref": "fixture"}, "b": {"value": 20, "unit": "count", "source_ref": "fixture"}},
                "formulas": {"double_a": "a * 2"}, "bindings": [
                    {"document": kind, "pointer": f"/slides/{index}/elements/0/text", "template": "{double_a:.0f}" if index == 0 else "{b:.0f}"}
                    for kind in ("page_spec", "scene") for index in (0, 1)]}
    path = job.parent / "bindings.json"
    run_deck.write(path, contract)
    config = read_json(job)
    config["data_bindings"] = path.name
    run_deck.write(job, config)
    return path, contract


def test_local_numeric_update_preserves_unrelated_render_and_review(pipeline_case):
    job, work, spec, scene, calls = pipeline_case
    path, contract = binding_contract(pipeline_case)
    run_deck.run(job, work)
    from test_run_deck import review_fixture
    review_fixture(pipeline_case)
    assert run_deck.run(job, work)["status"] == "complete"
    contract["inputs"]["a"]["value"] = 6
    spec["slides"][0]["elements"][0]["text"] = "12"
    scene["slides"][0]["elements"][0]["text"] = "12"
    run_deck.write(path, contract)
    run_deck.write(job.parent / "page-spec.json", spec)
    run_deck.write(job.parent / "scene.json", scene)
    result = run_deck.run(job, work)
    assert result["rendered_slides"] == ["s01"] and result["reused_slides"] == ["s02"]
    assert calls == [[1, 2], [1]]
    assert [s["status"] for s in read_json(work / "visual-review.json")["slides"]] == ["pending", "pass"]


def test_transitive_provenance_change_affects_only_declared_page(pipeline_case):
    job, work, _, _, _ = pipeline_case
    path, contract = binding_contract(pipeline_case)
    before = run_deck.keys(run_deck.load_inputs(job, work), "powerpoint")
    contract["inputs"]["a"]["source_ref"] = "corrected scope"
    run_deck.write(path, contract)
    after = run_deck.keys(run_deck.load_inputs(job, work), "powerpoint")
    assert before["s01"] != after["s01"] and before["s02"] == after["s02"]
    dependencies = page_dependencies(path)
    assert set(dependencies["s01"]["inputs"]) == {"a"}
    assert set(dependencies["s01"]["formulas"]) == {"double_a"}


def measure(items):
    return {"items": items, "page_number": 1, "slide_width_pt": 720, "slide_height_pt": 405}


def measured_item(name, bounds, height=20):
    return {"status": "measured", "element_id": name, "bounds": bounds,
            "content_width_pt": bounds[2], "content_height_pt": height,
            "available_width_pt": 200, "available_height_pt": 25}


def test_actual_bounds_detect_small_overflow_and_text_overlap_without_autopass():
    items = [measured_item("a", [20, 30, 100, 30], 30), measured_item("b", [30, 30, 100, 20])]
    result = findings(measure(items), "s01")
    assert any(f.get("kind") == "text_overlap" for f in result)
    assert next(f for f in result if f["element_id"] == "a")["status"] == "risk"
    assert next(f for f in result if f["element_id"] == "b")["status"] == "no_obvious_risk"


def test_table_expansion_and_unsupported_groups_remain_explicit():
    result = findings(measure([{"element_id": "table", "status": "table_bounds", "bounds": [10, 20, 300, 420]},
                               {"element_id": "grouped", "status": "unverified", "reason": "group transform"}]), "s01")
    assert [f["status"] for f in result] == ["risk", "unverified"]


def test_cost_history_preserves_failed_first_attempt_and_missing_times(tmp_path):
    path = tmp_path / "work.jsonl"
    append(path, "t1", "start", note="actual start", at="2026-10-03T00:00:00Z")
    append(path, "t1", "generation", page_id="s01", note="actual image call", at="2026-10-03T00:01:00Z")
    append(path, "t1", "delivery", status="fail", note="overflow found", at="2026-10-03T00:02:00Z")
    append(path, "t1", "revision", page_id="s01", note="layout repaired", at="2026-10-03T00:03:00Z")
    append(path, "t1", "review", note="actual review, time unavailable", at="2026-10-03T00:04:00Z")
    append(path, "t1", "delivery", status="pass", note="repaired delivery", at="2026-10-03T00:05:00Z")
    append(path, "t1", "end", note="actual end", at="2026-10-03T00:06:00Z")
    result = summarize(path)
    assert result["first_delivery_status"] == "fail" and result["final_delivery_status"] == "pass"
    assert result["generation_calls"] == result["revised_page_count"] == 1
    assert result["wall_seconds"] == 360
    assert result["review_events_without_duration"] == 1
    incomplete = tmp_path / "pending.jsonl"
    append(incomplete, "t2", "start", note="not delivered")
    total = aggregate([path, incomplete])
    assert total["registered_tasks"] == 2 and total["pending_first_delivery"] == 1 and total["first_pass_rate"] == 0
    with pytest.raises(ValueError, match="distinct"):
        aggregate([path, path])
    data = path.read_text(encoding="utf-8").replace("overflow found", "pass")
    path.write_text(data, encoding="utf-8")
    with pytest.raises(ValueError, match="changed"):
        summarize(path)


def test_missing_cost_log_and_negative_duration_cannot_become_zero(tmp_path):
    path = tmp_path / "missing.jsonl"
    with pytest.raises(ValueError, match="not exist"):
        summarize(path)
    with pytest.raises(ValueError, match="nonnegative"):
        append(path, "t", "review", seconds=-1, note="invalid")


def test_pipeline_reports_explicit_cost_log_without_affecting_visual_approval(pipeline_case):
    job, work, _, _, _ = pipeline_case
    log = job.parent / "production.jsonl"
    append(log, "fixture", "start", note="actual start")
    append(log, "fixture", "review", note="duration unknown")
    config = read_json(job)
    config["work_log"] = log.name
    run_deck.write(job, config)
    result = run_deck.run(job, work)
    assert result["status"] == "awaiting_review"
    assert result["production_metrics"]["review_seconds"] is None
    assert result["production_metrics"]["wall_seconds"] is None
    assert "制作成本" in (work / "summary.md").read_text(encoding="utf-8")


def test_real_measurement_tasks_and_corrupt_measurement_cache(pipeline_case, monkeypatch):
    job, work, _, _, calls = pipeline_case
    renderer = run_deck.render_selected

    def measured_renderer(deck, output, width, backend, slides):
        actual = renderer(deck, output, width, backend, slides)
        for index in slides:
            run_deck.write(output / f"{index:03d}.layout.json", measure([measured_item("text", [20, 30, 100, 30], 30)]))
        return actual

    monkeypatch.setattr(run_deck, "render_selected", measured_renderer)
    config = read_json(job)
    config["measure_text"] = True
    run_deck.write(job, config)
    first = run_deck.run(job, work)
    assert any(a["kind"] == "measured_layout" and a["rendered"] for a in first["actions"])
    assert all(f["status"] == "risk" for f in first["measured_layout"])
    from test_run_deck import review_fixture
    review_fixture(pipeline_case)
    resumed = run_deck.run(job, work)
    assert resumed["status"] == "complete" and resumed["measured_layout"]
    assert not any(a["kind"] == "measured_layout" for a in resumed["actions"])
    state = run_deck.cached_state(work)
    from pathlib import Path
    Path(state["pages"]["s01"]["layout"]["path"]).write_bytes(b"corrupt")
    assert run_deck.run(job, work)["rendered_slides"] == ["s01"]
    assert calls == [[1, 2], [1]]
