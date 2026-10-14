#!/usr/bin/env python3
"""Compare a visual transcription of generated pages with approved Page Spec text."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from json_io import read_json
from validate_page_spec import load_page_spec


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compact(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(char for char in normalized if char.isalnum() or char in ".%‰+-/")


def numbers(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value)
    return re.findall(r"(?<![A-Za-z0-9])[+-]?\d+(?:,\d{3})*(?:\.\d+)?(?:%|‰)?", normalized)


def compact_number(value: str) -> str:
    return compact(value).replace(",", "")


def image_path(spec_path: Path, slide: dict) -> Path:
    if slide["image_status"] not in ("generated", "revision", "approved"):
        raise ValueError(f"Page image is not ready for transcription: {slide['id']}")
    root = spec_path.resolve().parent
    target = (root / slide["image_file"]).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise ValueError(f"Missing or unsafe page image: {slide['image_file']}")
    return target


def template(spec_path: Path, slides: list[dict]) -> dict:
    return {"version": "1.0", "slides": [
        {"id": slide["id"], "image_sha256": sha256(image_path(spec_path, slide)),
         "status": "partial", "observed_text": ""}
        for slide in slides
    ]}


def audit(spec_path: Path, slides: list[dict], observations: dict) -> dict:
    if observations.get("version") != "1.0" or not isinstance(observations.get("slides"), list):
        raise ValueError("Observations must contain version 1.0 and a slides array")
    by_id = {slide["id"]: slide for slide in slides}
    seen = set()
    results = []
    for observation in observations["slides"]:
        slide_id = observation.get("id")
        if slide_id not in by_id or slide_id in seen:
            raise ValueError(f"Unknown or duplicate observation slide: {slide_id}")
        seen.add(slide_id)
        slide = by_id[slide_id]
        current_hash = sha256(image_path(spec_path, slide))
        if observation.get("image_sha256") != current_hash:
            raise ValueError(f"Stale visual transcription for {slide_id}: image hash changed")
        status = observation.get("status")
        text = observation.get("observed_text")
        if status not in ("partial", "complete") or not isinstance(text, str):
            raise ValueError(f"{slide_id}: status must be partial/complete and observed_text must be a string")
        observed = compact(text)
        observed_numbers = {compact_number(number) for number in numbers(text)}
        findings = []
        expected = [
            (element["id"], element["text"])
            for element in slide["elements"]
            if element["kind"] == "text" and element["confirmation_status"] != "unresolved"
        ]
        expected += [("required_visible_values", value) for value in slide.get("required_visible_values", [])]
        for element_id, value in expected:
            if compact(value) and compact(value) not in observed:
                missing_numbers = [number for number in numbers(value) if compact_number(number) not in observed_numbers]
                findings.append({
                    "element_id": element_id,
                    "expected": value,
                    "kind": "missing_numeric" if missing_numbers else "missing_text",
                    "missing_numbers": missing_numbers,
                    "status": "issue" if status == "complete" else "needs_review",
                })
        results.append({"id": slide_id, "status": status, "findings": findings,
                        "unresolved_source_elements": [element["id"] for element in slide["elements"]
                                                       if element["confirmation_status"] == "unresolved"],
                        "unchecked_data_elements": [element["id"] for element in slide["elements"]
                                                    if element["kind"] in ("chart", "table")]})
    missing_slides = sorted(set(by_id) - seen)
    issues = sum(finding["status"] == "issue" for result in results for finding in result["findings"])
    incomplete = len(missing_slides) + sum(result["status"] != "complete" for result in results)
    return {"slides": results, "missing_observations": missing_slides, "issues": issues,
            "incomplete": incomplete, "pass": issues == 0 and incomplete == 0,
            "note": "Visual transcription is evidence, not authority. Chart/table data and unrecognized text still require review."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_spec", type=Path)
    parser.add_argument("observations", type=Path)
    parser.add_argument("--init", action="store_true", help="Create a hash-bound transcription template")
    parser.add_argument("--slide", action="append", default=[], help="Check or prepare only this slide ID")
    parser.add_argument("--output", type=Path, help="Write JSON audit report")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    spec_path = args.page_spec.resolve()
    spec, _ = load_page_spec(spec_path)
    ids = set(args.slide)
    if ids - {slide["id"] for slide in spec["slides"]}:
        parser.error(f"Unknown slide IDs: {', '.join(sorted(ids - {slide['id'] for slide in spec['slides']}))}")
    slides = [slide for slide in spec["slides"] if not ids or slide["id"] in ids]
    if args.init:
        if args.observations.exists():
            parser.error("observation file already exists")
        args.observations.parent.mkdir(parents=True, exist_ok=True)
        args.observations.write_text(json.dumps(template(spec_path, slides), ensure_ascii=False, indent=2), encoding="utf-8")
        print(args.observations)
        return
    observations = read_json(args.observations)
    if ids:
        observations = {**observations, "slides": [item for item in observations["slides"] if item.get("id") in ids]}
    report = audit(spec_path, slides, observations)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"issues": report["issues"], "incomplete": report["incomplete"], "pass": report["pass"]}, ensure_ascii=False))
    if report["issues"] or (args.require_complete and report["incomplete"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
