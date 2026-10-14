# 小さな展示を、ひとつの体験に。

仮想の展示企画5枚。日時・会場・参加条件は未定。4週前・3週前・1週前・当日は開場日から逆算した仮の工程で、実績ではありません。

## 原典を使った方法

[Akxan/ppt-agent-skill](https://github.com/Akxan/ppt-agent-skill/tree/01825dee2ad40a8c719824252605396b9a570d57) / MIT / `01825dee2ad40a8c719824252605396b9a570d57`。
26作風から実在する `bauhaus_block` を選択。原典 `ppt-output/style-gallery/bauhaus_block.html` のCSS、紙色・赤/青/黄・巨大sans・硬い幾何・厳格gridを使用し、日本語展示の本文と局所CSSを追加しました。元style.jsonは `input/style.json`。未変更原本は `upstream/`、局所差分は `source/*.diff`。

原典 `html_packager.py` でWebプレビューを作成し、`html2svg.py` のPuppeteer/dom-to-svg、`svg2pptx.py` のnative OOXML形状生成を実行。原典文書には「SVG画像を形状へ変換」の説明もありますが、このpinの実コードはSVGの文字・円・四角・線・pathをnative PowerPoint形状へ直接解析します。完成PPTXの文字と形状はそのまま編集できます。native chart/table/数式は使用していません。

Windowsのfile URL、UTF8、依存bundle/cache置き場、字体ロード待ちを局所adapterで対応。原典DOM routeに失敗したときのPDF/画像代替は無効化し、失敗を報告します。汎用レンダラーやartifact-tool SDKは使用していません。

Web packagerは、各ページへ同じ字体を5回base64化する代わりに同梱 `fonts/` へ相対参照する局所adapterを適用。`preview.html` はfontsフォルダと一緒に保持してください。画像素材の原典inline処理は保っています。

## 閲覧と編集

- `deck.pptx`：PowerPointで文字をクリックして編集。図形の色・大きさ・位置も編集可能。関連する部品は複数の形状として配置されています。
- `render/deck.pdf`、`render/slide-*.png`：PowerPoint16の実描画による閲覧用。
- `preview.html`：原典packagerによるブラウザの翻ページプレビュー。HTMLを編集する場合は `slides/slide-*.html` を使用。
- `svg/`：原典DOM-to-SVG出力。文字はtext要素を保ったvectorです。

見出しはZen Kaku Gothic New Black、短い本文はBIZ UDPMincho、英数字はManrope。公式未変更TTFとOFLを同梱。OS字体・Office字体の抽出はありません。PowerPoint表示用にこれらをWindowsへ登録してください（字体を右クリックしてインストール）。HTMLは同梱字体を参照します。

## 再生成

Node.js24以降、Python3.12、Chrome、PowerPoint16（PNG/PDF出力時）が必要です。依存・Chrome本体・bundle/cacheはZIPに含めません。

```powershell
$env:PUPPETEER_SKIP_DOWNLOAD='true'
npm install --ignore-scripts
python -m pip install -r requirements.txt
python source/build.py --node C:/path/to/node.exe --chrome 'C:/Program Files/Google/Chrome/Application/chrome.exe'
powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
```

原典のOSS生成器と未変更原本、差分、入力・依頼・原稿、字体許諾を同梱。Puppeteer/dom-to-svg/esbuildは各packageのMIT/Apache等を `dependencies/` に保存。Python依存の個別許諾も保持。共有PowerPoint ApplicationをQuitせず、自分が開いたdeckのみCloseします。

## 確認範囲

原典packager/DOM-to-SVG/native PPTXの成功、PowerPoint16で5枚PNG/PDF生成、代表完成物の初回表示まで。ユーザー指定により全ページ詳細目視、独立レビュー、構造監査、ZIP再実行は実施していません。今回は固定のカード数と追加interview/承認待ちを適用せず、計画を入力へ記録して制作しました。
