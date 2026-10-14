---
name: hand-drawn-ja-entry
description: 手描きイラストの章扉を日本語で制作するときに使う。ABYR1206/claude-skill-hand-drawn-slidesの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 手描きイラストの章扉

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/ABYR1206/claude-skill-hand-drawn-slides/tree/322a265344e73cd54f77f3f07b6a9f15bb7d2d99

- https://github.com/ABYR1206/claude-skill-hand-drawn-slides/blob/322a265344e73cd54f77f3f07b6a9f15bb7d2d99/hand-drawn-chapter-slides/SKILL.md
- https://github.com/ABYR1206/claude-skill-hand-drawn-slides/blob/322a265344e73cd54f77f3f07b6a9f15bb7d2d99/hand-drawn-chapter-slides/scripts/illustrations.md
- https://github.com/ABYR1206/claude-skill-hand-drawn-slides/blob/322a265344e73cd54f77f3f07b6a9f15bb7d2d99/LICENSE

Original instruction-driven PptxGenJS + sharp template and original SVG library; author implementation, Japanese font/color adaptation.

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Node.js
- PptxGenJS
- sharp
- 任意:指定TTFの手動導入

- 表紙と4章の章扉サンプル。全文の業務資料ではない。
- 見出し・ノートはPPTXで編集できる。手描きイラストは原典SVGからの画像で、原SVGはキットに収録。

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: チームのアイデアを、育てる。

ABYR1206のhand-drawn-chapter-slides原典SKILL、PptxGenJSコード雛形、illustrations.mdの原SVGを使い、日本語の章扉5枚「チームのアイデアを、育てる。」を制作。表紙＋見つける／話してみる／試してみる／振り返る。フル業務資料ではなく章扉の作例。紙の暖色と鮮やかな朱赤、Zen Maru Gothic・Dela Gothic One・Manropeで、短い大見出しと余白、黒い手描き線とオフ白の象徴図形。背景、原SVG、左下章題、右下ページという原典の骨格を保つ。指示による和文書体/朱赤の変更を記録。架空のチームワークショップ導入案、実績・効果の主張なし。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: ABYR1206 / 原典条件: MIT

- https://github.com/ABYR1206/claude-skill-hand-drawn-slides/blob/322a265344e73cd54f77f3f07b6a9f15bb7d2d99/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
