# 再生成

この作例の現在の正本はsource内の入力・CSS・helperです。Node/Pythonと必要な依存・ブラウザーを別途用意します。依存キャッシュは配布に含めません。

source/build.py --stage preview --case . --upstream source/upstreamで2頁を組みます。実ブラウザーで確認してstages.jsonのpreview_openedを更新します。この同梱既存作例の再生成に限り --stage append --existing-deck-repairを使います。新規資料は人間が承認するまで止まり、このフラグを承認の代用にしてはいけません。

全頁を実表示して字体・重なり・頁送りを確認し、実行ログを現在の出力へ束縛して保存します。
