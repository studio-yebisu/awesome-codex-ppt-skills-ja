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
