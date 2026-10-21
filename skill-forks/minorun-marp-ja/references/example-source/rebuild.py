from pathlib import Path
import argparse,subprocess,sys,os,json,re
C=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--marp',required=True);a.add_argument('--node',default='node');a.add_argument('--browser',required=True);v=a.parse_args()
commands=[[sys.executable,C/'source/upstream/tools/check-ai-smell.py',C/'deck.md','--all']]
for flags,name in [([], 'index.html'),(['--pdf'],'deck.pdf'),(['--images','png','--image-scale','1'],'render/compiler.png')]:
 commands.append([v.node,v.marp,'--no-stdin',C/'deck.md','--html','--theme',C/'minorun-dark.css','--allow-local-files','--browser-path',v.browser,*flags,'-o',C/name])
results=[]
for cmd in commands:
 r=subprocess.run(list(map(str,cmd)),cwd=C,capture_output=True,text=True,encoding='utf8',errors='replace');results.append({'argv':list(map(str,cmd)),'exit_code':r.returncode,'output':r.stdout+r.stderr})
 if r.returncode:break
(C/'source/rebuild-receipt.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf8')
if any(r['exit_code'] for r in results):raise SystemExit(1)
html=(C/'index.html').read_text('utf8');html=re.sub(r'<html lang="[^"]*"','<html lang="ja"',html);html=html.replace('lang="C"','lang="ja"');html=html.replace('</body>','<script>'+(C/'source/catalog-bridge.js').read_text('utf8')+'</script></body>');(C/'index.html').write_text(html,'utf8')
print('original check + Marp HTML/PDF/PNG complete; visual review required')
