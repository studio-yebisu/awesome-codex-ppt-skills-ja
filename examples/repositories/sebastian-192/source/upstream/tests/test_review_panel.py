import json
import re
from pathlib import Path

import pytest
import review_panel
import run_deck
from PIL import Image

pytest_plugins = ["test_run_deck"]


def payload(work):
    html = (work / "review-panel.html").read_text(encoding="utf-8")
    return json.loads(re.search(r'<script id="panel-data" type="application/json">(.*?)</script>', html, re.DOTALL)[1])


def record(work):
    data = payload(work)
    return {key: data[key] for key in ("version", "snapshot", "visual_review", "content_observations")}


def completed(work, spec):
    result = record(work)
    for item, page in zip(result["visual_review"]["slides"], spec["slides"]):
        item.update(status="pass", notes="Explicit fixture inspection")
        item["data_visual_inventory"].update(status="pass", notes="Checked fixture data visual list",
                                             observed_element_ids=[e["id"] for e in page["elements"] if e["kind"] in ("chart", "table")])
        for data in item["data_reviews"]:
            data.update(status="pass", notes="Explicit fixture data checks")
            data["checks"] = dict.fromkeys(data["checks"], "pass")
    for item, page in zip(result["content_observations"]["slides"], spec["slides"]):
        item.update(status="complete", observed_text="\n".join(e["text"] for e in page["elements"] if e["kind"] == "text"))
    return result


def import_value(job, work, value):
    path = job.parent / "download.json"
    run_deck.write(path, value)
    with run_deck.locked_workspace(job, work):
        return review_panel.import_record(job, work, path)


def test_generated_panel_is_offline_pending_and_source_cannot_inject_script(pipeline_case):
    job, work, spec, scene, _ = pipeline_case
    value = '</script><img src="https://example.invalid/leak" onerror="alert(1)">'
    spec["slides"][0]["title"] = value
    scene["slides"][0]["elements"][0]["text"] = "Alpha"
    run_deck.write(job.parent / "page-spec.json", spec)
    result = run_deck.run(job, work)
    assert result["status"] == "awaiting_review" and Path(result["review_panel"]).is_file()
    data = payload(work)
    assert data["pages"][0]["title"] == value
    html = (work / "review-panel.html").read_text(encoding="utf-8")
    assert value not in html and "connect-src 'none'" in html
    assert data["pages"][0]["source"].startswith("data:image/png;base64,")
    assert all(s["status"] == "pending" for s in data["visual_review"]["slides"])
    assert all(s["observed_text"] == "" for s in data["content_observations"]["slides"])
    assert "本地逐页审阅面板" in (work / "summary.md").read_text(encoding="utf-8")


def test_import_requires_new_scoring_and_archives_old_records(pipeline_case):
    job, work, spec, _, calls = pipeline_case
    run_deck.run(job, work)
    imported = import_value(job, work, completed(work, spec))
    assert imported["status"] == "awaiting_review"
    assert not (work / "scorecard.json").exists()
    assert run_deck.read(work / "summary.json")["status"] == "awaiting_review"
    assert list((work / "review-history").glob("visual-review-*.json"))
    result = run_deck.run(job, work)
    assert result["status"] == "complete" and result["rendered_slides"] == [] and calls == [[1, 2]]
    assert run_deck.read(work / "scorecard.json")["status"] == "pass"


def test_pending_export_does_not_pass_and_failed_review_stays_failed(pipeline_case):
    job, work, spec, _, _ = pipeline_case
    run_deck.run(job, work)
    import_value(job, work, record(work))
    assert run_deck.run(job, work)["status"] == "awaiting_review"
    value = completed(work, spec)
    value["visual_review"]["slides"][0].update(status="fail", notes="Observed overlap in fixture")
    import_value(job, work, value)
    assert run_deck.run(job, work)["status"] == "failed"


@pytest.mark.parametrize("change", ["scene", "spec", "source", "render", "review", "observations"])
def test_stale_panel_rejected_without_changing_evidence(pipeline_case, change):
    job, work, spec, scene, _ = pipeline_case
    run_deck.run(job, work)
    value = completed(work, spec)
    if change == "scene":
        scene["slides"][0]["elements"][0]["w"] += 1
        run_deck.write(job.parent / "scene.json", scene)
    elif change == "spec":
        spec["slides"][0]["speaker_notes"] = "Changed note"
        scene["slides"][0]["speaker_notes"] = "Changed note"
        run_deck.write(job.parent / "page-spec.json", spec)
        run_deck.write(job.parent / "scene.json", scene)
    elif change in ("source", "render"):
        path = job.parent / spec["slides"][0]["image_file"] if change == "source" else Path(run_deck.cached_state(work)["pages"]["s01"]["path"])
        Image.new("RGB", (160, 90), "red").save(path)
    else:
        path = work / ("visual-review.json" if change == "review" else "content-observations.json")
        old = run_deck.read(path)
        old["slides"][0]["notes" if change == "review" else "observed_text"] = "Concurrent edit"
        run_deck.write(path, old)
    before = {name: (work / name).read_bytes() for name in (*review_panel.TARGETS, "scorecard.json", "summary.json")}
    with pytest.raises((ValueError, TypeError)):
        import_value(job, work, value)
    assert before == {name: (work / name).read_bytes() for name in before}
    assert not (work / ".review-import.json").exists()


