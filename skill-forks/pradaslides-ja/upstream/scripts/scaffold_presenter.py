#!/usr/bin/env python3
"""Create a dependency-free PradaSlides HTML presenter workspace."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def default_tone(slide: dict[str, Any], index: int, total: int) -> str:
    if slide.get("role") in {"cover", "closing"}:
        return "dark"
    if slide.get("role") == "section":
        return "accent"
    return "dark" if index in {max(1, total // 2)} else "light"


def create_deck(plan: dict[str, Any], design: dict[str, Any]) -> dict[str, Any]:
    slides = plan.get("slides") if isinstance(plan.get("slides"), list) else []
    output_slides = []
    for index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        output_slides.append(
            {
                "id": slide.get("id") or f"P{index + 1:02d}",
                "role": slide.get("role") or "content",
                "topology": slide.get("topology") or "stage",
                "layout": slide.get("layout_id") or slide.get("layout_family") or "custom-scaffold",
                "tone": slide.get("tone") or default_tone(slide, index, len(slides)),
                "density": "standard",
                "transition": "none",
                "title": slide.get("title") or "",
                "kicker": str(slide.get("journey_phase") or slide.get("role") or "").upper(),
                "html": (
                    '<div class="prada-composition">'
                    '<div class="prada-region prada-region-copy" data-slot="copy"></div>'
                    '<div class="prada-region prada-region-visual" data-slot="visual"></div>'
                    "</div>"
                ),
                "notes": slide.get("speaker_notes_purpose") or "",
                "source": " · ".join(slide.get("source_ids", [])),
                "furniture": {
                    "kicker": True,
                    "pageNumber": True,
                    "progress": True,
                    "frameCorners": slide.get("role") in {"cover", "closing"},
                    "sectionRail": slide.get("role") == "section",
                    "ghostMarker": False,
                    "metricStrip": False,
                    "pageHint": slide.get("role") == "cover",
                    "sourceLine": bool(slide.get("source_ids")),
                },
                "authoring": {
                    "incomplete": True,
                    "instruction": "Replace html with audience-facing composition and clear this flag before delivery.",
                },
            }
        )
    return {
        "meta": {
            "title": plan.get("project") or "PradaSlides deck",
            "status": "draft",
            "storageKey": "pradaslides:" + str(plan.get("project") or "deck").lower().replace(" ", "-"),
            "transition": "none",
        },
        "design": {
            "canvas": design.get("canvas", {}),
            "typography": design.get("typography", {}),
            "color": design.get("color", {}),
        },
        "slides": output_slides,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deck-plan", type=Path, required=True)
    parser.add_argument("--design-system", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="Replace runtime files; preserve unrelated files")
    args = parser.parse_args()

    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    runtime = Path(__file__).resolve().parents[1] / "assets" / "html-presenter"
    if not runtime.is_dir():
        raise SystemExit(f"Presenter runtime missing: {runtime}")
    for name in ("index.html", "presenter.css", "presenter.js", "deck.css"):
        destination = output / name
        if destination.exists() and not args.force:
            continue
        shutil.copy2(runtime / name, destination)

    deck_path = output / "deck.js"
    if deck_path.exists() and not args.force:
        print(f"Preserved existing: {deck_path}")
    else:
        plan = load_object(args.deck_plan)
        design = load_object(args.design_system)
        payload = create_deck(plan, design)
        deck_path.write_text(
            "window.PRADA_DECK = "
            + json.dumps(payload, ensure_ascii=False, indent=2)
            + ";\n",
            encoding="utf-8",
        )
        print(f"Created authoring scaffold: {deck_path}")
    print(f"Presenter runtime ready: {output}")
    print("Author each slide's html and clear authoring.incomplete before delivery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
