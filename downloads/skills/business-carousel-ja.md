---
name: business-carousel-ja-entry
description: 正方形のカルーセルを日本語で制作するときに使う。minhnv0807/ai-business-skillsの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 正方形のカルーセル

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/minhnv0807/ai-business-skills/tree/0360adced422a08f70c3eff8905b81962872105d

- https://github.com/minhnv0807/ai-business-skills/blob/0360adced422a08f70c3eff8905b81962872105d/LICENSE
- https://github.com/minhnv0807/ai-business-skills/blob/0360adced422a08f70c3eff8905b81962872105d/skills/en/43-carousel-brief-global/SKILL.md

この集の43-carousel-brief-globalは、デザイナーへ渡すブリーフと構成確認用HTMLを作る指示型スキルです。原典に自動スライド生成CLIはありません。読み手・ブランド→構成→短い原稿→図案と背景→1080×1080のHTMLという原典の工程をCodexが実行しました。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.13 / fontTools / Brotli（この作例の再現）
- HTTPで表示できるブラウザー
- 公式BIZ UDPGothicのOFL書体（固定版を取得・サブセット化）



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 引き継ぎ、何を書けばいい？

minhnv0807/ai-business-skillsの43-carousel-brief-globalを読み、添付の架空ブランドと原稿で「引き継ぎ、何を書けばいい？」を日本語6枚のSNSカルーセルとして構成確認する。原典のHook→Problem→Insight→Solution→Example→CTA、1枚1論点、Hook/CTA濃色・本文淡色、1080×1080のHTML、ページ番号と進捗を守る。Proofの実績は作らず、記入例と明示。BIZ UDPGothicのOFLを保ち、プレビューと公開用の仕上げ・人の承認を区別する。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: minhnv0807 / 原典条件: MIT

- https://github.com/minhnv0807/ai-business-skills/blob/0360adced422a08f70c3eff8905b81962872105d/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
