"""Rebuild native pages from frozen ImageGen blueprints, preserving original diff failures."""
from pathlib import Path
import hashlib,json,subprocess,sys,shutil,datetime,argparse
P=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input',type=Path,default=P/'input/outline.json',help='Frozen outline.json or its byte-identical data.json alias')
parser.add_argument('--render',action='store_true',help='Accepted explicitly; PowerPoint rendering is always performed by this pipeline')
args=parser.parse_args()
selected=args.input.resolve()
if not selected.is_file():raise SystemExit('Input file does not exist: '+str(selected))
if selected.read_bytes()!=(P/'input/outline.json').read_bytes():raise SystemExit('Input differs from the frozen blueprint content. Create new blueprints and measurements before rebuilding changed content.')
(P/'input/data.json').write_bytes((P/'input/outline.json').read_bytes())
R=P/'review/replay';R.mkdir(parents=True,exist_ok=True)
receipts=[]
def run(argv,allowed=(0,)):
    r=subprocess.run([str(x) for x in argv],cwd=P,capture_output=True,text=True,encoding='utf-8',errors='replace')
    name=f'{len(receipts)+1:02d}-{Path(str(argv[1])).stem if len(argv)>1 else "run"}.log';log=R/name;log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
    receipts.append({'argv':[str(x) for x in argv],'cwd':str(P),'exit_code':r.returncode,'log':str(log.relative_to(P)).replace('\\','/'),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'original_gate_failure_expected':r.returncode!=0 and r.returncode in allowed})
    (R/'execution-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if r.returncode not in allowed:raise RuntimeError(r.stdout+'\n'+r.stderr)
    print(f'{len(receipts):02d}: exit {r.returncode} '+Path(str(argv[1])).name)
py=sys.executable;node=shutil.which('node');ps=shutil.which('powershell') or shutil.which('pwsh')
if not node or not ps:raise SystemExit('Node.js and PowerShell are required')
for n in range(1,6):
    tag=f'{n:02d}';bp=P/f'design/slide-{tag}-blueprint.png'
    if not bp.exists():raise SystemExit('Frozen ImageGen blueprint missing: '+str(bp))
    run([py,P/'source/upstream/scripts/build_content_lock.py','--outline',P/'input/outline.json','--slide',n,'--out',P/f'design/slide-{tag}-content-lock.json'])
    run([py,P/'source/prepare_measurements.py',n])
    run([node,P/'source/reconstruct.cjs',n])
    run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',P/'source/render_powerpoint.ps1','-PresentationPath',P/f'pages/slide-{tag}.pptx','-OutputDirectory',P/f'render/page-{tag}'])
    run([py,P/'source/audit_page.py',n])
    d=P/'review/approved-renders';d.mkdir(exist_ok=True);shutil.copy2(P/f'render/page-{tag}/slide-01.png',d/f'slide-{tag}.png')
run([py,P/'source/merge_verified_pages_ja.py','--pages',*[P/f'pages/slide-{n:02d}.pptx' for n in range(1,6)],'--out',P/'deck.pptx','--manifest-out',P/'review/merge.json'])
run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',P/'source/render_powerpoint.ps1','-PresentationPath',P/'deck.pptx','-OutputDirectory',P/'render'])
run([py,P/'source/upstream/scripts/compare_merged_render.py','--approved-dir',P/'review/approved-renders','--merged-dir',P/'render','--out',P/'review/merge-regression.json'])
run([py,P/'source/upstream/scripts/inspect_pptx_objects.py',P/'deck.pptx','--out',P/'review/original-object-inspection.json'])
run([py,P/'source/upstream/scripts/validate_pptx.py',P/'deck.pptx','--strict','--json-out',P/'review/original-strict-validation.json'],allowed=(0,1))
(P/'QA.json').write_text(json.dumps({'status':'generated_awaiting_review','artifact_sha256':hashlib.sha256((P/'deck.pptx').read_bytes()).hexdigest(),'original_gate_not_passed':True,'human_adoption':'pending','visual_review':'Rebuilt artifacts require a new full-page visual review; original catalog QA is not transferred.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Rebuilt 5 slides; original strict gate result is retained. Rebuilt files require a fresh visual review before adoption.')
