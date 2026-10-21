#!/usr/bin/env python3
"""Inspect a PPTX package without third-party Python dependencies."""

from __future__ import annotations

import argparse
import hashlib
import posixpath
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote
from xml.etree import ElementTree as ET

from _report import Diagnostic, emit_report


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def xml_root(archive: zipfile.ZipFile, name: str, diagnostics: list[Diagnostic]) -> ET.Element | None:
    try:
        return ET.fromstring(archive.read(name))
    except KeyError:
        diagnostics.append(Diagnostic("error", "PPTX_PART_MISSING", f"Missing package part: {name}", name))
    except ET.ParseError as exc:
        diagnostics.append(Diagnostic("error", "PPTX_XML", f"Invalid XML: {exc}", name))
    return None


def relationship_owner(rels_name: str) -> str:
    path = PurePosixPath(rels_name)
    if rels_name == "_rels/.rels":
        return ""
    parts = list(path.parts)
    try:
        rels_index = parts.index("_rels")
    except ValueError:
        return ""
    filename = parts[-1]
    if not filename.endswith(".rels"):
        return ""
    owner_name = filename[: -len(".rels")]
    return str(PurePosixPath(*parts[:rels_index], owner_name))


def resolve_target(owner: str, target: str) -> str:
    target = unquote(target).replace("\\", "/")
    if target.startswith("/"):
        return target.lstrip("/")
    base = posixpath.dirname(owner)
    return posixpath.normpath(posixpath.join(base, target)).lstrip("./")


def relationship_map(archive: zipfile.ZipFile, rels_name: str, diagnostics: list[Diagnostic]) -> dict[str, dict[str, str]]:
    root = xml_root(archive, rels_name, diagnostics)
    if root is None:
        return {}
    owner = relationship_owner(rels_name)
    result: dict[str, dict[str, str]] = {}
    for rel in root.findall("rel:Relationship", NS):
        rel_id = rel.get("Id", "")
        target = rel.get("Target", "")
        mode = rel.get("TargetMode", "Internal")
        result[rel_id] = {
            "target": target,
            "resolved": target if mode == "External" else resolve_target(owner, target),
            "mode": mode,
            "type": rel.get("Type", ""),
        }
    return result


def slide_order(archive: zipfile.ZipFile, diagnostics: list[Diagnostic]) -> tuple[list[str], dict[str, Any]]:
    presentation = xml_root(archive, "ppt/presentation.xml", diagnostics)
    rels = relationship_map(archive, "ppt/_rels/presentation.xml.rels", diagnostics)
    if presentation is None:
        return [], {}
    order: list[str] = []
    for node in presentation.findall("p:sldIdLst/p:sldId", NS):
        rel_id = node.get(f"{{{NS['r']}}}id", "")
        rel = rels.get(rel_id)
        if not rel:
            diagnostics.append(Diagnostic("error", "PPTX_SLIDE_REL", f"Slide relationship {rel_id!r} is missing", "ppt/presentation.xml"))
            continue
        order.append(rel["resolved"])

    size = presentation.find("p:sldSz", NS)
    geometry: dict[str, Any] = {}
    if size is not None:
        try:
            cx, cy = int(size.get("cx", "0")), int(size.get("cy", "0"))
            geometry = {
                "cx": cx,
                "cy": cy,
                "width_inches": round(cx / 914400, 3),
                "height_inches": round(cy / 914400, 3),
                "aspect": round(cx / cy, 4) if cy else None,
            }
        except ValueError:
            diagnostics.append(Diagnostic("warning", "PPTX_SIZE", "Invalid slide-size values", "ppt/presentation.xml"))
    return order, geometry


def shape_text(shape: ET.Element) -> str:
    values = [node.text or "" for node in shape.findall(".//a:t", NS)]
    return " ".join(value.strip() for value in values if value.strip())


def inspect_slide(root: ET.Element, index: int, part: str) -> dict[str, Any]:
    texts = [node.text or "" for node in root.findall(".//a:t", NS)]
    all_text = " ".join(value.strip() for value in texts if value.strip())
    title = ""
    placeholders: list[dict[str, Any]] = []
    for shape in root.findall(".//p:sp", NS):
        ph = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
        if ph is None:
            continue
        ph_type = ph.get("type", "body")
        text = shape_text(shape)
        placeholders.append({"type": ph_type, "has_text": bool(text), "text": text})
        if ph_type in {"title", "ctrTitle"} and text and not title:
            title = text
    if not title:
        title = next((value.strip() for value in texts if value.strip()), "")
    return {
        "index": index,
        "part": part,
        "title": title,
        "text": all_text,
        "word_count": len(all_text.split()),
        "text_sha256": hashlib.sha256(all_text.encode("utf-8")).hexdigest() if all_text else None,
        "placeholder_count": len(placeholders),
        "empty_placeholders": [item["type"] for item in placeholders if not item["has_text"]],
        "chart_count": len(root.findall(".//c:chart", NS)),
        "table_count": len(root.findall(".//a:tbl", NS)),
    }


