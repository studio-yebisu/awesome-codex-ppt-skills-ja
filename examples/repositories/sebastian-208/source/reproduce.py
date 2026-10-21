"""Package the frozen imagegen pages using the original pinned packager.

No image generation, OCR or local creative drawing happens during replay.
"""
from pathlib import Path
import os,sys,shutil,subprocess,json,hashlib,argparse
C=Path(__file__).resolve().parents[1]
UP=C/'source/upstream-original/skills/academic-image-ppt/scripts/package_image_pptx_with_notes.mjs'

def main():
 p=argparse.ArgumentParser();p.add_argument('--node',default=shutil.which('node'));p.add_argument('--node-modules',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--preview-python',default=sys.executable);a=p.parse_args();assert a.node
 env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONUTF8='1');env['NODE_PATH']=str(a.node_modules.resolve()) if a.node_modules else str(C/'source/node_modules');receipts=[]
 def run(argv,tag):
  r=subprocess.run(list(map(str,argv)),cwd=C,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');out=C/'source/checks';out.mkdir(exist_ok=True);log=out/(tag+'.log');log.write_text(r.stdout+r.stderr,encoding='utf-8');receipts.append({'argv':list(map(str,argv)),'exit_code':r.returncode,'log':log.relative_to(C).as_posix(),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()});(out/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(tag,r.returncode,flush=True)
  if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
 run([a.node,UP,'--images','image_pages','--notes','NOTES.md','--out','deck.pptx','--title','雨の図書室'],'original-packager')
 if a.render:
  run(['pwsh','-NoProfile','-File','source/render_powerpoint.ps1','-PresentationPath',C/'deck.pptx','-OutputDirectory',C/'render'],'powerpoint')
  run([a.preview_python,'source/render_pdf_previews.py',C/'render'],'pdf-rgb')
 run([a.preview_python,'source/verify_current.py'],'image-notes-proof')
 print(C/'deck.pptx')
if __name__=='__main__':main()
