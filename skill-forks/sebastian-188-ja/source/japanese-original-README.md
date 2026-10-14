# AIに任せる前の設計図

日本語の制作依頼を書く、7頁の架空例集。Swissの赤・黒・白で、目的／読み手／入力／制約／完成条件を具体化します。

- 完成資料：deck.pdf（7頁・ベクターPDF）
- 原典方式の正本：svg/ の1920×1080 SVG（text・図形をソースで編集可）
- 閲覧：index.html（ページ送り、矢印キー、5秒再生、フルスクリーン）
- PNG：render/（実PDFの描画）
- 制作入力：input/BRIEF.md、input/data.json、PROMPT.txt
- 日本語派生：SKILL.md
- 再生成：Python 3 + Inkscape + PyMuPDF + Noto Sans CJK JP、`python source/build.py`

原典 [https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb](https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb)、commit c873b61673ab0ada5c09f863bff89c8f1b3248fb。MIT / Copyright (c) 2025 vigorX777。

原典のMarkdown→構成→style→作者SVGという方式を使い、Swissの大色面・巨大活字・対比分割を日本語へ調整。上流export scriptは実行せず、既存InkscapeでPDFを書き出しました。Playwright/Chromiumの起動は環境のsocket権限制限で失敗したため代替しました。HTMLプレイヤーは独自追加です。

PDFは固定レイアウト、SVGはソース編集。PowerPointでの個別要素変換は未確認。特定AIの性能・料金は主張していません。フォントは環境のNoto Sans CJK JPを使用、ファイルは再配布していません。原配布元：https://github.com/notofonts/noto-cjk （SIL OFL）。
