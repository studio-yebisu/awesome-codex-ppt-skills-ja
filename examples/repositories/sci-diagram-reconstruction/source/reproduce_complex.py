"""Replay the saved accepted additional pass04 in a disposable copy under a prepared host runtime."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

C=Path(__file__).resolve().parents[1]
PASS=C/'complex-example/pass-04'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--node',default=shutil.which('node'))
    p.add_argument('--overwrite',action='store_true')
    p.add_argument('--render',action='store_true')
    p.add_argument('--soffice',default=shutil.which('soffice'))
    p.add_argument('--pdftoppm',default=shutil.which('pdftoppm'))
    a=p.parse_args()
    if not a.node:raise SystemExit('Existing Node.js required; no installation performed.')
    if sha(PASS/'source.png')!=sha(C/'complex-example/input/source.png'):raise SystemExit('Source copies differ.')
    if (PASS/'editable.pptx').exists() and not a.overwrite:raise SystemExit('Use --overwrite only in a disposable replay copy.')
    if a.render and not(a.soffice and a.pdftoppm):raise SystemExit('Existing LibreOffice and pdftoppm required; supply their paths.')
    supplied=[str(Path(x).resolve().parent) for x in [sys.executable,a.node,a.soffice,a.pdftoppm] if x and Path(x).is_file()]
    env=dict(os.environ,PATH=os.pathsep.join(supplied+[os.environ.get('PATH','')]),PYTHONDONTWRITEBYTECODE='1')
    commands=[]
    def run(argv,phase,cwd=C):
        r=subprocess.run(list(map(str,argv)),cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
        commands.append({'phase':phase,'exit_code':r.returncode})
        print(phase,r.returncode,flush=True)
        if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    run([a.node,C/'upstream/scripts/probe_runtime.mjs','--runtime','pptxgenjs','--task-dir',PASS],'original-runtime-probe')
    run([a.node,'build.mjs','--overwrite'],'saved-additional-pass04-build',PASS)
    run([sys.executable,'upstream/scripts/check_pptx.py','complex-example/pass-04/editable.pptx','--source','complex-example/pass-04/source.png','--build-source','complex-example/pass-04/build.mjs','--require-single-slide','--slide','1','--output','complex-example/qa/replay-check.json'],'original-checker-without-pass-index-override')
    run([sys.executable,'source/check_complex_native.py','--output','complex-example/qa/replay-native-structure.json'],'saved-example-native-structure')
    if a.render:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        # Keep LibreOffice's temporary profile ancestry short on Windows.
        lo=C/'qa'/('c-lo-'+stamp)
        pp=C/'qa'/('c-pp-'+stamp)
        with tempfile.TemporaryDirectory(prefix='sci-render-') as temporary:
            rendered=Path(temporary)/'lo'
            run([sys.executable,'upstream/scripts/render_pptx.py',PASS/'editable.pptx','--output-dir',rendered,'--keep-pdf','--soffice',a.soffice,'--pdftoppm',a.pdftoppm],'original-isolated-libreoffice-render')
            shutil.copytree(rendered,lo)
        run(['pwsh','-NoProfile','-File','source/render_powerpoint.ps1','-PresentationPath',PASS/'editable.pptx','-OutputDirectory',pp],'powerpoint-pdf-export')
        run([a.pdftoppm,'-png','-scale-to-x','1600','-scale-to-y','-1','-singlefile',pp/'deck.pdf',pp/'slide-01'],'powerpoint-pdf-png')
    report={'status':'checks_executed_new_output_requires_visual_review','source':'complex-example/pass-04/source.png',
            'source_sha256':sha(PASS/'source.png'),'build_sha256':sha(PASS/'build.mjs'),
            'pptx_sha256':sha(PASS/'editable.pptx'),'commands':commands,
            'new_authored_pass':False,'saved_authored_pass_index':4,
            'original_default_authoring_pass_budget':2,'original_checker_pass_index_argument':None,
            'additional_author_pass_basis':'Explicit continued-refinement request; replay executes the saved pass04 without authoring another pass',
            'local_adapter':'Self-contained bounded STORE ZIP rewrite inside pass-04/build.mjs; no Python arrow helper',
            'exact_handoff_files':['build.mjs','source.png','editable.pptx'],
            'fresh_install_executed':False,
            'prior_visual_or_independent_review_transferred':False}
    (C/'complex-example/qa/reproduction.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
