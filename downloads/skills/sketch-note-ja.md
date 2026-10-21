---
name: sketch-note-ja
description: sketch-note-pptの紙色・吹き出し・手描き線と固有controllerで、日本語の動く単一HTMLスライドを組む。HTMLとSVGを編集する用途に使う。
license: MIT
---

## このスキルでできること

原稿を紙面・吹き出し・手描き線・段階表示のあるHTMLに組み、比較や図解を見せる。

- 困っている状況: 文字だけの説明では、比較・補足・判断の分かれ道が同じ重さに見える。
- 必要な入力: 題材・読み手・ページ構成・原稿と図にする関係
- 受け取るもの: ブラウザーで発表する単一HTMLと、編集用HTML・SVG・CSS・JS
- 必要環境: Python3標準ライブラリ（単一HTMLの梱包用） / モダンブラウザー / 同梱の原典CSS/JSとOFL字体
- 作例で試した範囲: 書体の字形・太さ・余白・改行を比較する6頁へ、原典の紙面・吹き出し・図解・段階表示を適用した。空白を囲んでいた丸を実際の字へ固定し、本文を横切る矢印を除去。全6頁と大小2画面の修復箇所を確認した。
- 制約: 出力はHTML・SVG・CSS・JS。PPTXや画像からの自動復元は扱わない。 / 比較する書体や図形は本作例の制作判断。書体選択や学習効果を自動評価するスキルではない。 / 原典CSSとcontrollerを保持し、日本語書体と注釈は局所差分。独立再評価は修復後に実施予定。

# Sketch Notes 日本語ガイド

原典は Watermelon4000/sketch-note-ppt、固定commit `0729098c28a2105b3e2f6225b3afe125e3959fb6`。MIT ©2026 Watermelon4000。[原文SKILL](example/source/upstream/skill/SKILL.md)と[LICENSE](LICENSE)を保持しています。実字体は個別のOFL-1.1です。

1. 題材・読者・枚数・言語を原稿へ保存する。[依頼文](example/PROMPT.md)と[日本語原稿](example/input/MANUSCRIPT.md)を自分の題材へ置き換える。この例は実測のない観察教材6頁です。
2. 原典default sketch-notesを選び、1頁1主題、cover→比較/図解→takeawayの順を作る。全面カード格子にせず、字形の大小・余白・視線の方向を内容に合わせる。
3. [未変更CSS](example/source/upstream/style/sketch-notes-base.css)を実際に使う。`.deck`、`.slide.active`、二重墨枠、紙色、`.halftone`、`.bubble`、`.sketch-underline`、`.decision-tree`を維持。原典SKILLの`.reveal`は見出し・主オブジェクト・吹き出しへ付け、本文段落へ直接付けない。文字サイズはclamp、各頁はスクロールなしで収める。
4. [slides.html](example/source/slides.html)に和文とSVG線を組み、[adaptation.css](example/source/adaptation.css)へ局所差分を置く。原典には必須AI画像工程がないため、この例は自作SVGとCSSで成立させる。日本語表示では原典の遠隔字体を公式固定Zen Maru/BIZ/Manropeへ置換し、TTFと[OFL](example/source/fonts/)を保全する。OS字体は抽出配布しない。
5. 原典demoのcontrollerを使う。←/→・↑/↓・Space・Home/End・swipeで送り、端で止まる元go()の契約を守る。[局所patch](example/source/controller.patch)はsame-originの0-based yebisu-slide/yebisu-pageだけを追加する。
6. Python標準ライブラリで `python example/source/rebuild.py` を実行すると、CSS/JS/実字体を埋め込んだ[単一HTML](example/index.html)を作る。元方式にnpm・生成CLI・外部SDKはない。このPythonは梱包補助であり、汎用スライドrendererではない。

7. 完成HTMLの全ページを発表画面で表示する。日本語・改行・比較する字の大きさ・手描き線の指す先を確認し、線と本文の接触や空白を囲む注釈を直す。前後・先頭末尾の移動と、必要なら大小画面も確認する。実施範囲はQAへ記録し、独立評価の合格と分ける。

この6頁の作例では、字体比較の丸を実際の「雨」に固定し、説明文を横切る矢印を除いた。全6頁を1280×720で、修復箇所を1600×900でも確認した。独立再評価は未了。

編集対象はHTML/SVG/CSS/JS。PPTXを生成したとは表現しない。書体と声の関係はこの教材の選択案で、読了率や学習効果の実測を発明しません。

## 単体の本文から使う

この本文は `skill-forks/sketch-note-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Watermelon4000/sketch-note-ppt/tree/0729098c28a2105b3e2f6225b3afe125e3959fb6

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sketch-note-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: Watermelon4000 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Watermelon4000/sketch-note-ppt/blob/0729098c28a2105b3e2f6225b3afe125e3959fb6/LICENSE
