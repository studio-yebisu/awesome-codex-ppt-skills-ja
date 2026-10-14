# 五つの点から、一本の線を。

初学者向け6枚・約5分の小教材。単位のない合成5点を実計算した。傾き0.8、切片1.4、残差二乗和3.6（丸め表示）。現実の観測値・研究成果・予測精度は示していない。

主出力は原典Quarto renderがembed-resources/self-contained-mathで生成したindex.html。字体、SVG、Reveal runtime、KaTeXをHTMLへ含む。完成HTMLをブラウザで開き、→キーで次へ、←キーで前へ。本文・数式・表・コードはtalk.qmd、図はinput/data.csvとsource/compute_fit.py、字体と微調整はsource/japanese.scss/fonts.htmlから編集する。PPTXは生成していない。

## 再生成

Python3へNumPy/Matplotlibを公式配布から用意する（今回NumPy2.5.4/Matplotlib3.11.2）。Quartoは公式portable1.9.38を取得して展開しbinをPATHへ。ZIPは140363520bytes、SHA256 `3dd3b22616dcae65f710b1d6c019b818027312c8cbf54a0a08fdd9842346375e`。

[公式Windows portable1.9.38](https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.38/quarto-1.9.38-win.zip) / [公式取得案内](https://quarto.org/docs/download/) / 詳細source/QUARTO-CLI.json。CLI本体は制作ZIPに入れない。

展開した制作キットのルートで:

```powershell
python source/compute_fit.py
quarto render talk.qmd
```

または `python source/build.py --case . --quarto quarto`（既存入力からrenderのみ）。原典拡張0.4.1はQuarto>=1.4を要求する。repository内では `python tools/build_quarto_talks_showcase.py --prepare --quarto <quarto.cmd絶対パス>` が公式字体receipt・原本から準備して実計算/renderまで行う。

## 原典との関係

source/upstreamのtemplate.qmd、_extensions、SKILL、LICENSEは固定commitの未変更原本。実制作は同じ拡張/元SCSS/semantic classes。source/local.diffにQMD差分、追加font/bridgeを記録。16–24枚既定を依頼の6枚へ変更。自動タイトルを避けpagetitleにし、最初の教材ページへ題名と表を置く。表示コードは元templateと同じ普通のPython fenced blockで、同じ計算をcompute_fit.pyから実行した。Quartoのノートブック実行とは称さない。

原典Reveal APIへの小さなsame-origin bridgeだけを追加。yebisu-slide/index=0..5をReveal.slide(index)へ、slidechangedをyebisu-pageへ通知。controller/navigationは原典runtime。

## 確認

実計算、Quarto render exit0、初回主要表示、元→キーの1→2、代表2PNG、短いSKILL quick_validateのみ。全頁詳細検査・独立レビュー・全ZIP再実行はしていない。Quarto1.9.38に非致命的SCSS CSS-variable export warningが出たが、生成CSSは出力され、初回字体/白青の表示とnavigationを確認した。ログをoutput/quarto-render.logへ保持。色変数のCSS custom property書出しはこの警告の対象であり、拡張SCSS本体を置き換えていない。

原文条件はLICENSE、DEPENDENCIES.md、licenses、fonts/*/OFL.txtを参照。SOURCE/PROVENANCE/QAは確認範囲を区別する。
