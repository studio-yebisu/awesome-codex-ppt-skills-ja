---
name: agent-slides-ja
description: 既存PPTXの書式・配置を抽出し、planとnative編集操作からPowerPointを生成・検査する。
---

## このスキルでできること

既存PPTXから文字の位置・字体・色を取り出し、その書式を保って本文と編集できる図を入れる。

- 困っている状況: 会社のテンプレートを渡しても、既存の配置・書式ルールが制作に引き継がれない。
- 必要な入力: 書式を引き継ぐPPTXテンプレート、その抽出結果、原稿・発表条件・作図指示。
- 受け取るもの: テンプレートの書式を引き継ぐ編集可能PPTXと、頁の計画・編集操作・検査の記録。
- 必要環境: Python3.12+・同梱の元agent-slides runtimeとその依存 / PowerPoint等のPPTX描画環境 / 同梱Zen Kaku Gothic New・Manrope/OFL
- 作例で試した範囲: 紺/橙の自作templateを元CLIで抽出。見出し52pt・本文23pt・白・位置を継承し、仮の行程と関係図をnative部品で追加した。元qaはok:true、入力2頁と完成1頁を目視した。
- 制約: 入力はこの作例用に作ったtemplate。実在企業の資料を試した結果ではない。 / 1枚指定と大見出しを優先。元の自動構造頁・24pt標準・汎用split-panel移動規則とは異なる範囲を記録。 / 背景・橙帯・固定ラベルはlayoutに属し、PowerPointのスライドマスターで編集する。


# 1枚で企画を伝える

1. 読者、話し合う目的、核となる提案、架空条件を決める。原典slides-buildとstorytelling/layout-patterns/operationsを読む。
2. Python3.12+で `pip install ./runtime`。原典extract→preflight契約を保持する。input/projectに完成例の抽出契約とbase_template.pptxを同梱。
3. input/slides.jsonのplanとopsを編集。巨大な提案文、短い約束、仮の行程、 unorderedな関係図を分ける。数値は実績と計画を区別。
4. `python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact`。
5. `python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --dry-run --compact`、続けて同コマンドのdry-runを`--output deck-rebuilt.pptx`へ置換。
6. 原典必須gate `python -m slides_cli.cli qa deck-rebuilt.pptx --profile input/project/design-profile.json --slides-json @input/slides.json --out qa.json --compact` を実行しok:trueを確認。問題を直して再実行する。
7. 指定字体を導入してPowerPointで全頁PNG/PDFを描画し、文字・図・配置・継承書式を目視する。本例は1頁で、左の仮行程と右の関係図を区別する。作者検査と指定済み独立評価は別記録とする。

原典MIT、commit820782a5fb8cb8f251d7c0750e4299c321cd068c。1枚指定に合わせ自動構造ページ追加を省いた明示派生。SKILL本文だけでは生成できず、原典runtime・ops・template契約が必要。原作者の公式日本語版ではありません。

## 単体の本文から使う

この本文は `skill-forks/agent-slides-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/mpuig/agent-slides/tree/820782a5fb8cb8f251d7c0750e4299c321cd068c

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `agent-slides-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: mpuig / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/mpuig/agent-slides/blob/820782a5fb8cb8f251d7c0750e4299c321cd068c/LICENSE
