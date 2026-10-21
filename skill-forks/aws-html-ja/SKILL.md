---
name: aws-html-ja
description: aws-html-slides原典のPPT conversion extractorとNeon HTML/controller/animationで、既存PPTXを日本語の動くWebスライドへ変換する。
---

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
