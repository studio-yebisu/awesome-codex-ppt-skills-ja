# クリックを減らす、予約の流れ。

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
