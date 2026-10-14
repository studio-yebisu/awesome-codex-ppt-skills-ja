---
name: cogine-templates-ja
description: Cogine AIの原典metadataから一つのHTMLテンプレートを選び、folder clone・slot mapping・demo差替えで日本語スライドを作る。
---
# Cogine AIテンプレート・日本語制作

原典は[cogine-ai/ai-slide-templates（固定commit）](https://github.com/cogine-ai/ai-slide-templates/tree/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb)、`8a7a59d39f059a7e58da9c3471014ba7fe3b98eb`、[MIT](https://github.com/cogine-ai/ai-slide-templates/blob/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/LICENSE)、©2026 Cogine AI。[SOURCE.json](SOURCE.json)に実使用と差分を記録する。

## MDだけを取得した場合

このMDだけではtemplateやコードは揃わない。一式の[日本語キットZIP](../../downloads/cogine-templates-ja.zip)から、`source/upstream/`の原典・`input/`の対応表・`source/build.py`・`source/japanese-fonts.css`・`assets/`のSVG・`fonts/`の実TTF/OFLを取得する。この相対リンクは配布サイト用。単独MDから原典を取得する場合は以下の固定URLを使い、選択folder内のtemplate.html/template.jsonを一緒にコピーする。

- [AGENTS.md](https://github.com/cogine-ai/ai-slide-templates/blob/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/AGENTS.md)：原典の契約。
- [INPUT_GUIDE.md](https://github.com/cogine-ai/ai-slide-templates/blob/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/INPUT_GUIDE.md)：依頼と原稿の整理。
- [全template folder](https://github.com/cogine-ai/ai-slide-templates/tree/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/templates)：各template.jsonで選ぶ。
- [今回のmetadata](https://github.com/cogine-ai/ai-slide-templates/blob/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/templates/editorial-luxury/template.json)と[今回のtemplate.html](https://github.com/cogine-ai/ai-slide-templates/blob/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/templates/editorial-luxury/template.html)：実版式・palette・装飾・元navigation。
- [原典SKILL](https://github.com/cogine-ai/ai-slide-templates/blob/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/skills/ai-slide-templates/SKILL.md)：原典の手順。

## 制作の要点

1. 原典[AGENTS](source/upstream/AGENTS.md)を読み、必要なら[INPUT_GUIDE](source/upstream/INPUT_GUIDE.md)で目的・読み手・原稿・禁止する主張を整理する。
2. 各template.jsonのscheme/formality/density/layouts/content_limits/best_for/avoid_for/mood/toneを比較し、一つを選ぶ。中央の索引だけで選ばない。
3. 選択folderを出力へ丸ごとコピーしてtemplate.htmlとtemplate.jsonを揃える。layout_slotsがあれば対応を保存する。未定義なら実HTMLのDOM領域から作る局所mappingであると明記する。
4. demoの見出し・本文・数字・引用・画像を差し替える。容量を超える場合は近い版式を複製し、元palette/grid/spacing/装飾/controllerを保持する。別builderへ名前だけ付ける置換はしない。
5. 完成HTMLをブラウザで開き、主要初回表示と宣言されたnavigationを確認する。

作例は[選択とslot mapping](input/template-selection-and-slots.json)の通り`editorial-luxury`を6枚へ調整。原典content_limitsは見出し34字・本文360字・bullet3・card4、推奨6〜10枚。layout_slotsは原典に未定義。cover/contents/image-grid/quote/positioning/closingの実版式を使い、茶葉・包み・結びのSVGを原典画像枠へ入れる。

## 日本語差分と編集性

原典は字体の保持を要求するが、今回ユーザーは日本語派生と字体変更を承認済み。Shippori Minchoの見出し、Zen Kaku Gothic Newの本文、Manropeの英数字へ役割を保って変更し、日本語行間を調整した。palette・major grid・装飾・navigationは保持する。これは今回の派生条件であり、他の依頼へ無条件に一般化しない。[公式字体/OFL](fonts/SOURCE.json)と[局所差分](source/template-local.diff)を保持し、OS字体を抽出しない。

主出力は単独HTML。編集はHTML本文・SVG・CSSと[構造化入力](input/content.json)。PPTX/PDFは生成していない。[再生成方法](README.md)は標準Pythonでfolder cloneと差替えを行う。CSS・字体・SVGをinline化するため外部写真や字体サービスは不要。

ユーザー指定により、今回の確認は主要初回表示・原典navigation1→2・必要生成・この短いSKILLのquick_validateに限定。optional visual-validator、全頁詳細検査、全kit再実行、採点は追加しない。架空の企画と商品仕様・効能・実績を区別する。
