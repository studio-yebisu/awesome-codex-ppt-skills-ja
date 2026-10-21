---
name: revealjs-skill-ja
description: ryanbbrown/revealjs-skillの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

## このスキルでできること

説明原稿をブラウザーで順に見せる資料にし、同じ内容をPDFでも配れる。

- 困っている状況: HTMLを並べるだけでは、発表のページ操作・ノート・段階表示を個別に作る必要がある。
- 必要な入力: 発表の目的・読み手・原稿、使用する図やデータ、講稿。
- 受け取るもの: ページ送りや発表操作を備えたreveal.jsのHTML資料と、原典の書き出しによるPDF・画像。
- 必要環境: 作例はNode.js 24.18、同梱reveal.js 5.2.1。原典create-presentation.jsで骨格を作る。 / PDF/画像の作例QAはDecktape 3.16.1（依存Puppeteer 24.40.0）。overflow検査には別系統のPuppeteer 25.13.0を使う。source/qa/package-lock.jsonの両系統を保ち、既存Edgeを指定する。 / 原典check-overflow.jsとHTTPでのブラウザー表示を確認する。新規の日本語組版は作例固有で、自動変換器の機能ではない。 / 同梱の再検証入口 python source/verify.py はPython 3標準ライブラリーを使う。reveal.js本体一般の必須依存とは区別する。
- 作例で試した範囲: 架空の社内検索企画を原典scaffoldから6頁のHTMLへ制作。原典overflow検査とDecktapeによるPDF・画像出力を行った。


# revealjs-skill-ja

Studio Yebisuの日本語派生版。原作者の公式翻訳ではありません。

## 原典を読む

- upstream/skills/revealjs/SKILL.md

同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。

## 固有の制作方式

原典create-presentation.jsで骨格を作る。元スキルのpt単位とsection構造を守り、reveal.jsの実ナビゲーションを使う。

## 日本語で完成させる

- 先に読み手、目的、結論、必要なページ、出力形式を決める。
- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。
- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。
- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境と全ページの実描画を確認する。
- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 原典の検査を省かない

- 話す順番と枚数を決め、create-presentation.jsで骨格を作る
- 本文はp要素、2列はinline gridで書く
- 項目の関係は矢印、表の見出しと行は色と罫線で分ける
- 原典check-overflow.jsを実行する
- Decktapeで全頁画像とPDFを出し、実表示を確認する

- 原典scaffold後の日本語組版は専用の手作業実装
- fragment・縦方向の入れ子・PDFからの逆変換は未実演
- 企画の数値は架空の条件と目標で、効果実績ではない
- Decktape3.16.1を同caseのQA依存へ固定。ブラウザーは既存Edgeを指定

原典の必須工程と、実施できなかった対人確認・実機条件を分けて記録する。再生成後に古いQA合格を引き継がない。作例の現在の検査記録はexample/QA.json。

## 単体の本文から使う

この本文は `skill-forks/revealjs-skill-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/ryanbbrown/revealjs-skill/tree/d0ccd344c4aaf9f045e5a15be6a2ab67b595796f

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `revealjs-skill-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: ryanbbrown / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/ryanbbrown/revealjs-skill/blob/d0ccd344c4aaf9f045e5a15be6a2ab67b595796f/LICENSE
