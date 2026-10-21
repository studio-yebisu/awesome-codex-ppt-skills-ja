---
name: magic-slide-ja
description: daniel-style/magic-slideの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

## このスキルでできること

説明をまたいで残る要素と変える要素を先に決め、同じ図形の移動や拡大で内容の変化を示せる。

- 困っている状況: 毎ページで要素を消して出すと、時間や準備品の変化を追いにくい。
- 必要な入力: 発表の原稿・目的・読み手と、頁をまたいで引き継ぐ要素や変化。
- 受け取るもの: 同じ要素の移動や拡大でページをつなぐHTML、全体表示と講稿。
- 必要環境: 生成と原典serve.pyはPython 3。injectorのJavaScript構文確認はNode.js。 / 表示QAにはPlaywrightと対応ブラウザー。原典serve経由の編集・保存と静的カタログiframeの表示を区別する。
- 作例で試した範囲: 朝の支度を40分から30分へ移す仮説を5頁で説明。同じ数字・準備品を4つの頁境界で引き継ぎ、Magic Moveの前・途中・後を記録した。


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
- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境と全ページの実描画を確認する。
- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 原典の検査を省かない

- sources/outline.mdで結論・読み手・終わり方を決める
- sources/brief.mdで題材・書体・配色と採らない表現を決める
- 数字と持ち物に同じmagic-idを付け、各頁の意味に沿って置く
- 原典mergeと認証scopeのみ派生したinjectorで生成する
- 原典serveでOverview→通常再生→全境界の動きを確認する

- 40・30・4・3・3分は仮定、短縮効果は未検証
- 認証付きQA関数のscope修正のみ。server認証と保存先制限は原典のまま
- 静的カタログiframeでは編集・保存が使えない
- agentの検証と人のrevision/adoptionは別。後者はpending
- 静止画だけcursorとtrailを非表示にして撮影。通常runtimeは保持

原典の必須工程と、実施できなかった対人確認・実機条件を分けて記録する。再生成後に古いQA合格を引き継がない。作例の現在の検査記録はexample/QA.json。

## 単体の本文から使う

この本文は `skill-forks/magic-slide-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/daniel-style/magic-slide/tree/e29d87cb315eb0afc939820b100d870eabf43f89

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `magic-slide-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: daniel-style / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/daniel-style/magic-slide/blob/e29d87cb315eb0afc939820b100d870eabf43f89/LICENSE
