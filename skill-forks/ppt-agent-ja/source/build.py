"""Akxan original Bauhaus mock + HTML -> DOM/SVG -> native OOXML converter.
The original public runtime is preserved; only Windows/UTF8/cache adapters apply.
"""
from pathlib import Path
import argparse, difflib, hashlib, importlib.metadata, json, os, re, shutil, subprocess, sys, zipfile

SCRIPT=Path(__file__).resolve();ROOT=SCRIPT.parents[1]
CASE=ROOT/'examples/repositories/ppt-agent-showcase' if SCRIPT.parent.name=='tools' else SCRIPT.parent.parent
FORK=ROOT/'skill-forks/ppt-agent-ja'
PIN='01825dee2ad40a8c719824252605396b9a570d57';REPO='Akxan/ppt-agent-skill'
TITLES=['小さな展示を、ひとつの体験に。','作品・場所・言葉を、つなぐ','入口から、余韻まで。','準備は、四つの区切りで。','開く前に、一度だけ歩く。']
PROMPT='''日本語5枚の仮想展示企画「小さな展示を、ひとつの体験に。」を制作してください。
Akxan/ppt-agent-skillの26作風から実在するbauhaus_blockを選び、原典のmock/styleとHTML→dom-to-svg→svg2pptxのOSS生成器を実際に使う。
三原色の円・四角・三角、硬い版式、大きな和文タイトル、展示の関係図、来場導線、準備日程を少ない要素で見せる。
Zen Kaku Gothic New Blackの大見出し、BIZ UDPMinchoの短い説明、Manropeの英数字。角丸カードや無難な業務資料に揃えない。
全5枚は表紙、関係図、来場導線、準備日程、開く前の体験確認。展示は仮想、日時・会場・参加条件は未定、日程は相対的な仮案。
ユーザー指定の内部判断・軽い確認を優先し、追加インタビュー、全ページ目視、独立レビュー、構造監査、ZIP再実行は行わない。
実生成と代表完成物の初回表示まで進め、完成PPTX/PNG/PDFと原典Webプレビュー、入力/原稿/依頼/再生成コード、未変更原本/局所差分、字体許諾、日本語SKILL、SOURCE、2ZIPまで完成させる。
artifact-tool SDKを使わず、原典の許されるOSS経路で実行。別レンダラーへの名前貼りや黙った画像PPTX代替をしない。'''

def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

CSS=r'''
@font-face{font-family:'Zen Kaku Gothic New';src:url('../fonts/zenkakugothicnew/ZenKakuGothicNew-Black.ttf') format('truetype');font-weight:900}
@font-face{font-family:'BIZ UDPMincho';src:url('../fonts/bizudpmincho/BIZUDPMincho-Regular.ttf') format('truetype');font-weight:400}
@font-face{font-family:'Manrope';src:url('../fonts/manrope/Manrope[wght].ttf') format('truetype');font-weight:200 800}
:root{--display-font:'Zen Kaku Gothic New',sans-serif;--body-font:'BIZ UDPMincho',serif;--number-font:'Manrope',sans-serif;--paper:var(--bg)}
.jp-stage{width:1280px;height:720px;position:relative;overflow:hidden}
.jp-head{font-family:var(--display-font);font-weight:900;letter-spacing:-.04em;line-height:1.1;position:absolute;color:var(--ink)}
.jp-text{font-family:var(--body-font);font-size:28px;line-height:1.55;position:absolute;letter-spacing:0;color:var(--ink)}
.jp-num{font-family:var(--number-font);font-variant-numeric:tabular-nums;font-weight:800;letter-spacing:-.04em;position:absolute;color:var(--ink)}
.jp-foot{position:absolute;left:80px;top:666px;font:16px var(--body-font);color:var(--ink-soft)}
.jp-page{position:absolute;right:80px;top:654px;font:26px var(--number-font);font-weight:800;color:var(--ink)}
.jp-label{position:absolute;font-family:var(--display-font);font-weight:900;font-size:34px;color:var(--ink)}
.top-bar .left,.top-bar .right{font-family:var(--number-font);font-size:13px}
.native-svg{position:absolute;left:0;top:0;width:1280px;height:720px}
'''

