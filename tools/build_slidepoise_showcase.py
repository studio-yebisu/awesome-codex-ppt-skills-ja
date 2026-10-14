"""Portable rebuild of the image → OpenCV → contract → constructor SlidePoise case."""
from pathlib import Path
from datetime import datetime
import argparse,json,os,shutil,subprocess,sys,zipfile,hashlib

REPO='henryhyw/slidepoise';PIN='481a028486b528e65706c4e14aa9b74a5e340f12'
TITLE='クリックを減らす、予約の流れ。'
IDS=['reduce-steps','branch-and-information','targets-and-order']
TITLES=['迷う操作を、半分に。','分岐は、空席で決まる。','目標を決めて、順に直す。']
NOTES=['仮想の地域ワークショップ予約サイトの設計案です。現在案8操作から目標4操作へ。計測した改善実績ではありません。','空席による分岐と予約前の判断材料を一画面へ。会場名、120分、持ち物は画面例の架空設定です。','4操作・入力完了率90%・入力60秒は目標値です。情報統合、空席分岐、計測と見直しの順で実装する案です。']
PROMPT='SlidePoise原典の生成画像→semantic map→OpenCV計測→reconstruction contract→constructor scene→固有render-deckを実際に使い、日本語「クリックを減らす、予約の流れ。」を制作してください。仮想の地域ワークショップ予約サイトを題材に、8操作から4操作への設計目標、空席による分岐と予約前の情報、4操作/入力完了率90%/入力60秒の目標と実装順を3枚へまとめる。数値は仮想設定・目標で、実測としない。大きな和文、墨、コバルト/朱赤、意味のある図形関係。角丸カードの格子は避ける。自作AI生成画像だけを原典計測コードでnative文字/図形/freeform/connectorへ再構成し、汎用builderで代替しない。原典MITとOSS TTF/OFLを保持。原典に必要なbuildと代表完成物初回表示までを確認し、全詳細目視/構造監査/独立review/ZIP再実行を追加しない。PowerPoint Application.Quitは禁止、自分のdeckだけClose。'
ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='tools' else Path(__file__).resolve().parent
OUT=ROOT/'examples/repositories/slidepoise-showcase' if Path(__file__).parent.name=='tools' else ROOT
FORK=ROOT/'skill-forks/slidepoise-ja'

def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def jwrite(p,s):write(p,json.dumps(s,ensure_ascii=False,indent=2)+'\n')

def rebuild():
 if (OUT/'deck.pptx').exists():
  (OUT/'backups').mkdir(exist_ok=True);shutil.copy2(OUT/'deck.pptx',OUT/'backups'/('deck-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.pptx'))
 for sid in IDS:
  d=OUT/'slides'/sid/'work'
  # Generation request/prompt and original image are preserved; this rebuild replays reconstruction.
  subprocess.run([sys.executable,str(OUT/'runtime/slidepoise/scripts/normalize_generation_canvas.py'),'--input',str(d/'generated-original.png'),'--config',str(OUT/'work/resolved-config.json'),'--output',str(d/'accepted-slide.png')],check=True)
  subprocess.run([sys.executable,str(OUT/'runtime/slidepoise/scripts/slidepoise_runtime.py'),'reconstruct-slide','--image',str(d/'accepted-slide.png'),'--semantic-map',str(d/'semantic-map.json'),'--upstream-handoff',str(d/'reconstruction-handoff.json'),'--config',str(OUT/'work/reconstruction-config.json'),'--slide-id',sid,'--output-dir',str(d/'reconstruction')],check=True)
 env=os.environ.copy();env['PYTHON']=sys.executable
 subprocess.run([sys.executable,str(OUT/'runtime/slidepoise/scripts/slidepoise_runtime.py'),'render-deck','--manifest',str(OUT/'work/deck-scenes.json'),'--output',str(OUT/'deck.pptx')],env=env,check=True)

