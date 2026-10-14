# 文字のかたちを、観察する。

日本語6頁の手描き風Webスライド。[index.html](index.html)だけで、ネット接続なしに開けます。←/→・↑/↓・Space・Home/End・swipeと下部ボタンで操作します。原典demoのgo()は先頭・末尾で止まる契約を保持しています。

原典: Watermelon4000/sketch-note-ppt、commit `0729098c28a2105b3e2f6225b3afe125e3959fb6`、MIT ©2026 Watermelon4000。原典が規定する手書き風HTML authoring routeを使い、元CSS全文、吹き出し・波線下線・二重枠・ハーフトーン・crosshatch、decision-tree、元JS controllerとSKILLのreveal CSSを内包しています。原典は生成CLIやnpmを要求せず、AIが原稿を直接HTMLへ組む方式です。

編集は[source/slides.html](source/slides.html)、[adaptation.css](source/adaptation.css)、[controller.js](source/controller.js)で行います。単一HTMLへ再梱包するにはPython 3の標準ライブラリで `python source/rebuild.py` を実行します。画像化で文字を固定せず、公式字体で実際の日本語を描画します。PPTXは生成していません。

原典は[source/upstream/](source/upstream/)へ未変更保存。CSSを上書きせず、和文font、clampの大きな文字、左右の誌面構成、手描きSVGの線描き、reduced-motionは局所CSSに分離しました。原典の遠隔字体を、固定Google Fonts由来のZen Maru Gothic/BIZ UDPGothic/Manropeへ置換しています。原文OFLと実TTFは[source/fonts/](source/fonts/)、hashとpinは[FONT-SOURCE.json](source/FONT-SOURCE.json)。字体は未改変、OS抽出なしです。

同一originの親から0-based `{type:'yebisu-slide', index:N}` を受け、元go()のあと `{type:'yebisu-page', index:N}` を返す小adapterだけ追加しました。`source/controller.patch`に差分を保持。file://で単独表示する場合は親通知を送りません。親サイト統合の動作はここでは確認していません。

内容は自作の観察教材です。書体と声の対応は選択案で、効果・読了率・学習効果等の実測はありません。図は自作のinline SVGと原典CSSの編集記号です。第三者写真・生成画像・ロゴは使っていません。

確認はHTML組立成功、Chromeで表紙と字体比較の初回表示、ArrowRightで1/6から2/6への移動、page errorなし。代表PNG2枚を表示しました。残り全頁の詳細目視・独立レビュー・構造監査・ZIP再実行は未実施です。[QA](QA.json)に確認範囲を保存しています。
