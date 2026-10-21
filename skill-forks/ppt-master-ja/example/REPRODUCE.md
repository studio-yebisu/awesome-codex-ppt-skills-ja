# 固定例の再実行

空の場所へZIPを展開し、このファイルのあるフォルダーから実行する。Windows PowerPoint、PowerShell、Python（python-pptx/lxml/Pillow/pywin32/numpy/PyMuPDF）、PDFium、Node.jsとplaywright1.62.1/Chromium、BIZ UDPGothic Regular/Boldが必要。`fonts/`のOFLを保持する。PPTX字体は埋め込まない。

```powershell
python source/reproduce.py --preview-python C:/path/to/pdfium/python.exe
```

PDFiumも同じPythonにあればflagを省く。元PPT Masterは`source/upstream`に保持する。`PPT_MASTER_PATH`で同じ固定版を指定する場合は既定の取得先を置き換えるだけで、異なる版を混ぜない。SVG描画のNode依存はsource/package.json。既存依存は`--node-modules C:/path/to/node_modules`で指定できる。この機械での検証は既存依存のみを再利用し、新規導入はしていない。

処理はguard→P05後early→元calculator2回→final→native変換→実PowerPoint測定→文字枠幅の補正→再測定→実PP/PDF→RGB描画→SVG描画/比較→内容・字体・座標の照合→私的コピーの文字編集/保存/再表示。PowerPointアプリQuitは呼ばず自分が開いた資料だけを閉じる。

`export_with_biz.py`はBIZ familyを元の東アジア字体集合へメモリー内登録する。`fit_text_frames.py`は文字・字号・基線・色を保ち、実測で不足する幅だけを補う。原典のchecker/変換器は無変更。原典postflightは補正前のcompiler出力、最終PPTXの照合はcurrent-check-receiptsとlayout-overflowへ分離する。

固定の8頁を専用コードから再現する。任意の新しい原稿をinput/data.jsonだけで変換する汎用器ではない。新題材は一般SKILLのrouteと原典資料で新規に制作する。原典の主担当による全頁手書き、init/import、全Default工程を実証したとは扱わない。再生成直後はQAを要目視へ戻し、前版の目視・独立評価を継承しない。
