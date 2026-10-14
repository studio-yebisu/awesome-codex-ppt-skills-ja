---
name: swiss-svg-ja
description: 日本語文稿からSwiss Styleの1920×1080 SVG資料を制作する。
---
# Swiss SVG・日本語制作

原典は [vigorX777/ppt-svg-generator](https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb)、MIT / Copyright (c) 2025 vigorX777。本作例は原典の作者workflowを日本語へ調整した派生です。

1. Markdown文稿を読み、目的・読み手・入力・制約・完成条件を抽出。実績と架空例を区別する。
2. `.ppt-session/structure.json` に頁タイプ・見出し・密度を保存。
3. 原典 `styles/04-swiss-style.md` を読み、`.ppt-session/design.json` に赤・黒・白、1920×1080、書体・余白を固定。
4. 原典 `specs/page-templates.md` を参照し、封面・対比・入力・制約・確認・終頁の組版を使い分ける。カード列を繰り返さない。
5. 左寄せtextのstyle、6桁色、無filter、無角丸、UTF-8でSVGを著述。日本語の意味単位で見出しを改行。Microsoft YaHei優先、Noto Sans CJK JPを日本語fallbackに追加。
6. 正本SVGを残し、必要なら自作 `source/build.py` で既存Inkscape→PDF、PyMuPDF→PNGを出力する。初回主要出力を確認する。

## 必要参照と実行
同梱source/upstreamにはSKILL、commands/quick・generate・export、specs、Swiss style、LICENSEを保持。本文だけではこれらは取得できません。一式ZIPか上の固定URLを使ってください。

実行：Python 3、Inkscape CLI、PyMuPDF、Noto Sans CJK JPを用意し、`python source/build.py`。

## 編集性・限界
SVGのtext/図形はソース編集可。PDFは固定レイアウト。PowerPointへの挿入・形状変換は実機未検証。native要素のPPTXは納品していません。ブラウザのフォントfallbackで見た目が変わる場合があります。
