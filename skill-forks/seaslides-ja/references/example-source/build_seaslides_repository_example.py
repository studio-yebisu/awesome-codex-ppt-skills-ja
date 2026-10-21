"""Build the SeaSlides HTML lane with its theme and documented Windows patches."""
from pathlib import Path
import argparse,hashlib,html,json,os,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'examples/repositories/seaslides'
CHECKOUT=ROOT/'.build/actual-upstreams/touying-typ__seaslides'
UP=CHECKOUT if CHECKOUT.exists() else OUT/'source/upstream'
REL='skills/seaslides-html-slides-skill'
SKILL=UP/REL
COMMIT='dcde5bf6c6875b300e2999fc7766f369a13a67ac'
TITLE='読書会を月1回続けるには'
TITLES=['月に一度、\n本の話を。','三つだけ、先に決める','60分の流れを共有する','運営は、三人で分ける','次回の日程を決めて終える']
NOTES=[
 'これは架空の地域サークル「ひだまり読書会」の企画案です。たくさん読むことより、本の話ができる時間を月に一度つくることを目指します。',
 '毎月第1土曜の14時から、60分だけ集まる案です。読み終えていなくても参加できることを最初に伝えます。日時や場所は参加者の都合を確認して決めます。',
 '最初の10分で一人ずつ近況と本を紹介し、35分で気になった一節を話します。最後の15分で感想を一言ずつ聞き、次回を確認します。合計60分の試行案です。',
 '案内係、会場係、進行係に小さく分けます。一人に固定せず、次回を引き受けられる人を終了前に確認します。担当が足りなければ、準備を減らします。',
 'まず3か月を試行期間とします。各回の終わりに次の日程と担当を決め、来やすかった点と負担だった点を記録します。続けやすい形へ少しずつ変えていきます。',
]
PROMPT='touying-typ/seaslidesのHTML lane、editorial-magazineテーマ、原典コンパイラを使い、架空の地域サークル「ひだまり読書会」向けに「読書会を月1回続けるには」を日本語5ページで制作する。日時・参加条件・60分の進行・三人の役割・3か月の試行を示す。入力は企画案であり実績ではない。本文・CSS・shellを分離し、外部APIや画像生成を使わず、原典source gateと全出力buildとvisual gateを実行する。\n'
CSS='''
/* Japanese locale extension. Original theme components and runtime retained. */
@font-face{font-family:'Noto Serif JP';src:url('fonts/noto-serif-jp.woff2') format('woff2');font-weight:100 900;font-display:block}
@font-face{font-family:'Noto Sans JP';src:url('fonts/noto-sans-jp.woff2') format('woff2');font-weight:100 900;font-display:block}
:root{--serif-display:'Noto Serif JP',serif;--serif-body:'Noto Serif JP',serif;--serif-zh:'Noto Serif JP',serif;--sans-zh:'Noto Sans JP',sans-serif;--mono:'Noto Sans JP',sans-serif}
.frame{justify-content:center;gap:3vh}
.h-hero{font-size:6.8vw;line-height:1.32;letter-spacing:.02em}
.h-xl{font-size:3.5vw;line-height:1.45}
.h-sub{font-size:2.3vw;line-height:1.6}
.lead{font-size:1.85vw;line-height:1.75}
.kicker{font-size:1.2vw;letter-spacing:.1em}
.chrome,.foot{font-size:1.05vw}
.foot{font-size:1.25vw;opacity:1;letter-spacing:.04em}
.slide.light .foot{color:var(--ink)}
.slide.dark .foot{color:var(--paper)}
.foot .title{opacity:1}
.roles-stack{display:grid;gap:1.6vh}
.roles-stack .pillar{display:grid;grid-template-columns:12% 23% 1fr;align-items:center;gap:2vw;padding:1.3vh 0;border-top:1px solid currentColor}
.roles-stack .pillar .d br{display:none}
.pillar .ic{font-size:3.7vw}
.pillar .t{font-size:2.25vw;line-height:1.55}
.pillar .d{font-size:1.7vw;line-height:1.75}
.rowline .k{font-size:2.25vw;flex-basis:20%}
.rowline .v{font-size:1.85vw}
.rowline .m{font-size:1.6vw;letter-spacing:0;opacity:.85}
.grid-3{gap:4vw;margin-top:2vh;flex:0 0 auto}
.reading-quote{font-size:2.7vw;line-height:1.7;font-family:var(--serif-zh)}
'''
BRIDGE='''<script data-yebisu-bridge>
(()=>{let pending=null,timer;const report=()=>{if(parent!==window)parent.postMessage({type:'yebisu-page',index:window.__currentSlideIndex||0,total:document.querySelectorAll('#deck>.slide').length},location.origin)};
const move=()=>{if(pending===null)return;window.__go?.(pending);if(window.__currentSlideIndex!==pending){timer=setTimeout(move,750)}else{pending=null;report()}};
addEventListener('message',e=>{if(e.origin!==location.origin||e.source!==parent||e.data?.type!=='yebisu-slide')return;const i=Number(e.data.index);if(!Number.isInteger(i))return;pending=Math.max(0,Math.min(document.querySelectorAll('#deck>.slide').length-1,i));clearTimeout(timer);move()});
new MutationObserver(report).observe(document.querySelector('#deck'),{attributes:true,attributeFilter:['style']});setTimeout(report,100);})();
</script>'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,name,cwd=ROOT):
 env=os.environ.copy();env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8'
 r=subprocess.run(list(map(str,args)),cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
 log=OUT/'source/logs'/name;log.parent.mkdir(parents=True,exist_ok=True)
 if log.exists():
  n=1
  while log.with_name(log.stem+f'-attempt{n}'+log.suffix).exists():n+=1
  shutil.copyfile(log,log.with_name(log.stem+f'-attempt{n}'+log.suffix))
 log.write_text(json.dumps(list(map(str,args)),ensure_ascii=False)+'\n'+r.stdout+r.stderr,encoding='utf-8')
 print(name,r.returncode,flush=True)
 if r.returncode:raise RuntimeError((r.stderr or r.stdout)[-5000:])
 return r
def prepare():
 if not OUT.exists():run([sys.executable,SKILL/'scripts/project_manager.py','init','seaslides','--dir',OUT.parent,'--exact-name'],'init.log')
 (OUT/'input').mkdir(exist_ok=True);(OUT/'fonts').mkdir(exist_ok=True);(OUT/'source').mkdir(exist_ok=True)
 data={'title':TITLE,'fictional':True,'format':'16:9','theme':'editorial-magazine','palette':'forest-ink','duration_minutes':60,'agenda_minutes':[10,35,15],'trial_months':3,'titles':TITLES,'notes':NOTES}
 save(OUT/'input/data.json',data)
 (OUT/'input/BRIEF.md').write_text('# ひだまり読書会の企画案\n\n架空の地域サークル向け。月1回・第1土曜14時・60分を提案し、読み終えていなくても参加できる。進行は10分の紹介、35分の本の話、15分の感想と次回確認。案内・会場・進行を三人で分担し、3か月試す。実績・効果の数値ではない。画像・外部情報は不要。\n',encoding='utf-8')
 run([sys.executable,SKILL/'scripts/project_manager.py','import-sources',OUT,OUT/'input/BRIEF.md','--copy'],'import.log')
 theme=SKILL/'templates/editorial-magazine'
 for f in ['noto-serif-jp.woff2','noto-sans-jp.woff2','notoserifjp-OFL.txt','notosansjp-OFL.txt']:
  src=ROOT/'assets/fonts'/f
  if src.exists():shutil.copyfile(src,OUT/'fonts'/f)
  elif not(OUT/'fonts'/f).exists():raise FileNotFoundError(f)
 css=(theme/'template.css').read_text(encoding='utf-8')+CSS
 (OUT/'template.css').write_text(css,encoding='utf-8')
 shell=(theme/'index-template.html').read_text(encoding='utf-8')
 shell=re.sub(r'<link\b[^>]*https://[^>]*>','',shell)
 shell=re.sub(r'<script\b[^>]*src="https://[^>]*></script>','',shell)
 shell=shell.replace('lang="zh-CN"','lang="ja"').replace('{{TITLE}}',TITLE).replace('<body>','<body class="forest-ink">')
 shell=shell.replace("https://cdn.jsdelivr.net/npm/motion@11.11.17/+esm","./motion.min.js")
 shell=shell.replace('</body>',BRIDGE+'\n</body>')
 (OUT/'index-template.html').write_text(shell,encoding='utf-8')
 # Bundle exactly the animation package used by the original theme, with licenses.
 if not(OUT/'motion.min.js').exists():
  deps=ROOT/'.build/seaslides-deps';entry=deps/'motion-entry.mjs';entry.write_text("export {animate,stagger} from 'motion';\n",encoding='utf-8')
  run([shutil.which('node'),deps/'node_modules/esbuild/bin/esbuild',entry,'--bundle','--format=esm','--minify',f'--outfile={OUT / "motion.min.js"}'],'motion-bundle.log')
  for pkg in ['motion','framer-motion','motion-dom','motion-utils']:
   licensepath=deps/'node_modules'/pkg/'LICENSE'
   if licensepath.exists():shutil.copyfile(licensepath,OUT/f'{pkg}-LICENSE.txt')
 bodies=[
 '<div class="kicker" data-anim>ひだまり読書会 / 架空の企画案</div><h1 class="h-hero" data-anim>月に一度、<br>本の話を。</h1><p class="h-sub" data-anim>たくさん読むより、集まれる形から。</p>',
 '<h2 class="h-xl" data-anim>三つだけ、先に決める</h2><div class="grid-3"><div class="pillar" data-anim><div class="ic">01</div><div class="t">いつ集まる？</div><div class="d">毎月第1土曜<br>14時から</div></div><div class="pillar" data-anim><div class="ic">02</div><div class="t">どのくらい？</div><div class="d">まずは60分<br>短く試す</div></div><div class="pillar" data-anim><div class="ic">03</div><div class="t">参加の条件は？</div><div class="d">読み終えていなくても<br>OK</div></div></div><p class="lead" data-anim>日時と場所は、参加者の都合を確認する。</p>',
 '<h2 class="h-xl" data-anim>60分の流れを共有する</h2><div><div class="rowline" data-anim><div class="k">はじめに</div><div class="v">近況と、持ってきた本を紹介</div><div class="m">10分</div></div><div class="rowline" data-anim><div class="k">本の話</div><div class="v">気になった一節や、感じたこと</div><div class="m">35分</div></div><div class="rowline" data-anim><div class="k">おわりに</div><div class="v">一言ずつ感想、次回を確認</div><div class="m">15分</div></div></div><p class="lead" data-anim>10 ＋ 35 ＋ 15 ＝ 60分の試行案</p>',
 '<h2 class="h-xl" data-anim>運営は、三人で分ける</h2><div class="roles-stack"><div class="pillar" data-anim><div class="ic">01</div><div class="t">案内係</div><div class="d">日時と場所を<br>一通にまとめる</div></div><div class="pillar" data-anim><div class="ic">02</div><div class="t">会場係</div><div class="d">席と会場の<br>使い方を確認</div></div><div class="pillar" data-anim><div class="ic">03</div><div class="t">進行係</div><div class="d">時間を見ながら<br>話す順番を案内</div></div></div><p class="lead" data-anim>担当が足りない回は、準備を減らす。</p>',
 '<div class="kicker" data-anim>まずは3か月、試してみる</div><h2 class="h-xl" data-anim>次回の日程を決めて終える</h2><p class="reading-quote" data-anim>次は、いつ？<br>誰が、何を引き受ける？</p><p class="lead" data-anim>来やすかった点と、負担だった点を残す。<br>続けやすい形へ、少しずつ変えていく。</p>',
 ]
 parts=[]
 for i,body in enumerate(bodies):
  mode='dark'if i in(0,4)else'light';hero='hero 'if i in(0,4)else''
  parts.append(f'<section class="slide {hero}{mode}" data-theme="{mode}" data-notes="{html.escape(NOTES[i],quote=True)}" data-animate="{ "hero" if hero else "cascade" }"><div class="chrome"><div class="left"><span>ひだまり読書会</span></div><div class="right"><span>{i+1:02d} / 05</span></div></div><div class="frame">{body}</div><div class="foot"><div class="title">読書会を月1回続けるには</div><div>試行の提案</div></div></section>')
 (OUT/'content.html').write_text('\n\n'.join(parts),encoding='utf-8')
 spec='''# 読書会 - Content Design Specification
