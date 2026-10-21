"""Replay this chapter example in an existing prepared runtime; no installs."""
from pathlib import Path
import argparse,subprocess,sys,os,shutil,tempfile,json,hashlib
C=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--node',default=shutil.which('node'));p.add_argument('--soffice',default=shutil.which('soffice'));p.add_argument('--pdftoppm',default=shutil.which('pdftoppm'));p.add_argument('--render',action='store_true');a=p.parse_args();assert a.node
 env=dict(os.environ,HANDDRAWN_PYTHON=sys.executable);rows=[]
 def run(argv,phase):
  r=subprocess.run(list(map(str,argv)),cwd=C,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');rows.append({'phase':phase,'exit_code':r.returncode});print(phase,r.returncode,flush=True)
  if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 run([a.node,'build.cjs'],'original-template-and-Japanese-font-adapter');run([sys.executable,'source/check_recipe.py'],'recipe-structure-check')
 if a.render:
  assert a.soffice and a.pdftoppm,'Existing LibreOffice and pdftoppm required.'
  with tempfile.TemporaryDirectory(prefix='hand-chapter-lo-')as tmp:
   t=Path(tmp);run([a.soffice,'-env:UserInstallation='+str((t/'profile').as_uri()),'--headless','--convert-to','pdf','--outdir',t,C/'deck.pptx'],'original-Step6-LibreOffice-PDF')
   dest=C/'reviews/libreoffice';dest.mkdir(parents=True,exist_ok=True);shutil.copy2(t/'deck.pdf',dest/'deck.pdf')
  run([a.pdftoppm,'-jpeg','-r','150','reviews/libreoffice/deck.pdf','reviews/libreoffice/slide'],'original-Step6-all-page-JPEG150dpi')
  run(['pwsh','-NoProfile','-File','source/render_powerpoint.ps1','-PresentationPath',C/'deck.pptx','-OutputDirectory',C/'render'],'additional-PowerPoint-PDF')
  run([sys.executable,'source/render_pdf_previews.py','render'],'actual-PowerPoint-PDF-PNG')
  run(['pwsh','-NoProfile','-File','source/test_native_edit.ps1','-PresentationPath',C/'deck.pptx','-OutputDirectory',C/'qa/editability'],'separate-copy-native-title-edit')
  run([sys.executable,'source/render_pdf_previews.py','qa/editability','--pdf-name','native-title-edited.pdf','--single-output','native-title-edited.png','--page','2'],'actual-edited-page-PNG')
 out={'status':'execution_complete_new_outputs_require_visual_review','commands':rows,'pptx_sha256':hashlib.sha256((C/'deck.pptx').read_bytes()).hexdigest(),'fresh_install_executed':False,'prior_visual_review_transferred':False}
 (C/'source/reproduction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
