#!/usr/bin/env python3
"""Merge approved single-page PPTX files through PowerPoint COM when available."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge verified single-page PPTX files without regenerating pages.")
    parser.add_argument("--pages", nargs="+", required=True, help="Approved single-page PPTX files.")
    parser.add_argument("--out", required=True, help="Merged deck path.")
    parser.add_argument("--manifest-out", required=True, help="Merge manifest JSON.")
    args = parser.parse_args()

    try:
        import win32com.client  # type: ignore
    except ImportError:
        manifest = {
            "method": "merge_approved_single_page_pptx",
            "merged": False,
            "failure": "pywin32 is required for PowerPoint COM merge on Windows",
            "source_single_page_pptx": args.pages,
            "regenerated_pages": False,
        }
        Path(args.manifest_out).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(manifest, indent=2))
        return 1

    output = str(Path(args.out).resolve())
    app = win32com.client.Dispatch("PowerPoint.Application")
    # Japanese fork: preserve other PowerPoint documents and create no visible window.
    had_presentations = app.Presentations.Count > 0
    presentation = app.Presentations.Add(False)
    try:
        first = app.Presentations.Open(str(Path(args.pages[0]).resolve()), True, False, False)
        try:
            presentation.PageSetup.SlideWidth = first.PageSetup.SlideWidth
            presentation.PageSetup.SlideHeight = first.PageSetup.SlideHeight
        finally:
            first.Close()
        for page in args.pages:
            presentation.Slides.InsertFromFile(str(Path(page).resolve()), presentation.Slides.Count)
            # InsertFromFile otherwise adopts the destination master's white background.
            source = app.Presentations.Open(str(Path(page).resolve()), True, False, False)
            try:
                inserted = presentation.Slides(presentation.Slides.Count)
                inserted.FollowMasterBackground = False
                inserted.Background.Fill.Solid()
                inserted.Background.Fill.ForeColor.RGB = source.Slides(1).Background.Fill.ForeColor.RGB
            finally:
                source.Close()
        presentation.SaveAs(output)
    finally:
        presentation.Close()
        if not had_presentations:
            app.Quit()

    manifest = {
        "method": "merge_japanese_fork_reviewed_single_page_pptx",
        "original_gate_not_passed": True,
        "merged": True,
        "output": output,
        "source_single_page_pptx": args.pages,
        "regenerated_pages": False,
    }
    manifest_path = Path(args.manifest_out)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
