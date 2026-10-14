"""SlideFly persistent actors, original inline and standard-library PPTX exporter."""
from pathlib import Path
import base64,hashlib,json,re,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'examples/repositories/slidefly-showcase';FORK=ROOT/'skill-forks/slidefly-ja';UP=ROOT/'.build/actual-upstreams/andyluu98__slidefly';SK=UP/'skill/slidefly';COMMIT='7de466df3f2e0199c4939ccbe4490688d4165fa3';REPO='andyluu98/slidefly'
TITLE='街を歩く、寄り道を選ぶ。'
PROMPT='SlideFlyの原典morph-engine/nav/frames/free-layoutとinline-assets.pyを使い、日本語6枚「街を歩く、寄り道を選ぶ。」を制作。架空の散歩企画で実在地点・営業情報・天気・実績は主張しない。同じnamed actorの旅人・道・目印が6poseで動き、道の分岐はSVGで説明。暖かな紙・朱橙・深緑、大きな和文とSpace Groteskの英数字。日本語は意味の切れ目で明示改行。カード反復なし。原典の標準Python export-pptxで文字/actor編集とMorph設定を作り、実再生を確かめた範囲と区別する。'
TITLES=[TITLE,'目的地を、\nひとつ減らす。','曲がる理由は、\n気分でいい。','立ち止まる場所も、\n予定のひとつ。','帰り道には、\n違う曲がり角。','歩いたあとに、\n次の寄り道を。']
NOTES=['架空の散歩企画。地図・道の位置は説明用の創作です。','行きたい場所を詰め込む前に、一つだけ選ぶ案です。距離や所要時間を保証するものではありません。','明るい通りか静かな道か、気分で選ぶ分岐の例。実在地点の道案内ではありません。','途中で立ち止まりたい場所を選ぶ案です。ベンチの設置や営業時間の情報ではありません。','行きと違う曲がり角を選ぶ、という余地を残します。通行の可否や安全を確認した地図ではありません。','見つけたことを一言残して、次の散歩の選択肢にする提案です。効果の実績ではありません。']
CSS=r'''
.deck-stage{--actors:"trail marker traveler";--dense-stage:diagram;--font-display:"Zen Kaku Gothic New",sans-serif;--font-body:"Zen Kaku Gothic New",sans-serif;--bg:#F3EFE2;--fg:#16201D;--muted:#415148;--accent:#CF5033;--card-bg:transparent;--card-fg:#16201D;--card-radius:0px;--title-weight:700;--title-tracking:-.035em;--title-case:none;--bullet-radius:0px}
[data-actor="trail"]{background-color:#1B5D4A;--x:2200px;--y:500px;--w:650px;--h:32px;--r:0deg}
[data-actor="marker"]{background-color:#F4C95B;border:5px solid #16201D;border-radius:0%;--x:2200px;--y:750px;--w:130px;--h:130px}
[data-actor="traveler"]{background-color:#CF5033;border-radius:50%;--x:2200px;--y:250px;--w:150px;--h:150px}
[data-pose="p1"] [data-actor="trail"]{--x:1200px;--y:695px;--w:690px;--h:38px;--r:-23deg}
[data-pose="p1"] [data-actor="traveler"]{--x:1410px;--y:335px;--w:175px;--h:175px}
[data-pose="p1"] [data-actor="marker"]{--x:1640px;--y:700px;--w:130px;--h:130px;--r:18deg}
[data-pose="p2"] [data-actor="trail"]{--x:1080px;--y:697px;--w:680px;--h:30px;--r:0deg}
[data-pose="p2"] [data-actor="traveler"]{--x:1330px;--y:573px;--w:120px;--h:120px}
[data-pose="p2"] [data-actor="marker"]{--x:1675px;--y:600px;--w:110px;--h:110px;--r:0deg}
[data-pose="p3"] [data-actor="trail"]{--x:1350px;--y:790px;--w:475px;--h:24px;--r:-18deg}
[data-pose="p3"] [data-actor="traveler"]{--x:1595px;--y:650px;--w:95px;--h:95px}
[data-pose="p3"] [data-actor="marker"]{--x:1260px;--y:748px;--w:90px;--h:90px;--r:45deg}
[data-pose="p4"] [data-actor="trail"]{--x:1150px;--y:770px;--w:530px;--h:65px;--r:0deg}
[data-pose="p4"] [data-actor="traveler"]{--x:1350px;--y:570px;--w:170px;--h:95px;border-radius:12%}
[data-pose="p4"] [data-actor="marker"]{--x:1740px;--y:520px;--w:95px;--h:270px;--r:0deg}
[data-pose="p5"] [data-actor="trail"]{--x:1320px;--y:160px;--w:42px;--h:690px;--r:24deg}
[data-pose="p5"] [data-actor="traveler"]{--x:1560px;--y:350px;--w:115px;--h:115px;border-radius:50%}
[data-pose="p5"] [data-actor="marker"]{--x:1460px;--y:840px;--w:240px;--h:55px;--r:0deg}
[data-pose="p6"] [data-actor="trail"]{--x:1190px;--y:780px;--w:650px;--h:26px;--r:0deg}
[data-pose="p6"] [data-actor="traveler"]{--x:1350px;--y:290px;--w:360px;--h:360px;border-radius:50%}
[data-pose="p6"] [data-actor="marker"]{--x:1615px;--y:680px;--w:155px;--h:90px;--r:-8deg}
.slide.walk{padding:0!important}.walk-title{font-family:var(--font-display);font-weight:700;line-height:1.25;letter-spacing:-5px;white-space:pre-line;margin:0}.walk-body{font-size:37px;line-height:1.8;white-space:pre-line;margin:0}.walk-label{font:500 25px "Space Grotesk","Zen Kaku Gothic New",sans-serif;margin:0}.walk-note{font-size:21px;line-height:1.65;margin:0;color:#415148}.walk svg{color:#16201D}.walk .walk-rule{height:2px;background:#1B5D4A}.deck-stage[data-pose="p3"]{--accent:#F4C95B}.slide[data-frame="media-left"] .frame-panel{border-radius:0}.walk .frame-panel{z-index:-1}
'''
BRANCH='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 520" aria-label="架空の分岐図"><path d="M75 455 L310 265 L585 65 M310 265 L625 450" fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="square"/><circle cx="310" cy="265" r="25" fill="#CF5033"/><rect x="560" y="45" width="55" height="55" fill="#F3EFE2" stroke="currentColor" stroke-width="3"/><rect x="600" y="423" width="55" height="55" fill="#F3EFE2" stroke="currentColor" stroke-width="3"/></svg>'
def block(tag,cls,text,x,y,w,h,size=None):
 sty=f'position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
 if size:sty+=f'font-size:{size}px;'
 return f'<{tag} class="{cls}" style="{sty}">{text}</{tag}>'
