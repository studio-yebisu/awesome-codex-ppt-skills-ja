---
name: learndeck-ja
description: LearnDeck原典のHTML-to-PPT DOM実測converterで、日本語HTMLからnative文字と図形・個別SVG画像を持つPPTXを作る。
---

# LearnDeck 日本語版（非公式）

1. 題材、枚数、確定事項と提供案を短く整理。style指定があれば再質問せず従う。各ページに一つの主張を置き、巨大見出しと役割のある図をHTML .slideで作る。
2. 同梱upstream/SKILL.mdを必要範囲で読む。新規計画は原典generate_ppt.jsも使える。本作例は柔軟な日本語bold構図のためHTML-to-PPT modeを使う。
3. local runtime/scripts/html_to_ppt.jsで変換する。ChromiumのDOM位置が正本。playwright/pptxgenjs/sharp/jszipを用意し、Codexではload_workspace_dependenciesのNode/NODE_PATHを使う。
4. 原典は既定で追加検査を省略するが、明示された修正・検証依頼では元HTMLを直して同じconverterを再実行する。HTMLとPowerPointを全頁描画して字間・改行・余白を目視し、native要素とSVG由来PNGの分離を記録する。
5. Native text/background/rect/ellipseと、SVG由来の個別PNG imageを区別して伝える。SVG元と実TTF/OFL、原MIT、source.htmlを保全。PPTXフォント未埋込時は別端末への導入が必要と説明する。

本forkのruntimeだけ、原典converterの単一font-face固定をcomputed fontFamilyで置換し、roleごとの日本語書体を保存。languageはja-JP。未変更原本はupstream/scripts。SVG書き出し時は実DOMのviewport幅・高さを保存し、SVGのpreserveAspectRatioをPNGへ反映する局所補正も適用。その他のDOM/native object/gradient pipelineは原典のまま。

具体例と入力はexample/に同梱。`node runtime/scripts/html_to_ppt.js --input example/source.html --out-dir output --name deck --no-preview --font-face "BIZ UDPGothic" --viewport-width 1280 --viewport-height 720`。画像をnative shapeと称さず、提供案を実績と称さない。

原作者LearnAIHubC。https://github.com/LearnAIHubC/LearnDeck 。MIT帰属はLICENSE.txt、使用pinはSOURCE.json。書体は各OFL。公式・原作者の公認ではありません。

元Generate PPT（slides.jsonから5styleへ生成）はこの作例では未実施。radial背景・影は近似、CSS filterは無視されます。元HTMLとPPTXの完全一致は保証せず、花の内部はnative図形ではありません。修正時はsource.htmlが正本で、元DOM変換→全頁の実描画→要素照合の順で確認し、source/*.diffとQAへ結果を残します。

小さいラベル・脚注・頁番号は背景と4.5:1以上のコントラストを確保する。今回の3頁はクリーム色の文字と少し暗くした朱赤で4.561:1。原典DOM変換後のHTMLとPowerPointの両方を実描画して確認する。
