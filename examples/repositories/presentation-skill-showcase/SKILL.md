---
name: presentation-skill-ja
description: 原典outline/role-contract/native PptxGenJSで日本語引継ぎ資料を作る。
---

# 日本語Presentation Skill

siril9/presentation-skill `efd899c5ddf866af2ce0001c4c9340af775d4d55` / MIT。原典の既定rendererは `scripts/build_deck_pptxgenjs.js`。汎用generatorに名前だけ貼らず、outline schema、render-plan、canonical role-contract、templateを実行する。

1. 原典present.py briefで内容・style/grammarを選び、そのreadability contractと候補をoutlineへ引き継ぐ。今回の候補はlavender-ops / operations-grid。入力はsourceであり、生成PPTXや画像を直接patchしない。
2. 原典schemaのnative flow_steps、timeline、table、comparisonを使う。図の内容を画像へ黙って代替しない。画像が必要な内容では原典asset pipelineを別途整える。
3. 短い日本語見出し・native図表・明暗・余白。表紙見出しは役割幅に収まる短い行で明示改行し、句読点だけの行を作らない。font_pairの局所adapterだけでShippori / BIZ UDPGothic / Manropeを役割別に対応し、差分を保存。字体は公式TTF/OFLのみ。
4. 可読性の不具合はsourceで直す。Operating Gridの上端barと見出しを離す、section補助枠にCYCLE/CONTROLなどの仮ラベルを残さず日本語の値とstage_labelsを入れる、文字色は実際の背景に対し4.5:1以上。template変更は対象関数内に限定し `source/legibility.diff` に残す。
5. 原典Node engineをPptxGenJS4.0.1/jszip3.10.1で実行。Python data/asset pipelineのdoctor不足はログへ記録し、整備済みと称しない。この作例は原典既定Nodeのnative要素だけで完成する。
6. PowerPoint16でPNG/PDFを描画。Application.Quitは禁止、自deckだけClose。全ページを目視し、独立reviewの指摘はoutline/template adapterへ戻して再生成する。原典finalizeなどの確認は実行後に結果を `QA.json` へ記録し、記録前に合格と書かない。
7. PPTX/PNG/PDF、JSON/原稿/依頼/再生成コード/未変更原本/局所差分/許諾/日本語ガイドを渡す。人名・会社・実績を捏造しない。

## quick_validate

`node runtime/scripts/build_deck_pptxgenjs.js --outline input/outline.json --output deck.pptx --style-preset lavender-ops` を実行し、PowerPointで6枚を描画して全ページを確認する。
