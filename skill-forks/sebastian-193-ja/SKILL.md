---
name: scholar-ppt-cn-ja
description: 原典のテンプレートとPptxGenJS作者方式で、仮説・方法・評価を編集可能な日本語研究発表にする。
---

# 公共空間サイン研究資料の日本語派生スキル

原典：https://github.com/deathcats4/scholar-ppt-cn/tree/6fca3dc0f0fd6033279cc1bd29467967cc185272
MIT。原典のRoute B、Template DNA、PptxGenJS作者方式を採用する。原典の専用生成スクリプトを必須とする方式ではない。

1. 入力を読み、実施済の結果と計画を区別する。未実施の仮説を成果と書かない。
2. 同梱defaultテンプレートから16:9、白背景、濃青024C98・1D5EA7、明快なタイトル階層を抽出する。原典master1とtheme1をネイティブ保全する。著者・組織・見本データ・ロゴは資料へ流用しない。
3. 研究内容に応じて表紙、行動フロー、仮説比較、平面図、仕様注釈、観察経路、条件図、改善循環を組む。同じカードを繰り返さない。
4. 日本語の見出し・本文・図形を編集可能なPptxGenJS要素にする。話者ノートを独立して置く。日本語書体はNoto Sans CJK JP。環境の書体を使い、OS書体を抽出して同梱しない。
5. node source/build.cjs、python source/preserve_master.pyを順に実行する。
6. 完成PPTXを利用可能なレンダラーで初回描画し、主要表示と明白な欠けを確認する。自作最小検査で8頁、ノート、文字、native master保全を確かめる。

変更：この日本語派生では原典の巨大なQA手順・QAスクリプトを実行せず、最小検査と初回描画へ置換した。原典全QA合格を意味しない。完成物の実際のレンダラー・制約はPROVENANCE.jsonを見る。

日本語SKILL本文だけに原典コードは含まれない。一式ZIPには入力・作者生成コード・defaultテンプレート・MIT LICENSE・必要な原典参照を含む。

## 作例の書体を揃える

Noto Sans CJK JPのRegular/Boldは、サイトの「作例の書体を取得」から公式配布物とOFL原文を取得できる。原稿とPPTXに指定したフォント名を揃える。Noto Sans JPとは名前が異なる。OSの書体は抽出せず、作成者と受け手の端末に公式フォントを導入する。

固定配布元: https://github.com/notofonts/noto-cjk/tree/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/OTF/Japanese
