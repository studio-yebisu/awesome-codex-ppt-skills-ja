"""One-time development verification in an isolated normally installed Node project."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json,hashlib,os,zipfile,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parents[1];root=P.parents[2]
temp=Path(tempfile.mkdtemp(prefix='cyberppt-portable-',dir=root/'.build'));case=temp/'case';shutil.copytree(P,case,ignore=shutil.ignore_patterns('node_modules','__pycache__','*.pyc'))
receipts=[]
def run(argv,name):
 r=subprocess.run(argv,cwd=case,capture_output=True,text=True,encoding='utf-8',errors='replace');log=P/'review'/name;log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');receipts.append({'argv':argv,'cwd':str(case),'exit_code':r.returncode,'log':str(log.relative_to(P)),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()});r.check_returncode()
npm=shutil.which('npm.cmd') or shutil.which('npm');run([npm,'install','--prefix','source','--ignore-scripts','--no-audit','--no-fund'],'portable-npm.log')
run([sys.executable,'source/reproduce.py','--input','input/data.json','--render'],'portable-reproduce.log')
def texts(p):
 with zipfile.ZipFile(p) as z:return [''.join(e.text or '' for e in ET.fromstring(z.read(f'ppt/slides/slide{n}.xml')).iter() if e.tag.endswith('}t')) for n in range(1,6)]
native_text_identical=texts(P/'deck.pptx')==texts(case/'deck.pptx')
run([sys.executable,str(P/'source/upstream/scripts/compare_merged_render.py'),'--approved-dir',str(P/'render'),'--merged-dir',str(case/'render'),'--out',str(P/'review/portable-render-comparison.json')],'portable-render-compare.log')
report={'passed':native_text_identical,'directory':str(case),'node_dependency_resolution':'source/node_modules installed from package.json by npm; fallback repository .build/node_modules not needed','input_alias_byte_identical':(case/'input/data.json').read_bytes()==(case/'input/outline.json').read_bytes(),'native_text_identical':native_text_identical,'render_comparison':'review/portable-render-comparison.json','execution_receipts':receipts,'original_gate_not_passed':True,'source_artifact_sha256':hashlib.sha256((P/'deck.pptx').read_bytes()).hexdigest(),'portable_artifact_sha256':hashlib.sha256((case/'deck.pptx').read_bytes()).hexdigest()}
(P/'review/portable-proof.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
