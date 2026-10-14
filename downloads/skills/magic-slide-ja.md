---
name: magic-slide-ja
description: daniel-style/magic-slideの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

# magic-slide-ja

Studio Yebisuの日本語派生版。原作者の公式翻訳ではありません。

## 原典を読む

- upstream/SKILL.md

同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。

## 固有の制作方式

原典のoutline/Brief Lite、モジュールHTML/CSS、merge、inject、serveとMagic Moveを使う。隣接ページで数字・準備品を意味に沿って受け渡す。認証関数のscopeだけを修正した日本語派生injectorを使い、原典と差分を保持する。cursor、dock、Overview、動き、serverの認証と保存先制限を保持する。表示用iframeと、原典serverでの編集・保存を案内し、agent QAと人のrevision/adoptionを区別する。

## 日本語で完成させる

- 先に読み手、目的、結論、必要なページ、出力形式を決める。
- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。
- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。
- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境を案内し、主要な完成ファイルが開くことを確認する。
- 原典の方式で実ファイルを生成し、主要な出力の初回表示を確認する。原典の必須ビルド確認は維持し、明白な欠けだけ直す。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 単体の本文から使う

この本文は `skill-forks/magic-slide-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/daniel-style/magic-slide/tree/e29d87cb315eb0afc939820b100d870eabf43f89

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `magic-slide-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: daniel-style / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/LICENSE
