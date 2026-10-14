---
name: agent-slides-ja
description: 原典agent-slidesのtemplate契約とplan+ops CLIで、巨大和文・関係図・行程を持つnative1枚企画書を作る。
---

# 1枚で企画を伝える

1. 読者、話し合う目的、核となる提案、架空条件を決める。原典slides-buildとstorytelling/layout-patterns/operationsを読む。
2. Python3.12+で `pip install ./runtime`。原典extract→preflight契約を保持する。input/projectに完成例の抽出契約とbase_template.pptxを同梱。
3. input/slides.jsonのplanとopsを編集。巨大な提案文、短い約束、仮の行程、 unorderedな関係図を分ける。数値は実績と計画を区別。
4. `python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact`。
5. `python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --dry-run --compact`、続けて同コマンドのdry-runを`--output deck-rebuilt.pptx`へ置換。
6. Zen Kaku Gothic NewとManropeをfonts/から導入。PowerPointで主出力を確認し、source/render_powerpoint.ps1でPNG/PDFへ書き出す。

原典MIT、commit820782a5fb8cb8f251d7c0750e4299c321cd068c。1枚指定に合わせ自動構造ページ追加を省いた明示派生。SKILL本文だけでは生成できず、原典runtime・ops・template契約が必要。原作者の公式日本語版ではありません。
