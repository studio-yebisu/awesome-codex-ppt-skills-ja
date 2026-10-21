---
name: image-to-editable-ppt-ja
description: 元画像を文字・図形・アイコンへ分け、文字とカードを編集できるPPTXへ戻す。
---

## このスキルでできること

元画像を文字・図形・アイコンへ分け、文字とカードを編集できるPPTXへ戻す。

- 困っている状況: 画像になったスライドでは、本文を直すにも画像全体の再生成が必要になる。
- 必要な入力: 再構築する画像の各頁、正確な文字・数値、編集する部分と画像のまま保つ部分の指定。
- 受け取るもの: 文字・図形を個別に編集できるPPTXと、画像から部品への対応表・検査記録。複雑な素材は画像として保持する。
- 必要環境: Python3.10+と原典editppt CLIの固定依存（PyMuPDF/python-pptx等） / 新規入力には頁worker対応エージェントと選択した画像backend。保存済み結果の再統合は画像生成不要。 / 今回の描画はWindows PowerPoint/Yu Gothic/Arial Narrow、同梱BIZ UDPGothic Bold。
- 作例で試した範囲: 原図2枚を新規runの実worker2名へ渡し、1頁は成功版のSHA照合で再利用、2頁はgit commitの字間と位置を原図に合わせて修復。原典record/finalizeを通し、文字21件を含むnative41要素とbitmap7点を統合。


# 既存画像を編集できる文字と図形へ再構成する

既存画像を頁ごとに分解し、文字や普通図形をnative、複雑なアイコンを個別画像へ分け、原典CLIで検査・統合する。

## 入力と出力

渡すもの：編集できるようにしたい既存のスライド画像、PDF、画像を含むPPT/PPTX。ノートがあれば元ファイルも渡す。

得られるもの：文字・普通の図形・画像を分けた編集可能なPPTX、再構成manifestと頁/全体の検査記録。

原典 [ningzimu/image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill/tree/b7be494e31a0ed56ef98716891db5474606b8cdf)、固定commit `b7be494e31a0ed56ef98716891db5474606b8cdf`。原文と利用条件を保存した日本語派生で、公式翻訳ではありません。

## 使う手順

1. 原典run prepareで画像を入力し、頁ごとのworker promptと入力SHAを作る。文字/普通図形/画像の分類を各頁で決める。
2. 別workerへ各頁をdispatchする。workerだけが頁manifestを作り、分離アイコンをprocess-sheetし、page build/contact-sheet/validateまで行う。
3. orchestratorは結果とSHA・validationを確かめてrecordし、全頁受入後に原典run finalizeで統合・検査する。
4. PowerPointで原図と出力の両頁を見比べ、別コピーで文字変更と再表示を確認する。保存済みworker結果だけの再出力はsource/reproduce.pyを使う。

## この作例で試した範囲

原図2枚を新規runの実worker2名へ渡し、1頁は成功版のSHA照合で再利用、2頁はgit commitの字間と位置を原図に合わせて修復。原典record/finalizeを通し、文字21件を含むnative41要素とbitmap7点を統合。

**1頁：Gitの保存・記録・共有**：原図と完成版の3カード・2矢印・9文字を見る。文字とpillはnative、3アイコンだけbitmapとして分かれる。 原典はtext_inventoryとelement manifestで各要素をnative text/shapeと画像へ分類し、頁workerが再構成する。

**2頁：変更は3つの場所を進む**：中央から右のgit commitとpillの間を見る。普通の空白1個、同じ21.5pt、原図の文字幅に近い字体と位置へ戻し、箱間を35px確保した。12文字と箱/矢印はnative、4アイコンはbitmap。 原典のpage build/validateはmanifestから再構成して要素・画像来歴を検査する。字体の手動校正は原典schemaの例外として記録。

**2頁：2頁のラベルを別コピーで編集**：中央の説明だけが「次に記録する内容」から「次回の記録内容」へ変わる。PPTXへ文字変更を保存し、再描画した実画像。 原典のeditable出力は文字を画像へ焼き込まない。別PPTXのnative文字runを実変更し、主成果物のSHA不変も確認する。

## 用意するもの

- Python3.10+と原典editppt CLIの固定依存（PyMuPDF/python-pptx等）
- 新規入力には頁worker対応エージェントと選択した画像backend。保存済み結果の再統合は画像生成不要。
- 今回の描画はWindows PowerPoint/Yu Gothic/Arial Narrow、同梱BIZ UDPGothic Bold。

## 制約と未実施

- 元画像は同じカタログ内のcodex-image-pptで作ったGit説明画像。外部の複雑な実資料の復元精度は示さない。
- 文字・カード・背景・普通矢印はnative。7アイコンは元画像の実image_gen編集で分離済みのbitmapで、内部の線や色は編集できない。
- 今回の修復は2名の実workerが各頁build/validateを担当し、orchestratorが原典dispatch/record/finalizeを実行。元の分離画像はSHA照合で再利用し、新しい画像生成・外部OCRは未実施。
- 字体・平塗りと改行は近似。画素一致を保証せず、正しい文字・箱・矢印方向・編集性を照合する。
- 1頁は公式BIZ UDPGothic Bold/OFL同梱。2頁はYu GothicとArial Bold/Arial Narrow Boldを使用しOS字体は非再配布。新規入力のOCR/backend設定は原典に従う。
- 講稿はカタログ制作時に新規追加した説明で、画像から抽出したノートではない。本文XMLと画像bytesを保つnotes-only処理を記録。

現在版は制作側が全頁の実画像を確認しています。独立モデルの現在版再評価・人間の採用とは別です。自己採点はしていません。現在hashと検査は [example/QA.json](example/QA.json)、実行範囲は [example/PROVENANCE.json](example/PROVENANCE.json)、再実行は [example/REPRODUCE.md](example/REPRODUCE.md) を参照してください。

原文は upstream/、現在作例は example/。再実行CWDは example/ です。

## 単体の本文から使う

この本文は `skill-forks/image-to-editable-ppt-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/ningzimu/image-to-editable-ppt-skill/tree/b7be494e31a0ed56ef98716891db5474606b8cdf

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `image-to-editable-ppt-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: ningzimu / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/ningzimu/image-to-editable-ppt-skill/blob/b7be494e31a0ed56ef98716891db5474606b8cdf/LICENSE
