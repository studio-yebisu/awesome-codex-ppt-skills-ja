---
name: native-math-ja
description: 原典Sandwich themeとOMML数式注入で編集可能な日本語数式PowerPointを作る。
---

# 日本語のnative数式PowerPoint

Noi1r/powerpoint-skill `a39cd8cfba332741a96d52bebd2bb378b638364e` / MIT。原典theme/helpersとinject_ommlを実際に実行する。

1. 原典themes.mdのJavaScript helperを抽出し、Sandwichと日本語字体を設定。図形・表・グラフをPptxGenJSで編集可能に作る。
2. formulas.jsonは `render:omml`。原典render_latexでmanifestを作り、addMathTextでplaceholderを配置。
3. 原典inject_omml.pyを実行。Pandoc→DOCX→OMML注入。失敗と残存placeholderは必ず修正し、画像数式へ黙って替えない。
4. Office字体/XSLを抽出配布せず、公式TTF/OFLを同梱。補助XSLはこの原典経路では不要。OMMLはPowerPointで直接編集できる。
5. PNG/PDFはPowerPoint実描画。共有ApplicationをQuitせず、自分のdeckだけCloseする。LibreOfficeではOMML欠けがある。
6. 今回はユーザー指定の内部判断・軽い確認を優先。必須interview/outline承認待ち、5並列review、References/ThankYou/Backup固定追加を適用せず、5枚教材を守る。計画は入力へ記録。全ページ詳細監査・独立review・ZIP再実行は不要。
7. 原典実行、数式注入成功、placeholder残存なし、代表初回表示を記録。.pptx/.png/.pdf、source/license、編集条件とガイドを渡す。

## quick_validate

`python source/build.py --node C:/path/to/node.exe --pandoc C:/path/to/pandoc.exe` の成功後、PowerPointで代表完成物を一度開く。

## 単体の本文から使う

この本文は `skill-forks/native-math-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Noi1r/powerpoint-skill/tree/a39cd8cfba332741a96d52bebd2bb378b638364e

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `native-math-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: Noi1r / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Noi1r/powerpoint-skill/blob/a39cd8cfba332741a96d52bebd2bb378b638364e/LICENSE
