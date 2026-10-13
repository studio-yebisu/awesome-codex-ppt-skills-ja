# wangzan101/html-to-ppt-pdfの日本語制作

原典: https://github.com/wangzan101/html-to-ppt-pdf/tree/0ce6f66815fc0c0f6de9c976856213a952dfafe6

原典build.mjsでHTMLを7枚のPNGにしてPPTX・PDFへ梱包

既存Guizang HTMLを、無改変の原典build.mjsでPNG・画像PPTX・PDFへ変換する。原文HTMLとAGPL対応ソースを保持し、export.htmlだけでdotからの移動をforce:trueへ補正する。原典の短い撮影間隔と700ms待ちの競合によるページ重複を、全ページと一意なPNGで確認する。日本語発表ノートの後処理は本文画像とスライドXMLを保持する。本文編集・motion保持・新規資料構成の生成ではない。MIT変換器、AGPL入力ソース、OFL書体を区別する。

## 作例

- 週末の汐見港町 ― HTMLからPPTX・PDFへ / 7枚 / pptx
- カタログ内の案内: repository.html?repo=wangzan101/html-to-ppt-pdf
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=wangzan101/html-to-ppt-pdf
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3（再現ラッパー）
- Node.js 22+ / npm / Playwright Chromium
- 初回の依存取得にネット接続
- Microsoft PowerPointとPowerShell 7（任意のネイティブ描画確認）

## 元の制作コマンド

    python source/reproduce.py --powerpoint

    python source/reproduce-input.py

## 確認範囲

- 各ページは画像1枚。PPTXの本文・図表を個別編集できない。
- PDFもラスタ画像。検索可能な文字・ベクトルPDFではない。
- 動きやブラウザの操作UIは静止画像になる。
- 既存HTMLからの変換例であり、新しい資料構成の生成ではない。
- 原文直入力の初回では2ページ目が重複したため、入力側の操作互換処理を同梱。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
