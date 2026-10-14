---
name: qiaomu-bento-ja-entry
description: Bentoで整理する提案を日本語で制作するときに使う。joeseesun/qiaomu-bento-pptの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# Bentoで整理する提案

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/joeseesun/qiaomu-bento-ppt/tree/55c63c836f42bc9175757d077428c395cd93effe

- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/SKILL.md
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/references/workflow.md
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/references/upstream-contract.md
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/references/upstream/bento-format.md
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/references/upstream/bento-agents.md
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/scripts/bento_deck.py
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/upstream.lock.json
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/NOTICE.md

原典の固定Bento shell・文書スキーマを使用。bento_deck.pyでJSONを検証し、シェルを変えずに編集版と再生版の.bento.htmlを構築。検索の同一要素が権限確認から回答へ移るmorphを制作。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.13
- スキルに同梱されたBento shell v1.0.10
- ブラウザ



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 社内検索を4週間で試す

joeseesun/qiaomu-bento-ppt の原典スキルを読み、添付の入力資料を使って「社内検索を4週間で試す」を日本語で制作してください。bento/slides / morph + native tableを使用し、そのリポ固有の生成手順・テンプレート・実装を保ってください。完成ファイルを開き、全ページの日本語・図表・ページ移動を確認してください。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: joeseesun / 原典条件: MIT

- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/LICENSE
- https://github.com/joeseesun/qiaomu-bento-ppt/blob/55c63c836f42bc9175757d077428c395cd93effe/NOTICE.md

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
