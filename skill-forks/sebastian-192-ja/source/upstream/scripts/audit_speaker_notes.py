#!/usr/bin/env python3
"""Compare declared speaker notes with saved PPTX notes and optional Scene."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pptx import Presentation
from scene import load_scene
from speaker_notes import check_notes, check_scene_notes
from validate_page_spec import load_page_spec


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(spec_path: Path, deck_path: Path, scene_path: Path | None = None) -> dict:
    spec, _ = load_page_spec(spec_path)
    presentation = Presentation(deck_path)
    errors = check_notes(presentation, spec["slides"])
    if scene_path:
        scene, _ = load_scene(scene_path)
        errors.extend(check_scene_notes(spec, scene))
        errors.extend(check_notes(presentation, scene["slides"], scene=True))
    declared = [slide["id"] for slide in spec["slides"] if "speaker_notes" in slide]
    return {"status": "fail" if errors else "pass" if declared else "not_declared",
            "page_spec_sha256": sha256(spec_path), "deck_sha256": sha256(deck_path),
            "scene_sha256": sha256(scene_path) if scene_path else None,
            "declared_slide_ids": declared, "errors": errors,
            "scope": "Exact declared text, with CR/LF normalization; not semantic depth or visual review."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_spec", type=Path)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--scene", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.resolve() in {p.resolve() for p in (args.page_spec, args.pptx, args.scene) if p}:
        parser.error("report must not overwrite an input")
    try:
        report = audit(args.page_spec, args.pptx, args.scene)
    except (ValueError, OSError) as error:
        parser.exit(2, f"audit_speaker_notes: {error}\n")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True))
    raise SystemExit(1 if report["errors"] else 0)


if __name__ == "__main__":
    main()
