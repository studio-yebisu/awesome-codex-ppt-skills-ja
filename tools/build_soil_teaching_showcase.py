"""SOIL Mode C native template adaptation. No common slide renderer."""
from pathlib import Path
import argparse, hashlib, json, shutil, zipfile, math

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams/chunyifish__soil-teaching-slides'
SK=UP/'soil-teaching-slides'
OUT=ROOT/'examples/repositories/soil-teaching-showcase'
FORK=ROOT/'skill-forks/soil-teaching-ja'
REPO='chunyifish/soil-teaching-slides'
PIN='ebeb43ce0e4360ba2ffc91dcfb4be5ba203bb09f'
TITLE='割合は、全体との比べ方。'
TITLES=[TITLE,'同じ6個でも、割合は変わる','40個のうち12個は、30%','60個の30%は、18個','20%引きは、80%を払う','8個は、32個の何%？']
NOTES=['まず全体を決めてから、その一部を比べます。赤い3区画は10区画のうち3区画。','赤の個数は両方6個。全体が20個なら30%、40個なら15%。全体が違うと割合が変わります。','全体40個を10等分すると一区画4個。赤い12個は三区画なので3/10、0.3、30%です。','60個の10%は6個。30%はその三つ分なので18個です。','もとの価格を100%とすると、20%引きで残る支払いは80%。1200円の80%は960円です。','8÷32=0.25、25%。割合=比べる量÷もとにする量。本文の数値は学習用設定です。']
PROMPT='SOIL Teaching Slidesの原典Mode C HTML template / slides.js / styles.cssとSOIL cognitive page rolesを実際に使い、日本語6枚「割合は、全体との比べ方。」を制作してください。小学校高学年向けに、全体と部分、同じ6個でも全体20個/40個で30%/15%になる比較、12/40から30%、60個の30%=18個、1200円の20%引き=960円、8/32=25%を図で理解する構成。温かい紙色・深緑・赤橙、大きい日本語。意味のある区画・個数・帯だけをSVG/HTMLで描き、原典fragment/controllerで一段階ずつ示す。反復する角丸カードは使わない。数値は学習用設定、実績ではありません。オフラインで開ける日本語navigation、実TTF/OFL、李俊儀の帰属、MIT softwareとCC BY-NC-SA 4.0 contentの条件を保持。計画とstyleは指定済みなので確認待ちにせずINPUTに記録して完成まで進める。'

