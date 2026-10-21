"""Japanese flower-service concept through LearnDeck's actual DOM converter."""
from pathlib import Path
import argparse, hashlib, json, math, os, shutil, subprocess, zipfile

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams/LearnAIHubC__LearnDeck'
OUT=ROOT/'examples/repositories/learndeck-showcase'
FORK=ROOT/'skill-forks/learndeck-ja'
PIN='d5ea12ca88f9a87edaf20b6bb48847790baed698'
REPO='LearnAIHubC/LearnDeck'
TITLE='花を、一本から。'
TITLES=[TITLE,'一本なら、置く場所を選べる。','選ぶ。届く。飾る。','束にする日も、休む日も。','次の一輪を、楽しみにする。']
NOTES=['架空の花の定期便サービスの提供案です。運営中のサービスや実績ではありません。','大きな花束だけでなく、小さな器へ一本を届ける体験を考えます。室内の置き場所の例です。','選ぶ、受け取る、飾るという利用の流れの案です。花種の選択範囲や配送方法は未確定です。','生活に合わせて本数と受取頻度を調整する提供案。実装済みの休止機能や販売条件ではありません。','価格、配送地域、花の選び方は未確定。季節ごとの品揃えと配送品質を確かめて内容を決める提案です。']
PROMPT='LearnAIHubC/LearnDeckの原典HTML-to-PPT方式を実行して、架空の花の定期便サービス「花を、一本から。」を5枚の編集可能PPTXにしてください。日本語HTMLのDOM位置を原典html_to_ppt.js/html_to_editable_pptx.jsで実測し、文字と背景/図形をnative object、花のSVGを個別画像として組み立てる。紙色・強い朱赤・墨黒、巨大な文字、一輪と花束を大胆に置く。表紙の短い日本語はDela Gothic One、余韻のある見出しはShippori Mincho、本文はBIZ UDPGothic。角丸カード反復を避け、ページごとに見出しの位置と構図を変える。価格/実績を捏造せず、提供案と未確定事項を短く明示。原典のDOM変換を--no-previewで実行し、今回の明示依頼に基づいてHTMLとPowerPointの全5頁を実描画・目視し、字間・見出し下余白・要素分離を確認する。SVG元・原典MIT・実TTF/OFLを保全。元converterの単一フォント制約を局所的にcomputed font-familyへ拡張した場合は差分を記録する。'
NODE=Path('C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
MODULES=Path('C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')

def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def jwrite(p,s):write(p,json.dumps(s,ensure_ascii=False,indent=2)+'\n')

def flower(x=310,y=180,r=74,stem=True,cream=False):
 red='#F2EBD9' if cream else '#D84228';ink='#F2EBD9' if cream else '#211F1B'
 s=''
 if stem:
  s+=f'<path d="M{x} {y+54} C{x+12} 370 {x-34} 450 {x-19} 610" stroke="{ink}" stroke-width="10" fill="none"/>'
  s+=f'<path d="M{x-9} 448 Q{x-137} 343 {x-122} 427 Q{x-108} 477 {x-9} 448 Z" fill="{ink}" stroke="none"/>'
  s+=f'<path d="M{x-8} 388 Q{x+130} 277 {x+122} 365 Q{x+95} 403 {x-8} 388 Z" fill="{ink}" stroke="none"/>'
 for n in range(8):
  a=n*math.pi/4;cx=x+math.cos(a)*r;cy=y+math.sin(a)*r
  s+=f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{r*.65:.2f}" ry="{r*.43:.2f}" transform="rotate({n*45} {cx:.2f} {cy:.2f})" fill="{red}" stroke="none"/>'
 s+=f'<circle cx="{x}" cy="{y}" r="{r*.46}" fill="{ink}" stroke="none"/>'
 return s
def svg(content,view='0 0 620 660',label='一輪の花'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" fill="none" stroke="none" role="img" aria-label="{label}">{content}</svg>'
def bouquet(cream=False):
 ink='#F2EBD9' if cream else '#211F1B'
 s=''
 for x,y,r in [(200,212,60),(322,133,73),(435,220,55)]:
  s+=f'<path d="M{x} {y} L318 614" stroke="{ink}" stroke-width="8" fill="none"/>'
  s+=flower(x,y,r,False,False)
 s+=f'<path d="M207 359 L431 359 L362 583 L276 583 Z" fill="{ink}" stroke="none"/>'
 s+='<path d="M261 471 L370 471" stroke="#D84228" stroke-width="15" fill="none"/>'
 return svg(s,label='三輪の花をまとめた花束')

CSS='''
*{box-sizing:border-box}body{margin:0;background:#ccc;color:#211F1B;font-family:"BIZ UDPGothic",sans-serif}.slide{position:relative;width:1280px;height:720px;overflow:hidden;background:#F2EBD9;margin:0}h1,h2,h3,p{margin:0}.jp-dela{font-family:"Dela Gothic One",sans-serif;font-weight:400}.jp-mincho{font-family:"Shippori Mincho",serif;font-weight:700}.number{font-family:"Manrope",sans-serif}.red{color:#D84228}.ink{background:#211F1B}.label{position:absolute;font-size:21px;line-height:1.5;letter-spacing:2px}.foot{position:absolute;left:65px;bottom:25px;width:1050px;font-size:17px;line-height:1.45;color:#6D675C}.page{position:absolute;right:64px;bottom:27px;font-size:18px}.body{font-size:30px;line-height:1.75}.art svg{width:100%;height:100%}.fine-line{height:2px;background:#211F1B}.rule-white{height:2px;background:#F2EBD9}
.s1 h1{position:absolute;left:62px;top:222px;width:900px;font-size:108px;line-height:1.35;letter-spacing:10px}.s1 .intro{position:absolute;left:72px;top:525px;width:710px;font-size:29px;line-height:1.8}.s1 .art{position:absolute;left:802px;top:70px;width:450px;height:650px}.s1 .label{left:68px;top:52px}.s1 .accent{position:absolute;left:65px;top:172px;width:85px;height:8px;background:#D84228}
.s2 .art{position:absolute;left:48px;top:83px;width:420px;height:529px}.s2 .vase{position:absolute;left:214px;top:473px;width:110px;height:145px;background:#D84228;border-radius:0}.s2 .shelf{position:absolute;left:65px;top:615px;width:454px;height:10px;background:#211F1B}.s2 .label{left:640px;top:90px}.s2 h2{position:absolute;left:636px;top:174px;width:604px;font-size:64px;line-height:1.4;letter-spacing:-2px}.s2 .body{position:absolute;left:642px;top:476px;width:542px}.s2 .art-note{position:absolute;left:68px;top:637px;width:447px;font-size:18px;color:#6D675C}
.s3{background:#C03A24;color:#F2EBD9}.s3 .label{left:65px;top:52px}.s3 h2{position:absolute;left:64px;top:118px;width:1160px;font-size:68px;line-height:1.2;letter-spacing:-2px}.s3 .row{position:absolute;left:65px;top:252px;width:1150px;height:365px;display:flex;gap:68px}.s3 .step{position:relative;width:338px;height:365px}.s3 .step-n{position:absolute;left:0;top:0;font-size:76px;line-height:1;color:#211F1B}.s3 .step h3{position:absolute;left:0;top:104px;font-size:49px;line-height:1.2}.s3 .step .body{position:absolute;left:0;top:190px;width:322px;font-size:27px;line-height:1.8}.s3 .vertical{position:absolute;left:365px;top:253px;width:2px;height:350px;background:#F2EBD9}.s3 .v2{left:771px}.s3 .label,.s3 .foot,.s3 .page{color:#F2EBD9}.s3 .small-flower{position:absolute;right:4px;top:0;width:82px;height:86px}.s3 .small-flower svg{width:100%;height:100%}
.s4{background:#211F1B;color:#F2EBD9}.s4 .label{left:65px;top:58px}.s4 h2{position:absolute;left:64px;top:171px;width:765px;font-size:72px;line-height:1.35;letter-spacing:-3px}.s4 .body{position:absolute;left:70px;top:420px;width:699px;font-size:28px}.s4 .art{position:absolute;left:807px;top:110px;width:438px;height:563px}.s4 .fine-line{position:absolute;left:68px;top:590px;width:620px;background:#D84228}.s4 .rest{position:absolute;left:68px;top:611px;width:718px;font-size:21px;color:#F2EBD9}.s4 .foot{color:#BAAFA0}
.s5 .label{left:65px;top:55px}.s5 .big-disc{position:absolute;left:869px;top:125px;width:318px;height:318px;border-radius:50%;background:#D84228}.s5 h2{position:absolute;left:66px;top:163px;width:1070px;font-size:77px;line-height:1.35;letter-spacing:-3px}.s5 .body{position:absolute;left:73px;top:450px;width:1070px;font-size:27px;line-height:1.8}.s5 .definition{position:absolute;left:73px;top:590px;width:1120px;font-size:20px}.s5 .close-line{position:absolute;left:68px;top:416px;width:740px;height:4px;background:#211F1B}
'''

def markup():
 single=svg(flower())
 white_head=svg(flower(180,180,65,False,True),'70 70 220 220','花の形')
 bodies=[
 f'<p class="label">花の定期便　提供案</p><div class="accent"></div><h1 class="jp-dela">花を、<br>一本から。</h1><p class="intro">花のある暮らしを、<br>小さな一輪から始める。</p><div class="art">{single}</div>',
 f'<div class="art">{single}</div><div class="vase"></div><div class="shelf"></div><p class="art-note">窓辺、机、玄関。小さな器と、いつもの場所。</p><p class="label">小さく始める</p><h2 class="jp-mincho">一本なら、<br>置く場所を<br>選べる。</h2><p class="body">大きな花束を置く前に、<br>ふだんの景色へ、一輪。</p>',
 '<p class="label">利用の流れ　提供案</p><h2 class="jp-mincho">選ぶ。届く。飾る。</h2><div class="vertical"></div><div class="vertical v2"></div><div class="row">'+''.join(f'<div class="step"><p class="step-n number">{n+1:02}</p><div class="small-flower">{white_head}</div><h3 class="jp-mincho">{title}</h3><p class="body">{body}</p></div>' for n,(title,body) in enumerate([('選ぶ。','好きな雰囲気を伝える。<br>花の選び方は、検討中。'),('届く。','受け取る日を決める。<br>配送方法は、これから。'),('飾る。','小さな器に、一輪。<br>飾り方の案も添える。')]))+'</div>',
 f'<p class="label">暮らしに合わせる　提供案</p><h2 class="jp-mincho">束にする日も、<br>休む日も。</h2><p class="body">受け取る本数と頻度を、<br>暮らしのリズムに合わせて選ぶ。</p><div class="art">{bouquet(True)}</div><div class="fine-line"></div><p class="rest">本数の変更・お休みは機能案です。販売条件は未確定。</p>',
 '<p class="label">これから決めること</p><div class="big-disc"></div><h2 class="jp-mincho">次の一輪を、<br>楽しみにする。</h2><div class="close-line"></div><p class="body">価格、配送地域、花の選び方は未確定。<br>季節と配送品質を確かめながら、内容を決める。</p><p class="definition">この資料は架空サービスの提供案です。受付中の商品や、導入実績ではありません。</p>'
 ]
 return '\n'.join(f'<section class="slide s{n+1}" aria-label="{TITLES[n]}">{b}<p class="foot">架空サービスの提供案。価格・配送条件・提供内容は未確定。</p><p class="page number">{n+1:02} / 05</p></section>' for n,b in enumerate(bodies))

def main(case_only=False):
 OUT.mkdir(parents=True,exist_ok=True);FORK.mkdir(parents=True,exist_ok=True)
 shutil.copytree(UP/'scripts',OUT/'upstream/scripts',dirs_exist_ok=True)
 for f in ['SKILL.md','LICENSE.txt','package.json']:shutil.copy2(UP/f,OUT/'upstream'/f)
 shutil.copy2(UP/'LICENSE.txt',OUT/'LICENSE.txt')
 # A local derivative preserves the original command while fixing its one-font coercion.
 runtime=OUT/'runtime/scripts';shutil.copytree(UP/'scripts',runtime,dirs_exist_ok=True)
 cp=runtime/'html_to_editable_pptx.js';code=cp.read_text(encoding='utf-8')
 code=code.replace('fontSize: s.fontSize,','fontFamily: s.fontFamily,\n        fontSize: s.fontSize,')
 code=code.replace('fontFace: opts.fontFace,\n        fontSize:','fontFace: (rs.fontFamily || style.fontFamily || opts.fontFace).split(",")[0].replace(/[\'\"]/g, "").trim(),\n        fontSize:')
 code=code.replace('fontFace: opts.fontFace,\n    fontSize:','fontFace: (style.fontFamily || opts.fontFace).split(",")[0].replace(/[\'\"]/g, "").trim(),\n    fontSize:')
 code=code.replace('return clone.outerHTML;', 'const viewport = svg.getBoundingClientRect();\n      clone.setAttribute("width", String(viewport.width));\n      clone.setAttribute("height", String(viewport.height));\n      return clone.outerHTML;')
 code=code.replace('lang: "zh-CN"','lang: "ja-JP"').replace('pptx.lang = "zh-CN"','pptx.lang = "ja-JP"')
 write(cp,code)
 fonts=[('delagothicone','DelaGothicOne-Regular.ttf','Dela Gothic One',400),('shipporimincho','ShipporiMincho-Bold.ttf','Shippori Mincho',700),('bizudpgothic','BIZUDPGothic-Regular.ttf','BIZ UDPGothic',400),('bizudpgothic','BIZUDPGothic-Bold.ttf','BIZ UDPGothic',700),('manrope','Manrope[wght].ttf','Manrope','200 800')]
 fontcss=''
 for folder,file,family,weight in fonts:
  (OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(ROOT/'downloads/fonts'/folder/file,OUT/'fonts'/file);shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt')
  fontcss+=f'@font-face{{font-family:"{family}";src:url("fonts/{file}");font-weight:{weight};font-display:block}}\n'
 html='<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+TITLE+'</title><style>'+fontcss+CSS+'</style></head><body>'+markup()+'</body></html>'
 write(OUT/'source.html',html);write(OUT/'PROMPT.md',PROMPT+'\n');write(OUT/'input/BRIEF.md','# 制作依頼\n\n'+PROMPT+'\n')
 jwrite(OUT/'input/data.json',{'title':TITLE,'titles':TITLES,'notes':NOTES,'page_count':5,'style':'bold','format':'editable PPTX','palette':['#F2EBD9','#D84228','#C03A24','#211F1B'],'sample_notice':'架空サービスの提供案。価格・配送地域・販売条件・花の選択範囲は未確定。'})
 env=os.environ.copy();env['NODE_PATH']=str(MODULES)
 cmd=[str(NODE),str(runtime/'html_to_ppt.js'),'--input',str(OUT/'source.html'),'--out-dir',str(OUT),'--name','deck','--no-preview','--font-face','BIZ UDPGothic','--viewport-width','1280','--viewport-height','720']
 result=subprocess.run(cmd,env=env,capture_output=True,text=True,encoding='utf-8',check=True)
 write(OUT/'conversion.json',result.stdout);print(result.stdout)
 shutil.copy2(OUT/'deck-editable.pptx',OUT/'deck.pptx')
 # Editable source SVG is extracted by the original converter, not flattened with text.
 refs=[{'path':f,'sha256':hashlib.sha256((UP/f).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{PIN}/{f}'} for f in ['SKILL.md','scripts/html_to_ppt.js','scripts/html_to_editable_pptx.js','scripts/generate_ppt.js','LICENSE.txt']]
 deps=[]
 for name in ['playwright','pptxgenjs','sharp','jszip']:
  pkg=json.loads((MODULES/name/'package.json').read_text(encoding='utf-8'))
  deps.append({'package':name,'version':pkg['version'],'license':pkg['license'],'bundled_in_kit':False})
 jwrite(OUT/'runtime/DEPENDENCIES.json',deps)
 provenance={'repository':REPO,'commit':PIN,'license':'MIT','author':'LearnAIHubC','official':False,'method':'Original HTML-to-PPT alias and converter: Chromium DOM measurement, native text/rectangle/ellipse reconstruction, inline SVG extraction with individual PNG compatibility images.','original_source_preserved':True,'source_refs':refs,'original_cli_executed':'runtime/scripts/html_to_ppt.js --input source.html --out-dir . --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720','modifications':['Local converter only: collect computed fontFamily for elements/text runs and use its first family instead of forcing every run to one font.','Local converter language metadata changed zh-CN to ja-JP.','SVG export local repair: persist actual DOM viewport width/height before sharp rasterization so preserveAspectRatio letterboxing survives PPTX placement. Original DOM measurement, native reconstruction and gradient patch pipeline retained.'],'editability':{'text':'Native editable text boxes with Dela/Shippori/BIZ roles.','shapes':'Native background, bar, ellipse, vase, shelf and divider shapes.','flowers':'Separate PNG image objects from SVG; SVG sources retained. Petals are not native editable PowerPoint shapes.'},'font_notice':'Actual unmodified Google Fonts TTF and OFL included; PPTX does not embed fonts. Registered fonts used for local PowerPoint rendering.','fonts':[{'family':family,'file':file,'weight':weight,'source_commit':'66928797f271fed5ee428544e7229685e2d90127','license':'OFL-1.1'} for folder,file,family,weight in fonts],'dependencies':deps,'artifact_tool_used':False}
 jwrite(OUT/'PROVENANCE.json',provenance);jwrite(OUT/'SOURCE.json',provenance)
 write(OUT/'README.md','''# 花を、一本から。

架空の花の定期便サービスの提供案、5枚。価格・配送地域・販売条件・花の選択範囲は未確定です。実際の営業案内や導入実績ではありません。

原典LearnDeckのHTML-to-PPTモードを実行しました。元html_to_ppt.jsがhtml_to_editable_pptx.jsを呼び、Chromiumでsource.htmlのDOM座標を測定。PptxGenJSでnative文字・rectangle/ellipse等を組み、SVGを個別PNG画像へ変換して配置します。花のSVGはdeck-assets/svg/に残ります。全文の一枚画像へはしていません。

PPTXの文字、背景、丸、帯、花器、棚、区切り線は編集可能。花のpetal/stemは個別PNG画像で、native PowerPoint shapeではありません。元SVGとHTMLは編集可能です。原典converterは一つの--font-faceへ全て固定するため、本作例のruntime/だけcomputed fontFamilyを拾ってDela/Shippori/BIZを保存する局所変更とja-JP metadataを追加しました。未変更の原本はupstream/、変更点はPROVENANCE.jsonです。

再変換: Node18+にplaywright/pptxgenjs/sharp/jszipを用意し、Chromiumを入れて `node runtime/scripts/html_to_ppt.js --input source.html --out-dir . --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720`。Codexではload_workspace_dependenciesのNodeとNODE_PATHを使えます。HTML/CSSはsource.html内、依頼文はPROMPT.md、原データはinput/data.jsonです。

原作者LearnAIHubC、使用pinはSOURCE.json。原典MITをLICENSE.txtに保持。非公式の日本語作例です。Google Fontsの未改変TTFと原文OFLをfonts/へ同梱。PPTXはフォント未埋込なので別端末ではこれらの書体を手動導入してください。Windows fontsから抽出していません。

今回の明示修正依頼ではsource.html修正→元converter再実行→HTMLとPowerPoint全頁の描画・目視を行います。実行記録はQA.jsonとsource/の照合記録を参照。独立再評価とZIP再実行は別記録です。index.htmlはPowerPoint表示のPNGプレビューです。HTMLとPowerPointの文字組みが完全に一致する保証ではありません。
''')
 write(FORK/'SKILL.md','''---
name: learndeck-ja
description: LearnDeck原典のHTML-to-PPT DOM実測converterで、日本語HTMLからnative文字と図形・個別SVG画像を持つPPTXを作る。
---

# LearnDeck 日本語版（非公式）

1. 題材、枚数、確定事項と提供案を短く整理。style指定があれば再質問せず従う。各ページに一つの主張を置き、巨大見出しと役割のある図をHTML .slideで作る。
2. 同梱upstream/SKILL.mdを必要範囲で読む。新規計画は原典generate_ppt.jsも使える。本作例は柔軟な日本語bold構図のためHTML-to-PPT modeを使う。
3. local runtime/scripts/html_to_ppt.jsで変換する。ChromiumのDOM位置が正本。playwright/pptxgenjs/sharp/jszipを用意し、Codexではload_workspace_dependenciesのNode/NODE_PATHを使う。
4. 原典は既定で追加検査を省略するが、明示された修正・検証依頼では元HTMLを直して同じconverterを再実行する。HTMLとPowerPointを全頁描画して字間・改行・余白を目視し、native要素とSVG由来PNGの分離を記録する。
5. Native text/background/rect/ellipseと、SVG由来の個別PNG imageを区別して伝える。SVG元と実TTF/OFL、原MIT、source.htmlを保全。PPTXフォント未埋込時は別端末への導入が必要と説明する。

本forkのruntimeだけ、原典converterの単一font-face固定をcomputed fontFamilyで置換し、roleごとの日本語書体を保存。languageはja-JP。未変更原本はupstream/scripts。SVG書き出し時は実DOMのviewport幅・高さを保存し、SVGのpreserveAspectRatioをPNGへ反映する局所補正も適用。その他のDOM/native object/gradient pipelineは原典のまま。

具体例と入力はexample/に同梱。`node runtime/scripts/html_to_ppt.js --input example/source.html --out-dir output --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720`。画像をnative shapeと称さず、提供案を実績と称さない。

原作者LearnAIHubC。https://github.com/LearnAIHubC/LearnDeck 。MIT帰属はLICENSE.txt、使用pinはSOURCE.json。書体は各OFL。公式・原作者の公認ではありません。
''')
 shutil.copytree(OUT/'upstream',FORK/'upstream',dirs_exist_ok=True);shutil.copytree(OUT/'runtime',FORK/'runtime',dirs_exist_ok=True);shutil.copy2(OUT/'LICENSE.txt',FORK/'LICENSE.txt');jwrite(FORK/'SOURCE.json',provenance)
 write(FORK/'README.md','# LearnDeck日本語キット\n\n非公式の日本語改変。原典MITを保持、書体はOFL。example/deck.pptxとexample/source.html、原典と局所変更版runtimeを同梱。SVG由来の花は個別PNG画像、文字と基本図形はnative editableです。\n')
 jwrite(OUT/'QA.json',{'status':'generated','generation':'Original HTML-to-PPT converter executed --no-preview; five editable slides generated.','checks':[],'limits':['PowerPoint first display pending','No additional validation or full-page detailed audit.']})
 if not case_only:fragments(refs,provenance)
 print('LearnDeck generated:',OUT/'deck.pptx')

def fragments(refs,provenance):
 base='examples/repositories/learndeck-showcase/'
 case={'id':'learndeck-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'learndeck-ja','page_count':5,'format':'pptx','preview_kind':'powerpoint-render','preview_canvas':{'width':1600,'height':900},'style':'強い朱赤 × 紙色 × 墨黒 / 巨大和文と一輪','use_case':'架空サービスの提供案','preview':base+'index.html','cover':base+'render/slide-01.png','interior':base+'render/slide-04.png','pages':[base+f'render/slide-{n:02}.png' for n in range(1,6)],'artifact_download':'downloads/learndeck-example-ja.zip','source_download':'downloads/learndeck-example-ja.zip','fork_download':'downloads/learndeck-ja.zip','pptx_download':base+'deck.pptx','pdf_download':base+'render/deck.pdf','input':base+'input/BRIEF.md','input_data':base+'input/data.json','prompt':base+'PROMPT.md','prompt_text':PROMPT,'provenance':base+'PROVENANCE.json','qa':base+'QA.json','guide':base+'README.md','titles':TITLES,'notes':NOTES,'sample_notice':'架空サービスの提供案。価格・配送条件・提供内容は未確定。','method':provenance['method'],'navigation':'native-runtime-bridge','editability':'Native text and basic shapes; separate flower PNGs with original SVG retained.','status':'generated','execution_status':'generated','preview_notice':'LearnDeck原典DOM converterで生成。native文字・基本図形、花は個別PNG画像。','representative_previews':[base+'render/slide-01.png',base+'render/slide-04.png'],'preview_image_notice':'5枚のPowerPoint初回書き出しPNG。全ページ詳細目視は未実施。'}
 guide={'repository':REPO,'production_status':'generated','execution_status':'generated','execution_type':'original_html_to_ppt_dom_native_with_local_font_family_extension','case_ids':[case['id']],'summary_ja':'LearnDeck原典DOM実測converterで花の提供案5枚をPPTX化。大きな和文、native基本図形、個別花SVG/PNG。','requirements':['Node18+','playwright/pptxgenjs/sharp/jszip','Chromium','PPTX閲覧用PowerPoint等'],'steps':['source.htmlで日本語bold構図を作る','原典HTML-to-PPT alias/converterを--no-preview実行','SVG元と実TTF/OFLを保全','完成PPTXを初回表示する'],'commands':['node runtime/scripts/html_to_ppt.js --input source.html --out-dir . --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720'],'source_refs':refs,'upstream_commit':PIN,'license':'MIT','license_notice_ja':'原典softwareはMIT、同梱書体はOFL。日本語改変と未変更原本を保持。','caveats':['PPTX flower SVG visuals are separate PNG compatibility images, not editable petal shapes.','PPTX fonts are not embedded; full original TTF/OFL supplied.','Local converter adds computed fontFamily, ja-JP and DOM SVG viewport preservation.','Fictional offer; prices, shipping area and terms undecided.'],'skill':'skill-forks/learndeck-ja/SKILL.md','guide':case['guide']}
 jwrite(ROOT/'data/sol-learndeck-repository-examples.json',[case]);jwrite(ROOT/'data/sol-learndeck-repository-guides.json',[guide])

def viewer():
 html='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>花を、一本から。</title><style>*{box-sizing:border-box}body{margin:0;background:#211F1B;display:grid;place-items:center;height:100vh}.stage{width:min(100vw,177.777vh);aspect-ratio:16/9;position:relative}img{width:100%;height:100%;object-fit:contain}nav{position:fixed;bottom:12px;right:16px;display:flex;gap:12px;align-items:center;background:#211F1B;color:#F2EBD9;padding:8px 15px;font-family:sans-serif}button{font:inherit;background:transparent;border:1px solid #F2EBD9;color:#F2EBD9;padding:7px 14px}span{font-size:15px}.embed nav{display:none}</style><div class="stage"><img id="slide" src="render/slide-01.png" alt="花を、一本から。"></div><nav aria-label="スライド操作"><button id="previous">戻る</button><span id="count">1 / 5</span><button id="next">進む</button></nav><script>const titles=TITLES;let n=0;function show(i){n=Math.max(0,Math.min(4,i));document.querySelector('#slide').src='render/slide-'+String(n+1).padStart(2,'0')+'.png';document.querySelector('#slide').alt=titles[n];document.querySelector('#count').textContent=(n+1)+' / 5';if(parent!==window)parent.postMessage({type:'yebisu-page',index:n,total:5},location.origin)}document.querySelector('#previous').onclick=()=>show(n-1);document.querySelector('#next').onclick=()=>show(n+1);addEventListener('keydown',e=>{if(e.key==='ArrowRight')show(n+1);if(e.key==='ArrowLeft')show(n-1);if(e.key==='Home')show(0);if(e.key==='End')show(4)});addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))show(e.data.index)});if(parent!==window)document.body.classList.add('embed');show(0)</script></html>'''
 write(OUT/'index.html',html.replace('const titles=TITLES;',f'const titles={json.dumps(TITLES,ensure_ascii=False)};'))

def package():
 excluded={'.private','backups','.build','.git','__pycache__','node_modules','cache'}
 def ignore(folder,names):return [n for n in names if n in excluded or n.endswith(('.pyc','.log')) or (Path(folder)/n).is_symlink() or ((Path(folder)/n).is_dir() and os.path.isjunction(Path(folder)/n))]
 viewer();shutil.copytree(OUT,FORK/'example',dirs_exist_ok=True,ignore=ignore)
 for folder,name in [(OUT,'learndeck-example-ja'),(FORK,'learndeck-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for current,dirs,files in os.walk(folder,followlinks=False):
    dirs[:]=[d for d in dirs if d not in ignore(current,dirs)]
    for file in sorted(files):
     p=Path(current)/file
     if file not in ignore(current,[file]):z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--package-only',action='store_true');parser.add_argument('--case-only',action='store_true');args=parser.parse_args()
 if args.package_only:package()
 else:main(case_only=args.case_only)