def h(text,x,y,w,size=64):return f'<div class="jp-head" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px">{text}</div>'
def t(text,x,y,w,size=28,color='ink'):return f'<div class="jp-text" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;color:var(--{color})">{text}</div>'
def num(text,x,y,w,size=48):return f'<div class="jp-num" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px">{text}</div>'
def svg(body):return '<svg class="native-svg" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">'+body+'</svg>'
def rect(x,y,w,hh,c):return f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" fill="var(--{c})"/>'
def circle(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--{c})"/>'
def path(d,c,stroke=None,sw=2):return f'<path d="{d}" fill="var(--{c})"'+(f' stroke="var(--{stroke})" stroke-width="{sw}"' if stroke else '')+'/>'
def line(x1,y1,x2,y2,c='ink',sw=2):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var(--{c})" stroke-width="{sw}"/>'

def make_pages():
    # Sparse native geometry follows the original Bauhaus mock, not a generic grid.
    cover=svg(circle(1010,248,119,'red')+rect(834,402,225,225,'blue')+path('M1124 390 L1250 616 L998 616 Z','yellow'))
    cover+=h('小さな展示を、<br>ひとつの<br>体験に。',78,132,780,86)
    cover+=t('作品だけでなく、<br>出会い方もつくる。',86,516,650,30)
    relation=svg(rect(90,286,235,235,'blue')+circle(638,403,151,'red')+path('M1035 278 L1175 521 L895 521 Z','yellow')+line(325,403,487,403)+line(789,403,962,403))
    relation+=h('作品・場所・言葉を、つなぐ',80,116,1130,58)
    relation+=t('場所',144,360,180,43,'bg')+t('作品',591,361,190,43,'bg')+t('言葉',987,390,190,43)
    relation+=t('配置と案内が、作品との距離を決める。',85,584,1100,31)
    flow=svg(circle(172,327,66,'red')+rect(414,261,132,132,'blue')+circle(788,327,66,'red')+path('M1091 251 L1179 402 L1003 402 Z','yellow'))
    flow+=svg(line(238,327,398,327)+path('M388 315 L410 327 L388 339 Z','ink')+line(546,327,706,327)+path('M696 315 L718 327 L696 339 Z','ink')+line(854,327,986,327)+path('M976 315 L998 327 L976 339 Z','ink'))
    flow+=h('入口から、余韻まで。',80,110,1110,72)
    for x,n,a,b in [(74,'01','入口','ひとこと案内'),(382,'02','見る','作品を比べる'),(690,'03','話す','短い問いを置く'),(998,'04','持ち帰る','次の一歩を添える')]:
        flow+=num(n,x,425,210,35)+h(a,x,477,250,37)+t(b,x,545,250,24)
    schedule=svg(line(297,262,297,592,'ink',2))
    schedule+=h('準備は、四つの区切りで。',80,110,1120,65)
    for y,n,a,b,c in [(241,'-4W','作品とテーマ','展示する理由をひとつに絞る','red'),(333,'-3W','配置とことば','見せる順番と案内を合わせる','blue'),(425,'-1W','実物で通す','作品・照明・導線を並べて歩く','red'),(517,'DAY 0','小さく開く','反応を聞き、次の展示へ残す','yellow')]:
        schedule+=svg(rect(286,y+15,23,23,c))+num(n,78,y-4,210,47)+h(a,357,y-4,500,35)+t(b,357,y+43,720,24)
    schedule+=t('開場日から逆算した、相対的な準備案。',80,612,1080,22)
    ending=svg(rect(880,189,299,299,'yellow')+circle(969,492,97,'red')+rect(1090,405,118,185,'blue'))
    ending+=h('開く前に、<br>一度だけ歩く。',80,116,860,79)
    ending+=t('入口の言葉。<br>見る順番。<br>出口のひとこと。',86,394,710,36)
    return [cover,relation,flow,schedule,ending]

