---
name: pradaslides-ja-entry
description: 構成から仕上げるPowerPointを日本語で制作するときに使う。prodigeproject/pradaslidesの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 構成から仕上げるPowerPoint

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/prodigeproject/pradaslides/tree/b9219b238d812d0dd7b4ed9fb514effbad0d0928

- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/LICENSE
- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/README.md
- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/SKILL.md
- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/references/art-direction-and-pptx-reconstruction.md
- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/references/artifact-contracts.md
- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/references/capability-orchestration.md
- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/references/content-and-narrative.md
- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/references/design-and-visuals.md

原典計画契約とlint → native PPTX → PowerPoint実描画 → 原典render-parity presenter

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Windows / Microsoft PowerPoint / PowerShell 7
- Python 3.10+ / python-pptx 1.0.2
- Node.js 22+ / ChromeまたはEdge
- Yu Gothic（OSフォント）

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 町内会の備品貸出を、迷わない手順に

PradaSlidesの原典ワークフローで「町内会の備品貸出を、迷わない手順に」を日本語6ページにする。既定の編集可能PPTXを正本とし、原典build_pptx_preview.pyでPowerPoint実描画からHTML presenterを作る。町内会で備品を借りる人が申込み・受取り・異常時の連絡・返却を確認できる内容にする。すべて架空の手順案。生成画像を使わず、申込書の例と手順図・照合表をnative要素で作る。原典の計画lint、PPTX検査、HTML QAを使い、全ページを実描画・目視する。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: prodigeproject / 原典条件: MIT

- https://github.com/prodigeproject/pradaslides/blob/b9219b238d812d0dd7b4ed9fb514effbad0d0928/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
