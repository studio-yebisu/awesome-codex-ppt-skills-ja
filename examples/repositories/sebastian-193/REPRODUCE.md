# 再実行

ZIPを空の作業フォルダーへ展開し、このファイルのあるフォルダーで実行する。新しい生成物には以前の目視確認・独立評価を引き継がない。

- Node / PptxGenJS4.0.1、Python、原典QAと保持XMLを含む一式ZIP。
- 公式BIZ UDPGothic、PowerPoint、PowerShell 7。PDF由来RGBプレビューにはpypdfium2。

Node依存は `source/package.json` の固定版を使う。新しい環境では `npm install --prefix source --ignore-scripts --no-audit --no-fund` で用意する。既存環境では再インストール不要。

```powershell
node source/build.cjs
python source/preserve_master.py  # 原典の構造化ツールで8頁のグループと接続線も作る
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
python source/render_pdf_previews.py render
python source/upstream/scripts/qa_pptx.py deck.pptx --profile group-meeting --report source/qa-report.json
python source/upstream/scripts/verify_final_qa.py deck.pptx source/qa-report.json --require-profile group-meeting
```

PowerPointの処理は指定した資料だけを読み取り専用で開く。PDFをPowerPointから出力し、そのPDFから表示用RGB PNGを作る。OSのフォントファイルは抽出・再配布しない。同梱フォントは各OFLを確認して導入する。

現在の検査・限界は `QA.json` と `PROVENANCE.json`。厳密な画像一致、学術内容の査読、利用者の承認を自動検査の成功だけから主張しない。

8頁の編集確認を再現する場合は `pwsh -NoProfile -File source/verify-group-edit.ps1 -CaseDirectory .` を実行する。これは別コピーを作り、箱を動かして保存・再表示する。既存の完成資料は変更しない。
