---
name: cyberppt-ja-entry
description: 情報を整理するPPTXを日本語で制作するときに使う。crazyykhllc-bit/CyberPPTの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 情報を整理するPPTX

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/crazyykhllc-bit/CyberPPT/tree/980e5576565f0673c67ee41b01d20ed66cb8417c

- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/LICENSE
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/references/ppt-production.md
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/references/quality-assurance.md
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/references/source-analysis.md
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/references/storyline.md
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/references/visual-system.md
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/scripts/build_component_signature.py
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/scripts/build_content_lock.py

原典の内容lock、ImageGen設計見本、測定・比較スクリプトを使い、主要文字と表をPptxGenJSで再構築。厳密画像一致と日本語派生QAを分離。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Node.js / PptxGenJS 4.0.1
- Python / Pillow, numpy, pywin32
- Windows / Microsoft PowerPoint
- Yu Gothic / Yu Mincho / Times New Roman
- 新規設計見本にはImageGen

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 商店街のイベント案内を、一つにまとめる

CyberPPTの固定commitの原文と補助スクリプトを使い、日本語5枚の企画資料「商店街のイベント案内を、一つにまとめる」を作る。
題材は架空のこもれび商店街。課題仮説、イベントの比較項目、更新担当、試行計画を説明する。実在の開催情報・実測の改善効果に見せない。
内容をlockし、ImageGenで全ページの設計見本を作り、原典の紙色＋銅色の小売向けスタイルを採用する。設計見本からPptxGenJSで単頁ずつネイティブ再構築し、PowerPoint本体で描画する。
原典の厳密画像一致テストは実行し、失敗結果をそのまま残す。日本語派生では字形の完全一致と可読性・編集性を区別し、要素の意味と数字を保持する。見切れ・不自然な折り返しを修正する。
原典原文・派生差分・入力・見本・単頁・比較結果・実行ログを保存する。人間の承認や正式採用を受けたとは記録しない。


上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: crazyykhllc-bit / 原典条件: MIT

- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/LICENSE
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/assets/icons/tabler-outline/license.svg

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
