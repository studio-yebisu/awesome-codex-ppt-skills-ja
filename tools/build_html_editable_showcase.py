"""Create a Japanese HTML brand proposal; invoke Hasasasa's original converter."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'examples/repositories/html-editable-showcase'
UP=ROOT/'.build/actual-upstreams/Hasasasa__html-to-editable-pptx'
FORK=ROOT/'skill-forks/html-editable-ja'
COMMIT='17c1dbb76e958543dc2741a7d50ca374354f33b7'
REPO='Hasasasa/html-to-editable-pptx'
TITLES=['小さな店の、ひとつの旗。','味の前に、姿勢が伝わる。','深い茶色に、ひと筋のレモン。','店先から、手元まで。','一杯の記憶を、店の旗に。']
NOTES=['架空の焙煎所「ひと旗」のブランド提案です。HTMLから編集できるPPTXへ変換します。','新しさを追うより、今日の一杯を丁寧にする。その姿勢を短い言葉と記号へまとめます。','レモン色は目印、濃い茶色は豆と焙煎、墨黒は文字に使う案です。和文・本文・英数字の役割を分けます。','看板、袋、棚札にひとつの旗を展開。寸法・印刷条件・素材は制作時に確認します。','提案段階です。店の言葉と印刷サンプルを確かめ、採用する範囲を決めます。売上や効果の実績ではありません。']
PROMPT='原典 Hasasasa/html-to-editable-pptx のSKILLとconvert.pyを使い、架空焙煎所「ひと旗」の日本語ブランド提案を5枚制作。題名「小さな店の、ひとつの旗。」。レモン色×墨黒×濃いコーヒー茶。大胆な和文タイポ、余白、HTML/SVG図形、誌面ごとの構図変化。角丸カードなし。HTML原稿のテキストと簡単な図形を編集できるPPTXへ変換。実在ブランド・売上実績・効果数値を捏造しない。見出しZen Kaku Gothic New、引用Shippori Mincho、英数字Manrope。使用原TTF/OFLとMIT帰属を保持。'
HTML=r'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小さな店の、ひとつの旗。 — 焙煎所のブランド提案</title><style>
@font-face{font-family:'Zen Kaku Gothic New';src:url('fonts/ZenKakuGothicNew-Regular.ttf');font-weight:400}@font-face{font-family:'Zen Kaku Gothic New';src:url('fonts/ZenKakuGothicNew-Black.ttf');font-weight:900}@font-face{font-family:'Shippori Mincho';src:url('fonts/ShipporiMincho-Bold.ttf');font-weight:700}@font-face{font-family:Manrope;src:url('fonts/Manrope[wght].ttf');font-weight:200 800}
*{box-sizing:border-box}html,body{margin:0;overflow:hidden;background:#151b1d}#stage{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}.slide{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#f4f0df;color:#151b1d;visibility:hidden;font-family:'Zen Kaku Gothic New',sans-serif}.slide.active{visibility:visible}.kicker{position:absolute;left:100px;top:75px;font:600 23px Manrope;letter-spacing:3px}.caption{position:absolute;left:100px;bottom:50px;font-size:21px}.label{font:600 24px Manrope;letter-spacing:2px}h1,h2,h3,p{margin:0}h1,h2{font-weight:900;line-height:1.25;letter-spacing:-5px}.cover{background:#edeb63}.cover h1{position:absolute;left:95px;top:245px;font-size:147px}.cover .subtitle{position:absolute;left:104px;top:695px;font-size:36px;line-height:1.7}.brand{font:600 28px Manrope;letter-spacing:3px;position:absolute;right:100px;top:80px}.flag-pole{position:absolute;left:1430px;top:285px;width:11px;height:530px;background:#38271f}.flag-cloth{position:absolute;left:1440px;top:285px;width:315px;height:245px;background:#38271f}.cover .flag-cloth{border-right:80px solid #edeb63;border-top:122px solid transparent;border-bottom:123px solid transparent}.principle{background:#38271f;color:#f4f0df}.principle .kicker{color:#edeb63}.principle h2{position:absolute;left:100px;top:215px;font-size:109px}.principle .quote{position:absolute;left:105px;top:645px;font-family:'Shippori Mincho',serif;font-weight:700;font-size:56px;line-height:1.6}.principle .body{position:absolute;right:140px;bottom:160px;width:630px;font-size:31px;line-height:1.9;color:#cfc0aa}.line{position:absolute;left:1070px;top:340px;width:2px;height:510px;background:#8f7963}.identity h2{position:absolute;left:100px;top:190px;font-size:101px}.swatches{position:absolute;left:100px;top:540px;display:flex;gap:0}.swatch{width:515px;height:275px;padding:35px}.swatch h3{font-size:43px;font-weight:900}.swatch p{margin-top:20px;font-size:25px;line-height:1.6}.lemon{background:#edeb63}.coffee{background:#38271f;color:#f4f0df}.ink{background:#151b1d;color:#f4f0df}.identity .type-note{position:absolute;left:105px;bottom:135px;font-size:26px}.touch h2{position:absolute;left:100px;top:185px;font-size:109px}.touch .board{position:absolute;left:100px;top:480px;width:430px;height:345px;background:#38271f;color:#edeb63;padding:55px}.touch .board h3{font-size:76px;letter-spacing:5px;font-weight:900}.touch .board p{font:600 19px Manrope;margin-top:23px;letter-spacing:3px}.touch .bag{position:absolute;left:740px;top:425px;width:340px;height:480px;background:#edeb63;border-top:35px solid #38271f}.touch .bag h3{position:absolute;left:50px;top:45px;font-size:68px;line-height:1.2;font-weight:900}.touch .bag p{position:absolute;left:50px;bottom:45px;font:600 20px Manrope;letter-spacing:2px}.touch .ticket{position:absolute;left:1300px;top:570px;width:450px;height:220px;background:#f4f0df;border-top:8px solid #38271f;border-bottom:2px solid #38271f;padding:35px}.touch .ticket h3{font-size:47px;font-weight:900}.touch .ticket p{font-size:25px;margin-top:20px}.touch .touch-label{position:absolute;top:925px;font-size:26px}.closing{background:#edeb63}.closing h2{position:absolute;left:100px;top:225px;font-size:145px}.closing .steps{position:absolute;left:110px;bottom:195px;display:flex;gap:55px}.closing .steps p{font-size:28px;border-top:2px solid #151b1d;width:420px;padding-top:22px;line-height:1.8}.closing .steps b{font:700 21px Manrope;margin-right:20px}.closing .caption{font-size:21px}.controls{position:fixed;right:25px;bottom:20px;background:#151b1de0;color:#edeb63;padding:9px 15px;font:14px Manrope;display:flex;align-items:center;gap:12px;z-index:30}.controls button{background:transparent;color:#edeb63;border:0;font-size:24px;cursor:pointer}@media(prefers-reduced-motion:reduce){*{animation:none;transition:none}}
</style></head><body><main id="stage">
<section class="slide cover active" data-pptx-slide><p class="kicker">HITOHATA / ROASTERY BRAND PROPOSAL</p><p class="brand">ひと旗</p><h1>小さな店の、<br>ひとつの旗。</h1><p class="subtitle">焙煎所のブランド提案<br>いい一杯に、目印を。</p><div class="flag-pole"></div><div class="flag-cloth"></div><p class="caption">架空ブランド「ひと旗」 / 実在の店舗・商品ではありません</p></section>
<section class="slide principle" data-pptx-slide><p class="kicker">01 / BRAND ATTITUDE</p><h2>味の前に、<br>姿勢が伝わる。</h2><p class="quote">新しさよりも、<br>今日の一杯を、丁寧に。</p><div class="line"></div><p class="body">豆を語りすぎる前に、<br>店の姿勢をひとつの言葉へ。<br><br>「ひと旗」は、<br>小さな焙煎所の目印です。</p><p class="caption">ブランドの言葉と名前は、この提案のための創作です。</p></section>
<section class="slide identity" data-pptx-slide><p class="kicker">02 / VISUAL LANGUAGE</p><h2>深い茶色に、<br>ひと筋のレモン。</h2><div class="swatches"><div class="swatch lemon"><h3>目印になる。</h3><p>レモン色 / #EDEB63<br>旗と、ひとことのアクセント。</p></div><div class="swatch coffee"><h3>深さを添える。</h3><p>コーヒー茶 / #38271F<br>豆と焙煎を思わせる土台。</p></div><div class="swatch ink"><h3>言葉を立てる。</h3><p>墨黒 / #151B1D<br>読ませる文字と、細い罫線。</p></div></div><p class="type-note">見出しは太く。本文は端正に。英数字は、静かに添える。</p><p class="caption">配色・書体の提案です。実物の印刷色は試作で確認します。</p></section>
<section class="slide touch" data-pptx-slide><p class="kicker">03 / TOUCHPOINTS</p><h2>店先から、手元まで。</h2><div class="board"><h3>ひと旗</h3><p>COFFEE ROASTERY</p></div><div class="bag"><h3>ひと<br>旗。</h3><p>ROASTED WITH CARE</p></div><div class="ticket"><h3>今日の一杯。</h3><p>ゆっくり、味わう。</p></div><p class="touch-label" style="left:100px">看板 / 遠くから名前が届く。</p><p class="touch-label" style="left:740px">袋 / 家まで目印が続く。</p><p class="touch-label" style="left:1300px">棚札 / 選ぶ時間を急がせない。</p><p class="caption">用途のイメージ案。商品仕様、寸法、印刷条件は未決定です。</p></section>
<section class="slide closing" data-pptx-slide><p class="kicker">04 / NEXT STEP</p><h2>一杯の記憶を、<br>店の旗に。</h2><div class="steps"><p><b>01</b>店の言葉を確かめる。<br>名前と姿勢を、店主の声に。</p><p><b>02</b>小さく印刷してみる。<br>看板と袋で、色と読みやすさを。</p><p><b>03</b>使う範囲を決める。<br>無理なく続く、ひとつの目印へ。</p></div><p class="caption">架空ブランドの企画案 / 採用・販売・効果の実績ではありません</p></section>
</main><nav class="controls"><button id="prev" aria-label="前へ">←</button><span id="count"></span><button id="next" aria-label="次へ">→</button></nav><script>
let current=0;const slides=[...document.querySelectorAll('.slide')];function scale(){let f=Math.min(innerWidth/1920,innerHeight/1080);document.getElementById('stage').style.transform=`translate(${(innerWidth-1920*f)/2}px,${(innerHeight-1080*f)/2}px) scale(${f})`}function go(i){current=Math.max(0,Math.min(4,i));slides.forEach((s,n)=>s.classList.toggle('active',n===current));document.getElementById('count').textContent=`${current+1} / 5`;if(parent!==window)parent.postMessage({type:'yebisu-page',index:current,total:5},location.origin)}addEventListener('resize',scale);addEventListener('keydown',e=>{if(['ArrowRight',' '].includes(e.key))go(current+1);if(e.key==='ArrowLeft')go(current-1)});addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))go(e.data.index)});document.getElementById('prev').onclick=()=>go(current-1);document.getElementById('next').onclick=()=>go(current+1);scale();go(0);
</script></body></html>'''

ADAPTER=r'''"""Local full-TTF registry; all rendering/conversion stays in original convert.py."""
from pathlib import Path
import os,runpy,sys
HERE=Path(__file__).resolve().parent
UP=HERE/'upstream'
CACHE=HERE/'cache/fonts';CACHE.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(UP/'scripts'))
import font_paths
font_paths.CACHE_DIR=CACHE
import embed_fonts,font_resolver
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import shutil
entries=[]
for family,style,cjk,regular,bold,aliases in [
 ('Zen Kaku Gothic New','sans',True,'ZenKakuGothicNew-Regular.ttf','ZenKakuGothicNew-Black.ttf',['Noto Sans SC']),
 ('Shippori Mincho','serif',True,'ShipporiMincho-Bold.ttf','ShipporiMincho-Bold.ttf',['Noto Serif SC']),
 ('Manrope','sans',False,'Manrope[wght].ttf','Manrope[wght].ttf',[])]:
 slots={}
 for slot,filename,weight in [('regular',regular,400),('bold',bold,700)]:
  destination=CACHE/(family.replace(' ','')+'-'+slot+'.ttf')
  source=HERE/'fonts'/filename
  if '[' in filename:
   font=TTFont(source);instance=instantiateVariableFont(font,{'wght':weight},inplace=False);instance.save(destination)
  else:shutil.copy2(source,destination)
  slots[slot]=destination.name
 entries.append({'typeface':family,'charset':'128' if cjk else '0','pitchFamily':'18' if style=='serif' else '34','cjk':cjk,'style':style,'slots':slots,'aliases':aliases})
font_resolver.register_in_font_plan(entries)
font_resolver.resolve_fonts=lambda needed,bundled:{'resolved':entries,'unavailable':[],'cached':[e['typeface'] for e in entries]}
runpy.run_path(str(UP/'convert.py'),run_name='__main__')
'''

def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args()
 OUT.mkdir(parents=True,exist_ok=True);FORK.mkdir(parents=True,exist_ok=True)
 dest=OUT/'upstream'
 if not dest.exists():shutil.copytree(UP,dest,ignore=shutil.ignore_patterns('__pycache__','.git','tests','.config.local.toml','lessons-learned.md'))
 write(dest/'.config.local.toml','[fonts]\nauto_install="no"\n[cleanup]\ndefault="keep"\n[audit]\nmode="manual"\n')
 write(OUT/'index.html',HTML);write(OUT/'convert_local_fonts.py',ADAPTER)
 write(OUT/'PROMPT.txt',PROMPT+'\n')
 data={'title':'小さな店の、ひとつの旗。 — 焙煎所のブランド提案','sample_notice':'架空ブランド「ひと旗」。実在店舗・商品、売上・効果実績ではありません。','titles':TITLES,'notes':NOTES}
 write(OUT/'input/data.json',json.dumps(data,ensure_ascii=False,indent=2));write(OUT/'input/BRIEF.md','# 制作依頼\n\n'+PROMPT)
 (OUT/'fonts').mkdir(exist_ok=True)
 for folder,files in [('zenkakugothicnew',['ZenKakuGothicNew-Regular.ttf','ZenKakuGothicNew-Black.ttf']),('shipporimincho',['ShipporiMincho-Bold.ttf']),('manrope',['Manrope[wght].ttf'])]:
  for f in files:shutil.copy2(ROOT/'downloads/fonts'/folder/f,OUT/'fonts'/f)
  shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt')
 shutil.copy2(UP/'LICENSE',OUT/'LICENSE')
 write(OUT/'DEPENDENCIES.md','''# 依存と条件

原典 requirements.txt: python-pptx (MIT), lxml (BSDとlibxml2/libxsltの条件), fontTools (MIT), Playwright (Apache-2.0), Pillow (HPND)。任意のpdf2image (MIT)、pywin32 (PSF系)。Chromiumには第三者ライセンスが含まれます。実際の条件は各配布物のLICENSE/NOTICEを参照。依存バイナリ・venv・ブラウザcacheはZIPに含めません。使用フォント原TTFとSIL OFLはfonts/へ同梱。Manropeは変換用cacheに静的instanceを作り、PPTX内部のサブセットは原典処理で生成する方式ですが、今回の配布PPTXは原典 --no-embed-fonts を使用。原典の埋込版がPowerPoint COMで開かなかったためです。配布するTTFは未改変原配布物です。
''')
 if not args.prepare_only:
  py=OUT/'.venv/Scripts/python.exe'
  command=[str(py),str(OUT/'convert_local_fonts.py'),str(OUT/'index.html'),'--out',str(OUT/'deck.pptx'),'--keep-screenshots','--no-embed-fonts','--no-verify','--no-visual-audit']
  with (OUT/'convert.log').open('w',encoding='utf-8') as log:subprocess.run(command,cwd=OUT,stdout=log,stderr=subprocess.STDOUT,check=True)
 finish(data,args.prepare_only)

def finish(data,prepared):
 source={'repository':REPO,'commit':COMMIT,'license':'MIT','scope':'Original converter plus local full-TTF Japanese font registry adapter','upstream_preserved':True,'case_studies':['html-editable-showcase']}
 write(OUT/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 prov=dict(source,method='Original convert.py CLI → preflight → original Playwright measure → python-pptx assemble; original --no-embed-fonts compatibility option. Wrapper registers local Japanese font families and maps seeded Noto SC aliases to JP fonts; no converter replacement.',command='python convert_local_fonts.py index.html --out deck.pptx --keep-screenshots --no-embed-fonts --no-verify --no-visual-audit',modifications=['Local font resolver adapter only; core converter remains unchanged.','No OS font installation. Detailed structural/visual audit disabled per project scope.','Embedded-TTF output failed PowerPoint COM open; original --no-embed-fonts output opened successfully. Full original TTFs/OFL provided for manual font installation.'],source_refs=[{'path':f,'sha256':hashlib.sha256((UP/f).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{COMMIT}/{f}'} for f in ['SKILL.md','convert.py','scripts/measure.py','scripts/assemble.py','scripts/embed_fonts.py','LICENSE']])
 write(OUT/'PROVENANCE.json',json.dumps(prov,ensure_ascii=False,indent=2))
 write(OUT/'README.md','''# 小さな店の、ひとつの旗。

架空の焙煎所「ひと旗」のブランド提案、5ページ。レモン色・コーヒー茶・墨黒、和文タイポと編集誌の余白で、店の姿勢から配色、看板と袋、次の試作へつなぎます。

`index.html` は元HTML、`deck.pptx` は原典 Hasasasa/html-to-editable-pptx による編集可能なPPTX。文字と単純な図形を編集する制作方式です。OOXMLの表現制約があるため全要素の完全一致を保証しません。

原典 commit: 17c1dbb76e958543dc2741a7d50ca374354f33b7 / MIT。原文LICENSE、upstream固有converter、入力、依頼文、フルOSS日本語・英数字フォントとOFLを同梱。`convert_local_fonts.py` は日本語TTFを原典FONT_PLANへ登録し、中国語フォントの自動種子を日本語へ対応させる薄いアダプター。核心のmeasure/assemble/embed処理は変更していません。

再変換: Python環境へ `pip install -r upstream/requirements.txt` と `python -m playwright install chromium`、次に `python convert_local_fonts.py index.html --out deck.pptx --keep-screenshots --no-embed-fonts --no-verify --no-visual-audit`。OSへのフォントインストールはしません。PPTX閲覧ソフトによって内包フォントの扱いが異なり、利用端末で手動インストールが必要な場合があります。

代表プレビューはHTMLの1ページです。原典のフォント埋込版はPowerPoint COMで開かなかったため、原典の --no-embed-fonts 経路を配布。PowerPointは5枚として開けました。端末に書体が無ければ代替書体で表示されます。全ページ詳細目視、構造監査、ZIP再実行、正式採用は未実施。実施した軽い確認だけをQA.jsonに記録します。依存条件はDEPENDENCIES.mdを参照。
''')
 write(FORK/'SKILL.md','''---
name: html-editable-ja
description: HTMLスライドをHasasasa原典converterで編集可能なPPTXへ変換する。
---

# HTMLから編集できる日本語PPTX

1. 同梱 `upstream/SKILL.md` を読み、原HTMLのページを `[data-pptx-slide]` で明示する。制作方式は原典convert.pyを使う。
2. 一頁一主張。見出しZen Kaku Gothic New、引用Shippori Mincho、英数字Manropeなど役割を分ける。日本語は意味のまとまりで改行し、過密ならページを分ける。
3. 単純なHTML背景・罫線・図形はPPTX編集を活かせる。複雑装飾とSVGは画像になる場合がある。全面画像へ平坦化しない。
4. `pip install -r upstream/requirements.txt`、`python -m playwright install chromium` の後 `python convert.py input.html --out output.pptx` を実行。OSへのフォント導入はユーザー判断。
5. 日本語フォントの局所登録例と入力は同梱referencesを参照。生成成功と主要画面の初回表示だけを確認し、採用や全ページQAとは区別する。

原典MITと使用フォントOFLを保持。技能本文だけでは変換器は付属しないため、一式ZIPのupstream/とPython依存が必要。
''')
 if not (FORK/'upstream').exists():shutil.copytree(OUT/'upstream',FORK/'upstream',ignore=shutil.ignore_patterns('__pycache__','cache','.config.local.toml','lessons-learned.md'))
 shutil.copy2(UP/'LICENSE',FORK/'LICENSE');(FORK/'references').mkdir(exist_ok=True)
 shutil.copy2(OUT/'convert_local_fonts.py',FORK/'references/convert_local_fonts.py')
 write(FORK/'references/ADAPTER.md','ローカル例のconvert_local_fonts.pyは作品フォルダー内で実行します。upstream/とfonts/を隣接配置。原典CLIのmeasure/assemble/embedは変更せず、FONT_PLANへ日本語TTFを登録する例です。実行例とフルフォントは作品ZIPを参照。')
 source['files']=[{'path':p.relative_to(FORK).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json']
 write(FORK/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 case={'id':'html-editable-showcase','title':data['title'],'repository':REPO,'skill_repository':REPO,'upstream_commit':COMMIT,'fork_id':'html-editable-ja','page_count':5,'format':'pptx','preview_kind':'html','preview_canvas':{'width':1920,'height':1080},'style':'レモン × 墨黒 × コーヒー茶 / 編集できるブランド提案','use_case':'ブランド・店舗提案','preview':'examples/repositories/html-editable-showcase/index.html','cover':'examples/repositories/html-editable-showcase/render/slide-01.png','interior':'examples/repositories/html-editable-showcase/render/slide-01.png','artifact_download':'examples/repositories/html-editable-showcase/deck.pptx','source_download':'downloads/html-editable-example-ja.zip','fork_download':'downloads/html-editable-ja.zip','input':'examples/repositories/html-editable-showcase/input/BRIEF.md','input_data':'examples/repositories/html-editable-showcase/input/data.json','prompt':'examples/repositories/html-editable-showcase/PROMPT.txt','prompt_text':PROMPT,'provenance':'examples/repositories/html-editable-showcase/PROVENANCE.json','qa':'examples/repositories/html-editable-showcase/QA.json','guide':'examples/repositories/html-editable-showcase/README.md','titles':TITLES,'notes':NOTES,'sample_notice':data['sample_notice'],'method':prov['method'],'editability':'native_pptx_text_and_simple_shapes','navigation':'native-runtime-bridge','status':'prepared' if prepared else 'generated','execution_status':'prepared' if prepared else 'generated','representative_previews':['examples/repositories/html-editable-showcase/render/slide-01.png'],'preview_image_notice':'全5ページのうち代表1枚。HTML参照プレビューで、PPTX全ページの視覚一致検査ではありません。'}
 if (OUT/'render/deck.pdf').exists():
  case.update(preview_kind='powerpoint-render',preview='examples/repositories/html-editable-showcase/pptx-preview.html',pages=[f'examples/repositories/html-editable-showcase/render/slide-{i:02}.png' for i in range(1,6)],interior='examples/repositories/html-editable-showcase/render/slide-03.png',pdf_download='examples/repositories/html-editable-showcase/render/deck.pdf',comparison='examples/repositories/html-editable-showcase/index.html',comparison_label='制作HTMLを見る',preview_image_notice='完成PPTXからPowerPointで書き出した全5ページのPNGです。制作HTMLとの全ページ一致検査は行っていません。')
  case.pop('representative_previews',None)
 write(ROOT/'data/sol-html-editable-repository-examples.json',json.dumps([case],ensure_ascii=False,indent=2))
 guide={'repository':REPO,'production_status':case['status'],'execution_status':case['execution_status'],'execution_type':'original_cli_conversion_local_font_adapter','case_ids':[case['id']],'summary_ja':'原典HTML-to-editable-PPTXで架空焙煎所の日本語5枚を実制作。局所日本語TTF登録で書体を維持。','requirements':['Python 3','原典requirements依存','Playwright Chromium'],'steps':['HTMLとデータを作る','日本語原TTFを局所登録','原典CLIでmeasure/assemble/embed','主ファイルの初回表示を軽く確認'],'commands':[prov['command']],'source_refs':prov['source_refs'],'upstream_commit':COMMIT,'license':'MIT','skill':'skill-forks/html-editable-ja/SKILL.md','guide':case['guide']}
 write(ROOT/'data/sol-html-editable-repository-guides.json',json.dumps([guide],ensure_ascii=False,indent=2))
 if not prepared:package()

def package():
 for folder,name in [(OUT,'html-editable-example-ja'),(FORK,'html-editable-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.parts)&{'cache','.build','__pycache__','.venv'} and '_audit' not in p.as_posix() and p.suffix not in {'.pyc','.log'} and '_measurements' not in p.name and '_preflight' not in p.name:z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

if __name__=='__main__':main()
