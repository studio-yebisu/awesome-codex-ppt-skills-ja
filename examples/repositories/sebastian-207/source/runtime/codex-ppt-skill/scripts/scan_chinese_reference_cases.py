#!/usr/bin/env python3
"""
Purpose: Scan local Chinese PPT reference case sources and build a case inventory.
Input: --reference-root pointing to _reference_skills/ppt and --output pointing to chinese-gallery.
Output: case_inventory.md and case_index.json.
Failure behavior: Skip unreadable PPTX files with extraction_notes; never move or overwrite source PPTX files.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
import zipfile
from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET


EMU_PER_INCH = 914400
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}


def _read(zipf: zipfile.ZipFile, name: str) -> str:
    return zipf.read(name).decode("utf-8", errors="replace")


def _safe_id(path: Path, source_type: str) -> str:
    stem = path.parent.parent.name if source_type == "finished_deck" else path.parent.name
    stem = re.sub(r"^ppt169_", "", stem)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower() or path.stem.lower()
    return f"zh-{source_type.replace('_deck', '')}-{slug}"


def _aspect_ratio(zipf: zipfile.ZipFile) -> str:
    try:
        root = ET.fromstring(_read(zipf, "ppt/presentation.xml"))
        size = root.find("p:sldSz", NS)
        if size is None:
            return "unknown"
        width = int(size.attrib.get("cx", "0")) / EMU_PER_INCH
        height = int(size.attrib.get("cy", "0")) / EMU_PER_INCH
        ratio = width / height if height else 0
        if abs(ratio - 16 / 9) < 0.04:
            return "16:9"
        if abs(ratio - 4 / 3) < 0.04:
            return "4:3"
        return f"{ratio:.3f}:1"
    except Exception:
        return "unknown"


def _texts(xml: str) -> list[str]:
    return [unescape(t).strip() for t in re.findall(r"<a:t[^>]*>(.*?)</a:t>", xml, flags=re.S) if t.strip()]


def _heuristics(path: Path, text: str, source_type: str) -> tuple[str, list[str], list[str]]:
    lower = str(path).lower()
    tags: list[str] = []
    useful: set[str] = {"typography"}
    use_case = "general chinese presentation"

    rules = [
        ("ai", "AI / technology", ["tech", "business"], ["business", "structure"]),
        ("lora", "AI technical explanation", ["tech", "academic"], ["academic", "structure"]),
        ("fashion", "fashion weekly digest", ["editorial", "magazine"], ["visual", "typography"]),
        ("home", "home design trends", ["lifestyle", "editorial"], ["visual", "style"]),
        ("lin_huiyin", "Chinese architecture/person profile", ["culture", "architecture"], ["style", "structure"]),
        ("liziqi", "Chinese cultural color story", ["chinese-culture", "visual"], ["style", "visual"]),
        ("swiss", "design education", ["swiss-grid", "design"], ["typography", "structure"]),
        ("high_rise", "urban issue / news analysis", ["news", "public-issue"], ["structure", "business"]),
        ("global_ai", "AI capital / business analysis", ["business", "data"], ["business", "chart"]),
        ("pritzker", "architecture / art space", ["architecture", "editorial"], ["visual", "style"]),
        ("bookstore", "zine / bookstore culture", ["zine", "editorial"], ["style", "typography"]),
        ("ucas", "Chinese academic template", ["academic", "institution"], ["template", "structure"]),
        ("thu", "Chinese university template", ["academic", "institution"], ["template", "structure"]),
        ("hit", "Chinese university template", ["academic", "institution"], ["template", "structure"]),
        ("beamer", "technical interview or academic talk", ["academic", "technical"], ["template", "structure"]),
    ]
    for needle, case, add_tags, add_useful in rules:
        if needle in lower:
            use_case = case
            tags.extend(add_tags)
            useful.update(add_useful)
    if source_type == "template":
        useful.add("template")
    else:
        useful.add("style")
    if re.search(r"\d+%|\b\d+[,.]?\d*\b|\u6570\u636e|\u8d44\u672c|\u8d8b\u52bf|\u5e02\u573a", text):
        useful.add("chart")
    return use_case, sorted(set(tags)), sorted(useful)


def _inspect_case(path: Path, source_type: str) -> dict[str, object]:
    try:
        with zipfile.ZipFile(path) as zipf:
            names = zipf.namelist()
            slide_parts = sorted(n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n))
            all_texts: list[str] = []
            placeholder_count = 0
            picture_count = 0
            for part in slide_parts:
                xml = _read(zipf, part)
                all_texts.extend(_texts(xml))
                placeholder_count += len(re.findall(r"<p:ph\b", xml))
                picture_count += len(re.findall(r"<p:pic\b", xml))
            text_joined = " ".join(all_texts)
            cjk_count = len([t for t in all_texts if re.search(r"[\u4e00-\u9fff]", t)])
            layout_names = []
            for name in sorted(n for n in names if n.startswith("ppt/slideLayouts/slideLayout") and n.endswith(".xml")):
                xml = _read(zipf, name)
                match = re.search(r'<p:cSld[^>]*name="([^"]+)"', xml)
                layout_names.append(unescape(match.group(1)) if match else Path(name).stem)
            use_case, tags, useful = _heuristics(path, text_joined, source_type)
            return {
                "case_id": _safe_id(path, source_type),
                "source_path": str(path),
                "source_type": source_type,
                "page_count": len(slide_parts),
                "aspect_ratio": _aspect_ratio(zipf),
                "likely_use_case": use_case,
                "style_tags": tags,
                "dominant_colors": [],
                "layout_patterns": layout_names[:12] if layout_names else ["unknown"],
                "has_master_or_layouts": any(n.startswith("ppt/slideMasters/") or n.startswith("ppt/slideLayouts/") for n in names),
                "has_placeholders": placeholder_count > 0,
                "useful_for": useful,
                "extraction_notes": f"Metadata-only V1 scan. Chinese text runs: {cjk_count}. Pictures: {picture_count}. Dominant colors and thumbnails not generated in V1.",
                "risks_or_limitations": "May include rasterized visuals; editability and visual quality require manual inspection.",
            }
    except Exception as exc:
        return {
            "case_id": _safe_id(path, source_type),
            "source_path": str(path),
            "source_type": source_type,
            "page_count": 0,
            "aspect_ratio": "unknown",
            "likely_use_case": "unknown",
            "style_tags": [],
            "dominant_colors": [],
            "layout_patterns": [],
            "has_master_or_layouts": False,
            "has_placeholders": False,
            "useful_for": [],
            "extraction_notes": f"scan_failed: {exc}",
            "risks_or_limitations": "Unreadable by V1 scanner.",
        }


def discover(reference_root: Path) -> tuple[list[Path], list[Path], list[str]]:
    missing: list[str] = []
    finished_pattern = reference_root / "hugohe3__ppt-master" / "examples" / "ppt169_*" / "exports" / "*.pptx"
    template_pattern = reference_root / "icip-cas__PPTAgent" / "pptagent" / "templates" / "*" / "source.pptx"
    finished = [Path(p) for p in glob.glob(str(finished_pattern))]
    templates = [Path(p) for p in glob.glob(str(template_pattern))]
    if not finished:
        missing.append(str(finished_pattern))
    if not templates:
        missing.append(str(template_pattern))
    return sorted(finished), sorted(templates), missing


def write_inventory(cases: list[dict[str, object]], missing: list[str], output: Path) -> None:
    lines = [
        "# Chinese Reference Case Inventory",
        "",
        "Generated by `scripts/scan_chinese_reference_cases.py`.",
        "",
        f"- Case count: {len(cases)}",
        f"- Missing source patterns: {', '.join(missing) if missing else 'none'}",
        "",
        "| case_id | source_type | pages | aspect | likely_use_case | useful_for | source_path |",
        "|---|---:|---:|---|---|---|---|",
    ]
    for case in cases:
        lines.append(
            f"| `{case['case_id']}` | {case['source_type']} | {case['page_count']} | {case['aspect_ratio']} | {case['likely_use_case']} | {', '.join(case['useful_for'])} | `{case['source_path']}` |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference-root", type=Path, default=Path("_reference_skills/ppt"))
    parser.add_argument("--output", type=Path, default=Path("codex-ppt-skill/assets/reference-cases/chinese-gallery"))
    args = parser.parse_args()

    finished, templates, missing = discover(args.reference_root)
    cases = [_inspect_case(p, "finished_deck") for p in finished]
    cases.extend(_inspect_case(p, "template") for p in templates)
    cases.sort(key=lambda c: str(c["case_id"]))

    args.output.mkdir(parents=True, exist_ok=True)
    write_inventory(cases, missing, args.output / "case_inventory.md")
    (args.output / "case_index.json").write_text(
        json.dumps({"case_count": len(cases), "missing_source_patterns": missing, "cases": cases}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Scanned {len(cases)} cases.")
    if missing:
        print("Missing patterns:")
        for item in missing:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
