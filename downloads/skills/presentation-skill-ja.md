---
name: presentation-skill-ja
description: 原典outline/role-contract/native PptxGenJSで日本語引継ぎ資料を作る。
---

## このスキルでできること

原稿の関係・順序・比較を別の図解や表で表し、元の生成器と検査で編集できるPPTXを作る。

- 困っている状況: 情報をすべて箇条書きにすると、順序・比較・担当・期限の関係が読み取れない。
- 必要な入力: 資料の目的・読者・元の原稿やデータ。既存資料を編集する場合は元PPTX。
- 受け取るもの: 文字・図解・表などを編集できるPPTXと、構成・生成ソース・検査結果。
- 必要環境: Node.js・原典pinned PptxGenJS4.0.1/jszip3.10.1 / Pythonと原典finalizer、描画用LibreOffice/Poppler / PowerPoint16と同梱Shippori/BIZ/Manrope/OFL / 科学データ解析を足す場合は原典pinned Python科学依存一式を別途整備
- 作例で試した範囲: 6頁で必要情報の関係、作業順、記入用表、着手条件を別のnative構造にした。元finalize再実行は全検査0件、全6頁を目視。表の列名再掲と斜体もsourceで修正し、制作ZIPの実再生成が一致した。
- 制約: 架空の引継ぎ教材。担当・期限・状態は説明用の設定。 / 原典Node routeとnative要素のfinalizeを実行。Python科学データ依存一式の準備完了ではない。 / 日本語字体・数値字体・見出し位置・dark文字色・表metadataは局所adapter。元との差分と担当範囲を記録。 / 元の自動検査通過と人の視覚確認・独立再評価を区別する。


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

表のmetadataは表本体の列名を繰り返さず件数を示し、日本語captionを合成斜体にしません。今回の追加修正はCodexによるsource/table-legibility.diff。元builder・finalizeを再実行し、全6頁を実描画・目視しました。独立再評価は未了です。

## 単体の本文から使う

この本文は `skill-forks/presentation-skill-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/siril9/presentation-skill/tree/efd899c5ddf866af2ce0001c4c9340af775d4d55

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `presentation-skill-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: siril9 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/siril9/presentation-skill/blob/efd899c5ddf866af2ce0001c4c9340af775d4d55/LICENSE
- https://github.com/siril9/presentation-skill/blob/efd899c5ddf866af2ce0001c4c9340af775d4d55/plugins/presentation-skill/skills/presentation-skill/LICENSE