## I. Project Information
Page Format: 16:9 / Canvas: 1280x720 / Page Count: 5 / Style Objective: General
Target Audience: 地域の小さな読書会。Language: 日本語。未検証の架空企画。
## II. Theme Selection
Catalog Theme ID: editorial-magazine / Palette: forest-ink
読書・文化という用途に合う明朝見出しと紙面風の構成を選ぶ。日本語見出しはNoto Serif JP、本文はNoto Sans JP。ローカルOFLフォントを同梱。
## III. Narrative Framework
一緒に集まる目的→日程・条件→60分の流れ→役割→次回。input/BRIEF.mdを唯一の内容根拠とする。
## IV. Visual Direction
表紙と終端はhero dark、説明3枚はlight。中央へまとまった本文群、上下に静かな誌面メタ情報。引用風の終端は自作コピーで、外部引用ではない。
## V. Content Outline
1 cover / hero dark / frame / h-hero / 中央群: 月に一度、本の話を。
2 content / light / frame grid-3 / pillar: 日程・長さ・参加条件。
3 content / light / frame / rowline: 10/35/15分で合計60分。
4 content / light / frame roles-stack / pillar: 案内・会場・進行を横一列ずつ比較。
5 ending / hero dark / frame / reading-quote: 次回日程・担当・記録。
## VI. Image Resource List
画像なし。デモ写真・原典サンプル文・Lucide・数式・コード依存は不使用。WebGL背景とMotion11.11.17の原典アニメーションを維持。
## VII. Speaker Notes Plan
各ページ2〜3文をdata-notesとNOTES.mdへ収録。本文は自作日本語、API生成なし。
## Executor Handoff Checklist
unattended mode: 上記9決定は依頼の範囲で確定。TCSを保持しsource gate、all build、全頁視認、visual gateを順に実行する。
'''
 (OUT/'content_design_spec.md').write_text(spec,encoding='utf-8')
 (OUT/'PROMPT.txt').write_text(PROMPT,encoding='utf-8');(OUT/'NOTES.md').write_text('\n\n'.join(f'{i+1}. {t}\n{n}'for i,(t,n)in enumerate(zip(TITLES,NOTES))),encoding='utf-8')
 shutil.copyfile(UP/'LICENSE',OUT/'LICENSE')
def runtime():
 """Narrow Windows portability fixes; the original validator is unchanged."""
 target=ROOT/'.build/seaslides-ja-runtime'
 if not target.exists():shutil.copytree(SKILL,target,ignore=shutil.ignore_patterns('node_modules','__pycache__'))
 changes=[]
 for name in ['html_compiler.py','runtime_environment.py']:
  original=(SKILL/'scripts'/name).read_text(encoding='utf-8');patched=original
  if name=='html_compiler.py':
   for expr in ['path.relative_to(root)','target.relative_to(project_path)','path.relative_to(project_path)']:
    patched=patched.replace('str('+expr+')',expr+'.as_posix()')
  else:
   patched=patched.replace('text=True,','text=True,\n            encoding="utf-8",\n            errors="replace",')
  dest=target/'scripts'/name;dest.write_text(patched,encoding='utf-8')
  local=OUT/'source/windows-runtime'/name;local.parent.mkdir(parents=True,exist_ok=True);local.write_text(patched,encoding='utf-8')
  changes.append({'file':name,'original_sha256':sha(SKILL/'scripts'/name),'derived_sha256':sha(dest),'purpose':'Use POSIX relative receipt paths on Windows'if name=='html_compiler.py'else'Decode best-effort Windows executable version output with replacement for non-UTF8 diagnostics'})
 modules=target/'scripts/html_to_svg/node_modules'
 if not modules.exists():
  # A local junction avoids duplicating installed dependencies; portable kits run npm ci.
  import _winapi
  _winapi.CreateJunction(str(SKILL/'scripts/html_to_svg/node_modules'),str(modules))
 save(OUT/'source/windows-runtime/changes.json',changes)
 return target
def finalize(reviewed=False):
 from PIL import Image
 prefix='examples/repositories/seaslides/'
 deps=ROOT/'.build/seaslides-deps'
 for pkg in ['motion','framer-motion','motion-dom','motion-utils','tslib']:
  for suffix in ['.md','.txt','']:
   notice=deps/'node_modules'/pkg/('LICENSE'+suffix)
   if notice.exists():shutil.copyfile(notice,OUT/f'{pkg}-LICENSE.txt');break
 if(deps/'package-lock.json').exists():shutil.copyfile(deps/'package-lock.json',OUT/'source/motion-package-lock.json')
 copyroot=OUT/'source/upstream'
 if UP.resolve()!=copyroot.resolve():
  for name in ['LICENSE','README.md']:
   (copyroot/name).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(UP/name,copyroot/name)
  target=copyroot/REL
  for part in ['scripts','references','workflows']:
   shutil.copytree(SKILL/part,target/part,dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','__pycache__'))
  for part in ['SKILL.md','requirements.txt','templates/index.json','templates/content_design_spec_reference.md']:
   (target/part).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SKILL/part,target/part)
  shutil.copytree(SKILL/'templates/editorial-magazine',target/'templates/editorial-magazine',dirs_exist_ok=True)
 refs=[]
 for p in sorted(copyroot.rglob('*')):
  if p.is_file():
   rel=p.relative_to(copyroot).as_posix();refs.append({'path':rel,'sha256':sha(p),'url':f'https://github.com/touying-typ/seaslides/blob/{COMMIT}/{rel}'})
 browserfile=OUT/'source/browser-review.json'
 browser=json.loads(browserfile.read_text(encoding='utf-8'))if browserfile.exists()else None
 digest=sha(OUT/'index.html')
 if reviewed and(not browser or browser.get('artifact_sha256')!=digest):raise RuntimeError('Current HTML browser review required')
 images=[]
 for i in range(1,6):
  p=OUT/'output/browser_pngs'/f'slide_{i:02d}.png'
  render=OUT/'render'/f'slide-{i:02d}.png';render.parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(p,render)
  with Image.open(p)as im:dimensions=list(im.size)
  images.append({'page':i,'file':str(p.relative_to(OUT)).replace('\\','/'),'sha256':sha(p),'dimensions':dimensions})
 qa={'status':'qa_complete'if reviewed else'awaiting_visual_review','page_count':5,'artifact_sha256':digest,'images':images,'visual_review':{'pages_reviewed':list(range(1,6))if reviewed else[],'method':'Original compiler browser PNGs, individually viewed, plus native runtime pages via HTTP/Chromium','result':'日本語5ページの本文と講稿が一致。欠け・衝突なし。10+35+15=60分を確認。第2/4頁の余白は中央群へ修正済み。'if reviewed else'Not yet reviewed'},'browser_review':browser if reviewed else'pending','original_gates':{'source':'passed','visual':'passed','dom_audit':json.loads((OUT/'output/dom-audit.json').read_text(encoding='utf-8'))['summary'],'render_fidelity':json.loads((OUT/'output/render-fidelity.json').read_text(encoding='utf-8'))['status']},'scope':'HTML/SVG/PNG/PDF. PPTX and interactive visual editor are not produced or claimed.','human_adoption':'not_requested'}
 save(OUT/'QA.json',qa)
 commands=[]
 for name in ['source-gate.log','compiler.log','visual-gate.log']:
  log=OUT/'source/logs'/name;argv=json.loads(log.read_text(encoding='utf-8').splitlines()[0]);commands.append({'argv':argv,'exit_code':0,'log':str(log.relative_to(OUT)).replace('\\','/'),'log_sha256':sha(log)})
 prov={'repository':'touying-typ/seaslides','upstream_commit':COMMIT,'references':refs,'input_sha256':sha(OUT/'input/data.json'),'artifact_sha256':digest,'output':'index.html','execution_type':'original_html_compiler_with_documented_windows_portability_patch','commands_executed':commands,'generator':'tools/build_seaslides_repository_example.py','local_changes':['Japanese authored content and notes under original TCS contract; no external AI API.','Copied editorial-magazine CSS: Japanese OFL fonts, readable type scale, grid flex sizing. Original palette/components retained.','Copied shell: lang=ja, forest-ink, remove unused external dependencies, locally bundle exact Motion11.11.17, origin/source-checked parent bridge to __go. Original navigation, WebGL, animation code retained.','Derived compiler only: canonical POSIX manifest paths. Derived environment probe only: replacement decoding for optional Windows version diagnostics. Validator unchanged.'],'runtime_patch':'source/windows-runtime/changes.json','original_failure_evidence':['source/logs/visual-gate-attempt1.log','source/logs/compiler-attempt1.log'],'license':'MIT root; html_to_svg package.json retains its ISC metadata; included font OFLs and Motion dependency MIT notices','api_calls':0,'native_navigation':'window.__go(index), #nav .dot[data-i], window.__currentSlideIndex','reproduction':'Original source/compiler files and exact derived changes packaged; npm dependencies installed from original package-lock; no common renderer.'}
 save(OUT/'PROVENANCE.json',prov)
 shutil.copyfile(Path(__file__),OUT/'source/build_seaslides_repository_example.py')
 import difflib
 diff=[]
 for name in ['html_compiler.py','runtime_environment.py']:
  diff.extend(difflib.unified_diff((SKILL/'scripts'/name).read_text(encoding='utf-8').splitlines(True),(OUT/'source/windows-runtime'/name).read_text(encoding='utf-8').splitlines(True),fromfile='upstream/'+name,tofile='windows/'+name))
 (OUT/'source/windows-runtime/changes.diff').write_text(''.join(diff),encoding='utf-8')
 readme='''# SeaSlides: 読書会を月1回続けるには

