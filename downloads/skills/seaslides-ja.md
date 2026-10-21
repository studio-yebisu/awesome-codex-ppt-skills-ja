---
name: seaslides-ja
description: touying-typ/seaslidesの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

## このスキルでできること

同じ本文をHTML・SVG・PNG・PDFへ揃え、用途に合う紙面を保てる。

- 困っている状況: HTML・PDF・画像を別々に作ると、内容やページ構成がずれる。
- 必要な入力: 発表の目的・読み手・原稿、使用するデータや素材、必要な講稿。
- 受け取るもの: 同じ原稿・構成・テーマから生成するHTML資料と、原典の書き出し機能によるSVG・PNG・PDF。
- 必要環境: 作例のcompilerはPython 3.13、最終visual gateはpypdfを持つPython 3.12で実行。Pillow・pypdf・python-pptx、Node.js 24を使う再現条件で、最小対応版の保証ではない。 / 原典scripts/html_to_svg/package-lock.jsonのnpm依存、Playwright 1.60とChromium headless shell 1223。Motion 11.11.17の同梱bundleを使用。 / source/rebuild.pyはPythonからsource gate・HTML compiler --all・visual gateを呼ぶ。HTMLの閲覧はローカルHTTP。
- 作例で試した範囲: 架空の読書会の原稿・講稿をTCSにまとめ、HTML laneの同一buildから5頁のHTML・SVG・PNG・PDFを生成した。


# seaslides-ja

Studio Yebisuの日本語派生版。原作者の公式翻訳ではありません。

## 原典を読む

- upstream/skills/seaslides-html-slides-skill/SKILL.md

同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。

## 固有の制作方式

原典のHTML lane、TCS、editorial-magazineテーマを使い、source gate→固有compiler --all→visual gateで生成する。Windowsのreceipt相対パスをPOSIX表記へ直す2ファイルの派生差分を保持し、validatorは変更しない。原典Motion・WebGL・ナビゲーションを保持し、日本語OFL書体と講稿を収録する。HTML表示はローカルHTTP経由。PPTXは今回の出力に含めない。

## 日本語で完成させる

- 先に読み手、目的、結論、必要なページ、出力形式を決める。
- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。
- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。
- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境と全ページの実描画を確認する。
- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 原典の検査を省かない

- content_design_spec.mdで5頁の役割を決める
- content.htmlの本文と講稿、template.cssの再利用部品を編集する
- source/rebuild.pyで原典source gate・--all・visual gateを実行する
- overviewから全browser PNGを確認し、HTMLプレーヤーの移動も試す

- この作例はHTML lane。Typst・PPTX・画像生成は未実施
- Windowsの相対パスと診断文字コードだけ派生補正。validatorは無改変
- 静止画像とプレーヤーの操作UIは別の証拠
- 架空の読書会の企画で、開催実績ではない

原典の必須工程と、実施できなかった対人確認・実機条件を分けて記録する。再生成後に古いQA合格を引き継がない。作例の現在の検査記録はexample/QA.json。

## 単体の本文から使う

この本文は `skill-forks/seaslides-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/touying-typ/seaslides/tree/dcde5bf6c6875b300e2999fc7766f369a13a67ac

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `seaslides-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: touying-typ / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/touying-typ/seaslides/blob/dcde5bf6c6875b300e2999fc7766f369a13a67ac/LICENSE
