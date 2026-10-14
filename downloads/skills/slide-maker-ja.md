---
name: slide-maker-ja-entry
description: 図表を組めるPPTXを日本語で制作するときに使う。addsumtech/slides_makerの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 図表を組めるPPTX

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/addsumtech/slides_maker/tree/3767cc346d63ef1646082c87f15fbf0be582b152

- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/LICENSE
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/README.md
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/SKILL.md
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/agents/critic.md
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/references/critic-panel.md
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/references/design-principles.md
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/references/handoff-checklist.md
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/references/review-rubrics.md

原典のdeckkitで編集可能な図を組み、native_chartで探索回数をグラフ化。全ページをPowerPoint本体で描画しました。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.10+ / python-pptx, pymupdf, Pillow, matplotlib, numpy
- Yu Gothic / Consolas
- PowerPoint（今回の描画QA）



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 並べておくと、探し方が変わる

addsumtech/slides_maker の原典deckkit/native_chartを実行し、日本語の初学者向け教材「並べておくと、探し方が変わる」を5枚で作る。Pythonで昇順1〜15の全目的値を線形探索・二分探索し、実行トレースを入力として図とnative chartへ接続する。13は13回対4回、全15通りの最大は15回対4回。秒数や整列コストを測定済みと表現しない。PowerPoint描画を全頁確認し独立criticを行う。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: addsumtech / 原典条件: MIT

- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/LICENSE
- https://github.com/addsumtech/slides_maker/blob/3767cc346d63ef1646082c87f15fbf0be582b152/skills/slide-maker/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
