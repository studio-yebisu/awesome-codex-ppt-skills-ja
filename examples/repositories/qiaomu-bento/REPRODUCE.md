# 現在版の再生成と検証

Python/fontTools/Brotli。現在のdeck.json、input/source.bento.htmlの同一ID、同梱standalone shellから別出力を作る。既存ファイルへ上書きしない。独立コピーは元CLIの--new-documentを使う。同じIDのコピーは既存ブラウザー状態の影響を受ける場合がある。

作例ZIPを展開したルートから実行する。既存依存を利用した配布再実行の実績はsource/round4-zip-replay.json。新しい環境の依存導入成功とは区別する。

```text
python source/rebuild_bento.py --output-dir new-output
```

元のreproduce/一括ラッパーは初回制作時の固定原稿を再生成する旧経路。現在の修復版には上記の正本を使う。再生成後のQAは、全頁と個別動作を確認するまで未確認として扱う。ローカル検査は独立Kimi/Opus評価や人間の採用判断とは別。
