# 現在版の再生成と検証

Node/npm、原典lock。Windowsの検査には環境変数YEBISU_NPM_CLIとYEBISU_CHROMIUMで既存のnpm CLIとChrome/Edgeを指定する。段階を編集する実体はapp内のTSX。distはbuild結果。

作例ZIPを展開したルートから実行する。既存依存を利用した配布再実行の実績はsource/round4-zip-replay.json。新しい環境の依存導入成功とは区別する。

```text
cd app
npm ci
npm run build
node --experimental-strip-types scripts/windows-verify.mjs
node --experimental-strip-types scripts/windows-inspect-presentation.mjs book-exchange --width 1440 --height 900
```

元のreproduce/一括ラッパーは初回制作時の固定原稿を再生成する旧経路。現在の修復版には上記の正本を使う。再生成後のQAは、全頁と個別動作を確認するまで未確認として扱う。ローカル検査は独立Kimi/Opus評価や人間の採用判断とは別。
