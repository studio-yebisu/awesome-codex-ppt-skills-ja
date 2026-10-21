#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import zipfile
from html import escape
from pathlib import Path


REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NOTES_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"
MASTER_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster"
SLIDE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
NOTES_CT = "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"


def notes_xml(text: str) -> str:
    safe = escape(text or "", quote=False)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Notes Placeholder 2"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="4400550"/><a:ext cx="5486400" cy="3600450"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p><a:r><a:rPr lang="zh-CN" sz="1200"/><a:t>{safe}</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:notes>
'''


def rels_xml(slide_idx: int) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  <Relationship Id="rId1" Type="{MASTER_REL}" Target="../notesMasters/notesMaster1.xml"/>
  <Relationship Id="rId2" Type="{SLIDE_REL}" Target="../slides/slide{slide_idx}.xml"/>
</Relationships>
'''


def ensure_notes_relation(rels_text: str, slide_idx: int) -> str:
    target = f"../notesSlides/notesSlide{slide_idx}.xml"
    if target in rels_text and NOTES_REL in rels_text:
        return rels_text
    insert = f'<Relationship Id="rIdNotes{slide_idx}" Type="{NOTES_REL}" Target="{target}"/>'
    if "</Relationships>" in rels_text:
        return rels_text.replace("</Relationships>", insert + "</Relationships>")
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL_NS}">{insert}</Relationships>'


def ensure_content_types(content: str, count: int) -> str:
    additions = []
    for idx in range(1, count + 1):
        part = f"/ppt/notesSlides/notesSlide{idx}.xml"
        if part not in content:
            additions.append(f'<Override PartName="{part}" ContentType="{NOTES_CT}"/>')
    if additions and "</Types>" in content:
        content = content.replace("</Types>", "".join(additions) + "</Types>")
    return content


def embed_notes(pptx: Path, notes_manifest: Path, output: Path) -> int:
    data = json.loads(notes_manifest.read_text(encoding="utf-8-sig"))
    notes = [s.get("notes") or s.get("speaker_notes") or "" for s in data.get("slides", [])]
    with zipfile.ZipFile(pptx) as zin:
        names = zin.namelist()
        slide_count = len([n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")])
        count = min(slide_count, len(notes))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
            tmp_path = Path(tmp.name)
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "[Content_Types].xml":
                    content = zin.read(item.filename).decode("utf-8")
                    zout.writestr(item, ensure_content_types(content, count))
                    continue
                if item.filename.startswith("ppt/notesSlides/notesSlide") or item.filename.startswith("ppt/notesSlides/_rels/notesSlide"):
                    continue
                if item.filename.startswith("ppt/slides/_rels/slide") and item.filename.endswith(".xml.rels"):
                    try:
                        idx = int(item.filename.rsplit("slide", 1)[1].split(".xml", 1)[0])
                    except Exception:
                        zout.writestr(item, zin.read(item.filename))
                        continue
                    text = zin.read(item.filename).decode("utf-8")
                    if idx <= count:
                        text = ensure_notes_relation(text, idx)
                    zout.writestr(item, text)
                    continue
                zout.writestr(item, zin.read(item.filename))
            zout.writestr("ppt/notesSlides/", b"")
            zout.writestr("ppt/notesSlides/_rels/", b"")
            for idx in range(1, count + 1):
                zout.writestr(f"ppt/notesSlides/notesSlide{idx}.xml", notes_xml(notes[idx - 1]))
                zout.writestr(f"ppt/notesSlides/_rels/notesSlide{idx}.xml.rels", rels_xml(idx))
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(tmp_path), output)
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pptx", type=Path, required=True)
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = {"input": str(args.pptx), "notes": str(args.notes), "output": str(args.output), "embedded": False, "warnings": [], "errors": []}
    if not args.pptx.exists():
        report["errors"].append("PPTX not found.")
    if not args.notes.exists():
        report["errors"].append("notes_manifest.json not found.")
    if not report["errors"]:
        count = embed_notes(args.pptx, args.notes, args.output)
        report["embedded"] = True
        report["notes_count"] = count
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
