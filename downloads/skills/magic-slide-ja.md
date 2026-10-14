---
name: magic-slide-ja-entry
description: すばやく作るWebスライドを日本語で制作するときに使う。daniel-style/magic-slideの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# すばやく作るWebスライド

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/daniel-style/magic-slide/tree/e29d87cb315eb0afc939820b100d870eabf43f89

- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/AGENTS.md
- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/LICENSE
- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/README.md
- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/references/design-system.md
- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/references/flip-engine.md
- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/references/generation-guide.md
- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/references/html-contract.md
- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/references/images.md

原典merge-slides / auth scopeのみ派生injector / original serve / native Magic Move

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python3 / 原典serve.py
- Node（injectorのJS構文検査）
- Playwright（表示QA）

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 朝の支度を10分短くする企画

原典Magic Slideで「朝の支度を10分短くする企画」を日本語5枚にする。架空の5日間実験案、40分→30分と4+3+3分は仮定、効果は未検証と明示。服・鍵・バッグのカードと時間の数字を、隣接ページへ意味のあるMagic Moveとして受け渡す。原典merge/serveと認証関数のscopeを修正した日本語派生injectorを使い、原典のUIと動きを保持する。写真・外部APIは使わない。講稿を各頁に付け、原典Overviewを先に確認した後、サイト実例用に全頁・motion・移動をagent QAする。人間の正式レビューはpendingのまま残す。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: daniel-style / 原典条件: MIT

- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
