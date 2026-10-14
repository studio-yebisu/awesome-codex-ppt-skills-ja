"""Author a bespoke Japanese deck using frontend-slides' actual fixed-stage recipe."""
from pathlib import Path
import base64, hashlib, json, shutil, zipfile

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'.build/actual-upstreams/zarazhangrui__frontend-slides'
OUT=ROOT/'examples/repositories/sol-motion-showcase'
COMMIT='9906a34d640d2111f724544cbc50f7f130569ae1'
PROMPT='frontend-slides原典の固定1920×1080 stage・viewport-base.css全文・SlidePresentation構造を直接使い、日本語6ページ「夜の図書館 — 仕事帰りに出会う、次の一冊」を制作。架空の企画として明記。墨紺と蛍光ライム、大胆な和文タイポ、静かな余白、SVGの開いた本と都市の窓、段階的な入場アニメーション。問い→体験→選書→運営案→余韻の流れで、来館の動機を広告コピーにする。数値実績や実在施設を捏造しない。'

SLIDES=r'''
<section class="slide cover"><div class="eyebrow reveal">NIGHT LIBRARY / CONCEPT PROPOSAL</div><h1 class="reveal">夜の<br><span>図書館</span><i>。</i></h1><div class="cover-sub reveal">仕事帰りに出会う、<br>次の一冊。</div><svg class="book reveal" viewBox="0 0 680 680" aria-label="光のように開いた本"><path d="M340 540 L50 420 L50 100 L340 230 Z" fill="#d4ff43"/><path d="M340 540 L630 420 L630 100 L340 230 Z" fill="none" stroke="#d4ff43" stroke-width="3"/><path d="M365 260 L600 160 M365 310 L600 210 M365 360 L600 260 M365 410 L600 310" stroke="#d4ff43" stroke-width="2"/></svg><p class="foot">架空の図書館企画 / 実在の施設・開催情報ではありません</p></section>
<section class="slide question"><div class="eyebrow reveal">01 / THE MOMENT</div><p class="quiet reveal">今日も、駅と家のあいだで。</p><h2 class="reveal">帰る前に、<br>少しだけ<span>別世界。</span></h2><div class="rule reveal"></div><p class="body reveal">仕事の続きを考える夜に、<br>仕事とは違う一文を。</p><svg class="windows" viewBox="0 0 500 800" aria-hidden="true"><path d="M20 780 V100 H470 V780 M20 250 H470 M20 420 H470 M20 590 H470 M170 100 V780 M320 100 V780" stroke="#394455" fill="none" stroke-width="2"/><path d="M170 420 H320 V590 H170 Z" fill="#d4ff43" class="lit"/></svg></section>
<section class="slide journey"><div class="eyebrow reveal">02 / THE EXPERIENCE</div><h2 class="reveal">予定のない夜にも、<br><span>入口がある。</span></h2><div class="journey-line reveal"></div><div class="stops"><article class="reveal"><b>01</b><h3>灯りに<br>誘われる。</h3><p>外から見える、開いた本。<br>ふらりと入れる入口に。</p></article><article class="reveal"><b>02</b><h3>気分で<br>選べる。</h3><p>棚の前で、深呼吸。<br>探すより、出会う選書。</p></article><article class="reveal"><b>03</b><h3>一文を<br>連れて帰る。</h3><p>読み切らなくていい。<br>続きが、明日の楽しみに。</p></article></div></section>
<section class="slide shelf"><div class="eyebrow reveal">03 / CURATION</div><h2 class="reveal">今夜の気分は、<br><span>どの棚に近い？</span></h2><div class="shelf-tabs reveal" role="tablist" aria-label="気分別の選書案"><button class="selected" role="tab" aria-selected="true" data-mood="0">頭をほどく</button><button role="tab" aria-selected="false" data-mood="1">遠くへ行く</button><button role="tab" aria-selected="false" data-mood="2">明日をひらく</button></div><div id="mood-text" class="mood reveal" aria-live="polite"><h3>答えを出さない、<br>読書もある。</h3><p>詩や短いエッセイから。<br>ひとつの段落に、少し長くとどまる。</p></div><svg class="shelf-art reveal" viewBox="0 0 450 500" aria-hidden="true"><path d="M25 460 H425" stroke="#d4ff43" stroke-width="3"/><path d="M40 450 V130 H100 V450 M125 450 V70 H190 V450 M215 450 V180 H265 V450 M300 450 L240 110 L305 98 L367 440" fill="none" stroke="#d4ff43" stroke-width="3"/></svg></section>
<section class="slide plan"><div class="eyebrow reveal">04 / PILOT DESIGN</div><h2 class="reveal">小さく開いて、<br><span>夜の使い方を探す。</span></h2><div class="plan-list"><div class="reveal"><b>開く</b><p>まずは一角に、夜の選書棚。<small>開館時間・担当体制は、施設と相談して決める。</small></p></div><div class="reveal"><b>聴く</b><p>帰り道の人が、どこで立ち止まるか。<small>短い感想と滞在の様子から、入口と棚を調整する。</small></p></div><div class="reveal"><b>育てる</b><p>読者の一言を、次の選書に。<small>続けられる負担かを確かめ、次の開催を判断する。</small></p></div></div><p class="foot">試行の設計案です。利用実績・実施決定・効果の主張ではありません。</p></section>
<section class="slide close"><div class="eyebrow reveal">NIGHT LIBRARY</div><p class="quiet reveal">今日の終わりに、</p><h2 class="reveal">物語の<br><span>はじまりを。</span></h2><div class="close-rule reveal"></div><p class="body reveal">夜の図書館<br><span>仕事帰りに出会う、次の一冊。</span></p><p class="foot">架空の企画 / CONCEPT ONLY</p><span class="star reveal" aria-hidden="true">✳</span></section>
'''