def markup():
 slides=[];body=['気になる場所を一つだけ。\n残りは、歩きながら決める。','予定に空白があると、\n曲がり角を選び直せる。','明るい通り。静かな道。\nどちらも、今日は仮の選択肢。','眺める。メモする。何もしない。\n途中で止まる時間を残す。','行きとは違う景色を、\n帰りにひとつ見つける。','見つけたことを一言だけ。\n次に歩くときの入口に。']
 for i in range(6):
  title=TITLES[i] if i else '街を歩く、\n寄り道を選ぶ。';x=1040 if i==2 else 110;tw=770 if i==2 else 1100;ts=98 if i==2 else 115
  extra=' data-frame="media-left" data-stage="diagram"' if i==2 else ''
  s=f'<section class="slide walk" data-layout="free" data-pose="p{i+1}"{extra}>'
  s+=block('p','walk-label reveal',f'{i+1:02} / WALK &amp; WANDER',110,76,900,60)
  s+=block('h1' if i==0 else 'h2','walk-title reveal',title,x,235 if i!=2 else 220,tw,355,ts)
  s+=block('p','walk-body reveal',body[i],x,645 if i!=2 else 505,tw,205)
  s+=block('div','walk-rule','',110,952,1690,2)
  s+=block('p','walk-note','架空の散歩企画 / 道・地点は創作の説明図です。',110,980,1480,55)
  if i==2:s+=f'<div style="position:absolute;left:95px;top:250px;width:775px;height:570px">{BRANCH}</div>'
  slides.append(s+'</section>')
 return '\n'.join(slides)