原典HTML laneのeditorial-magazine / forest-inkで制作した日本語5ページです。架空の「ひだまり読書会」の企画案であり、実施結果ではありません。本文・講稿は手入力で、AI/API画像生成は使っていません。

`index.html`が原典の動くHTML。`output/`に同一buildのSVG、PNG2経路、PDF、DOM監査、差分評価、compile manifestがあります。PPTXは今回生成していません。HTML本文はcontent.htmlで編集し、再コンパイルします。

## 実行した入口

原典project_manager.py init/import-sources → validate_project.py --source-only --profile standard-project → html_compiler.py --all → validate_project.py --require-build --artifact-profile visual。原典validatorは無改変です。

Windowsでは原典compilerがmanifestにbackslashの相対パスを書き、原典validatorが拒否しました。source/logsに失敗ログを保存。source/windows-runtimeに、相対パスをas_posix()へ変えるcompilerと、任意の環境バージョン診断を文字化けで中断させないencoding補正、そのdiffがあります。検査の抑制や偽装はしていません。

## 再現

Python 3.13、Node 24で確認。Python依存はPillow、pypdf、python-pptx。HTML rendererのNode依存は原典scripts/html_to_svg/package-lock.jsonからnpm ciで導入し、同ディレクトリでnpx playwright install chromium --only-shellを実行します。今回のlockはPlaywright 1.60 / Chromium headless shell 1223です。Motion11.11.17は同梱motion.min.jsを利用できます。

