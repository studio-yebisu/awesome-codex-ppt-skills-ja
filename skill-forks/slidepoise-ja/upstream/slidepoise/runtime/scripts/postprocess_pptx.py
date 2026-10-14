#!/usr/bin/env python3
"""Apply native DrawingML treatments at one namespace-aware package boundary."""
from __future__ import annotations

import argparse
import copy
import json
import posixpath
import re
import tempfile
import zipfile
from pathlib import Path

from lxml import etree


SLIDE_RE = re.compile(r"^ppt/slides/slide\d+\.xml$")
DRAWING_PART_RE = re.compile(r"^ppt/(slides/slide|slideLayouts/slideLayout|slideMasters/slideMaster)\d+\.xml$")
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}

LABEL_CHILD_ORDER = ("idx", "dLbl", "delete", "layout", "tx", "numFmt", "spPr", "txPr",
                     "dLblPos", "showLegendKey", "showVal", "showCatName", "showSerName",
                     "showPercent", "showBubbleSize", "separator", "showLeaderLines",
                     "leaderLines", "extLst")


def tag(name: str) -> str:
    prefix, local = name.split(":")
    return f"{{{NS[prefix]}}}{local}"


def parse_xml(xml: str) -> etree._Element:
    return etree.fromstring(xml.encode("utf-8"), etree.XMLParser(resolve_entities=False, no_network=True))


def normalize_shape_ids(root: etree._Element) -> int:
    """Repair emitter collisions without changing any unambiguous native reference.

    PptxGenJS assigns tables and ordinary shapes from separate ID sequences. Keep
    existing unique IDs, allocate unused IDs to repeated occurrences and missing
    properties, and reject references whose original target is already ambiguous.
    """
    properties = list(root.iter(tag("p:cNvPr")))
    by_id = {}
    for item in properties:
        value = item.get("id")
        if value is None:
            continue
        if not re.fullmatch(r"[0-9]+", value) or int(value) > 4294967295:
            raise ValueError(f"Invalid native drawing ID. {value}")
        by_id.setdefault(int(value), []).append(item)
    duplicate_ids = {value for value, items in by_id.items() if len(items) > 1}
    for element in root.iter():
        if element.tag in {tag("a:stCxn"), tag("a:endCxn")}:
            reference = element.get("id")
        elif isinstance(element.tag, str) and element.tag.startswith("{" + NS["p"] + "}") and element.tag != tag("p:oleObj"):
            # Presentation timing and build targets use spid. oleObj instead
            # refers to a VML fallback shape in a separate identifier space.
            reference = element.get("spid")
        else:
            continue
        if reference is not None and reference.isdigit() and int(reference) in duplicate_ids:
            names = [item.get("name", "") for item in by_id[int(reference)]]
            raise ValueError(f"Ambiguous native drawing reference {reference} targets duplicate IDs. {names}")
    used = set(by_id)
    seen = set()
    candidate = 1
    changed = 0
    for item in properties:
        value = int(item.get("id")) if item.get("id") is not None else None
        if value is None or value in seen:
            while candidate in used:
                candidate += 1
            if candidate > 4294967295:
                raise ValueError("No unused native drawing ID is available")
            item.set("id", str(candidate))
            used.add(candidate)
            changed += 1
        else:
            seen.add(value)
    return changed


def object_name(shape: etree._Element) -> str:
    properties = shape.find("./p:nvSpPr/p:cNvPr", NS)
    if properties is None:
        properties = shape.find("./p:nvCxnSpPr/p:cNvPr", NS)
    return properties.get("name", "") if properties is not None else ""


def normalize_route_line(shape: etree._Element) -> None:
    """Keep cap and join treatments identical for native lines and freeform routes."""
    line = shape.find("p:spPr/a:ln", NS)
    if line is None:
        return
    # An omitted size is the Office default. Do not silently enlarge endpoints.
    # Explicit, per-route sizes are applied from renderer metadata below.
    if not any(child.tag in {tag("a:round"), tag("a:bevel"), tag("a:miter")} for child in line):
        index = next((index for index, child in enumerate(line)
                      if child.tag in {tag("a:headEnd"), tag("a:tailEnd"), tag("a:extLst")}), len(line))
        line.insert(index, etree.Element(tag("a:round")))


