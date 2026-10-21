---
name: beamer-ja
description: 原典Warm EditorialのBeamerを日本語教材・数式・TikZ資料に使う。
---

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