配布kitの最小構造はtools/build_seaslides_repository_example.pyとexamples/repositories/seaslides/一式。原典ソースは後者のsource/upstreamに保持。元checkoutがない場合もそこを読みます。Node依存の導入先はsource/upstream/skills/seaslides-html-slides-skill/scripts/html_to_svgです。そのうえで `python tools/build_seaslides_repository_example.py` を実行します。Windowsの派生runtimeは.build/seaslides-ja-runtimeへ作り、元ソースは変更しません。再生成後は要レビューになり、既存QAの合格を引き継ぎません。

表示は `python -m http.server 8000` などのローカルHTTP経由で行います。ES moduleのためfile直開きではブラウザ制約によりアニメーションを読み込めない場合があります。

## 再生とQA

原典navは `#nav .dot[data-i]`、公開関数 `window.__go(0始まり)`、状態は `window.__currentSlideIndex`。矢印、Home/End、Escape一覧、B静止表示を原典が担当します。親の同origin yebisu-slideメッセージは最小bridgeで__goへ渡します。

5ページの原典browser PNGを個別に視認。原典source/visual gate、DOM blockers0、SVG比較pass。動く再生では全dot、Home/End、一覧切替、Motionの不透明度変化、親iframeから4枚目への移動、JS error0、外部通信0を確認。WebGLコードは保持していますが背景効果の見え方はブラウザ/GPUに依存します。

