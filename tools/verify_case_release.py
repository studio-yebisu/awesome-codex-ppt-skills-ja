"""Independent, read-only release verification. No browser automation or artistic grading."""
from pathlib import Path,PurePosixPath
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
import hashlib,json,re,struct,subprocess,sys,tempfile,zipfile,xml.etree.ElementTree as ET,zlib

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/".build/actual-upstreams"
ERRORS=[];PASSED=[]
EXPECTED={"cafe-pptx":8,"ec-monthly":7,"cafe-web":8,"git-onboarding":7,"port-town":7,"knowledge-search":8}
FORKS={"ppt-master-ja":"hugohe3/ppt-master","frontend-slides-ja":"zarazhangrui/frontend-slides","guizang-ppt-skill-ja":"op7418/guizang-ppt-skill"}
NS={"p":"http://schemas.openxmlformats.org/presentationml/2006/main","a":"http://schemas.openxmlformats.org/drawingml/2006/main"}
def read(p):return Path(p).read_text(encoding="utf-8-sig")
def load(p):return json.loads(read(p))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise AssertionError(message)
def run(label,fn):
    try:fn();PASSED.append(label)
    except Exception as e:ERRORS.append({"check":label,"error":str(e)})
def inside(base,relative):
    require(isinstance(relative,str) and relative and "\\" not in relative,"Invalid relative path: "+str(relative))
    url=urlsplit(relative)
    require(not url.scheme and not url.netloc and not relative.startswith("/"),"Nonlocal path: "+relative)
    part=unquote(url.path)
    require(".." not in PurePosixPath(part).parts and ":" not in part,"Unsafe path: "+relative)
    p=(base/part).resolve()
    require(p.is_relative_to(base.resolve()),"Escaping path: "+relative)
    return p
def required_path(base,relative):
    p=inside(base,relative);require(p.is_file(),"Missing file: "+str(p));return p
