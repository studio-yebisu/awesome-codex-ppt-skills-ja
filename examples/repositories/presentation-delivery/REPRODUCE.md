# 再実行

ZIPを空の作業フォルダーへ展開し、このファイルのあるフォルダーで実行する。新しい生成物には以前の目視確認・独立評価を引き継がない。

- Python、Node22以上、固定Node依存とChromium。
- PPTX確認にはWindows / PowerPoint / PowerShellと公式BIZ UDPGothic。PDF由来RGBプレビューにはpypdfium2。

Node 22以上とnpmが必要。通常コマンドは `source/runtime/package-lock.json` から依存とChromiumを設定する。既に同じ固定依存とChromiumがある環境では `--reuse-existing-dependencies` を付けると設定処理を省く。Node実体が標準PATHにない場合は `--node C:/path/to/node.exe` を付ける。表示入口は `python -m http.server 8000` の後 `http://127.0.0.1:8000/index.html`。HTMLが正本でPPTXはbest-effort派生。

```powershell
python source/reproduce.py --powerpoint
python source/render_pdf_previews.py render
```

PowerPointの処理は指定した資料だけを読み取り専用で開く。PDFをPowerPointから出力し、そのPDFから表示用RGB PNGを作る。OSのフォントファイルは抽出・再配布しない。同梱フォントは各OFLを確認して導入する。

現在の検査・限界は `QA.json` と `PROVENANCE.json`。厳密な画像一致、学術内容の査読、利用者の承認を自動検査の成功だけから主張しない。

比較画像は現行HTMLを再captureした後、`python source/build_comparisons.py`で再生成する。review/comparison-sources/に左右の元PNGを保存し、比較PNGと全元画像のSHAをreview/html-pptx-comparisons.jsonへ記録する。
