---
name: html-scrolline-ja-entry
description: スクロールで語る企画を日本語で制作するときに使う。gongnyang/awesome-html-scrolline-deckの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# スクロールで語る企画

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/gongnyang/awesome-html-scrolline-deck/tree/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc

- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/LICENSE
- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/SKILL.md
- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/README.md
- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/plan/CONTRACTS.md
- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/docs/writing-a-deck.md
- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/docs/getting-started.md
- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/docs/export.md
- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/package.json

原典deck CLI・Scrolline engine・rail-advance・era-shift・Vite build・smoke

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Node.js 22+ / npm
- Python 3（再実行CLI）
- ChromeまたはEdge / ffmpeg（smoke描画）
- 日本語フォント（WindowsではYu Mincho / Yu Gothic）

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 小さな展示を、ひらくまで

Scrolline v2の原典SKILL、CONTRACTS、railコンセプトと原典CLIを使い、「小さな展示を、ひらくまで」を日本語のスクロール資料にする。架空の写真展の計画案と明記し、企画・会場・案内・当日準備を6停止点で示す。原典のrail-advanceで項目と月を進め、era-shiftで段階を連続的につなぐ。engine・moves・conceptsは変更しない。deck.yamlとdeck側の日本語CSSで調整し、原典plan、Vite build、smoke、実際のキーとホイール操作を確認する。原典全体CIの失敗は隠さず、ローカルHTTP表示の確認と分けて残す。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: gongnyang / 原典条件: MIT（原典） / GSAPは独自の無償標準条件 / LenisはMIT

- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
