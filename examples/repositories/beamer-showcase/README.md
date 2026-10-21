# 待ち時間のしくみ

5枚の日本語Beamer教材。PDFが主出力で、編集は `deck.tex` で行います。PPTXは生成していません。

## 使用した原典

[xukp20/build-beamer-slides](https://github.com/xukp20/build-beamer-slides/tree/e63b61b140a00596e5260ec7611e42bfde7efb5f) / MIT / `e63b61b140a00596e5260ec7611e42bfde7efb5f`。
原典の `styles/warm-editorial/template-169.tex` の表紙構図と `theme.tex` を実際に使用。`WarmFrameHeader`、`WarmFrameFooter`、`WarmBodyText`、`WarmDisplayMath`、`warm/node`、`warm/flow` 等を直接呼び出します。原典は `upstream/` に変更せず保管。

和文用xeCJKと字体指定、墨紺の色だけを `deck.tex` 側に追加。数式と図はLaTeX/TikZのベクトルです。Shippori Minchoの明朝見出し、Zen Kaku Gothic Newの本文。公式配布の未変更TTFとOFLを `fonts/` に同梱し、OSから字体を抽出していません。

原典が使うTeX Gyre Pagella、Heros、Pagella Mathも、[公式GUST](https://www.gust.org.pl/projects/e-foundry/tex-gyre)から取得した未変更OTFとGUST Font License/LPPLを同梱。`font-paths.tex` が原典の欧文字体名を相対ファイルへ結び付けます。`theme-portable.tex` は原典themeの数学字体指定1行だけを、同じPagella Mathのファイルパスへ変更したもの。全macro・幾何・色定義は原典のままで、OSへの字体登録は不要です。

## 再生成

標準XeLaTeX環境ならこのフォルダで次を実行します。

```powershell
xelatex -interaction=nonstopmode -halt-on-error deck.tex
xelatex -interaction=nonstopmode -halt-on-error deck.tex
```

このPCではXeLaTeXコマンドがないため、公式[Tectonic 0.17.0](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0)のXeTeXベースエンジンで同じソースをコンパイルしました。エンジン変更だけで、別の描画方式への代替ではありません。

```powershell
python -m pip install pymupdf
python build.py --tectonic C:/path/to/tectonic.exe
```

Tectonicは初回にTeXパッケージをダウンロードします。字体は同梱を参照します。TeXランタイム、パッケージキャッシュ、OS字体はZIPに含みません。PythonはPNGの作成にだけ使用します。

Windows公式portableの取得例です。公開場所ではなくローカル作業フォルダへ展開してください。

```powershell
Invoke-WebRequest 'https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/tectonic-0.17.0-x86_64-pc-windows-msvc.zip' -OutFile tectonic.zip
Expand-Archive -LiteralPath tectonic.zip -DestinationPath .build/tectonic
python build.py --tectonic .build/tectonic/tectonic.exe
```

## 内容と確認範囲

到着・処理とも一定の学習用モデル。5秒処理・3/4/6秒到着を仮定した算術で、実測値や性能実績ではありません。到着と処理の変動、優先度、複数窓口を含む実系の予測には別のモデルが必要です。

原典review-loopとpage-audit-checklistに沿って2回compile、全5ページ216dpiと重要箇所500dpi cropを描画し、文字・式・罫線・図と接続を目視します。3枚目の3式を独立した位置へ置き、罫線・例文から離しました。4枚目の「順番待ち」は意味の区切りで改行します。実施結果は `reviews/page-audit.json` と `QA.json`。Kimi K3・Opus5.5の独立再評価は技術検査と区別します。

本PCにはxelatexがないため、原典scripts/render_and_check.shそのものは未実行です。同じTeXを既存Tectonicで2回compileし、同じ解像度条件で描画する実行adapterを使います。専用CLIの実行と原典チェックリストの目視実施を混同しません。
