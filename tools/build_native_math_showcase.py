"""Original Noi1r themes/helpers -> PptxGenJS -> original inject_omml (Pandoc).
No generic deck renderer or image math fallback. Works as packaged source/build.py.
"""
from pathlib import Path
import argparse, difflib, hashlib, importlib.metadata, json, os, re, shutil, subprocess, sys, zipfile
SCRIPT=Path(__file__).resolve()
ROOT=SCRIPT.parents[1]
CASE=ROOT/'examples/repositories/native-math-showcase' if SCRIPT.parent.name=='tools' else SCRIPT.parent.parent
PIN='a39cd8cfba332741a96d52bebd2bb378b638364e'
REPO='Noi1r/powerpoint-skill'
TITLES=['平均の、その先。','平均は、中心を表す','分散は、ずれを二乗して平均する','標準偏差で、元の単位に戻す','平均と散らばりを、一緒に読む']
PROMPT='''中高生・学び直し向け5分教材「平均の、その先。」を日本語PowerPoint5枚totalで作成してください。
仮想の得点データA=[4,5,6], B=[0,5,10]。どちらも平均は5だが散らばりが異なります。
mean→variance→standard deviationを、動機と同じデータの計算例で簡潔に説明。全3件を全体とした分散で、分母はn。n-1の不偏分散との違いは短く明記。
原典Noi1r/powerpoint-skillのSandwichテーマとPptxGenJS helpersを実際に使い、render_latex.pyのOMML manifestとinject_omml.pyのPandoc→DOCX→OMML注入を実行。
暗い表紙・結論、明るい本文、青と橙。Shippori明朝見出し、BIZ UDPGothic本文、Manrope英数字。導入でnative点図/表、本文でnative図表と編集可能な式。カード格子を繰り返さない。
全5ページの文字・数式・図表を実描画で確認し、原典overlap検査と独立レビューで修正する。制作計画は入力へ保存する。この5分教材は本編5枚のため、原典のReferences/ThankYou/Backup追加は作例固有の省略として明記する。
最後のPNG/PDFはPowerPoint16の実描画。数式を画像へ黙って置き換えない。PPTX、PNG/PDF、原典runtime/未変更原本/差分、入力/依頼/ガイド/許諾/日本語SKILL、2ZIPを完成させる。'''
FORMULAS=[
 {'id':'mean','latex':r'\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i'},
 {'id':'mean-a','latex':r'\bar{x}_A=\frac{4+5+6}{3}=5'},
 {'id':'var-a','latex':r'\sigma_A^2=\frac{1+0+1}{3}=\frac{2}{3}'},
 {'id':'var-b','latex':r'\sigma_B^2=\frac{25+0+25}{3}=\frac{50}{3}'},
 {'id':'sd-a','latex':r'\sigma_A=\sqrt{\frac{2}{3}}\approx 0.82'},
 {'id':'sd-b','latex':r'\sigma_B=\sqrt{\frac{50}{3}}\approx 4.08'},
]
for f in FORMULAS:f.update(mode='display',render='omml')
SKILL_JA='''---
name: native-math-ja
description: 原稿・研究資料から、数式をPowerPoint内で編集できる発表資料を作る。
---

# 数式を編集できるPowerPointを作る

原典: Noi1r/powerpoint-skill / commit a39cd8cfba332741a96d52bebd2bb378b638364e / MIT。
原文はupstream/powerpoint-slides/SKILL.md、テーマと全規則は同梱referencesを読む。非公式の日本語案内。

## 自分の資料で使う

1. 原稿や論文を読み、主要な主張、前提知識、例、数式を抽出する。PPTXが必要な用途で使い、Beamer/TeX出力は別スキルへ分ける。
2. 発表時間、聞き手、前提、範囲、深さ、テーマを決める。既に依頼に指定があれば使い、足りない条件だけを確認する。
3. 頁構成・各頁の目的・版式・数式と図の配置を計画する。定義の前に動機、定義から2頁以内に具体例を置く。原典の承認契約はユーザーの既存の指示に合わせる。
4. 原典themes.mdからテーマとPptxGenJS helpersを使う。字体・配色・版式は資料に合わせる。図形、表、グラフをnativeで作る。
5. 数式をformulas.jsonへ集める。通常はrender:ommlを使い、原典render_latex.pyでmanifestを生成。addMathTextのplaceholderを配置し、inject_omml.pyでPandoc→DOCX→OMMLを注入する。残存placeholderを0にする。画像への代替は明示し、黙って編集性を失わせない。
6. 実際にPPTXを生成して全頁を描画する。OMMLはPowerPointで確認する。LibreOfficeでは欠ける場合がある。数式と表の間隔、はみ出し、対比、数式の正確さを頁ごとに確認する。
7. 原典check_overlaps.py、visual-check、audit、pedagogy、excellenceの契約を読み、対応する検査と修正を行う。原典の採点90点以上条件と独立確認を、生成成功だけで置き換えない。未実行は未実行と記録する。
8. 完成PPTX、PDF/PNG、原稿・数式・生成ソース、利用条件、検査範囲を渡す。原典のReferences/Thank You/Backup構成から省く場合は、用途と変更を明記する。

## 必要環境

Node.jsとPptxGenJS、Pythonとlxml、Pandoc。OMMLの表示・編集確認にはMicrosoft PowerPointを使う。PptxGenJSはMIT、lxmlはBSD系、PandocはGPLの外部実行依存。字体は公式配布と原文OFLを使い、Office付属字体やXSLを抽出再配布しない。

## 同梱作例の範囲

5分・5枚の仮想得点教材。Sandwichの青と橙を文字の対比が取れる濃さへ調整し、明朝見出しと日本語本文書体を設定した。本編5枚に絞ったためReference/Thank You/Backup追加を省略。研究論文の抽出例ではない。実行と独立評価の状態は作例QA.jsonを確認する。
'''

