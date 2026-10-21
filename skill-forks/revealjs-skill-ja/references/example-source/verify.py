from pathlib import Path
import argparse,subprocess,sys,json,os,shutil
C=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--browser',required=True);a.add_argument('--node',default='node');v=a.parse_args();env=os.environ.copy();env['NODE_PATH']=str(C/'source/qa/node_modules');env['PUPPETEER_EXECUTABLE_PATH']=v.browser
(C/'render/decktape').mkdir(exist_ok=True,parents=True)
commands=[[v.node,C/'source/upstream/skills/revealjs/scripts/check-overflow.js','index.html'],[v.node,C/'source/qa/node_modules/decktape/decktape.js','reveal','--chrome-path',v.browser,'--size','1600x900','--screenshots','--screenshots-directory','render/decktape',(C/'index.html').as_uri(),'deck.pdf']]
receipts=[]
for i,cmd in enumerate(commands):
 r=subprocess.run(list(map(str,cmd)),cwd=C,env=env,capture_output=True,text=True,encoding='utf8',errors='replace');txt=r.stdout+r.stderr;(C/f'source/verify-{i+1}.txt').write_text(txt,'utf8');receipts.append({'argv':list(map(str,cmd)),'exit_code':r.returncode,'log':f'source/verify-{i+1}.txt'})
 if r.returncode or 'OVERFLOW:' in txt:break
(C/'source/verify-receipt.json').write_text(json.dumps(receipts,indent=2),'utf8')
if any(x['exit_code']for x in receipts) or len(receipts)!=2:raise SystemExit(1)
print('Original overflow + Decktape complete. Inspect all images before acceptance.')
