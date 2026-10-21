# 保存済み入力からの再実行

ZIPを新しい場所へ展開し、このファイルのあるフォルダーをCWDにします。出力を作り直した場合、過去の目視・独立評価は引き継ぎません。

計画検査→native制作→PowerPoint描画→原典presenterを実行します。HTML QAはNode.jsと既存Chrome/Edgeを使い、HTTP用互換版の差分を source/qa_http.patch に保存しています。

- Python3.10+ / python-pptx / PowerPoint16とYu Gothic（今回の描画）
- HTMLの検査にはNode22+とChromeまたはEdge。HTTPで表示。

Python依存は source/requirements.txt と原典の指定を確認してください。PDF→PNGには pypdfium2、検査記録には pypdf が必要です。生成側の専用PythonとPDF/検査側のPythonが別の場合、後者を明示して実行します。今回の配布検査は既存の固定依存を利用し、新規installはしていません。

```powershell
python source/reproduce.py
python source/qa.py --node <absolute-node-path>
python source/inspect_current.py
```

現在版の実再実行範囲は QA.json と source/distribution-replay.json を確認してください。再生成後の全頁確認と必要な原典条件の受入が残ります。OS字体を抽出・同梱しません。
