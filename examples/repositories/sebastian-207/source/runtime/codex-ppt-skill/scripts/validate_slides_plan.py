#!/usr/bin/env python3
"""
Purpose: Validate slides_plan.json shape and content_budget presence.
Input: slides_plan.json.
Output: JSON validation report to stdout or --output.
Failure behavior: Report errors; exit 1 when invalid.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {"slide_id", "title", "purpose", "slide_type", "layout_family", "content_budget"}


def validate(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    slides = data.get("slides")
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(slides, list) or not slides:
        errors.append("slides must be a non-empty list")
        slides = []
    seen: set[str] = set()
    for idx, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            errors.append(f"slide {idx} must be an object")
            continue
        missing = sorted(REQUIRED - set(slide))
        if missing:
            errors.append(f"slide {idx} missing fields: {', '.join(missing)}")
        slide_id = slide.get("slide_id")
        if slide_id in seen:
            errors.append(f"duplicate slide_id: {slide_id}")
        if slide_id:
            seen.add(str(slide_id))
        budget = slide.get("content_budget")
        if not isinstance(budget, dict):
            errors.append(f"slide {idx} content_budget must be an object")
        else:
            if "max_words" not in budget:
                warnings.append(f"slide {idx} content_budget missing max_words")
            if "max_cards" not in budget:
                warnings.append(f"slide {idx} content_budget missing max_cards")
    return {"valid": not errors, "errors": errors, "warnings": warnings, "slide_count": len(slides)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slides_plan", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()
    report = validate(args.slides_plan)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
