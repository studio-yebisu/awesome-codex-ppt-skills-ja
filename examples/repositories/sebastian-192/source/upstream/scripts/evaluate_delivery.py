#!/usr/bin/env python3
"""Create a hash-bound delivery scorecard from rendered slides and review evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_chart_geometry import audit as audit_geometry
from audit_editability import audit as audit_editability
from audit_page_content import audit as audit_content
from audit_speaker_notes import audit as audit_notes
from json_io import read_json
from render_deck import reference_files, sha256
from update_data_bindings import inspect as inspect_bindings
from validate_page_spec import load_page_spec


def data_checks(element):
    return ["source_values", "labels_units", "scale_geometry" if element["kind"] == "chart" else "row_column_alignment"]


def verified_render(report_path: Path, spec_path: Path, count: int) -> tuple[dict, Path]:
    report = read_json(report_path)
    deck = Path(report["deck"]).resolve()
    if not deck.is_file() or report.get("deck_sha256") != sha256(deck):
        raise ValueError("Render report is stale or lacks a deck hash; rerun render_deck.py")
    if report.get("page_spec_sha256") != sha256(spec_path):
        raise ValueError("Render report lacks the current Page Spec hash; rerun render_deck.py --page-spec")
    pages = report.get("slides", [])
    if len(pages) != count:
        raise ValueError("Render report slide count differs from Page Spec")
    references = reference_files(spec_path, count)
    for number, (page, reference) in enumerate(zip(pages, references), 1):
        rendered = Path(page["rendered"]).resolve()
        if page.get("slide") != number or not rendered.is_file() or page.get("rendered_sha256") != sha256(rendered):
            raise ValueError(f"Rendered slide {number} changed or is missing")
        if (not isinstance(page.get("reference"), str)
                or Path(page["reference"]).resolve() != reference
                or page.get("reference_sha256") != sha256(reference)):
            raise ValueError(f"Reference slide {number} changed or lacks a hash; rerun render_deck.py --page-spec")
    return report, deck


def review_template(spec: dict, render: dict) -> dict:
    return {"version": "1.2", "deck_sha256": render["deck_sha256"],
            "page_spec_sha256": render["page_spec_sha256"], "render_backend": render["backend"], "slides": [
        {"id": slide["id"], "rendered_sha256": page["rendered_sha256"],
         "reference_sha256": page["reference_sha256"], "status": "pending", "notes": "",
         "data_visual_inventory": {"status": "pending", "notes": "", "observed_element_ids": []},
         "data_reviews": [{"element_id": element["id"], "status": "pending", "notes": "",
                           "checks": {key: "pending" for key in data_checks(element)}}
                          for element in slide["elements"] if element["kind"] in ("chart", "table")]}
        for slide, page in zip(spec["slides"], render["slides"])
    ]}


def verified_visual_review(review_path: Path, spec: dict, render: dict) -> dict:
    review = read_json(review_path)
    if (review.get("version") != "1.2" or review.get("deck_sha256") != render["deck_sha256"]
            or review.get("page_spec_sha256") != render["page_spec_sha256"]
            or review.get("render_backend") != render["backend"]):
        raise ValueError("Visual review is stale or has an invalid version; create a new --init-review template")
    items = review.get("slides", [])
    if len(items) != len(spec["slides"]):
        raise ValueError("Visual review slide count differs from Page Spec")
    for slide, page, item in zip(spec["slides"], render["slides"], items):
        if (item.get("id") != slide["id"] or item.get("rendered_sha256") != page["rendered_sha256"]
                or item.get("reference_sha256") != page["reference_sha256"]):
            raise ValueError(f"Visual review is stale or out of order at {slide['id']}")
        if item.get("status") not in ("pass", "fail", "pending") or not isinstance(item.get("notes"), str):
            raise ValueError(f"Invalid visual review status at {slide['id']}")
        expected_ids = {element["id"] for element in slide["elements"] if element["kind"] in ("chart", "table")}
        expected_elements = {element["id"]: element for element in slide["elements"] if element["id"] in expected_ids}
        inventory = item.get("data_visual_inventory", {"status": "pending", "notes": "", "observed_element_ids": []})
        if (not isinstance(inventory, dict) or inventory.get("status") not in ("pass", "fail", "pending")
                or not isinstance(inventory.get("notes"), str)
                or not isinstance(inventory.get("observed_element_ids"), list)
                or any(not isinstance(eid, str) for eid in inventory["observed_element_ids"])
                or len(set(inventory["observed_element_ids"])) != len(inventory["observed_element_ids"])
                or (inventory["status"] != "pending" and not inventory["notes"].strip())):
            raise ValueError(f"Invalid data visual inventory at {slide['id']}")
        if inventory["status"] == "pass" and set(inventory["observed_element_ids"]) != expected_ids:
            inventory["status"] = "fail"
            inventory["notes"] += " Observed data visuals differ from Page Spec."
        item["data_visual_inventory"] = inventory
        data_reviews = item.get("data_reviews", [])
        if not isinstance(data_reviews, list):
            raise TypeError(f"Invalid data reviews at {slide['id']}")
        seen = set()
        for data_review in data_reviews:
            if not isinstance(data_review, dict):
                raise TypeError(f"Invalid data review entry at {slide['id']}")
            element_id = data_review.get("element_id")
            if element_id not in expected_ids or element_id in seen:
                raise ValueError(f"Unknown or duplicate data review at {slide['id']}: {element_id}")
            seen.add(element_id)
            if (data_review.get("status") not in ("pass", "fail", "pending")
                    or not isinstance(data_review.get("notes"), str)
                    or (data_review["status"] in ("pass", "fail") and not data_review["notes"].strip())):
                raise ValueError(f"Data review requires a valid status and review notes at {slide['id']}: {element_id}")
            checks = data_review.get("checks", {})
            keys = data_checks(expected_elements[element_id])
            if (not isinstance(checks, dict) or set(checks) - set(keys)
                    or any(value not in ("pass", "fail", "pending") for value in checks.values())):
                raise ValueError(f"Invalid data review checks at {slide['id']}: {element_id}")
            data_review["checks"] = {key: checks.get(key, "pending") for key in keys}
            declared = data_review["status"]
            data_review["declared_status"] = declared
            if "fail" in data_review["checks"].values():
                data_review["status"] = "fail"
            elif declared == "pass" and "pending" in data_review["checks"].values():
                data_review["status"] = "pending"
            if data_review["status"] == "fail" and not data_review["notes"].strip():
                raise ValueError(f"Failed data review checks require notes at {slide['id']}: {element_id}")
        # Missing entries remain unreviewed, even if the overall page is marked pass.
        data_reviews.extend({"element_id": element_id, "status": "pending", "notes": ""}
                            for element_id in sorted(expected_ids - seen))
        item["data_reviews"] = data_reviews
    return review


def evaluate(spec_path: Path, render_path: Path, review_path: Path,
             observation_paths: list[Path], scene_path: Path | None = None,
             chart_observation_path: Path | None = None,
             data_bindings_path: Path | None = None) -> dict:
    spec, _ = load_page_spec(spec_path)
    render, deck = verified_render(render_path, spec_path, len(spec["slides"]))
    review = verified_visual_review(review_path, spec, render)
    observations = {"version": "1.0", "slides": []}
    for path in observation_paths:
        item = read_json(path)
        if item.get("version") != "1.0" or not isinstance(item.get("slides"), list):
            raise ValueError(f"Invalid observation file: {path}")
        observations["slides"].extend(item["slides"])
    content = audit_content(spec_path, spec["slides"], observations)
    visual_failed = [item["id"] for item in review["slides"] if item["status"] == "fail"]
    visual_pending = [item["id"] for item in review["slides"] if item["status"] == "pending"]
    data_reviews = [{**data_review, "slide_id": item["id"]}
                    for item in review["slides"] for data_review in item["data_reviews"]]
    data_failed = [item for item in data_reviews if item["status"] == "fail"]
    data_pending = [item for item in data_reviews if item["status"] == "pending"]
    inventory_failed = [item["id"] for item in review["slides"] if item["data_visual_inventory"]["status"] == "fail"]
    inventory_pending = [item["id"] for item in review["slides"] if item["data_visual_inventory"]["status"] == "pending"]
    geometry = audit_geometry(spec_path, chart_observation_path) if chart_observation_path else None
    editability = audit_editability(deck, scene_path) if scene_path else None
    speaker_notes = audit_notes(spec_path, deck, scene_path)
    dependencies = inspect_bindings(data_bindings_path, spec_path, scene_path) if data_bindings_path else None
    edit_errors = editability["errors"] if editability else []
    if content["issues"] or visual_failed or data_failed or edit_errors or inventory_failed or speaker_notes["errors"] or (geometry and geometry["status"] == "fail") or (dependencies and dependencies["status"] == "fail"):
        status = "fail"
    elif content["incomplete"] or visual_pending or data_pending or inventory_pending or (geometry and geometry["status"] == "incomplete"):
        status = "incomplete"
    else:
        status = "pass"
    return {
        "status": status,
        "deck": str(deck), "deck_sha256": render["deck_sha256"],
        "page_spec_sha256": sha256(spec_path),
        "evidence": {"render_report_sha256": sha256(render_path),
                     "visual_review_sha256": sha256(review_path),
                     "observation_sha256": {str(path): sha256(path) for path in observation_paths},
                     "reference_sha256": {slide["id"]: page["reference_sha256"]
                                          for slide, page in zip(spec["slides"], render["slides"])},
                     "scene_sha256": sha256(scene_path) if scene_path else None,
                     "chart_observations_sha256": sha256(chart_observation_path) if chart_observation_path else None,
                     "data_bindings_sha256": sha256(data_bindings_path) if data_bindings_path else None},
        "slides": len(spec["slides"]),
        "render_backend": render["backend"],
        "render_environment": render.get("environment"),
        "measured_layout": render.get("measured_layout", []),
        "content": {"issues": content["issues"], "incomplete": content["incomplete"],
                    "missing_observations": content["missing_observations"],
                    "findings": {item["id"]: item["findings"] for item in content["slides"] if item["findings"]}},
        "visual": {"passed": sum(item["status"] == "pass" for item in review["slides"]),
                   "failed": visual_failed, "pending": visual_pending,
                   "difference_means": [page.get("mean_absolute_difference") for page in render["slides"]]},
        "data": {"passed": sum(item["status"] == "pass" for item in data_reviews),
                 "failed": data_failed, "pending": data_pending, "reviews": data_reviews},
        "data_visual_inventory": {"failed": inventory_failed, "pending": inventory_pending,
                                  "reviews": [{"slide_id": item["id"], **item["data_visual_inventory"]} for item in review["slides"]]},
        "chart_geometry": geometry or {"checked": False},
        "speaker_notes": speaker_notes,
        "data_dependencies": dependencies or {"checked": False},
        "editability": {"checked": bool(editability), "errors": edit_errors,
                        "warnings": editability["warnings"] if editability else [],
                        "text_layout": editability["text_layout"] if editability else []},
        "note": "A pass reflects recorded checks for this artifact version; pixel difference is diagnostic, not a quality threshold.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_spec", type=Path)
    parser.add_argument("render_report", type=Path)
    parser.add_argument("visual_review", type=Path)
    parser.add_argument("--init-review", action="store_true", help="Create a hash-bound visual review template")
    parser.add_argument("--observations", type=Path, action="append", default=[])
    parser.add_argument("--scene", type=Path, help="Audit current PPTX editability against this Scene")
    parser.add_argument("--chart-observations", type=Path, help="Include independently observed bar geometry checks")
    parser.add_argument("--data-bindings", type=Path, help="Verify declared numeric, prose and notes dependencies")
    parser.add_argument("--output", type=Path, help="Write the evaluation JSON")
    args = parser.parse_args()
    spec_path = args.page_spec.resolve()
    render_path = args.render_report.resolve()
    review_path = args.visual_review.resolve()
    if args.init_review:
        if review_path.exists():
            parser.error("visual review file already exists")
        spec, _ = load_page_spec(spec_path)
        render, _ = verified_render(render_path, spec_path, len(spec["slides"]))
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text(json.dumps(review_template(spec, render), ensure_ascii=False, indent=2), encoding="utf-8")
        print(review_path)
        return
    result = evaluate(spec_path, render_path, review_path,
                      [path.resolve() for path in args.observations],
                      args.scene.resolve() if args.scene else None,
                      args.chart_observations.resolve() if args.chart_observations else None,
                      args.data_bindings.resolve() if args.data_bindings else None)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "slides": result["slides"],
                      "content_issues": result["content"]["issues"],
                      "visual_pending": len(result["visual"]["pending"]),
                      "data_pending": len(result["data"]["pending"]),
                      "data_failed": len(result["data"]["failed"])}, ensure_ascii=False))
    if result["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
