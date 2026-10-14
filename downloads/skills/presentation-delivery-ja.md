---
name: presentation-delivery-ja-entry
description: HTMLから編集できるPPTXを日本語で制作するときに使う。ConnorRX56/presentation-delivery-skillsの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# HTMLから編集できるPPTX

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/ConnorRX56/presentation-delivery-skills/tree/06ddac077030c62f0118b225860cac46fbf658ea

- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/LICENSE
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/README.md
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/LICENSE
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/SKILL.md
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/package.json
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/references/slide-decks.md
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/references/editable-pptx.md
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/references/typography.md

原典HTML-first Path A → 原典DOM要素変換・寸法検査 → native PPTX / PDF

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python3（標準ライブラリ）
- Node.js22以上 / npm / 初回公式Chromium取得
- PowerPoint描画: Windows / Microsoft PowerPoint / PowerShell7 / インストール済みBIZ UDPGothic

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 引き継ぎは、次の一手まで。

ConnorRX56/presentation-delivery-skillsのvisual-deck-studio原典を使い、社内向け「引き継ぎは、次の一手まで。」を日本語6枚で作る。HTML-first Path Aの960×540ptと4条件を守り、原典deck_index.html、html2pptx.js、PDF exporterを使用する。原典の検査を保ち、本文と単純図形をPowerPointで編集可能にする。既存カタログの紙色・深緑とBIZ UDPGothicを参考にする。ファイル名や作業状況の例は架空と明記し、発表ノートを付ける。2枚の表示確認後に全6枚を作り、HTTPのHTML、PDF、PowerPoint本体で表示を確認する。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: ConnorRX56 / 原典条件: MIT原典 / OFL BIZ UDPGothic / 各Node依存の原文通知

- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/LICENSE
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
