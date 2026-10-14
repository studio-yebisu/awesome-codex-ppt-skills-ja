---
name: japanese-corporate-ja-entry
description: 日本語の業務資料を日本語で制作するときに使う。gonta223/japanese-corporate-pptx-skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 日本語の業務資料

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/gonta223/japanese-corporate-pptx-skill/tree/05480bfa2d8f097ab397861cbe390429e1dbb824

- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/SKILL.md
- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/references/research-backed-patterns.md
- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/references/jtc-authenticity.md
- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/references/visual-style.md
- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/references/writing-and-density.md
- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/references/layout-catalog.md
- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/references/qa-checklist.md
- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/skills/japanese-corporate-pptx/assets/japanese-corporate-ponchi-template.pptx

公式15型PPTXから1・2・11・9・8・14枚目を選択し、SKILLの規約に従ってネイティブ図形・チャート・表を編集。専用生成APIは同梱されていない。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.13 / python-pptx / lxml / Pillow
- Microsoft PowerPoint 16.0 と PowerShell 7（PNG/PDF描画）
- 同梱の japanese-corporate-ponchi-template.pptx



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: くらし便 EC事業 9月報告

添付の架空EC月次データを使い、gonta223/japanese-corporate-pptx-skillの固有の制作方法で完結した日本語資料を作成してください。売上増と粗利率低下を区別し、返品理由の分類、商品説明の修正、担当・期限、広告増額の判断条件を含めます。編集可能なPPTXと全ページPDFを出力してください。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: gonta223 / 原典条件: MIT

- https://github.com/gonta223/japanese-corporate-pptx-skill/blob/05480bfa2d8f097ab397861cbe390429e1dbb824/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
