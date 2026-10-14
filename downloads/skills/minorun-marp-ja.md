---
name: minorun-marp-ja-entry
description: Markdownで育てる資料を日本語で制作するときに使う。minorun365/minorun-marp-skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# Markdownで育てる資料

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/minorun365/minorun-marp-skill/tree/736fd5e9fafb80148a1e6eaa5ae5f9d859431257

- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/skills/slide-story/SKILL.md
- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/skills/slide-figures/SKILL.md
- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/skills/slide-design-dark/SKILL.md
- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/theme/minorun-dark.css
- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/tools/check-ai-smell.py
- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/LICENSE

原典のslide-story・slide-figures・slide-design-darkを適用。黒地テーマ本体を保持し、作業・ステージ・記録・共有の図を段階的に開示するMarp原稿を制作。Marp CLIで実HTMLを生成。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Node.js 24.18
- Marp CLI 4.4.0
- 元スキルを読めるエージェント
- PDF書出しにはChrome系ブラウザと原典の検査ツール



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: Gitの変更、どこに保存された？

minorun365/minorun-marp-skill の原典スキルを読み、添付の入力資料を使って「Gitの変更、どこに保存された？」を日本語で制作してください。minorun-dark / Marpを使用し、そのリポ固有の生成手順・テンプレート・実装を保ってください。完成ファイルを開き、全ページの日本語・図表・ページ移動を確認してください。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: minorun365 / 原典条件: Apache-2.0

- https://github.com/minorun365/minorun-marp-skill/blob/736fd5e9fafb80148a1e6eaa5ae5f9d859431257/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
