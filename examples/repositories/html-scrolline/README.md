# 内容の停止点と動きを分け、同じ時間軸を切らずに進めて変化を追えるようにする。

railだけを使い、5月企画→6月会場→7月案内→8月当日を連続して示す。月の間隔を広げて項目名を添え、停止画と自然な移動途中の両方で変化を確かめた。

## 入力と出力

入力：主張ごとの停止点、時刻や項目、使うconceptとmove。作例は写真展の4段階。

出力：原典railの6停止点を持つHTMLと、月・項目付きのレール、自然な遷移の3時点。

## 自分の資料へ使う

1. 原典の6conceptから説明に合うものを選ぶ。railなら日付と項目、停止点ごとの一つの主張を用意する。
2. deck.yamlにbeatの内容、steps、handoffとmoveを書く。動きを本文に埋め込まず、engine/moves/conceptsを変更しない。
3. 原典plan→Vite build→HTTP smokeを実行し、停止点ごとの図・字形・位置を確認する。
4. キー/ホイールと移動途中を確認する。MP4が必要な場合は原典npm run exportを別途実行し、その動画も確認する。

## 実際に使った機能

- 原典CLI plan→Vite build→HTTP smokeを実行。6停止点のerrors/overlaps/clipped/tinyは0。
- engine/moves/conceptsは変更せず、deckのCSSだけで月の実距離を360pxへ広げる。元moveが実座標を読んで同じレールを移動する。
- rail-advanceとera-shiftを元のArrowRightで再生し、前・途中・完了後を保存。日時カウンター・項目ラベル・紙色の変化を示す。

## 未実施と条件

- 原典はrail/data/launch/zoom/canvas/kineticの6conceptとMP4 exportを持つ。今回制作したのはrailだけで、残り5conceptとMP4は未実施。
- 内部localeはenのまま、日本語本文と端末字体を利用。日本語locale機能を実装した作例ではない。
- 原典全体CIのWindowsパス3件不合格は旧実行記録を保持。今回のbuild/smokeと操作検査を、全CI合格へ読み替えない。印刷・縦長mobile・60fpsの定量確認も未実施。

現在の再現コマンドはREPRODUCE.md、原典の条件と日本語での一般手順はSKILL.md、現在の実行・画像hashはQA.json。初回PROMPTの限定検査指示は過去の依頼で、後続修復の範囲はこの記録とsourceのRound4ログを使う。
