# GongRzhe/Office-PowerPoint-MCP-Server の日本語実行例

公式MCP stdioのcreate_presentation_from_template/add_slide/manage_text/add_table/add_chart/save_presentationを実行。表とネイティブチャートを含む日本語PPTX。

組織・数値は架空。入力はinput/data.json、依頼文はPROMPT.txt、講稿はNOTES.md。deck.pptxは編集可能、render/deck.pdfは閲覧用。

## 環境と導入

- Python 3.13（実測）
- PowerShell 7 / pwsh（描画スクリプト）
- Noto Sans JP
- Microsoft PowerPoint 16.0（PNG/PDF描画用）

MCP 2.3ではFastMCP importが削除されるため1.30.0で実行。リポはarchived。原典format_chartはlegend_positionを反映しないため、has_legend=Falseと公式manage_textによる系列表示で重なりを回避。

## 再現

カタログ全体のrootで、対応原典を .build/actual-upstreams/GongRzhe__Office-PowerPoint-MCP-Server に置き、上記commitへ固定します。次のコマンドのPythonは依存を導入した環境を使います。

    .venv\Scripts\python tools/build_native_repository_examples.py --only mcp --render

一般の利用者は上流README/SKILLを使用してください。MCPは python upstream/ppt_mcp_server.py --transport stdio をクライアントから起動し、source/mcp-calls.jsonの操作・引数を参考に実行。MckはupstreamをPython import pathへ追加しsource/build_native_repository_examples.py内のbuild_mck()と同じstoryをDeckBuilder.buildへ渡します。source/storyline.jsonは保存用で、再読込する場合はseries内のRGB配列をpptx.dml.color.RGBColorへ戻します。当地スクリプトはこの2作例専用で、汎用生成サービスではありません。

## 出典・確認

PROVENANCE.jsonに固定commit、実ファイルhash、適用ファイル、environment.jsonに依存。QA.jsonとrender/powerpoint-render.jsonに検証範囲。LICENSEを保持。原作者の公式日本語版ではありません。
