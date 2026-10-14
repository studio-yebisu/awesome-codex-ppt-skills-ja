"""Compare declared native table text with words extracted from its real PDF render.

These are localized discrepancies for the host to inspect, not a visual verdict.
The PDF has already been rendered by Office. Source font settings alone cannot
reveal a word that the renderer has broken across lines.
"""
from __future__ import annotations
import hashlib
import posixpath
import re
import shutil
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def ordered_slide_parts(archive, presentation):
    relationships = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in relationships
               if r.get("Type", "").endswith("/slide") and r.get("TargetMode") != "External"}
    result = []
    for item in presentation.findall("p:sldIdLst/p:sldId", NS):
        target = targets[item.get(f"{{{NS['r']}}}id")]
        result.append(posixpath.normpath(target.lstrip("/") if target.startswith("/") else "ppt/" + target))
    return result


def tokens(text):
    return re.findall(r"\w+(?:[.,]\d+)*", unicodedata.normalize("NFKC", text).casefold())


def compare_cell(expected, words, bbox):
    x, y, w, h = bbox
    selected = [word for word in words if x <= (word["box"][0] + word["box"][2]) / 2 < x+w
                and y <= (word["box"][1] + word["box"][3]) / 2 < y+h]
    observed = " ".join(word["text"] for word in selected)
    # Report absent complete tokens. Do not join broken lines to hide split words.
    actual = set(tokens(observed))
    missing = sorted(set(tokens(expected)) - actual)
    return {"expected": expected, "rendered": observed, "missing_complete_tokens": missing,
            "rendered_words": selected}


def collect_rendered_table_text(pptx, pdf):
    tool = shutil.which("pdftotext")
    if tool is None:
        return {"evidence_type": "rendered_table_text", "available": False,
                "reason": "pdftotext is not available", "agent_interpretation_required": True}
    result = subprocess.run([tool, "-bbox-layout", str(pdf), "-"], capture_output=True, check=True)
    root = ET.fromstring(result.stdout)
    pages = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "page"]
    facts = []
    with zipfile.ZipFile(pptx) as archive:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        parts = ordered_slide_parts(archive, presentation)
        slides = [ET.fromstring(archive.read(part)) for part in parts]
        if len(pages) != len(slides) or any(slide.get("show") in {"0", "false"} for slide in slides):
            return {"evidence_type": "rendered_table_text", "available": False,
                    "reason": "PDF page count differs from the deck or hidden slides require explicit page mapping",
                    "pdf_pages": len(pages), "deck_pages": len(slides),
                    "agent_interpretation_required": True}
        size = presentation.find("p:sldSz", NS)
        width, height = int(size.get("cx")), int(size.get("cy"))
        for index, page in enumerate(pages, 1):
            sx, sy = float(page.get("width"))/width, float(page.get("height"))/height
            words = [{"text": node.text or "", "box": [float(node.get(k)) for k in ("xMin", "yMin", "xMax", "yMax")]}
                     for node in page.iter() if node.tag.rsplit("}", 1)[-1] == "word"]
            slide = slides[index - 1]
            # Packaged native tables are emitted at slide level. Nested transforms
            # require a separate coordinate transform and are not guessed here.
            for frame in slide.findall("p:cSld/p:spTree/p:graphicFrame", NS):
                table = frame.find(".//a:tbl", NS)
                if table is None:
                    continue
                identity = frame.find("p:nvGraphicFramePr/p:cNvPr", NS).get("name")
                offset = frame.find("p:xfrm/a:off", NS)
                left, top = int(offset.get("x"))*sx, int(offset.get("y"))*sy
                columns = [int(c.get("w"))*sx for c in table.findall("a:tblGrid/a:gridCol", NS)]
                rows = table.findall("a:tr", NS)
                heights = [int(row.get("h"))*sy for row in rows]
                for r, row in enumerate(rows):
                    for c, cell in enumerate(row.findall("a:tc", NS)):
                        text = " ".join("".join(p.itertext()) for p in cell.findall("a:txBody/a:p", NS))
                        if not text.strip() or c >= len(columns):
                            continue
                        cols, row_count = int(cell.get("gridSpan", 1)), int(cell.get("rowSpan", 1))
                        box = [left+sum(columns[:c]), top+sum(heights[:r]), sum(columns[c:c+cols]), sum(heights[r:r+row_count])]
                        evidence = compare_cell(text, words, box)
                        facts.append({"slide_number": index, "table": identity, "row": r, "column": c,
                                      "bbox_pdf_points": box, **evidence})
    return {"evidence_type": "rendered_table_text", "available": True,
            "pptx_sha256": hashlib.sha256(pptx.read_bytes()).hexdigest(),
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "cells": facts, "discrepancies": [f for f in facts if f["missing_complete_tokens"]],
            "agent_interpretation_required": True,
            "limitations": "PDF extraction can differ for ligatures or unusual scripts. An absent complete token is evidence to inspect, not a visual acceptance decision."}
