---
name: ppt-master-ja-entry
description: 編集できる日本語PPTXを日本語で制作するときに使う。hugohe3/ppt-masterの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 編集できる日本語PPTX

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/hugohe3/ppt-master/tree/ca04346de145ed6462ddf34682848e71df5e20a2

- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/README.md
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/SKILL.md
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/LICENSE

日本語の文字・図形profile。上流guard・checker・native SVG→PPTX変換器を使用。Default全工程ではない。PowerPoint本体でPNG/PDF出力。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- 原典のスキルを読めるコーディングエージェント
- 各作例のPROVENANCE.jsonに記録した制作環境
- Noto Sans JP（PowerPointでの表示）

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 喫茶つむぎ 2号店出店提案

$ppt-master-ja を使ってください。

「喫茶つむぎ 2号店出店提案」をppt-master-jaで日本語の8枚にしてください。
input/data.jsonを数値・事実・仮定の正本とします。読者：店舗経営者・店長。8分の決裁説明と、後日の店内説明会。
構成：運河沿いB案を、調査・交渉へ → 新店の顧客と、既存店との役割 → 候補地の比較：B案は82点 → 損益分岐は、一日60人 → 仕込みと購買を共通化する → 契約前に、3つのリスクを確認 → 5週目に、投資判断を置く → 今日の決裁：B案の調査を進める。
出力：編集可能なPPTX、閲覧用PDF、ページ別講稿。
単位・比較期間を揃え、仮説と事実、目標と実績を区別。日本語字形と改行を実表示で確認。架空のサンプルと明記し、原典・条件・制作ソースを保持。実施した検証だけを記録してください。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: hugohe3 / 原典条件: MIT

- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/LICENSE
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/LICENSE
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/scripts/pptx_shapes/data/NOTICE.md
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/templates/icons/tabler-outline/license.svg

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
