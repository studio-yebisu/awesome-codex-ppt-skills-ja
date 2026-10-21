# 保存済み入力からの再実行

ZIPを新しい場所へ展開し、このファイルのあるフォルダーをCWDにします。出力を作り直した場合、過去の目視・独立評価は引き継ぎません。

Build Mode の実行です。再生成で acceptance の状態は OPEN へ戻り、全頁の視覚確認が必要です。R7 の人間承認を自動で取得したことにはなりません。

- Python3.10+ / pptx-designer1.0.0b11 / python-pptx1.0.2
- PowerPoint、公式Shippori Mincho/BIZ UDPGothic。原典task toolsはsource/upstream/。

Python依存は source/requirements.txt と原典の指定を確認してください。PDF→PNGには pypdfium2、検査記録には pypdf が必要です。生成側の専用PythonとPDF/検査側のPythonが別の場合、後者を明示して実行します。今回の配布検査は既存の固定依存を利用し、新規installはしていません。

```powershell
python source/build_ppt_design_repository_example.py --upstream source/upstream --input input/data.json --output-dir . --render
python source/render_pdf_previews.py render
python source/inspect_current.py
```

現在版の実再実行範囲は QA.json と source/distribution-replay.json を確認してください。再生成後の全頁確認と必要な原典条件の受入が残ります。OS字体を抽出・同梱しません。
