# 作例の再実行

このファイルのあるフォルダーで、Python3.10以上・python-pptx/Pillow、Windows版PowerPoint、PowerShellを使います。書体はfonts/のTTFを導入しOFLを保持します。新規依存installは今回検証していません。

```powershell
python rebuild.py
pwsh -NoProfile -File runtime/export_case.ps1 -PresentationPath deck.pptx -OutputDirectory render
python source/check_quality.py
```

原典の複製・export・overflow・stale scanを実行します。Tolerance40は原典の値を維持。技術検査後は全頁と一覧を実際に読み、別版へ以前の目視や独立評価を移さないでください。実論文の抽出を行う入口ではなく、保存したMarkdown/JSONからの再生成です。
