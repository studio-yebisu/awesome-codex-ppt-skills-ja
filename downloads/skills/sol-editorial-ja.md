---
name: sol-editorial-ja-entry
description: 編集誌のようなPowerPointを日本語で制作するときに使う。likaku/Mck-ppt-design-skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 編集誌のようなPowerPoint

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/likaku/Mck-ppt-design-skill/tree/e190e083b715b63172e1c4fea01bc5f9bb21a021

- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/SKILL.md
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/mck_ppt/deck_builder.py
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/mck_ppt/engine.py
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/mck_ppt/core.py
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/mck_ppt/constants.py
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/references/team/brand-guide.md
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/references/framework/engine-api.md
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/references/framework/guard-rails.md

原典DeckBuilder / MckEngineを使用し、原典core primitivesで6版式を明示拡張したnative PPTX。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python / python-pptx / lxml
- 固定原典Mck-ppt-design-skill
- 描画: Windows Microsoft PowerPoint
- Zen Kaku Gothic New / Shippori Mincho / Space Grotesk

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 余白を買う — 日帰りワークラウンジのブランド提案

架空の日帰りワークラウンジ「YOHAKU」のブランド提案を日本語6ページで作ってください。タイトルは「余白を買う」。対象は企画担当者と空間運営者。席数や売上の実績を作らず、企画の約束・一日の体験・言葉の使い方を伝えてください。アイボリー、墨黒、鮮やかな赤橙。大きな和文タイポと編集誌の余白、平面図形を使い、角丸カードや管理画面のような構成を避けてください。原典likaku/Mck-ppt-design-skillのDeckBuilderとtype/data schemaを使い、MckEngineの派生版としてレイアウト変更を明記。編集可能なPPTX、入力JSON、生成コードとプレビューを残してください。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: likaku / 原典条件: Apache-2.0

- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/LICENSE
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/NOTICE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