CSS=r'''
/* === NIGHT LIBRARY / CUSTOM EDITORIAL SYSTEM === */
:root{--slide-bg:#111b29;--stage-bg:#070d14;--ink:#f3f0e7;--lime:#d4ff43;--ease-out-expo:cubic-bezier(.16,1,.3,1)}
*{box-sizing:border-box}body{font-family:NightSans,sans-serif;color:var(--ink)}.slide{padding:80px 100px}.eyebrow{font-size:22px;letter-spacing:5px;color:var(--lime)}h1,h2,h3,p{margin:0}h1,h2{font-weight:850;letter-spacing:-8px;line-height:1.16}h1{font-size:205px;margin-top:90px}h2{font-size:112px;margin-top:82px}h1 span,h2 span{color:var(--lime)}h1 i{font-style:normal;font-size:140px;color:var(--lime)}.cover-sub{position:absolute;left:105px;bottom:145px;font-size:40px;line-height:1.65}.book{position:absolute;right:75px;top:135px;width:720px;height:720px}.foot{position:absolute;left:100px;bottom:46px;font-size:20px;color:#a4aebb;letter-spacing:1px}.quiet{font-size:37px;margin-top:112px;color:#b3bdc7}.body{font-size:36px;line-height:1.7}.question h2{margin-top:40px}.question .body{margin-top:38px}.rule{width:140px;height:4px;background:var(--lime);margin-top:48px}.windows{position:absolute;right:100px;top:130px;width:490px;height:800px}.lit{opacity:.65}.journey h2{font-size:101px}.journey-line{position:absolute;top:485px;left:100px;width:1660px;height:2px;background:#7a8b70}.stops{display:grid;grid-template-columns:repeat(3,1fr);gap:90px;margin-top:100px}.stops b{font-size:27px;letter-spacing:3px;color:var(--lime);background:var(--slide-bg);padding-right:24px}.stops h3{font-size:58px;line-height:1.3;margin-top:36px;letter-spacing:-2px}.stops p{font-size:29px;line-height:1.7;color:#b6c0ca;margin-top:28px}.shelf h2{font-size:104px}.shelf-tabs{display:flex;gap:36px;margin-top:65px}.shelf-tabs button{font:inherit;font-size:30px;color:#a5b2c3;background:none;border:0;border-bottom:2px solid #45515e;padding:15px 0;cursor:pointer}.shelf-tabs button.selected{color:var(--lime);border-color:var(--lime)}.mood{margin-top:65px}.mood h3{font-family:NightSerif,serif;font-size:70px;font-weight:600;line-height:1.35}.mood p{font-size:29px;color:#bcc5d0;line-height:1.7;margin-top:28px}.shelf-art{position:absolute;right:120px;bottom:130px;width:490px;height:490px}.plan h2{font-size:102px}.plan-list{margin-top:70px}.plan-list>div{display:flex;gap:70px;padding:27px 0;border-top:1px solid #52606a}.plan-list b{font-size:48px;color:var(--lime);width:190px}.plan-list p{font-size:36px;line-height:1.5}.plan-list small{display:block;font-size:25px;color:#b7c2ce;margin-top:7px}.close h2{font-size:146px;margin-top:30px}.close .quiet{margin-top:100px}.close-rule{width:260px;height:4px;background:var(--lime);margin:48px 0 30px}.close .body{font-size:34px}.close .body span{font-size:27px;color:#aab8c6}.star{font-family:NightSans,sans-serif;font-size:490px;color:var(--lime);position:absolute;right:170px;top:290px;line-height:1}.deck-controls{display:flex;align-items:center;gap:12px;background:#111b29df;padding:7px 16px;border-radius:3px;color:#a9bac7;font-size:12px}.deck-controls button{color:var(--lime);background:none;border:0;font-size:22px;cursor:pointer}.deck-controls a{color:#a9bac7;margin-left:8px;text-decoration:none}
/* === ORCHESTRATED ENTRANCE / SOURCE ANIMATION RECIPE === */
.reveal{opacity:0;transform:translateY(38px);transition:opacity .9s var(--ease-out-expo),transform .9s var(--ease-out-expo)}.visible .reveal{opacity:1;transform:translateY(0)}.book{transform:translateY(40px) rotate(-5deg)}.visible .book{transform:translateY(0) rotate(0)}.visible .lit{animation:light 1.7s both}@keyframes light{from{opacity:0}to{opacity:.65}}.mood.swap{animation:reading .6s both}@keyframes reading{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
'''
CSS+='\n.eyebrow,.stops b,.deck-controls{font-family:NightLatin,NightSans,sans-serif}\n'