@pytest.mark.parametrize("change", ["binding", "extra", "order", "notes"])
def test_tampered_records_cannot_modify_binding_or_schema(pipeline_case, change):
    job, work, spec, _, _ = pipeline_case
    run_deck.run(job, work)
    value = completed(work, spec)
    if change == "binding":
        value["visual_review"]["slides"][0]["rendered_sha256"] = "0" * 64
    elif change == "extra":
        value["visual_review"]["slides"][0]["unauthorized"] = True
    elif change == "order":
        value["content_observations"]["slides"].reverse()
    else:
        value["visual_review"]["slides"][0]["notes"] = ""
    before = (work / "visual-review.json").read_bytes()
    with pytest.raises(ValueError):
        import_value(job, work, value)
    assert before == (work / "visual-review.json").read_bytes()


def test_data_subchecks_and_unexpected_inventory_cannot_be_bypassed(pipeline_case):
    job, work, spec, _, _ = pipeline_case
    element = {"id": "chart", "kind": "chart", "role": "evidence", "native_intent": "native",
               "source_ref": "fixture source", "confirmation_status": "confirmed",
               "data": {"categories": ["A"], "series": [{"name": "N", "values": [1]}]}}
    spec["slides"][0]["elements"].append(element)
    run_deck.write(job.parent / "page-spec.json", spec)
    assert run_deck.run(job, work)["status"] == "awaiting_review"
    value = completed(work, spec)
    value["visual_review"]["slides"][0]["data_reviews"][0]["checks"]["scale_geometry"] = "pending"
    import_value(job, work, value)
    assert run_deck.run(job, work)["status"] == "awaiting_review"
    value = completed(work, spec)
    value["visual_review"]["slides"][0]["data_visual_inventory"]["observed_element_ids"] += ["unexpected"]
    import_value(job, work, value)
    assert run_deck.run(job, work)["status"] == "failed"


def test_external_evidence_remains_read_only(pipeline_case):
    job, work, _, _, _ = pipeline_case
    run_deck.run(job, work)
    external = job.parent / "external.json"
    external.write_bytes((work / "visual-review.json").read_bytes())
    config = run_deck.read(job)
    config["visual_review"] = external.name
    run_deck.write(job, config)
    before = external.read_bytes()
    result = run_deck.run(job, work)
    assert "外部" in result["panel_note"] and not (work / "review-panel.html").exists()
    with pytest.raises(ValueError, match="外部"):
        review_panel.generate_panel(job, work)
    assert external.read_bytes() == before


def test_interrupted_pair_import_recovers_before_pipeline_scoring(pipeline_case, monkeypatch):
    job, work, spec, _, _ = pipeline_case
    run_deck.run(job, work)
    value = completed(work, spec)
    original = run_deck.write

    def interrupted(path, value):
        if path == work / "content-observations.json":
            raise OSError("Simulated interrupted second evidence write")
        return original(path, value)

    monkeypatch.setattr(run_deck, "write", interrupted)
    with pytest.raises(OSError):
        import_value(job, work, value)
    assert (work / ".review-import.json").exists()
    assert not (work / "scorecard.json").exists()
    assert run_deck.read(work / "summary.json")["status"] == "awaiting_review"
    monkeypatch.setattr(run_deck, "write", original)
    assert run_deck.run(job, work)["status"] == "complete"
    assert not (work / ".review-import.json").exists()


def test_damaged_import_journal_blocks_recovery_without_evidence_writes(pipeline_case):
    job, work, _, _, _ = pipeline_case
    run_deck.run(job, work)
    before = {name: (work / name).read_bytes() for name in review_panel.TARGETS}
    run_deck.write(work / ".review-import.json", {"snapshot": {}, "sha256": "broken"})
    with pytest.raises(ValueError, match="damaged"):
        run_deck.run(job, work)
    assert before == {name: (work / name).read_bytes() for name in before}
