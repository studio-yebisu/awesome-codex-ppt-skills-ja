#!/usr/bin/env python3
"""OMML formula injection: replace {{MATH:id}} placeholders in .pptx with native math.

Pipeline:
  1. PptxGenJS writes placeholder text: {{MATH:formula-id}}
  2. This script converts LaTeX→OMML via pandoc, then replaces placeholders
     in the .pptx XML with native PowerPoint math elements.

Usage:
  python inject_omml.py input.pptx formulas.json output.pptx
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from copy import deepcopy
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("ERROR: lxml required. Install: pip install lxml", file=sys.stderr)
    sys.exit(1)

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
}
for prefix, uri in NS.items():
    etree.register_namespace(prefix, uri)

PLACEHOLDER_RE = re.compile(r"\{\{MATH:([a-zA-Z0-9_-]+)\}\}")
A_NS = NS["a"]
A14_NS = NS["a14"]
MC_NS = NS["mc"]


def _check_pandoc() -> bool:
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def latex_to_omml(latex: str) -> etree._Element | None:
    """Convert LaTeX math to OMML via pandoc → docx → extract m:oMathPara/m:oMath."""
    with tempfile.NamedTemporaryFile(suffix=".tex", mode="w", delete=False) as f:
        f.write(f"$${latex}$$\n")
        tex_path = f.name
    docx_path = tex_path.replace(".tex", ".docx")
    try:
        r = subprocess.run(
            ["pandoc", tex_path, "-f", "latex", "-t", "docx", "-o", docx_path],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode != 0:
            print(f"  pandoc error: {r.stderr[:300]}", file=sys.stderr)
            return None
        with zipfile.ZipFile(docx_path, "r") as zf:
            doc_xml = zf.read("word/document.xml")
        tree = etree.fromstring(doc_xml)
        m_ns = NS["m"]
        omaths = tree.findall(f".//{{{m_ns}}}oMathPara")
        if not omaths:
            omaths = tree.findall(f".//{{{m_ns}}}oMath")
        return deepcopy(omaths[0]) if omaths else None
    except Exception as e:
        print(f"  conversion error: {e}", file=sys.stderr)
        return None
    finally:
        Path(tex_path).unlink(missing_ok=True)
        Path(docx_path).unlink(missing_ok=True)


def _merge_paragraph_runs(p_elem):
    """Merge all <a:r> run texts in a paragraph to reconstruct split placeholders.

    PptxGenJS may split {{MATH:id}} across multiple <a:r> elements.
    Returns list of (full_text, [(run_elem, original_text), ...]) per paragraph.
    """
    runs = []
    for child in p_elem:
        tag = child.tag
        if tag == f"{{{A_NS}}}r":
            t_elem = child.find(f"{{{A_NS}}}t")
            text = t_elem.text if t_elem is not None and t_elem.text else ""
            runs.append((child, text))
    full_text = "".join(t for _, t in runs)
    return full_text, runs


def _rebuild_paragraph(p_elem, full_text, runs, omml_cache):
    """Replace placeholders in merged text, rebuild run structure."""
    matches = list(PLACEHOLDER_RE.finditer(full_text))
    if not matches:
        return 0

    # Collect run properties from first run as template
    first_run = runs[0][0] if runs else None
    rpr_template = None
    if first_run is not None:
        rpr_template = first_run.find(f"{{{A_NS}}}rPr")

    # Remove all existing runs from paragraph
    for run, _ in runs:
        p_elem.remove(run)

    # Find insertion point (after pPr if present, else at start)
    insert_idx = 0
    for i, child in enumerate(p_elem):
        if child.tag == f"{{{A_NS}}}pPr":
            insert_idx = i + 1
            break

    replaced = 0
    last_end = 0

    for match in matches:
        fid = match.group(1)

        # Text before this placeholder
        before = full_text[last_end:match.start()]
        if before:
            r_elem = _make_text_run(before, rpr_template)
            p_elem.insert(insert_idx, r_elem)
            insert_idx += 1

        # OMML or fallback text
        if fid in omml_cache:
            a14_m = etree.SubElement(
                p_elem, f"{{{A14_NS}}}m"
            )
            # Insert at correct position
            p_elem.remove(a14_m)
            a14_m = etree.Element(f"{{{A14_NS}}}m")
            a14_m.append(deepcopy(omml_cache[fid]))
            p_elem.insert(insert_idx, a14_m)
            insert_idx += 1
            replaced += 1
        else:
            # Keep placeholder as text (conversion failed)
            r_elem = _make_text_run(match.group(0), rpr_template)
            p_elem.insert(insert_idx, r_elem)
            insert_idx += 1

        last_end = match.end()

    # Text after last placeholder
    after = full_text[last_end:]
    if after:
        r_elem = _make_text_run(after, rpr_template)
        p_elem.insert(insert_idx, r_elem)

    return replaced


def _make_text_run(text, rpr_template=None):
    """Create an <a:r> element with optional run properties."""
    r = etree.Element(f"{{{A_NS}}}r")
    if rpr_template is not None:
        r.append(deepcopy(rpr_template))
    t = etree.SubElement(r, f"{{{A_NS}}}t")
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return r


def _ensure_namespaces(tree):
    """Ensure root element declares mc: and a14: namespaces."""
    root = tree
    nsmap = root.nsmap if hasattr(root, "nsmap") else {}
    need_rebuild = False
    new_nsmap = dict(nsmap)
    if "mc" not in nsmap and MC_NS not in nsmap.values():
        new_nsmap["mc"] = MC_NS
        need_rebuild = True
    if "a14" not in nsmap and A14_NS not in nsmap.values():
        new_nsmap["a14"] = A14_NS
        need_rebuild = True
    if need_rebuild:
        # lxml doesn't allow modifying nsmap after creation;
        # re-serialize and re-parse with updated namespaces
        xml_str = etree.tostring(tree, encoding="unicode")
        ns_decls = ""
        if "mc" not in nsmap:
            ns_decls += f' xmlns:mc="{MC_NS}"'
        if "a14" not in nsmap:
            ns_decls += f' xmlns:a14="{A14_NS}"'
        # Insert namespace declarations into root element
        root_tag_end = xml_str.index(">")
        # Check for self-closing or not
        if xml_str[root_tag_end - 1] == "/":
            insert_pos = root_tag_end - 1
        else:
            insert_pos = root_tag_end
        xml_str = xml_str[:insert_pos] + ns_decls + xml_str[insert_pos:]
        return etree.fromstring(xml_str.encode("utf-8"))
    return tree


def inject_omml_into_pptx(pptx_path: str, formulas: dict, output_path: str) -> dict:
    """Replace {{MATH:id}} placeholders with OMML math. Returns stats dict."""
    if os.path.abspath(pptx_path) != os.path.abspath(output_path):
        shutil.copy2(pptx_path, output_path)

    # Filter to omml-eligible formulas
    omml_formulas = {}
    for fid, fdata in formulas.items():
        render = fdata.get("render", "auto")
        mode = fdata.get("mode", "display")
        if render == "auto":
            render = "image" if mode == "paragraph" else "omml"
        if render == "omml" and fdata.get("latex"):
            omml_formulas[fid] = fdata

    if not omml_formulas:
        return {"success": 0, "failed": 0, "skipped": len(formulas)}

    # Convert all OMML formulas
    omml_cache = {}
    failed_ids = []
    for fid, fdata in omml_formulas.items():
        omml = latex_to_omml(fdata["latex"])
        if omml is not None:
            omml_cache[fid] = omml
            print(f"  Converted {fid}")
        else:
            failed_ids.append(fid)
            print(f"  FAILED {fid}", file=sys.stderr)

    # Process pptx slides
    with zipfile.ZipFile(output_path, "r") as zin:
        all_files = {}
        for name in zin.namelist():
            all_files[name] = zin.read(name)

    slide_files = [n for n in all_files if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
    total_replaced = 0

    for slide_file in slide_files:
        xml_bytes = all_files[slide_file]
        if b"{{MATH:" not in xml_bytes:
            continue

        tree = etree.fromstring(xml_bytes)

        # Process all paragraphs
        for p_elem in tree.iter(f"{{{A_NS}}}p"):
            full_text, runs = _merge_paragraph_runs(p_elem)
            if "{{MATH:" not in full_text:
                continue
            count = _rebuild_paragraph(p_elem, full_text, runs, omml_cache)
            if count > 0:
                total_replaced += count
                print(f"  Injected {count} formula(s) in {slide_file}")

        # Ensure namespaces
        tree = _ensure_namespaces(tree)
        all_files[slide_file] = etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)

    # Rewrite zip
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in all_files.items():
            zout.writestr(name, data)

    stats = {
        "success": total_replaced,
        "failed": len(failed_ids),
        "skipped": len(formulas) - len(omml_formulas),
        "failed_ids": failed_ids,
    }
    print(f"\nDone: {stats['success']} injected, {stats['failed']} failed, {stats['skipped']} skipped (image) → {output_path}")
    return stats


def main():
    if len(sys.argv) < 4:
        print("Usage: python inject_omml.py input.pptx formulas.json output.pptx")
        sys.exit(1)

    if not _check_pandoc():
        print("ERROR: pandoc not found. Install: brew install pandoc", file=sys.stderr)
        sys.exit(1)

    pptx_path, formulas_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(formulas_path) as f:
        formulas_list = json.load(f)
    formulas = {item["id"]: item for item in formulas_list}

    stats = inject_omml_into_pptx(pptx_path, formulas, output_path)

    if stats["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