JS=r'''
/* === FRONTEND-SLIDES / SLIDEPRESENTATION CONTROLLER ADAPTATION === */
class SlidePresentation{
 constructor(){this.slides=document.querySelectorAll('.slide');this.currentSlide=0;this.stage=document.getElementById('deckStage');this.setupStageScale();this.setupKeyboardNav();this.setupTouchNav();this.setupWheelNav();this.slides.forEach(s=>s.querySelectorAll('.reveal').forEach((e,i)=>e.style.transitionDelay=`${.08+i*.12}s`));this.showSlide(Number(location.hash.slice(1)||1)-1);}
 setupStageScale(){const scale=()=>{const factor=Math.min(innerWidth/1920,innerHeight/1080);this.stage.style.transform=`translate(${(innerWidth-1920*factor)/2}px,${(innerHeight-1080*factor)/2}px) scale(${factor})`};scale();addEventListener('resize',scale)}
 setupKeyboardNav(){addEventListener('keydown',e=>{if(e.target.closest('button,a'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide-1)}if(e.key==='Home')this.showSlide(0);if(e.key==='End')this.showSlide(this.slides.length-1)})}
 setupTouchNav(){let start=0;addEventListener('touchstart',e=>start=e.changedTouches[0].clientX,{passive:true});addEventListener('touchend',e=>{const delta=e.changedTouches[0].clientX-start;if(Math.abs(delta)>60)this.showSlide(this.currentSlide+(delta<0?1:-1))},{passive:true})}
 setupWheelNav(){let last=0;addEventListener('wheel',e=>{if(Date.now()-last>700&&Math.abs(e.deltaY)>25){this.showSlide(this.currentSlide+(e.deltaY>0?1:-1));last=Date.now()}},{passive:true})}
 showSlide(index){this.currentSlide=Math.max(0,Math.min(index,this.slides.length-1));this.slides.forEach((s,i)=>{s.classList.toggle('active',i===this.currentSlide);s.classList.toggle('visible',i===this.currentSlide);s.setAttribute('aria-hidden',i!==this.currentSlide)});document.getElementById('count').textContent=`${String(this.currentSlide+1).padStart(2,'0')} / 06`;history.replaceState(null,'',`#${this.currentSlide+1}`)}
}
window.deck=new SlidePresentation();
/* === SAME-ORIGIN YEBISU VIEWER BRIDGE === */
const nativeShow=deck.showSlide.bind(deck);deck.showSlide=function(index){nativeShow(index);if(parent!==window)parent.postMessage({type:'yebisu-page',index:this.currentSlide,total:this.slides.length},location.origin)};
addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))deck.showSlide(e.data.index)});deck.showSlide(deck.currentSlide);
document.getElementById('prev').onclick=()=>deck.showSlide(deck.currentSlide-1);document.getElementById('next').onclick=()=>deck.showSlide(deck.currentSlide+1);
const moods=[['答えを出さない、<br>読書もある。','詩や短いエッセイから。<br>ひとつの段落に、少し長くとどまる。'],['帰り道から、<br>知らない街へ。','旅の記録や物語から。<br>いつもの景色に、新しい窓をひらく。'],['知らなかったことが、<br>明日の種になる。','暮らしや自然、ものづくりの本から。<br>小さな「やってみたい」を見つける。']];document.querySelectorAll('[data-mood]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-mood]').forEach(x=>{x.classList.toggle('selected',x===b);x.setAttribute('aria-selected',x===b)});const m=moods[Number(b.dataset.mood)],t=document.getElementById('mood-text');t.innerHTML=`<h3>${m[0]}</h3><p>${m[1]}</p>`;t.classList.remove('swap');void t.offsetWidth;t.classList.add('swap')});
'''

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'source').mkdir(exist_ok=True)
 fonts=[]
 (OUT/'fonts').mkdir(exist_ok=True)
 for name,path in [('NightSans',ROOT/'.build/fonts/NotoSansJP[wght].ttf'),('NightSerif',ROOT/'.build/fonts/NotoSerifJP[wght].ttf'),('NightLatin',ROOT/'downloads/fonts/spacegrotesk/SpaceGrotesk[wght].ttf')]:
  shutil.copy2(path,OUT/'fonts'/path.name)
  fonts.append(f"@font-face{{font-family:{name};src:url(data:font/ttf;base64,{base64.b64encode(path.read_bytes()).decode()}) format('truetype');font-weight:100 900;font-display:block}}")
 source_refs=[]
 for rel in ['SKILL.md','html-template.md','viewport-base.css','animation-patterns.md','LICENSE']:
  shutil.copy2(SRC/rel,OUT/'source'/rel)
  source_refs.append({'path':rel,'sha256':hashlib.sha256((SRC/rel).read_bytes()).hexdigest(),'url':f'https://github.com/zarazhangrui/frontend-slides/blob/{COMMIT}/{rel}'})
 shutil.copy2(SRC/'LICENSE',OUT/'LICENSE')
 for name in ['notosansjp','notoserifjp']:
  shutil.copy2(ROOT/f'examples/cases/port-town/licenses/fonts/{name}-OFL.txt',OUT/f'{name}-OFL.txt')
 shutil.copy2(ROOT/'downloads/fonts/spacegrotesk/OFL.txt',OUT/'fonts/spacegrotesk-OFL.txt')
 html='<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>夜の図書館 — 仕事帰りに出会う、次の一冊</title><style>'+''.join(fonts)+(SRC/'viewport-base.css').read_text(encoding='utf-8')+CSS+'</style></head><body><div class="deck-viewport"><main class="deck-stage" id="deckStage">'+SLIDES+'</main></div><nav class="deck-controls" aria-label="スライド移動"><button id="prev" aria-label="前へ">←</button><span id="count" aria-live="polite"></span><button id="next" aria-label="次へ">→</button><a href="README.md">制作メモ</a></nav><script>'+JS+'</script></body></html>'
 (OUT/'index.html').write_text(html,encoding='utf-8')
 (OUT/'PROMPT.txt').write_text(PROMPT+'\n',encoding='utf-8')
 prov={'repository':'zarazhangrui/frontend-slides','upstream_commit':COMMIT,'license':'MIT','copyright':'Copyright (c) 2025 Zara Zhang','source_refs':source_refs,'method':'Original viewport-base.css included verbatim; html-template.md stage and SlidePresentation architecture directly adapted; animation-patterns.md staggered editorial reveal. Bespoke Japanese composition authored with CSS/SVG, no common renderer.','starrykit':'Withdrawn because Hosted MCP is unavailable; no claim of StarryKit generation.','fonts':'Full Noto Sans JP and Noto Serif JP embedded as TTF; SIL OFL 1.1 licenses included.','status':'generated','page_count':6}
 (OUT/'PROVENANCE.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'README.md').write_text('''# 夜の図書館

仕事帰りに出会う、次の一冊。架空の図書館企画を6ページの広告・提案スライドにしました。実在施設、開館時間、利用実績は含みません。

`index.html` を開き、矢印・スペース・ホイール・スワイプで移動。4ページの気分別の棚はクリックで切り替えられます。墨紺と蛍光ライム、和文ゴシックと明朝、SVGの本・窓・棚で構成。フル日本語フォントを内包し、CDNや外部AI APIは使いません。

制作は zarazhangrui/frontend-slides の MIT 原典（commit 9906a34d640d2111f724544cbc50f7f130569ae1）。原典固定stageのCSS全文、HTML構造、SlidePresentation、段階表示を直接使用・拡張しています。`source/` に使用ファイル、`PROVENANCE.json` にハッシュ、`PROMPT.txt` にAI依頼文を保存。元スキルを共通rendererで置き換えていません。

再生成: repoルートで `python tools/build_sol_motion_showcase.py`。軽い確認の範囲は `QA.json`。正式採用・全ページ視覚QA・配布ZIP検証は未実施です。
''',encoding='utf-8')
 skill=ROOT/'skill-forks/sol-motion-ja';skill.mkdir(parents=True,exist_ok=True)
 shutil.copy2(SRC/'LICENSE',skill/'LICENSE')
 (skill/'SKILL.md').write_text('''---
name: sol-motion-ja
description: frontend-slides原典の固定stageで、日本語の広告・企画用モーションスライドを作る。
---

# 日本語モーションスライド

1. 原典 `examples/repositories/sol-motion-showcase/source/SKILL.md`、`html-template.md`、`viewport-base.css` を読む。CSS全文と1920×1080 stage、SlidePresentationの構造を使う。
2. 読者に残す一言を決め、5〜6ページの役割と完成コピーを先に書く。架空の計画と実績を混同しない。
3. 墨紺・蛍光ライムなど少数の色、大きい和文見出し、広い余白、内容を示すSVG図形を使う。全ページを同じカード配置にしない。
4. 一枚の入場を段階表示で演出。矢印・スワイプ・ホイール、reduce motionを保ち、必要なページだけタブ等の操作を加える。
5. 日本語フルフォントとOFL、原典MIT帰属を添え、HTMLと依頼文、使用commitを渡す。生成と確認済みを分けて記録する。

実例: `examples/repositories/sol-motion-showcase/index.html`。再生成: `python tools/build_sol_motion_showcase.py`。本技能は frontend-slides のローカル制作用派生で、StarryKit Hosted MCP の代替を名乗らない。
''',encoding='utf-8')
 case={'id':'sol-motion-showcase','title':'夜の図書館 — 仕事帰りに出会う、次の一冊','repository':prov['repository'],'skill_repository':prov['repository'],'upstream_commit':COMMIT,'fork_id':'sol-motion-ja','page_count':6,'format':'html','preview_kind':'html','style':'墨紺 × 蛍光ライム / Japanese editorial motion','use_case':'文化施設の広告・企画提案','cover':'examples/repositories/sol-motion-showcase/render/slide-01.png','interior':'examples/repositories/sol-motion-showcase/render/slide-04.png','preview':'examples/repositories/sol-motion-showcase/index.html','input':'examples/repositories/sol-motion-showcase/PROMPT.txt','prompt':'examples/repositories/sol-motion-showcase/PROMPT.txt','prompt_text':PROMPT,'provenance':'examples/repositories/sol-motion-showcase/PROVENANCE.json','qa':'examples/repositories/sol-motion-showcase/QA.json','guide':'examples/repositories/sol-motion-showcase/README.md','method':prov['method'],'sample_notice':'架空の図書館企画。実在の施設、実施決定、利用実績ではありません。','editability':'html_css_svg_js','status':'generated','execution_status':'generated','navigation':'keyboard-wheel-swipe','pages':['examples/repositories/sol-motion-showcase/render/slide-01.png','examples/repositories/sol-motion-showcase/render/slide-04.png']}
 (ROOT/'data/sol-motion-repository-examples.json').write_text(json.dumps([case],ensure_ascii=False,indent=2),encoding='utf-8')
 guide={'repository':prov['repository'],'production_status':'generated','execution_status':'generated','execution_type':'original_fixed_stage_recipe_direct_authoring','case_ids':['sol-motion-showcase'],'summary_ja':'原典frontend-slides固定stageで日本語6ページの架空文化施設企画を実制作。墨紺×蛍光ライム、大胆な和文タイポ、段階表示と選書タブ。','requirements':['Python 3','モダンブラウザ','取得済み原典とフル日本語フォント'],'steps':['完成コピーを6つの役割に分ける','原典viewport-base全文とcontrollerを使用','内容固有のSVGと段階表示を制作','buildと代表2画面だけ軽く確認'],'commands':['python tools/build_sol_motion_showcase.py'],'source_refs':source_refs,'upstream_commit':COMMIT,'license':'MIT','guide':'examples/repositories/sol-motion-showcase/README.md','skill':'skill-forks/sol-motion-ja/SKILL.md'}
 (ROOT/'data/sol-motion-repository-guides.json').write_text(json.dumps([guide],ensure_ascii=False,indent=2),encoding='utf-8')
 finish_package(case,guide,skill)
 print('Generated 6-page deck and offline packages:',OUT/'index.html')

def finish_package(case,guide,skill):
 titles=['夜の図書館。','帰る前に、少しだけ別世界。','予定のない夜にも、入口がある。','今夜の気分は、どの棚に近い？','小さく開いて、夜の使い方を探す。','今日の終わりに、物語のはじまりを。']
 notes=['架空の図書館企画です。仕事帰りの寄り道として、本との出会いを提案します。','駅と家のあいだに、仕事と違う一文に触れる時間をつくります。','灯りに誘われ、気分で選び、一文を持ち帰る。読み切ることを条件にしない体験案です。','気分別の棚は選書例です。タブで詩・旅・暮らしの入口を切り替えられます。','施設と相談して小さく試し、感想と運営負担を確かめます。実施決定や効果の主張ではありません。','一日の終わりを、次の物語の入口へ。開催情報や実在施設の案内ではありません。']
 (OUT/'input').mkdir(exist_ok=True)
 data={'title':case['title'],'sample_notice':case['sample_notice'],'titles':titles,'notes':notes,'page_count':6,'format':'1920x1080','brief':PROMPT}
 (OUT/'input/data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'input/BRIEF.md').write_text('# 制作依頼\n\n'+PROMPT+'\n\n6枚の役割: 企画の顔 / 来館の動機 / 体験の流れ / 選書例 / 試行設計 / 余韻。\n',encoding='utf-8')
 case.update(artifact_download='downloads/sol-motion-example-ja.zip',source_download='downloads/sol-motion-example-ja.zip',fork_download='downloads/sol-motion-ja.zip',input='examples/repositories/sol-motion-showcase/input/BRIEF.md',input_data='examples/repositories/sol-motion-showcase/input/data.json',titles=titles,notes=notes,preview_canvas={'width':1920,'height':1080},preview_image_count=2,preview_image_notice='HTML全6ページのうち、静止画は表紙と選書ページの代表2枚です。',navigation='native-runtime-bridge')
 case.pop('pages',None)
 case['representative_previews']=['examples/repositories/sol-motion-showcase/render/slide-01.png','examples/repositories/sol-motion-showcase/render/slide-04.png']
 (ROOT/'data/sol-motion-repository-examples.json').write_text(json.dumps([case],ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'README.md').write_text((OUT/'README.md').read_text(encoding='utf-8')+'\n英数字はSpace Groteskを併用（フルTTF・OFL同梱）。HTMLは6ページ、静止プレビューは代表2枚です。サイトとの同一origin postMessageページ送りを接続済み。ZIPを展開してindex.htmlを開けばオフライン再生できます。\n',encoding='utf-8')
 source={'repository':'zarazhangrui/frontend-slides','commit':COMMIT,'license':'MIT','scope':'Japanese motion authoring entrypoint, original reference CSS/controller architecture, offline example','upstream_preserved':True,'case_studies':['sol-motion-showcase']}
 (OUT/'SOURCE.json').write_text(json.dumps(source,ensure_ascii=False,indent=2),encoding='utf-8')
 (skill/'upstream').mkdir(exist_ok=True)
 for f in (OUT/'source').iterdir():shutil.copy2(f,skill/'upstream'/f.name)
 (skill/'SKILL.md').write_text((skill/'SKILL.md').read_text(encoding='utf-8').replace('`examples/repositories/sol-motion-showcase/source/SKILL.md`、`html-template.md`、`viewport-base.css`','同梱 `upstream/SKILL.md`、`upstream/html-template.md`、`upstream/viewport-base.css`'),encoding='utf-8')
 source['files']=[{'path':p.relative_to(skill).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(skill.rglob('*')) if p.is_file() and p.name!='SOURCE.json']
 (skill/'SOURCE.json').write_text(json.dumps(source,ensure_ascii=False,indent=2),encoding='utf-8')
 prov=json.loads((OUT/'PROVENANCE.json').read_text(encoding='utf-8'));prov['fonts']='Full Noto Sans JP, Noto Serif JP and Space Grotesk embedded; used TTF/OFL files included.';prov['viewer_bridge']='same-origin yebisu-slide input / yebisu-page output';(OUT/'PROVENANCE.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2),encoding='utf-8')
 for folder,name in [(OUT,'sol-motion-example-ja'),(skill,'sol-motion-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.parts)&{'cache','.build','__pycache__'}:z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

if __name__=='__main__':main()