def files(folder):
    return {p.relative_to(folder).as_posix():p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc"}
def canonical_hash(d):
    return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def close(a,b,label):require(abs(a-b)<1e-7,label+": "+str(a)+" != "+str(b))

class Links(HTMLParser):
    def __init__(self):super().__init__();self.paths=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        for key in ("href","src"):
            if key in attrs:self.paths.append(attrs[key])

def png(path,expected=None):
    raw=path.read_bytes()
    require(raw[:8]==b"\x89PNG\r\n\x1a\n","Not genuine PNG: "+str(path))
    width,height=struct.unpack(">II",raw[16:24])
    require(width>0 and height>0,"Invalid PNG dimensions")
    if expected:require((width,height)==expected,"PNG dimensions: "+str((width,height)))
    else:require(abs(width/height-16/9)<.025,"Not 16:9: "+str(path))
    pos=8;compressed=bytearray();ended=False
    while pos+12<=len(raw):
        length=struct.unpack(">I",raw[pos:pos+4])[0];kind=raw[pos+4:pos+8];body=raw[pos+8:pos+8+length]
        require(pos+12+length<=len(raw),"Truncated PNG")
        crc=struct.unpack(">I",raw[pos+8+length:pos+12+length])[0]
        require(zlib.crc32(kind+body)&0xffffffff==crc,"PNG CRC mismatch")
        if kind==b"IDAT":compressed.extend(body)
        pos+=12+length
        if kind==b"IEND":ended=True;break
    require(ended and compressed,"PNG missing IDAT/IEND")
    require(bool(zlib.decompress(compressed)),"PNG pixels empty")

def catalog_check():
    current=load(ROOT/"data/skills.json")
    old=json.loads(subprocess.check_output(["git","show","03a2cb0:data/skills.json"],cwd=ROOT))
    require(current==old,"Original catalog changed from 03a2cb0")
    require(len(current["skills"])==209 and len(current["kinds"])==6,"Catalog cardinality")
    require(len({r["repo_full_name"] for r in current["skills"]})==209,"Duplicate catalog repository")
    projects=load(ROOT/"data/project-workflows.json")["projects"]
    require(len(projects)==209,"Workflow count")
    for source,record in zip(current["skills"],projects):
        require(record["original_project"]==source,"Original project fields/order changed")
        expected=[e for e in CASES if e["repository"]==source["repo_full_name"]]
        require([e["id"] for e in record["examples"]]==[e["id"] for e in expected],"Workflow cases mismatch")
        if not expected:require(record["generation_status"]=="not_generated_here","Unexecuted repository marked generated")
    require(sum(len(p["examples"]) for p in projects)==6,"Canonical case count includes history")
def manifest_check():
    require({r["id"]:r["page_count"] for r in CASES}==EXPECTED,"Manifest cases/pages differ")
    require(sum(r["page_count"] for r in CASES)==45,"Slide total")
    require(len({r["id"] for r in CASES})==6,"Duplicate case")
    for row in CASES:
        require(row["repository"]==row["skill_repository"]==FORKS[row["fork_id"]],"Repository/fork mismatch")
        require(row["upstream_commit"]==PINS[row["repository"]]["commit"],"Case commit mismatch")
        for key in ("cover","interior","preview","artifact_download","source_download","input","input_data","prompt","provenance","qa","fork_download","guide"):
            required_path(ROOT,row[key])
        require(read(ROOT/row["prompt"])==row["prompt_text"],"Prompt text mismatch")
        require(len(row["titles"])==len(row["notes"])==row["page_count"],"Titles/notes count mismatch")
        require(canonical_hash(load(ROOT/row["input_data"]))==row["input_sha256"],"Input hash mismatch")
        if row["id"] in ("cafe-pptx","cafe-web"):
            other=next(r for r in CASES if r["id"]==row["compare_id"])
            require(other["compare_id"]==row["id"] and other["input_sha256"]==row["input_sha256"],"Cafe comparison mismatch")
def calculations():
    d=load(ROOT/"data/case-inputs.json");c=d["cafe"];ec=d["ec"]
    actual=load(ROOT/"examples/cases/cafe-pptx/calculations.json")
    revenue=c["daily_customers"]*c["ticket_yen"]*c["business_days"]/10000
    fixed=sum(c["fixed_cost_man_yen"].values());variable=revenue*c["variable_cost_ratio"]
    close(revenue,234.52,"Revenue");close(variable,82.082,"Variable cost");close(revenue-variable-fixed,42.438,"Profit")
    values={"revenue_man_yen":revenue,"variable_cost_man_yen":variable,"fixed_cost_man_yen":fixed,"profit_man_yen":revenue-variable-fixed,"break_even_man_yen":fixed/(1-c["variable_cost_ratio"]),"break_even_daily_customers":fixed/(1-c["variable_cost_ratio"])*10000/c["ticket_yen"]/c["business_days"]}
    for k,v in values.items():close(actual[k],v,k)
    require(actual["site_scores"]==[sum(w*s/c["score_scale"] for w,s in zip(c["weights"],site["scores"])) for site in c["sites"]],"Candidate scores")
    close(sum(x["sales_man_yen"] for x in ec["channels"]),ec["sales_man_yen"],"Channel total")
    close(sum(x["previous_man_yen"] for x in ec["channels"]),ec["previous_sales_man_yen"],"Prior channel total")
    for cid,key in [("cafe-pptx","cafe"),("cafe-web","cafe"),("ec-monthly","ec"),("git-onboarding","git"),("port-town","harbor"),("knowledge-search","knowledge")]:
        require(load(ROOT/"examples/cases"/cid/"input/data.json")==d[key],"Input differs: "+cid)
def qa_check(row):
    qa=load(ROOT/row["qa"])
    require(qa.get("status") in ("passed","verified","qa_complete","verified_local","complete"),"QA not complete: "+str(qa.get("status")))
    require(len(qa)>1,"QA has no evidence")
    for key in ("browser_review","visual_review"):
        if key in qa and isinstance(qa[key],str):
            require(qa[key] not in ("pending","failed","blocked","not_run"),key+" incomplete")
def images(row):
    folder=ROOT/"examples/cases"/row["id"]/"render"
    paths=[folder/("slide-%02d.png"%i) for i in range(1,row["page_count"]+1)]
    for p in paths:png(p,(1600,900) if row["format"]=="pptx" else None)
    require(len({sha(p) for p in paths})==len(paths),"Duplicate rendered slides: "+row["id"])
    require(len(list(folder.glob("slide-*.png")))==row["page_count"],"Extra/missing rendered pages")
def provenance(row):
    prov=load(ROOT/row["provenance"]);repo=row["repository"]
    require(prov["repository"]==repo and prov["upstream_commit"]==row["upstream_commit"],"Provenance pin mismatch")
    require(prov["input_sha256"]==row["input_sha256"],"Provenance input mismatch")
    require(len(prov["upstream_files"])>=2,"Missing upstream evidence")
    for f in prov["upstream_files"]:require(sha(required_path(UP/repo.replace("/","__"),f["path"]))==f["sha256"],"Upstream hash: "+f["path"])
    folder=ROOT/"examples/cases"/row["id"]
    require(sha(folder/"LICENSE")==sha(ROOT/"skill-forks"/row["fork_id"]/"LICENSE"),"Case license differs")
    originals=list((ROOT/"assets/fonts").rglob("*OFL.txt"))
    for p in originals:require(sha(folder/"licenses/fonts"/p.name)==sha(p),"Font notice differs: "+p.name)
def pptx(row):
    p=ROOT/row["artifact_download"];n=row["page_count"]
    with zipfile.ZipFile(p) as z:
        require(z.testzip() is None,"PPTX CRC")
        slides=[f for f in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml",f)]
        notes=[f for f in z.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml",f)]
        require(len(slides)==len(notes)==n,"PPTX slides/notes")
        for s in slides:
            raw=z.read(s);doc=ET.fromstring(raw)
            require(len(doc.findall(".//p:sp",NS))>1 and len(doc.findall(".//a:t",NS))>1,"Missing native text/shapes: "+s)
            require(not doc.findall(".//p:pic",NS),"Unexpected raster picture in native case: "+s)
            require(b'ja-JP' in raw,"Missing ja-JP: "+s)
        require(all(ET.fromstring(z.read(s)).findall(".//a:t",NS) for s in notes),"Empty notes")
    folder=ROOT/"examples/cases"/row["id"]
    report=load(folder/"render/powerpoint-render.json")
    require(report["application"]=="Microsoft PowerPoint" and report["slide_count"]==n,"PowerPoint report mismatch")
    require(report["source_sha256"].lower()==sha(p),"PPTX changed since PowerPoint render")
    require(len(report["slides"])==n,"Report slide count")
    require([r["page"] for r in report["slides"]]==list(range(1,n+1)),"Report page ordering")
    require((ROOT/row["pdf_download"]).read_bytes().startswith(b"%PDF-"),"PDF signature")
    require(row["pages"]==["examples/cases/"+row["id"]+"/render/slide-%02d.png"%i for i in range(1,n+1)],"PPTX preview pages")
def javascript_check(doc):
    for i,script in enumerate(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>",doc,re.S)):
        with tempfile.NamedTemporaryFile(suffix=".mjs",mode="w",encoding="utf-8",delete=False) as f:f.write(script);name=f.name
        try:
            r=subprocess.run(["node","--check",name],capture_output=True,text=True)
            require(r.returncode==0,"Inline JS "+str(i)+": "+r.stderr)
        finally:Path(name).unlink(missing_ok=True)
def html_case(row):
    p=ROOT/row["preview"];doc=read(p);folder=p.parent
    require(len(re.findall(r'<section class="slide(?: |")',doc))==row["page_count"],"HTML section count")
    require('<html lang="ja"' in doc,"HTML language")
    require(not re.search(r'<link[^>]*(fonts\.googleapis|api\.fontshare|fonts\.gstatic)',doc),"Remote font link")
    require("data:font/" in doc and "Noto Sans JP" in doc,"Missing embedded Japanese font")
    require("yebisu-slide" in doc and "yebisu-page" in doc,"Missing parent synchronization")
    require("e.source!==parent" in doc and "e.origin!==location.origin" in doc,"Message origin/source guards missing")
    parser=Links();parser.feed(doc)
    for link in parser.paths:
        url=urlsplit(link)
        if not url.scheme and not url.netloc and url.path:required_path(folder,link.removeprefix("./"))
    if row["fork_id"]=="frontend-slides-ja":
        original=UP/"zarazhangrui__frontend-slides"
        require(read(original/"viewport-base.css").replace("\r\n","\n") in doc.replace("\r\n","\n"),"Original viewport CSS missing")
        require("class SlidePresentation" in doc and "setupStageScale()" in doc and "1920" in doc and "1080" in doc,"Original stage controller missing")
        require("localStorage" in doc and "editToggle" in doc,"Editing contract missing")
        require(":root[data-upstream=frontend]{" in doc,"Global frontend color override")
        require(("terminal" in doc and "JetBrains Mono" in doc) if row["id"]=="git-onboarding" else ("Archivo Black" in doc and "Space Grotesk" in doc),"Preset fonts missing")
    else:
        require("function go(n,opts={})" in doc and "SPEAKER_NOTES" in doc and "__playSlide" in doc,"Original Guizang runtime missing")
        for i in range(1,row["page_count"]+1):require('data-slide-id="page-'+str(i)+'"' in doc,"Guizang slide ID missing")
        require("lucide@latest" not in doc,"Unpinned Lucide")
        for f in ("motion.min.js","lucide.min.js","motion-LICENSE.txt","lucide-LICENSE.txt"):required_path(folder,"assets/"+f)
        if row["id"]=="knowledge-search":require('data-layout="' in doc,"Swiss layout identity absent")
    javascript_check(doc)
def zip_check(path,folder):
    expected=files(folder)
    with zipfile.ZipFile(path) as z:
        require(z.testzip() is None,"ZIP CRC failure")
        members=[i for i in z.infolist() if not i.is_dir()]
        require(len({i.filename for i in members})==len(members),"Duplicate ZIP entry")
        normalized={}
        for item in members:
            name=item.filename;parts=PurePosixPath(name).parts
            require(not name.startswith(("/","\\")) and "\\" not in name and ".." not in parts and ":" not in name,"Unsafe ZIP path: "+name)
            require("__pycache__" not in parts and "node_modules" not in parts and not name.endswith(".pyc"),"Cache in ZIP")
            require((item.external_attr>>16)&0o170000!=0o120000,"Symlink in ZIP")
            relative=name[len(folder.name)+1:] if name.startswith(folder.name+"/") else name
            require(relative not in normalized,"Ambiguous ZIP roots")
            normalized[relative]=item
        require(set(normalized)==set(expected),"ZIP/file set mismatch: missing="+str(sorted(set(expected)-set(normalized))[:8])+" extra="+str(sorted(set(normalized)-set(expected))[:8]))
        for name,p in expected.items():require(hashlib.sha256(z.read(normalized[name])).hexdigest()==sha(p),"ZIP stale: "+name)
def fork_check(fork,repo):
    folder=ROOT/"skill-forks"/fork;source=load(folder/"SOURCE.json")
    require(source["repository"]==repo and source["commit"]==PINS[repo]["commit"],"Fork pin mismatch")
    actual=files(folder);actual.pop("SOURCE.json",None)
    listed={f["path"]:f["sha256"] for f in source["files"]}
    require(len(listed)==len(source["files"]),"Duplicate SOURCE entries")
    require(set(listed)==set(actual),"SOURCE inventory differs")
    for p,h in listed.items():require(sha(required_path(folder,p))==h,"SOURCE stale: "+p)
    required_path(folder,"references/japanese-business-workflow.md")
    require("references/japanese-business-workflow.md" in read(folder/"SKILL.md"),"Japanese workflow unreachable")
    require(sha(folder/"LICENSE")==sha(UP/repo.replace("/","__")/"LICENSE"),"Upstream license differs")
    upstream_entry=UP/repo.replace("/","__")/("skills/ppt-master/SKILL.md" if fork=="ppt-master-ja" else "SKILL.md")
    require(sha(folder/"SKILL.upstream.md")==sha(upstream_entry),"Archived original SKILL changed")
    zip_check(ROOT/"downloads"/(fork+".zip"),folder)
def guard_check():
    folder=ROOT/"skill-forks/ppt-master-ja";entry=read(folder/"SKILL.md")
    for value in ['copyright: "Copyright (c) 2025-2026 Hugo He"','license: "MIT"','official_repository: "https://github.com/hugohe3/ppt-master"','- "SPONSORS.md"','- "SPONSORS_CN.md"']:
        require(value in entry,"Protected metadata missing: "+value)
    require('python3 "'+chr(36)+'{SKILL_DIR}/scripts/attribution_guard.py"' in entry,"Guard invocation changed")
    upstream=UP/"hugohe3__ppt-master/skills/ppt-master"
    for rel in ("scripts/attribution_guard.py","scripts/svg_quality_checker.py","scripts/svg_to_pptx.py","SPONSORS.md","SPONSORS_CN.md"):
        require(sha(folder/rel)==sha(upstream/rel),"Protected original changed: "+rel)
    r=subprocess.run([sys.executable,str(folder/"scripts/attribution_guard.py")],capture_output=True,text=True,cwd=ROOT)
    require(r.returncode==0,r.stdout+r.stderr)
def download_check():
    rows=load(ROOT/"data/case-downloads.json")
    if isinstance(rows,dict):rows=rows["artifacts"]
    require(len({r["file"] for r in rows})==len(rows),"Duplicate download records")
    wanted={"downloads/"+f+".zip" for f in FORKS}|{"downloads/"+cid+"-ja.zip" for cid in EXPECTED}
    require(wanted.issubset({r["file"] for r in rows}),"Missing nine canonical ZIP records")
    for row in rows:
        p=required_path(ROOT,row["file"])
        require(sha(p)==row["sha256"] and p.stat().st_size==row["bytes"],"Download hash/size: "+row["file"])
def main():
    global CASES,PINS
    CASES=load(ROOT/"data/case-studies.json")
    PINS={r["repository"]:r for r in load(ROOT/"data/upstreams.json")}
    run("catalog and workflow preservation",catalog_check)
    run("manifest and links",manifest_check)
    run("inputs and numerical consistency",calculations)
    for row in CASES:
        cid=row["id"]
        for title,fn in (("QA",qa_check),("PNG structure and uniqueness",images),("provenance and notices",provenance),("PPTX" if row["format"]=="pptx" else "HTML and JS",pptx if row["format"]=="pptx" else html_case)):
            run(cid+" / "+title,lambda fn=fn,row=row:fn(row))
        run(cid+" / case ZIP",lambda row=row:zip_check(ROOT/row["source_download"],ROOT/"examples/cases"/row["id"]))
    for fork,repo in FORKS.items():run(fork+" / SOURCE and ZIP",lambda fork=fork,repo=repo:fork_check(fork,repo))
    run("protected upstream attribution",guard_check)
    run("download registry",download_check)
    report=dict(passed=not ERRORS,checks_passed=len(PASSED),checks_failed=len(ERRORS),catalog=209,cases=6,slides=45,limitations="Static verification does not certify aesthetics, human adoption, or browser behavior beyond recorded QA.",successful_checks=PASSED,failures=ERRORS)
    out=ROOT/".build/case-release-check.json";out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if ERRORS else 0
if __name__=="__main__":sys.exit(main())
