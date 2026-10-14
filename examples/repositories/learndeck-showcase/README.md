# 花を、一本から。

架空の花の定期便サービスの提供案、5枚。価格・配送地域・販売条件・花の選択範囲は未確定です。実際の営業案内や導入実績ではありません。

原典LearnDeckのHTML-to-PPTモードを実行しました。元html_to_ppt.jsがhtml_to_editable_pptx.jsを呼び、Chromiumでsource.htmlのDOM座標を測定。PptxGenJSでnative文字・rectangle/ellipse等を組み、SVGを個別PNG画像へ変換して配置します。花のSVGはdeck-assets/svg/に残ります。全文の一枚画像へはしていません。

PPTXの文字、背景、丸、帯、花器、棚、区切り線は編集可能。花のpetal/stemは個別PNG画像で、native PowerPoint shapeではありません。元SVGとHTMLは編集可能です。原典converterは一つの--font-faceへ全て固定するため、本作例のruntime/だけcomputed fontFamilyを拾ってDela/Shippori/BIZを保存する局所変更とja-JP metadataを追加しました。未変更の原本はupstream/、変更点はPROVENANCE.jsonです。

再変換: Node18+にplaywright/pptxgenjs/sharp/jszipを用意し、Chromiumを入れて `node runtime/scripts/html_to_ppt.js --input source.html --out-dir . --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720`。Codexではload_workspace_dependenciesのNodeとNODE_PATHを使えます。HTML/CSSはsource.html内、依頼文はPROMPT.md、原データはinput/data.jsonです。

原作者LearnAIHubC、使用pinはSOURCE.json。原典MITをLICENSE.txtに保持。非公式の日本語作例です。Google Fontsの未改変TTFと原文OFLをfonts/へ同梱。PPTXはフォント未埋込なので別端末ではこれらの書体を手動導入してください。Windows fontsから抽出していません。

原典--no-previewで追加QAを省略。完成PPTXをPowerPointで一度PNG/PDFへ書き出し、主な完成物を初回表示する範囲です。全ページ詳細目視・構造監査・ZIP再実行は行いません。index.htmlはPowerPoint表示のPNGプレビューです。HTMLとPowerPointの文字組みが完全に一致する保証ではありません。
