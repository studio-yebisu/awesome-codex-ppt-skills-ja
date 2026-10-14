#!/usr/bin/env python3
"""Create an offline review panel and import explicitly recorded, current evidence."""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import io
import json
import tempfile
from pathlib import Path

from audit_page_content import audit as audit_content
from audit_page_content import template as content_template
from deck_diagnostics import error_action, print_result
from evaluate_delivery import review_template, verified_render, verified_visual_review
from PIL import Image
from render_deck import sha256

TARGETS = ("visual-review.json", "content-observations.json")


def context(config_path, work):
    from run_deck import (
        build_key,
        cached_state,
        keys,
        load_inputs,
        read,
        valid_artifact,
    )
    if read(work / "owner.json") != {"version": "1.0", "config": str(config_path)}:
        raise ValueError("Workspace belongs to a different job")
    inputs = load_inputs(config_path, work)
    if inputs["optional"].get("visual_review") or inputs["observations"]:
        raise ValueError("外部审阅/观测文件保持只读，请按配置提供证据；面板只编辑工作目录内的默认记录。")
    state = cached_state(work)
    if not valid_artifact(state.get("build"), build_key(inputs), work):
        raise ValueError("Current build is stale; rerun run_deck.py before reviewing")
    wanted = keys(inputs, state.get("backend"))
    if (state.get("spec") != inputs["spec"] or state.get("review_keys") != wanted
            or any(not valid_artifact(state.get("pages", {}).get(sid), key, work) for sid, key in wanted.items())):
        raise ValueError("Rendered pages are stale; rerun run_deck.py before reviewing")
    render, deck = verified_render(work / "render-report.json", inputs["spec_path"], len(wanted))
    if (render != state.get("render") or str(deck) != state["build"]["path"]
            or any(page["rendered"] != state["pages"][sid]["path"] for sid, page in zip(wanted, render["slides"]))):
        raise ValueError("Render report differs from the owned pipeline state")
    paths = {"job": config_path, "page_spec": inputs["spec_path"], "state": work / "state.json",
             "render_report": work / "render-report.json", **{name: work / name for name in TARGETS}}
    if inputs["scene_path"]:
        paths["scene"] = inputs["scene_path"]
    paths.update(inputs["optional"])
    snapshot = {"config": str(config_path), "workspace": str(work),
                "files": {name: sha256(path) if path.is_file() else None for name, path in paths.items()},
                "assets": inputs["assets"], "runtime": inputs["runtime"]}
    return inputs, render, snapshot


def base_records(inputs, render, work):
    from run_deck import read
    old = verified_visual_review(work / TARGETS[0], inputs["spec"], render)
    review = review_template(inputs["spec"], render)
    for before, after in zip(old["slides"], review["slides"]):
        for name in ("status", "notes", "data_visual_inventory"):
            after[name] = copy.deepcopy(before[name])
        prior = {item["element_id"]: item for item in before["data_reviews"]}
        for item in after["data_reviews"]:
            previous = prior[item["element_id"]]
            item.update(status=previous.get("declared_status", previous["status"]), notes=previous["notes"])
            item["checks"].update(previous.get("checks", {}))
    observations = read(work / TARGETS[1])
    audit_content(inputs["spec_path"], inputs["spec"]["slides"], observations)
    base = content_template(inputs["spec_path"], inputs["spec"]["slides"])
    by_id = {item["id"]: item for item in observations["slides"]}
    for item in base["slides"]:
        if item["id"] in by_id:
            item.update(status=by_id[item["id"]]["status"], observed_text=by_id[item["id"]]["observed_text"])
    return {"version": "1.0", "visual_review": review, "content_observations": base}


def image_uri(path, expected_hash):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        raise ValueError("Image changed while creating review panel; rerun run_deck.py")
    with Image.open(io.BytesIO(raw)) as image:
        mime = {"PNG": "image/png", "JPEG": "image/jpeg"}.get(image.format)
    if not mime:
        raise ValueError("Review panel requires PNG or JPEG images")
    return "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")


def generate_panel(config_path, work, actions=None):
    """Caller holds the workspace lock; every panel is a frozen, offline snapshot."""
    from run_deck import read
    config_path, work = config_path.resolve(), work.resolve()
    inputs, render, snapshot = context(config_path, work)
    if actions is None and (work / "summary.json").is_file():
        actions = read(work / "summary.json").get("actions", [])
    data = {**base_records(inputs, render, work), "snapshot": snapshot, "pages": [], "actions": actions or []}
    for slide, page in zip(inputs["spec"]["slides"], render["slides"]):
        data["pages"].append({"id": slide["id"], "title": slide["title"], "elements": slide["elements"],
                              "required_visible_values": slide.get("required_visible_values", []),
                              "source": image_uri(Path(page["reference"]), page["reference_sha256"]),
                              "rendered": image_uri(Path(page["rendered"]), page["rendered_sha256"])})
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = Path(__file__).with_name("review_panel.html").read_text(encoding="utf-8")
    target = work / "review-panel.html"
    if target.is_symlink() or not target.resolve().is_relative_to(work):
        raise ValueError("Unsafe review panel output path")
    content = template.replace("__PANEL_DATA__", payload)
    if not target.exists() or target.read_text(encoding="utf-8") != content:
        target.write_text(content, encoding="utf-8")
    return target


