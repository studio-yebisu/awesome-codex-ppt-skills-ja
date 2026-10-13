# GongRzhe/Office-PowerPoint-MCP-Serverの日本語制作

原典: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/tree/3631ba2ec0c24504476f78bf74d329c9be11caaa

公式MCP stdioのcreate_presentation_from_template/add_slide/manage_text/add_table/add_chart/save_presentationを実行。表とネイティブチャートを含む日本語PPTX。

原典のstdio MCPへ実際にツール呼び出しを送る。mcp 1.30.0を使う。文字、テーブル、ネイティブチャートを生成し、PowerPoint本体で確認する。サーバーはアーカイブ済み。

## 作例

- くらし便 EC事業 9月報告 / 6枚 / pptx
- カタログ内の案内: repository.html?repo=GongRzhe/Office-PowerPoint-MCP-Server
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=GongRzhe/Office-PowerPoint-MCP-Server
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13（実測）
- PowerShell 7 / pwsh（描画スクリプト）
- Noto Sans JP
- Microsoft PowerPoint 16.0（PNG/PDF描画用）

## 元の制作コマンド

    git clone https://github.com/GongRzhe/Office-PowerPoint-MCP-Server .build/actual-upstreams/GongRzhe__Office-PowerPoint-MCP-Server

    git -C .build/actual-upstreams/GongRzhe__Office-PowerPoint-MCP-Server checkout 3631ba2ec0c24504476f78bf74d329c9be11caaa

    python -m venv .venv

    .venv\Scripts\python -m pip install "mcp[cli]==1.30.0" python-pptx Pillow fonttools

    .venv\Scripts\python tools/build_native_repository_examples.py --only mcp --render

## 確認範囲

- MCP 2.3ではFastMCP importが削除されるため1.30.0で実行。リポはarchived。原典format_chartはlegend_positionを反映しないため、has_legend=Falseと公式manage_textによる系列表示で重なりを回避。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
