#!/usr/bin/env python3
"""Snapshot approved pages and plan which slides need regeneration or review."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from json_io import read_json
from speaker_notes import canonical_notes
from validate_page_spec import load_page_spec


def digest_bytes(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fingerprint(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def contained_path(root: Path, value: str) -> Path:
    base = root.resolve()
    target = (base / value).resolve()
    if not target.is_relative_to(base):
        raise ValueError(f"Path escapes Page Spec directory: {value}")
    return target


def style_fingerprint(spec: dict, root: Path) -> str:
    style = spec["style"]
    visible = {key: value for key, value in style.items() if key != "authorization"}
    references = {}
    for value in style.get("tokens", {}).get("reference_images", []):
        path = contained_path(root, value)
        references[value] = digest_bytes(path) if path.is_file() else None
    return fingerprint({"canvas": spec["canvas"], "style": visible, "reference_hashes": references})


def slide_fingerprint(slide: dict) -> str:
    ignored = {"image_file", "image_status", "generation_prompt", "prompt_record", "speaker_notes"}
    semantic = {key: value for key, value in slide.items() if key not in ignored}
    if "elements" in semantic:
        semantic["elements"] = [
            {key: value for key, value in element.items() if key != "prompt_record"}
            for element in semantic["elements"]
        ]
    return fingerprint(semantic)


def notes_fingerprint(slide: dict) -> str:
    return fingerprint({"declared": "speaker_notes" in slide,
                        "text": canonical_notes(slide.get("speaker_notes", ""))})


def snapshot(spec_path: Path) -> dict:
    spec, _ = load_page_spec(spec_path, require_images=True)
    root = spec_path.resolve().parent
    return {
        "version": "1.0",
        "content_version": spec["content_version"],
        "style_hash": style_fingerprint(spec, root),
        "slide_count": len(spec["slides"]),
        "slides": [
            {"id": slide["id"], "page_number": slide["page_number"],
             "semantic_hash": slide_fingerprint(slide),
             "speaker_notes_hash": notes_fingerprint(slide),
             "image_file": slide["image_file"],
             "image_sha256": digest_bytes(contained_path(root, slide["image_file"]))}
            for slide in spec["slides"]
        ],
    }


def plan(previous: dict, spec: dict, root: Path) -> dict:
    if previous.get("version") != "1.0" or not isinstance(previous.get("slides"), list):
        raise ValueError("Invalid snapshot format")
    old = {slide["id"]: slide for slide in previous["slides"]}
    if len(old) != len(previous["slides"]):
        raise ValueError("Snapshot has duplicate slide IDs")
    global_change = []
    if previous.get("style_hash") != style_fingerprint(spec, root):
        global_change.append("style_or_canvas_changed")
    if previous.get("slide_count") != len(spec["slides"]):
        global_change.append("slide_count_changed")
    results = []
    for slide in spec["slides"]:
        prior = old.get(slide["id"])
        reasons = [reason for reason in global_change if reason != "slide_count_changed"]
        if "slide_count_changed" in global_change and slide.get("depends_on_slide_count", False):
            reasons.append("slide_count_changed")
        if prior is None:
            reasons.append("new_slide")
        else:
            if prior["semantic_hash"] != slide_fingerprint(slide):
                reasons.append("content_or_layout_changed")
            if prior["page_number"] != slide["page_number"]:
                reasons.append("page_order_changed")
        path = contained_path(root, slide["image_file"])
        notes_changed = prior is not None and prior.get("speaker_notes_hash", notes_fingerprint({})) != notes_fingerprint(slide)
        current_hash = digest_bytes(path) if path.is_file() else None
        if reasons:
            action = "regenerate"
        elif current_hash is None:
            action, reasons = "regenerate", ["image_missing"]
        elif current_hash != prior["image_sha256"]:
            action, reasons = "review_existing", ["image_bytes_changed"]
        elif slide["image_status"] != "approved":
            action, reasons = "review_existing", ["image_not_approved"]
        else:
            action = "reuse"
        results.append({"id": slide["id"], "page_number": slide["page_number"],
                        "action": action, "reasons": reasons,
                        "export_reasons": ["speaker_notes_changed"] if notes_changed else [],
                        "stale_approval": action != "reuse" and slide["image_status"] == "approved"})
    removed = sorted(set(old) - {slide["id"] for slide in spec["slides"]})
    return {"version": "1.0", "global_changes": global_change, "slides": results,
            "removed_slide_ids": removed,
            "rebuild_image_deck": bool(removed) or any(item["action"] != "reuse" or item["export_reasons"] for item in results),
            "rebuild_editable_deck": bool(removed) or any(item["action"] != "reuse" or item["export_reasons"] for item in results),
            "note": "A plan does not approve images or change Page Spec. Confirm authorized changes and revalidate affected outputs."}


def write_new(path: Path, value: dict) -> None:
    if path.exists():
        raise ValueError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    command = parser.add_subparsers(dest="command", required=True)
    save = command.add_parser("snapshot", help="Record approved inputs and image hashes before editing")
    save.add_argument("page_spec", type=Path)
    save.add_argument("output", type=Path)
    compare = command.add_parser("plan", help="Compare a snapshot with a new Page Spec")
    compare.add_argument("snapshot", type=Path)
    compare.add_argument("page_spec", type=Path)
    compare.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "snapshot":
        result = snapshot(args.page_spec.resolve())
    else:
        old = read_json(args.snapshot)
        spec, _ = load_page_spec(args.page_spec.resolve())
        result = plan(old, spec, args.page_spec.resolve().parent)
    write_new(args.output, result)
    print(json.dumps({"output": str(args.output), "slides": len(result["slides"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
