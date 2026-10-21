"""Scaffold with the original init, then author the talk around an unchanged engine and build."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,socket,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
def build(args):
 case=args.case.resolve();work=args.workspace.resolve();up=args.upstream.resolve()
 assert work.is_relative_to(ROOT.resolve()) and work!=ROOT.resolve() and work!=up, 'Private init target must stay inside this workspace.'
 npm='npm.cmd' if os.name=='nt' else 'npm'
 logs=case/'.private/runtime-logs';logs.mkdir(parents=True,exist_ok=True)
 if not (work/'.beatdeck.json').is_file():
  if work.exists():raise RuntimeError('Fresh init requires an absent private talk path; original source must remain separate.')
  shutil.copytree(up,work,ignore=shutil.ignore_patterns('examples','.git','node_modules','dist'))
  receipt={'unchanged_original':str(up),'verified_private_target':str(work),'within_workspace':True,'third_party_examples_not_copied':True}
  (logs/'init-path.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
  init=subprocess.run([npm,'run','init','--','--title','パンが、店先に届くまで。','--author','八百万図AIツールボックス / 架空企画','--lang','ja','--theme','light','--name','bread-stage'],cwd=work,capture_output=True,text=True,encoding='utf-8')
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
 destination=(case/'dist').resolve()
 assert destination.is_relative_to(case) and destination!=case
 generated={p.relative_to(work/'dist').as_posix() for p in (work/'dist').rglob('*') if p.is_file()}
 # Retain public notices. Preserve superseded hashed assets privately before
 # removing only those generated asset files from the rebuilt public folder.
 for prior in destination.rglob('*') if destination.exists() else []:
  if not prior.is_file():continue
  relative=prior.relative_to(destination).as_posix()
  if relative not in generated and relative!='THIRD-PARTY-NOTICES.md':
   if not relative.startswith('assets/'):raise RuntimeError('Unexpected non-generated dist companion: '+relative)
   backup=case/'.private/prior-dist-assets'/relative;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(prior,backup);prior.unlink()
 shutil.copytree(work/'dist',destination,dirs_exist_ok=True)
 (case/'source/build-receipt.json').write_text(json.dumps({'command':'npm run build','exit_code':result.returncode,'typecheck_bundle_offline_check':True,'scene_count':len(plan),'flattened_beats':sum(len(s['beats']) for s in plan),'verify_executed':False},indent=2)+'\n',encoding='utf-8')
 print('Original engine build copied to',case/'dist')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(args):
 """Run the unmodified original verification CLI, without reducing its defaults."""
 case=args.case.resolve();work=args.workspace.resolve();up=args.upstream.resolve()
 assert work.is_relative_to(ROOT.resolve()) and work!=ROOT.resolve() and work!=up
 output=(work/'artifacts/verify').resolve()
 # The original CLI recursively replaces this owned generated-output directory.
 assert output.is_relative_to(work) and output!=work and output.name=='verify' and output.parent.name=='artifacts'
 assert sha(work/'scripts/verify.mjs')==sha(up/'scripts/verify.mjs'),'Original verify script differs'
 assert sha(work/'scripts/lib.mjs')==sha(up/'scripts/lib.mjs'),'Original verification helper differs'
 public={p.relative_to(case/'dist').as_posix():sha(p) for p in (case/'dist').rglob('*') if p.is_file()}
 built={p.relative_to(work/'dist').as_posix():sha(p) for p in (work/'dist').rglob('*') if p.is_file()}
 # Public license notices are non-executing companions, not a different bundle.
 assert {k:v for k,v in public.items() if k!='THIRD-PARTY-NOTICES.md'}==built,'Public runtime differs from the test target'
 with socket.socket() as probe:
  if probe.connect_ex(('127.0.0.1',4174))==0:raise RuntimeError('Original verification port 4174 is in use; preserve the other process and retry later.')
 npm='npm.cmd' if os.name=='nt' else 'npm'
 command=[npm,'run','verify','--','--source=reference/SCRIPT.md']
 result=subprocess.run(command,cwd=work,capture_output=True,text=True,encoding='utf-8',errors='replace')
 private=case/'.private/runtime-logs';private.mkdir(parents=True,exist_ok=True)
 (private/'verify-stdout.txt').write_text(result.stdout,encoding='utf-8')
 (private/'verify-stderr.txt').write_text(result.stderr,encoding='utf-8')
 if (output/'report.json').is_file():
  shutil.copytree(output,case/'render/verify',dirs_exist_ok=True)
  report=json.loads((output/'report.json').read_text('utf-8'))
  exact_count=re.search(r'exact text: (\d+) line',result.stdout)
  receipt={'command':'npm run verify -- --source=reference/SCRIPT.md','exit_code':result.returncode,'original_verify_sha256':sha(up/'scripts/verify.mjs'),'original_lib_sha256':sha(up/'scripts/lib.mjs'),'default_diff_percent':0.1,'tolerances_changed':False,'public_runtime_bytes_equal':True,'public_additional_companions':['THIRD-PARTY-NOTICES.md'],'report':'render/verify/report.json','contact_sheet':'render/verify/contact.png','beats':report['beats'],'exact_text_element_count':int(exact_count[1]) if exact_count else None,'qr_configured':'QR: not configured' not in result.stdout,'manual_live_reliability_check':'not performed','physical_wifi_off_test':'not performed'}
  (case/'source/VERIFY.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n','utf-8')
  if result.returncode==0:
   build_receipt=case/'source/build-receipt.json'
   data=json.loads(build_receipt.read_text('utf-8'));data.update(verify_executed=True,verify_receipt='source/VERIFY.json',source_wide_exact_text_validated=False)
   build_receipt.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(result.stdout,flush=True)
 result.check_returncode()

def package(case):
 """Package only explicit public content; never traverse dependency junctions."""
 for folder,name in [(case,'beatdeck-example-ja.zip'),(ROOT/'skill-forks/beatdeck-ja','beatdeck-ja.zip')]:
  destination=ROOT/'downloads'/name
  with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as archive:
   for base,dirs,names in os.walk(folder,followlinks=False):
    here=Path(base)
    dirs[:]=[d for d in dirs if d not in {'node_modules','.private','.build','.git','__pycache__','cache','artifacts'} and not (here/d).is_symlink() and not (getattr(here/d,'is_junction',lambda:False))()]
    for filename in names:
     path=here/filename
     if path.suffix=='.pyc' or filename in {'build-log.txt','init-log.txt'}:continue
     archive.write(path,Path(folder.name)/path.relative_to(folder))
  print(name,sha(destination))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--case',type=Path,default=ROOT/'examples/repositories/beatdeck-showcase');p.add_argument('--workspace',type=Path,default=ROOT/'.build/beatdeck-talk');p.add_argument('--upstream',type=Path,default=ROOT/'.build/actual-upstreams/borjaperfra__beatdeck');p.add_argument('--verify',action='store_true');p.add_argument('--verify-only',action='store_true');p.add_argument('--package-only',action='store_true');args=p.parse_args()
 if args.package_only:package(args.case.resolve())
 elif args.verify_only:verify(args)
 else:
  build(args)
  if args.verify:verify(args)
