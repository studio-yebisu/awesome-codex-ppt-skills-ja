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
 d=S/'decks/exhibit-ja';(d/'main.js').write_text('import { boot } from \'../../engine/index.js\';\nimport \'../../engine/engine.css\';\nimport moves from \'../../moves/index.js\';\nimport concept from \'../../concepts/rail/index.js\';\nimport \'../../concepts/rail/tokens.css\';\nimport \'../../concepts/rail/layout.css\';\nimport deck from \'./deck.yaml\';\nimport \'./japanese.css\';\n\n// Default to the first original stop before boot; survives the original font rebuild.\nconst query = new URLSearchParams(location.search);\nif (!query.has("stop") && !query.has("t")) { const u = new URL(location.href); u.searchParams.set("stop", "opening"); history.replaceState(null, "", u); }\nboot({\n  host: document.getElementById(\'app\'),\n  deck,\n  concept,\n  moves,\n  assetBase: new URL(\'./\', document.baseURI).href,\n  mode: import.meta.env.SCROLLINE_MODE,\n});\n',encoding='utf-8')
 (d/'index.html').write_text('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小さな展示を、ひらくまで</title></head><body><div id="app"></div><aside class="nav-help">スクロール / ← → で進む</aside><aside class="sample-label">架空の写真展・計画案</aside><script type="module" src="./main.js"></script></body></html>',encoding='utf-8')
 (d/'japanese.css').write_text('''.sl-concept-rail { --sl-font-display: "Yu Mincho", "Hiragino Mincho ProN", serif; --sl-font-text: "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif; --sl-font-mono: "Consolas", monospace; --sl-size-l: calc(var(--px) * 100 * 1px); }
.nav-help { position:fixed; top:18px; right:28px; font:16px "Yu Gothic",sans-serif; color:#555; z-index:40; pointer-events:none; }
.sample-label { position:fixed; bottom:18px; right:28px; font:16px "Yu Gothic",sans-serif; color:#555; z-index:40; pointer-events:none; }

/* Keep the now marker below the heading; show the rolling month once. */
.sl-concept-rail .sl-chronology__now{inset-block:32% 30%;height:auto}
.sl-concept-rail .sl-chronology__ghost,.sl-concept-rail .sl-chronology__date{display:none}
''',encoding='utf-8')
 (d/'japanese.css').write_text((d/'japanese.css').read_text(encoding='utf-8')+'\n/* Round4 authored rail: expand monthly geometry and label the persistent event points. */\n.sl-concept-rail [data-now]>.sl-chronology__track{width:calc(var(--sl-span) * 360 * var(--px) * 1px)}\n.sl-concept-rail [data-now]>.sl-chronology__track::after{background:repeating-linear-gradient(to right,var(--sl-fg) 0 calc(var(--rail-u) * 2),transparent calc(var(--rail-u) * 2) calc(var(--rail-u) * 360))}\n.sl-concept-rail .sl-chronology__date{display:block;font-size:calc(var(--rail-u) * 24)}\n.sl-concept-rail .sl-chronology__event::after{position:absolute;top:calc(100% + 76 * var(--rail-u));left:0;white-space:nowrap;font:calc(var(--rail-u) * 24) var(--sl-font-text);color:var(--sl-fg);content:""}\n.sl-concept-rail [data-beat="prepare"] .sl-chronology__event:nth-child(1)::after{content:"5月 / 企画"}\n.sl-concept-rail [data-beat="prepare"] .sl-chronology__event:nth-child(2)::after{content:"6月 / 会場"}\n.sl-concept-rail [data-beat="deliver"] .sl-chronology__event:nth-child(1)::after{content:"7月 / 案内"}\n.sl-concept-rail [data-beat="deliver"] .sl-chronology__event:nth-child(2)::after{content:"8月 / 当日"}\n.plan-route{position:fixed;bottom:10%;left:6.25%;right:6.25%;display:flex;justify-content:space-between;z-index:35;pointer-events:none;color:#373329;font:24px "Yu Gothic",sans-serif;letter-spacing:.02em}.plan-route span+span::before{content:"→";margin-right:34px;color:#6b6457}\n',encoding='utf-8')
 (d/'index.html').write_text((d/'index.html').read_text(encoding='utf-8').replace('</body>','<aside class="plan-route" aria-label="写真展の計画全体"><span>5月 企画</span><span>6月 会場</span><span>7月 案内</span><span>8月 当日</span></aside></body>'),encoding='utf-8')
 run([node,'tools/cli.mjs','plan','exhibit-ja'],'original-plan')
 env=dict(os.environ);env['SCROLLINE_DECK']='exhibit-ja';env['SCROLLINE_OUT']=str(P/'presentation')
 run([npm,'run','build'],'original-build',env)
 print(str(P))
if __name__=='__main__':main()
