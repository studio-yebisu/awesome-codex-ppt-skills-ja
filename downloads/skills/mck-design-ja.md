---
name: mck-design-ja
description: likaku/Mck-ppt-design-skillの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

# mck-design-ja

Studio Yebisuの日本語派生版。原作者の公式翻訳ではありません。

## 原典を読む

- upstream/SKILL.md

同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。

## 固有の制作方式

原典DeckBuilderとMckEngineを使う。原典の存在しないlayouts参照を前提にせず、同梱engine-apiと実コードを読む。今回のS3/S4検査はPASS、98点。自動採点をデザイン承認とは扱わない。

## 日本語で完成させる

- 先に読み手、目的、結論、必要なページ、出力形式を決める。
- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。
- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。
- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境と全ページの実描画を確認する。
- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## この方式で気をつけること

- 同梱専用生成器の再生と、自分の原稿から適切な高水準APIを選ぶ一般手順を区別する。
- 原典固定パス ~/.workbuddy/skills/mck-ppt-design を同梱upstreamへ切り替える。references/layoutsは固定原典にも存在しないため、API/容量表/公開引数を読む。

## 単体の本文から使う

この本文は `skill-forks/mck-design-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/likaku/Mck-ppt-design-skill/tree/e190e083b715b63172e1c4fea01bc5f9bb21a021

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `mck-design-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: likaku / 原典条件: Apache-2.0。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/LICENSE
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/NOTICE
