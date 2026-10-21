---
name: agent-slides-ja
description: 既存PPTXの書式・配置を抽出し、planとnative編集操作からPowerPointを生成・検査する。
---

# 1枚で企画を伝える

1. 読者、話し合う目的、核となる提案、架空条件を決める。原典slides-buildとstorytelling/layout-patterns/operationsを読む。
2. Python3.12+で `pip install ./runtime`。原典extract→preflight契約を保持する。input/projectに完成例の抽出契約とbase_template.pptxを同梱。
3. input/slides.jsonのplanとopsを編集。巨大な提案文、短い約束、仮の行程、 unorderedな関係図を分ける。数値は実績と計画を区別。
4. `python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact`。
5. `python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --dry-run --compact`、続けて同コマンドのdry-runを`--output deck-rebuilt.pptx`へ置換。
6. 原典必須gate `python -m slides_cli.cli qa deck-rebuilt.pptx --profile input/project/design-profile.json --slides-json @input/slides.json --out qa.json --compact` を実行しok:trueを確認。問題を直して再実行する。
7. 指定字体を導入してPowerPointで全頁PNG/PDFを描画し、文字・図・配置・継承書式を目視する。本例は1頁で、左の仮行程と右の関係図を区別する。作者検査と指定済み独立評価は別記録とする。

原典MIT、commit820782a5fb8cb8f251d7c0750e4299c321cd068c。1枚指定に合わせ自動構造ページ追加を省いた明示派生。SKILL本文だけでは生成できず、原典runtime・ops・template契約が必要。原作者の公式日本語版ではありません。
