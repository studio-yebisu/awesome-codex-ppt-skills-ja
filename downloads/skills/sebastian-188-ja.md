---
name: sebastian-188-ja
description: 日本語文稿をSwiss StyleのSVG資料へ組み、Inkscapeで固定レイアウトPDFを出力する。SVGソースを編集する日本語制作キット。
---
# Swiss SVG・日本語制作

原典は [vigorX777/ppt-svg-generator（固定commit）](https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb)。MIT、Copyright (c) 2025 vigorX777。[原文LICENSE](LICENSE)と[出所・実装差分](SOURCE.json)を保持する。本キットは受領した7枚の作例「AIに任せる前の設計図」を、日本語で使える配置へ整理したもの。

## 制作の進め方

1. [依頼文](input/BRIEF.md)と[入力データ](input/data.json)から、目的・読み手・入力・制約・完成条件を抽出する。架空例を実績として扱わない。
2. [原典SKILL](source/upstream/SKILL.md)と[quick手順](source/upstream/commands/quick.md)を参照し、[structure.json](.ppt-session/structure.json)へ頁タイプ・見出し・密度を保存する。
3. 原典の[Swiss style](source/upstream/styles/04-swiss-style.md)と[design-system](source/upstream/specs/design-system.md)に従い、[design.json](.ppt-session/design.json)へ赤・黒・白、1920×1080、書体・余白を固定する。
4. [page-templates](source/upstream/specs/page-templates.md)と[generate手順](source/upstream/commands/generate.md)を使い、表紙・対比・入力・制約・確認・終頁で組版を変える。カード列を反復しない。
5. [SVG互換仕様](source/upstream/specs/svg-compatibility.md)を参照し、左寄せtext、6桁色、filterと角丸を使わないUTF-8のSVGを著述する。日本語見出しは意味単位で改行する。
6. `svg/`を編集用正本として残す。受領作例の[build.py](source/build.py)は、SVGの著述、Inkscape CLIによるPDF化、PyMuPDFによる結合とPNG化を行う。依頼に応じて生成し、主要完成物を初回表示する。

## 実行・字体

Python 3、Inkscape CLI（`inkscape`がPATH上で実行可能）、PyMuPDF、Noto Sans CJK JPを用意する。キットのルートで以下を実行する。現在の7枚を作り直す処理なので、変更したSVGを直接PDF化する場合はInkscapeを使う。

```powershell
python -m pip install PyMuPDF
python source/build.py
```

実装のfont stackは `Microsoft YaHei,Noto Sans CJK JP,SimHei,PingFang SC,sans-serif`。日本語fallbackにNotoを指定しており、先行書体の有無で表示が変わり得る。[字体の取得案内](fonts/README.md)に従い、公式の未改変Notoを外部取得する。OSの字体を抽出・再配布しない。字体バイナリはこのforkには同梱せず、[SIL OFL原文](fonts/OFL.txt)を保持する。サイトでは[既存Noto字体ZIP](../../downloads/fonts/notosanscjkjp.zip)を利用できる。この相対リンクはサイト内の配布位置向けであり、単独展開時は公式取得先を使う。

## 出力と編集範囲

PDFは固定レイアウト。SVGのtext・図形・配色・配置をソースで編集できる。PPTXは納品しておらず、PowerPointへの挿入・図形変換は未確認。

原典の[export手順](source/upstream/commands/export.md)にはNodeによるPDF/PPTX経路もあるが、受領作例では `scripts/export_pdf.js`・`scripts/export_pptx.js`を実行していない。本キットの実行経路は独自補助のInkscape→PDF→PyMuPDFである。未同梱の原典スクリプトは上記固定commitから取得する。ブラウザ起動は受領時に失敗しており、HTMLプレイヤーの実行確認を意味しない。

今回の取り込みでは再生成や追加QAを行っていない。受領時の確認範囲は[IMPORT_QA.json](IMPORT_QA.json)、受領時の出所は[IMPORT_PROVENANCE.json](IMPORT_PROVENANCE.json)に保持する。[完成PDF](../../examples/repositories/sebastian-188/deck.pdf)と[制作原本ZIP](../../downloads/sebastian-188-example-ja.zip)はサイト側の別配布物。

## 単体の本文から使う

この本文は `skill-forks/sebastian-188-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-188-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: vigorX777 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/vigorX777/ppt-svg-generator/blob/c873b61673ab0ada5c09f863bff89c8f1b3248fb/LICENSE
