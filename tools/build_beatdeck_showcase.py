"""Scaffold with the original init, then author the talk around an unchanged engine and build."""
from pathlib import Path
import argparse,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
def build(args):
 case=args.case.resolve();work=args.workspace.resolve();up=args.upstream.resolve()
 assert work.is_relative_to(ROOT.resolve()) and work!=ROOT.resolve() and work!=up, 'Private init target must stay inside this workspace.'
 npm='npm.cmd' if os.name=='nt' else 'npm'
 logs=case/'source';logs.mkdir(parents=True,exist_ok=True)
 if not (work/'.beatdeck.json').is_file():
  if work.exists():raise RuntimeError('Fresh init requires an absent private talk path; original source must remain separate.')
  shutil.copytree(up,work,ignore=shutil.ignore_patterns('examples','.git','node_modules','dist'))
  receipt={'unchanged_original':str(up),'verified_private_target':str(work),'within_workspace':True,'third_party_examples_not_copied':True}
  (logs/'init-path.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
  init=subprocess.run([npm,'run','init','--','--title','パンが、店先に届くまで。','--author','Studio Yebisu / 架空企画','--lang','ja','--theme','light','--name','bread-stage'],cwd=work,capture_output=True,text=True,encoding='utf-8')
  (logs/'init-log.txt').write_text(init.stdout+init.stderr,encoding='utf-8');init.check_returncode()
 # Content audit precedes authored code. The source and audit are copied as inputs.
 for d in ['docs','reference']:shutil.copytree(case/d,work/d,dirs_exist_ok=True)
 for d in ['01-Open.tsx','02-End.tsx']:
  p=work/'deck/scenes'/d
  if p.is_file():p.unlink() # Only the known blank starter layers in this verified private talk.
 shutil.copytree(case/'source/authored/deck',work/'deck',dirs_exist_ok=True)
 shutil.copytree(case/'fonts',work/'deck/assets/fonts',dirs_exist_ok=True)
 plan=json.loads((case/'input/scene-plan.json').read_text(encoding='utf-8'))
 (work/'deck/scenes.ts').write_text("import type {SceneDef} from 'beatdeck';\nexport const SCENES:SceneDef[]="+json.dumps(plan,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
 if not (work/'node_modules').is_dir():subprocess.run([npm,'ci','--ignore-scripts','--no-audit','--no-fund'],cwd=work,check=True)
 result=subprocess.run([npm,'run','build'],cwd=work,capture_output=True,text=True,encoding='utf-8')
 (logs/'build-log.txt').write_text(result.stdout+result.stderr,encoding='utf-8')
 print(result.stdout,flush=True)
 if result.returncode:print(result.stderr,flush=True)
 result.check_returncode()
 shutil.copytree(work/'dist',case/'dist',dirs_exist_ok=True)
 (logs/'build-receipt.json').write_text(json.dumps({'command':'npm run build','exit_code':result.returncode,'typecheck_bundle_offline_check':True,'scene_count':len(plan),'flattened_beats':sum(len(s['beats']) for s in plan),'verify_executed':False},indent=2)+'\n',encoding='utf-8')
 print('Original engine build copied to',case/'dist')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--case',type=Path,default=ROOT/'examples/repositories/beatdeck-showcase');p.add_argument('--workspace',type=Path,default=ROOT/'.build/beatdeck-talk');p.add_argument('--upstream',type=Path,default=ROOT/'.build/actual-upstreams/borjaperfra__beatdeck');build(p.parse_args())