def frozen(value):
    """Only explicitly editable review fields may change; binding fields stay exact."""
    result = copy.deepcopy(value)
    for slide in result["visual_review"]["slides"]:
        slide["status"] = slide["notes"] = None
        inventory = slide["data_visual_inventory"]
        for name in ("status", "notes", "observed_element_ids"):
            inventory[name] = None
        for item in slide["data_reviews"]:
            item["status"] = item["notes"] = None
            item["checks"] = {name: None for name in item["checks"]}
    for item in result["content_observations"]["slides"]:
        item["status"] = item["observed_text"] = None
    return result


def validate_record(record, inputs, render, snapshot, work):
    from run_deck import write
    base = {**base_records(inputs, render, work), "snapshot": snapshot}
    if frozen(record) != frozen(base):
        raise ValueError("审阅记录已过期或绑定字段被修改，请重新运行任务并打开新面板。")
    for slide in record["visual_review"]["slides"]:
        if slide["status"] != "pending" and not slide["notes"].strip():
            raise ValueError("视觉通过/失败需要填写实际核对说明。")
    with tempfile.TemporaryDirectory(prefix=".review-check-", dir=work) as temp:
        path = Path(temp) / "review.json"
        write(path, record["visual_review"])
        verified_visual_review(path, inputs["spec"], render)
    audit_content(inputs["spec_path"], inputs["spec"]["slides"], record["content_observations"])


def recover_import(config_path, work):
    """Complete an interrupted two-file commit before another pipeline run can score it."""
    from run_deck import archive_review, digest, read, summary, write
    journal_path = work / ".review-import.json"
    journal = read(journal_path)
    if journal.pop("sha256", None) != digest(journal) or set(journal) != {"snapshot", "records", "after_hashes"}:
        raise ValueError("Review import journal is damaged; preserve workspace for recovery")
    _, _, current = context(config_path, work)
    original = journal["snapshot"]
    if set(journal["records"]) != set(TARGETS) or set(journal["after_hashes"]) != set(TARGETS):
        raise ValueError("Invalid review import targets")
    for name in TARGETS:
        if current["files"][name] not in (original["files"][name], journal["after_hashes"][name]):
            raise ValueError("Review evidence changed during interrupted import; preserve files")
        current["files"][name] = original["files"][name]
    if current != original:
        raise ValueError("Inputs changed during interrupted review import; preserve files")
    archive_review(work, work / "scorecard.json")
    (work / "scorecard.json").unlink(missing_ok=True)
    summary(work, {"status": "awaiting_review", "stages": {}, "actions": [
        {"kind": "review_import", "message": "正在提交审阅记录；需完成记录恢复后重新评分。"}],
        "rendered_slides": [], "reused_slides": [], "timings_seconds": {}})
    for name in TARGETS:
        path = work / name
        if sha256(path) != journal["after_hashes"][name]:
            archive_review(work, path)
            write(path, journal["records"][name])
    journal_path.unlink()
    summary(work, {"status": "awaiting_review", "stages": {}, "actions": [
        {"kind": "evaluate", "message": "记录已导入；重复原运行命令，重新计算当前交付评分。"}],
        "rendered_slides": [], "reused_slides": [], "timings_seconds": {},
        "review_sheet": str(work / "review.png")})


def import_record(config_path, work, record_path):
    from run_deck import digest, read, write
    inputs, render, snapshot = context(config_path, work)
    record = read(record_path)
    validate_record(record, inputs, render, snapshot, work)
    records = dict(zip(TARGETS, (record["visual_review"], record["content_observations"])))
    # Same serialization as atomic pipeline writes, allowing recovery after either replace.
    hashes = {name: hashlib.sha256((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")).hexdigest()
              for name, value in records.items()}
    journal = {"snapshot": snapshot, "records": records, "after_hashes": hashes}
    write(work / ".review-import.json", {**journal, "sha256": digest(journal)})
    recover_import(config_path, work)
    return {"status": "awaiting_review", "status_label": "记录已导入，等待重新评分", "workspace": str(work)}


def main():
    from run_deck import locked_workspace
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--import-record", type=Path)
    args = parser.parse_args()
    config_path, work = args.job.resolve(), args.workspace.resolve()
    try:
        if not (work / "owner.json").is_file():
            raise ValueError("先运行 run_deck.py，生成当前渲染和审阅模板。")
        with locked_workspace(config_path, work):
            if args.import_record:
                result = import_record(config_path, work, args.import_record.resolve())
            else:
                result = {"status": "ready", "status_label": "审阅面板已生成", "review_panel": str(generate_panel(config_path, work))}
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        result = {"status": "blocked", "actions": [error_action(error, config_path)]}
    print_result(result)
    if result["status"] == "blocked":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
