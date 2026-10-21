"""Original native engine + explicitly diffed Japanese runtime; original QA gates."""
from pathlib import Path
import os,subprocess,sys,json,hashlib,argparse,shutil
C=Path(__file__).resolve().parents[1];UP=C/'source/upstream-original/codex-ppt-skill';RT=C/'source/runtime/codex-ppt-skill'
def main():
 p=argparse.ArgumentParser();p.add_argument('--node',default=shutil.which('node'));p.add_argument('--node-modules',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--preview-python',default=sys.executable);a=p.parse_args();assert a.node
 env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONUTF8='1');env['NODE_PATH']=str(a.node_modules.resolve()) if a.node_modules else str(C/'source/node_modules');receipts=[]
 def run(argv,tag,expected=(0,)):
  r=subprocess.run(list(map(str,argv)),cwd=C,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');out=C/'source/checks';out.mkdir(exist_ok=True);log=out/(tag+'.log')
  def display(value):
   text=str(value)
   for raw,label in [(str(C),'$CASE'),(str(a.node),'$NODE'),(str(sys.executable),'$PYTHON'),(str(a.preview_python),'$PREVIEW_PYTHON')]:
    text=text.replace(raw,label).replace(raw.replace('\\','/'),label).replace(raw.replace('/','\\'),label)
   return text
  log.write_text(display(r.stdout+r.stderr),encoding='utf-8');receipts.append({'argv':list(map(display,argv)),'path_display_normalized':True,'exit_code':r.returncode,'log':log.relative_to(C).as_posix(),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()});(out/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(tag,r.returncode,flush=True)
  if r.returncode not in expected:raise RuntimeError(r.stdout+'\n'+r.stderr)
 run([sys.executable,UP/'scripts/build_reference_board.py','--topic','bookstore editorial culture','--style','editorial-ink','--output-dir','qa/reference-selection'],'original-reference-board')
 run([sys.executable,UP/'scripts/validate_slides_plan.py','input/slides_plan.json','--output','qa/slides-plan-validation.json'],'original-plan-validation')
 run([a.node,RT/'scripts/build_native_pptx.mjs','--spec','input/spec_lock.json','--slides','input/slides_plan.json','--asset-plan','input/asset_plan.json','--notes','input/speaker_notes.json','--reference-board','input/reference_board.json','--output','deck.pptx'],'original-native-build')
 if a.render:
  run(['pwsh','-NoProfile','-File','source/render_powerpoint.ps1','-PresentationPath',C/'deck.pptx','-OutputDirectory',C/'render'],'powerpoint')
  run([a.preview_python,'source/render_pdf_previews.py',C/'render'],'pdf-rgb')
  out=C/'qa/original-render';out.mkdir(parents=True,exist_ok=True)
  for i in range(1,9):shutil.copy2(C/f'render/slide-{i:02}.png',out/f'slide_{i:02}.png')
  shutil.copy2(C/'render/deck.pdf',out/'final.pdf')
  run([sys.executable,UP/'scripts/validate_pptx.py','deck.pptx','--expected-slide-count','8','--asset-plan','input/asset_plan.json','--preview-dir',out,'--require-notes','--expected-aspect-ratio','16:9','--output','qa/pptx-validation.json','--markdown','qa/qa_report.md'],'original-pptx-validation')
  run([sys.executable,UP/'scripts/aesthetic_qa.py','--pptx','deck.pptx','--preview-dir',out,'--slides-plan','input/slides_plan.json','--spec','input/spec_lock.json','--reference-board','input/reference_board.json','--asset-plan','input/asset_plan.json','--output-dir','qa','--case-id','sebastian-207'],'original-aesthetic',expected=(0,2))
  q=json.loads((C/'qa/aesthetic_qa_report.json').read_text(encoding='utf-8'));print('Original aesthetic',q['status'],q['score'])
  if q['status']!='PASS':raise SystemExit(2)
 print(C/'deck.pptx')
if __name__=='__main__':main()
