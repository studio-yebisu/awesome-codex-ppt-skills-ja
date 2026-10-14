---
name: ppt-design-system-ja
description: 原典ppt-design-systemのテンプレート・配色・レイアウトで日本語HTML資料を制作する。Forest Inkの実作例と再現入力を参考に、参加案内や説明資料を作るときに使う。
---

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

## 単体の本文から使う

この本文は `skill-forks/ppt-design-system-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/att6113/ppt-design-system/tree/9f39af607ab82da2827530c38b9dc86eb75768ee

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `ppt-design-system-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: att6113 / 原典条件: MIT（原典。通知同梱）。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/att6113/ppt-design-system/blob/9f39af607ab82da2827530c38b9dc86eb75768ee/LICENSE
