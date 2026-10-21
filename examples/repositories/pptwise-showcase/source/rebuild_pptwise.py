"""Source-built original pptwise0.44.0: spec → inspect → pages → build.

No layout override, PPTX modification, package installation, or API call.
The integration agent implemented this repair; it is not attributed to Opus.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess

CASE=Path(__file__).resolve().parents[1]
SOURCE=CASE/'source/pipeline'
INPUT=CASE/'input'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--node',default=os.environ.get('PPTWISE_NODE') or shutil.which('node'))
 ap.add_argument('--cli',type=Path)
 args=ap.parse_args()
 if not args.node:raise SystemExit('Node22.19+が必要です（--nodeで指定）')
 local=CASE/'runtime/dist/cli.js'
 fixed=CASE.parents[2]/'.build/actual-upstreams/liustack__pptwise/dist/cli.js'
 cli=(args.cli or (local if (CASE/'runtime/node_modules').is_dir() else fixed if fixed.is_file() else local)).resolve()
 if not cli.is_file():raise SystemExit('同梱runtime/dist/cli.jsが必要です。別の固定CLIは--cliで指定します')
 SOURCE.mkdir(exist_ok=True,parents=True)
 receipts=[]
 def clean(value):
  if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
  if isinstance(value,list):return [clean(v) for v in value]
  if isinstance(value,str):
   for p in [CASE,cli.parent,Path(args.node).parent]:
    value=value.replace(str(p),'.').replace(p.as_posix(),'.')
   return value
  return value
 def run(cmd,name,allow_failure=False):
  p=subprocess.run([args.node,str(CASE/'source/pptwise_ja_font_adapter.mjs'),str(cli),*cmd],cwd=CASE,capture_output=True,text=True,encoding='utf-8',errors='replace')
  text=clean(p.stdout);(SOURCE/(name+'.txt')).write_text(text,encoding='utf-8')
  if p.stderr:(SOURCE/(name+'.stderr.txt')).write_text(clean(p.stderr),encoding='utf-8')
  receipts.append({'command':['node','source/pptwise_ja_font_adapter.mjs','<fixed-source-built-cli>',*cmd],'exit_code':p.returncode,'stdout':'source/pipeline/'+name+'.txt'})
  if p.returncode and not allow_failure:raise RuntimeError(text+clean(p.stderr))
  return p
 def build(name,partial=False):
  p=run(['build','input','--json','--no-git-ignore','--no-alternatives'],name,allow_failure=partial)
  report=json.loads(p.stdout)
  dump(SOURCE/(name+'.json'),clean(report))
  if not partial and (p.returncode or report.get('status')!='ok' or not report.get('pptx')):
   raise RuntimeError('原典buildが未合格。source/pipeline/'+name+'.jsonを確認してsourceを直してください')
  return report
 try:
  # Rebuild retained source inputs without replacing pages or inventing data.
  run(['schema','--spec'],'schema-spec')
  run(['narratives','--json'],'narratives')
  run(['themes','--json'],'themes')
  run(['spec','validate','input/deck.spec.json'],'spec-validate')
  for p in load(INPUT/'deck.spec.json')['pages']:
   run(['inspect','input','--page',p['id']],f'inspect-{p["id"]}')
   for part in load(INPUT/'pages'/(p['id']+'.json')).get('components',[]):
    run(['inspect','input','--page',p['id'],'--component',part['type']],f'inspect-{p["id"]}-{part["type"]}')
  report=build('build-final')
  for p in load(INPUT/'deck.spec.json')['pages']:
   run(['inspect','input','--page',p['id'],'--fit'],f'fit-{p["id"]}')
  output=Path(report['pptx']);output=output if output.is_absolute() else CASE/output
  if not output.is_file():raise RuntimeError('buildの出力PPTXが存在しません')
  relative=output.resolve().relative_to(CASE.resolve()).as_posix()
  dump(SOURCE/'execution.json',{'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ok','original_cli_sha256':sha(cli),'bundled_cli_same_bytes':local.is_file() and sha(local)==sha(cli),'receipts':receipts,'pptx':relative,'pptx_sha256':sha(output),'original_files_modified':False,'renderer_geometry_modified':False,'font_allowlist_adapter':{'file':'source/pptwise_ja_font_adapter.mjs','scope':'In-memory SAFE_FONTS/CJK_SAFE_FACES additions only','added':['Zen Kaku Gothic New','Space Grotesk'],'original_chunk_sha256':'36c3b6ef31a0e36b5814e357e8033b12ae61f9e90537b0ddb6e54c7b19df2d1e'},'pptx_post_processed':False,'copied_or_renamed_final_pptx':False,'not_performed':['Human adoption','Independent review of this repaired version'],'original_self_check':'CLI JSON build/fit reports only','separate_catalog_visual_check':'PowerPoint PNG visual inspection requested by the user is a separate catalog check; not the original self-check.'})
  print(json.dumps({'status':'ok','pptx':relative,'sha256':sha(output)},ensure_ascii=False))
 except Exception:
  dump(SOURCE/'execution-incomplete.json',{'status':'incomplete','receipts':receipts,'no_pass_claim':True})
  raise

if __name__=='__main__':main()
