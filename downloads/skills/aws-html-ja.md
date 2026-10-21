---
name: aws-html-ja
description: aws-html-slides原典のPPT conversion extractorとNeon HTML/controller/animationで、既存PPTXを日本語の動くWebスライドへ変換する。
---

## このスキルでできること

既存PPTXの文字と図形を保ち、ブラウザーで順に再生できる資料へ変えられる。

- 困っている状況: 既存PPTXをWebで見せたいが、文字・ノート・図の関係を手で写し直したくない。
- 必要な入力: 変換するPPTX、読み手・用途と、希望する見た目や変更点。
- 受け取るもの: 元資料の内容を抽出したデータと、ブラウザーで発表する動き付きHTML。
- 必要環境: 作例の再生成はPython 3.10+とpython-pptx。保存した入力PPTX、原典extractor、補助SVG化コードを使う。 / 出力は字体を埋め込んだ単独HTML。表示・ページ送りは対応ブラウザーで確認する。
- 作例で試した範囲: 展示案内の自作PPTX5頁を変換。元の文字抽出に、ネイティブ図形のSVG化と15ラベルの中央揃えを補助実装し、Neonのページ送りで表示した。


# 日本語PPTX→動くWebスライド（非公式）

1. 入力PPTXを正本にし、原典upstream/aws-html-slides/SKILL.mdのPPT conversion経路を読む。言語/style/編集範囲が指定済みなら再質問しない。本例は日本語・Neon派生・HTML/SVG編集。
2. 元scripts/extract-pptx.pyを実行し、文字/画像/notes/順序を保持。原典gen-content.pyは新規制作専用で、変換ではStep4/5を飛ばす。勝手に新内容を補わない。
3. Native形状が入力の意味を担う場合は実OOXMLのgeometry/path/色を別JSONへ補助抽出。元情報をSVGとして保全し、動きの順序を役割に合わせて加える。
4. 元Neon previewのcontroller/FXとviewport-base.css全文、100vh/100dvh・clamp・height breakpoints・reduce motionを保持。SVGはfixed viewBoxで縮尺。多ページをgeneric rendererへ置き換えない。
5. 最小のsame-origin player adapterは別diffへ記録。AWS非公式の展示案にAWSlogo/著作権主体を持ち込まず、明示の派生footerへ置換。本例はStudio Yebisu表示、元MITは保持。
6. 原典extractと実画面のページ送りを確認。文字・図の対応に問題があれば出力だけの配置変更を記録する。本例は2・3枚目の15ラベルを図形の中心に揃えた。元座標と新anchorはexample/source/svg-label-alignment.jsonを参照。技術検査と独立評価は分け、未確認範囲もQAに残す。HTML/SVG編集とPPTX入力保全を区別する。

example/rebuild.py、input/deck.pptx、extraction/、source/*.svgが具体例。source/controller.diffに局所変更。書体は元TTF/OFLを添付し、fontをsingle HTMLへembedしてoffline再生。

原典 https://github.com/lanceli93/aws-html-slides 、MIT ©2025 Zara Zhang。固定pinとAkxan由来の入力出所はSOURCE.json。AWS/原作者の公認・提携ではない。

## 原典の検査を省かない

- 入力PPTXを保存し、原典extract-pptx.pyで文字・画像・notesを抽出する
- 図形が意味を持つ入力はOOXMLのgeometryと色を別に記録する
- 元Neon controllerへ固定viewBoxのSVGを載せる
- 必要な出力だけの配置変更をadapterへ記録する
- 元PPTXの全頁描画と変換後を比べ、頁移動・ラベル・番号を確認する

- ネイティブ図形のSVG化と中央揃えは作例の補助実装で、原典extractor単体の機能ではない
- 入力PPTXは無改変。変換後2・3頁の15ラベルだけx/anchorを変更
- この入力に画像と講稿はなく、それらの抽出を実証した例ではない
- HTML/SVG編集用。新しい編集可能PPTXは出力しない
- AWS/原作者との公認・提携ではない

原典の必須工程と、実施できなかった対人確認・実機条件を分けて記録する。再生成後に古いQA合格を引き継がない。作例の現在の検査記録はexample/QA.json。

ページ送り・日本語の操作案内・再表示時の動きはsource/controller.diffの局所差分。

## 単体の本文から使う

この本文は `skill-forks/aws-html-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/lanceli93/aws-html-slides/tree/5ae3d68b66277e8a0d0b6ceea479a4b5117f16b2

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `aws-html-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: lanceli93 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/lanceli93/aws-html-slides/blob/5ae3d68b66277e8a0d0b6ceea479a4b5117f16b2/LICENSE
