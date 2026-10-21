# 保存済み入力からの再実行

ZIPを新しい場所へ展開し、このファイルのあるフォルダーをCWDにします。出力を作り直した場合、過去の目視・独立評価は引き継ぎません。

実MCP 95操作で制作し、別コピーへ5操作で編集保存を検査します。原典APIと生成後adapterの範囲は source/runtime-adapters.md を参照してください。

- Python3.10+ / mcp1.30.0 / python-pptx1.0.2 / Pillow
- PowerPointとBIZ UDPGothic（非埋込）。PDF→PNGにはpypdfium2。

Python依存は source/requirements.txt と原典の指定を確認してください。PDF→PNGには pypdfium2、検査記録には pypdf が必要です。生成側の専用PythonとPDF/検査側のPythonが別の場合、後者を明示して実行します。今回の配布検査は既存の固定依存を利用し、新規installはしていません。

```powershell
python source/build_mcp.py
python source/check_native_edit.py
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
python source/render_pdf_previews.py render
python source/inspect_current.py
```

現在版の実再実行範囲は QA.json と source/distribution-replay.json を確認してください。再生成後の全頁確認と必要な原典条件の受入が残ります。OS字体を抽出・同梱しません。
