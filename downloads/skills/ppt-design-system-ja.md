---
name: ppt-design-system-ja-entry
description: デザインを揃えるPPTXを日本語で制作するときに使う。att6113/ppt-design-systemの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# デザインを揃えるPPTX

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/att6113/ppt-design-system/tree/9f39af607ab82da2827530c38b9dc86eb75768ee

- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/LICENSE
- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/SKILL.md
- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/README.md
- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/assets/template.html
- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/references/themes.md
- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/references/layouts.md
- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/references/presets.md

原典HTMLテンプレート・Forest Ink配色・原典ナビゲーション

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3（生成。標準ライブラリのみ）
- Node.js 22+ と Chrome/Edge（任意の描画検証）
- 閲覧端末の日本語フォント

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 雨の日も迷わない、図書館イベント案内

att6113/ppt-design-systemの原典SKILLとassets/template.htmlを使い、「雨の日も迷わない、図書館イベント案内」を日本語6ページにする。Forest Ink配色、原典の見出し階層、カバー・数値カード・本文・問い・比較・終わりのレイアウトを使う。本文は架空の読書会への参加案内として役に立つ内容にし、製品の説明書にしない。原典の矢印キー・ドット・横スクロールを保持する。日本語フォントは端末のフォントを使い、外部フォントを不要にする。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: att6113 / 原典条件: MIT（原典。通知同梱）

- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
