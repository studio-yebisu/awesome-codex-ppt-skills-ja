---
name: knowledge-cat-ppt-ja-entry
description: 図解でわかる教材を日本語で制作するときに使う。gnipbao/knowledge-cat-ppt-skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 図解でわかる教材

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/gnipbao/knowledge-cat-ppt-skill/tree/889c3dc00b356607fa9af935eb807056c3394886

- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/LICENSE
- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/SKILL.md
- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/README.md
- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/references/engine-routing.md
- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/references/native-pptx-recipes.md
- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/references/story-architecture.md
- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/references/design-systems.md
- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/references/qa-rubric.md

原典のnativeビルダーを使い、本文・表・図形・講稿を編集できる5枚のPowerPointを作成。Codexのartifact-tool環境を使用します。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python + python-pptx/Pillow
- Node + @oai/artifact-tool workspace
- PowerPointとNoto Sans JPは最終描画に使用

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 迷わない議事録のまとめ方

gnipbao/knowledge-cat-ppt-skillのnative-pptx laneと原典build_native_pptx.mjsを使い、架空の青葉企画向け「迷わない議事録のまとめ方」を日本語5枚で制作してください。決定事項・担当と期限・未決事項を分け、架空の記入例と会議末尾の確認方法を示します。入力計画を正本にし、本文・表・図形・講稿を編集可能にします。外部APIを呼ばず、原典validator・editability/probeとPowerPoint描画・目視で確かめてください。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: gnipbao / 原典条件: MIT

- https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/889c3dc00b356607fa9af935eb807056c3394886/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