def convert_connector(shape: etree._Element) -> bool:
    """Convert only explicitly tagged placeholders and retain native geometry."""
    name = object_name(shape)
    if shape.tag != tag("p:sp") or not name.startswith("SC_CONNECTOR__"):
        return False
    text_body = shape.find("p:txBody", NS)
    if text_body is not None:
        if any(text.text for text in text_body.findall(".//a:t", NS)):
            raise ValueError(f"Connector placeholder contains text that would be lost. {name}")
        shape.remove(text_body)
    nonvisual = shape.find("p:nvSpPr", NS)
    if nonvisual is None or nonvisual.find("p:cNvPr", NS) is None or shape.find("p:spPr", NS) is None:
        raise ValueError(f"Connector placeholder lacks native shape properties. {name}")
    shape.tag = tag("p:cxnSp")
    nonvisual.tag = tag("p:nvCxnSpPr")
    properties = nonvisual.find("p:cNvSpPr", NS)
    if properties is None:
        properties = etree.Element(tag("p:cNvCxnSpPr"))
        nonvisual.insert(1, properties)
    else:
        properties.tag = tag("p:cNvCxnSpPr")
        properties.attrib.pop("txBox", None)
        locks = properties.find("a:spLocks", NS)
        if locks is not None:
            locks.tag = tag("a:cxnSpLocks")
            locks.attrib.pop("noTextEdit", None)
    geometry = shape.find("p:spPr/a:prstGeom", NS)
    if "__CURVED" in name and geometry is not None and geometry.get("prst") == "line":
        geometry.set("prst", "curvedConnector3")
    normalize_route_line(shape)
    return True


def convert_connector_block(block: str) -> tuple[str, bool]:
    """Compatibility helper for a single XML shape fragment."""
    wrapper = parse_xml(f'<root xmlns:p="{NS["p"]}" xmlns:a="{NS["a"]}">{block}</root>')
    if len(wrapper) != 1:
        raise ValueError("Expected exactly one shape fragment")
    changed = convert_connector(wrapper[0])
    return etree.tostring(wrapper[0], encoding="unicode"), changed


def adjust_round_rectangles(root: etree._Element, adjustments: dict[str, int]) -> int:
    changed = 0
    for shape in root.iter(tag("p:sp")):
        name = object_name(shape)
        if name not in adjustments:
            continue
        geometry = shape.find("p:spPr/a:prstGeom", NS)
        if geometry is None or geometry.get("prst") != "roundRect":
            continue
        value = f"val {max(0, min(50000, int(adjustments[name])))}"
        values = geometry.find("a:avLst", NS)
        if values is None:
            values = etree.SubElement(geometry, tag("a:avLst"))
        adjustment = next((item for item in values if item.get("name") == "adj"), None)
        if adjustment is None:
            adjustment = etree.SubElement(values, tag("a:gd"), name="adj")
        if adjustment.get("fmla") != value:
            adjustment.set("fmla", value)
            changed += 1
    return changed


def apply_round_rect_adjustments(xml: str, adjustments: dict[str, int]) -> tuple[str, int]:
    root = parse_xml(xml)
    changed = adjust_round_rectangles(root, adjustments)
    return etree.tostring(root, encoding="unicode"), changed


def apply_character_spacing(root: etree._Element, spacing: dict[str, int]) -> int:
    """Preserve signed hundredths of a point, including condensed tracking."""
    changed = 0
    for shape in root.iter(tag("p:sp")):
        name = object_name(shape)
        if name not in spacing:
            continue
        raw = spacing[name]
        if isinstance(raw, bool) or not isinstance(raw, int):
            raise ValueError(f"Character spacing must be signed integer hundredths of a point. {name}")
        text_body = shape.find("p:txBody", NS)
        if text_body is None:
            raise ValueError(f"Character-spacing metadata refers to an object without a text body. {name}")
        value = str(raw)
        properties = list(text_body.findall(".//a:rPr", NS))
        properties.extend(text_body.findall(".//a:defRPr", NS))
        properties.extend(text_body.findall(".//a:endParaRPr", NS))
        for run in text_body.findall(".//a:r", NS):
            if run.find("a:rPr", NS) is None:
                prop = etree.Element(tag("a:rPr"))
                run.insert(0, prop)
                properties.append(prop)
        for paragraph in text_body.findall("a:p", NS):
            paragraph_properties = paragraph.find("a:pPr", NS)
            if paragraph_properties is None:
                paragraph_properties = etree.Element(tag("a:pPr"))
                paragraph.insert(0, paragraph_properties)
            if paragraph_properties.find("a:defRPr", NS) is None:
                prop = etree.Element(tag("a:defRPr"))
                extension = paragraph_properties.find("a:extLst", NS)
                index = paragraph_properties.index(extension) if extension is not None else len(paragraph_properties)
                paragraph_properties.insert(index, prop)
                properties.append(prop)
        if any(prop.get("spc") != value for prop in properties):
            for prop in properties:
                prop.set("spc", value)
            changed += 1
    return changed


