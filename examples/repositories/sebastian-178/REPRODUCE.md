# 現在版の再生成と検証

Python/fontTools/Brotli、Git Bash、既存Chrome/Edge。Windows差分はsource/windows-scriptsとwindows-bin。YEBISU_PYTHONとCHROME_BINを指定する。生成はsource/build.pyが正本。

作例ZIPを展開したルートから実行する。既存依存を利用した配布再実行の実績はsource/round4-zip-replay.json。新しい環境の依存導入成功とは区別する。

```text
python source/build.py
bash source/windows-scripts/check-deck-quality.sh source/index.html
bash source/windows-scripts/check-deck-contrast.sh source/index.html
bash source/windows-scripts/check-deck-fit.sh source/index.html
bash source/windows-scripts/render.sh source/index.html replay-output --package --pdf --png
```

元のreproduce/一括ラッパーは初回制作時の固定原稿を再生成する旧経路。現在の修復版には上記の正本を使う。再生成後のQAは、全頁と個別動作を確認するまで未確認として扱う。ローカル検査は独立Kimi/Opus評価や人間の採用判断とは別。