def viewer():
 html='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>クリックを減らす、予約の流れ。</title><style>body{margin:0;background:#112132;height:100vh;display:grid;place-items:center}img{width:min(100vw,177.777vh);aspect-ratio:16/9;object-fit:contain}nav{position:fixed;bottom:12px;right:16px;background:#246AF1;color:white;display:flex;align-items:center;gap:14px;padding:9px;font-family:sans-serif}button{font:inherit;background:none;border:1px solid white;color:white;padding:8px 15px}.embed nav{display:none}</style><img id="slide" src="render/slide-01.png" alt="迷う操作を、半分に。"><nav aria-label="スライド操作"><button id="prev">戻る</button><span id="counter">1 / 3</span><button id="next">進む</button></nav><script>const titles=TITLES;let n=0;function show(i){n=Math.max(0,Math.min(2,i));document.querySelector('#slide').src='render/slide-'+String(n+1).padStart(2,'0')+'.png';document.querySelector('#slide').alt=titles[n];document.querySelector('#counter').textContent=(n+1)+' / 3';if(parent!==window)parent.postMessage({type:'yebisu-page',index:n,total:3},location.origin)}document.querySelector('#prev').onclick=()=>show(n-1);document.querySelector('#next').onclick=()=>show(n+1);addEventListener('keydown',e=>{if(e.key==='ArrowRight')show(n+1);if(e.key==='ArrowLeft')show(n-1)});addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))show(e.data.index)});if(parent!==window)document.body.classList.add('embed');show(0)</script></html>'''
 write(OUT/'index.html',html.replace('const titles=TITLES;',f'const titles={json.dumps(TITLES,ensure_ascii=False)};'))

