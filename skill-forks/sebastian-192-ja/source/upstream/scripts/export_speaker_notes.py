#!/usr/bin/env python3
"""Export declared Page Spec speaker notes as a traceable Markdown companion."""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path

from audit_speaker_notes import sha256
from speaker_notes import canonical_notes
from validate_page_spec import load_page_spec


def literal(text: str) -> str:
    # Longer fences preserve source text containing Markdown fences or HTML.
    length = max([len(m) for m in re.findall(r"`+", text)] + [2]) + 1
    fence = "`" * length
    return f"{fence}text\n{text}\n{fence}"


def export(spec_path: Path, output: Path) -> dict:
    if output.suffix.lower() != ".md" or output.resolve() == spec_path.resolve():
        raise ValueError("Output must be a separate .md file")
    spec, _ = load_page_spec(spec_path)
    declared = [s for s in spec["slides"] if "speaker_notes" in s]
    if not declared:
        raise ValueError("No speaker_notes declared; production notes are not inferred from work records")
    lines = ["# SlideMuse · Speaker notes", "", literal(spec["title"]), "",
             f"Page Spec SHA-256: `{sha256(spec_path)}`", "",
             "This companion preserves declared notes and source references. It does not replace visible slide evidence.", ""]
    for slide in spec["slides"]:
        lines.extend([f"## {slide['page_number']:02d} · {slide['id']}", "", literal(slide["title"]), ""])
        if "speaker_notes" in slide:
            text = canonical_notes(slide["speaker_notes"])
            lines.extend([literal(text) if text else "(Explicitly empty speaker notes.)", ""])
        else:
            lines.extend(["(Speaker notes not declared.)", ""])
        refs = list(dict.fromkeys(slide.get("source_refs", []) + [e["source_ref"] for e in slide["elements"]]))
        if refs:
            lines.extend(["Source references:", "", literal("\n".join(refs)), ""])
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=output.parent, suffix=".md")
    os.close(fd)
    try:
        Path(temporary).write_text("\n".join(lines), encoding="utf-8")
        os.replace(temporary, output)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return {"output": str(output.resolve()), "slides": len(spec["slides"]),
            "declared_slides": len(declared), "page_spec_sha256": sha256(spec_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        report = export(args.page_spec, args.output)
    except (ValueError, OSError) as error:
        parser.exit(2, f"export_speaker_notes: {error}\n")
    print(json.dumps(report, ensure_ascii=True))


if __name__ == "__main__":
    main()
