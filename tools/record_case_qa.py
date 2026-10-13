"""Record the performed checks on actual local case studies."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/"data/case-studies.json").read_text(encoding="utf-8"))
dom=json.loads((ROOT/".build/case-qa/web-dom-checks.json").read_text(encoding="utf-8"))
offline=json.loads((ROOT/".build/case-qa/offline-proof.json").read_text(encoding="utf-8"))
editor=json.loads((ROOT/".build/case-qa/editor-proof.json").read_text(encoding="utf-8"))
site=json.loads((ROOT/".build/case-qa/site-checks.json").read_text(encoding="utf-8"))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for c in cases:
    folder=ROOT/"examples/cases"/c["id"]
    report=dict(status="verified_local",checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),page_count=c["page_count"],artifact_sha256=sha(folder/("deck.pptx" if c["format"]=="pptx" else "index.html")),visual_review="all_pages_reviewed_by_agent",human_adoption="not_requested",site_checks=site,images=[dict(page=i,file="render/slide-"+str(i).zfill(2)+".png",sha256=sha(folder/"render"/("slide-"+str(i).zfill(2)+".png"))) for i in range(1,c["page_count"]+1)])
    if c["format"]=="pptx":
        pp=json.loads((folder/"render/powerpoint-render.json").read_text(encoding="utf-8-sig"))
        assert pp["source_sha256"]==report["artifact_sha256"]
        report.update(powerpoint_application=pp["application"],powerpoint_version=pp["version"],powerpoint_render="render/powerpoint-render.json",pdf="render/deck.pdf",preview_method="PNG exported from completed PPTX, not input SVG")
        report["converter_warning_note"]="Noto Sans JP is outside the compiler PPT-safe font list. Actual PowerPoint output was reviewed with installed Noto Sans JP. Font is not embedded; recipient needs it."
    else:
        pages=next(e for e in dom if e["id"]==c["id"])["pages"]
        assert len(pages)==c["page_count"] and all(not p.get("clipped") and not p.get("error") for p in pages)
        report.update(html_sha256=sha(folder/"index.html"),browser_review="passed",viewport={"width":1280,"height":720},render_motion="reduced for stable page images; normal motion separately loaded",page_checks=pages,offline_check=next(e for e in offline["cases"] if e["id"]==c["id"]))
        if c["fork_id"]=="frontend-slides-ja":report["editor_check"]={k:v for k,v in editor.items() if k!="path"}
    (folder/"QA.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print("6 QA records with artifact and image hashes")
