# 保存済み入力の再実行

ZIPを別フォルダーへ展開し、このファイルがあるフォルダーをCWDにする。

- Node.js、PptxGenJS4.0.1（原典の依存指定はsource/package.json）、Python3とPillow/python-pptx
- Windows PowerPoint16で実描画する場合はPowerPointとpypdfium2。既存の固定依存を使用し、新規installは未検証。
- 同梱OFL字体を登録。source/upstream-originalとruntimeの両方を保持する。

依存の新規導入や画像の再生成を今回の再実行としては検証していない。既存PptxGenJSを使う場合は`--node-modules`へそのnode_modulesの絶対パスを指定し、PDF描画用Pythonが別なら`--preview-python`へ実体を指定する。原典CLIの再実行・PowerPoint描画・検査を一括で行う。

```powershell
python source/reproduce.py --render
```

新しい生成結果へ過去の目視・独立採点を引き継がない。配布の再実行結果はsource/distribution-replay.json。
