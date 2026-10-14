---
name: guizang-ppt-skill-ja-entry
description: 雑誌とSwissのレイアウトを日本語で制作するときに使う。op7418/guizang-ppt-skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 雑誌とSwissのレイアウト

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/op7418/guizang-ppt-skill/tree/c91369c449d34755d320a8b81d0734000d99d1ab

- https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/README.md
- https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/SKILL.md
- https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/LICENSE

元HTMLテンプレートに題材別本文を挿入。元ページ制御・演出を維持し、日本語字形・講稿・構図を調整。

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

作例: 週末の汐見港町 回遊企画提案

$guizang-ppt-skill-ja を使ってください。

「週末の汐見港町 回遊企画提案」をguizang-ppt-skill-jaで日本語の7枚にしてください。
input/data.jsonを数値・事実・仮定の正本とします。読者：架空の商店会と案内スタッフ。7分の企画説明。
構成：週末の汐見港町 → 対象者と体験 → 4時間の徒歩行程 → 集客と、次の店への案内 → 4日間の試行と運営 → 試行の測り方 → 次の判断。
出力：Magazine / Ink Classicの元テンプレートを使用したHTML一式と講稿。
単位・比較期間を揃え、仮説と事実、目標と実績を区別。日本語字形と改行を実表示で確認。架空のサンプルと明記し、原典・条件・制作ソースを保持。実施した検証だけを記録してください。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: op7418 / 原典条件: AGPL-3.0

- https://github.com/op7418/guizang-ppt-skill/blob/c91369c449d34755d320a8b81d0734000d99d1ab/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
