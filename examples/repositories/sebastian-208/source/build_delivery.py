from pathlib import Path
import json,re,shutil,zipfile,hashlib
from PIL import Image,ImageDraw
root=Path('/workspace/shared/slide-208-prep');run=root/'run-rain-library';out=root/'delivery/examples/repositories/sebastian-208'
bp=(run/'qa/deck-blueprint.md').read_text();secs=re.split(r'\n## Slide ',bp)[1:];notes=[];slides=[]
for i,s in enumerate(secs,1):
 note=re.search(r'^Notes: (.*)',s,re.M).group(1);notes.append(note)
 slides.append({'number':i,'title':s.split('\n')[0],'copy':re.search(r'^Exact copy: (.*)',s,re.M).group(1),'direction':re.search(r'^Direction: (.*)',s,re.M).group(1),'notes':note})
for f in (run/'image_pages').glob('*.png'):
 im=Image.open(f);im.resize((1600,900),Image.Resampling.LANCZOS).save(out/'image_pages'/f.name)
for f in (run/'thumbnails').glob('*.png'):shutil.copy(f,out/'thumbnails'/f.name)
for f in (run/'qa').glob('*.md'):shutil.copy(f,out/'qa'/f.name)
notesmd='# Speaker Notes\n\n'+'\n\n'.join(f'## Slide {i:02d}\n{n}' for i,n in enumerate(notes,1))+'\n'
(out/'NOTES.md').write_text(notesmd);(run/'qa/speaker-notes.md').write_text(notesmd)
shutil.copy(run/'qa/alignment-summary.md',out/'input/BRIEF.md');(out/'input/data.json').write_text(json.dumps({'title':'雨の図書室','fictional':True,'slides':slides},ensure_ascii=False,indent=2))
shutil.copy(root/'LICENSE',out/'LICENSE');shutil.copy(root/'skills/academic-image-ppt/SKILL.md',out/'source/UPSTREAM-SKILL.md')
shutil.copy(root/'skills/academic-image-ppt/scripts/package_image_pptx_with_notes.mjs',out/'source/package_image_pptx_with_notes.upstream.mjs')
s=(root/'skills/academic-image-ppt/scripts/package_image_pptx_with_notes.mjs').read_text().replace('pptx.lang = "zh-CN"','pptx.lang = "ja-JP"').replace('pptx.author = "Academic Image PPT"','pptx.author = "Studio Yebisu"').replace('pptx.company = "Academic Image PPT"','pptx.company = "Studio Yebisu"')
(out/'source/package_image_pptx_with_notes.mjs').write_text(s)
shutil.copy(root/'package.json',out/'source/package.json');shutil.copy(root/'package-lock.json',out/'source/package-lock.json')
shutil.copy(run/'prompts/style-boards.md',out/'source/style-boards.md');shutil.copy(Path(__file__),out/'source/build_delivery.py')
prompt='原典academic-image-pptを使い、日本語の架空の空間デザイン研究提案「雨の図書室」を11頁の画像版PPTXにしてください。庇・席・記録棚の小さな公共空間を提案し、研究実績や測定値は捏造しないでください。紙白・深紺・雨灰、明朝の大胆な見出し、細線建築図、暗色の区切り。各頁はbuilt-in imagegenで16:9の画像として生成し、話者ノートを付け、付属の包装スクリプトを使ってください。本文と図は画像で、個別テキスト編集できないことを明示してください。詳細なコピー・図・ノートはinput/data.json、構成はqa/deck-blueprint.mdを参照してください。\n'
(out/'PROMPT.txt').write_text(prompt)
contract='# 自律制作の進行記録\n\nユーザーは付属原典スクリプト実行を許可し、個別の承認を求めず判断して完成するよう指示。A「雨と余白」、11頁構成、slide06実寸アンカーを制作担当の判断で採用。ユーザーがAや各サンプルを選択したとは記録しない。原典の個別承認ゲートを、自律サンプル制作の担当判断へ変更した派生である。3案ボードの枠比率は厳密な16:9ではないが、最終頁は全て1600×900。生成時1672×941を機械的リサイズ。視覚描画・文字編集はローカルで行っていない。03/05/07/09の区切りと10頁の実施前ラベルをimagegenで再生成。\n'
(out/'qa/autonomous-production.md').write_text(contract)
(run/'qa/thumbnail-style-contract.md').write_text('A 雨と余白。紙白、深紺、雨灰。日本語明朝見出しとsans本文、細線建築図。大きな余白、暗い区切り、細い引出線、雨と庇の水平線。自律判断による採用。\n')
shutil.copy(run/'qa/thumbnail-style-contract.md',out/'qa/thumbnail-style-contract.md')
(out/'README.md').write_text('# 雨の図書室\n\n架空の空間デザイン研究提案、11頁。原典academic-image-pptのbuilt-in imagegen→画像1枚/頁→ノート付きPPTX方式。\n\nindex.htmlで完成PNGを再生、deck.pptxをPowerPointで開く。本文・図はページ画像であり個別テキストや図形として編集できない。画像差替えと話者ノートの編集は可能。\n\n入力はinput/BRIEF.md、data.json。全体依頼はPROMPT.txt。原典固定commit、変更点と確認範囲はPROVENANCE.jsonとQA.json。\n\n再包装: npm install --ignore-scripts --cache /tmp/slide208-npm-cache、node source/package_image_pptx_with_notes.mjs --images image_pages --notes NOTES.md --out deck.pptx --title 雨の図書室。依存pptxgenjs 4.0.1。画像生成はbuilt-in imagegenを使い、課金APIを追加利用していない。\n\n書体名は画像生成時の意図。実フォント使用・埋込・再配布は確認していない。画像には架空の構想を描く。施工図や研究成果ではない。\n')
(out/'SKILL.ja.md').write_text('---\nname: rain-library-academic-image-ppt-ja\ndescription: 原典academic-image-pptに基づく日本語の画像版研究提案スライド\n---\n\n# 日本語・画像版研究提案\n\n原典: https://github.com/demoolight/academic-image-ppt/tree/2aac1a711ff658ab67d79a0e98cc54b5a0468751 。MIT、LICENSE保持。\n\n入力と構成を先に整え、各頁の主張・正確なコピー・図の目的・根拠・ノートを記す。架空提案と実績を区別する。3案のstyle boardをbuilt-in imagegenで作り、選んだ方向の契約を記録する。原典は各段階のユーザー承認を求める。本作はユーザーの自律完遂指示により制作担当が判断する派生で、承認を取得したとは記録しない。\n\n1. input/data.jsonとqa/deck-blueprint.mdを入力にする。\n2. 紙白・深紺・雨灰、大きな明朝見出し、細線図版、暗い区切りを使う。\n3. built-in imagegenで一頁一画像。ローカル描画で代用しない。文字・ラベル・頁番号・未検証表記を確認する。\n4. 機械的な寸法調整のみ許可。完成PNGは1600×900。\n5. source/package_image_pptx_with_notes.mjsで画像とNOTES.mdを包装する。\n6. 頁数・画像数・ノート数を照合し、主な出力の表示と明白な欠けを確認する。\n\n本文・図は画像、ノートと画像差替えは編集可能。個別図形編集可能PPTXと称さない。\n')
prov={'repository':'demoolight/academic-image-ppt','upstream_commit':'2aac1a711ff658ab67d79a0e98cc54b5a0468751','license':'MIT','method':'built-in imagegen full-page images + original packaging script with speaker notes','editability':'raster_slides','preview_kind':'image-slides','fictional':True,'changes':['Japanese fictional spatial-design proposal rather than extracted thesis','Autonomous creator decisions replace individual user approval gates under explicit instruction','ja-JP package language and Studio Yebisu metadata','Generated 1672x941 images mechanically normalized to 1600x900','Four dark section dividers and experimental-plan page regenerated with imagegen'],'font_status':'Font styling requested only; actual font files not embedded or redistributed','visual_generation':'built-in imagegen; no API/CLI generation','approval_record':'User authorized upstream script execution and autonomous completion; no individual style or blueprint approval claimed'}
(out/'PROVENANCE.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2))
html='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>雨の図書室</title><style>body{margin:0;background:#14283d;color:#f5f2e9;font:16px sans-serif}header,nav{padding:14px 24px;display:flex;gap:12px;align-items:center;justify-content:center}a{color:inherit}main{max-width:1400px;margin:auto}img{display:block;width:100%;aspect-ratio:16/9}button{padding:10px 20px;border:0;border-radius:4px;cursor:pointer}p{padding:0 24px;text-align:center}</style><header>雨の図書室 · 架空の空間デザイン研究提案 <a href="deck.pptx">PPTX</a></header><main><img id="slide" src="image_pages/slide_01.png" alt="雨の図書室 第1頁"></main><nav><button id="prev">前へ</button><span id="counter">1 / 11</span><button id="next">次へ</button><button id="play">再生</button></nav><p>本文・図は画像です。PPTXではページ画像差替えと話者ノートを編集できます。</p><script>let n=1,t=null;function show(){document.querySelector('#slide').src='image_pages/slide_'+String(n).padStart(2,'0')+'.png';document.querySelector('#slide').alt='雨の図書室 第'+n+'頁';document.querySelector('#counter').textContent=n+' / 11'}document.querySelector('#prev').onclick=()=>{n=n===1?11:n-1;show()};document.querySelector('#next').onclick=()=>{n=n===11?1:n+1;show()};document.querySelector('#play').onclick=()=>{if(t){clearInterval(t);t=null;document.querySelector('#play').textContent='再生'}else{t=setInterval(()=>{n=n===11?1:n+1;show()},4500);document.querySelector('#play').textContent='停止'}};document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')document.querySelector('#next').click();if(e.key==='ArrowLeft')document.querySelector('#prev').click()});</script></html>'''
(out/'index.html').write_text(html)
cs=Image.new('RGB',(1440,1200),'#d9d9d9');draw=ImageDraw.Draw(cs)
for i,f in enumerate(sorted((out/'image_pages').glob('*.png'))):
 x=i%3*480;y=i//3*300;cs.paste(Image.open(f).resize((480,270)),(x,y));draw.text((x+10,y+278),f.name,fill='black')
cs.save(out/'qa/contact-sheet.png');shutil.copy(out/'qa/contact-sheet.png',run/'qa/contact-sheet.png')
print(out)
