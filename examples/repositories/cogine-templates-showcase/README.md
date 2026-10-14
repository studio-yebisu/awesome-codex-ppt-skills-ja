# 香りを、贈る。

[完成template.html](template.html)は、架空の茶の贈りもの企画6枚。商品仕様・価格・効能・売上実績は含まない。茶葉・包み・結びは自作の説明用SVGで、特定商品ではない。

原典cogine-ai/ai-slide-templatesの`editorial-luxury`を選び、folder clone→slot mapping→demo差替えの方式で実制作した。石色の紙面、金の細線、大きな明朝、画像枠、元navigationを保持。8枚のdemoからcover / contents / image-grid / quote / positioning / closingの6版式を使った。[選択と対応](input/template-selection-and-slots.json)に候補比較・content_limits・実DOMを記録。原典JSONにはlayout_slotsがないため、局所DOM mappingとして区別した。

ユーザーは日本語派生と字体変更を承認済み。原典のPlayfair Display/Interを、Shippori Mincho Boldの見出し、Zen Kaku Gothic New Regularの本文、Manropeの英数字へ変更した。日本語の行間だけ調整し、原典のpalette・grid・装飾・navigationは維持した。[公式未改変TTF/OFLと出所](fonts/SOURCE.json)を保持し、HTMLに字体・CSS・SVGをinline化。単独HTMLを外部字体や写真なしで開ける。OS字体は抽出していない。

## 編集と再生成

編集対象はtemplate.htmlの文字・SVG・CSS。[input/content.json](input/content.json)のreplacementsが原典demoの対応表で、[source/build.py](source/build.py)が選択folderをコピーして差し替える。PPTX/PDFは生成していない。

```powershell
python source/build.py --case . --upstream source/upstream
python -m http.server 8000 --bind 127.0.0.1
```

ブラウザで`http://127.0.0.1:8000/template.html`を開く。主制作はPython標準ライブラリとブラウザだけで、npm buildは不要。矢印キー・Space/PageUp/PageDown・ボタン・スワイプで移動、Home/Endで先頭/末尾。原典の元controllerへ0-based同一originのカタログbridgeを追加している。

[source/upstream/](source/upstream/AGENTS.md)は原典AGENTS、INPUT_GUIDE、SKILL、選択template.html/template.json、全template metadataの未変更原本。[局所差分](source/template-local.diff)では字体base64だけを表示用placeholderへ省略し、完全データは完成HTMLと実TTFに保持。[MIT原文](LICENSE)、[SOURCE](SOURCE.json)、[PROVENANCE](PROVENANCE.json)を同梱する。

確認は生成成功、完成HTMLと代表表紙の初回表示、原典navigationの1→2、短い日本語SKILLのquick_validateだけ。代表PNGは最初の2枚を1600×900で出力。[任意の出力補助](source/render_representatives.cjs)はNode/Playwright/Chromeの新しいheadlessブラウザを使う。全頁PNG・全頁詳細検査・optional visual-validator・全kit再実行・採点は実施していない。
