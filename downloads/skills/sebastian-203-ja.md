---
name: academic-review-decksmith-ja
description: 研究概要・論文レビューを、出典と仮説を区別した日本語の編集可能PowerPointにする。
---

# 日本語の研究スライド

原典の固定版と同梱テンプレートを使う。原典の研究アウトライン対応に従い、未実施提案では結果を作らず、問い・仮説・方法・評価・制約を構成する。

1. 入力と原典参照を読む。事実、仮説、計画を区別する。
2. 1頁1論点。背景、空間モデル、検証関係、比較条件、試行方法、評価、実施条件へ整理する。
3. academic-template.pptxを複製し、master、白地、青い罫線、余白、下部帯、頁番号を保持。見本の著者・機関・文言は残さない。
4. 日本語は意味のまとまりで改行。Noto Sans CJK JPを指定。図・表・工程はネイティブ編集可能にし、重要な図には読図・読表の短い説明を添える。
5. 実測値・引用・研究成果を捏造しない。未実施提案の状態を表紙とフッターに明示。
6. 完成PPTXを実レンダリングし、初回表示で欠けと衝突を確認。確認方法と限界を記録する。

## 必要な参照

原典SKILL.mdとreferences/academic_review_deck_workflow.md、figure_formula_guidelines.md、review_language_rules.md。本文だけではテンプレ・生成ソースは揃わないため、一式ZIPを使用する。

原典固定版：https://github.com/ficooooo/Paper2ScholarSlides/tree/207f2b6c8493c569f6caf466c87d868c42936cf6

MIT。LICENSEを保持。OS書体は抽出配布しない。

## 作例の書体を揃える

Noto Sans CJK JPのRegular/Boldは、サイトの「作例の書体を取得」から公式配布物とOFL原文を取得できる。原稿とPPTXに指定したフォント名を揃える。Noto Sans JPとは名前が異なる。OSの書体は抽出せず、作成者と受け手の端末に公式フォントを導入する。

固定配布元: https://github.com/notofonts/noto-cjk/tree/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/OTF/Japanese

## 単体の本文から使う

この本文は `skill-forks/sebastian-203-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/ficooooo/Paper2ScholarSlides/tree/207f2b6c8493c569f6caf466c87d868c42936cf6

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-203-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: ficooooo / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/ficooooo/Paper2ScholarSlides/blob/207f2b6c8493c569f6caf466c87d868c42936cf6/LICENSE
