# 再実行

ZIPを空の作業フォルダーへ展開し、このファイルのあるフォルダーで実行する。新しい生成物には以前の目視確認・独立評価を引き継がない。

- Python / python-pptx、原典テンプレートを含む一式ZIP。
- 公式BIZ UDPGothicとPowerPoint等の実描画環境。PDF由来RGBプレビューにはpypdfium2。

```powershell
python source/build_deck.py
python source/upstream/scripts/scan_ppt_text.py deck.pptx
powershell -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
python source/render_pdf_previews.py render
```

PowerPointの処理は指定した資料だけを読み取り専用で開く。PDFをPowerPointから出力し、そのPDFから表示用RGB PNGを作る。OSのフォントファイルは抽出・再配布しない。同梱フォントは各OFLを確認して導入する。

現在の検査・限界は `QA.json` と `PROVENANCE.json`。厳密な画像一致、学術内容の査読、利用者の承認を自動検査の成功だけから主張しない。
