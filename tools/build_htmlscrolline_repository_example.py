"""Build a Japanese rail deck with the actual Scrolline v2 engine and moves."""
from pathlib import Path
import json,shutil,subprocess,sys,hashlib,os
R=Path(__file__).resolve().parents[1];P=R/'examples/repositories/html-scrolline';U=R/'.build/actual-upstreams/gongnyang__awesome-html-scrolline-deck';S=P/'source/upstream'
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 for d in ['source','input','review','render']:(P/d).mkdir(parents=True,exist_ok=True)
 for name in ['engine','moves','concepts','tools','docs','plan','state']:
  shutil.copytree(U/name,S/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 for name in ['package.json','package-lock.json','.npmrc','vite.config.js','vitest.config.js','SKILL.md','README.md','LICENSE','ACQUISITION.json']:
  if (U/name).exists():shutil.copy2(U/name,S/name)
 shutil.copy2(U/'LICENSE',P/'LICENSE-UPSTREAM.txt')
 receipts=[]
 def run(argv,label,env=None,allow=(0,)):
  cmd=[str(a) for a in argv];r=subprocess.run(cmd,cwd=S,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');f=P/'review'/(label+'.log');f.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');receipts.append({'argv':cmd,'cwd':str(S),'exit_code':r.returncode,'log':f.relative_to(P).as_posix(),'log_sha256':hashlib.sha256(f.read_bytes()).hexdigest()});dump(P/'review/execution-receipts.json',receipts)
  if r.returncode not in allow:raise RuntimeError(r.stdout+'\n'+r.stderr)
  return r
 npm=shutil.which('npm.cmd') or shutil.which('npm');node=shutil.which('node')
 run([npm,'ci','--ignore-scripts'],'npm-ci')
 if not (S/'decks/exhibit-ja').exists():run([node,'tools/cli.mjs','new','exhibit-ja','--concept','rail'],'original-new')
 run([node,'tools/cli.mjs','moves','--family','rail'],'original-moves')
 deck={'id':'exhibit-ja','title':'小さな展示を、ひらくまで','lang':'en','concept':'rail','sample':True,'sources':[],'timing':{'unit':0.65,'hold':0.85,'overlap':0.15},'beats':[
 {'id':'opening','type':'text','text':'小さな展示を、 ひらくまで','lines':['小さな展示を、','ひらくまで'],'size':'l','place':{'slot':'center'},'enter':{'move':'line-mask-rise'},'exit':{'move':'engine:fade-out'}},
 {'id':'prepare','type':'chronology','label':'まず、企画と会場を決める','counter':'month','now':0.23,'ground':True,'tone':0,'scale':'time','axis':'x','events':[{'date':'2027-05','title':'企画を決める','note':'誰に、どんな写真を見てもらうか。'},{'date':'2027-06','title':'会場を確かめる','note':'広さ・展示方法・利用条件を確認。'}],'place':{'world':{'x':0,'y':0,'z':0,'s':1}},'enter':{'move':'rail-surface'},'steps':[{'name':'venue','move':'rail-advance','params':{'to':1}}],'link':{'move':'era-shift','params':{'duration':2.0}},'repeat':'intended'},
 {'id':'deliver','type':'chronology','label':'次に、案内と当日を整える','counter':'month','now':0.23,'ground':True,'tone':4,'scale':'time','axis':'x','events':[{'date':'2027-07','title':'案内を届ける','note':'日時・場所・問い合わせ先をそろえる。'},{'date':'2027-08','title':'当日を整える','note':'展示順・受付・撤収の担当を決める。'}],'place':{'world':{'x':0,'y':0,'z':0,'s':1}},'enter':{'move':'engine:none','at':0.15},'steps':[{'name':'opening-day','move':'rail-advance','params':{'to':1}}],'exit':{'move':'engine:fade-out'},'repeat':'intended'},
 {'id':'closing','type':'text','text':'次に決めるのは、 展示のテーマ。','lines':['次に決めるのは、','展示のテーマ。'],'size':'l','place':{'slot':'center'},'enter':{'move':'line-mask-rise'},'repeat':'intended'}]}
 # JSON is valid YAML and remains data-only input for the original Vite YAML plugin.
 dump(P/'input/data.json',deck);dump(S/'decks/exhibit-ja/deck.yaml',deck)
 d=S/'decks/exhibit-ja';(d/'main.js').write_text('import { boot } from \'../../engine/index.js\';\nimport \'../../engine/engine.css\';\nimport moves from \'../../moves/index.js\';\nimport concept from \'../../concepts/rail/index.js\';\nimport \'../../concepts/rail/tokens.css\';\nimport \'../../concepts/rail/layout.css\';\nimport deck from \'./deck.yaml\';\nimport \'./japanese.css\';\n\nboot({\n  host: document.getElementById(\'app\'),\n  deck,\n  concept,\n  moves,\n  assetBase: new URL(\'./\', document.baseURI).href,\n  mode: import.meta.env.SCROLLINE_MODE,\n}).then((session) => {\n  const query = new URLSearchParams(location.search);\n  if (session.driver && !query.has("stop") && !query.has("t")) session.driver.seek(session.map.stops[0].t, { immediate: true });\n});\n',encoding='utf-8')
 (d/'index.html').write_text('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小さな展示を、ひらくまで</title></head><body><div id="app"></div><aside class="nav-help">スクロール / ← → で進む</aside><aside class="sample-label">架空の写真展・計画案</aside><script type="module" src="./main.js"></script></body></html>',encoding='utf-8')
 (d/'japanese.css').write_text('''.sl-concept-rail { --sl-font-display: "Yu Mincho", "Hiragino Mincho ProN", serif; --sl-font-text: "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif; --sl-font-mono: "Consolas", monospace; --sl-size-l: calc(var(--px) * 100 * 1px); }
.nav-help { position:fixed; top:18px; right:28px; font:16px "Yu Gothic",sans-serif; color:#555; z-index:40; pointer-events:none; }
.sample-label { position:fixed; bottom:18px; right:28px; font:16px "Yu Gothic",sans-serif; color:#555; z-index:40; pointer-events:none; }
''',encoding='utf-8')
 run([node,'tools/cli.mjs','plan','exhibit-ja'],'original-plan')
 env=dict(os.environ);env['SCROLLINE_DECK']='exhibit-ja';env['SCROLLINE_OUT']=str(P/'presentation')
 run([npm,'run','build'],'original-build',env)
 print(str(P))
if __name__=='__main__':main()
