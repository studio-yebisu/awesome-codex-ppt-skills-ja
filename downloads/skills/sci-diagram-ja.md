---
name: sci-diagram-ja
description: 原典SciDiagramの公式portable templateで科学の関係を日本語のnative図形・矢印としてPPTX化する。
---

# 日本語の科学概念図

1. 一次資料で概念を確認。量を示すデータがない図は「縮尺のない概念モデル」と明記する。
2. upstream/SKILL.md、references/reconstruction.md、runtime-pptxgenjs.mdを読む。SCI_DIAGRAM_RUNTIME=pptxgenjsを選ぶ。全要素のnative/raster所有と矢印方向を先に決める。
3. source/input.jsonのNODES/EDGES/INSETSを編集。EDGESのfrom/to/directionとpointsが関係を定義する。INSETSはこの例では空。配置から関係を推測しない。
4. Node20+を用意。source/で `npm ci --ignore-scripts --no-audit --no-fund`。公式templateが要求するPptxGenJS4.0.1をpin済み。Zen Kaku Gothic NewとSpace Groteskをfonts/の公式TTFから導入。
5. 展開先で `node source/build.mjs`。出力はsource/deck.pptx。意図的な再生成だけ`--overwrite`を指定する。
6. Windows PowerPointで開いて主ページを確認。PNG/PDFはsource/render_powerpoint.ps1、または原典upstream/scripts/render_pptx.pyとLibreOffice/pdftoppmを使う。実施範囲だけ記録。

原典の単図再構成を新規概念図5枚へ明示拡張した例。SKILL本文だけでは生成できず、同梱build.mjs・input.json・MITのPptxGenJSが必要。原典Apache-2.0、commit cc8f0030edf80eeab6e52849b8c39fe638466776。原作者の公式日本語版ではありません。

## この方式で気をつけること

- 掲載効果の主証拠は複合例。単純例の4箱・4方向は最小復元と文字・箱・線の編集を確かめる補足。
- 初稿のコードと対応表は実Claude Opus5.5。標準制作pass02のFONT修正、継続改善pass04の角丸・矢じりと現在の自己完結化、実行・検査はCodex。
- 複合例の標準2pass終了と追加改善pass04、R13の保存プログラムの引き渡し修正は異なる工程。--pass-index Noneを追加改善の承認証拠にしない。
- 現在のpass04/build.mjsに矢じり補正を内包し、準備済みruntimeでbuild.mjs/source.png/editable.pptxの3ファイルだけを再生。旧Python補正と旧profileのpass02終端・角丸近似は履歴で、現在の仕様ではない。

## 単体の本文から使う

この本文は `skill-forks/sci-diagram-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/HututuWorks/sci-diagram-pptx/tree/cc8f0030edf80eeab6e52849b8c39fe638466776

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sci-diagram-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: HututuWorks / 原典条件: Apache-2.0。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/LICENSE
- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/skills/sci-diagram-pptx/LICENSE
