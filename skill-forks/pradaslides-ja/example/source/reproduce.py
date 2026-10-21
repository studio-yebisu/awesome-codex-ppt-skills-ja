"""Reproduce this native PPTX and original render-parity presenter on Windows."""
from pathlib import Path
import subprocess,sys,json,hashlib,datetime,os
ROOT=Path(__file__).resolve().parents[1];UP=ROOT/'source/upstream/scripts'
def run(label,args):
 p=subprocess.run(args,cwd=ROOT,text=True,encoding='utf-8',errors='replace',capture_output=True);log=ROOT/'review'/f'{label}.log';log.parent.mkdir(exist_ok=True);log.write_text(p.stdout+p.stderr,encoding='utf-8')
 (ROOT/'review'/f'{label}-receipt.json').write_text(json.dumps({'argv':args,'cwd':str(ROOT),'exit_code':p.returncode,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()},ensure_ascii=False,indent=2),encoding='utf-8')
 print(label,p.returncode,p.stdout[-300:]);return p.returncode
def generate():
 if run('plan',[sys.executable,'source/plan.py']):raise SystemExit('plan failed')
 failures=[]
 for name,target in [('validate_brief','brief'),('validate_design_system','design-system'),('validate_source_ledger','source-ledger'),('validate_layout_manifest','layout-manifest'),('validate_asset_manifest','asset-manifest'),('validate_visual_generation_plan','visual-generation-plan')]:
  if run(name,[sys.executable,str(UP/f'{name}.py'),f'project/{target}.json','--json-output',f'review/{name}.json']):failures.append(name)
 args=[sys.executable,str(UP/'lint_deck_plan.py'),'project/deck-plan.json','--strict-visual','--json-output','review/lint.json']
 for n in ['brief','source-ledger','asset-manifest','design-system','layout-manifest']:args += ['--'+n,f'project/{n}.json']
 if run('lint',args):failures.append('lint')
 if failures:raise SystemExit('Planning gates failed: '+','.join(failures))
 for name,args in [('author',[sys.executable,'source/author.py']),('powerpoint',['pwsh','-NoProfile','-File','source/render_powerpoint.ps1','-PresentationPath','output/deck.pptx','-OutputDirectory',str(ROOT/'render')]),('pdf-rgb',[os.environ.get('PDF_PREVIEW_PYTHON',sys.executable),'source/render_pdf_previews.py','render']),('inspect',[sys.executable,str(UP/'inspect_pptx.py'),'output/deck.pptx','--json','review/pptx-inspection.json']),('preview',[sys.executable,str(UP/'build_pptx_preview.py'),'--output','presenter','--slides-dir','render','--deck-plan','project/deck-plan.json','--title','町内会の備品貸出を、迷わない手順に','--force'])]:
  if run(name,args):raise SystemExit(name+' failed')

def write_review_state(status):
 state={'status':status,'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_pages_visually_reviewed_by_author':False,'independent_reproduction':'pending','independent_visual_review':'pending','human_adoption':False,'note':'This reproduction invalidates reviews of previous outputs. Review the newly generated files before recording approval.'}
 if status=='generated_awaiting_review':
  state['artifact_sha256']=hashlib.sha256((ROOT/'output/deck.pptx').read_bytes()).hexdigest()
 (ROOT/'QA.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
 write_review_state('generation_in_progress')
 try:generate()
 except BaseException:
  write_review_state('generation_failed')
  raise
 write_review_state('generated_awaiting_review')
if __name__=='__main__':main()
