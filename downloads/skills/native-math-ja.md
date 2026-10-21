---
name: native-math-ja
description: 原稿・研究資料から、数式をPowerPoint内で編集できる発表資料を作る。
---

## このスキルでできること

原稿の数式を画像にせず、図表と一緒にPowerPoint内で編集できる教材へ組み立てる。

- 困っている状況: 数式を画像で貼ると、変数や分母をPowerPointで変更できない。
- 必要な入力: 説明したい原稿・数式・具体例のデータ・発表時間と聞き手
- 受け取るもの: 文字・図表・数式を編集できるPPTXと数式・生成ソース
- 必要環境: Node.jsとPptxGenJS / Pythonとlxml / Pandoc（外部実行依存） / Microsoft PowerPoint（native数式の実表示・編集確認） / 作例はShippori Mincho・BIZ UDPGothic・Manrope（公式TTF/OFL同梱）
- 作例で試した範囲: 原典Sandwichの青・橙を濃く調整し、図表の部品とOMML注入を実行。各頁の式を2ブロック以内にし、全5頁の目視と原典overlap検査0件を確認した。
- 制約: 仮想得点3件を全体とした分散を説明する教材。論文からの抽出や、実際の調査結果を示す例ではない。 / 本編5枚へ絞った作例で、原典のReferences/Thank You/Backup追加は省略した。 / OMMLの確認にはPowerPointを使用。LibreOfficeでは数式が欠ける場合がある。 / 原典の5並列excellenceと包括的構造監査、ZIP再実行は未実施。修正後のKimi K3・Opus5.5再評価は未了。


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

## 単体の本文から使う

この本文は `skill-forks/native-math-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Noi1r/powerpoint-skill/tree/a39cd8cfba332741a96d52bebd2bb378b638364e

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `native-math-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: Noi1r / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Noi1r/powerpoint-skill/blob/a39cd8cfba332741a96d52bebd2bb378b638364e/LICENSE