def apply_arrowhead_sizes(root: etree._Element, treatments: dict) -> int:
    """Preserve Agent-authored endpoint sizing for both native and freeform routes."""
    found = set()
    changed = 0
    for shape in root.iter():
        if shape.tag not in {tag("p:sp"), tag("p:cxnSp")}:
            continue
        name = object_name(shape)
        if name not in treatments:
            continue
        if name in found:
            raise ValueError(f"Arrowhead metadata matches duplicate route names. {name}")
        treatment = treatments[name]
        if not isinstance(treatment, dict) or set(treatment) != {"width", "length"} or any(
                value not in {"sm", "med", "lg"} for value in treatment.values()):
            raise ValueError(f"Arrowhead size must declare native width and length. {name}")
        endpoint = shape.find("p:spPr/a:ln/a:tailEnd", NS)
        if endpoint is None or endpoint.get("type", "none") == "none":
            raise ValueError(f"Arrowhead metadata refers to a route without an arrow. {name}")
        endpoint.set("w", treatment["width"])
        endpoint.set("len", treatment["length"])
        found.add(name)
        changed += 1
    if set(treatments) - found:
        raise ValueError(f"Arrowhead metadata refers to missing routes. {sorted(set(treatments) - found)}")
    return changed


def transform_xml(xml: str, rounding: dict[str, int], spacing: dict[str, int],
                  arrowheads: dict | None = None) -> tuple[str, dict[str, int]]:
    root = parse_xml(xml)
    identifiers = normalize_shape_ids(root)
    normalized = 0
    autofit_tags = {tag("a:noAutofit"), tag("a:normAutofit"), tag("a:spAutoFit")}
    for body in root.iter(tag("a:bodyPr")):
        if not any(child.tag in autofit_tags for child in body):
            warp = body.find("a:prstTxWarp", NS)
            body.insert(body.index(warp) + 1 if warp is not None else 0, etree.Element(tag("a:noAutofit")))
            normalized += 1
    converted = sum(convert_connector(shape) for shape in list(root.iter(tag("p:sp"))))
    for shape in root.iter(tag("p:sp")):
        if object_name(shape).startswith("SC_FREEFORM_ROUTE__"):
            normalize_route_line(shape)
    rounded = adjust_round_rectangles(root, rounding)
    tracked = apply_character_spacing(root, spacing)
    sized = apply_arrowhead_sizes(root, arrowheads or {})
    if any(object_name(shape).startswith("SC_CONNECTOR__") for shape in root.iter(tag("p:sp"))):
        raise RuntimeError("Native connector conversion left an unconverted placeholder")
    facts = {"converted": converted, "textBodiesNormalized": normalized,
             "roundedRectanglesAdjusted": rounded, "textCharacterSpacingApplied": tracked,
             "shapeIdsNormalized": identifiers, "arrowheadSizesApplied": sized}
    return etree.tostring(root, encoding="unicode"), facts


def process_xml(xml: str, round_rect_adjustments: dict[str, int] | None = None,
                text_character_spacing: dict[str, int] | None = None) -> tuple[str, int, int, int]:
    """Keep the public four-value API while sharing the structural transformer."""
    updated, facts = transform_xml(xml, round_rect_adjustments or {}, text_character_spacing or {})
    return updated, facts["converted"], facts["textBodiesNormalized"], facts["roundedRectanglesAdjusted"]


def insert_label_child(parent: etree._Element, child: etree._Element) -> None:
    """Retain the DrawingML sequence while inserting an authored label property."""
    order = {tag(f"c:{name}"): index for index, name in enumerate(LABEL_CHILD_ORDER)}
    rank = order[child.tag]
    index = next((index for index, sibling in enumerate(parent)
                  if order.get(sibling.tag, len(order)) > rank), len(parent))
    parent.insert(index, child)


