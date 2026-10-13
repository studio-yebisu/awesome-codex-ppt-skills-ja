# 制作JSON

`assets/example.json` が実行できる入力例。`scripts/render-deck.mjs` のvalidatorも参照する。

デッキには `id`（英小文字・数字・ハイフン）、`title`、`font`、`background`、`ink`、`slides` を指定。
各ページは `title`、`notes`、`duration`（秒）、`nodes` を持つ。キャンバスは1280×720。
ノードは `text` / `rect` / `circle` / `line` / `path`。座標とサイズはpx、色は16進カラー。
`text` は `x,y,text,size,weight` を指定。`y` はベースライン。改行は `\n`、`leading` は行送り。
`rect` は `x,y,w,h,fill`。`circle` は `x,y,r,fill`。線は `x,y,x2,y2,stroke,strokeWidth`。
`path` はSVG pathの `d`。追加HTMLや外部スクリプトをJSONへ入れない。
`delay` は出現を遅らせるミリ秒。`font` と `anchor`（start / middle / end）はテキスト単位で指定できる。

SVGとHTMLを生成：

```text
node <このスキル>/scripts/render-deck.mjs <入力JSON> <新しい出力フォルダ>
```

Node.js 22以上を推奨。ライブラリやアカウント、APIキーは不要。
HTMLをブラウザで開き、左右キー・自動再生・講稿を確認する。SVGはベクトル編集アプリで開ける。
出力フォルダがすでにある場合、CLIは上書きせず停止する。新しいフォルダを指定する。
Webフォントは別配布。このパッケージではフォント本体を同梱しない。OFL配布元のNoto / BIZ UDを使用する。

編集可能PPTXが必要な場合は `scripts/export-pptx.mjs` を使う。
スキルフォルダで `npm install --ignore-scripts` した後、
`node <このスキル>/scripts/export-pptx.mjs <入力JSON> <新しいファイル.pptx>` を実行する。
PptxGenJSを使用し、文字・図形・線はネイティブオブジェクト、自由形状pathはSVG画像として収録する。
自由形状はPowerPointでポイント編集できる図形ではない。表・chartはこの簡易CLIでは扱わず、必要に応じて別のネイティブ制作系を使う。
フォントは埋め込まず、閲覧先のフォントで表示する。日本語フォントを用意し、PowerPointで最終表示を確認する。
