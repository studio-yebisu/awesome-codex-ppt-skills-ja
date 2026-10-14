---
name: react-slide-deck-ja-entry
description: Reactで育てるスライドを日本語で制作するときに使う。code-on-sunday/slide-deck-generatorの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# Reactで育てるスライド

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/code-on-sunday/slide-deck-generator/tree/a6369f31b0cc4dd5830796455326777a8fe4c7c6



原典React App / SlideLayout / useSlideScale / Framer Motion variants / Vite build

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python3.13 / fontTools / Brotli
- Node.js24とnpm
- HTTPの配信環境



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: FAQを育てる4週間

原典slide-deckのReact/Vite工程とen-context-engineeringのApp・SlideLayout・useSlideScale・animation variantsを使い、日本語でFAQ整備の4週間プランを5枚作る。架空の社内チームの計画で、10問は目標。Bold Signalの配色を保ち、Noto Sans JPで日本語化。問題→問い→概念→例→持ち帰りの順に、段階的な図解と週別タブを入れる。外部AI APIや画像生成は不要。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: code-on-sunday / 原典条件: MIT

- https://github.com/code-on-sunday/slide-deck-generator/blob/a6369f31b0cc4dd5830796455326777a8fe4c7c6/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