def prepare():
    up=ROOT/'.build/actual-upstreams/Akxan__ppt-agent-skill'
    files=['LICENSE','SKILL.md','references/styles/index.md','references/styles/vibrant.md','references/typography.md','references/pipeline-compat.md','references/layouts/asymmetric.md','references/page-templates/cover.md','ppt-output/style-gallery/bauhaus_block.html','scripts/html_packager.py','scripts/html2svg.py','scripts/svg2pptx.py']
    for rel in files:
        p=CASE/'upstream'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(up/rel,p)
    shutil.copy2(up/'LICENSE',CASE/'LICENSE')
    wanted={'zenkakugothicnew':['ZenKakuGothicNew-Black.ttf'],'bizudpmincho':['BIZUDPMincho-Regular.ttf'],'manrope':['Manrope[wght].ttf']}
    for family,fonts in wanted.items():
        for name in fonts+['OFL.txt']:
            dest=CASE/'fonts'/family/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'downloads/fonts'/family/name,dest)
    fontkit=json.loads((ROOT/'data/oss-font-kit.json').read_text(encoding='utf-8'))
    dump(CASE/'fonts/SOURCE.json',{'families':[f for f in fontkit['families'] if f['id'] in wanted],'used_files':wanted,'os_font_extraction':False,'modified':False})
    mock=(up/'ppt-output/style-gallery/bauhaus_block.html').read_text(encoding='utf-8')
    css=re.search(r'<style>(.*?)</style>',mock,re.S).group(1)
    original_css=css
    css=re.sub(r"(?m)^\s*@import[^\n]*\n",'',css)
    css+=CSS
    for i,body in enumerate(make_pages()):
        top=f'<div class="top-bar"><span class="left">EXHIBITION / CONCEPT</span><span class="right">BAUHAUS BLOCK / JA</span></div>'
        footer='<div class="jp-foot">仮想の展示企画 / 日時・会場・参加条件は未定</div>'+f'<div class="jp-page">{i+1:02}</div>'
        html=f'<!doctype html><html lang="ja"><meta charset="utf-8"><title>{TITLES[i]}</title><style>{css}</style><body><main class="jp-stage">{body}{top}{footer}</main></body></html>'
        write(CASE/'slides'/f'slide-{i+1:02}.html',html)
    write(CASE/'source/style.diff',''.join(difflib.unified_diff(original_css.splitlines(True),css.splitlines(True),fromfile='original bauhaus_block mock CSS',tofile='Japanese font and exhibition geometry adapter CSS')))
    styledata=(up/'references/styles/vibrant.md').read_text(encoding='utf-8')
    style=json.loads(re.search(r'```json\s*(\{\s*"style_id": "bauhaus_block".*?\})\s*```',styledata,re.S).group(1))
    dump(CASE/'input/style.json',style)
    dump(CASE/'input/requirements.json',{'title':TITLES[0],'type':'hypothetical exhibition concept','page_count':5,'style':'original bauhaus_block','image_mode':'native geometric shapes, no AI illustration','fonts':{'display':'Zen Kaku Gothic New Black','body':'BIZ UDPMincho','english_numbers':'Manrope'},'confirmed_by_user':'internal decisions, light generation verification, no new interview gates'})
    dump(CASE/'input/planning.json',{'pages':[{'page':i+1,'title':t,'page_type':p,'layout_hint':l,'content':c,'status':'hypothetical proposal'} for i,(t,p,l,c) in enumerate(zip(TITLES,['cover','content','content','content','end'],['asymmetric','single-focus','waterfall','primary-secondary','asymmetric'],['大きなタイトルと原典三原色の円・四角・三角','場所・作品・言葉を線でつなぐ関係図','入口、見る、話す、持ち帰るの4段階','開場4週前、3週前、1週前、当日の相対計画','開く前に来場導線を1回歩く企画案']))],'user_overrides':['No repeated card quotas','No forced interview/confirmation waits','No independent review/full page audit/ZIP replay']})
    write(CASE/'input/BRIEF.md','# 小さな展示を、ひとつの体験に。\n\n仮想の小規模展示。作品・場所・言葉をまとめて設計する5枚の企画資料。日時・会場・参加条件は未定。準備日程は開場日から逆算した相対案で実績ではない。赤丸は作品/対話、青い四角は場所/見る、黄色い三角は言葉/持ち帰るという概念の記号。\n')
    write(CASE/'PROMPT.md',PROMPT+'\n')
    write(CASE/'MANUSCRIPT.md','\n\n'.join(f'## {i+1}. {tt}\n\n'+desc for i,(tt,desc) in enumerate(zip(TITLES,['小さな展示は、作品を並べるだけではなく出会い方をつくる。','作品・場所・言葉を結び付け、配置と案内を同時に設計。','入口で短く案内、作品を見る、短い問いを話す、次の一歩を持ち帰る。','4週前に作品とテーマ、3週前に配置とことば、1週前に実物を並べて歩く。当日は小さく開く。相対的な仮の工程。','入口の言葉・見る順番・出口のひとことを開く前に確かめる。日時・会場・参加条件は未定。'])))+'\n')
    runtime=CASE/'runtime/scripts'
    for name in ['html_packager.py','html2svg.py','svg2pptx.py']:
        text=(up/'scripts'/name).read_text(encoding='utf-8');original=text
        if name=='html_packager.py':
            # Keep one local font kit instead of embedding the same fonts five times.
            text=text.replace("ext = img_path.suffix.lower().lstrip('.')", "ext = img_path.suffix.lower().lstrip('.')\n            if ext in ('ttf', 'otf', 'woff', 'woff2'):\n                font_ref = img_path.resolve().relative_to(html_dir.parent.resolve()).as_posix()\n                return f'{attr}{font_ref}{closing}'")
        if name=='html2svg.py':
            # Original script already imports os.
            text=text.replace("'file://' + item.html","require('url').pathToFileURL(item.html).href")
            text=text.replace('work_dir = Path(__file__).resolve().parent.parent','work_dir = Path(os.environ.get("PPT_AGENT_WORK_DIR", str(Path(__file__).resolve().parent.parent))).resolve()')
            text=text.replace('await page.addScriptTag({ path: config.bundlePath });','await page.evaluate(async () => { await document.fonts.ready; });\n        await page.addScriptTag({ path: config.bundlePath });')
            text=text.replace('return convert_pdf2svg(html_files, output_dir, work_dir)','raise RuntimeError("Original DOM-to-SVG route failed; fallback disabled for this example")')
        write(runtime/name,text)
        write(CASE/'source'/f'{name}.diff',''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='upstream/scripts/'+name,tofile='runtime/scripts/'+name)))
    source=CASE/'source';source.mkdir(exist_ok=True);shutil.copy2(SCRIPT,source/'build.py')
    render=(ROOT/'tools/render_powerpoint.ps1').read_text(encoding='utf-8').replace('if ($existingPowerPoint.Count -eq 0 -and $powerPoint.Presentations.Count -eq 0) { $powerPoint.Quit() }','# Shared PowerPoint: close this opened deck only. Application.Quit is prohibited.')
    write(source/'render_powerpoint.ps1',render)
    dump(CASE/'package.json',{'private':True,'dependencies':{'puppeteer':'25.13.0','dom-to-svg':'0.12.2','esbuild':'0.28.2'}})
    shutil.copy2(ROOT/'.build/ppt-agent-runtime/package-lock.json',CASE/'package-lock.json')
    write(CASE/'requirements.txt','python-pptx==1.0.2\nlxml==6.1.3\nPillow==12.3.0\n')
    for pname in ['python-pptx','lxml','Pillow']:
        dist=importlib.metadata.distribution(pname)
        for item in dist.files or []:
            if item.name.lower().startswith(('license','notice','copying')):
                p=Path(dist.locate_file(item))
                if p.is_file():dest=CASE/'dependencies'/pname/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    npmroot=ROOT/'.build/ppt-agent-runtime/node_modules'
    for meta in npmroot.rglob('package.json'):
        if meta.parent.name=='node_modules':continue
        try:j=json.loads(meta.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError):continue
        name=j.get('name',meta.parent.name).replace('/','__')
        for p in meta.parent.iterdir():
            if p.is_file() and p.name.lower().startswith(('license','notice','copying')):
                dest=CASE/'dependencies'/name/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)

