---
name: html-editable-ja-entry
description: HTMLから文字と図形のPPTXへを日本語で制作するときに使う。Hasasasa/html-to-editable-pptxの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# HTMLから文字と図形のPPTXへ

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/Hasasasa/html-to-editable-pptx/tree/17c1dbb76e958543dc2741a7d50ca374354f33b7

- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/SKILL.md
- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/convert.py
- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/scripts/measure.py
- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/scripts/assemble.py
- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/scripts/embed_fonts.py
- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/LICENSE

Original convert.py CLI → preflight → original Playwright measure → python-pptx assemble; original --no-embed-fonts compatibility option. Wrapper registers local Japanese font families and maps seeded Noto SC aliases to JP fonts; no converter replacement.

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3
- 原典requirements依存
- Playwright Chromium

- PowerPointで開ける配布版は、原典の --no-embed-fonts を使用。日本語書体は公式TTFを端末へ導入する。
- 原典FONT_PLANへの日本語フォント登録アダプターを使用。変換本体は原典の measure/assemble を維持。

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 小さな店の、ひとつの旗。 — 焙煎所のブランド提案

原典 Hasasasa/html-to-editable-pptx のSKILLとconvert.pyを使い、架空焙煎所「ひと旗」の日本語ブランド提案を5枚制作。題名「小さな店の、ひとつの旗。」。レモン色×墨黒×濃いコーヒー茶。大胆な和文タイポ、余白、HTML/SVG図形、誌面ごとの構図変化。角丸カードなし。HTML原稿のテキストと簡単な図形を編集できるPPTXへ変換。実在ブランド・売上実績・効果数値を捏造しない。見出しZen Kaku Gothic New、引用Shippori Mincho、英数字Manrope。使用原TTF/OFLとMIT帰属を保持。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: Hasasasa / 原典条件: MIT

- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
