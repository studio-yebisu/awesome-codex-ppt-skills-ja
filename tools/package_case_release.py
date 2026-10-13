"""Refresh actual fork hashes/packages while preserving the maintained Japanese edits."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cases=json.loads((ROOT/"data/case-studies.json").read_text(encoding="utf-8"))
pins=json.loads((ROOT/"data/upstreams.json").read_text(encoding="utf-8"))
records=[]
for name in ["ppt-master-ja","frontend-slides-ja","guizang-ppt-skill-ja"]:
    folder=ROOT/"skill-forks"/name
    for f in (ROOT/"assets/fonts").glob("*"):
        if f.is_file():shutil.copy2(f,folder/"references/fonts"/f.name)
    source=json.loads((folder/"SOURCE.json").read_text(encoding="utf-8"))
    source["scope"]="original implementation, maintained Japanese business workflow, local case studies"
    source["case_studies"]=[c["id"] for c in cases if c["fork_id"]==name]
    source["files"]=[dict(path=f.relative_to(folder).as_posix(),sha256=sha(f)) for f in sorted(folder.rglob("*")) if f.is_file() and f.name!="SOURCE.json" and "__pycache__" not in f.parts and f.suffix!=".pyc"]
    (folder/"SOURCE.json").write_text(json.dumps(source,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    target=ROOT/"downloads"/(name+".zip")
    with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as z:
        for f in sorted(folder.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.suffix!=".pyc":z.write(f,(Path(name)/f.relative_to(folder)).as_posix())
    records.append(dict(file=target.relative_to(ROOT).as_posix(),sha256=sha(target),bytes=target.stat().st_size,type="skill-source"))
    for pin in pins:
        if pin["repository"]==source["repository"]:pin["generated_case_ids"]=source["case_studies"]
for c in cases:
    for key in ["artifact_download","source_download","pdf_download"]:
        value=c.get(key)
        if value and not any(r["file"]==value for r in records):
            path=ROOT/value
            records.append(dict(file=value,sha256=sha(path),bytes=path.stat().st_size,type=key))
(ROOT/"data/case-downloads.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
(ROOT/"data/upstreams.json").write_text(json.dumps(pins,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print("3 maintained forks, "+str(len(records))+" downloadable artifacts, updated source hashes")
