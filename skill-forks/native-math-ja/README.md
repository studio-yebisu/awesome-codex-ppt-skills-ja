# 平均の、その先。

中高生・学び直し向け5分教材、全5枚。仮想得点A=[4,5,6], B=[0,5,10]。調査結果ではありません。

## 原典の実行方法

[Noi1r/powerpoint-skill](https://github.com/Noi1r/powerpoint-skill/tree/a39cd8cfba332741a96d52bebd2bb378b638364e) / MIT / `a39cd8cfba332741a96d52bebd2bb378b638364e`。
原典 `references/themes.md` のSandwich JSON、スライドmasters、`sTitle` / `addTable` / `addChart` / `addMathText` を実際に使用。原典JavaScript helper全文を取り出し、Sandwich themeと日本語字体に変更。未変更原本は `upstream/`、抽出原文は `source/original-helpers.cjs`、変更は `source/helpers.diff`。

1. 原典 `render_latex.py` で `render:omml` 数式のmanifestを作成（画像化もTeX環境も不要）。
2. PptxGenJSでnative図形・表・グラフと数式placeholderを生成。
3. 原典 `inject_omml.py` を実行。PandocがLaTeX数式をDOCXのOMMLへ変換し、原典がPPTXへ注入。
4. PowerPoint16でPNG/PDFを実描画。LibreOfficeではOMML数式が欠けるという原典の制限があるため、完成プレビューに使いません。

## 数式の編集

`deck.pptx` をMicrosoft PowerPointで開き、数式の文字をクリックしてカーソルを入れます。「数式」タブから分数・平方根・添字を編集できます。数式は画像ではありません。本文・図形・nativeグラフ・表も編集できます。グラフは右クリック「データの編集」で値を変更。PDF/PNGは閲覧用で、編集はPPTXを使用してください。

欧文数字はManrope、和文明朝はShippori Mincho、本文はBIZ UDPGothic。公式未変更TTF/OFLのみ同梱し、OS字体を抽出していません。OMMLの数学字体はOfficeの実行時字体を使用し、Office字体は同梱しません。

## 再生成

Node.js、Python3、公式[Pandoc](https://pandoc.org/installing.html)、PowerPoint16（プレビュー生成用）が必要です。

```powershell
npm install
python -m pip install -r requirements.txt
python source/build.py --node C:/path/to/node.exe --pandoc C:/path/to/pandoc.exe
powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
```

Pandoc3.12.1公式portable取得例（バイナリはキットに含めません）：

```powershell
Invoke-WebRequest 'https://github.com/jgm/pandoc/releases/download/3.12.1/pandoc-3.12.1-windows-x86_64.zip' -OutFile pandoc.zip
Expand-Archive -LiteralPath pandoc.zip -DestinationPath .build/pandoc
```

原典injectorはPandoc→DOCX方式。MathML変換XSLやOffice付属XSLの参照・抽出・同梱はありません。PandocはGPL-2.0-or-laterの外部実行依存で、同梱はCOPYRIGHT説明のみ。PptxGenJS4.0.1はMIT、lxml6.1.3の個別許諾も `dependencies/` に保持。

## 確認範囲

原典JS生成と数式注入の成功、数式placeholder残存なし、PowerPoint16のPNG/PDF出力、代表完成物の初回表示まで。ユーザー指定により全ページ詳細目視、独立レビュー、全PPTX構造監査、ZIP再実行は未実施。分散は全3件を全体としたn分母。不偏分散（n−1）はこの教材の計算に使っていません。