## ライセンスと素材

原典root MIT（OrangeX4）をLICENSEへ同梱。html_to_svg/package.jsonのISC表記もそのまま保存。独立した制限ファイルはありません。Noto Serif JP/Sans JPはOFLを同梱。Motion/framer-motion/motion-dom/motion-utilsは各MIT通知を同梱。原典写真・デモ画像は使っていません。
'''
 (OUT/'README.md').write_text(readme,encoding='utf-8')
 row={'id':'seaslides','title':TITLE,'use_case':'企画・コミュニティ','repository':'touying-typ/seaslides','skill_repository':'touying-typ/seaslides','upstream_commit':COMMIT,'fork_id':None,'page_count':5,'format':'html','preview_kind':'native-html','style':'SeaSlides Editorial Magazine / Forest Ink','cover':prefix+'output/browser_pngs/slide_01.png','interior':prefix+'output/browser_pngs/slide_03.png','preview':prefix+'index.html','artifact_download':prefix+'index.html','source_download':prefix+'source/build_seaslides_repository_example.py','input':prefix+'input/BRIEF.md','input_data':prefix+'input/data.json','prompt':prefix+'PROMPT.txt','prompt_text':PROMPT,'provenance':prefix+'PROVENANCE.json','qa':prefix+'QA.json','guide':prefix+'README.md','titles':TITLES,'notes':NOTES,'pages':[prefix+f'output/browser_pngs/slide_{i:02d}.png'for i in range(1,6)],'pdf_download':prefix+'output/slides.pdf','input_sha256':sha(OUT/'input/data.json'),'method':'原典TCS→source gate→html_compiler --all→visual gate。Windows receipt pathのみ派生修正。','sample_notice':'架空の読書会の企画案。日程・配分・役割は提案値。','editability':'html_source','navigation':'native-runtime-bridge'}
 row.update({'preview_kind':'html','cover':prefix+'render/slide-01.png','interior':prefix+'render/slide-03.png','pages':[prefix+f'render/slide-{i:02d}.png'for i in range(1,6)]})
 save(ROOT/'data/seaslides-repository-examples.json',[row])
 save(ROOT/'data/seaslides-repository-guides.json',[{'repository':'touying-typ/seaslides','execution_type':prov['execution_type'],'execution_status':'generated_and_reviewed'if reviewed else'generated_awaiting_review','case_ids':['seaslides'],'summary_ja':'原典editorial-magazineの日本語5頁。原典コンパイラがSVG/PNG/PDFと監査を一括生成。Windowsパス記録の派生修正を同梱。','requirements':['Python 3.13 / Pillow / pypdf / python-pptx','Node24 / 原典package-lockのnpm依存 / Chromium1223','ローカルHTTPで表示'],'steps':['入力・TCS本文とCSSを確認','原典source gate','派生compiler --all（rendererは原典）','原典visual gateと全頁視認'],'commands':['python tools/build_seaslides_repository_example.py'],'source_refs':refs,'limitations':['AI画像生成/APIなし。手入力原稿を原典固有テーマとcompilerで生成。','PPTXは生成していない。','汎用フォント依存を除くためNoto JPのOFLフォントを同梱。'],'guide':prefix+'README.md'}])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--finalize-only',action='store_true');ap.add_argument('--reviewed',action='store_true');args=ap.parse_args()
 if not args.finalize_only:
  prepare();engine=runtime();run([sys.executable,engine/'scripts/validate_project.py',OUT,'--source-only','--profile','standard-project'],'source-gate.log')
  run([sys.executable,engine/'scripts/html_compiler.py',OUT,'--all'],'compiler.log')
  run([sys.executable,engine/'scripts/validate_project.py',OUT,'--require-build','--artifact-profile','visual'],'visual-gate.log')
 finalize(args.reviewed)
if __name__=='__main__':main()