def finish():
 upstream=OUT/'upstream';shutil.copy2(upstream/'LICENSE',OUT/'LICENSE')
 write(OUT/'PROMPT.md',PROMPT+'\n');write(OUT/'input/BRIEF.md','# 制作依頼\n\n'+PROMPT+'\n')
 write(OUT/'input/SOURCE.md','''# クリックを減らす、予約の流れ。

仮想の地域ワークショップ予約サイトの設計案。実在サービスの改善実績ではありません。

- 現在案: 一覧、詳細、日程、空席、会員登録、入力、確認、完了の8操作。
- 改善目標: 内容と空席、日程、入力、完了の4操作。
- 分岐: 開催日を選び、空席があれば予約入力、満席なら次の日程。
- 予約前の情報: 会場、所要時間、持ち物。画面例の「みどり市民センター」「120分」「筆記用具・飲み物」は生成画像から採用した架空の設定です。
- 目標: 完了まで4操作、入力完了率90%、入力時間60秒。現時点の実測値ではありません。
- 実装順: 情報をまとめる、空席分岐を実装、計測して見直す。

図の出所: 原典prepare_generationが出力した3つの拘束済みrequestをbuiltin image_genへ渡した自作生成画像。画像とそのsemantic map、OpenCV計測、contract、constructor、native PPTXを一式保全。
''')
 refs=[{'path':f,'sha256':hashlib.sha256((upstream/f).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{PIN}/{f}'} for f in ['slidepoise/SKILL.md','slidepoise/scripts/prepare_generation.py','slidepoise/scripts/normalize_generation_canvas.py','slidepoise/scripts/slidepoise_runtime.py','slidepoise/runtime/scripts/measure_visual_scene.py','slidepoise/runtime/src/slidepoise/reconstruction/contract.py','slidepoise/runtime/src/slidepoise/reconstruction/scene.py','slidepoise/runtime/js/scene_to_pptx.mjs','LICENSE']]
 source={'repository':REPO,'commit':PIN,'license':'MIT','author':'SlidePoise contributors (henryhyw/slidepoise)','official':False,'source_refs':refs,'method':'Original prepare_generation compiled exact bound requests → builtin image_gen → original normalize_generation_canvas → host-authored semantic map → original OpenCV measurement → original reconstruction contract → original constructor scene → original slidepoise_runtime render-deck / scene_to_pptx renderer and native postprocess.','generation_tool':'image_gen__imagegen','image_count':3,'measure_engine':'OpenCV 4.12.0','constructor_objects':[34,28,24],'editability':'native_elements','editable_features':['text','shapes','connectors'],'native_scope':'Native Japanese/Latin text, rectangles/roundRect/ellipses, editable freeform chevrons and diamond, native connectors; no full-slide screenshot image objects.','not_exercised':['External library reference retrieval, Console/profile installation, SAM, image editing, third-party photographs/logos, independent review, all-page detailed visual QA, ZIP re-execution.'],'upstream_preserved':True,'modifications':['Local runtime text_fit.py only: map requested Dela/BIZ/Manrope families to the bundled original OSS TTF metrics on Windows rather than falling back to Arial.','Reconstruction config explicitly uses agent_observed font-family policy so Manrope is preserved; original generation config/request remain unchanged.','Headline target-size/weight adjusted in semantic map after the first PowerPoint display wrapped the Japanese final period. The second native render shows the full sentence.','Local export_case.ps1 omits Application.Quit and closes only its openedDeck.','Three substantive pages replace the initial six-page proposal so the original image/OpenCV/constructor path is fully exercised.','Scoped source acquisition excludes media/examples/library-set assets; each pinned source blob matches the audited Git tree.'],'visual_limitations':['Native font shaping and flat fills differ from generated text ink and paper shading; pixel-perfect fidelity is not claimed.','Third final page was generated/opened/exported but not detailed visually reviewed.'],'fonts':{'source_commit':'66928797f271fed5ee428544e7229685e2d90127','families':['Dela Gothic One','BIZ UDPGothic','Manrope'],'license':'OFL-1.1','full_original_TTF_and_OFL_included':True,'PPTX_font_embedding':False},'artifact_tool_used':False}
 jwrite(OUT/'SOURCE.json',source);jwrite(OUT/'PROVENANCE.json',source)
 deps={'python':[{'package':'opencv-python','version':'4.12.0.88','license':'Apache-2.0 / wheel includes third-party notices'},{'package':'numpy','version':'2.2.6','license':'BSD-3-Clause'},{'package':'Pillow','version':'12.3.0','license':'MIT-CMU'},{'package':'python-pptx','version':'1.0.2','license':'MIT'}],'node':[{'package':'pptxgenjs','version':'4.0.1','license':'MIT'},{'package':'jszip','version':'3.10.1','license':'MIT OR GPL-3.0-or-later'}],'bundled_packages':False,'PowerPoint':'Requires an installed licensed Windows PowerPoint; not redistributed.'}
 jwrite(OUT/'DEPENDENCIES.json',deps)
 write(OUT/'README.md','''# クリックを減らす、予約の流れ。

仮想の地域ワークショップ予約サイト、3枚。8操作から4操作への設計目標、空席の分岐と一画面の情報、目標指標と実装順を説明します。4操作・90%・60秒は目標、120分と会場名は画面例の架空設定で、実測ではありません。

## 原典方式

SlidePoise固定版のprepare_generationでconfig/intent/resourcesを拘束したrequestを生成し、そのpromptを改変せずbuiltin image_genへ渡しました。生成した3画像を目視して選び、原典normalizerで1672×941から1600×900へ余白を除かずcontain-fit。semantic-mapをAgentが画像から作成し、元reconstruct-slideでOpenCV計測→contract→constructorまで実行。元render-deckとscene_to_pptx、native postprocessorでPPTX化しました。生成画像工程やcompiler lineageをscene直書きで省略していません。

文字、基本図形、chevron/diamondのfreeform、native connectorは編集可能です。全頁画像をPPTXに貼ったものではありません。画像の紙の微妙な陰影や文字の見え方まで同一にする保証はありません。Dela見出し、BIZ本文、Manrope英数字をnative font指定し、実TTF/OFLを同梱。PPTXはフォント未埋込なので別端末へは手動導入してください。

## 再生成

展開先でPython3.10+に `pip install opencv-python==4.12.0.88 numpy==2.2.6 Pillow==12.3.0 python-pptx==1.0.2`。Nodeに `npm install pptxgenjs@4.0.1 jszip@3.10.1`、NODE_PATHへnode_modulesを設定してください。`python rebuild.py` で保全済み生成画像→原典OpenCV/contract/constructor→render-deckを再実行。既存PPTXはbackups/へコピーします。Windowsでは `powershell -NoProfile -File export_case.ps1 -PresentationPath deck.pptx -OutputDirectory render` でPNG/PDF。Consoleやglobal profileのインストールは不要です。

別題材にする場合はPROMPT.mdとinput/SOURCE.mdを置き換え、各slides/<id>/workのslide-intent/resource-selectionを更新して原典prepare_generation.pyでrequestを再compileし、生成画像とsemantic mapを新たに作成してください。元画像を使い回して別内容を主張しないでください。個別generation-brief.mdが実際にbuiltin toolへ渡したpromptです。保全したrequestの絶対path bindingsは当時の実行証跡で、別端末の画像再生成では入力を現地でcompileし直します。

## 条件と差分

原作者henryhyw/slidepoise、固定pinはSOURCE.json。MIT原文はLICENSE、未変更code/docs/schemaはupstream、使用版はruntime。third-party library media/PwC資料/例の完成物は含めません。取得sourceのGit blobは固定treeに一致。本作例は非公式です。

runtime差分はWindowsのfitterに同梱OSS TTFのfamily対応表を足した箇所だけ。再構成configに観察字体を許すpolicyを指定し、最初のPowerPoint表示で句点が次行へ回った見出しtarget size/weightだけsemantic mapで修正。局所exportはApplication.Quitを呼ばず、自分のdeckだけCloseします。依存packageのversion/条件はDEPENDENCIES.json、package本体はZIPへ同梱していません。

確認は実生成、元OpenCV/contract/constructor/rendererの成功、計測overlay、代表完成物の初回表示とその明白な句点修正までです。全ページ詳細目視、構造監査、独立レビュー、ZIP再実行は未実施です。外部library retrieval・Console・SAMは使っていません。
''')
 jwrite(OUT/'QA.json',{'status':'light_check_complete','checks':['Original compiled generation requests executed via builtin image_gen (three targets).','Original normalizer + OpenCV measurement + contract + constructor + render-deck succeeded (34/28/24 objects).','Generated targets and OpenCV overlays inspected for ownership.','PowerPoint16 opened and exported three PNG/PDF; primary first display revealed headline punctuation wrapping, corrected semantic size/weight and reconstructed/rendered again.','First and branch native representative displays observed after correction.'],'all_pages_detailed_visual_review':False,'structural_audit':False,'independent_review':False,'zip_reexecution':False,'limits':['Final third page was opened/exported but not detailed visually reviewed.','Native reconstruction does not claim identical generated font ink or paper shading.','Metrics and wireframe details are fictional assumptions/targets.']})
 FORK.mkdir(parents=True,exist_ok=True);shutil.copytree(upstream,FORK/'upstream',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));shutil.copy2(OUT/'LICENSE',FORK/'LICENSE');jwrite(FORK/'SOURCE.json',source)
 write(FORK/'SKILL.md','''---
name: slidepoise-ja
description: SlidePoiseの生成画像→OpenCV→contract→constructor→固有rendererを保ち、日本語のnative編集可能PPTXを作る。
---

# SlidePoise 日本語版（非公式）

1. 題材・主張・関係・出所・仮定をintentへ書く。数字が目標なら目標と明記。Native diagramが説明する関係を決め、反復card gridへ押し込まない。
2. 同梱upstream/slidepoise/SKILL.mdと必要referencesを読む。画像工程を省かない。元prepare_generation.pyでconfig/intent/resourcesからrequestをcompileし、exact promptとreferenceをbuiltin画像toolへ渡す。能力がなければ依存工程だけ止めて具体条件を知らせる。
3. 得た画像を見て採用し、元normalizerでcanvasを整える。Agentがsemantic-mapに文字・論理的allocation・図形・connector owner・target字体を記す。座標を汎用builderへ写す代替は禁止。
4. 元reconstruct-slideでOpenCV計測→contract→constructorをcompile。overlayでownershipを読む。元render-deckで順序通りnative PPTX化し、画像を全頁背景へ貼って編集可能と称さない。
5. 必要な原典buildと代表完成物の初回表示を確認。本作例はユーザーの軽い確認指定で全詳細目視/独立review/構造監査/ZIP再実行を省略。明白な句点欠けをsemantic targetへ戻して修正した。

日本語の見出し/本文/英数字を別familyへ。実TTF/OFLだけ添付する。local Windows fitterは同梱OSS familyを明示解決する差分のみ。PowerPoint COMはApplication.Quitを使わず自分のdeckをClose。

example/rebuild.pyが保全画像からの原典再構成入口、example/PROMPT.mdは別題材への依頼文。例では3枚の生成画像・semantic map・OpenCV計測・contract・constructor・PPTXが揃う。Original global Console/profile install、外部library retrieval、SAMは未実行。

原典 https://github.com/henryhyw/slidepoise 、MIT原文とpinはLICENSE/SOURCE.json。非公式改変。Fontは各OFL、PPTXフォント未埋込時は他端末へ導入する。任意reviewを省いたことと原典build成功を区別する。
''')
 write(FORK/'README.md','# SlidePoise日本語キット\n\n原典MITとOFLを保持。example/の入力→AI生成画像→OpenCV→contract→constructor→native PPTXが本作例。スキルと元codeを添付、依存packagesは未同梱。\n')
 base='examples/repositories/slidepoise-showcase/'
 case={'id':'slidepoise-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'slidepoise-ja','page_count':3,'format':'pptx','preview_kind':'powerpoint-render','preview_canvas':{'width':1600,'height':900},'style':'墨 × コバルト × 朱赤 / 生成画像をnative図解へ','use_case':'仮想予約サイトの改善案','preview':base+'index.html','cover':base+'render/slide-01.png','interior':base+'render/slide-02.png','pages':[base+f'render/slide-{n:02}.png' for n in range(1,4)],'artifact_download':base+'deck.pptx','source_download':'downloads/slidepoise-example-ja.zip','fork_download':'downloads/slidepoise-ja.zip','pptx_download':base+'deck.pptx','pdf_download':base+'render/deck.pdf','input':base+'input/SOURCE.md','input_data':base+'input/case-data.json','prompt':base+'PROMPT.md','prompt_text':PROMPT,'provenance':base+'PROVENANCE.json','qa':base+'QA.json','guide':base+'README.md','titles':TITLES,'notes':NOTES,'sample_notice':'仮想サイトの設計案。操作数/完了率/入力時間は目標値、実測ではありません。会場名と120分も画面例の設定。','method':source['method'],'navigation':'native-runtime-bridge','editability':'native_elements','editable_features':['text','shapes','connectors'],'status':'light_check_complete','execution_status':'light_check_complete','preview_notice':'原典AI画像→OpenCV→contract→constructorでnative文字/図形/connectorへ再構成。字形や紙の陰影の完全一致は未保証。','representative_previews':[base+'render/slide-01.png',base+'render/slide-02.png'],'preview_image_notice':'3枚をPowerPoint export。代表完成物の初回表示と句点修正まで確認、全詳細目視なし。'}
 guide={'repository':REPO,'production_status':'generated','execution_status':'light_check_complete','execution_type':'original_image_opencv_contract_constructor_native_renderer','case_ids':[case['id']],'summary_ja':'原典の画像生成→OpenCV→contract→constructor→固有rendererを3枚で完走。予約サイトの仮想改善案をnative文字/図形/connectorへ。','requirements':['Python3.10+ / OpenCV / numpy / Pillow / python-pptx','Node / pptxgenjs4.0.1 / jszip3.10.1','画像再生成のみbuiltin image tool等','PowerPoint16（PNG/PDF表示）'],'steps':['元prepare_generationでprompt/requestをcompile','builtin toolで画像生成しAgentがsemantic mapを作る','元reconstruct-slideでOpenCV/contract/constructor','元render-deckでnative PPTXと代表初回表示'],'commands':['python rebuild.py','powershell -NoProfile -File export_case.ps1 -PresentationPath deck.pptx -OutputDirectory render'],'source_refs':refs,'upstream_commit':PIN,'license':'MIT','license_notice_ja':'原典MIT、書体OFLを保持。外部library media・PwC素材・大学logoは含みません。','caveats':source['visual_limitations'],'skill':'skill-forks/slidepoise-ja/SKILL.md','guide':case['guide']}
 jwrite(ROOT/'data/sol-slidepoise-repository-examples.json',[case]);jwrite(ROOT/'data/sol-slidepoise-repository-guides.json',[guide]);viewer()
 shutil.copy2(Path(__file__),OUT/'rebuild.py');write(OUT/'.gitignore','**/__pycache__/\n*.pyc\nbackups/\n')
 for sid in IDS:
  d=OUT/'slides'/sid/'work';jwrite(d/'measurement-review.json',{'stage':'host source-ownership observation','inspected_file':'reconstruction/measurement/debug_overlay.png','observation':'The overlay assigns distinct text and diagram owners within the selected target. Branch ports/timeline direction come from host semantic ownership, not automatic aesthetic selection.','limitations':'Source mapping inspection only; no independent output QA.'})
 package()

def package():
 shutil.copytree(OUT,FORK/'example',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc','backups'))
 for folder,name in [(OUT,'slidepoise-example-ja'),(FORK,'slidepoise-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.parts)&{'__pycache__','backups'} and p.suffix!='.pyc':z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--finish',action='store_true');parser.add_argument('--package-only',action='store_true');args=parser.parse_args()
 if args.finish:finish()
 elif args.package_only:package()
 else:rebuild()
