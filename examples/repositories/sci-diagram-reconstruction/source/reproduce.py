"""Replay the accepted reconstruction using its original unchanged build/checker.

This is not a new reconstruction of another input. Use a prepared host runtime
root; never copy/install node_modules into the delivery pass.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,shutil,subprocess,sys,os,tempfile
C=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--node',default=shutil.which('node'));p.add_argument('--overwrite',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--soffice',default=shutil.which('soffice'));p.add_argument('--pdftoppm',default=shutil.which('pdftoppm'));a=p.parse_args();assert a.node
    assert sha(C/'pass-01/source.png')==sha(C/'input/source.png')
    if (C/'pass-01/editable.pptx').exists()and not a.overwrite:raise SystemExit('Accepted output exists; use --overwrite explicitly to rebuild this copy.')
    # The unchanged original probe discovers commands through PATH. Expose only
    # the explicitly supplied existing executables to this child process tree.
    # LibreOffice may ship an older python.exe. Keep the caller's verified
    # Python ahead of that program directory for the original runtime probe.
    supplied=[Path(x).resolve().parent for x in [sys.executable,a.node,a.soffice,a.pdftoppm]if x and Path(x).is_file()]
    child_env=dict(os.environ,PATH=os.pathsep.join([str(x)for x in supplied]+[os.environ.get('PATH','')]))
    receipts=[]
    def run(argv,phase,cwd=C):
        r=subprocess.run(list(map(str,argv)),cwd=cwd,env=child_env,capture_output=True,text=True,encoding='utf-8',errors='replace')
        receipts.append({'phase':phase,'exit_code':r.returncode});print(phase,r.returncode,flush=True)
        if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    run([a.node,C/'upstream/scripts/probe_runtime.mjs','--runtime','pptxgenjs','--task-dir',C/'pass-01'],'original-runtime-probe')
    run([a.node,'build.mjs','--overwrite'],'accepted-build',C/'pass-01')
    run([sys.executable,'upstream/scripts/check_pptx.py','pass-01/editable.pptx','--source','pass-01/source.png','--build-source','pass-01/build.mjs','--require-single-slide','--slide','1','--pass-index','1','--output','qa/check-pass-01.json'],'original-package-check')
    run([sys.executable,'source/check_native_lines.py'],'native-line-topology')
    if a.render:
        assert a.soffice and a.pdftoppm,'Existing LibreOffice and pdftoppm required; supply --soffice/--pdftoppm. No installation performed.'
        lo_output=C/'qa'/('original-libreoffice-replay-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
        # The original renderer creates its own isolated LibreOffice profile.
        # Keep that profile below the OS temp directory to avoid deep Windows
        # profile paths; preserve the completed evidence beside this replay.
        with tempfile.TemporaryDirectory(prefix='sci-render-') as temporary:
            rendered=Path(temporary)/'lo'
            run([sys.executable,'upstream/scripts/render_pptx.py','pass-01/editable.pptx','--output-dir',rendered,'--keep-pdf','--soffice',a.soffice,'--pdftoppm',a.pdftoppm],'original-isolated-libreoffice-render')
            shutil.copytree(rendered,lo_output)
        run(['pwsh','-NoProfile','-File','source/render_powerpoint.ps1','-PresentationPath',C/'pass-01/editable.pptx','-OutputDirectory',C/'render'],'powerpoint-render')
        run([a.pdftoppm,'-png','-scale-to-x','1600','-scale-to-y','-1','-singlefile','render/deck.pdf','render/slide-01'],'actual-powerpoint-pdf-rgb')
    (C/'qa/reproduction.json').write_text(json.dumps({'status':'checks_executed_new_output_requires_visual_review','accepted_build':'pass-01/build.mjs','source':'pass-01/source.png','source_sha256':sha(C/'pass-01/source.png'),'pptx_sha256':sha(C/'pass-01/editable.pptx'),'commands':receipts,'prior_visual_or_independent_review_transferred':False,'fresh_install_executed':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
