"""Rebuild the fixed Cafe example using its disclosed original compiler route."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
CASE=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--preview-python',default=sys.executable);p.add_argument('--node-modules');args=p.parse_args()
    env=os.environ.copy()
    if args.node_modules:env['NODE_PATH']=str(Path(args.node_modules).resolve())
    receipts=[]
    def run(argv,allowed=(0,)):
        r=subprocess.run([str(x) for x in argv],cwd=CASE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
        receipts.append({'argv':['python' if str(x)==sys.executable else str(x) for x in argv],'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()})
        (CASE/'source/execution-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if r.returncode not in allowed:raise RuntimeError(receipts[-1])
        print(r.stdout.strip(),flush=True)
        return r
    py=sys.executable;ps=shutil.which('powershell') or shutil.which('pwsh');node=shutil.which('node')
    assert ps and node
    run([py,'source/build_cafe.py'])
    run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File','source/check_layout.ps1'],allowed=(0,2))
    (CASE/'review').mkdir(exist_ok=True)
    shutil.copy2(CASE/'source/layout-overflow.json',CASE/'review/compiler-layout-overflow.json')
    run([py,'source/fit_text_frames.py'])
    run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File','source/check_layout.ps1'])
    run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File','source/render_powerpoint.ps1','-PresentationPath','deck.pptx','-OutputDirectory','render'])
    run([args.preview_python,'source/render_pdf_previews.py','render'])
    run([node,'source/capture_svg.cjs'])
    run([py,'source/build_comparisons.py'])
    run([py,'source/inspect_artifacts.py'])
    run([py,'source/edit_reopen.py'])
    qa={'status':'generated_requires_visual_review','artifact_sha256':hashlib.sha256((CASE/'deck.pptx').read_bytes()).hexdigest(),'all_pages_inspected_by_integrator':False,'independent_current_version_review':'pending','actual_execution_receipts':'source/execution-receipts.json','scope':'Fresh generation does not inherit prior visual or independent acceptance.'}
    (CASE/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
