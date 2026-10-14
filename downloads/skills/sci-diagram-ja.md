---
name: sci-diagram-ja-entry
description: 編集できる科学の概念図を日本語で制作するときに使う。HututuWorks/sci-diagram-pptxの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 編集できる科学の概念図

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/HututuWorks/sci-diagram-pptx/tree/cc8f0030edf80eeab6e52849b8c39fe638466776

- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/README.md
- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/skills/sci-diagram-pptx/SKILL.md
- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/LICENSE

原典公式PptxGenJS portable templateを直接拡張。NODES/EDGES/INSETSとnative矢印・断面図による5枚の新規科学概念図。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Node.js20+ / PptxGenJS4.0.1 (MIT)
- 書体: Zen Kaku Gothic New / Space Grotesk
- 描画: Windows Microsoft PowerPoint、またはLibreOffice/pdftoppm/Python3.10+

- 原典のportable PptxGenJS 4.0.1方式を使用。内部評価専用のホストSDKは必要ない。
- 科学内容はUSGS一次解説に基づく概念モデル。定量的な実験結果ではない。

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 雨が、地下水になるまで。

雨が地下水になる仕組みを、一般の読者へ向けた日本語5ページの科学概念図にしてください。表題は「雨が、地下水になるまで。」。砂色・藍・鮮やかな水色、大胆な和文見出しと編集可能な断面図・矢印・注釈で構成します。USGSの一次解説を参照し、降水から地表流出、蒸発・蒸散、浸透を分け、不飽和帯と飽和帯、地下水面、涵養、川への流出を正しく説明してください。定量値や実験結果を作らず、縮尺のない概念モデルと明記。HututuWorks/sci-diagram-pptxの原典native ownershipと明示的NODES/EDGES/INSETS、source→targetのtail矢印規約を使います。原典の単図再構成を新規概念図5枚に拡張したことを明記し、native PPTXと入力JSON、実行したbuild.mjsを残してください。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: HututuWorks / 原典条件: Apache-2.0

- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/LICENSE
- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/skills/sci-diagram-pptx/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
