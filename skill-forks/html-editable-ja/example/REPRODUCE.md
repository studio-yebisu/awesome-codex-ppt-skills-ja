# 保存済みHTMLの再変換

作例rootをCWDにする。Pythonはupstream/requirements.txtの既存依存とPlaywright Chromiumがあるものを使う。PDF→PNG用のPythonが別ならその実体を明示する。

```powershell
python convert_local_fonts.py index.audited.html --out deck.pptx --keep-screenshots --no-embed-fonts
pwsh -NoProfile -File render_current.ps1 -PresentationPath deck.pptx -OutputDirectory render
pwsh -NoProfile -File test_native_edit.ps1 -PresentationPath deck.pptx -OutputDirectory qa/editability
python render_pdf_previews.py render
python render_pdf_previews.py qa/editability --pdf-name native-text-edited.pdf --single-output native-text-edited.png
python render_pdf_previews.py qa/editability --pdf-name native-flag-edited.pdf --single-output native-flag-edited.png
```

変換の原典コードは未改変。local-font/native-flag/flat-effect/no-quit/audit-labelのadapterは同梱コードとQAに明記。新規install・字体埋込みの成功・新しいHTMLの全工程へ検査を広げたとは扱わない。再生成後は全頁を読み、新しい出力へ過去の目視や独立評価を移さない。
