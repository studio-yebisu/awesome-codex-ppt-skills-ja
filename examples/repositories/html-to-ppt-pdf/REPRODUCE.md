# 週末の汐見港町 ― HTMLからPPTX・PDFへの変換・再現キット

Python3、Node.js22以上とnpm、初回依存・公式Chromium取得のネット接続が必要です。

1. ZIPを展開してPowerShellを開く。
2. `.\reproduce\Reproduce.ps1` を実行。既存HTML7ページを再撮影し、画像PPTXとPDFへ変換します。
3. 出力は `reproduce/workspace/examples/repositories/html-to-ppt-pdf/`。新出力のQAは確認前です。
4. `-Render` を追加するとWindows / Microsoft PowerPoint / PowerShell7で実描画を確認します。必要なら `-NodePath "Node.jsの実行ファイルの絶対パス"` を指定します。

既存Guizang HTMLを、無改変の原典build.mjsでPNG・画像PPTX・PDFへ変換する。原文HTMLとAGPL対応ソースを保持し、export.htmlだけでdotからの移動をforce:trueへ補正する。原典の短い撮影間隔と700ms待ちの競合によるページ重複を、全ページと一意なPNGで確認する。日本語発表ノートの後処理は本文画像とスライドXMLを保持する。本文編集・motion保持・新規資料構成の生成ではない。MIT変換器、AGPL入力ソース、OFL書体を区別する。

このキットは既存の7ページを変換する再現用経路です。異なる資料には原典SKILLと日本語派生版から入力HTML・ページ数・静止状態を確認し、すべてのページを比較してください。入力HTML自体の再制作はsource/reproduce-input.pyと対応ソースを参照。初期の重複ソース試行はローカルに保存し、配布には使用中の対応ソースだけを含めています。
