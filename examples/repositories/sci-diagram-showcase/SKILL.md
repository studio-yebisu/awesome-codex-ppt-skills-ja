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
