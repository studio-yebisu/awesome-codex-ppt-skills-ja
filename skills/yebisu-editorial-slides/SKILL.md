---
name: yebisu-editorial-slides
description: 雑誌とスイスデザインの構成を日本語向けに改修。Notoの和文書体、余白、講稿を使って企画を伝えます。 単なる既存文章の校正には使わない。
metadata:
  license: AGPL-3.0-only
  author: Studio Yebisu
---

# 余白で見せる、企画スライド

派生元：[op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) / `c91369c449d34755d320a8b81d0734000d99d1ab`。原作者の公式日本語版ではありません。原文・許諾・変更履歴は [CHANGES.md](CHANGES.md) と [LICENSE](LICENSE) を参照。

## 制作方針

企画・ブランド・発表会の資料に、エディトリアルまたはスイスデザインを選ぶ。エディトリアルはNoto Serif JPの大きな見出し、暖かな背景、広い余白。スイスはNoto Sans JPのサイズ差、グリッド、ひとつの強調色を使う。上流のWebGLテンプレート、スポンサーUI、プレゼンター同期機能は含まない。制作JSONからSVGと単独HTMLを生成し、発表者ノートを付ける。

日本語の資料を完成させる。出力形式、読者、目的を既存資料と依頼から判断し、未指定の細かなスタイルは選んで進める。
前提を変える情報が不足するときだけ確認する。デモ数値を実績として書かず、上流の公式成果物を名乗らない。
[日本語文字組み](references/japanese.md)を参照し、原稿の意味を保ちながら見出しと本文を整える。
JSON制作と同梱CLIの対応範囲は [入出力](references/schema.md) にある。実行できる入力例は `assets/example.json`。
原稿、制作JSON、SVG、再生HTML、講稿をまとめる。PPTXが必要な場合は同梱CLIの制限を確認して出力する。
出力を表示し、文字のはみ出し、改行、単位、出典、講稿を確認する。ネイティブ図形と画像を区別して報告する。
上流原文は比較・帰属のための保存資料で、この派生版の実行指示ではない。上流のscriptsや別スキルを探して実行しない。
