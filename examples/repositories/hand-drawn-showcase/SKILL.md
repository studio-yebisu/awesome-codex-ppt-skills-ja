---
name: hand-drawn-ja
description: 章の題名に合う手描きSVGと低彩度の背景で、編集できる文字を持つ章扉PPTXを作る。
---

# 手描きの章扉を作る

用途はプレゼンテーションの章の切り替えです。章題・番号・象徴図を揃えます。本文やグラフを含むフル資料のスキルとは区別します。

渡すもの: 章数、各章の短い題名・話題、表紙の有無、章番号とページ番号の開始値。

受け取るもの: 手描き風の象徴図と章題を組み合わせた章扉PPTXと生成用ソース。文字は個別編集でき、挿絵は原典方式ではPNGになる。

## 手順

1. 章数・各章題・表紙の有無・章とページの開始番号を決め、原典SKILLのStep1を確認する。

2. 隣り合う章で似た色を避け、原典の低彩度の寒暖色から背景を選ぶ。各章の意味に合うSVGを40点のライブラリーから選ぶ。

3. 原典のPptxGenJS＋sharp雛形で13.333×7.5の章扉を作る。章題Georgia40pt regular、章ラベルとページCalibri14pt、指定座標を保つ。日本語書体を補う場合は差分として記録する。

4. 表紙を含める場合は左上54pt以上の見出しと小さな装飾だけを置き、章ラベルや章扉と同じ大きな図を置かない。

5. Step6通りにPPTXをLibreOfficeでPDF化し、pdftoppm150dpiで全ページを画像化する。切れ・重なり・図の位置・配色・番号を目視し、修復後も該当頁を再描画する。

原典は `upstream/hand-drawn-chapter-slides/SKILL.md`、SVGは `upstream/hand-drawn-chapter-slides/scripts/illustrations.md`。固定commit `322a265344e73cd54f77f3f07b6a9f15bb7d2d99`、MITを保持しています。

## 同梱作例と再実行

一式ZIPは `example/`、作例単体ZIPはrootを作業場所にします。入力 `input/data.json`、入口 `build.cjs` です。用意済みNode.js＋PptxGenJS4.0.1＋sharp0.35.5、Python3を使い `node build.cjs`。日本語fallbackの小adapterもこのコマンドから動きます。`HANDDRAWN_PYTHON` で既存Pythonを指定できます。依存と書体の新規導入は再実行検査で行っていません。

全工程は `python source/reproduce.py --render --node <既存node> --soffice <既存soffice> --pdftoppm <既存pdftoppm>`。PDF→PNGの追加検査にはPythonのpypdfium2が必要です。原典Step6のLO PDF→全頁JPEG150dpiに、PowerPoint再表示と別コピーでのnative章題編集を追加しました。PowerPointは開いた資料だけを閉じます。

作例「話し合いの進め方」は表紙＋4章です。観察→虫眼鏡、共有→吹き出し、試行→階段、記録→チェックリストと対応させています。原典の低彩度背景、左下章題、右下番号を保持。表紙の小sparkleは派生作図、和文はYu Minchoに補います。旧版の赤枠・大きな苗木・循環図は現在版では使用しません。

章扉・区切り頁を作るスキル。本文の論理構成、業務データのグラフ、図表を備えたフル資料の作成をこの例では示さない。

原典はGeorgia/Calibriを厳密指定する。本例は欧文指定を保持し、日本語グリフだけYu Minchoへ明示する派生。和文まで原典と同一書体とは説明しない。

CalibriとYu MinchoはWindows既存書体を参照し、字体ファイルはZIPへ同梱・PPTXへ埋込みしない。別環境は対応する書体が必要。

手描きの挿絵は原SVGからPNG化するため線や塗りの個別編集はできない。変更する場合はSVGを編集して再生成する。

同梱の表紙sparkleは原典の新規図形ルールに沿う小さな派生SVG。章の4点は原典SVGを未改変使用。チェックリストの線は象徴的な記号で実際の記録内容ではない。

原典に対話で要件を集める段階があるが、本例は委任された改修で要件を確定した。過去の人間承認や現行版の独立評価合格は主張しない。

現行画像の確認はCodexによる実装側QAです。独立モデル再評価・人間の採用判断とは区別します。`QA.json`、`reviews/page-audit.json`、`source/recipe-check.json`、`source/zip-replay.json`を参照してください。
