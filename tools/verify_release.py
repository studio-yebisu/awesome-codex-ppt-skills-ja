"""Current catalog release verification; withdrawn prototypes are excluded."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, zipfile, xml.etree.ElementTree as ET
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    subprocess.run([sys.executable,str(ROOT/'tools/verify_actual_examples.py')],check=True)
    artifacts=[]
    paths=['downloads/guizang-ppt-skill-ja.zip','downloads/frontend-slides-ja.zip','downloads/ppt-master-ja.zip','downloads/guizang-magazine-ja.zip','downloads/frontend-bold-signal-ja.zip','examples/actual/ppt-master-native/ppt-master-ja.pptx']
    for relative in paths:
        p=ROOT/relative
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None,p
            assert all(not n.startswith('/') and '..' not in Path(n).parts and '__pycache__' not in n and 'node_modules/' not in n for n in z.namelist()),p
            if p.suffix=='.zip':assert any(n.endswith('/LICENSE') for n in z.namelist()),p
        artifacts.append(dict(file=relative,bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest()))
    (ROOT/'data/actual-downloads.json').write_text(json.dumps(artifacts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(passed=True,release_artifacts=len(artifacts),source_forks=3,original_catalog=209,examples=3,slides=12),ensure_ascii=False))
    sys.exit(0)

# The old prototype-only checks below are retained as historical code.
class Links(HTMLParser):
    def __init__(self):super().__init__();self.targets=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ['href','src']:
            if key in a:self.targets.append(a[key])
reports=[]
for record in json.loads((ROOT/'data/downloads.json').read_text(encoding='utf-8')):
    p=ROOT/record['file'];assert sha256(p.read_bytes()).hexdigest()==record['sha256'],p
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None,p
        assert all('node_modules/' not in n and not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist()),p
for html in [ROOT/'index.html',ROOT/'guide.html',ROOT/'licenses.html']:
    parser=Links();parser.feed(html.read_text(encoding='utf-8'))
    for link in parser.targets:
        url=urlsplit(link)
        if url.scheme or link.startswith('#'):continue
        target=html.parent/unquote(url.path)
        assert target.exists(),f'{html.name}: broken link {link}'
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
for pptx in sorted((ROOT/'downloads').glob('*.pptx')):
    with zipfile.ZipFile(pptx) as z:
        slides=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        notes=[n for n in z.namelist() if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml')]
        native=sum(len(ET.fromstring(z.read(n)).findall('.//p:sp',ns)) for n in slides)
        runs=sum(len(ET.fromstring(z.read(n)).findall('.//a:t',ns)) for n in slides)
        assert len(slides)==4 and len(notes)==4 and native>25 and runs>20,pptx.name
        if pptx.stem=='local-coffee':
            assert any('/charts/' in n and n.endswith('.xml') and '/_rels/' not in n for n in z.namelist())
            assert any(n.endswith('.xlsx') and n.startswith('ppt/embeddings/') for n in z.namelist())
        reports.append(dict(deck=pptx.stem,slides=4,notes=4,native_shapes=native,text_runs=runs))
out=ROOT/'.build/release-check.json';out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({'passed':True,'downloads':17,'presentations':reports},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':True,'downloads':17,'decks':len(reports),'slides':24,'native_shapes':sum(r['native_shapes'] for r in reports)},ensure_ascii=False))