SLIDES=r'''
// Japanese educational slides. Original T/F/masters/math/chart/table helpers above.
function text(sl,t,x,y,w,h,size=18,color=T.tx.pri,face=F.body.face,bold=false){sl.addText(t,{x,y,w,h,fontSize:size,fontFace:face,color,bold,margin:0,valign:'mid',shrinkText:true,breakLine:false})}
function foot(sl,n,dark=false){text(sl,'学習用の仮想データ / 調査結果ではありません',.5,5.17,8.3,.2,10,dark?'C5CDD0':T.tx.mut);text(sl,String(n).padStart(2,'0'),9,5.12,.5,.3,11,dark?'FFFFFF':T.tx.mut,'Manrope')}
function dots(sl,vals,y,color,dark=false){
 const x=.9,w=4.4;
 sl.addShape(pres.ShapeType.line,{x,y:y+.27,w,h:0,line:{color:dark?'758084':'C9D0D3',width:.7}});
 vals.forEach(v=>sl.addShape(pres.ShapeType.ellipse,{x:x+w*v/10-.075,y:y+.195,w:.15,h:.15,line:{color,transparency:100},fill:{color}}));
}
// 01: dark cover, substantive native dot plots.
{
 const s=pres.addSlide({masterName:'TITLE_SLIDE'});
 text(s,'DATA / 5分の学習ノート',.55,.55,8.9,.35,14,'F3B156','Manrope',true);
 text(s,'平均の、\nその先。',.55,1.12,4.6,1.7,48,'FFFFFF','Shippori Mincho',true);
 text(s,'同じ「5」に、\n違う散らばり。',.58,3.35,4.6,1,24,'FFFFFF');
 text(s,'A',5.5,1.65,.5,.4,18,'60B5E2','Manrope',true); text(s,'4   5   6',6.05,1.65,3.1,.4,22,'FFFFFF','Manrope');
 text(s,'B',5.5,2.9,.5,.4,18,'F5B451','Manrope',true); text(s,'0   5   10',6.05,2.9,3.1,.4,22,'FFFFFF','Manrope');
 [1.15,2.4].forEach((dy,i)=>{const vals=i?[0,5,10]:[4,5,6];const color=i?'F5B451':'60B5E2';const x=6.05,w=3.1,y=dy+1.05;s.addShape(pres.ShapeType.line,{x,y,w,h:0,line:{color:'758084',width:.7}});vals.forEach(v=>s.addShape(pres.ShapeType.ellipse,{x:x+w*v/10-.065,y:y-.065,w:.13,h:.13,line:{color,transparency:100},fill:{color}}));});
 text(s,'0',5.96,4, .4,.3,12,'C5CDD0','Manrope');text(s,'10点',8.83,4,.6,.3,12,'C5CDD0');foot(s,1,true);
}
// 02: original native-table helper, with original OMML helper.
{
 const s=pres.addSlide({masterName:'CONTENT_SLIDE'});sTitle(s,'平均は、中心を表す');
 text(s,'3件ずつの得点。どちらが、中心に集まっている？',.55,1.03,9,.5,19);
 F.tblCell.size=22;F.tblHead.size=16;
 const c=t=>({text:String(t),options:{fontFace:'Manrope',align:'center'}});
 addTable(s,['データ','1件目','2件目','3件目'],[[c('A'),c(4),c(5),c(6)],[c('B'),c(0),c(5),c(10)]],.6,1.92,4.4,[1.2,1.07,1.07,1.06],.6);
 addMathText(s,'mean',5.4,1.78,4,1.05,{fontSize:27});
 addMathText(s,'mean-a',.65,3.69,4.4,1,{fontSize:25,color:T.ac.pos});
 text(s,'Bも合計15点。\n3件で割ると平均は5点。',5.4,3.61,4,1,20,T.ac.neg);
 text(s,'足して、件数で割る。平均だけでは、散らばりは見えない。',.65,4.75,8.7,.25,14,T.tx.sec);foot(s,2);
}
// 03: formula and native bar chart, not an image renderer.
{
 const s=pres.addSlide({masterName:'CONTENT_SLIDE'});sTitle(s,'分散は、ずれを二乗して平均する');
 text(s,'平均からのずれ。二乗すると、正負が打ち消し合わない。',.6,.95,8.9,.45,17);
 text(s,'平均との差を二乗 → 足す → 件数で割る',.6,1.55,8.8,.65,25,T.tx.pri,F.body.face,true);
 F.tblCell.size=12;F.caption.size=11;
 addChart(s,pres.ChartType.bar,[{name:'A',labels:['1件目','2件目','3件目'],values:[1,0,1]},{name:'B',labels:['1件目','2件目','3件目'],values:[25,0,25]}],.6,2.75,4.5,1.77,{showLegend:true,chartColors:[T.ac.pos,T.ac.neg],catAxisLabelFontSize:10,valAxisLabelFontSize:10,valAxisMinVal:0,valAxisMaxVal:30,valAxisMajorUnit:10,showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:'0',dataLabelColor:T.tx.pri,dataLabelBkgrdColor:T.bg.content,dataLabelFormatCodeSourceLinked:false,showTitle:false,showBorder:false,showCatName:false});
 text(s,'二乗したずれ：A=1,0,1 ／ B=25,0,25',.8,2.56,4.5,.2,11,T.tx.sec);
 addMathText(s,'var-a',5.3,2.83,4.05,.78,{fontSize:24,color:T.ac.pos});
 addMathText(s,'var-b',5.3,3.92,4.05,.78,{fontSize:24,color:T.ac.neg});
 text(s,'全3件を「全体」として計算。分母はn（ここでは3）。',.6,4.84,8.9,.22,12,T.tx.sec);foot(s,3);
}
// 04: original native-chart helper plus native radical formulas.
{
 const s=pres.addSlide({masterName:'CONTENT_SLIDE'});sTitle(s,'標準偏差で、元の単位に戻す');
 text(s,'分散の単位は「点の二乗」。平方根で「点」に戻す。',.6,.97,8.9,.45,18);
 text(s,'分散の平方根をとる',.65,1.7,4,.65,27,T.tx.pri,F.body.face,true);
 text(s,'平均からの広がりを\n同じ単位で比べる目安。',5.2,1.7,4.15,.82,21);
 addMathText(s,'sd-a',.65,2.9,4.15,1.05,{fontSize:26,color:T.ac.pos});
 addMathText(s,'sd-b',5.2,2.9,4.15,1.05,{fontSize:26,color:T.ac.neg});
 addChart(s,pres.ChartType.bar,[{name:'標準偏差',labels:['A','B'],values:[.8164965809,4.082482905]}],.7,4.07,8.6,.85,{barDir:'bar',showLegend:false,varyColors:true,chartColors:[T.ac.pos,T.ac.neg],catAxisLabelFontFace:'Manrope',catAxisLabelFontSize:12,catAxisLabelFrequency:'1',valAxisMinVal:0,valAxisMaxVal:5,valAxisMajorUnit:1,valAxisLabelFontSize:10,valGridLine:{color:'D0D0D0',width:.4},showValue:false});
 foot(s,4);
}
// 05: dark conclusion, editable summary table and a concrete reading habit.
{
 const s=pres.addSlide({masterName:'THANK_YOU'});
 text(s,'平均と散らばりを、\n一緒に読む',.6,.58,8.8,1.2,35,'FFFFFF','Shippori Mincho',true);
 text(s,'平均',.6,2.3,2.4,.4,18,'C5CDD0');text(s,'中心の位置',3.3,2.3,5.6,.4,25,'FFFFFF');
 text(s,'標準偏差',.6,3.03,2.4,.4,18,'C5CDD0');text(s,'中心からの広がり',3.3,3.03,5.6,.4,25,'FFFFFF');
 s.addTable([[{text:'',options:{fill:{color:T.bg.title}}},{text:'A',options:{color:'60B5E2'}},{text:'B',options:{color:'F5B451'}}],[['平均（点）','5','5']].flat(),[['標準偏差（点）','0.82','4.08']].flat()],{x:.65,y:3.72,w:8.6,colW:[4,2.3,2.3],rowH:.34,fontFace:F.body.face,fontSize:15,color:'FFFFFF',fill:{color:T.bg.title},border:{type:'solid',color:'677276',pt:.4},margin:3,align:'center'});
 text(s,'※ 全体の分散を使用。標本から推定する不偏分散とは区別。',.65,4.86,8.7,.2,11,'C5CDD0');foot(s,5,true);
}
pres.writeFile({fileName:'source/deck-placeholders.pptx'}).then(()=>console.log('Original theme/helpers: 5 Japanese slides generated.'));
'''

