# 保存済み入力からの再実行

ZIPを新しい場所へ展開し、このファイルのあるフォルダーをCWDにします。出力を作り直した場合、過去の目視・独立評価は引き継ぎません。

input/data.json と input/patch.json から203操作を組みます。初回の94操作と現在の203操作は異なる版です。保持監査は byte 同一と XML 内容一致を分けます。

- Python3.10+ / python-pptxほか原典requirements
- PowerPoint、元資料と同じOS字体。元資料をinput/donor.pptxへ固定。

Python依存は source/requirements.txt と原典の指定を確認してください。PDF→PNGには pypdfium2、検査記録には pypdf が必要です。生成側の専用PythonとPDF/検査側のPythonが別の場合、後者を明示して実行します。今回の配布検査は既存の固定依存を利用し、新規installはしていません。

```powershell
python source/reproduce.py --render
python source/render_pdf_previews.py render
python source/audit_preservation.py
```

現在版の実再実行範囲は QA.json と source/distribution-replay.json を確認してください。再生成後の全頁確認と必要な原典条件の受入が残ります。OS字体を抽出・同梱しません。
