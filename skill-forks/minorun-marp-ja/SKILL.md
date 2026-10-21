---
name: minorun-marp-ja
description: minorun365/minorun-marp-skillの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

# minorun-marp-ja

Studio Yebisuの日本語派生版。原作者の公式翻訳ではありません。

## 原典を読む

- upstream/skills/slide-story/SKILL.md
- upstream/skills/slide-figures/SKILL.md
- upstream/skills/slide-design-dark/SKILL.md

同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。

## 固有の制作方式

元の日本語3スキル（story・figures・dark design）を読み、問いと段階的な図解を作る。原典minorun-darkテーマでMarp CLIを実行し、check-ai-smellも実行する。

## 日本語で完成させる

- 先に読み手、目的、結論、必要なページ、出力形式を決める。
- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。
- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。
- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境と全ページの実描画を確認する。
- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 原典の検査を省かない

- 5分の導入範囲と読み手をinput/BRIEF.mdで確定する
- deck.mdで問いと回答を続け、見出しを一行にする
- 段階SVGで既存の箱の位置を保って一要素ずつ足す
- source/rebuild.pyへMarp CLIとブラウザーの場所を渡す
- check-ai-smell --allとPDF全頁を確認する

- 元35分教材のうち5分の導入抜粋。元依頼は入力内へ保存
- 20分演習・ブランチ・レビュー・競合解消は扱わない
- Gitコマンドは説明例で、リモート送信はしていない
- 本文を変えたときは埋込サブセット書体の収録文字も更新する

原典の必須工程と、実施できなかった対人確認・実機条件を分けて記録する。再生成後に古いQA合格を引き継がない。作例の現在の検査記録はexample/QA.json。
