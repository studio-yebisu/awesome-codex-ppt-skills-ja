---
name: office-powerpoint-mcp-ja
description: 原稿と数値をMCPへ渡し、文字・表・データ連動チャートを持つPPTXを作成・修正できる。
---

# MCPの操作で作成・比較・修正する

python-pptxを使うMCPサーバーのツールを通して、PPTXの作成・管理・文字・表・図表・テンプレートを操作する。

## 入力と出力

渡すもの：作成・編集したい資料の内容、表やチャートの元データ、必要に応じて元PPTXやテンプレート。

得られるもの：MCPツールで作成・編集したPPTXと、実行した操作・保存・描画確認の記録。

原典 [GongRzhe/Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/tree/3631ba2ec0c24504476f78bf74d329c9be11caaa)、固定commit `3631ba2ec0c24504476f78bf74d329c9be11caaa`。原文と利用条件を保存した日本語派生で、公式翻訳ではありません。

## 使う手順

1. source/upstream/ppt_mcp_server.pyをstdioで起動し、list_toolsで実際の操作と引数を調べる。
2. source/build_mcp.pyで元MCPの作成・文字・表・チャート操作とbefore_after_comparisonテンプレートを呼ぶ。input/data.jsonを数値の正本にする。
3. source/runtime-adapters.mdの局所互換処理を確認し、PowerPoint描画で表・凡例・単位・前後値を照合する。
4. source/check_native_edit.pyで別コピーの本文とチャート1点を変更・保存し、元ファイルのSHAが変わらないことを確認する。

## この作例で試した範囲

原典MCPへ95操作を実行し、比較表・2系列チャート・比較テンプレートを制作。日本語と比較型の局所調整はadapterへ分け、別コピーへ本文変更と220→221のchart更新を保存した。

**2頁：売上増と粗利率低下を同時に見る**：表の売上1000→1200、粗利率38→36、返品率4→6を照合する。セルはデータを持つOffice表。 原典のadd_table/format_table_cellで構造化した行列を作り、数値と書式を分けて操作する。

**3頁：売上増200万円の中心は自然検索**：斜線/塗りの2系列と8値、下に一度だけ置いた凡例を見る。上の45%は自然検索の増加90÷全増加200の計算で、構成比ではない。 原典のadd_chartは系列・カテゴリ・値からnativeチャートを作る。斜線/凡例位置と和文字体は明示adapter。

**4頁：粗利額は増え、率は2ポイント低下**：左右の前年/当年と下の差額棒を読む。原典比較型へ実データを渡し、無関係な黄色の楕円・矢印はadapterで外して他頁の見出し位置へ合わせた。 高水準before_after_comparisonで比較構造を作る。未対応の日本語・配置調整は元の生成機能と分けて記録する。

## 用意するもの

- Python3.10+ / mcp1.30.0 / python-pptx1.0.2 / Pillow
- PowerPointとBIZ UDPGothic（非埋込）。PDF→PNGにはpypdfium2。

## 制約と未実施

- 原典はSKILL文書ではなくMCPサーバー。固定コミットを同梱し、現在の公開保守状態はこの実行では判定しない。
- 実作成95操作と別コピー編集5操作を実行。25テンプレートのうち1種を使用。画像効果・professional design・自動text修正は未実施。
- 日本語書式/ノート・凡例/斜線・セル縦中央・空段落・テンプレート横幅変換と装飾除去/見出し配置は明示adapter。原典API単独の出力とは区別。
- BIZ UDPGothicの公式TTF/OFLを同梱し非埋込。数値は架空の例。チャート1点の書換保存は原典MCPで行い、GUI編集は未検査。

現在版は制作側が全頁の実画像を確認しています。独立モデルの現在版再評価・人間の採用とは別です。自己採点はしていません。現在hashと検査は [QA.json](QA.json)、実行範囲は [PROVENANCE.json](PROVENANCE.json)、再実行は [REPRODUCE.md](REPRODUCE.md) を参照してください。
