# 保存済み入力からの再実行

ZIPを新しい場所へ展開し、このファイルのあるフォルダーをCWDにします。出力を作り直した場合、過去の目視・独立評価は引き継ぎません。

現在の再実行は run-repair-r4 の受入済み worker manifest を原典 finalize で統合します。新規入力の再構成ではなく、新しい worker・画像生成・OCR は実行しません。旧 run/run-repair は初回や前版の履歴です。

- Python3.10+と原典editppt CLIの固定依存（PyMuPDF/python-pptx等）
- 新規入力には頁worker対応エージェントと選択した画像backend。保存済み結果の再統合は画像生成不要。
- 今回の描画はWindows PowerPoint/Yu Gothic/Arial Narrow、同梱BIZ UDPGothic Bold。

Python依存は source/requirements.txt と原典の指定を確認してください。PDF→PNGには pypdfium2、検査記録には pypdf が必要です。生成側の専用PythonとPDF/検査側のPythonが別の場合、後者を明示して実行します。今回の配布検査は既存の固定依存を利用し、新規installはしていません。

```powershell
python source/reproduce.py
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
python source/render_pdf_previews.py render
python source/verify_editability.py --render
python source/render_pdf_previews.py qa/editability/render
python source/inspect_current.py
```

現在版の実再実行範囲は QA.json と source/distribution-replay.json を確認してください。再生成後の全頁確認と必要な原典条件の受入が残ります。OS字体を抽出・同梱しません。
