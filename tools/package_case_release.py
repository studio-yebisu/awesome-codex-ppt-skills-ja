"""Refresh actual fork hashes/packages while preserving the maintained Japanese edits."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cases=json.loads((ROOT/"data/case-studies.json").read_text(encoding="utf-8"))
pins=json.loads((ROOT/"data/upstreams.json").read_text(encoding="utf-8"))
records=[]
fork_names=sorted({c["fork_id"] for c in cases if c.get("fork_id")})
for name in fork_names:
    folder=ROOT/"skill-forks"/name
    source=json.loads((folder/"SOURCE.json").read_text(encoding="utf-8"))
    case_ids=[c["id"] for c in cases if c.get("fork_id")==name]
    source["case_studies"]=case_ids
    source["files"]=[dict(path=f.relative_to(folder).as_posix(),sha256=sha(f)) for f in sorted(folder.rglob("*")) if f.is_file() and f.name!="SOURCE.json" and "__pycache__" not in f.parts and f.suffix!=".pyc"]
    (folder/"SOURCE.json").write_text(json.dumps(source,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    target=ROOT/"downloads"/(name+".zip")
    with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as z:
        for f in sorted(folder.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.suffix!=".pyc":
                info=zipfile.ZipInfo((Path(name)/f.relative_to(folder)).as_posix())
                info.external_attr=0o100644<<16
                z.writestr(info,f.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
    records.append(dict(file=target.relative_to(ROOT).as_posix(),sha256=sha(target),bytes=target.stat().st_size,type="skill-source"))
    for pin in pins:
        if pin["repository"]==source["repository"]:pin["generated_case_ids"]=case_ids
for c in cases:
    for key in ["artifact_download","source_download","pdf_download","pptx_download"]:
        value=c.get(key)
        if value and not any(r["file"]==value for r in records):
            path=ROOT/value
            records.append(dict(file=value,sha256=sha(path),bytes=path.stat().st_size,type=key))
(ROOT/"data/case-downloads.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
(ROOT/"data/upstreams.json").write_text(json.dumps(pins,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(str(len(fork_names))+" maintained forks, "+str(len(records))+" downloadable artifacts, updated source hashes")
