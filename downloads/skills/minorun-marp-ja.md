---
name: minorun-marp-ja
description: minorun365/minorun-marp-skillの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

## このスキルでできること

操作の説明を問いと段階図に変え、保存・選択・記録・共有の違いを追える。

- 困っている状況: 仕組み全体を一枚で見せると、話し手の説明と聞き手の読む順番がずれる。
- 必要な入力: 話の骨子、各頁で伝える内容、段階的に見せる図やコード、発表条件。
- 受け取るもの: 原典の暗色テーマを使ったMarp原稿と、図を少しずつ見せるHTML・PDF資料。
- 必要環境: 作例で使用した版はNode.js 24.18とMarp CLI 4.4.0。最小対応版の記録ではない。source/rebuild.pyとcheck-ai-smell.pyにはPython 3を使用。 / PDF/PNG出力にChromeまたはEdge。原典の全検査はPoppler・MuPDF tools・Pillow、SVG箱検査はMarp同梱puppeteer-coreを参照する。 / 字体の収録文字を変える場合はサブセットを更新する。別のmarp-mcpのAPIではなくminorunのMarp原稿・テーマ・検査ツールを使う。
- 作例で試した範囲: Git初学者向けの5分の導入を9頁に整理。問いと4段階の図をminorun-darkで組み、Marp CLIでHTML・PDF・PNGを出力した。


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

## 単体の本文から使う

この本文は `skill-forks/minorun-marp-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/minorun365/minorun-marp-skill/tree/736fd5e9fafb80148a1e6eaa5ae5f9d859431257

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `minorun-marp-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: minorun365 / 原典条件: Apache-2.0。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/LICENSE