def inspect_package(path: Path) -> tuple[list[Diagnostic], dict[str, Any]]:
    diagnostics: list[Diagnostic] = []
    try:
        archive = zipfile.ZipFile(path)
    except (FileNotFoundError, zipfile.BadZipFile, OSError) as exc:
        return [Diagnostic("error", "PPTX_OPEN", str(exc), str(path))], {}

    with archive:
        names = set(archive.namelist())
        for required in ("[Content_Types].xml", "_rels/.rels", "ppt/presentation.xml"):
            if required not in names:
                diagnostics.append(Diagnostic("error", "PPTX_REQUIRED", f"Missing required package part: {required}", required))

        missing_targets: list[dict[str, str]] = []
        external_links: list[dict[str, str]] = []
        rels_files = sorted(name for name in names if name.endswith(".rels"))
        for rels_name in rels_files:
            rels = relationship_map(archive, rels_name, diagnostics)
            for rel_id, rel in rels.items():
                if rel["mode"] == "External":
                    external_links.append({"part": rels_name, "id": rel_id, "target": rel["target"], "type": rel["type"]})
                elif rel["resolved"] not in names:
                    missing_targets.append({"part": rels_name, "id": rel_id, "target": rel["resolved"]})
        for item in missing_targets:
            diagnostics.append(Diagnostic("error", "PPTX_BROKEN_REL", f"Relationship target missing: {item['target']}", item["part"]))

        order, geometry = slide_order(archive, diagnostics)
        slides: list[dict[str, Any]] = []
        for index, part in enumerate(order, 1):
            root = xml_root(archive, part, diagnostics)
            if root is None:
                continue
            record = inspect_slide(root, index, part)
            slides.append(record)
            if not record["title"]:
                diagnostics.append(Diagnostic("warning", "PPTX_NO_TITLE", "No title or text could be inferred", f"slide {index}"))
            if record["empty_placeholders"]:
                diagnostics.append(Diagnostic("warning", "PPTX_EMPTY_PLACEHOLDER", "Empty placeholders: " + ", ".join(record["empty_placeholders"]), f"slide {index}"))

        hashes = Counter(record["text_sha256"] for record in slides if record["text_sha256"])
        for digest, count in hashes.items():
            if count > 1:
                duplicate_slides = [str(record["index"]) for record in slides if record["text_sha256"] == digest]
                diagnostics.append(Diagnostic("warning", "PPTX_DUP_TEXT", f"Identical slide text on slides {', '.join(duplicate_slides)}"))

        notes_parts = sorted(name for name in names if name.startswith("ppt/notesSlides/notesSlide") and name.endswith(".xml"))
        notes_with_text = 0
        for part in notes_parts:
            root = xml_root(archive, part, diagnostics)
            if root is None:
                continue
            note_text = " ".join((node.text or "").strip() for node in root.findall(".//a:t", NS) if (node.text or "").strip())
            # PowerPoint often includes slide-number placeholders; require more than a bare number.
            if any(token for token in note_text.split() if not token.isdigit()):
                notes_with_text += 1

        media_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".emf", ".wmf", ".tif", ".tiff", ".bmp", ".mp4", ".mp3", ".wav", ".m4a", ".mov"}
        media = [name for name in names if PurePosixPath(name).suffix.lower() in media_extensions and (name.startswith("ppt/media/") or name.startswith("ppt/embeddings/"))]
        report = {
            "schema_version": "1.0",
            "file": str(path),
            "size_bytes": path.stat().st_size,
            "zip_part_count": len(names),
            "slide_count": len(order),
            "slide_geometry": geometry,
            "slides": slides,
            "notes_part_count": len(notes_parts),
            "notes_with_text": notes_with_text,
            "chart_count": sum(record["chart_count"] for record in slides),
            "table_count": sum(record["table_count"] for record in slides),
            "media_count": len(media),
            "external_relationships": external_links,
            "missing_relationship_targets": missing_targets,
            "limitations": [
                "This is a structural OOXML preflight, not a visual render check.",
                "Title inference may use the first text object when no title placeholder exists.",
                "Open and render the deck in a target office application before delivery.",
            ],
        }
        if not order:
            diagnostics.append(Diagnostic("error", "PPTX_NO_SLIDES", "No ordered slides found", "ppt/presentation.xml"))
        if external_links:
            diagnostics.append(Diagnostic("info", "PPTX_EXTERNAL", f"Package has {len(external_links)} external relationships; verify offline behavior"))
        return diagnostics, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx")
    parser.add_argument("--json", dest="json_output", help="Write full JSON report")
    args = parser.parse_args()
    path = Path(args.pptx).expanduser().resolve()
    diagnostics, report = inspect_package(path)
    return emit_report(
        "PPTX structural inspection",
        diagnostics,
        json_output=args.json_output,
        extra={"report": report},
    )


if __name__ == "__main__":
    raise SystemExit(main())