def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare():
    upstream=ROOT/'.build/actual-upstreams/Noi1r__powerpoint-skill'
    for rel in ['LICENSE','powerpoint-slides/SKILL.md','powerpoint-slides/references/themes.md','powerpoint-slides/scripts/inject_omml.py','powerpoint-slides/scripts/render_latex.py','powerpoint-slides/formula-rendering.md']:
        out=CASE/'upstream'/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(upstream/rel,out)
    shutil.copy2(upstream/'LICENSE',CASE/'LICENSE')
    for family in ['shipporimincho','bizudpgothic','manrope']:
        target=CASE/'fonts'/family;target.mkdir(parents=True,exist_ok=True)
        for p in (ROOT/'downloads/fonts'/family).iterdir():
            if p.suffix=='.ttf' or p.name=='OFL.txt':shutil.copy2(p,target/p.name)
    source=CASE/'source';source.mkdir(exist_ok=True)
    shutil.copy2(ROOT/'tools/render_powerpoint.ps1',source/'render_powerpoint.ps1')
    render=(source/'render_powerpoint.ps1').read_text(encoding='utf-8')
    render=render.replace('if ($existingPowerPoint.Count -eq 0 -and $powerPoint.Presentations.Count -eq 0) { $powerPoint.Quit() }','# Shared PowerPoint application: close only our opened presentation; never Quit.')
    write(source/'render_powerpoint.ps1',render)
    shutil.copy2(SCRIPT,source/'build.py')
    dump(CASE/'input/data.json',{'purpose':'学習用の仮想得点。調査結果ではない','datasets':{'A':[4,5,6],'B':[0,5,10]},'variance_divisor':'n; all three values treated as population','mean':{'A':5,'B':5},'population_variance':{'A':2/3,'B':50/3},'population_standard_deviation':{'A':(2/3)**.5,'B':(50/3)**.5}})
    dump(CASE/'input/plan.json',{'duration_minutes':5,'audience':'中高生・学び直し','total_slides':5,'theme':'upstream Sandwich, darker semantic colors for contrast','slides':[{'title':t,'layout':l} for t,l in zip(TITLES,['dark title + native dot plot','native table + mean equations','two formulas + native grouped bars with values','two native radical formulas + native bar chart','dark conclusion + native summary table'])],'review':'All5 visual check, original overlap checker, Kimi K3 and Opus5.5 independent review loop','fixed_extras':'No References/ThankYou/Backup extra slides in this5-minute educational example; deviation disclosed'})
    write(CASE/'input/BRIEF.md','# 平均の、その先。\n\n仮想得点A=[4,5,6], B=[0,5,10]。5分・5枚の教材。平均はどちらも5、全体の分散は2/3と50/3、標準偏差は約0.82点と4.08点。分母は全3件を全体としたn。母集団を推定する不偏分散とは区別する。\n')
    write(CASE/'PROMPT.md',PROMPT+'\n')
    dump(CASE/'formulas.json',FORMULAS)
    refs=(CASE/'upstream/powerpoint-slides/references/themes.md').read_text(encoding='utf-8')
    original=refs.split('```javascript\n',1)[1].split('// === SLIDES ===',1)[0]
    # Original theme JSON and complete helpers, with typography/theme substitutions only.
    theme=re.search(r'\*\*Sandwich\*\*.*?```json\n(.*?)\n```',refs,re.S).group(1)
    t=json.loads(theme)
    # Darker blue/orange retain the semantic pair and meet text contrast on white.
    t['accent']['positive']='006B98'
    t['accent']['negative']='A65A00'
    theme_js='const T = '+json.dumps({'bg':t['background'],'tx':{'pri':t['text']['primary'],'sec':t['text']['secondary'],'mut':t['text']['muted'],'wh':'FFFFFF'},'ac':{'pos':t['accent']['positive'],'neg':t['accent']['negative'],'emp':t['accent']['emphasis']},'chart':t['chart'],'cardFill':t['card_fill'],'divider':t['divider']},indent=2)+';'
    adapted=re.sub(r'const T = \{.*?\n\};',theme_js,original,count=1,flags=re.S)
    adapted=adapted.replace('"Georgia"','"Shippori Mincho"').replace('"Calibri"','"BIZ UDPGothic"').replace('pres.author = "Presenter Name";','pres.author = "Studio Yebisu";').replace('pres.title = "Presentation Title";','pres.title = "平均の、その先。";')
    adapted=adapted.replace('margin: 0\n  });','margin: 0, shrinkText: true\n  });')
    write(source/'original-helpers.cjs',original)
    write(source/'generate_slides.cjs',adapted+SLIDES)
    write(source/'helpers.diff',''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True),fromfile='original themes.md JavaScript helpers',tofile='Sandwich Japanese helper adapter')))
    dump(CASE/'package.json',{'private':True,'dependencies':{'pptxgenjs':'4.0.1'}})
    write(CASE/'requirements.txt','lxml==6.1.3\n')
    # Preserve individual dependency notices without redistributing dependency binaries.
    deps=CASE/'dependencies';deps.mkdir(exist_ok=True)
    shutil.copy2(ROOT/'.build/node_modules/pptxgenjs/LICENSE',deps/'PptxGenJS-MIT.txt')
    shutil.copy2(ROOT/'.build/native-math-pandoc/pandoc-3.12.1/COPYRIGHT.txt',deps/'Pandoc-COPYRIGHT.txt')
    for name in ['lxml']:
        dist=importlib.metadata.distribution(name)
        for item in dist.files or []:
            if item.name.lower().startswith(('license','notice','copying')):
                p=Path(dist.locate_file(item))
                if p.is_file():target=deps/name/p.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    write(CASE/'README.md',f'''# 平均の、その先。

中高生・学び直し向け5分教材、全5枚。仮想得点A=[4,5,6], B=[0,5,10]。調査結果ではありません。

## 原典の実行方法

[Noi1r/powerpoint-skill](https://github.com/Noi1r/powerpoint-skill/tree/{PIN}) / MIT / `{PIN}`。
原典 `references/themes.md` のSandwich JSON、スライドmasters、`sTitle` / `addTable` / `addChart` / `addMathText` を実際に使用。原典JavaScript helper全文を取り出し、Sandwich themeと日本語字体に変更。未変更原本は `upstream/`、抽出原文は `source/original-helpers.cjs`、変更は `source/helpers.diff`。

1. 原典 `render_latex.py` で `render:omml` 数式のmanifestを作成（画像化もTeX環境も不要）。
2. PptxGenJSでnative図形・表・グラフと数式placeholderを生成。
3. 原典 `inject_omml.py` を実行。PandocがLaTeX数式をDOCXのOMMLへ変換し、原典がPPTXへ注入。
4. PowerPoint16でPNG/PDFを実描画。LibreOfficeではOMML数式が欠けるという原典の制限があるため、完成プレビューに使いません。

## 数式の編集

`deck.pptx` をMicrosoft PowerPointで開き、数式の文字をクリックしてカーソルを入れます。「数式」タブから分数・平方根・添字を編集できます。数式は画像ではありません。本文・図形・nativeグラフ・表も編集できます。グラフは右クリック「データの編集」で値を変更。PDF/PNGは閲覧用で、編集はPPTXを使用してください。

欧文数字はManrope、和文明朝はShippori Mincho、本文はBIZ UDPGothic。公式未変更TTF/OFLのみ同梱し、OS字体を抽出していません。OMMLの数学字体はOfficeの実行時字体を使用し、Office字体は同梱しません。

## 再生成

Node.js、Python3、公式[Pandoc](https://pandoc.org/installing.html)、PowerPoint16（プレビュー生成用）が必要です。

```powershell
npm install
python -m pip install -r requirements.txt
python source/build.py --node C:/path/to/node.exe --pandoc C:/path/to/pandoc.exe
powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
```

Pandoc3.12.1公式portable取得例（バイナリはキットに含めません）：

```powershell
Invoke-WebRequest 'https://github.com/jgm/pandoc/releases/download/3.12.1/pandoc-3.12.1-windows-x86_64.zip' -OutFile pandoc.zip
Expand-Archive -LiteralPath pandoc.zip -DestinationPath .build/pandoc
```

原典injectorはPandoc→DOCX方式。MathML変換XSLやOffice付属XSLの参照・抽出・同梱はありません。PandocはGPL-2.0-or-laterの外部実行依存で、同梱はCOPYRIGHT説明のみ。PptxGenJS4.0.1はMIT、lxml6.1.3の個別許諾も `dependencies/` に保持。

## 確認範囲

原典JS生成と数式注入の成功、数式placeholder残存なし、PowerPoint16のPNG/PDF出力、代表完成物の初回表示まで。ユーザー指定により全ページ詳細目視、独立レビュー、全PPTX構造監査、ZIP再実行は未実施。分散は全3件を全体としたn分母。不偏分散（n−1）はこの教材の計算に使っていません。
''')