BRIDGE='''<script>document.querySelectorAll('.deck-edge').forEach(b=>{const label=b.classList.contains('prev')?'前のスライド':'次のスライド';b.setAttribute('aria-label',label);b.setAttribute('title',label)});addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))deck.go(e.data.index)});const stage=document.querySelector('.deck-stage');new MutationObserver(()=>{if(parent!==window)parent.postMessage({type:'yebisu-page',index:deck.index,total:deck.count},location.origin)}).observe(stage,{attributes:true,attributeFilter:['data-slide']});</script>'''
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def main():
 OUT.mkdir(parents=True,exist_ok=True);FORK.mkdir(parents=True,exist_ok=True);dst=OUT/'upstream'
 if not dst.exists():
  dst.mkdir();shutil.copytree(SK/'scripts',dst/'scripts');(dst/'assets/styles').mkdir(parents=True)
  for p in (SK/'assets').glob('morph-*'):
   if p.is_file():shutil.copy2(p,dst/'assets'/p.name)
  for name in ['co-che-morph.md','tu-thiet-ke.md','xuat-pptx.md']:write(dst/'references'/name,(SK/'references'/name).read_text(encoding='utf-8'))
  shutil.copy2(SK/'assets/styles/bauhaus.css',dst/'assets/styles/bauhaus-reference.css');shutil.copy2(SK/'SKILL.md',dst/'SKILL.md');write(dst/'templates/deck-khung.html',(SK/'templates/deck-khung.html').read_text(encoding='utf-8'))
 if not (dst/'assets/icons').exists():shutil.copytree(SK/'assets/icons',dst/'assets/icons')
 shutil.copy2(UP/'LICENSE',OUT/'LICENSE')
 fontcss=''
 for folder,file,fam,weight in [('zenkakugothicnew','ZenKakuGothicNew-Regular.ttf','Zen Kaku Gothic New','400'),('zenkakugothicnew','ZenKakuGothicNew-Bold.ttf','Zen Kaku Gothic New','700'),('spacegrotesk','SpaceGrotesk[wght].ttf','Space Grotesk','300 700')]:
  src=ROOT/'downloads/fonts'/folder/file;(OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(src,OUT/'fonts'/file);shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt');fontcss+=f'@font-face{{font-family:"{fam}";src:url(data:font/ttf;base64,{base64.b64encode(src.read_bytes()).decode()});font-weight:{weight};font-display:block}}\n'
 write(OUT/'walk.css',fontcss+CSS)
 css=['morph-base.css','morph-layouts.css','morph-layouts-plus.css','morph-frames.css','morph-motion.css']
 scripts=['morph-frames.js','morph-engine.js','morph-nav.js','morph-audit.js']
 html='<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+TITLE+'</title>'+''.join(f'<link rel="stylesheet" href="upstream/assets/{f}">' for f in css)+'<link rel="stylesheet" href="walk.css"></head><body><div class="deck-viewport"><div class="deck-stage">'+markup()+'</div></div>'+''.join(f'<script src="upstream/assets/{f}"></script>' for f in scripts)+BRIDGE+'</body></html>'
 write(OUT/'source.html',html);write(OUT/'PROMPT.txt',PROMPT);write(OUT/'input/BRIEF.md','# 制作依頼\n\n'+PROMPT);write(OUT/'input/data.json',json.dumps({'title':TITLE,'titles':TITLES,'notes':NOTES,'sample_notice':'架空の散歩企画。実在地点・営業時間・天気・実績を示しません。','poses':[f'p{i}' for i in range(1,7)]},ensure_ascii=False,indent=2));write(OUT/'.gitignore','**/__pycache__/\n*.log\n')
 subprocess.run([sys.executable,str(dst/'scripts/inline-assets.py'),str(OUT/'source.html'),str(OUT/'index.html')],check=True)
 subprocess.run([sys.executable,str(dst/'scripts/export-pptx.py'),str(OUT/'index.html'),str(OUT/'deck.pptx')],check=True)
 finish()
def finish():
 source={'repository':REPO,'commit':COMMIT,'license':'MIT','scope':'Original persistent actor engine/nav/frames and inline/export scripts; bespoke six-pose Japanese free-layout deck','upstream_preserved':True,'case_studies':['slidefly-showcase']}
 write(OUT/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2));refs=[{'path':f,'sha256':hashlib.sha256((UP/f).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{COMMIT}/{f}'} for f in ['skill/slidefly/SKILL.md','skill/slidefly/assets/morph-engine.js','skill/slidefly/assets/morph-nav.js','skill/slidefly/assets/morph-frames.js','skill/slidefly/scripts/inline-assets.py','skill/slidefly/scripts/export-pptx.py','LICENSE']]
 write(OUT/'PROVENANCE.json',json.dumps(dict(source,source_refs=refs,method='Original deck template structure and custom free-layout guidance; original morph-engine persistent named actors transition via six CSS poses; frames/media-left, original nav/audit/inline-assets and export-pptx scripts.',modifications=['Custom walk.css and six authored layouts/poses, no named preset reused.','Bauhaus reference consulted for flat shape/movement vocabulary only; original CSS retained as reference.','Full local JP/Latin TTF embedded in authored CSS; no Google import or network service.','Same-origin frame bridge observes original stage data-slide; core runtime unchanged.'],editability='PPTX text boxes and named actor shapes are editable; inline SVG artwork is vector imagery. Original exporter writes Morph transition metadata; PowerPoint Morph playback not claimed until specifically observed.'),ensure_ascii=False,indent=2))
 write(OUT/'README.md','''# 街を歩く、寄り道を選ぶ。

架空の散歩企画、6枚。道と地点は創作で、実在地点の道案内・営業情報・天気・実績ではありません。暖かな紙・朱橙・深緑、意味単位で改行した和文と道の分岐図で構成。

原典SlideFlyのmorph-engine/nav/frames、free-layoutの指針を実使用。同じ旅人・道・目印actorが6poseで移動・形状変更。カード反復やpreset名の借用ではありません。原典inline-assets.pyで単一HTML化。原典export-pptx.py（標準Pythonのみ）でPPTX生成。

HTMLではnamed actorのMorph状動作。PPTXは文字とactorが編集可能、inline SVGはvector画像。Morph設定は原典exporterで付与しますが、PowerPoint内の実Morph再生確認とは区別します。HTMLの書体はフルTTF内包。PPTXはGoogle importがないので書体未埋込、fonts/の原TTFを手動導入してください（OFL同梱）。

再生成: `python upstream/scripts/inline-assets.py source.html index.html` → `python upstream/scripts/export-pptx.py index.html deck.pptx`。styleはwalk.css、内容はsource.html、原データはinput/data.json。原典runtimeは未変更。原MITはLICENSE、帰属と使用commitはSOURCE/PROVENANCE。

確認は原典deck.auditと主画面・一回の動き。全ページ詳細目視・独立レビュー・native監査・ZIP再実行は行いません。
''')
 write(FORK/'SKILL.md','''---
name: slidefly-ja
description: SlideFly原典の同一actorとposeを使い、日本語Morph状HTMLとPPTXを作る。
---

# 同じ形が、ページをまたいで動くスライド

1. upstream/SKILL.mdとreferences/co-che-morph.mdを読む。題材の移動・関係をnamed actorに割り当て、各ページで位置/大きさ/形を変えるposeを作る。
2. 原典morph-engine/nav/framesを使い、HTMLのstage/slide構造を保つ。独自layoutは原典free-layout指針で作る。本文は意味の切れ目で改行、明示改行はwhite-space:pre-line。
3. 見出し/本文はZen Kaku Gothic New、英数字はSpace Groteskなど役割を決める。図は内容を説明し、actorと文字が重ならないよう配置。
4. `python upstream/scripts/inline-assets.py source.html index.html` で単一HTML。PPTXが必要なら原典 `export-pptx.py index.html deck.pptx` を使う。通常Pythonだけで実行できる。
5. deck.auditと主画面・一回の動きを確認。PPTXの編集可能文字/actor、vector SVG、Morph設定と実再生を区別して報告する。

技能本文だけでruntimeは付属しない。一式ZIPと作品ZIPのsource/walk.cssを使用。原MITと使用原TTF/OFLを保持。書体の端末導入は手動。
''')
 if not (FORK/'upstream').exists():shutil.copytree(OUT/'upstream',FORK/'upstream',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 shutil.copy2(UP/'LICENSE',FORK/'LICENSE');source['files']=[{'path':p.relative_to(FORK).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json'];write(FORK/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 case={'id':'slidefly-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':COMMIT,'fork_id':'slidefly-ja','page_count':6,'format':'html','preview_kind':'html','preview_canvas':{'width':1920,'height':1080},'style':'暖かな紙 × 朱橙 × 深緑 / 持続actorの6pose','use_case':'架空の散歩企画・Morph状プレゼン','preview':'examples/repositories/slidefly-showcase/index.html','cover':'examples/repositories/slidefly-showcase/render/slide-01.png','interior':'examples/repositories/slidefly-showcase/render/slide-01.png','artifact_download':'downloads/slidefly-example-ja.zip','source_download':'downloads/slidefly-example-ja.zip','fork_download':'downloads/slidefly-ja.zip','pptx_download':'examples/repositories/slidefly-showcase/deck.pptx','input':'examples/repositories/slidefly-showcase/input/BRIEF.md','input_data':'examples/repositories/slidefly-showcase/input/data.json','prompt':'examples/repositories/slidefly-showcase/PROMPT.txt','prompt_text':PROMPT,'provenance':'examples/repositories/slidefly-showcase/PROVENANCE.json','qa':'examples/repositories/slidefly-showcase/QA.json','guide':'examples/repositories/slidefly-showcase/README.md','titles':TITLES,'notes':NOTES,'sample_notice':'架空企画。道の位置は創作、実在地点・営業時間・天気・実績ではありません。','method':'Original morph-engine/nav/frames/free-layout and inline-assets/export-pptx; custom actors/poses.','navigation':'native-runtime-bridge','editability':'HTML; native PPTX text/actor shapes, vector SVG artwork','status':'generated','execution_status':'generated','representative_previews':['examples/repositories/slidefly-showcase/render/slide-01.png'],'preview_image_notice':'単一HTML全6枚の代表静止プレビュー1枚。動きはHTMLで再生。'}
 write(ROOT/'data/sol-slidefly-repository-examples.json',json.dumps([case],ensure_ascii=False,indent=2));guide={'repository':REPO,'production_status':'generated','execution_status':'generated','execution_type':'original_morph_engine_inline_export','case_ids':[case['id']],'summary_ja':'原典persistent actor方式で架空の散歩企画6枚。単一HTMLと原典標準Python exporterのPPTX。','requirements':['Python3.10+','Chrome/Edge','PPTXはPowerPoint2019/365でMorph対応'],'steps':['named actorと6poseを作る','free-layoutとframeで和文を配置','原典inline-assetsで単一HTML化','原典auditと一回の動きを確認する'],'commands':['python upstream/scripts/inline-assets.py source.html index.html','python upstream/scripts/export-pptx.py index.html deck.pptx'],'source_refs':refs,'upstream_commit':COMMIT,'license':'MIT','skill':'skill-forks/slidefly-ja/SKILL.md','guide':case['guide']};write(ROOT/'data/sol-slidefly-repository-guides.json',json.dumps([guide],ensure_ascii=False,indent=2))
def package():
 for folder,name in [(OUT,'slidefly-example-ja'),(FORK,'slidefly-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.log'}:z.write(p,(Path(name)/p.relative_to(folder)).as_posix())
if __name__=='__main__':main()
