---
name: html-editable-ja
description: HTMLの文字と単純な図形を、受け取った人がPowerPointで個別に直せる部品へ変換し、元の表示と比較して修復する。
---

## このスキルでできること

HTMLの文字と単純な図形を、受け取った人がPowerPointで個別に直せる部品へ変換し、元の表示と比較して修復する。

- 困っている状況: HTML資料しかないと、PowerPointで提出・修正できない。
- 必要な入力: 既存のHTML資料・使用画像・使用フォント
- 受け取るもの: 文字と単純図形を編集できるPPTX。SVGや複雑な装飾は画像部品になる場合がある。
- 必要環境: 既存HTMLと参照素材。Python依存はupstream/requirements.txt、Playwright ChromiumとPPTX描画用PowerPointまたはLibreOffice。 / この作例の変換は既存.venv、字体導入no、audit.mode=page、cleanup.keep。新規installは検査していない。 / 同梱TTF/OFLの使用条件を確認する。PPTXは埋込なしなので利用端末に字体が必要。PDF掲載PNGには別途pypdfium2/Pillowを使う。
- 作例で試した範囲: この作例では字体埋込みの成功は未実証。埋込版をPowerPointで開けず、原因は未確定のため--no-embed-fontsで配布する。文字と単純図形の編集性、全頁比較、修復の実行を確認した範囲を示す。 原典preflight→DOM実測→assemble→Stage5a/5bを実行し、全5比較を別担当が読んだ。旗を同形のnative部品にし、2頁罫線の下端と5頁番号の独立行を修復。別PPTXで店名と旗の塗りを編集・保存・再表示した。


# HTMLの文字と図形を編集できるPowerPointへ変換する

ブラウザーでHTML資料の文字位置と書式を実測し、文字・単純図形を編集できるPowerPointへ変換する。原典は必要な字体の取得・部分埋込みと、複雑装飾の画像化、元HTMLとの比較・局所修復まで扱う。

**この作例では字体埋込みの成功は未実証。埋込版をPowerPointで開けず、原因は未確定のため--no-embed-fontsで配布する。文字と単純図形の編集性、全頁比較、修復の実行を確認した範囲を示す。**

