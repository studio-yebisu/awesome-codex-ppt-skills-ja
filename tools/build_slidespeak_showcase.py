"""Bespoke Japanese style package rendered through SlideSpeak's actual engine."""
from pathlib import Path
import base64,hashlib,json,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'examples/repositories/slidespeak-showcase';FORK=ROOT/'skill-forks/slidespeak-ja';UP=ROOT/'.build/actual-upstreams/SlideSpeak__slide-design-skill'
REPO='SlideSpeak/slide-design-skill';COMMIT='5e87d8ae71f6306e0c88f4910e6c09114581d91b'
TITLE='本の向こうへ。 架空の独立書店のリブランディング案'
PROMPT='SlideSpeak/slide-design-skill原典engine API、slide templates、gate、rendererを使い、日本語6ページ「本の向こうへ。」を制作。架空の独立書店「余白書店」の仮リブランディング案。緑のベタ、生成り、墨黒。誌面風の大きな和文と伸びた罫線、本のページを開くコード図形。Zen Kaku Gothic New・Shippori Mincho・Manropeで役割を分ける。既存presetを借りず、briefからtokens/chrome/6templatesをauthoringし、Solが完成slide-treeのslotsを作る。原典generateDeck/loadSkill/wrapAsStandaloneHtml経由で実HTMLを出す。売上実績や効果数値、実在のロゴ・書影は使わない。FAL/API課金なし。'
SLIDES=[
 {'type':'cover','density':'editorial','slots':{'title':'本の向こうへ。','subtitle':'読んだあとに、景色が少し変わる。','label':'余白書店 / リブランディング案（仮）','notice':'架空の独立書店の企画。実在店舗の実績ではありません。'}},
 {'type':'statement','density':'editorial','slots':{'title':'探していた本と、\nまだ知らない自分に。','body':'本を売る場所から、次の関心がひらく場所へ。','label':'店の約束を、言葉にする。'}},
 {'type':'quote','density':'editorial','slots':{'title':'「この棚の隣も、\n見てみたい。」','body':'一冊の出会いが、もうひとつの問いにつながる。','label':'企画の言葉（仮） / 利用者の実際の発言ではありません。'}},
 {'type':'split','density':'balanced','slots':{'title':'緑は、\n街の目印。','body':'大きな文字と、長い罫線。\n読む順番を整え、\n棚の続きがあることを伝える。','caption':'書影や実在ロゴを用いず、ページを開く形をコードで描く。','label':'見た目の提案 / 色は印刷サンプルで確認する。'}},
 {'type':'timeline','density':'balanced','slots':{'title':'言葉から、店先まで。','first':'店の声を集める。','second':'小さく形にする。','third':'続け方を決める。','one':'店主の思いと、\n棚の案内を整理。','two':'看板と棚札を試作し、\n読みやすさを確認。','three':'素材・費用・運営の負担を見て、\n採用範囲を決める。','label':'試行の順序案 / 日程や実施決定ではありません。'}},
 {'type':'closing','density':'editorial','slots':{'title':'一冊の先に、\n街の続き。','body':'余白書店の、新しい入口を。','label':'仮の提案 / 採用・実施・効果の主張ではありません。'}}]
