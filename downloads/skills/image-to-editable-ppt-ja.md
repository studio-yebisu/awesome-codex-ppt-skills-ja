---
name: image-to-editable-ppt-ja-entry
description: 画像から編集できる図へを日本語で制作するときに使う。ningzimu/image-to-editable-ppt-skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 画像から編集できる図へ

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/ningzimu/image-to-editable-ppt-skill/tree/b7be494e31a0ed56ef98716891db5474606b8cdf

- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/AGENTS.md
- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/LICENSE
- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/README.md
- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/README_en.md
- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/skills/image-to-editable-ppt/agents/openai.yaml
- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/skills/image-to-editable-ppt/cli/editppt/__init__.py
- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/skills/image-to-editable-ppt/cli/editppt/cli.py
- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/skills/image-to-editable-ppt/cli/editppt/runtime/__init__.py

Original editppt CLI + page workers + built-in image editing

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python3.10+ / 原典editppt CLI
- 新規入力には内蔵画像編集とpage worker対応エージェント
- PowerPoint（今回の表示QA）

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 画像から編集できるGit入門へ

既存の日本語Git入門画像2枚を、原典image-to-editable-pptのCLIとページworkerで編集可能なPowerPointへ再構成。文字、カード、単純な矢印はnative要素。アイコンはCodex内蔵image_genによる元画像の編集で分離し、画像として配置。第三者API、購入、外部OCRは使わない。元画像と完成PowerPointの全ページを視認し、編集できる部分と画像部分を明示する。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: ningzimu / 原典条件: MIT

- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
