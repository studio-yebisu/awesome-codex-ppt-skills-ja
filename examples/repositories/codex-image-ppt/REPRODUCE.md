# 保存済み入力からの再実行

ZIPを新しい場所へ展開し、このファイルのあるフォルダーをCWDにします。出力を作り直した場合、過去の目視・独立評価は引き継ぎません。

保存済み画像3枚を原典 assemble で再出力します。新たな画像生成・worker 分担・人間承認を行う入口ではありません。

- Python3.10+ / python-pptx、原典assemble
- 新しい画像生成にはbuilt-in画像編集とworker対応エージェント。保存済み画像の再出力は新規生成不要。

Python依存は source/requirements.txt と原典の指定を確認してください。PDF→PNGには pypdfium2、検査記録には pypdf が必要です。生成側の専用PythonとPDF/検査側のPythonが別の場合、後者を明示して実行します。今回の配布検査は既存の固定依存を利用し、新規installはしていません。

```powershell
python source/reproduce.py
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath codex-image-ppt.pptx -OutputDirectory render
python source/render_pdf_previews.py render
python source/inspect_current.py
```

現在版の実再実行範囲は QA.json と source/distribution-replay.json を確認してください。再生成後の全頁確認と必要な原典条件の受入が残ります。OS字体を抽出・同梱しません。