CSS=r'''
.slide{position:relative;overflow:hidden;color:#11211b;background:#f1eddf;font-family:"Zen Kaku Gothic New",sans-serif;padding:0!important}
.slide h1,.slide h2,.slide p{margin:0}.slide h1,.slide h2{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;line-height:1.24;letter-spacing:-5px}
.bookgreen{background:#146846;color:#f1eddf}.slide .book-label{position:absolute;left:110px;top:72px;font-size:27px;line-height:1.6}.slide .book-footer{position:absolute;left:110px;bottom:45px;font-size:23px;line-height:1.5}.slide .folio{position:absolute;right:100px;bottom:46px;font-family:Manrope,sans-serif;font-size:26px}
.slide .long-rule{position:absolute;left:110px;top:146px;width:1700px;height:2px;background:currentColor}.slide .lower-rule{position:absolute;left:110px;bottom:115px;width:1700px;height:2px;background:currentColor}
.book-cover h1{position:absolute;left:100px;top:275px;font-size:155px;width:1150px}.book-cover .sub{position:absolute;left:113px;top:680px;font-size:44px;line-height:1.8}.book-cover svg{position:absolute;right:100px;top:355px;width:590px;height:470px}
.book-statement h2{white-space:pre-line;position:absolute;left:105px;top:268px;width:1390px;font-size:127px;line-height:1.36}.book-statement .sub{position:absolute;left:113px;top:770px;font-size:42px}.book-statement .spine{position:absolute;right:145px;top:240px;width:80px;height:660px;border-left:4px solid #146846;border-right:4px solid #146846}
.book-quote h2{white-space:pre-line;position:absolute;left:150px;top:277px;width:1540px;font-family:"Shippori Mincho",serif;font-weight:700;font-size:120px;line-height:1.55;letter-spacing:-3px}.book-quote .sub{position:absolute;left:163px;top:760px;font-size:39px}.book-quote .quote-mark{position:absolute;left:108px;top:225px;width:25px;height:580px;background:#146846}
.book-split h2{white-space:pre-line;position:absolute;left:110px;top:182px;width:830px;font-size:109px}.book-split .sub{white-space:pre-line;position:absolute;left:115px;top:625px;width:745px;font-size:38px;line-height:1.9}.book-split .caption{position:absolute;left:1120px;top:793px;width:650px;font-size:27px;line-height:1.8}.book-split svg{position:absolute;left:1050px;top:248px;width:720px;height:465px}.book-split .vertical{position:absolute;left:977px;top:217px;height:660px;width:2px;background:#146846}
.book-timeline h2{position:absolute;left:110px;top:220px;font-size:116px}.book-timeline .process{position:absolute;left:110px;top:540px;width:1670px;display:grid;grid-template-columns:repeat(3,1fr);gap:62px}.book-timeline .step{position:relative;border-top:3px solid #146846;padding-top:38px}.book-timeline .step h3{font-size:47px;line-height:1.5;font-weight:900}.book-timeline .step p{white-space:pre-line;font-size:32px;line-height:1.85;margin-top:25px}.book-timeline .step b{font:600 38px Manrope,sans-serif;display:block;margin-bottom:19px;color:#146846}.book-timeline svg{position:absolute;right:90px;top:255px;width:290px;height:105px}
.book-closing h2{white-space:pre-line;position:absolute;left:105px;top:263px;width:1280px;font-size:142px;line-height:1.36}.book-closing .sub{position:absolute;left:115px;top:761px;font-size:43px}.book-closing svg{position:absolute;right:100px;top:420px;width:460px;height:310px}
.slide[data-density="editorial"] .sub{max-width:1380px}.slide[data-density="balanced"] .book-label{font-size:27px}
'''
BOOK='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 460" data-visual-event="signature-mark"><path d="M300 420 L45 315 V40 L300 146 L555 40 V315 Z" fill="none" stroke="currentColor" stroke-width="3"/><path d="M300 146 V420 M75 80 L275 163 M75 122 L275 205 M325 163 L525 80 M325 205 L525 122" stroke="currentColor" fill="none" stroke-width="3"/></svg>'
ARROW='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" data-visual-event="signature-mark"><path d="M25 150 H430 M300 35 L440 150 L300 265" stroke="currentColor" fill="none" stroke-width="4"/></svg>'
def footer():return '<div class="lower-rule"></div><p class="book-footer">{{label}}</p>'
def common():return '<div class="long-rule"></div>'
COMPONENTS='\n'.join([
 '<template id="slide-cover"><section class="slide bookgreen book-cover"><p class="book-label">{{label}}</p>'+common()+'<h1>{{title}}</h1><p class="sub">{{subtitle}}</p>'+BOOK+'<div class="lower-rule"></div><p class="book-footer">{{notice}}</p></section></template>',
 '<template id="slide-statement"><section class="slide book-statement">'+common()+'<h2>{{title}}</h2><p class="sub">{{body}}</p><div class="spine" data-visual-event="signature-mark"></div>'+footer()+'</section></template>',
 '<template id="slide-quote"><section class="slide book-quote">'+common()+'<div class="quote-mark"></div><h2>{{title}}</h2><p class="sub">{{body}}</p>'+footer()+'</section></template>',
 '<template id="slide-split"><section class="slide book-split">'+common()+'<h2>{{title}}</h2><p class="sub">{{body}}</p><div class="vertical"></div>'+BOOK+'<p class="caption">{{caption}}</p>'+footer()+'</section></template>',
 '<template id="slide-timeline"><section class="slide book-timeline">'+common()+'<h2>{{title}}</h2>'+ARROW+'<div class="process"><div class="step" data-visual-event="item-marker"><b>01</b><h3>{{first}}</h3><p>{{one}}</p></div><div class="step" data-visual-event="item-marker"><b>02</b><h3>{{second}}</h3><p>{{two}}</p></div><div class="step" data-visual-event="item-marker"><b>03</b><h3>{{third}}</h3><p>{{three}}</p></div></div>'+footer()+'</section></template>',
 '<template id="slide-closing"><section class="slide bookgreen book-closing">'+common()+'<h2>{{title}}</h2><p class="sub">{{body}}</p>'+ARROW+footer()+'</section></template>'
])
RUNTIME=r'''import{readFile,writeFile}from'node:fs/promises';import{dirname,join}from'node:path';import{fileURLToPath}from'node:url';import{generateDeck,loadSkill,wrapAsStandaloneHtml}from'./upstream/engine/index.ts';
const here=dirname(fileURLToPath(import.meta.url));const data=JSON.parse(await readFile(join(here,'input/slide-tree.json'),'utf8'));const brief=await readFile(join(here,'PROMPT.txt'),'utf8');
const llm={async generateSlideTree(prompt:string){await writeFile(join(here,'input/engine-prompt.txt'),prompt);return data;}};
const result=await generateDeck({skillName:'green-book-editorial',userPrompt:brief,slideCount:6,imageBudget:0,maxFalCalls:0,language:'ja',illustrative:true},{skillsRoot:join(here,'styles'),llm,images:{async resolve(){throw new Error('No image requests permitted in this authored deck')}}});
if(result.slides.length!==6)throw new Error('Engine did not deliver six slides');const skill=await loadSkill(join(here,'styles/green-book-editorial'));let html=wrapAsStandaloneHtml(skill,result.slides).replace('lang="en"','lang="ja"');await writeFile(join(here,'deck.html'),html);const bridge=await readFile(join(here,'player-adapter.html'),'utf8');await writeFile(join(here,'index.html'),html.replace('</body>',bridge+'</body>'));await writeFile(join(here,'engine-result.json'),JSON.stringify({...result,slides:result.slides.map(s=>({type:s.type})),client:'Sol-authored persisted slide-tree supplied through engine LLMClient. No external LLM call.'},null,2));console.log('Original engine rendered six bespoke slides.');
'''
PLAYER=r'''<style>html,body{width:100%;height:100%;overflow:hidden;margin:0;padding:0!important;background:#101b16}.slide{position:absolute!important;left:0;top:0;margin:0!important;box-shadow:none!important;visibility:hidden;transform-origin:0 0}.slide.active{visibility:visible}.book-controls{position:fixed;bottom:10px;right:15px;z-index:1000;background:#11211be0;color:#f1eddf;padding:8px 15px;display:flex;gap:13px;align-items:center;font:14px Manrope,sans-serif}.book-controls button{font:24px sans-serif;border:0;background:none;color:inherit;cursor:pointer}@media print{html,body{height:auto;overflow:visible;background:white}.slide{position:relative!important;visibility:visible;transform:none!important;page-break-after:always}.book-controls{display:none}}</style>
<nav class="book-controls"><button id="prev" aria-label="前へ">←</button><span id="counter"></span><button id="next" aria-label="次へ">→</button></nav><script>let n=0;const ss=[...document.querySelectorAll('.slide')];function scale(){let f=Math.min(innerWidth/1920,innerHeight/1080);ss.forEach(s=>s.style.transform=`translate(${(innerWidth-1920*f)/2}px,${(innerHeight-1080*f)/2}px) scale(${f})`)}function go(i){n=Math.max(0,Math.min(5,i));ss.forEach((s,k)=>s.classList.toggle('active',k===n));document.getElementById('counter').textContent=(n+1)+' / 6';if(parent!==window)parent.postMessage({type:'yebisu-page',index:n,total:6},location.origin)}addEventListener('resize',scale);addEventListener('keydown',e=>{if(['ArrowRight',' '].includes(e.key))go(n+1);if(e.key==='ArrowLeft')go(n-1)});addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))go(e.data.index)});document.getElementById('prev').onclick=()=>go(n-1);document.getElementById('next').onclick=()=>go(n+1);scale();go(0);</script>'''
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def main():
 OUT.mkdir(parents=True,exist_ok=True);FORK.mkdir(parents=True,exist_ok=True);style=OUT/'styles/green-book-editorial'
 fontcss=''
 for folder,filename,fam,weight in [('zenkakugothicnew','ZenKakuGothicNew-Regular.ttf','Zen Kaku Gothic New','400'),('zenkakugothicnew','ZenKakuGothicNew-Black.ttf','Zen Kaku Gothic New','900'),('shipporimincho','ShipporiMincho-Bold.ttf','Shippori Mincho','700'),('manrope','Manrope[wght].ttf','Manrope','200 800')]:
  src=ROOT/'downloads/fonts'/folder/filename;(OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(src,OUT/'fonts'/filename);shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt');fontcss+=f'@font-face{{font-family:"{fam}";src:url(data:font/ttf;base64,{base64.b64encode(src.read_bytes()).decode()});font-weight:{weight};font-display:block}}\n'
 write(style/'chrome.css',fontcss+CSS)
 tokens={'color':{'ground':{'page':'#F1EDDF','card':'#F1EDDF','ink':'#11211B'},'signal':{'primary':'#146846','subtle':'#0D4E33'},'support':{'muted':'#50695D','rule':'#146846'}},'type':{'header':{'family':'"Zen Kaku Gothic New", sans-serif','weight':900,'scale':[155,127,47,27]},'body':{'family':'"Zen Kaku Gothic New", sans-serif','weight':400,'scale':[38,32,27,23]},'data':{'family':'Manrope, sans-serif','weight':600}},'spacing':{'unit':4,'scale':[4,8,12,16,24,32,48,64,96]},'radius':{'card':0,'button':0,'input':0},'elevation':{'card':'none'},'icon':{'kit':'lucide'},'page':{'ratio':'16:9','width':1920,'height':1080,'safe':96}}
 write(style/'tokens.json',json.dumps(tokens,ensure_ascii=False,indent=2));write(style/'components.html',COMPONENTS)
 write(style/'SKILL.md','''---
name: green-book-editorial
version: 0.1.0
description: "架空書店のための緑・和文・罫線による編集誌style。"
inspiration: "本を開く動作と街に続く視線。独自briefから生成。"
typography_kit: "Zen Kaku Gothic New / Shippori Mincho / Manrope"
color_kit: "緑のベタ、生成り、墨黒"
image_style: "コードで描いた開いた本と矢印。写真・AI画像不要。"
forbidden: "カード量産、実在ロゴ、捏造数字、外部AI画像"
---

日本語の一頁一主張。意味のまとまりで改行。brief由来のstyleで既存presetは使わない。

## Graphic system
開いた本のSVGをsignature markに、長い罫線をstructureに、緑のベタ面をsurfaceにする。quoteは明朝、processは無枠の線と番号。余白は読む順序をつくる。
''')
 rows=[]
 for s,family in zip(SLIDES,['cover','statement','quote','split-visual','timeline','closing']):rows.append(f"| {s['type']} | {s['type']} page | {', '.join(s['slots'])} | page-no, page-total | {family} | |")
 write(style/'layout-grammar.md','| slide-type | when | required slots | optional slots | family | visual roles |\n|---|---|---|---|---|---|\n'+'\n'.join(rows)+'\n\n## Composition rules\n- First slide is cover, last is closing.\n- Alternate green fields and paper surfaces.\n- Each slide carries one dominant idea.\n')
 write(style/'image-style.md','Prompt template: `{subject}, editorial book shape, no logo`\nSearch-query template: `{subject} independent bookstore`\n- `product | person | building` → ask\nNo image requests in this authored deck.\n')
 write(OUT/'input/slide-tree.json',json.dumps({'slides':SLIDES},ensure_ascii=False,indent=2));write(OUT/'PROMPT.txt',PROMPT);write(OUT/'input/BRIEF.md','# リブランディング案（仮）\n\n'+PROMPT);write(OUT/'build.mts',RUNTIME);write(OUT/'player-adapter.html',PLAYER);write(OUT/'.gitignore','**/node_modules/\ncache/\n*.log\n')
 tsx=OUT/'upstream/node_modules/tsx/dist/cli.mjs'
 subprocess.run(['node',str(tsx),str(OUT/'upstream/scripts/validate-skill.ts'),str(OUT/'styles'),'green-book-editorial'],check=True,cwd=ROOT)
 subprocess.run(['node',str(tsx),str(OUT/'build.mts')],check=True,cwd=ROOT)
 html=(OUT/'deck.html').read_text(encoding='utf-8');write(OUT/'index.html',html.replace('</body>',PLAYER+'</body>'))
 finish()
def finish():
 source={'repository':REPO,'commit':COMMIT,'license':'MIT','scope':'Actual engine and bespoke Japanese style package','case_studies':['slidespeak-showcase'],'upstream_preserved':True}
 write(OUT/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2));shutil.copy2(UP/'LICENSE',OUT/'LICENSE')
 refs=[{'path':p,'sha256':hashlib.sha256((UP/p).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{COMMIT}/{p}'} for p in ['SKILL.md','docs/INTEGRATION.md','engine/index.ts','engine/renderer.ts','engine/skill-loader.ts','scripts/validate-skill.ts','LICENSE']]
 write(OUT/'PROVENANCE.json',json.dumps(dict(source,source_refs=refs,method='Bespoke authored tokens/chrome/components/grammar → original loadSkill → generateDeck with persisted Sol-authored slide-tree LLMClient → original validateSlideTree/brand guards → original renderer/wrapAsStandaloneHtml.',modifications=['No original preset reused; all six templates and tokens derive from this bookstore brief.','Original engine core unchanged. Player frame adapter is outside original slide output.','Local fonts added to chrome as full embedded TTF; original TTF/OFL packaged.','No paid AI or image service; LLMClient replays the current author-created JSON, not an external model call.']),ensure_ascii=False,indent=2))
 write(OUT/'README.md','''# 本の向こうへ。

架空の独立書店「余白書店」の仮リブランディング案、6ページ。緑のベタ、生成り、大きな和文、開いた本のコード図形、長い罫線で、店の言葉から試行の順序へつなぎます。実在書店の実績・実施決定・効果の主張は含みません。

原典SlideSpeak engineを実使用。独自briefからtokens/chrome/components/grammarを作者が設計し、Solが作成したslide-treeをLLMClientインターフェースへ渡し、原典loadSkill/generateDeck/validateSlideTree/rendererで生成。外部LLM/API/FALは呼びません。既存presetの名前借りや共通rendererへの置換ではありません。

`deck.html` は原典renderer出力。`index.html` は同じ出力に1920×1080再生とサイトframe連携だけを追加。書体はフルTTFを内包し、OFL原文をfonts/に同梱。原典MIT・engine sourceはupstream/に保持。

再生成: `cd upstream` → `npm ci` → `cd ..` → `node upstream/node_modules/tsx/dist/cli.mjs build.mts`。styleを変えるときはstyles/green-book-editorialの6ファイルとinput/slide-tree.jsonを編集。スタイルgate: `node upstream/node_modules/tsx/dist/cli.mjs upstream/scripts/validate-skill.ts styles green-book-editorial`（stylesを絶対パス指定可）。必要なruntimeは通常Node OSS依存だけ。

原典gateを実行し、全ページの改行・図・ページ移動を確認して直す。現在の実施範囲はQA.jsonへ記録する。独立再評価と区別する。
''')
 write(FORK/'SKILL.md','''---
name: slidespeak-ja
description: SlideSpeak原典engineでbrief由来の日本語styleを作り、実HTMLを生成する。
---

# 日本語の編集誌スライド

1. 同梱upstream/SKILL.md、docs/INTEGRATION.md、docs/SKILL-FORMAT.mdを読む。題材と見た目のbriefを決め、既存preset名で代用しない。
2. tokens、chrome、components、layout grammar、image-style、SKILLの6ファイルを作る。原典templates規約とgateに合わせる。見出し・本文・英数字の書体役割を決め、日本語は意味単位で改行し、過密ならページを分ける。
3. 原典loadSkill→generateDeck→wrapAsStandaloneHtmlを使う。LLMClientに完成slide-treeを渡し、原典検証・brand guard・rendererを通す。無料のコード図形だけでも制作できる。
4. build.mtsと独自style/入力を作品ZIPから利用。Node20+と `npm ci` が必要。原典gateを実行し、全頁の本文・図・改行・ページ移動を確認して直す。確認範囲を記録する。
5. 原典MIT、使用フォントの原TTF/OFLを保持。ホスト専有runtimeやAPI keyをZIPへ含めない。

技能本文だけではengineを含みません。一式ZIPのupstream sourceと作品ZIPのstyle/入力/build.mtsを使用。
''')
 if not (FORK/'upstream').exists():shutil.copytree(OUT/'upstream',FORK/'upstream',ignore=shutil.ignore_patterns('node_modules','.occ-measure*','*.log'))
 shutil.copy2(UP/'LICENSE',FORK/'LICENSE');source['files']=[{'path':p.relative_to(FORK).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json'];write(FORK/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 titles=[s['slots']['title'] for s in SLIDES];notes=['架空書店の仮提案です。読んだ先に新しい関心がひらく場所を目指します。','店の約束を、一冊と次の関心の出会いとして定める案です。','企画の言葉です。実際の利用者の発言や調査結果ではありません。','緑と大きな和文、開いたページの図形を提案。印刷色は試作で確かめます。','店の声、試作、採用範囲の順に進める案。日程と効果は確定していません。','本の先に街の続きがある、という店の入口を提案します。']
 case={'id':'slidespeak-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':COMMIT,'fork_id':'slidespeak-ja','page_count':6,'format':'html','preview_kind':'html','preview_canvas':{'width':1920,'height':1080},'style':'緑のベタ × 和文編集誌 / 本のページと長い罫線','use_case':'独立書店のリブランディング案','preview':'examples/repositories/slidespeak-showcase/index.html','cover':'examples/repositories/slidespeak-showcase/render/slide-01.png','interior':'examples/repositories/slidespeak-showcase/render/slide-01.png','artifact_download':'downloads/slidespeak-example-ja.zip','source_download':'downloads/slidespeak-example-ja.zip','fork_download':'downloads/slidespeak-ja.zip','input':'examples/repositories/slidespeak-showcase/input/BRIEF.md','input_data':'examples/repositories/slidespeak-showcase/input/slide-tree.json','prompt':'examples/repositories/slidespeak-showcase/PROMPT.txt','prompt_text':PROMPT,'provenance':'examples/repositories/slidespeak-showcase/PROVENANCE.json','qa':'examples/repositories/slidespeak-showcase/QA.json','guide':'examples/repositories/slidespeak-showcase/README.md','titles':titles,'notes':notes,'sample_notice':'架空の独立書店「余白書店」の仮提案。実在店舗の実績、採用、効果の主張ではありません。','method':'Original SlideSpeak engine/API/template renderer and bespoke author-created style, no external model/image calls.','navigation':'native-runtime-bridge','editability':'html_css_template_slots','status':'generated','execution_status':'generated','representative_previews':['examples/repositories/slidespeak-showcase/render/slide-01.png'],'preview_image_notice':'HTML全6ページの代表プレビュー1枚。全ページ目視は未実施。'}
 write(ROOT/'data/sol-slidespeak-repository-examples.json',json.dumps([case],ensure_ascii=False,indent=2))
 guide={'repository':REPO,'production_status':'generated','execution_status':'generated','execution_type':'original_engine_bespoke_style','case_ids':[case['id']],'summary_ja':'原典SlideSpeak engineで独自briefから設計した緑の和文編集誌6枚を実HTML化。外部API不要。','requirements':['Node20+','npm ci','原典engineと独自style'],'steps':['briefから6ファイルstyleを作る','slide-treeに日本語完成コピーを入れる','原典API/gate/rendererで生成する','主画面の初回表示を確認する'],'commands':['cd upstream && npm ci','node upstream/node_modules/tsx/dist/cli.mjs build.mts'],'source_refs':refs,'upstream_commit':COMMIT,'license':'MIT','skill':'skill-forks/slidespeak-ja/SKILL.md','guide':case['guide']};write(ROOT/'data/sol-slidespeak-repository-guides.json',json.dumps([guide],ensure_ascii=False,indent=2))
def package():
 for folder,name in [(OUT,'slidespeak-example-ja'),(FORK,'slidespeak-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.parts)&{'.private','node_modules','cache','__pycache__'} and p.suffix!='.log' and '.occ-measure' not in p.name:z.write(p,(Path(name)/p.relative_to(folder)).as_posix())
if __name__=='__main__':main()
