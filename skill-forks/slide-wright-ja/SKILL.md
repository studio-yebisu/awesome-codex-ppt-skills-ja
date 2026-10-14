---
name: slide-wright-ja
description: 独自テーマの日本語Webスライドを原典テンプレートで2枚試作し、同じHTMLへ残りを追加する。既存HTMLの編集にも使う。
---
# slide-wright・日本語制作

原典は[arifszn/slide-wright](https://github.com/arifszn/slide-wright/tree/d95ba204c9e98488b86b76ced75765ab4ec5de96)、固定commit `d95ba204c9e98488b86b76ced75765ab4ec5de96`、[MIT](LICENSE)、©2026 Ariful Alam。[SOURCE](SOURCE.json)と[未変更SKILL](source/upstream/SKILL.md)を保持する。

## 同じ実ファイルを育てる

1. 題材から読み手・密度を判断する。[theme-generation](source/upstream/slide-wright/references/theme-generation.md)と[design-aesthetics](source/upstream/slide-wright/references/design-aesthetics.md)に従い、専用の配色・字体・単一device・motionを決める。既製テーマは使わない。
2. [deck-template](source/upstream/slide-wright/references/deck-template.md)を実使用し、完成資料の実表紙と実contentの2枚を一つのHTMLへ書く。1920×1080、背景section・内部frame、inline CSS、notes、原典CDN5.1.0を保持する。
3. この実ファイルを最初にブラウザで開く。方向が決まったら、最初の2sectionをそのまま保持して残りを同じファイルへappendする。別のpreview HTMLから作り直さない。
4. [motion-recipes](source/upstream/slide-wright/references/motion-recipes.md)に従い、一斉entrance・少数のauto-animate・元controllerで動かす。reduce motionを保持する。

今回の作例では、ユーザーが内部判断で進めることを指定し、親がNight Orbitの方向と進行を指定したため、原典の「previewを出して確認待ちで停止」を追加しなかった。2枚を先に開く核心は実施し、[DESIGN](source/DESIGN.md)へこの変更を記録。ユーザーの美術承認済みとは称さない。別の依頼では、その依頼の確認範囲に従う。

## 編集・再生成

[再生成ガイド](README.md)の`build.py --stage preview`→ブラウザで開く→`--stage append`を使う。実本文は[source/slides-first-two.html](source/slides-first-two.html)と[source/slides-append-four.html](source/slides-append-four.html)、テーマは[source/night-theme.css](source/night-theme.css)。既存資料の変更はそのテーマと元controllerを保持して編集する。

主出力はHTML、編集対象はHTML本文・SVG・CSS・speaker notes。PPTXは生成していない。字体は公式の未改変Dela Gothic One、Zen Kaku Gothic New、Space Groteskをinline化し、[実TTF/OFLと出所](fonts/SOURCE.json)を同梱する。OS字体を抽出しない。エンジンとnotesは固定CDNを使用するためネット接続が必要。

元controllerへ0-based同一origin `yebisu-slide` / `yebisu-page` bridgeだけを加える（[build.py](source/build.py)と[局所差分](source/template-local.diff)）。別controllerへ名前だけ付ける置換はしない。架空イベント案と実測・実績を区別する。

今回の確認は2枚の初回表示と元エンジン稼働、同じHTMLへ6枚までappendした表示のみ。全6枚の詳細検査・独立レビュー・構造監査・ZIP再実行は追加していない。[印刷PDFの原典案内](source/upstream/slide-wright/references/export-pdf.md)も保持するが、作例PDFは未生成。
