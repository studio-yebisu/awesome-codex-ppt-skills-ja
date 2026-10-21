---
name: beamer-ja
description: 原典Warm EditorialのBeamerを日本語教材・数式・TikZ資料に使う。
---

## このスキルでできること

数式・説明・図を同じTeXテーマで組み、全頁と細部の描画を見て重なりを直す。

- 困っている状況: 数式と図を別々に作ると、本文との書式や修正方法がそろわない。
- 必要な入力: 説明する内容・数式・仮定・比較データ
- 受け取るもの: 編集用TeX/TikZとPDF、ページ画像。PPTXではない。
- 必要環境: Beamer・TikZ対応のTeX環境。本例は既存Tectonic0.17 / 同梱JP/数式字体と利用条件 / PDFを180〜220dpi/400〜600dpiで描画する環境
- 作例で試した範囲: 待ち時間の5頁教材を元Beamer/TikZテーマで制作。式と罫線の重なり、順番待ちの途中改行、矢印の浮きを修正し、216dpi全頁と500dpiの6箇所を目視した。
- 制約: この作例は一定処理時間・一定到着間隔の学習用設定。実測値や性能実績ではない。 / 既存Tectonicで2回コンパイル。元XeLaTeX用CLIは未実行で、置換範囲と差分を記録。 / TeXは編集できるが、PowerPoint内のnative図形として配布するものではない。


# 日本語Beamer

原典xukp20/build-beamer-slides `e63b61b140a00596e5260ec7611e42bfde7efb5f` (MIT)。PDFを主成果とし、.texを編集用に渡す。PPTXと称しない。

1. `upstream/styles/warm-editorial/template-169.tex` から構図を作り、`theme.tex` のmacroを直接使う。色・余白・線・数学字体は原典を基本にする。
2. `xeCJK` を読み、Shippori MinchoとZen Kaku Gothic Newの同梱TTF/OFLを相対パスで指定。見出しは明朝、本文はゴシック。
3. 題材の仮定、式、図の意味を定義し、図はTikZ、数式はLaTeXで実装。ユーザーの構図指定を優先。
4. 原典 `references/review-loop.md` と `page-audit-checklist.md` を読む。XeLaTeXを2回、または採用済みTectonicで同じソースを2回compile。エラーと関連overfullを解消し、全変更ページを180〜220dpi、重要な線・ラベル・式を400〜600dpi cropへ描画する。共通theme/font/macroを変えたら全ページを描画する。
5. 全影響ページとcropを元の解像度で目視し、文字のはみ出し、語中改行、式と罫線の接触、余白、各接続線の始終点を確認する。修正後は再compile・再描画し、原典Draft-Ready Gateを満たすまで繰り返す。実施ページ・修正・結果をreviews/へ記録する。ユーザーは独立評価を指定済みなので再質問せず、作者検査後に独立評価へ渡す。独立合格は別記録に残す。
6. .tex/PDF/PNG/入力/依頼/原典とMIT/fontとOFL/ガイドを渡す。TeXエンジン・cacheを含めない。

## quick_validate

`python build.py --tectonic C:/path/to/tectonic.exe` で2回compileした後、全変更PNGと重要cropをpage-audit-checklistで検査する。生成成功だけで完了としない。標準依存がある環境では原典scripts/render_and_check.shも利用できる。実行していない検査・独立評価を完了と記載しない。

## 単体の本文から使う

この本文は `skill-forks/beamer-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/xukp20/build-beamer-slides/tree/e63b61b140a00596e5260ec7611e42bfde7efb5f

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `beamer-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: xukp20 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/xukp20/build-beamer-slides/blob/e63b61b140a00596e5260ec7611e42bfde7efb5f/LICENSE
