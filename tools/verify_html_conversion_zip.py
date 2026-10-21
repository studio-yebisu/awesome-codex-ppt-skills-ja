"""Run the actual packaged converter and compare all PowerPoint page renders."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];CASE=ROOT/'examples/repositories/html-editable-showcase'
def main():
 archive=ROOT/'downloads/html-editable-example-ja.zip';target=CASE/'.private/distribution-replay-20261015';target.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None;assert any(n.endswith('/upstream/scripts/visual_audit.py') for n in z.namelist());z.extractall(target)
 p=target/'html-editable-example-ja';cmd=[sys.executable,str(p/'convert_local_fonts.py'),str(p/'index.audited.html'),'--out',str(p/'replay.pptx'),'--keep-screenshots','--no-embed-fonts']
 r=subprocess.run(cmd,cwd=p,capture_output=True,text=True,encoding='utf-8');(target/'stdout.txt').write_text(r.stdout,encoding='utf-8');(target/'stderr.txt').write_text(r.stderr,encoding='utf-8')
 if r.returncode:print(r.stdout[-2500:],r.stderr[-1500:]);raise SystemExit(r.returncode)
 idx=json.loads((p/'replay_audit/audit_index.json').read_text(encoding='utf-8'));assert idx['total_pages']==5 and idx['self_check_summary']['structural_warnings_count']==0
 pngs=sorted((p/'replay_audit/_ppt_renders').glob('*.png'));original=sorted((CASE/'deck_audit/_ppt_renders').glob('*.png'));assert len(pngs)==len(original)==5
 differences=[]
 for n,(a,b) in enumerate(zip(original,pngs),1):
  a=Image.open(a).convert('RGB');b=Image.open(b).convert('RGB');assert a.size==b.size;differences.append({'page':n,'rgb_difference_bbox':ImageChops.difference(a,b).getbbox()})
 assert all(d['rgb_difference_bbox'] is None for d in differences),differences
 record={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'route':'Extracted ZIP; original preflight/measure/assemble/Stage5a/5b with declared font/effects/header adapters','exit_code':r.returncode,'pages':5,'original_structural_warnings':0,'PowerPoint_render_comparison':differences,'dependency_scope':'Existing Python/Playwright/PowerPoint dependencies; fresh dependency installation not tested.'}
 (CASE/'qa/zip-replay.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(record))
if __name__=='__main__':main()
