# 読み手が決めることから逆算し、主張と根拠を工程・比較表・判断図へ整理する。

数値の根拠がない箇所は、工程図・比較表・判断の分岐を選んだ。判断図には接続線を入れ、小テストは3欄の幅をそろえ、日本語を句のまとまりで読めるようにした。

## 入力と出力

入力：読者の判断、答え、根拠となる原稿・データ。作例は動画を教材へ組み替える架空の7頁。

出力：原典runtime付きHTML7頁、単体package、PNG/PDF、Golden Path検査記録。

## 自分の資料へ使う

1. 読者が何を決めるかを先に定め、答えと根拠を分けて書く。分からない数値を作らない。
2. 原典content-to-exhibit-routerから、比較には表、順序には工程図、理由には関係図を選ぶ。
3. 1600×900の原典starterと6層CSS、元runtimeを保ち、source/build.pyで本文と日本語字体を生成する。
4. Golden Pathのquality→contrast→fit→renderを実行し、単体packageと全頁PNG/PDFを確認する。Windows差分はパス変換だけに限定する。

## 実際に使った機能

- 原典starter、6層CSS、原典runtime.jsをそのまま使用し、親との接続だけ局所bridgeへ分離。
- 日本語入力と公式字体subsetから7頁を生成し、quality/contrast/fit/renderの原典4工程をWindowsのパス差分だけで再実行。
- 実際のpackage出力から全7 PNG/PDFを更新。判断図の分岐、3欄の本文、24pxの表見出しを確認。

## 未実施と条件

- 架空の企画。学習効果・制作時間・収益の実績は含まない。原典のroot LICENSEとSKILLの記載不一致は解消していない。
- 原典runtimeを置き換えた初期実装は旧履歴。現在は元runtimeと局所catalog bridgeを使用。
- 日本語用CSSは原典CSSの後に追加。新しい原稿では同じ4検査と全頁の実描画をやり直す。

現在の再現コマンドはREPRODUCE.md、原典の条件と日本語での一般手順はSKILL.md、現在の実行・画像hashはQA.json。初回PROMPTの限定検査指示は過去の依頼で、後続修復の範囲はこの記録とsourceのRound4ログを使う。