def execute(node,chrome):
    deps=ROOT/'.build/ppt-agent-runtime/node_modules' if SCRIPT.parent.name=='tools' else CASE/'node_modules'
    work=ROOT/'.build/ppt-agent-renderer' if SCRIPT.parent.name=='tools' else CASE/'.build/ppt-agent-renderer'
    work.mkdir(parents=True,exist_ok=True)
    env={**os.environ,'NODE_PATH':str(deps),'PATH':str(Path(node).resolve().parent)+os.pathsep+os.environ.get('PATH',''),'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8','PUPPETEER_EXECUTABLE_PATH':str(Path(chrome).resolve()),'PPT_AGENT_WORK_DIR':str(work)}
    entry=work/'bundle-entry.js';bundle=work/'dom-to-svg.bundle.js'
    write(entry,"import { documentToSVG, elementToSVG, inlineResources } from 'dom-to-svg';\nwindow.__domToSvg = { documentToSVG, elementToSVG, inlineResources };\n")
    js='require("esbuild").buildSync('+json.dumps({'entryPoints':[str(entry)],'outfile':str(bundle),'bundle':True,'format':'iife','platform':'browser','nodePaths':[str(deps)]})+')'
    r=subprocess.run([str(node),'-e',js],env=env,cwd=CASE,capture_output=True,text=True,encoding='utf-8',errors='replace');write(CASE/'source/bundle.log',r.stdout+r.stderr)
    if r.returncode:raise RuntimeError('Original dom-to-svg bundle build: '+r.stderr)
    commands=[('package',[sys.executable,str(CASE/'runtime/scripts/html_packager.py'),str(CASE/'slides'),'-o',str(CASE/'preview.html'),'--title',TITLES[0]]),('dom-svg',[sys.executable,str(CASE/'runtime/scripts/html2svg.py'),str(CASE/'slides'),'-o',str(CASE/'svg')]),('native-pptx',[sys.executable,str(CASE/'runtime/scripts/svg2pptx.py'),str(CASE/'svg'),'-o',str(CASE/'deck.pptx'),'--html-dir',str(CASE/'slides')])]
    steps={}
    for name,cmd in commands:
        r=subprocess.run(cmd,cwd=CASE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');write(CASE/'source'/f'{name}.log',r.stdout+r.stderr)
        steps[name]={'exit_code':r.returncode,'log':'source/'+name+'.log'}
        if r.returncode:raise RuntimeError(name+': '+(r.stdout+r.stderr)[-6000:])
    dump(CASE/'source/BUILD.json',{'route':'original html_packager -> html2svg (dom-to-svg) -> svg2pptx native OOXML shape conversion','steps':steps,'bundle':'esbuild + original BUNDLE_ENTRY API','image_fallback_used':False,'artifact_tool_used':False,'slide_count_expected':5,'full_structure_audit':False})
    print('Original HTML/DOM/SVG/native-PPTX route succeeded for five Japanese pages.')

def finish():
    write(CASE/'README.md',f'''# 小さな展示を、ひとつの体験に。

仮想の展示企画5枚。日時・会場・参加条件は未定。4週前・3週前・1週前・当日は開場日から逆算した仮の工程で、実績ではありません。

## 原典を使った方法

[Akxan/ppt-agent-skill](https://github.com/Akxan/ppt-agent-skill/tree/{PIN}) / MIT / `{PIN}`。
26作風から実在する `bauhaus_block` を選択。原典 `ppt-output/style-gallery/bauhaus_block.html` のCSS、紙色・赤/青/黄・巨大sans・硬い幾何・厳格gridを使用し、日本語展示の本文と局所CSSを追加しました。元style.jsonは `input/style.json`。未変更原本は `upstream/`、局所差分は `source/*.diff`。

原典 `html_packager.py` でWebプレビューを作成し、`html2svg.py` のPuppeteer/dom-to-svg、`svg2pptx.py` のnative OOXML形状生成を実行。原典文書には「SVG画像を形状へ変換」の説明もありますが、このpinの実コードはSVGの文字・円・四角・線・pathをnative PowerPoint形状へ直接解析します。完成PPTXの文字と形状はそのまま編集できます。native chart/table/数式は使用していません。

Windowsのfile URL、UTF8、依存bundle/cache置き場、字体ロード待ちを局所adapterで対応。原典DOM routeに失敗したときのPDF/画像代替は無効化し、失敗を報告します。汎用レンダラーやartifact-tool SDKは使用していません。

Web packagerは、各ページへ同じ字体を5回base64化する代わりに同梱 `fonts/` へ相対参照する局所adapterを適用。`preview.html` はfontsフォルダと一緒に保持してください。画像素材の原典inline処理は保っています。

## 閲覧と編集

- `deck.pptx`：PowerPointで文字をクリックして編集。図形の色・大きさ・位置も編集可能。関連する部品は複数の形状として配置されています。
- `render/deck.pdf`、`render/slide-*.png`：PowerPoint16の実描画による閲覧用。
- `preview.html`：原典packagerによるブラウザの翻ページプレビュー。HTMLを編集する場合は `slides/slide-*.html` を使用。
- `svg/`：原典DOM-to-SVG出力。文字はtext要素を保ったvectorです。

見出しはZen Kaku Gothic New Black、短い本文はBIZ UDPMincho、英数字はManrope。公式未変更TTFとOFLを同梱。OS字体・Office字体の抽出はありません。PowerPoint表示用にこれらをWindowsへ登録してください（字体を右クリックしてインストール）。HTMLは同梱字体を参照します。

## 再生成

Node.js24以降、Python3.12、Chrome、PowerPoint16（PNG/PDF出力時）が必要です。依存・Chrome本体・bundle/cacheはZIPに含めません。

```powershell
$env:PUPPETEER_SKIP_DOWNLOAD='true'
npm install --ignore-scripts
python -m pip install -r requirements.txt
python source/build.py --node C:/path/to/node.exe --chrome 'C:/Program Files/Google/Chrome/Application/chrome.exe'
powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
```

原典のOSS生成器と未変更原本、差分、入力・依頼・原稿、字体許諾を同梱。Puppeteer/dom-to-svg/esbuildは各packageのMIT/Apache等を `dependencies/` に保存。Python依存の個別許諾も保持。共有PowerPoint ApplicationをQuitせず、自分が開いたdeckのみCloseします。

## 確認範囲

原典packager/DOM-to-SVG/native PPTXの成功、PowerPoint16で5枚PNG/PDF生成、代表完成物の初回表示まで。ユーザー指定により全ページ詳細目視、独立レビュー、構造監査、ZIP再実行は実施していません。今回は固定のカード数と追加interview/承認待ちを適用せず、計画を入力へ記録して制作しました。
''')
    write(CASE/'SKILL.md',f'''---
name: ppt-agent-ja
description: 原典Bauhaus BlockとHTML/DOM/SVG/native PowerPoint生成経路を使う日本語展示資料。
---

# 日本語PPT Agent

Akxan/ppt-agent-skill `{PIN}` / MIT。原典の26作風から実在するstyle/mockを読み、そのCSSと本文を日本語へ局所対応する。

1. input/requirements.json、planning.json、style.jsonへ企画と5枚構成を保存。今回はユーザーが内部判断と軽い確認を指定済み。必須interview/承認待ち、カード数の固定、追加reviewを適用しない。
2. `bauhaus_block` の三原色・巨大和文・硬い幾何・余白を保つ。本文は短い明朝、英数字はManrope。使用TTF/OFLのみを同梱し、OS字体を抽出しない。
3. 原典html_packager→html2svg(dom-to-svg/Puppeteer)→svg2pptx(native OOXML形状)を実行。WindowsfileURL/cache/字体待ちadapterはsourceの差分へ記録。原典DOM失敗時に別方式へ黙って替えない。
4. このpinのconverterはSVG文字・rect/circle/line/pathをnative形状にする。編集範囲はtext/shapesと説明し、native chart/table/数式を称しない。
5. PowerPoint16で完成PPTXのPNG/PDFを描画。Application.Quitは禁止、自deckだけClose。確認は生成成功と代表完成物初回表示まで。
6. .pptx本体、Web preview、HTML/SVG、入力/依頼/原稿、原典/差分/license/font/短いQAを渡す。backendや重いcacheをZIPへ入れない。全ページ詳細目視・独立review・構造監査・ZIP再実行を追加しない。

## quick_validate

`python source/build.py --node C:/path/to/node.exe --chrome C:/path/to/chrome.exe` の成功後、完成PPTXをPowerPointで代表1ページ表示。日本語欠けや明白な生成欠損があれば局所修正する。
''')
    for directory in ['upstream','runtime','source','fonts','dependencies','input','slides']:
        shutil.copytree(CASE/directory,FORK/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.log','__pycache__','*.pyc'))
    for name in ['SKILL.md','README.md','LICENSE','PROMPT.md','MANUSCRIPT.md','package.json','package-lock.json','requirements.txt']:shutil.copy2(CASE/name,FORK/name)
    source={'repository':REPO,'commit':PIN,'license':'MIT','modified':True,'used_style':'bauhaus_block','original_template':'upstream/ppt-output/style-gallery/bauhaus_block.html','route':'original html_packager -> html2svg dom-to-svg -> svg2pptx native OOXML shapes','local_changes':['Japanese exhibition manuscript','CSS font/geometry adapter','Windows file URL / font ready / private deps cache','DOM route failure does not fallback','User-selected minimal workflow replaces interview/card quotas/full audit'],'editable_features':['text','shapes'],'images_used':False,'artifact_tool_used':False,'example':'examples/repositories/ppt-agent-showcase'}
    dump(CASE/'SOURCE.json',source);dump(FORK/'SOURCE.json',source)
    dump(CASE/'PROVENANCE.json',{'repository':REPO,'upstream_commit':PIN,'license':'MIT','method':source['route'],'style':'Original Bauhaus Block HTML mock CSS + Japanese localized fonts/content','originals':{p.relative_to(CASE).as_posix():sha(p) for p in (CASE/'upstream').rglob('*') if p.is_file()},'changes':'source/*.diff','font_sources':'fonts/SOURCE.json','font_files':{p.relative_to(CASE).as_posix():sha(p) for p in (CASE/'fonts').rglob('*.ttf')},'dependency_notices':'dependencies/','package_versions':{'puppeteer':'25.13.0','dom-to-svg':'0.12.2','esbuild':'0.28.2','python-pptx':'1.0.2','lxml':'6.1.3','Pillow':'12.3.0'},'build':'source/BUILD.json','render':'render/powerpoint-render.json','content_status':'hypothetical exhibition concept; dates, venue, entry conditions undecided'})
    dump(CASE/'QA.json',{'status':'ready_for_first_display','original_route_success':True,'powerpoint_render_success':(CASE/'render/deck.pdf').exists(),'page_count':5,'editable_features':['text','shapes'],'representative_page_opened':False,'whole_deck_detailed_review':False,'independent_review':False,'structure_audit':False,'zip_reexecution':False,'review_mode':'user_requested_minimal','image_fallback_used':False})
    images=''.join(f'<figure><img src="render/slide-{i+1:02}.png" alt="{tt}"><figcaption>{i+1}. {tt}</figcaption></figure>' for i,tt in enumerate(TITLES))
    write(CASE/'index.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+TITLES[0]+'</title><style>body{margin:0;background:#f4f0e8;color:#1a1a1a;font-family:sans-serif}header,main{max-width:1280px;padding:28px;margin:auto}a{color:#003049}figure{margin:0 0 30px}img{display:block;width:100%}figcaption{padding-top:10px;font-size:14px}</style><header><h1>'+TITLES[0]+'</h1><p>仮想の展示企画 / Bauhaus Block / native text・shape PPTX</p><a href="deck.pptx">PowerPoint</a> · <a href="render/deck.pdf">PDF</a> · <a href="preview.html">原典Webプレビュー</a> · <a href="README.md">ガイド</a> · <a href="../../../downloads/ppt-agent-example-ja.zip">制作ZIP</a></header><main>'+images+'</main></html>')
    b='examples/repositories/ppt-agent-showcase'
    ex={'id':'ppt-agent-showcase','title':TITLES[0],'use_case':'大胆な和文版式で伝える5枚の展示企画','repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'ppt-agent-ja','page_count':5,'format':'pptx','preview_kind':'powerpoint-render','preview_notice':'原典DOM→SVG→native PPTX。文字と形状をPowerPoint内で編集。Web previewも同梱。','editability':'native_shapes','editable_features':['text','shapes'],'style':'原典Bauhaus Block / 赤・青・黄の幾何 / 巨大ゴシック見出し・明朝本文','cover':b+'/render/slide-01.png','interior':b+'/render/slide-03.png','preview':b+'/index.html','web_preview':b+'/preview.html','artifact_download':b+'/deck.pptx','pdf_download':b+'/render/deck.pdf','source_download':'downloads/ppt-agent-example-ja.zip','fork_download':'downloads/ppt-agent-ja.zip','input':b+'/input/BRIEF.md','input_data':b+'/input/planning.json','prompt':b+'/PROMPT.md','prompt_text':PROMPT,'provenance':b+'/PROVENANCE.json','qa':b+'/QA.json','guide':b+'/README.md','titles':TITLES,'notes':['仮想の展示企画。日時・会場・参加条件未定。準備日程は相対的な仮案。']*5,'method':'原典bauhaus_block mock/styleを日本語へ局所対応し、html_packager→html2svg(dom-to-svg/Puppeteer)→svg2pptx.pyでnative OOXML文字・図形を生成。PowerPoint16でPNG/PDF描画。','sample_notice':'仮想の展示企画。native text/shapesのみ、native chart/table/数式は使用していません。','pages':[b+f'/render/slide-{i:02}.png' for i in range(1,6)]}
    dump(ROOT/'data/sol-ppt-agent-repository-examples.json',[ex]);dump(ROOT/'data/sol-ppt-agent-repository-guides.json',[{'repository':REPO,'summary_ja':'Bauhaus Blockの実mockと原典DOM/SVG converterで大胆な日本語展示企画をnative PPTXへ。','example_ids':['ppt-agent-showcase'],'upstream_commit':PIN,'license':'MIT','license_paths':[b+'/LICENSE'],'skill_paths':['skill-forks/ppt-agent-ja/SKILL.md'],'production_status':'light_check_complete','requirements':['Node.js24+ / puppeteer25.13.0 / dom-to-svg0.12.2 / esbuild0.28.2','Python3.12 / python-pptx / lxml / Pillow','Chrome / Microsoft PowerPoint16 for export','Zen Kaku Gothic New Black / BIZ UDPMincho / Manrope (OFL)'],'commands':['npm install --ignore-scripts','python -m pip install -r requirements.txt','python source/build.py --node C:/path/to/node.exe --chrome C:/path/to/chrome.exe','powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render'],'guide':b+'/README.md','source_download':ex['source_download'],'fork_download':ex['fork_download'],'limitations':['仮想の企画・日程相対案・会場日時参加条件未定','native text/shapes、native chart/table/数式は未使用','全ページ詳細目視・独立レビュー・構造監査・ZIP再実行なし']}]);package()

def package():
    for folder,name in [(CASE,'ppt-agent-example-ja.zip'),(FORK,'ppt-agent-ja.zip')]:
        with zipfile.ZipFile(ROOT/'downloads'/name,'w',zipfile.ZIP_DEFLATED) as z:
            for p in folder.rglob('*'):
                if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.build']) and p.suffix!='.pyc' and not p.name.endswith('.bundle.js'):z.write(p,folder.name+'/'+p.relative_to(folder).as_posix())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--node');ap.add_argument('--chrome');ap.add_argument('--finish',action='store_true');args=ap.parse_args()
    if args.finish:finish()
    else:
        if not args.node or not args.chrome:ap.error('--node and --chrome required')
        if SCRIPT.parent.name=='tools':prepare()
        execute(Path(args.node).resolve(),args.chrome)
