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

## 単体の本文から使う

この本文は `skill-forks/agent-slides-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/mpuig/agent-slides/tree/820782a5fb8cb8f251d7c0750e4299c321cd068c

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `agent-slides-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: mpuig / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/mpuig/agent-slides/blob/820782a5fb8cb8f251d7c0750e4299c321cd068c/LICENSE
