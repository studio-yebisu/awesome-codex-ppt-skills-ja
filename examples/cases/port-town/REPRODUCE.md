# 現在版の再生成と検証

Node/Playwrightと既存Edge。index.htmlは完成した単体資料。7頁の本文はsource/business_web_content.py、メモと局所日本語化はsource/port_locale_notes.py。HTML編集後に元validatorの原本結果と日本語期待値差分を区別して再検証する。

作例ZIPを展開したルートから実行する。既存依存を利用した配布再実行の実績はsource/round4-zip-replay.json。新しい環境の依存導入成功とは区別する。

```text
node source/validate-presenter-ja.mjs index.html
node source/round4_pages_proof.cjs
node source/round4_presenter_proof.cjs
```

元のreproduce/一括ラッパーは初回制作時の固定原稿を再生成する旧経路。現在の修復版には上記の正本を使う。再生成後のQAは、全頁と個別動作を確認するまで未確認として扱う。ローカル検査は独立Kimi/Opus評価や人間の採用判断とは別。