def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def jwrite(p,s):write(p,json.dumps(s,ensure_ascii=False,indent=2)+'\n')
def svg_open(w,h,label):return f'<svg viewBox="0 0 {w} {h}" role="img" preserveAspectRatio="xMinYMin meet" aria-label="{label}">'
def tiles(count,cols,size=54,gap=9,red=0,red_columns=0):
 rows=(count+cols-1)//cols;w=cols*(size+gap)-gap;h=rows*(size+gap)-gap
 s=svg_open(w,h,f'全体{count}個、赤{red}個')
 for n in range(count):
  x=(n%cols)*(size+gap);y=(n//cols)*(size+gap)
  painted=(n%cols<red_columns) if red_columns else n<red
  s+=f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="'+('#CD5132' if painted else '#DCE3D9')+'"/>'
 return s+'</svg>'
def segments(n,red,width=1040,height=115):
 s=svg_open(width,height,f'{n}等分のうち{red}区画')
 for k in range(n):s+=f'<rect x="{k*width/n+2}" y="2" width="{width/n-4}" height="{height-4}" fill="'+('#CD5132' if k<red else '#DCE3D9')+'"/>'
 return s+'</svg>'

CSS='''
:root{--background:#F3EFDF;--surface:#F3EFDF;--text:#164735;--muted:#546351;--line:#97AA91;--accent:#CD5132;--safe-x:95px;--safe-y:64px;--font-sans:"Soil Japanese",sans-serif}
body{background:#24392C}.slide{padding:64px 95px}.slide:after{content:attr(data-page) " / 06";position:absolute;right:95px;top:65px;font:700 25px "Soil Numbers",sans-serif;color:var(--muted)}
.eyebrow{font-size:25px;letter-spacing:.13em;color:var(--muted);margin-bottom:25px}h1,h2{line-height:1.23;font-weight:700;font-size:68px;letter-spacing:-2px;margin-bottom:20px;max-width:1320px}h1{font-size:103px;letter-spacing:-4px}p{font-size:31px;line-height:1.65}.task{font-size:30px;color:var(--muted)}.red{color:var(--accent)}.number{font-family:"Soil Numbers",var(--font-sans)}.huge{font-size:110px;font-weight:600;line-height:1.05;letter-spacing:-4px}.percent{font-size:152px;font-weight:650;line-height:1;color:var(--accent)}.percent small{font-size:64px;letter-spacing:0}.math{font-size:52px;line-height:1.25;font-weight:700}.quiet{color:var(--muted)}.rule{height:2px;background:var(--line)}
.cover{justify-content:flex-start}.cover h1{position:absolute;top:248px;left:95px;width:950px}.cover .deck-lead{position:absolute;top:531px;left:103px;font-size:34px}.cover .cover-diagram{position:absolute;right:100px;top:300px;width:350px;height:350px}.cover .cover-caption{position:absolute;right:110px;top:682px;width:340px;font-size:28px}.cover .intro-rule{position:absolute;left:95px;right:95px;top:751px}.cover .lesson-line{position:absolute;top:779px;left:95px;font-size:23px;letter-spacing:.04em}
.cover-diagram svg{width:350px;height:350px}.cover-diagram .circle{fill:#DCE3D9}.cover-diagram .slice{fill:var(--accent);transform-origin:180px 180px;transition:transform 700ms cubic-bezier(.2,.7,.2,1)}.cover-diagram:hover .slice{transform:translate(-7px,-7px)}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:85px;position:absolute;left:95px;right:95px;top:330px}.compare figure{margin:0}.compare .group{height:240px;display:flex;align-items:flex-start}.compare svg{width:555px;height:240px;object-fit:contain}.compare .group:first-child{justify-content:flex-start}.compare h3{font-size:36px;margin:0 0 28px}.compare .result{font-size:46px;margin:6px 0 0;line-height:1.2}.compare .right{border-left:2px solid var(--line);padding-left:65px}.compare .right svg{width:555px}.takeaway{position:absolute;left:95px;right:95px;bottom:74px;border-top:2px solid var(--line);padding-top:20px;margin:0;font-size:35px;font-weight:700}
.fraction-work{position:absolute;top:310px;left:95px;width:860px}.fraction-work .original-grid{width:850px}.fraction-work svg{width:850px;height:333px}.bracket{border-bottom:3px solid var(--accent);border-left:3px solid var(--accent);border-right:3px solid var(--accent);height:20px;width:246px;margin-top:15px}.bracket-label{margin:15px 0 0;font-size:27px;color:var(--accent)}.fraction-equal{position:absolute;left:1050px;top:326px;width:460px}.fraction-equal .equation{font-size:54px;color:var(--muted);margin:0 0 25px}.fraction-equal .big-answer{margin:0 0 18px}.fraction-equal .answer-explain{font-size:29px;margin:25px 0}.fraction-cue{font-size:25px!important;margin-top:25px}
.amount-band{position:absolute;left:95px;top:360px;width:1050px}.amount-band svg{width:1050px;height:145px}.amount-band .whole{position:absolute;top:-69px;right:0;font-size:40px;font-weight:700}.amount-band .third{width:315px;border-bottom:3px solid var(--accent);border-right:3px solid var(--accent);border-left:3px solid var(--accent);height:26px;margin-top:7px}.amount-band .third-label{font-size:34px;margin-top:13px}.amount-calc{position:absolute;left:95px;top:632px;display:flex;gap:80px;align-items:baseline}.amount-calc p{font-size:38px;margin:0}.amount-calc strong{font-size:68px}.amount-side{position:absolute;right:80px;top:377px;width:265px;font-size:89px;font-weight:700;line-height:1.2}.amount-side small{font-size:41px;font-weight:400}.js .fragment:not(.is-revealed){transform:translateY(13px)}.js .fragment.is-revealed{transform:translateY(0)}
.price-ribbon{position:absolute;left:95px;right:95px;top:326px;height:194px;display:flex;align-items:stretch}.price-ribbon .pay{width:80%;background:var(--text);color:var(--background);padding:33px 42px}.price-ribbon .discount{width:20%;background:var(--accent);color:var(--background);padding:34px 25px}.price-ribbon p{margin:0;font-size:27px}.price-ribbon strong{font-size:66px;line-height:1.3}.price-ribbon .discount strong{font-size:61px}.discount-cross{position:absolute;left:80%;top:0;bottom:0;right:0;border:3px dashed var(--background);transform:translateX(24px) rotate(2deg);transition:transform 350ms}.price-label{position:absolute;left:95px;right:95px;top:268px;text-align:right;font-size:29px}.price-calc{position:absolute;left:95px;top:614px;right:95px;display:flex;align-items:baseline;gap:47px}.price-calc .expression{font-size:50px;flex:1}.price-calc .answer{font-size:125px;font-weight:650;line-height:1}.price-calc small{font-size:48px}.practice-art{position:absolute;left:95px;top:328px;width:645px}.practice-art svg{width:625px;height:318px}.practice-art p{font-size:28px;margin-top:20px}.practice-answer{position:absolute;left:855px;top:350px;width:650px}.practice-answer .line{font-size:53px;line-height:1.3;margin-bottom:22px}.practice-answer .percent{font-size:153px;margin:0}.concept-note{font-size:31px;margin:20px 0}.legal-strip{position:absolute;left:95px;right:95px;bottom:23px;font-size:16px;color:var(--muted)}
.controls{border-radius:0;bottom:10px;background:rgba(22,71,53,.9)}.controls button{border-radius:0;font-size:16px;width:69px}.status{min-width:156px}.step-status{color:#FFD4B5}.progress span{background:var(--accent)}
@media print{.slide,.slide.is-active{width:1600px;height:900px}.slide:last-child{break-after:auto;page-break-after:auto}.controls,.progress{display:none!important}@page{size:1600px 900px;margin:0}}
'''

def markup():
 cover_svg=svg_open(360,360,'10等分のうち3区画、全体の30%を赤く示した円')+'<circle class="circle" cx="180" cy="180" r="166"/><path class="slice" d="M180 180 L180 14 A166 166 0 0 1 337.9 231.3 Z"/>' + ''.join(f'<line x1="180" y1="180" x2="{180+166*math.sin(k*math.pi/5):.3f}" y2="{180-166*math.cos(k*math.pi/5):.3f}" stroke="#F3EFDF" stroke-width="3"/>' for k in range(10)) + '<circle cx="180" cy="180" r="9" fill="#F3EFDF"/></svg>'
 bodies=[
 f'''<h1 id="slide-01-title">割合は、<br>全体との比べ方。</h1><p class="deck-lead">「いくつある？」の、その先へ。</p><div class="cover-diagram">{cover_svg}</div><p class="cover-caption">全体を <b class="number">100%</b> とすると<br>赤い部分は <b class="red number">30%</b></p><div class="intro-rule rule"></div><p class="lesson-line">割合の見方を、6枚の図で。　小学校高学年向け</p>''',
 f'''<h2 id="slide-02-title">同じ<span class="red number">6個</span>でも、割合は変わる</h2><p class="task">赤の個数と、全体の個数。どちらが変わった？</p><div class="compare"><figure><h3>全体 <span class="number">20</span> 個</h3><div class="group">{tiles(20,10,48,9,6)}</div><p class="fragment result number">6 ÷ 20 = 0.3 = <b class="red">30%</b></p></figure><figure class="right"><h3>全体 <span class="number">40</span> 個</h3><div class="group">{tiles(40,10,48,9,6)}</div><p class="fragment result number">6 ÷ 40 = 0.15 = <b class="red">15%</b></p></figure></div><p class="takeaway fragment">同じ部分でも、全体が大きいほど割合は小さくなる。</p>''',
 f'''<h2 id="slide-03-title"><span class="number">40</span>個のうち<span class="red number">12</span>個は、<span class="red number">30%</span></h2><p class="task">全体を10等分すると、一つ分は4個。</p><div class="fraction-work"><div class="original-grid">{tiles(40,10,72,12,12,3)}</div><div class="fragment"><div class="bracket"></div><p class="bracket-label">赤は、10等分したうちの3つ分</p></div><p class="fraction-cue">同じ大きさの区画で比べると、割合が見える。</p></div><div class="fraction-equal"><p class="equation number fragment">12 ÷ 40 = 0.3</p><p class="big-answer percent number fragment">30<small>%</small></p><p class="answer-explain fragment">「全体の100分の30」<br>という表し方。</p></div>''',
 f'''<h2 id="slide-04-title"><span class="number">60</span>個の<span class="red number">30%</span>は、<span class="red number">18</span>個</h2><p class="task">まず10%。それを3つ分にすると？</p><div class="amount-band"><p class="whole">全体 <span class="number">60</span> 個</p>{segments(10,3)}<div class="fragment"><div class="third"></div><p class="third-label"><span class="red number">30%</span> は、10%の3つ分</p></div></div><div class="amount-calc"><p class="fragment"><span class="number">60 ÷ 10 = 6</span><br><span class="quiet">一つ分は6個</span></p><p class="fragment"><span class="number">6 × 3 = <strong class="red">18</strong></span><br><span class="quiet">赤はその3つ分</span></p></div><div class="amount-side fragment"><span class="number red">18</span><small>個</small></div>''',
 '''<h2 id="slide-05-title"><span class="number red">20%</span>引きは、<span class="number">80%</span>を払う</h2><p class="task">もとの価格は1,200円。払う部分はどちら？</p><p class="price-label">もとの価格 <b class="number">1,200</b> 円 = 全体 <b class="number">100%</b></p><div class="price-ribbon"><div class="pay"><p>支払う部分</p><strong class="number">80%</strong></div><div class="discount"><p>値引き</p><strong class="number">20%</strong></div><div class="discount-cross fragment" aria-hidden="true"></div></div><div class="price-calc"><p class="expression fragment number">1,200 × 0.8 =</p><p class="answer fragment number red">960<small>円</small></p></div><p class="takeaway fragment">払う金額は、残った割合で求められる。</p>''',
 f'''<h2 id="slide-06-title"><span class="red number">8</span>個は、<span class="number">32</span>個の何%？</h2><p class="task">全体と部分を見つけて、自分で式にしてみよう。</p><div class="practice-art">{tiles(32,8,65,13,8)}<p>全体 <b class="number">32</b> 個。赤い部分は <b class="red number">8</b> 個。</p></div><div class="practice-answer"><p class="line fragment number">8 ÷ 32 = 0.25</p><p class="percent fragment number">25<small>%</small></p><p class="concept-note fragment">全体の4分の1は、25%。</p></div><p class="takeaway fragment">割合 = 比べる量 ÷ もとにする量</p><p class="legal-strip">教材の数値は学習用の設定です。</p>'''
 ]
 roles=['考える入口','比較・誤解をほどく','仕組みを見つける','順序・量を求める','応用・支払いを考える','練習・まとめ']
 ids=['opening','compare-wholes','twelve-of-forty','thirty-of-sixty','discount','practice']
 return '\n'.join(f'<section class="slide '+('cover' if n==0 else 'lesson')+(' is-active' if n==0 else '')+f'" data-page="{n+1:02}" data-slide-id="{ids[n]}" aria-labelledby="slide-{n+1:02}-title"'+('' if n==0 else ' hidden')+f'><p class="eyebrow">割合の見方　{roles[n]}</p>{b}</section>' for n,b in enumerate(bodies))

def main():
 OUT.mkdir(parents=True,exist_ok=True);FORK.mkdir(parents=True,exist_ok=True)
 # Preserve the original unmodified Mode C runtime and method documents.
 ud=OUT/'upstream'
 (ud/'assets').mkdir(parents=True,exist_ok=True)
 shutil.copytree(SK/'assets/html-deck-template',ud/'assets/html-deck-template',dirs_exist_ok=True)
 for f in ['SKILL.md','references/html-slide-deck.md','references/html-style-selection.md','scripts/validate_html_deck.mjs']:
  (ud/f).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SK/f,ud/f)
 for name in ['LICENSE','LICENSE-CONTENT.md','NOTICE.md']:shutil.copy2(UP/name,OUT/name)
 # Prefer BIZ if the shared OSS kit has arrived; fallback stays portable.
 biz=ROOT/'downloads/fonts/bizudpgothic'
 jp='bizudpgothic' if (biz/'BIZUDPGothic-Regular.ttf').exists() else 'zenkakugothicnew'
 fam='BIZ UDPGothic' if jp=='bizudpgothic' else 'Zen Kaku Gothic New'
 fontfiles=['BIZUDPGothic-Regular.ttf','BIZUDPGothic-Bold.ttf'] if jp=='bizudpgothic' else ['ZenKakuGothicNew-Regular.ttf','ZenKakuGothicNew-Bold.ttf']
 (OUT/'fonts').mkdir(exist_ok=True);fontcss=''
 for filename,weight in zip(fontfiles,[400,700]):
  shutil.copy2(ROOT/'downloads/fonts'/jp/filename,OUT/'fonts'/filename)
  fontcss+=f'@font-face{{font-family:"Soil Japanese";src:url("fonts/{filename}");font-weight:{weight};font-display:block}}\n'
 shutil.copy2(ROOT/'downloads/fonts'/jp/'OFL.txt',OUT/'fonts'/f'{jp}-OFL.txt')
 latin='Manrope[wght].ttf';shutil.copy2(ROOT/'downloads/fonts/manrope'/latin,OUT/'fonts'/latin);shutil.copy2(ROOT/'downloads/fonts/manrope/OFL.txt',OUT/'fonts/manrope-OFL.txt')
 fontcss+=f'@font-face{{font-family:"Soil Numbers";src:url("fonts/{latin}");font-weight:200 800;font-display:block}}\n'
 stylesheet=CSS.replace('top:751px','top:790px').replace('top:779px','top:820px')
 write(OUT/'styles.css',(SK/'assets/html-deck-template/styles.css').read_text(encoding='utf-8')+'\n/* Japanese ratio lesson adaptation. Original MIT stylesheet preserved above. */\n'+fontcss+stylesheet)
 template=(SK/'assets/html-deck-template/index.html').read_text(encoding='utf-8')
 a=template.index('      <section');b=template.index('\n    </div>',a)
 html=template[:a]+markup()+template[b:]
 html=html.replace('zh-Hant-TW','ja').replace('SOIL HTML 簡報範本',TITLE).replace('簡報控制','スライド操作').replace('簡報','割合の教材').replace('上一步','前の段階').replace('下一步','次の段階').replace('切換全螢幕','全画面を切り替える').replace('>←</button>','>戻る</button>').replace('>→</button>','>進む</button>').replace('>⛶</button>','>全画面</button>').replace('data-total>3','data-total>6')
 html=html.replace('<main class="deck"','<main class="deck" tabindex="-1"')
 write(OUT/'index.html',html)
 js=(SK/'assets/html-deck-template/slides.js').read_text(encoding='utf-8')
 # Extend the actual controller instead of replacing it with a common player.
 js=js.replace("step.textContent = fragments.length > 0 ? `· ${revealed} / ${fragments.length}` : '';","step.textContent = fragments.length > 0 ? `段階 ${revealed} / ${fragments.length}` : '';")
 js=js.replace("if (updateHash) history.replaceState", "if (parent !== window) parent.postMessage({type:'yebisu-page',index,total:slides.length},location.origin);\n    if (updateHash) history.replaceState")
 insertion='''
  // Japanese example extension: site pagination and local preview use the original render.
  const show = (n, complete = false) => {
    const target = clamp(n);
    revealedCounts[target] = complete ? fragmentsFor(target).length : 0;
    render(target);
  };
  window.soilDeck = {show, next:advance, previous:retreat, get index(){return index;}};
  addEventListener('message', event => {
    if(event.source === parent && event.origin === location.origin && event.data?.type === 'yebisu-slide' && Number.isInteger(event.data.index)) show(event.data.index,true);
  });
  if(new URLSearchParams(location.search).has('preview')) document.body.classList.add('preview-mode');
'''
 js=js.replace("  addEventListener('hashchange'",insertion+"\n  addEventListener('hashchange'")
 write(OUT/'slides.js',js)
 write(OUT/'styles.css',(OUT/'styles.css').read_text(encoding='utf-8')+'\n.preview-mode .controls,.preview-mode .progress{display:none}\n')
 plan={'style':{'family':'Structured Teaching / user-directed paper and forest palette','reason':'Whole/part and ordered quantity operations are the learning relationship.','palette':['#F3EFDF','#164735','#CD5132'],'typography':[fam,'Manrope'],'motion':'instructional fragments 190ms, original slide fade 220ms','image_policy':'editable HTML/SVG, no raster assets'},'authorization':'User explicitly approved internal planning and selected Mode C/style; skip the upstream stop-and-wait confirmation for this task.','slides':[]}
 tasks=['全体と部分に注目する','同じ赤の個数と異なる全体を比較する','40個を10等分して12個の占める区画を見る','10%の量から30%の量を求める','値引きと支払いの部分を分ける','8÷32を計算し、割合の定義へ戻る']
 roles=['question opener','misconception clarifier / comparison','process','process / quantity','practice / application','practice / summary']
 labels=[['全体100%','赤30%'],['全体20個','全体40個','赤6個','30%','15%'],['全体40個','赤12個','10等分','30%'],['全体60個','10%は6個','30%は18個'],['もとの価格1,200円','値引き20%','支払い80%','960円'],['全体32個','赤8個','25%']]
 conclusions=['割合は、全体を100%としたときの部分の大きさ。','部分が同じでも、もとの量で割合は変わる。','12÷40=0.3を100分の表し方にすると30%。','もとの量と割合から、部分の量を求められる。','値引き後は残る割合80%で求める。','割合=比べる量÷もとにする量。']
 points=['全体を決めて部分の割合を読む。','同じ部分と異なる全体を比較する。','個数の比を小数と百分率へ結びつける。','10%の量を基準に30%の量を求める。','値引き率と支払いの割合を分ける。','全体と部分から割合を自分で求める。']
 for n in range(6):plan['slides'].append({'page':n+1,'total':6,'course':'割合の見方','title':TITLES[n],'teaching_point':points[n],'learner_task':tasks[n],'page_role':roles[n],'visual_structure':['whole/part circle','two equal-scale tile arrays','40-tile grid and fraction conversion','10-part band and calculation','80/20 band','32-tile practice grid'][n],'required_labels':labels[n],'core_takeaway':conclusions[n]})
 jwrite(OUT/'input/PLAN.json',plan);write(OUT/'input/BRIEF.md','# 制作依頼\n\n'+PROMPT+'\n\n確認済みの内部設計: Mode C、6枚、紙色・深緑・赤橙、学習上の順序で段階表示。原典の計画確認は、この制作指示で承認済みのため再確認しません。\n')
 jwrite(OUT/'input/data.json',{'title':TITLE,'titles':TITLES,'notes':NOTES,'page_count':6,'sample_notice':'学習用の設定値。販売価格や調査実績ではありません。'})
 write(OUT/'PROMPT.md',PROMPT+'\n')
 refs=[{'path':f,'sha256':hashlib.sha256((UP/f).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{PIN}/{f}'} for f in ['soil-teaching-slides/SKILL.md','soil-teaching-slides/assets/html-deck-template/index.html','soil-teaching-slides/assets/html-deck-template/slides.js','soil-teaching-slides/assets/html-deck-template/styles.css','soil-teaching-slides/references/html-slide-deck.md','soil-teaching-slides/references/html-style-selection.md','LICENSE','LICENSE-CONTENT.md','NOTICE.md']]
 license_label='MIT (software / HTML template); CC BY-NC-SA-4.0 (SOIL content / adapted skill)'
 source={'repository':REPO,'commit':PIN,'license':license_label,'author':'李俊儀','official':False,'upstream_preserved':True,'case_studies':['soil-teaching-showcase'],'method':'Original Mode C semantic template, 1600×900 scaling, fragment progressive disclosure, advance/retreat controller, local navigation/print/reduced motion; custom mathematical diagrams and Japanese copy.','modifications':['Original index template replaced with six authored SOIL-role sections.','Original CSS retained and overridden with a Japanese paper/forest visual system.','Original slides.js retains render/advance/retreat; Japanese labels and same-origin frame API added.','User-authorized plan/style is recorded instead of waiting for repeated confirmation.'],'fonts':{'japanese':fam,'latin':'Manrope','license':'OFL-1.1','source_commit':'66928797f271fed5ee428544e7229685e2d90127','full_font_files':fontfiles+[latin]},'license_boundaries':{'upstream_software':'MIT','upstream_method_and_skill':'CC BY-NC-SA-4.0','adapted_skill':'CC BY-NC-SA-4.0','lesson_numbers_and_copy':'original educational example; no claims of real results'},'source_refs':refs}
 jwrite(OUT/'SOURCE.json',source);jwrite(OUT/'PROVENANCE.json',source)
 readme='''# 割合は、全体との比べ方。

原典SOIL Teaching SlidesのMode Cテンプレートを使った、日本語6枚の算数教材です。紙色・深緑・赤橙の大きな図で、部分と全体、割合の計算、値引きの見方を説明します。数値は学習用設定です。

`index.html`を開くと、サーバーやPowerPointなしで使えます。右矢印/Space/「進む」は同じページの図や答えを一段ずつ表示し、すべて表示したら次へ進みます。左矢印は前の段階に戻ります。Home/End、ページhash、全画面、reduce motion、印刷時の全段表示は原典機構です。文字・図・配色はindex.html/styles.cssで編集できます。

原典の`assets/html-deck-template/index.html`からページ構造を作り、元`slides.js`のrender/advance/retreatとfragment状態管理を実使用しました。元styles.cssを保持して日本語用styleを追記。原本はupstream/に保存。共通slide rendererや別frameworkに置き換えていません。再生成はリポジトリの`python tools/build_soil_teaching_showcase.py`、配布物自体にはビルドが不要です。制作計画はinput/PLAN.json、依頼文はPROMPT.mdです。

## 利用条件

原作者: 李俊儀。SOIL Teaching Slides Skill（非公式の日本語改変例）。原典: https://github.com/chunyifish/soil-teaching-slides 。pinはSOURCE.jsonに記録。

HTML template/JavaScript/CSSなどソフトウェアはMIT。SOILの教育方法説明・原典SKILL・referencesおよび日本語派生SKILLはCC BY-NC-SA 4.0です。この部分を商用に再利用する許諾は含まれません。共有・改変時は帰属、変更表示、同じライセンスの継承が必要です。LICENSE/ LICENSE-CONTENT.md / NOTICE.mdを保持してください。原作者の公認・レビュー・推奨を意味しません。

書体はGoogle Fontsの原TTFとOFL原文をfonts/に同梱。Windows fontsからの抽出やremote fontを使いません。教材の日本語本文と数値は本作例で作成しました。

## 確認範囲

生成成功と主要完成画面の初回表示を軽く確認します。6枚のPNGは全段表示の静止プレビューです。全ページ詳細目視、独立レビュー、構造監査、ZIP再実行、授業での理解度、紙印刷は検証していません。技術的な生成成功と授業での採用は別の状態です。
'''
 write(OUT/'README.md',readme)
 write(FORK/'SKILL.md','''---
name: soil-teaching-ja
description: SOIL原典の認知的ページ役割とMode CオフラインHTMLで、大きな日本語と意味のある段階図を持つ教材を作る。
---

# SOIL 日本語教材スライド（非公式）

最初に各ページの題名、教える一点、学習者の作業、認知的役割、図の関係、短いラベル、結論を計画する。既定は計画確認を待つ。ユーザーが内部計画・題材・Mode C・styleを明示承認済みなら、その承認をinput/PLANに記録し、工程ごとの再確認は省略する。本作例はこの条件で制作した。

1. 同梱upstream/SKILL.mdとreferences/html-slide-deck.mdを必要範囲で読む。全体/部分、比較、順序、練習など、そのページの思考関係に合わせて図を決める。
2. assets/html-deck-templateを出力へコピー。1600×900 stage、semantic section、見出しとのaria-labelledby、unique data-slide-id、local styles.css/slides.jsを保つ。元テンプレートを直接変更しない。
3. 日本語を大きく短く配置。HTML/SVGの区画・線・数値で関係を示す。原典.fragmentを使い、題名・学習者の作業は最初から、根拠・答えは教える順で段階表示する。
4. 元controllerのadvance/retreatとfragment count、矢印/Space/Home/End/hash、全画面、reduce motion、印刷全段表示を保持する。CDN・remote font・analytics・新frameworkは不要。
5. 原典scripts/validate_html_deck.mjsを実行する。全頁を1280×720と1920×1080で確認し、文字・図・段階表示・キー操作・hash・全段表示の印刷を検査して直す。授業での理解度や紙での印刷品質は別に確認する。

実例はexample/、依頼と計画はexample/input/。index.htmlを直接開いて使える。大きい日本語の書体を変えるときは、配布許諾のある実TTFと原文ライセンスを含める。

SOIL Teaching Slides Skill by 李俊儀。原典 https://github.com/chunyifish/soil-teaching-slides 。この日本語改変SKILLと元の方法説明はCC BY-NC-SA 4.0（非商用・帰属・継承）、実行HTML template/JS/CSSはMIT、書体はOFL。原典の公認ではない。LICENSE-CONTENT.md/NOTICE.md/原MITを保持。
''')
 shutil.copytree(ud,FORK/'upstream',dirs_exist_ok=True)
 for name in ['LICENSE','LICENSE-CONTENT.md','NOTICE.md']:shutil.copy2(OUT/name,FORK/name)
 write(FORK/'README.md','# SOIL日本語Mode Cキット\n\n非公式改変。SKILL/教育方法説明はCC BY-NC-SA 4.0（非商用・帰属・同一条件継承）、software/HTML templateはMIT、同梱書体はOFLです。詳細はLICENSE-CONTENT.mdとNOTICE.md。example/index.htmlを開いて使えます。\n')
 jwrite(FORK/'SOURCE.json',source)
 base='examples/repositories/soil-teaching-showcase/'
 case={'id':'soil-teaching-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'soil-teaching-ja','page_count':6,'format':'html','preview_kind':'html','preview_canvas':{'width':1600,'height':900},'preview_options':{'preview':'1'},'style':'紙色 × 深緑 × 赤橙 / 全体と部分の段階図','use_case':'算数教材・割合の理解','preview':base+'index.html','cover':base+'render/slide-01.png','interior':base+'render/slide-02.png','artifact_download':'downloads/soil-teaching-example-ja.zip','source_download':'downloads/soil-teaching-example-ja.zip','fork_download':'downloads/soil-teaching-ja.zip','input':base+'input/BRIEF.md','input_data':base+'input/data.json','prompt':base+'PROMPT.md','prompt_text':PROMPT,'provenance':base+'PROVENANCE.json','qa':base+'QA.json','guide':base+'README.md','titles':TITLES,'notes':NOTES,'sample_notice':'数値は学習用設定です。教育方法・派生SKILLは非商用のCC BY-NC-SA 4.0、softwareはMIT。','license':license_label,'caveats':['SOIL method/skill/reference text and adapted Japanese SKILL: CC BY-NC-SA-4.0; noncommercial, attribution and share-alike required.','Executable HTML/CSS/JS template: MIT. Fonts: OFL-1.1.','Unofficial adaptation; no endorsement or lesson-effectiveness claim.'],'method':source['method'],'navigation':'native-runtime-bridge','editability':'Native HTML text and inline SVG diagrams; local CSS and original JavaScript controller','status':'generated','execution_status':'generated','preview_notice':'原典SOIL Mode Cを日本語化。Web図解を段階表示。教育方法/SKILLはCC BY-NC-SA 4.0。','representative_previews':[base+f'render/slide-{n:02}.png' for n in [1,2]],'preview_image_notice':'全6枚の全段表示PNG。主要画面の初回表示のみ確認、全ページ詳細目視は未実施。'}
 guide={'repository':REPO,'production_status':'generated','execution_status':'generated','execution_type':'original_soil_mode_c_html_template_controller','case_ids':[case['id']],'summary_ja':'原典SOILの認知的ページ役割とMode C template/controllerを実使用した、割合の日本語6枚教材。','requirements':['Chrome/Edge等のbrowser（offline可）','再生成のみPython3.10+'],'steps':['各ページの学習者taskとSOIL役割を記録','原典HTML/CSS/JSをコピーして日本語contentと図を作る','原典fragmentで根拠から答えを順に表示','主要完成画面を一度開く'],'commands':['python tools/build_soil_teaching_showcase.py'],'source_refs':refs,'upstream_commit':PIN,'license':license_label,'license_note':'softwareはMIT、SOIL method/SKILL/referencesと派生日本語SKILLはCC BY-NC-SA 4.0。非商用・帰属・継承条件を保持。','caveats':case['caveats'],'skill':'skill-forks/soil-teaching-ja/SKILL.md','guide':case['guide']}
 guide['license_notice_ja']='ソフトウェアはMIT。SOIL方法説明と日本語スキルの派生はCC BY-NC-SA 4.0で、非商用・帰属・継承条件があります。'
 jwrite(ROOT/'data/sol-soil-teaching-repository-examples.json',[case]);jwrite(ROOT/'data/sol-soil-teaching-repository-guides.json',[guide])
 jwrite(OUT/'QA.json',{'status':'generated','generation':'six semantic HTML slides created from original template','checks':[],'limitations':['Main display pending','No all-page detailed visual review, independent review, structural audit, ZIP re-execution or classroom-effectiveness test.']})
 package()
 print('Generated six-page SOIL Mode C:',OUT/'index.html','; Japanese font:',fam)

def package():
 # Include the completed source example in the skill kit to make instructions concrete.
 shutil.copytree(OUT,FORK/'example',dirs_exist_ok=True,ignore=shutil.ignore_patterns('.private','__pycache__','node_modules'))
 for folder,name in [(OUT,'soil-teaching-example-ja'),(FORK,'soil-teaching-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.relative_to(folder).parts)&{'.private','__pycache__','node_modules'}:z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

def render():
 from playwright.sync_api import sync_playwright
 (OUT/'render').mkdir(exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  page=browser.new_page(viewport={'width':1600,'height':900},device_scale_factor=1)
  page.goto((OUT/'index.html').as_uri()+'?preview=1')
  page.evaluate('document.fonts.ready');page.wait_for_timeout(250)
  for n in range(6):
   page.evaluate('(n)=>window.soilDeck.show(n,true)',n);page.wait_for_timeout(250)
   page.screenshot(path=str(OUT/'render'/f'slide-{n+1:02}.png'))
  browser.close()
 print('Rendered 6 all-fragment PNG previews. No all-page visual audit was performed.')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--package-only',action='store_true');parser.add_argument('--render',action='store_true');args=parser.parse_args()
 if args.render:render()
 elif args.package_only:package()
 else:main()
