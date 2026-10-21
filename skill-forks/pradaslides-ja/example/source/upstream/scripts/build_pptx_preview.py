#!/usr/bin/env python3
"""Build a dependency-free presenter preview from final PPTX slide renders."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def natural_key(path: Path) -> list[Any]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def load_plan(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    slides = value.get("slides", []) if isinstance(value, dict) else []
    return [slide for slide in slides if isinstance(slide, dict)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--slides-dir", type=Path, required=True)
    parser.add_argument("--deck-plan", type=Path)
    parser.add_argument("--title", default="PradaSlides presentation")
    parser.add_argument("--stage-width", type=int, default=1600)
    parser.add_argument("--stage-height", type=int, default=900)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    output = args.output.expanduser().resolve()
    source_dir = args.slides_dir.expanduser().resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"Slide render directory missing: {source_dir}")
    images = sorted(
        (path for path in source_dir.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS),
        key=natural_key,
    )
    if not images:
        raise SystemExit(f"No slide images found in: {source_dir}")

    runtime = Path(__file__).resolve().parents[1] / "assets" / "html-presenter"
    output.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "presenter.css", "presenter.js", "deck.css"):
        destination = output / name
        if destination.exists() and not args.force:
            continue
        shutil.copy2(runtime / name, destination)

    copied_dir = output / "slides"
    copied_dir.mkdir(exist_ok=True)
    if args.force:
        for stale in copied_dir.iterdir():
            if stale.is_file() and stale.name.startswith("slide-") and stale.suffix.lower() in IMAGE_EXTENSIONS:
                stale.unlink()
    plan = load_plan(args.deck_plan.expanduser().resolve() if args.deck_plan else None)
    slides: list[dict[str, Any]] = []
    furniture = {
        "kicker": False,
        "pageNumber": False,
        "progress": False,
        "frameCorners": False,
        "sectionRail": False,
        "ghostMarker": False,
        "metricStrip": False,
        "pageHint": False,
        "sourceLine": False,
    }

    for index, source in enumerate(images):
        destination = copied_dir / f"slide-{index + 1:03d}{source.suffix.lower()}"
        shutil.copy2(source, destination)
        planned = plan[index] if index < len(plan) else {}
        title = str(planned.get("title") or f"Slide {index + 1}")
        notes = str(planned.get("speaker_notes") or planned.get("speaker_notes_purpose") or "")
        relative = destination.relative_to(output).as_posix()
        slides.append(
            {
                "id": planned.get("id") or f"P{index + 1:02d}",
                "role": planned.get("role") or "content",
                "topology": planned.get("topology") or "render",
                "layout": "pptx-render",
                "tone": "dark",
                "density": "standard",
                "transition": "none",
                "title": title,
                "kicker": "",
                "classes": ["rendered-preview"],
                "html": (
                    f'<img class="prada-rendered-slide" src="{html.escape(relative, quote=True)}" '
                    f'alt="{html.escape(title, quote=True)}">'
                ),
                "notes": notes,
                "source": "",
                "furniture": furniture,
                "authoring": {"incomplete": False},
            }
        )

    payload = {
        "meta": {
            "title": args.title,
            "status": "final",
            "previewMode": "render-parity",
            "storageKey": "pradaslides:preview:" + re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-"),
            "transition": "none",
        },
        "design": {"canvas": {"width_px": args.stage_width, "height_px": args.stage_height}},
        "slides": slides,
    }
    deck_path = output / "deck.js"
    if deck_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite without --force: {deck_path}")
    deck_path.write_text(
        "window.PRADA_DECK = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Presenter preview ready: {output / 'index.html'}")
    print(f"Slides copied: {len(slides)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
