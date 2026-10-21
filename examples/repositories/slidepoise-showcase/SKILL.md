---
name: slidepoise-ja
description: 原稿の意図を画像で設計し、計測と意味の割当を経て編集可能なPowerPointへ再構築する。
---

# 画像で設計し、文字・図形を編集できるPowerPointへ

原典 henryhyw/slidepoise / 481a028486b528e65706c4e14aa9b74a5e340f12 / MIT。非公式の日本語案内。upstream/slidepoise/SKILL.mdと必要referencesを読む。

1. 原典CLIのdoctor・profile showで環境と選択Profile/Library Setsを確認し、resolve_config.pyで今回の上書きを解決する。目的・読み手・根拠・必要内容を確定し、work/deck-outline.jsonに安定した頁IDと順序・役割を書く。
2. 各頁の意図に合う参照候補を検索し、実物を見て選ぶ。Profileと共通frameを決める。画像の生成領域はframeを除く本文領域で、常に16:9とは限らない。
3. intentと資源からprepare_generationでrequestをcompileし、その正確なpromptと参照を画像ツールへ渡す。手動生成を選んだ場合は同じrequestを書き出して画像を取り込む。採用画像と原稿を実際に見比べる。
4. semantic mapと独立したcontent obligationsを記す。文字領域、図形、接続元/先、画像の役割はAgentが判断する。原典reconstruct-slideでOpenCV計測→overlay確認→contract→constructor sceneへ進む。コードは美しさや意味を判定しない。
5. 原典render-deckで頁順に組み立てる。全頁の実描画を開き、内容の欠落、文字のかたまり、光学的位置、接続方向、頁間の統一を生成画像と同じ縮尺で比べる。複数頁では独立した最終レビューを行う。問題を元の意図・mapへ戻して直し、再描画する。
6. 編集可能PPTX、プレビュー、使用素材・字体・差分と未解決事項を渡す。汎用PptxGenJS/python-pptx/HTML/SVGの独自builderを代替にしない。画像背景だけを編集可能と称さない。

## この作例で試したこと

仮想予約サイトの3頁。原典compile済みrequestで生成した画像→normalizer→host semantic map→OpenCV→contract→constructor→原典rendererを全頁で実行。native要素は34/28/21個。数値は目標で実測ではない。現在の全3頁をPowerPointで描画して見比べ、1頁の切り欠きと文字の接触、3頁の数字と単位の離れを修復した。数字と単位は同じnative文字領域にまとめ、元のcontent obligationsを保持した。

原画像と比べやすい平面の構成を保持しているが、書体のinkや紙の陰影の完全一致は保証しない。字体解決と文字領域の補正はsource/text-layout-repair.jsonに記録。原画像の再生成はしていない。独立した最終再評価、外部Library検索・Console/global Profile導入、SAM、実在ロゴ/写真の保持は未実施。

## 再現

Python3.10+、OpenCV/numpy/Pillow/python-pptx、Nodeとpptxgenjs4.0.1/jszip3.10.1。作り直す場合は画像生成ツールまたは手動取り込み。Windows PowerPoint描画にはMicrosoft PowerPointと同梱Dela Gothic One・BIZ UDPGothic・Manropeの導入が必要。各OFLを保持する。

作例ZIPでは `python rebuild.py` が保存画像から原典再構築を再実行する。例の内容とsemantic mapを再現する処理で、任意の題材を自動企画するアプリではない。`export_case.ps1`は自分が開いたdeckだけ閉じる。全頁の実表示と比較を行う。
