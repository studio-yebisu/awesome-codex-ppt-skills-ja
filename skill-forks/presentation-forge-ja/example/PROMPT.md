# 再制作の指示

一枚ずつ編集した本文と話す講稿を、発表者画面付きHTMLへまとめる。

入力: 原稿、頁ごとのHTML、発表者用の講稿、テーマ。
出力: 素材と字体を内包したHTML6枚。原典の発表者画面で現在頁・次頁・講稿を確認できる。

1. 新規資料はnew_deck.pyで作る。既存ブランドからのtheme作成では原典のimport-theme手順を使い、完成themeを.pfstyle.jsonへpackして引き渡す。再利用はunpackする。
2. 1ファイル1section.slideに分け、本文と話す説明・進行合図をaside.notesへ書く。見た目はthemeへ置き、motionはnone/subtle/balanced/lively/extraから選ぶ。engineは変えない。
3. 原典build.pyでCSS・JS・字体・素材を単独index.htmlへまとめる。
4. ブラウザーが使える場合は原典check_deck.pyを必ず実行し、問題を直してcontact sheetと全頁を見る。
5. Pキーで現在頁・次頁・講稿を確認する。編集保存や実機接続は実行できた範囲だけを記録する。

同梱作例の実施範囲: 未変更の原典check_deck --slides allで6頁・問題0。全6実PNGを目視。Pキーで現在4頁・次5頁・4頁の新しい話す説明と進行合図が一致することを確認。

制約: 未変更の原典engine/builderを使用。日本語の字体・改行と末尾の同一origin bridgeは局所差分。
制約: 今回Pキーの発表者画面と講稿の一致をheadlessで実確認。実機プロジェクター、手動通し稽古、保存編集は未確認。
制約: HTML出力。native PPTXは生成しない。
制約: 今回は既存obsidianテーマとbalancedを使用。theme import、.pfstyle.jsonのpack/unpack、5段階motionの比較は未実証。
