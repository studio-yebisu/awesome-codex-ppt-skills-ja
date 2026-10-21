---
name: native-math-ja
description: 原稿・研究資料から、数式をPowerPoint内で編集できる発表資料を作る。
---

# 数式を編集できるPowerPointを作る

原典: Noi1r/powerpoint-skill / commit a39cd8cfba332741a96d52bebd2bb378b638364e / MIT。
原文はupstream/powerpoint-slides/SKILL.md、テーマと全規則は同梱referencesを読む。非公式の日本語案内。

## 自分の資料で使う

1. 原稿や論文を読み、主要な主張、前提知識、例、数式を抽出する。PPTXが必要な用途で使い、Beamer/TeX出力は別スキルへ分ける。
2. 発表時間、聞き手、前提、範囲、深さ、テーマを決める。既に依頼に指定があれば使い、足りない条件だけを確認する。
3. 頁構成・各頁の目的・版式・数式と図の配置を計画する。定義の前に動機、定義から2頁以内に具体例を置く。原典の承認契約はユーザーの既存の指示に合わせる。
4. 原典themes.mdからテーマとPptxGenJS helpersを使う。字体・配色・版式は資料に合わせる。図形、表、グラフをnativeで作る。
5. 数式をformulas.jsonへ集める。通常はrender:ommlを使い、原典render_latex.pyでmanifestを生成。addMathTextのplaceholderを配置し、inject_omml.pyでPandoc→DOCX→OMMLを注入する。残存placeholderを0にする。画像への代替は明示し、黙って編集性を失わせない。
6. 実際にPPTXを生成して全頁を描画する。OMMLはPowerPointで確認する。LibreOfficeでは欠ける場合がある。数式と表の間隔、はみ出し、対比、数式の正確さを頁ごとに確認する。
7. 原典check_overlaps.py、visual-check、audit、pedagogy、excellenceの契約を読み、対応する検査と修正を行う。原典の採点90点以上条件と独立確認を、生成成功だけで置き換えない。未実行は未実行と記録する。
8. 完成PPTX、PDF/PNG、原稿・数式・生成ソース、利用条件、検査範囲を渡す。原典のReferences/Thank You/Backup構成から省く場合は、用途と変更を明記する。

## 必要環境

Node.jsとPptxGenJS、Pythonとlxml、Pandoc。OMMLの表示・編集確認にはMicrosoft PowerPointを使う。PptxGenJSはMIT、lxmlはBSD系、PandocはGPLの外部実行依存。字体は公式配布と原文OFLを使い、Office付属字体やXSLを抽出再配布しない。

## 同梱作例の範囲

5分・5枚の仮想得点教材。Sandwichの青と橙を文字の対比が取れる濃さへ調整し、明朝見出しと日本語本文書体を設定した。本編5枚に絞ったためReference/Thank You/Backup追加を省略。研究論文の抽出例ではない。実行と独立評価の状態は作例QA.jsonを確認する。
