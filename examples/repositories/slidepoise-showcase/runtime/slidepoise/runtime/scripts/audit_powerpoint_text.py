#!/usr/bin/env python3
"""Audit explicit PowerPoint text settings in a generated PPTX."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


TEXT_ANCHORS = {"t", "ctr", "b", "just", "dist"}
CELL_MARGINS = {"marL", "marR", "marT", "marB"}


def integer_in_range(value: str | None, minimum: int, maximum: int) -> bool:
    return bool(value is not None and re.fullmatch(r"[+-]?[0-9]+", value)
                and minimum <= int(value) <= maximum)


def autofit_name(body_pr: ET.Element) -> str | None:
    for local in ("noAutofit", "normAutofit", "spAutoFit"):
        if body_pr.find(f"a:{local}", NS) is not None:
            return local
    return None


def text_body_record(name: str, tx_body: ET.Element, cell_pr: ET.Element | None = None) -> dict:
    body_pr = tx_body.find("a:bodyPr", NS)
    paragraphs = tx_body.findall("a:p", NS)
    runs = tx_body.findall(".//a:r", NS)
    fonts = sorted(
        {
            node.get("typeface")
            for node in tx_body.findall(".//a:rPr/a:latin", NS)
            if node.get("typeface")
        }
    )
    sizes = sorted(
        {
            int(node.get("sz")) / 100
            for node in tx_body.findall(".//a:rPr", NS)
            if integer_in_range(node.get("sz"), 100, 400000)
        }
    )
    visible_text = "".join(node.text or "" for node in tx_body.findall(".//a:t", NS)).strip()
    body = dict(body_pr.attrib) if body_pr is not None else {}
    record = {
        "name": name,
        "paragraph_count": len(paragraphs),
        "run_count": len(runs),
        "fonts": fonts,
        "font_sizes_pt": sizes,
        "has_visible_text": bool(visible_text),
        "body_properties": body,
        "autofit": autofit_name(body_pr) if body_pr is not None else None,
        "explicit_line_spacing": all(p.find("a:pPr/a:lnSpc", NS) is not None for p in paragraphs),
        "explicit_paragraph_alignment": all(
            (p.find("a:pPr", NS) is not None and p.find("a:pPr", NS).get("algn") is not None)
            for p in paragraphs
        ),
        "all_runs_have_font": all(r.find("a:rPr/a:latin", NS) is not None for r in runs),
        "all_runs_have_size": all(
            r.find("a:rPr", NS) is not None and r.find("a:rPr", NS).get("sz") is not None
            for r in runs
        ),
        "invalid_font_sizes": [node.get("sz") for node in tx_body.findall(".//a:rPr", NS)
                               if node.get("sz") is not None
                               and not integer_in_range(node.get("sz"), 100, 400000)],
    }
    if cell_pr is not None:
        record["cell_properties"] = dict(cell_pr.attrib)
    return record


def audit(pptx: Path) -> dict:
    records: list[dict] = []
    with ZipFile(pptx) as archive:
        slide_names = sorted(
            name
            for name in archive.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        for slide_name in slide_names:
            root = ET.fromstring(archive.read(slide_name))
            for shape in root.findall(".//p:sp", NS):
                tx_body = shape.find("p:txBody", NS)
                if tx_body is None:
                    continue
                c_nv_pr = shape.find("p:nvSpPr/p:cNvPr", NS)
                name = c_nv_pr.get("name") if c_nv_pr is not None else "unnamed shape"
                record = text_body_record(name, tx_body)
                placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
                record["placeholder_type"] = placeholder.get("type") if placeholder is not None else None
                record["slide_part"] = slide_name
                record["kind"] = "shape"
                records.append(record)
            for graphic_frame in root.findall(".//p:graphicFrame", NS):
                c_nv_pr = graphic_frame.find("p:nvGraphicFramePr/p:cNvPr", NS)
                table_name = c_nv_pr.get("name") if c_nv_pr is not None else "unnamed table"
                table = graphic_frame.find(".//a:tbl", NS)
                if table is None:
                    continue
                for row_index, row in enumerate(table.findall("a:tr", NS), start=1):
                    for col_index, cell in enumerate(row.findall("a:tc", NS), start=1):
                        tx_body = cell.find("a:txBody", NS)
                        if tx_body is None:
                            continue
                        name = f"{table_name}.R{row_index}C{col_index}"
                        record = text_body_record(name, tx_body, cell.find("a:tcPr", NS))
                        record["slide_part"] = slide_name
                        record["kind"] = "table_cell"
                        records.append(record)

    findings = []
    for record in records:
        if not record["has_visible_text"]:
            continue
        # Native PowerPoint field placeholders (slide number/date/footer/header)
        # are controlled by the master/theme and do not carry ordinary run-level
        # formatting in the slide XML. Do not treat their field representation as
        # a textbox-authoring defect.
        if record.get("placeholder_type") in {"sldNum", "dt", "ftr", "hdr"}:
            continue
        if record["kind"] == "shape":
            body = record["body_properties"]
            missing = sorted({"wrap", "lIns", "tIns", "rIns", "bIns", "anchor"}.difference(body))
            if missing:
                findings.append({"name": record["name"], "issue": "missing body properties", "values": missing})
            for field in ("explicit_line_spacing", "explicit_paragraph_alignment"):
                if not record[field]:
                    findings.append({"name": record["name"], "issue": field})
        if record["autofit"] is None:
            findings.append({"name": record["name"], "issue": "autofit is implicit"})
        for field in ("all_runs_have_font", "all_runs_have_size"):
            if not record[field]:
                findings.append({"name": record["name"], "issue": field})
        if record["invalid_font_sizes"]:
            findings.append({"name": record["name"], "issue": "invalid font sizes", "values": record["invalid_font_sizes"]})
        if record["kind"] == "table_cell":
            # Table geometry uses tcPr margins/anchor. Cell paragraphs may use
            # normal DrawingML defaults, so textbox bodyPr and paragraph
            # explicitness requirements do not apply to this representation.
            cell = record.get("cell_properties", {})
            missing_cell = sorted((CELL_MARGINS | {"anchor"}).difference(cell))
            if missing_cell:
                findings.append({"name": record["name"], "issue": "missing cell properties", "values": missing_cell})
            invalid = {key: cell[key] for key in sorted(CELL_MARGINS.intersection(cell))
                       if not integer_in_range(cell[key], -(2 ** 31), 2 ** 31 - 1)}
            if "anchor" in cell and cell["anchor"] not in TEXT_ANCHORS:
                invalid["anchor"] = cell["anchor"]
            if invalid:
                findings.append({"name": record["name"], "issue": "invalid cell properties", "values": invalid})

    return {
        "pptx": str(pptx),
        "text_body_count": len(records),
        "finding_count": len(findings),
        "findings": findings,
        "text_bodies": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.pptx.expanduser().resolve())
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(1 if result["finding_count"] else 0)


if __name__ == "__main__":
    main()
