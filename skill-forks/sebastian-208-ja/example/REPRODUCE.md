# 保存済み画像とノートの再包装

ZIPを別フォルダーへ展開し、このファイルがあるフォルダーをCWDにする。

- Node.jsとPptxGenJS4.0.1（source/package-lock.json）、Python3とPillow/python-pptx。
- 実描画にはWindows PowerPoint16、PDF→PNGにはpypdfium2。既存依存を使用し、新規installは未検証。
- 新規頁画像の制作にはbuilt-in image_gen。保存済み頁の再包装に画像生成・OCRは不要。

```powershell
python source/reproduce.py --node <nodeの実体> --node-modules <既存node_modules> --render --preview-python <pypdfium2のあるPython>
```

新規installは今回の再実行に含めない。原典の未改変package_image_pptx_with_notes.mjsでimage_pages/とNOTES.mdを包装し、PowerPoint16でPDFへ出力してRGB PNGを作り、verify_current.pyで画像byte hash・一頁一画像・ノートを検査する。画像生成・OCRや紙面の描き直しは行わない。PPTXの日時と画像の絶対出典パスは展開先で変わるため、配布再実行では幾何・画像bytes・ノートと全頁PNGを比較する。結果はsource/distribution-replay.json。新しい生成へ過去の目視や独立評価を引き継がない。
