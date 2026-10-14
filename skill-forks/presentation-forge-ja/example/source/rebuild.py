"""Rebuild with the original Presentation Forge engine and standard-library builder."""
from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/presentation-forge-showcase' if (ROOT/'examples').exists() else ROOT

def build():
    deck=CASE/'source/deck'
    # The upstream builder first pulls user edits back into the slide files.
    done=subprocess.run([sys.executable,'build.py'],cwd=deck,text=True,encoding='utf-8',capture_output=True)
    if done.returncode: raise RuntimeError(done.stdout+'\n'+done.stderr)
    if '!' in done.stderr or '!' in done.stdout: raise RuntimeError('Original build warning: '+done.stdout+done.stderr)
    output=(deck/'index.html').read_text(encoding='utf-8')
    notices={'repository':'thmsgo18/presentation-forge','commit':'8268d3433af89a2f86e773ed8c84bbd9dd441896',
        'MIT':(CASE/'source/upstream/LICENSE').read_text(encoding='utf-8'),
        'template_MIT':(CASE/'source/upstream/template/LICENSE').read_text(encoding='utf-8'),
        'icons_ISC_Feather_MIT':(deck/'engine/icons-LICENSE').read_text(encoding='utf-8'),
        'fonts_OFL':{p.parent.name:p.read_text(encoding='utf-8') for p in (deck/'themes/obsidian/fonts').glob('*/OFL.txt')}}
    inline=json.dumps(notices,ensure_ascii=False).replace('</','<'+chr(92)+'/')
    bridge=(CASE/'source/catalog-bridge.js').read_text(encoding='utf-8')
    # The original engine has '</body>' inside its audience-document string.
    # Insert only at the final actual document close, preserving those strings.
    head,tail=output.rsplit('</body>',1)
    output=head+'<script type="application/json" id="license-notices">'+inline+'</script>\n<script>'+bridge+'</script>\n</body>'+tail
    (CASE/'index.html').write_text(output,encoding='utf-8',newline='\n')
    receipt={'command':[sys.executable,'build.py'],'builder':'source/deck/build.py (unchanged upstream)',
             'returncode':done.returncode,'stdout':done.stdout,'stderr':done.stderr,'slide_count':6,
             'post_build':'Append local same-origin adapter and full MIT/ISC/OFL notices; engine remains unchanged.'}
    (CASE/'source/BUILD.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(done.stdout.strip())
    print('Bundled6 Japanese slides, original engine/theme blocks, local fonts and full license notices.')

if __name__=='__main__':build()
