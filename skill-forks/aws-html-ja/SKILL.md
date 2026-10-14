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
6. 元buildと主要完成物/ページ送りの初回表示だけ確認。全詳細目視・構造監査・独立review・ZIP再実行を追加しない。HTML/SVG編集とPPTX入力保全を区別する。

example/rebuild.py、input/deck.pptx、extraction/、source/*.svgが具体例。source/controller.diffに局所変更。書体は元TTF/OFLを添付し、fontをsingle HTMLへembedしてoffline再生。

原典 https://github.com/lanceli93/aws-html-slides 、MIT ©2025 Zara Zhang。固定pinとAkxan由来の入力出所はSOURCE.json。AWS/原作者の公認・提携ではない。
