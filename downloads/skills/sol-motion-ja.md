---
name: sol-motion-ja-entry
description: 動きで魅せるWebスライドを日本語で制作するときに使う。zarazhangrui/frontend-slidesの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 動きで魅せるWebスライド

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/zarazhangrui/frontend-slides/tree/9906a34d640d2111f724544cbc50f7f130569ae1

- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/SKILL.md
- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/html-template.md
- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/viewport-base.css
- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/animation-patterns.md
- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/LICENSE

Original viewport-base.css included verbatim; html-template.md stage and SlidePresentation architecture directly adapted; animation-patterns.md staggered editorial reveal. Bespoke Japanese composition authored with CSS/SVG, no common renderer.

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3
- モダンブラウザ
- 取得済み原典とフル日本語フォント

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 夜の図書館 — 仕事帰りに出会う、次の一冊

frontend-slides原典の固定1920×1080 stage・viewport-base.css全文・SlidePresentation構造を直接使い、日本語6ページ「夜の図書館 — 仕事帰りに出会う、次の一冊」を制作。架空の企画として明記。墨紺と蛍光ライム、大胆な和文タイポ、静かな余白、SVGの開いた本と都市の窓、段階的な入場アニメーション。問い→体験→選書→運営案→余韻の流れで、来館の動機を広告コピーにする。数値実績や実在施設を捏造しない。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: zarazhangrui / 原典条件: MIT

- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