def execute(node,pandoc):
    env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8','PATH':str(Path(pandoc).resolve().parent)+os.pathsep+os.environ.get('PATH','')}
    if SCRIPT.parent.name=='tools':env['NODE_PATH']=str(ROOT/'.build/node_modules')
    logs={}
    commands=[('manifest',[sys.executable,str(CASE/'upstream/powerpoint-slides/scripts/render_latex.py'),'formulas.json','formulas']),('generate',[str(Path(node).resolve()),'source/generate_slides.cjs']),('inject',[sys.executable,str(CASE/'upstream/powerpoint-slides/scripts/inject_omml.py'),'source/deck-placeholders.pptx','formulas.json','deck.pptx'])]
    for name,cmd in commands:
        r=subprocess.run(cmd,cwd=CASE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');write(CASE/'source'/f'{name}.log',r.stdout+r.stderr);logs[name]={'exit_code':r.returncode,'log':'source/'+name+'.log'}
        if r.returncode:raise RuntimeError(name+': '+(r.stdout+r.stderr)[-6000:])
    with zipfile.ZipFile(CASE/'deck.pptx') as z:
        slides=[z.read(n) for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
        residual=sum(x.count(b'{{MATH:') for x in slides)
    if residual:raise RuntimeError('Unreplaced MATH placeholders: '+str(residual))
    dump(CASE/'source/BUILD.json',{'steps':logs,'residual_math_placeholders':residual,'formula_definition_count':len(FORMULAS),'omml_conversion_method':'original inject_omml.py -> Pandoc LaTeX to DOCX -> extract OMML','full_structure_audit':False})
    print('Original PptxGenJS helpers + Pandoc/OMML injector succeeded; zero residual placeholders.')

def finish():
    fork=ROOT/'skill-forks/native-math-ja'
    write(CASE/'SKILL.md',f'''---
name: native-math-ja
description: 原典Sandwich themeとOMML数式注入で編集可能な日本語数式PowerPointを作る。
---

# 日本語のnative数式PowerPoint

Noi1r/powerpoint-skill `{PIN}` / MIT。原典theme/helpersとinject_ommlを実際に実行する。

1. 原典themes.mdのJavaScript helperを抽出し、Sandwichと日本語字体を設定。図形・表・グラフをPptxGenJSで編集可能に作る。
2. formulas.jsonは `render:omml`。原典render_latexでmanifestを作り、addMathTextでplaceholderを配置。
3. 原典inject_omml.pyを実行。Pandoc→DOCX→OMML注入。失敗と残存placeholderは必ず修正し、画像数式へ黙って替えない。
4. Office字体/XSLを抽出配布せず、公式TTF/OFLを同梱。補助XSLはこの原典経路では不要。OMMLはPowerPointで直接編集できる。
5. PNG/PDFはPowerPoint実描画。共有ApplicationをQuitせず、自分のdeckだけCloseする。LibreOfficeではOMML欠けがある。
6. 今回はユーザー指定の内部判断・軽い確認を優先。必須interview/outline承認待ち、5並列review、References/ThankYou/Backup固定追加を適用せず、5枚教材を守る。計画は入力へ記録。全ページ詳細監査・独立review・ZIP再実行は不要。
7. 原典実行、数式注入成功、placeholder残存なし、代表初回表示を記録。.pptx/.png/.pdf、source/license、編集条件とガイドを渡す。

## quick_validate

`python source/build.py --node C:/path/to/node.exe --pandoc C:/path/to/pandoc.exe` の成功後、PowerPointで代表完成物を一度開く。
''')
    write(CASE/'SKILL.md', SKILL_JA)
    for directory in ['upstream','source','fonts','dependencies','input']:
        shutil.copytree(CASE/directory,fork/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.pptx','*.log','__pycache__','*.pyc'))
    for filename in ['SKILL.md','LICENSE','README.md','formulas.json','package.json','requirements.txt','PROMPT.md']:shutil.copy2(CASE/filename,fork/filename)
    dump(fork/'SOURCE.json',{'repository':REPO,'commit':PIN,'license':'MIT','modified':True,'used_files':['powerpoint-slides/references/themes.md','powerpoint-slides/scripts/render_latex.py','powerpoint-slides/scripts/inject_omml.py'],'changes':['Sandwich theme JSON applied','Japanese fonts','5-slide educational content','shared PowerPoint exporter does not Quit','user-selected minimal workflow replaces interviews/full reviews/fixed extras'],'math':'native OMML; no image formula fallback','example':'examples/repositories/native-math-showcase'})
    receipt=json.loads((CASE/'source/BUILD.json').read_text(encoding='utf-8'))
    dump(CASE/'PROVENANCE.json',{'repository':REPO,'upstream_commit':PIN,'license':'MIT','method':'Original themes.md Sandwich masters/helpers -> PptxGenJS4.0.1 -> original render_latex OMML manifest + original inject_omml.py Pandoc3.12.1 DOCX extraction -> Microsoft PowerPoint16 render','runtime_originals':{p.relative_to(CASE).as_posix():sha(p) for p in (CASE/'upstream').rglob('*') if p.is_file()},'helper_changes':'source/helpers.diff','formula_images_used':False,'auxiliary_xsl_used':False,'office_fonts_or_xsl_redistributed':False,'fonts':{p.relative_to(CASE).as_posix():sha(p) for p in (CASE/'fonts').rglob('*.ttf')},'dependency_licenses':['upstream MIT','PptxGenJS MIT','lxml BSD3 and dependencies: see dependencies/lxml','Pandoc GPL2+ external runtime only','fonts OFL1.1'],'input_status':'hypothetical educational scores; population variance divisor n','build':receipt})
    render_exists=(CASE/'render/slide-01.png').exists()
    dump(CASE/'QA.json',{'status':'rendered_ready_for_first_display' if render_exists else 'native_generated','original_generation_success':True,'original_injection_success':True,'residual_math_placeholders':0,'formula_definitions':len(FORMULAS),'powerpoint_rendered':render_exists,'representative_page_opened':False,'whole_deck_detailed_review':False,'independent_review':False,'full_pptx_structure_audit':False,'zip_reexecution':False,'review_mode':'user_requested_minimal','native_math_editing':'Microsoft PowerPoint math text, not images','office_render_receipt':'render/powerpoint-render.json'})
    images=''.join(f'<figure><img src="render/slide-{i+1:02}.png" alt="{t}"><figcaption>{i+1}. {t}</figcaption></figure>' for i,t in enumerate(TITLES))
    write(CASE/'index.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>平均の、その先。</title><style>body{margin:0;background:#2d3436;color:#fff;font-family:sans-serif}header,main{max-width:1200px;padding:24px;margin:auto}a{color:#f5b451}figure{margin:0 0 28px}img{display:block;width:100%}figcaption{font-size:13px;padding:10px 0}</style><header><h1>平均の、その先。</h1><p>5分・5枚の学習教材 / 仮想データ / native OMML数式</p><a href="deck.pptx">編集可能なPowerPoint</a> · <a href="render/deck.pdf">PDF</a> · <a href="README.md">日本語ガイド</a> · <a href="../../../downloads/native-math-example-ja.zip">制作ZIP</a></header><main>'+images+'</main></html>')
    base='examples/repositories/native-math-showcase'
    example={'id':'native-math-showcase','title':'平均の、その先。','use_case':'native数式・図表で学ぶ5分教材','repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'native-math-ja','page_count':5,'format':'pptx','preview_kind':'powerpoint-render','editability':'native_math','editable_features':['text','shapes','charts','tables','formulas'],'style':'Sandwich / 暗い表紙・結論と明るい本文 / 青・橙 / 明朝見出し','cover':base+'/render/slide-01.png','interior':base+'/render/slide-03.png','preview':base+'/index.html','artifact_download':base+'/deck.pptx','pdf_download':base+'/render/deck.pdf','source_download':'downloads/native-math-example-ja.zip','fork_download':'downloads/native-math-ja.zip','input':base+'/input/BRIEF.md','input_data':base+'/input/data.json','prompt':base+'/PROMPT.md','prompt_text':PROMPT,'provenance':base+'/PROVENANCE.json','qa':base+'/QA.json','guide':base+'/README.md','titles':TITLES,'notes':['仮想得点。全3件を全体とした分散の分母はn。調査結果ではない。']*5,'method':'原典Sandwich theme/helpersをPptxGenJSへ実適用。原典render_latexでOMML manifest生成、inject_ommlでPandoc→DOCX由来のnative数式注入。PowerPoint16でPNG/PDF実描画。','sample_notice':'学習用の仮想データ。数式はMicrosoft PowerPointで編集できるnative OMML。','pages':[base+f'/render/slide-{i:02}.png' for i in range(1,6)]}
    dump(ROOT/'data/sol-native-math-repository-examples.json',[example])
    dump(ROOT/'data/sol-native-math-repository-guides.json',[{'repository':REPO,'summary_ja':'Sandwich themeと原典OMML注入で数式・図表をPowerPoint内で編集する日本語教材。','example_ids':['native-math-showcase'],'upstream_commit':PIN,'license':'MIT','license_paths':[base+'/LICENSE'],'skill_paths':['skill-forks/native-math-ja/SKILL.md'],'production_status':'light_check_complete' if render_exists else 'native_generated','requirements':['Node.js / PptxGenJS4.0.1 (MIT)','Python / lxml6.1.3','Pandoc3.12.1 (GPL2+, external runtime)','Microsoft PowerPoint16 for native OMML PNG/PDF render','Shippori Mincho / BIZ UDPGothic / Manrope (OFL)'],'commands':['npm install','python -m pip install -r requirements.txt','python source/build.py --node C:/path/to/node.exe --pandoc C:/path/to/pandoc.exe','powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render'],'guide':base+'/README.md','source_download':example['source_download'],'fork_download':example['fork_download'],'limitations':['仮想データ・全体の分散n分母。調査結果ではない','OMMLはPowerPoint実描画。LibreOfficeでは欠ける場合がある','全ページ詳細監査・独立レビュー・ZIP再実行なし']}])
    package()

def package():
    for folder,name in [(CASE,'native-math-example-ja.zip'),(ROOT/'skill-forks/native-math-ja','native-math-ja.zip')]:
        with zipfile.ZipFile(ROOT/'downloads'/name,'w',zipfile.ZIP_DEFLATED) as z:
            for p in folder.rglob('*'):
                if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.build']) and p.suffix!='.pyc':z.write(p,folder.name+'/'+p.relative_to(folder).as_posix())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--node');ap.add_argument('--pandoc');ap.add_argument('--finish',action='store_true');args=ap.parse_args()
    if args.finish:finish()
    else:
        if not args.node or not args.pandoc:ap.error('--node and --pandoc required')
        if SCRIPT.parent.name=='tools':prepare()
        execute(args.node,args.pandoc)