def chart_label_parts(source: zipfile.ZipFile, slide_name: str, xml: str,
                      treatments: dict) -> dict[str, dict]:
    """Bind authored chart object names to internal chart parts through relationships."""
    if not treatments:
        return {}
    if not isinstance(treatments, dict):
        raise ValueError("Chart-label metadata must map chart object names to treatments")
    root = parse_xml(xml)
    relationship_name = posixpath.join(posixpath.dirname(slide_name), "_rels",
                                      posixpath.basename(slide_name) + ".rels")
    relationships = parse_xml(source.read(relationship_name).decode("utf-8"))
    by_id = {relation.get("Id"): relation for relation in relationships.findall("pr:Relationship", NS)}
    bound = {}
    found = set()
    for frame in root.iter(tag("p:graphicFrame")):
        properties = frame.find("p:nvGraphicFramePr/p:cNvPr", NS)
        name = properties.get("name", "") if properties is not None else ""
        if name not in treatments:
            continue
        if name in found:
            raise ValueError(f"Chart-label metadata matches duplicate object names. {name}")
        chart = frame.find(".//c:chart", NS)
        relation = by_id.get(chart.get(tag("r:id"))) if chart is not None else None
        if relation is None or relation.get("Type") != NS["r"] + "/chart" or relation.get("TargetMode") == "External":
            raise ValueError(f"Chart-label metadata requires an internal chart relationship. {name}")
        target = relation.get("Target", "")
        part = posixpath.normpath(target.lstrip("/") if target.startswith("/") else
                                 posixpath.join(posixpath.dirname(slide_name), target))
        if not part.startswith("ppt/charts/") or part not in source.namelist():
            raise ValueError(f"Chart-label relationship does not resolve to a chart part. {name}")
        if part in bound and bound[part] != treatments[name]:
            raise ValueError(f"Shared chart part has conflicting label treatments. {part}")
        bound[part] = treatments[name]
        found.add(name)
    missing = set(treatments) - found
    if missing:
        raise ValueError(f"Chart-label metadata refers to missing chart objects. {sorted(missing)}")
    return bound


def label_text_properties(parent: etree._Element, inherited: etree._Element | None = None) -> etree._Element:
    text = parent.find("c:txPr", NS)
    if text is None:
        if inherited is not None:
            text = copy.deepcopy(inherited)
        else:
            text = etree.Element(tag("c:txPr"))
            etree.SubElement(text, tag("a:bodyPr"))
            etree.SubElement(text, tag("a:lstStyle"))
            paragraph = etree.SubElement(text, tag("a:p"))
            etree.SubElement(etree.SubElement(paragraph, tag("a:pPr")), tag("a:defRPr"))
        insert_label_child(parent, text)
    return text


def transform_chart_labels(xml: str, treatment: dict) -> tuple[str, int]:
    """Apply native label formatting without copying workbook values into text."""
    if not isinstance(treatment, dict):
        raise ValueError("Each chart-label treatment must be an object")
    position, colors = treatment.get("position"), treatment.get("colors")
    if "wrap" in treatment and not isinstance(treatment["wrap"], bool):
        raise ValueError("Chart data-label wrap must be a boolean")
    if position is not None and position not in {"b", "bestFit", "ctr", "inBase", "inEnd", "l", "outEnd", "r", "t"}:
        raise ValueError(f"Invalid native chart data-label position. {position}")
    if colors is not None and (not isinstance(colors, list) or not colors or any(
            not isinstance(color, str) or not re.fullmatch(r"#?[0-9a-fA-F]{6}", color) for color in colors)):
        raise ValueError("Chart data-label colors must be a nonempty list of six-digit RGB colors")
    root = parse_xml(xml)
    labels = root.findall(".//c:dLbls", NS)
    if not labels:
        raise ValueError("Chart-label treatment requires native data labels to be enabled")
    before = etree.tostring(root)
    for group in labels:
        if "wrap" in treatment:
            for parent in [group, *group.findall("c:dLbl", NS)]:
                text = label_text_properties(parent, group.find("c:txPr", NS))
                body = text.find("a:bodyPr", NS)
                if body is None:
                    body = etree.Element(tag("a:bodyPr"))
                    text.insert(0, body)
                body.set("wrap", "square" if treatment["wrap"] else "none")
        if position is not None:
            for parent in [group, *group.findall("c:dLbl", NS)]:
                node = parent.find("c:dLblPos", NS)
                if node is None:
                    node = etree.Element(tag("c:dLblPos"))
                    insert_label_child(parent, node)
                node.set("val", position)
        if colors is None:
            continue
        for index, color in enumerate(colors):
            point = next((label for label in group.findall("c:dLbl", NS)
                          if label.find("c:idx", NS) is not None and
                          label.find("c:idx", NS).get("val") == str(index)), None)
            if point is None:
                point = etree.Element(tag("c:dLbl"))
                etree.SubElement(point, tag("c:idx"), val=str(index))
                insert_label_child(group, point)
            # Office readers differ in how a point treatment inherits label content.
            # Carry the native visibility flags and number format, never a value snapshot.
            for property_name in ("numFmt", "showLegendKey", "showVal", "showCatName", "showSerName",
                                  "showPercent", "showBubbleSize", "separator"):
                inherited = group.find(f"c:{property_name}", NS)
                if inherited is not None and point.find(f"c:{property_name}", NS) is None:
                    insert_label_child(point, copy.deepcopy(inherited))
            if position is not None and point.find("c:dLblPos", NS) is None:
                insert_label_child(point, etree.Element(tag("c:dLblPos"), val=position))
            text = label_text_properties(point, group.find("c:txPr", NS))
            for prop in text.xpath(".//a:defRPr | .//a:rPr | .//a:endParaRPr", namespaces=NS):
                for child in list(prop):
                    if child.tag in {tag(f"a:{name}") for name in
                                     ("noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill")}:
                        prop.remove(child)
                fill = etree.Element(tag("a:solidFill"))
                etree.SubElement(fill, tag("a:srgbClr"), val=color.lstrip("#").upper())
                line = prop.find("a:ln", NS)
                prop.insert(prop.index(line) + 1 if line is not None else 0, fill)
    return etree.tostring(root, encoding="unicode"), int(before != etree.tostring(root))