原典 [Hasasasa/html-to-editable-pptx](https://github.com/Hasasasa/html-to-editable-pptx/tree/17c1dbb76e958543dc2741a7d50ca374354f33b7)、固定commit `17c1dbb76e958543dc2741a7d50ca374354f33b7`、MIT。原典を保存した非公式日本語派生。

## 入出力

既存のHTML資料と参照する画像・字体、字体導入と比較方法の条件。

文字・単純図形を編集できるPPTXと修復用HTML。複雑装飾は画像になり、字体埋込みは実行条件に応じて確認する。

## 使い方

1. 元HTML・画像・字体をそろえ、字体導入可否と比較方法を既存の指定・configへ合わせる。原典supported-css.mdで編集可能な表現と画像化される表現を確認する。
2. 原典convert.pyへHTMLを渡す。原HTMLを保管し、修復は自動生成される.audited.htmlに限定する。字体の部分埋込みと無効化のどちらを使ったかを記録する。
3. Stage5aの構造検査とStage5bのHTML/PPTX比較を行う。pageは全頁、triageは一覧から選んだ頁を別担当で読む。生成成功だけを合格にしない。
4. 指摘を全部そろえて最小差分で一括修復し、変更頁を再変換する。全体CSS・字体の変更は全頁、同じ頁/要素の指摘が2回続く場合はsticky候補として判断を返す。
5. 原典lessons-learnedへ再利用できる回避則を記録し、文字・図形を別PPTXで編集/保存/再表示する。字体条件と残る差を比較画像の近くに書いて渡す。

## 原典の修復ルール

指摘は頁と要素名で記録し、全指摘を一括で最小修復する。追加/削除行は指摘数×3行以内。同じ頁/要素が連続2回残る場合はstickyとして判断を返し、勝手に変更範囲を広げない。共通CSS・字体の変更は全頁再変換する。再利用できるHTML回避則・OOXMLの限界をlessons-learnedへ分け、元のconverterを直接書き換えない。

## この作例

この作例では字体埋込みの成功は未実証。埋込版をPowerPointで開けず、原因は未確定のため--no-embed-fontsで配布する。文字と単純図形の編集性、全頁比較、修復の実行を確認した範囲を示す。 原典preflight→DOM実測→assemble→Stage5a/5bを実行し、全5比較を別担当が読んだ。旗を同形のnative部品にし、2頁罫線の下端と5頁番号の独立行を修復。別PPTXで店名と旗の塗りを編集・保存・再表示した。

**1頁：旗と文字を別のnative部品へ**：右の5頂点の旗と左の見出しを同頁の比較で確認する。別コピーでは右上の店名だけ、別のコピーでは旗の塗りだけを変更した。 単純図形は編集可能な表現を優先する。本例の旗は原典が画像化したSVGから専用adapterでnative freeformへ置換した範囲で、原典の汎用SVG機能とは分ける。

**2頁：本文と罫線の下端をそろえる**：右本文の最終行まで縦罫線が届き、文字を横切らないことをHTML/PPTX比較で見る。暗色背景・見出し・引用と本文を別部品として保つ。 原HTMLを保持し、audited.htmlの局所修復後に同じ頁を比較する。罫線のような単純要素を画像へ統合せず編集可能にする。

**5頁：番号を本文から分ける**：01/02/03が各列の独立した行となり、直下の見出しへ接触しないことを見る。3列の本文・上罫線は保持する。 全指摘を最小差分で直し、該当頁を増分で再変換する。空白だけでは修復未達だったため、明示改行で直し、前4頁の画像hash不変も確認した。

[全5頁のHTML/PPTX比較と字重差](example/qa/comparison/index.html)。

## 制約と差分

- この作例では字体埋込みの成功は未実証。埋込版をPowerPointで開けず、原因は未確定のため--no-embed-fontsで配布する。文字と単純図形の編集性、全頁比較、修復の実行を確認した範囲を示す。
- 旗は原典SVG通路の画像を、その5頂点と位置を保つnative freeformへ置き換えるcase専用adapterで対応。原典converterの汎用SVG変換機能ではなく、任意のSVGをnative化できるとは示さない。
- 日本語TTF登録・5点旗のnative化・暗黙effectRefを0へ・比較ラベルの英語化・PowerPointをQuitしない描画を局所adapterとして分離。原典convert/measure/assemble/embedは未改変。
- HTMLのfont-weight900は原典の写像でOOXMLのbold表現となる。実PDFはZen Kaku Gothic New Boldを使用し、ブラウザーのBlackとの字重・字幅の厳密一致は保証しない。
- 本例は架空のブランド案5頁。全CSS、任意のHTML、動き・動画・Web操作の再現、字体埋込みの成功、新規installを試した例ではない。
- 原典の最小修復は追加/削除行数が指摘数×3行以下、同一頁/要素が連続2回残る場合はsticky。今回は既存の自律改善指示と親の具体修復指示により番号の追加修復を行い、判断を履歴に残した。
- 原典のpage審査をCodexの別担当読解で実施。全5比較とp2/p5単体、p5修復後を親が実見した。原典Claude Agent APIの同一実装や独立Kimi/Opus満点・人間採用とは主張しない。

## 必要な環境

- 既存HTMLと参照素材。Python依存はupstream/requirements.txt、Playwright ChromiumとPPTX描画用PowerPointまたはLibreOffice。
- この作例の変換は既存.venv、字体導入no、audit.mode=page、cleanup.keep。新規installは検査していない。
- 同梱TTF/OFLの使用条件を確認する。PPTXは埋込なしなので利用端末に字体が必要。PDF掲載PNGには別途pypdfium2/Pillowを使う。

実行は[REPRODUCE.md](example/REPRODUCE.md)、現在の証拠はQA.jsonとPROVENANCE.json。制作担当の目視、別担当読解、独立採点、人間採用を分ける。

現在作例はexample/。実行CWDもexample/。原典はupstream/。

## この方式で気をつけること

- PowerPointで開ける配布版は、原典の --no-embed-fonts を使用。日本語書体は公式TTFを端末へ導入する。
- 原典FONT_PLANへの日本語フォント登録アダプターを使用。変換本体は原典の measure/assemble を維持。

## 単体の本文から使う

この本文は `skill-forks/html-editable-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Hasasasa/html-to-editable-pptx/tree/17c1dbb76e958543dc2741a7d50ca374354f33b7

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `html-editable-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: Hasasasa / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/LICENSE
