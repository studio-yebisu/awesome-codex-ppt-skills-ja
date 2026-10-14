---
name: hands-on-deck-ja-entry
description: JSONで編集するPowerPointを日本語で制作するときに使う。EveryInc/hands-on-deckの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# JSONで編集するPowerPoint

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/EveryInc/hands-on-deck/tree/a24b996ecff6393ccf39c4fee2b88c493fb0b693

- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/skills/hands-on-deck/designing-slides.md
- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/LICENSE
- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/README.md
- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/skills/hands-on-deck/scripts/deck.py
- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/skills/hands-on-deck/scripts/html2patch.py
- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/skills/hands-on-deck/scripts/inventory.py
- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/skills/hands-on-deck/scripts/merge_decks.py
- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/skills/hands-on-deck/scripts/rearrange.py

原典deck.pyのinspect・JSON patch・apply・fix・diffを実行

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.10+ / python-pptx / Pillow
- 描画: Windows / Microsoft PowerPoint
- 原典render: LibreOffice / Poppler
- Yu Gothic / Yu Mincho / Times New Roman



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: イベント案内の公開前チェック

hands-on-deckの固定commitと原典deck.pyを使い、同梱した編集可能な日本語PPTXを「イベント案内の公開前チェック」へ編集する。5枚のテーマを、概要、案内の経路、想定問題、確認担当、利用者目線の確認へ変更する。図形構造と書式を保ち、架空の例・未実施を明示する。inspectで対象を確認し、JSON patchをapply、fix、diff、PowerPoint描画を行う。全ページを別エージェントが小分けで確認し、実行ログと原典ライセンスを残す。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: EveryInc / 原典条件: MIT

- https://github.com/EveryInc/hands-on-deck/blob/a24b996ecff6393ccf39c4fee2b88c493fb0b693/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
