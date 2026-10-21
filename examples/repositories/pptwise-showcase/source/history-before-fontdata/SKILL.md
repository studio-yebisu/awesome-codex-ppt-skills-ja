---
name: pptwise-ja
description: 話の順序と頁の役割を先に決め、内容に合う部品とテーマ固有の図へ渡して、検査付きの編集可能資料へ組む。
---

# 構成と本文を分けて検査しながら作る

specで話の順序と頁の役割を固定し、steps/hub_spokeを用途で使い分ける。5頁は明示した架空の面積配分2案と概念画像をorigins recipeへ渡し、原典buildでsignature1件・errors0・warnings0を確認。

完成PPTXは[.pptwise/input/deck.pptx](.pptwise/input/deck.pptx)。root/deck.pptxは旧IR方式の履歴。現在出力を後加工・改名しない。

## 入力と出力

入力：読者・目的・発表形式、原稿と見出し、根拠になる数値、必要な画像とその出典。

出力：話の順序と頁の役割に合うテーマで組んだ編集可能PPTX、プレビュー、原典build/fitの検査記録。

## 手順

1. 読者・目的から話の順序とthemeを選び、deck.spec.jsonへ各頁のtype/kind/headingを固定する。
2. inspectで頁と部品の契約を読み、原稿の意味に合う部品をpagesへ書く。内容が合う場合にtheme固有のrecipeを使う。
3. 画像が必要ならasset-briefで実際の枠を確認し、許可された画像経路で取得・生成してassetsへ保存する。
4. 最大4頁ごとに原典buildを実行し、errors/warnings/fitを確認して入力を直す。完成後は全頁の読みやすさと根拠を確かめる。
## 範囲

- 原典Rally派生のmenuを保持し、5頁でorigins signatureを1件実行。提示5recipeの残り4件は未実施。
- 比率は比較用の架空の仮定で、実測・予測・確定設計ではない。画像は未建設拠点のAI概念図。グラフの面積を測った写真ではない。
- 生成は原典asset-brief後にbuilt-in image_genを直接使用。原典images generateのgenerator設定は実行しない。
- 原典の日本語書体allowlistだけをメモリー内で追加するadapterを明示。保存済み原典・レイアウト・出力PPTXの後加工なし。
- 図表はnative図形・文字で、データ連動Office chart/tableではない。新規npm ciと代替themeの再切替は未検証。
- 過去の個別ユーザー承認は未取得。現在の自律改修の委任により担当が実装した。

Node22.19+、Python、runtimeの固定依存を用意し、`python source/rebuild_pptwise.py`を実行する。--node/--cliで既存の実体を指定できる。fonts/の公式Zen Kaku Gothic NewとSpace Groteskを登録する。実PDFの字体も確認済み。元CLI・theme menu・描画器を保持する。原典MIT/commit65690bc705c1b5db41b5593015675945673da542を保持。現在版はCodexの修復で、新しいOpus制作ではない。独立再評価は別。配布再実行はsource/distribution-replay.json。
