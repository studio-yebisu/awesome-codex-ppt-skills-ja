# 花を、一本から。

架空の花の定期便サービスの提供案、5枚。価格・配送地域・販売条件・花の選択範囲は未確定です。実際の営業案内や導入実績ではありません。

原典LearnDeckのHTML-to-PPTモードを実行しました。元html_to_ppt.jsがhtml_to_editable_pptx.jsを呼び、Chromiumでsource.htmlのDOM座標を測定。PptxGenJSでnative文字・rectangle/ellipse等を組み、SVGを個別PNG画像へ変換して配置します。花のSVGはdeck-assets/svg/に残ります。全文の一枚画像へはしていません。

PPTXの文字、背景、丸、帯、花器、棚、区切り線は編集可能。花のpetal/stemは個別PNG画像で、native PowerPoint shapeではありません。元SVGとHTMLは編集可能です。原典converterは一つの--font-faceへ全て固定するため、本作例のruntime/だけcomputed fontFamilyを拾ってDela/Shippori/BIZを保存する局所変更とja-JP metadataを追加しました。未変更の原本はupstream/、変更点はPROVENANCE.jsonです。

再変換: Node18+にplaywright/pptxgenjs/sharp/jszipを用意し、Chromiumを入れて `node runtime/scripts/html_to_ppt.js --input source.html --out-dir . --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720`。Codexではload_workspace_dependenciesのNodeとNODE_PATHを使えます。HTML/CSSはsource.html内、依頼文はPROMPT.md、原データはinput/data.jsonです。

原作者LearnAIHubC、使用pinはSOURCE.json。原典MITをLICENSE.txtに保持。非公式の日本語作例です。Google Fontsの未改変TTFと原文OFLをfonts/へ同梱。PPTXはフォント未埋込なので別端末ではこれらの書体を手動導入してください。Windows fontsから抽出していません。

今回の修正はHTMLとPowerPointの全頁描画・目視、DOM文字とnative要素の照合まで実施。独立再評価とZIP再実行は別記録です。index.htmlはPowerPoint表示のPNGプレビューです。HTMLとPowerPointの文字組みが完全に一致する保証ではありません。

## 今回の修正と確認

元HTMLの表紙字間を-6pxから+10pxへ、2頁本文を下へ48px移して見出し下に33.21875pxの余白を確保しました。3頁の小さな表示は黒へ変更。元SVG抽出は表示幅/高さを保存しないため花が縦へ伸びていたので、実DOMのSVG viewportを保存する局所補正を加えました。source/html_to_editable_pptx.js.diffに元との全差分を保存しています。

元SKILLは追加検査を既定省略しますが、今回はユーザーの明示した修正・検証依頼に基づき、同じsource.htmlを元DOM converterで再変換しました。HTML全5頁とPowerPoint全5頁を作者が目視。source/html-dom-metrics.json、native-object-inventory.json、layout-conversion-audit.jsonと2組の同頁比較PNGを保存。文字36要素、基本図形8、花SVG由来の個別画像6を全頁で確認しています。PPTXは花をnative図形に変換したものではありません。

原典Generate PPT経路（slides.json→5styleプリセット）はこの作例では未実施。radial背景近似・影の近似・CSS filter無視などの原典制約があり、ChromeとPowerPointの字形・改行の完全一致は保証しません。元SKILLに専用の必須検証CLIはありません。今回の検査を元にないgateとして偽装しません。独立Kimi K3/Opus5.5再評価とZIP再実行は未了です。

## 3頁の読みやすさの修復

小さいラベル・脚注・頁番号をクリーム色へ変更し、赤地を少し暗くしてコントラスト4.5:1以上にしました。元HTML→原典DOM converter→native PPTX→実PowerPoint描画を再実行し、HTML/PPTX全5頁を確認しています。source/footer-repair.jsonが現在の記録です。
