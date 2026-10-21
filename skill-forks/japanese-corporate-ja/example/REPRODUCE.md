# 再実行

ZIPを空のフォルダーへ展開し、このファイルのあるフォルダーで実行する。新しい生成物へ過去の目視確認や独立評価は引き継がない。

必要なものはPython、python-pptx/lxml/Pillow、元15型PPTX一式、Windows PowerPointとPowerShell。BIZ系・Calibri・MS Gothicが使える環境を用意する。PDF由来RGBプレビューにはpypdfium2、実PDF字体の読取りにはPyMuPDF。

```powershell
python source/rebuild.py
powershell -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
python source/render_pdf_previews.py render
python source/check_native.py
powershell -NoProfile -File source/check_overflow.ps1
python source/check_pdf_fonts.py
powershell -NoProfile -File source/check_edit_reopen.ps1
```

各コマンドが失敗したら次へ進まず原因を修正する。現在の生成器は`source/rebuild.py`。初回制作の保存コード`source/build_japanese_repository_examples.py`は再生成の入口ではない。

PowerPoint処理は自分が開いた資料だけを閉じ、アプリのQuitを呼ばない。編集確認は`.private/edit-reopen/`内のコピーを使い、正本のdeck.pptxを変更しない。PDF出力をRGB PNGへ変換し、元の直接PNGも`render/direct-png/`へ保つ。OS字体は抽出・再配布しない。

全頁の実画像、contact、矢印・表・数値・出所・頁番号を実サイズで読む。JTC17/20の独立受理と利用者採用は別の工程。現在の技術検査は`QA.json`、両ZIPからの実再生成と全12頁RGB比較は`source/distribution-replay.json`。依存の新規導入や別PCでの互換性は今回の検査外。
