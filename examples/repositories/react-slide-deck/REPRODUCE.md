# 現在版の再生成と検証

Node/npm、既存Chrome/Edge。編集の正本はsource/appのApp.tsxとCSS。distをHTTPで表示する。原典SlideLayout/useSlideScale/variantsを使い、週切替は作例の独自操作。

作例ZIPを展開したルートから実行する。既存依存を利用した配布再実行の実績はsource/round4-zip-replay.json。新しい環境の依存導入成功とは区別する。

```text
cd source/app
npm ci
npm run build
```

元のreproduce/一括ラッパーは初回制作時の固定原稿を再生成する旧経路。現在の修復版には上記の正本を使う。再生成後のQAは、全頁と個別動作を確認するまで未確認として扱う。ローカル検査は独立Kimi/Opus評価や人間の採用判断とは別。
