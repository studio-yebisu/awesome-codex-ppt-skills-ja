---
name: paper2ppt-ja
description: 論文・研究ノートの主張を根拠に対応させ、編集可能な日本語の研究発表を作る。
---

# 根拠を保った研究発表を作る

原典 wp-a/paper2ppt / commit bb98ce95ca5942fc6551dddc723cbdfe2d637d59 / MIT。非公式の日本語案内。source/UPSTREAM_SKILL.mdとsource/upstream-referencesを読む。

1. 論文全文・一部・研究ノートのどれがあるかを分類し、目的、聞き手、時間、言語を決める。原典の既定は中国語12〜16枚・15〜20分。依頼の指定を優先する。一般営業資料や画像スライドの復元とは用途を分ける。
2. 原典scripts/preflight.pyで入力・出力先・制作と描画の環境を確認する。入力が欠ける場合は止めて不足を報告する。環境の不足を成功に置き換えない。
3. 作成前にclaim-to-sourceを作る。主張、原資料の節、根拠の内容、支持の程度、留保、使う頁を記す。引用、数値、因果、実験結果を推測で埋めない。ノートだけなら提案・仮説・評価計画と実証結果を分ける。
4. 問い、方法、結果、解釈、限界へ、資料に存在する内容を構成する。1頁1主張を基本に、原典のpaper-typesとevidence-first workflowで図と説明順を決める。結果がなければ結果頁を捏造しない。
5. 利用可能な専用PPTXツールを優先し、無ければ原典の許容するpython-pptx fallbackで作る。文字・表・主要図を編集可能にし、主張の出典と話者ノートを付ける。
6. 原典inspect_pptx.py --require-notesで構造を検査し、内容を台帳と照合する。利用できる描画器で全頁を実表示し、文字、図、出典、重なり、余白を直す。描画器が無ければ原典の状態structurally-verified-with-disclosure、作成不能ならblockedとし、passと混同しない。
7. 既定の納品はpresentation_ja.pptxとnotes/qa_report.md。PDF・PNG・制作一式などの追加は依頼に合わせる。QAには根拠対応、構造、描画、残る限界を分けて記す。

## この8枚の作例

架空・未実施の食品在庫UI研究計画をnotes-onlyとして扱った。BRIEF §1〜8に対応する8主張の台帳を保存し、それを生成器が読んでから全頁の出典・話者ノートを作る。原典preflightとinspectorを実行し、PowerPoint16で全8頁を描画・確認した。提案、仮説、評価計画、限界を区別し、食品ロス削減の実測値や安全保証を加えていない。

8枚・日本語・制作ZIPは今回の依頼による変更。source/build.pyは固定作例の生成器であり、任意論文を自動抽出する製品ではない。別の題材では元資料、主張台帳、構成、生成内容を更新する。配布のdeck.pptxはpresentation_ja.pptxと同じ互換名。独立評価と正式採用は別に記録する。

## 環境と書体

この再現にはPythonとpython-pptx1.0.2以上。原典preflightはPyMuPDF/Pillowも調べる。表示確認にはPowerPointまたはLibreOffice等の描画器が必要。依存を自動導入しない。
書体はNoto Sans CJK JP Regular/Bold。Noto Sans JPとは名前が異なる。公式Noto CJKのOFL配布物を作成者と受け手の端末に導入する。OSからフォントを抽出して再配布しない。

原典: https://github.com/wp-a/paper2ppt/tree/bb98ce95ca5942fc6551dddc723cbdfe2d637d59
書体: https://github.com/notofonts/noto-cjk/tree/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/OTF/Japanese