def postprocess(pptx_path: Path, metadata: dict | None = None) -> dict[str, int | str]:
    pptx_path = pptx_path.resolve()
    metadata = metadata or {}
    facts = {"converted": 0, "textBodiesNormalized": 0, "roundedRectanglesAdjusted": 0,
             "textCharacterSpacingApplied": 0, "chartLabelTreatmentsApplied": 0, "shapeIdsNormalized": 0,
             "arrowheadSizesApplied": 0}
    staged = None
    try:
        with zipfile.ZipFile(pptx_path, "r") as source:
            replacements = {}
            chart_treatments = {}
            for info in source.infolist():
                if not DRAWING_PART_RE.fullmatch(info.filename):
                    continue
                if not SLIDE_RE.fullmatch(info.filename):
                    root = parse_xml(source.read(info.filename).decode("utf-8"))
                    normalized = normalize_shape_ids(root)
                    if normalized:
                        replacements[info.filename] = etree.tostring(root, encoding="utf-8")
                        facts["shapeIdsNormalized"] += normalized
                    continue
                slide_metadata = (metadata.get("slides", {}).get(info.filename, {}) or {})
                rounding = slide_metadata.get("round_rect_adjustments", metadata.get("round_rect_adjustments", {})) or {}
                spacing = slide_metadata.get("text_character_spacing", metadata.get("text_character_spacing", {})) or {}
                updated, local = transform_xml(source.read(info.filename).decode("utf-8"), rounding, spacing,
                                               slide_metadata.get("arrowhead_sizes", {}))
                for key, count in local.items():
                    facts[key] += count
                replacements[info.filename] = updated.encode("utf-8")
                for part, treatment in chart_label_parts(source, info.filename, updated,
                                                         slide_metadata.get("chart_label_treatments", {})).items():
                    if part in chart_treatments and chart_treatments[part] != treatment:
                        raise ValueError(f"Shared chart part has conflicting label treatments. {part}")
                    chart_treatments[part] = treatment
            for part, treatment in chart_treatments.items():
                updated, count = transform_chart_labels(source.read(part).decode("utf-8"), treatment)
                replacements[part] = updated.encode("utf-8")
                facts["chartLabelTreatmentsApplied"] += count
            with tempfile.NamedTemporaryFile(dir=pptx_path.parent, suffix=".pptx", delete=False) as handle:
                staged = Path(handle.name)
            with zipfile.ZipFile(staged, "w", compression=zipfile.ZIP_DEFLATED) as target:
                target.comment = source.comment
                for info in source.infolist():
                    data = replacements[info.filename] if info.filename in replacements else source.read(info.filename)
                    target.writestr(info, data)
        # Close the source archive before the same-filesystem atomic replacement.
        staged.replace(pptx_path)
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)
    return {**facts, "status": "ok"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx")
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text(encoding="utf-8")) if args.metadata else {}
    print(json.dumps(postprocess(Path(args.pptx), metadata), indent=2))


if __name__ == "__main__":
    main()
