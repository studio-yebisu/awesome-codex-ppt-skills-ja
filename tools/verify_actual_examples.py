"""Check repository correspondence, authentic source paths, text and native output."""
from pathlib import Path
from html.parser import HTMLParser
from hashlib import sha256
from urllib.parse import urlsplit, unquote
from fontTools.ttLib import TTFont
import json, re, subprocess, zipfile, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/skills.json').read_text(encoding='utf-8'))
projects=json.loads((ROOT/'data/project-workflows.json').read_text(encoding='utf-8'))['projects']
examples=json.loads((ROOT/'data/actual-examples.json').read_text(encoding='utf-8'))
assert len(projects)==209 and len({p['repository'] for p in projects})==209
assert {p['repository']:p['original_project'] for p in projects}=={p['repo_full_name']:p for p in catalog['skills']},'Original 209 identity or fields changed'
assert len(examples)==3 and sum(e['slide_count'] for e in examples)==12
assert all(len(p['examples'])==(1 if p['repository'] in {e['repository'] for e in examples} else 0) for p in projects)

class Document(HTMLParser):
    def __init__(self):super().__init__();self.targets=[];self.text=[];self.skip=0;self.title='';self.in_title=False;self.scripts=[];self.script=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ['script','style']:self.skip+=1
        if tag=='script' and 'src' not in a and a.get('type','') not in ['application/json','text/plain']:self.script=[]
        if tag=='title':self.in_title=True
        for k in ['href','src']:
            if k in a:self.targets.append(a[k])
    def handle_endtag(self,tag):
        if tag=='script' and self.script is not None:self.scripts.append(''.join(self.script));self.script=None
        if tag in ['script','style']:self.skip-=1
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.script is not None:self.script.append(data)
        if not self.skip:self.text.append(data)

required_chars=set()
js_dir=ROOT/'.build/actual-js-check';js_dir.mkdir(parents=True,exist_ok=True)
html_files=[ROOT/'index.html',ROOT/'guide.html',ROOT/'licenses.html']
for e in examples:
    for key in ['cover','html','proof','download','fork_download']:assert (ROOT/e[key]).is_file(),(e['repository'],key)
    assert len(e['titles'])==len(e['notes'])==e['slide_count']
    folder=(ROOT/e['html']).parent
    proof=json.loads((folder/'PROVENANCE.json').read_text(encoding='utf-8'))
    assert proof['repository']==e['repository'] and proof['commit']==e['commit']
    for f in proof['used_files']:
        p=ROOT/'.build/actual-upstreams'/e['repository'].replace('/','__')/f['path']
        assert sha256(p.read_bytes()).hexdigest()==f['sha256'],p
    assert (folder/'LICENSE').is_file()
    html_files.extend([ROOT/e['html'],ROOT/e['proof']])
    if e['repository']=='zarazhangrui/frontend-slides':
        base=(ROOT/'skill-forks/frontend-slides-ja/viewport-base.css').read_text(encoding='utf-8')
        assert base in (ROOT/e['html']).read_text(encoding='utf-8'),'Upstream fixed-stage CSS was replaced'
    if e['repository']=='op7418/guizang-ppt-skill':
        raw=(ROOT/e['html']).read_text(encoding='utf-8')
        assert raw.count('data-slide-id=')==4 and 'function go(n,opts={})' in raw
        assert 'const SPEAKER_NOTES' in raw and 'bg-dark' in raw and 'bg-light' in raw
        r=subprocess.run(['node',str(ROOT/'skill-forks/guizang-ppt-skill-ja/scripts/validate-presenter-mode.mjs'),str(ROOT/e['html'])],capture_output=True,text=True,encoding='utf-8')
        assert r.returncode==0,r.stdout+r.stderr

for index,file in enumerate(html_files):
    doc=Document();doc.feed(file.read_text(encoding='utf-8'))
    assert doc.title and len(doc.title)<180 and '<' not in doc.title,file
    for link in doc.targets:
        u=urlsplit(link)
        if u.scheme or link.startswith('#') or not u.path:continue
        p=(file.parent/unquote(u.path)).resolve()
        assert p.is_relative_to(ROOT) and p.exists(),(file.relative_to(ROOT),link)
    required_chars.update(ord(c) for c in ''.join(doc.text) if '\u3040'<=c<='\u9fff')
    for n,script in enumerate(doc.scripts):
        temp=js_dir/f'{index}-{n}.mjs';temp.write_text(script,encoding='utf-8')
        r=subprocess.run(['node','--check',str(temp)],capture_output=True,text=True,encoding='utf-8')
        assert r.returncode==0,(file,r.stderr)
for stem in ['noto-sans-jp','noto-serif-jp']:
    cmap=TTFont(ROOT/f'assets/fonts/{stem}.woff2').getBestCmap()
    missing=required_chars-set(cmap)
    assert not missing,(stem,'missing glyphs: '+''.join(chr(c) for c in sorted(missing)))

native=ROOT/'examples/actual/ppt-master-native/ppt-master-ja.pptx'
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(native) as z:
    assert z.testzip() is None
    slide_names=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
    note_names=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
    assert len(slide_names)==len(note_names)==4
    shape_count=0;run_count=0
    for name in slide_names:
        xml=ET.fromstring(z.read(name));assert not xml.findall('.//p:pic',ns),'Rasterized full-slide fallback'
        shape_count+=len(xml.findall('.//p:sp',ns));run_count+=len(xml.findall('.//a:t',ns))
        texts=''.join(t.text or '' for t in xml.findall('.//a:t',ns));assert any('\u3040'<=c<='\u9fff' for c in texts)
    assert shape_count>=25 and run_count>=30
report=json.loads((native.parent/'validation/ppt-master-ja.report.json').read_text(encoding='utf-8'))
assert report['status'].startswith('passed'),report['status']
result=dict(passed=True,original_repositories=209,actual_examples=3,actual_slides=12,native_pptx_shapes=shape_count,native_text_runs=run_count,all_page_notes=4,full_slide_images=0,html_files_checked=len(html_files),noto_glyphs_checked=len(required_chars))
(ROOT/'.build/actual-example-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
