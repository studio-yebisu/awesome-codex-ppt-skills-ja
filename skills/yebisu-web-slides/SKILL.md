---
name: yebisu-web-slides
description: 依存の少ないHTMLと固定ステージを継承。日本語の登壇資料に、短い動きとキー操作を添えます。 単なる既存文章の校正には使わない。
metadata:
  license: MIT
  author: Studio Yebisu
---

# 軽くて動く、Webスライド

派生元：[zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) / `9906a34d640d2111f724544cbc50f7f130569ae1`。原作者の公式日本語版ではありません。原文・許諾・変更履歴は [CHANGES.md](CHANGES.md) と [LICENSE](LICENSE) を参照。

## 制作方針

16:9のステージを固定し、ページのスクロールを発表操作に使わない。CSSの短い出現、左右キー、停止できる自動再生、講稿を使えるようにする。スマートフォンとprefers-reduced-motionでも確認する。派手な演出を増やすより、話す順番と視線の誘導を揃える。

日本語の資料を完成させる。出力形式、読者、目的を既存資料と依頼から判断し、未指定の細かなスタイルは選んで進める。
前提を変える情報が不足するときだけ確認する。デモ数値を実績として書かず、上流の公式成果物を名乗らない。
[日本語文字組み](references/japanese.md)を参照し、原稿の意味を保ちながら見出しと本文を整える。
JSON制作と同梱CLIの対応範囲は [入出力](references/schema.md) にある。実行できる入力例は `assets/example.json`。
原稿、制作JSON、SVG、再生HTML、講稿をまとめる。PPTXが必要な場合は同梱CLIの制限を確認して出力する。
出力を表示し、文字のはみ出し、改行、単位、出典、講稿を確認する。ネイティブ図形と画像を区別して報告する。
上流原文は比較・帰属のための保存資料で、この派生版の実行指示ではない。上流のscriptsや別スキルを探して実行しない。
