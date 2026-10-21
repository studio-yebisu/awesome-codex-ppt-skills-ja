---
name: ppt-design-system-ja
description: 原典ppt-design-systemのテンプレート・配色・レイアウトで日本語HTML資料を制作する。Forest Inkの実作例と再現入力を参考に、参加案内や説明資料を作るときに使う。
---

## このスキルでできること

見出し・数値・問い・比較を、同じ配色と文字の規則で揃えられる。

- 困っている状況: ページごとに色や文字を選ぶと、見出し・説明・補足の役割がぶれる。
- 必要な入力: 資料の原稿・目的・読み手と、希望するスタイル。
- 受け取るもの: 配色と文字の階層を揃え、内容に合う版式と原典のナビゲーションを持つHTML資料。
- 必要環境: source/reproduce.pyによるHTML生成はPython 3標準ライブラリー。 / 任意の実描画検査はNode.js 22+と既存Chrome/Edge、ローカルHTTP。閲覧端末に日本語字体が必要。
- 作例で試した範囲: 架空の図書館イベント案内6頁にForest Inkと原典レイアウトを適用し、原典ナビゲーションを持つHTMLを作った。


# 原典デザインシステムで日本語資料を作る

Studio Yebisuの日本語派生版。原作者の公式日本語版ではありません。

まずupstream/SKILL.md、upstream/references/themes.md、upstream/references/layouts.mdを読む。原典assets/template.htmlとナビゲーションを使い、目的に合う配色とレイアウトを選ぶ。共通のカタログ用rendererへ置き換えない。

## 読み手に役立つ原稿へ

- 図書館の参加案内なら、日時・受付・会場・持ち物と、案内が変更されたときの次の行動を示す。実在の情報は主催者の情報で確認する。
- 図書館イベントの実例は架空の設定。時刻・会場をそのまま実際の案内に転用しない。
- 原典のcover、cards、body、question、comparison、closingを使い分ける。比較する行動が同じ重要度なら、片側だけを薄くして読みにくくしない。
- 日本語の見出しを意味の区切りで改行し、単位と数字を保つ。游明朝・游ゴシック等の端末書体を確認する。OSのフォントファイルを取り出して配布しない。

## 実例から制作する

references/WORKFLOW.mdの入力・原典・制作条件を読む。配布キットのinput/data.jsonと本文HTMLを自分の内容へ替え、原典テンプレートで全ページを作る。再現入口はsource/reproduce.pyで、原典のHTML生成CLIではなく、この派生版の原稿配置用プログラムである。

今回確認したのは6ページ・Forest InkのHTML経路。原典のキー・dot・横スクロールを保持する。localhost HTTPで全ページの文字、切れ、ナビゲーションを確認し、再生成は新たにレビューする。他テーマ・PPTX・印刷・縦画面を対応確認済みと表示しない。

## 個別条件を保持する

原典MITの通知をupstream/LICENSEに保持する。カタログのCC0を上流へ適用しない。自動検査を人による正式採用や外部公開へ読み替えない。

## 原典の検査を省かない

- 原典themes.mdから5配色の一つを選ぶ
- input/data.jsonに日時・会場・持ち物と頁の役割を書く
- layoutの数値カード・大きな問い・並列比較を内容で選ぶ
- python source/reproduce.pyで原典templateへ差し込む
- 全頁のP0/P1項目と元ナビゲーションを実画面で確認する

- 作例はHTMLのみでPPTX laneは未実施
- 原典テンプレートのJavaScriptを無改変で保持
- 游明朝・游ゴシック等の端末書体に依存。OS書体は配布しない
- 10種の全レイアウトや他4配色を実演した例ではない

原典の必須工程と、実施できなかった対人確認・実機条件を分けて記録する。再生成後に古いQA合格を引き継がない。作例の現在の検査記録はexample/QA.json。

## 単体の本文から使う

この本文は `skill-forks/ppt-design-system-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/att6113/ppt-design-system/tree/9f39af607ab82da2827530c38b9dc86eb75768ee

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `ppt-design-system-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: att6113 / 原典条件: MIT（原典。通知同梱）。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/LICENSE
