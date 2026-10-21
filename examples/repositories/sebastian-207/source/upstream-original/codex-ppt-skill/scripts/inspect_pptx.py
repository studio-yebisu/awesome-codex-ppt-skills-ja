#!/usr/bin/env python3
"""
Purpose: Inspect a PPTX without third-party dependencies.
Input: A .pptx path.
Output: JSON with slide count, size, text runs, media entries, layout names, placeholders.
Failure behavior: Exit non-zero with a concise error; never modify the input file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET


EMU_PER_INCH = 914400
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def _read(zipf: zipfile.ZipFile, name: str) -> str:
    return zipf.read(name).decode("utf-8", errors="replace")


def _xml_text_runs(xml: str) -> list[str]:
    runs = re.findall(r"<a:t[^>]*>(.*?)</a:t>", xml, flags=re.S)
    return [unescape(re.sub(r"\s+", " ", r)).strip() for r in runs if r.strip()]


def _presentation_size(zipf: zipfile.ZipFile) -> dict[str, object]:
    try:
        root = ET.fromstring(_read(zipf, "ppt/presentation.xml"))
        size = root.find("p:sldSz", NS)
        if size is None:
            return {"aspect_ratio": "unknown", "width_in": None, "height_in": None}
        cx = int(size.attrib.get("cx", "0"))
        cy = int(size.attrib.get("cy", "0"))
        width = round(cx / EMU_PER_INCH, 3) if cx else None
        height = round(cy / EMU_PER_INCH, 3) if cy else None
        ratio = "unknown"
        if width and height:
            ratio_value = width / height
            ratio = "16:9" if abs(ratio_value - 16 / 9) < 0.04 else "4:3" if abs(ratio_value - 4 / 3) < 0.04 else f"{ratio_value:.3f}:1"
        return {"aspect_ratio": ratio, "width_in": width, "height_in": height, "cx": cx, "cy": cy}
    except Exception as exc:
        return {"aspect_ratio": "unknown", "width_in": None, "height_in": None, "error": str(exc)}


def _layout_info(zipf: zipfile.ZipFile) -> list[dict[str, object]]:
    layouts: list[dict[str, object]] = []
    for name in sorted(n for n in zipf.namelist() if n.startswith("ppt/slideLayouts/slideLayout") and n.endswith(".xml")):
        xml = _read(zipf, name)
        match = re.search(r'<p:cSld[^>]*name="([^"]+)"', xml)
        placeholders = re.findall(r"<p:ph\b([^>]*)", xml)
        layouts.append(
            {
                "part": name,
                "name": unescape(match.group(1)) if match else Path(name).stem,
                "placeholder_count": len(placeholders),
            }
        )
    return layouts


def inspect_pptx(path: Path) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() != ".pptx":
        raise ValueError("Only .pptx files are supported by this V1 inspector.")

    with zipfile.ZipFile(path) as zipf:
        names = zipf.namelist()
        slide_parts = sorted(n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n))
        slides = []
        for idx, slide_part in enumerate(slide_parts, start=1):
            xml = _read(zipf, slide_part)
            slides.append(
                {
                    "slide_number": idx,
                    "part": slide_part,
                    "text_runs": _xml_text_runs(xml),
                    "placeholder_count": len(re.findall(r"<p:ph\b", xml)),
                    "shape_count": len(re.findall(r"<p:sp\b", xml)),
                    "picture_count": len(re.findall(r"<p:pic\b", xml)),
                }
            )

        return {
            "path": str(path),
            "slide_count": len(slide_parts),
            "slide_size": _presentation_size(zipf),
            "media_count": len([n for n in names if n.startswith("ppt/media/")]),
            "has_masters": any(n.startswith("ppt/slideMasters/") for n in names),
            "has_layouts": any(n.startswith("ppt/slideLayouts/") for n in names),
            "layouts": _layout_info(zipf),
            "slides": slides,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()

    try:
        data = inspect_pptx(args.pptx)
    except Exception as exc:
        print(f"inspect_pptx failed: {exc}", file=sys.stderr)
        return 1

    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
