---
name: codex-image-ppt-ja-entry
description: 画像で伝えるスライドを日本語で制作するときに使う。ningzimu/codex-ppt-skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 画像で伝えるスライド

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/ningzimu/codex-ppt-skill/tree/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c

- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/LICENSE
- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/scripts/assemble_ppt.py
- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/scripts/prepare_slide_prompts.py
- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/scripts/record_slide_dispatch.py
- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/scripts/record_slide_result.py
- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/scripts/slide_job_status.py
- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/scripts/slide_run_state.py
- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/SKILL.md

原典prepare_slide_prompts/dispatch/result/state CLIを使用し、Codex native image_gen.imagegenで全3ページを生成。原典assemble_ppt.pyが画像とspeech.mdからPPTXを構築。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Codex native image_gen.imagegen
- Python / python-pptx / Pillow / filelock
- PowerPointとPowerShell 7（実描画QA）

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: Gitの保存・記録・共有

Gitの保存・記録・共有を説明する日本語3ページ。表紙、作業ツリー/ステージ/ローカル履歴の3段図、確認して共有する手順。16:9、写真なし、読みやすいベクトル風図解。ningzimu/codex-ppt-skillのnative画像生成と原典packagerを使う。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: ningzimu / 原典条件: MIT

- https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
