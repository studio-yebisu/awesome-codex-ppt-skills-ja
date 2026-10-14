---
name: seaslides-ja-entry
description: 構成から組むWebスライドを日本語で制作するときに使う。touying-typ/seaslidesの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 構成から組むWebスライド

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/touying-typ/seaslides/tree/dcde5bf6c6875b300e2999fc7766f369a13a67ac

- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/LICENSE
- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/README.md
- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/skills/seaslides-html-slides-skill/references/ai-image-comparison/_index.md
- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/skills/seaslides-html-slides-skill/references/ai-image-comparison/README.md
- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/skills/seaslides-html-slides-skill/references/artifact-ownership.md
- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/skills/seaslides-html-slides-skill/references/checklist.md
- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/skills/seaslides-html-slides-skill/references/components.md
- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/skills/seaslides-html-slides-skill/references/design-guide.md

原典TCS→source gate→html_compiler --all→visual gate。Windows receipt pathのみ派生修正。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.13 / Pillow / pypdf / python-pptx
- Node24 / 原典package-lockのnpm依存 / Chromium1223
- ローカルHTTPで表示

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 読書会を月1回続けるには

touying-typ/seaslidesのHTML lane、editorial-magazineテーマ、原典コンパイラを使い、架空の地域サークル「ひだまり読書会」向けに「読書会を月1回続けるには」を日本語5ページで制作する。日時・参加条件・60分の進行・三人の役割・3か月の試行を示す。入力は企画案であり実績ではない。本文・CSS・shellを分離し、外部APIや画像生成を使わず、原典source gateと全出力buildとvisual gateを実行する。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: touying-typ / 原典条件: MIT

- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
