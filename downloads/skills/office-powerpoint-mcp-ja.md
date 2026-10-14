---
name: office-powerpoint-mcp-ja-entry
description: MCPでPowerPointを作るを日本語で制作するときに使う。GongRzhe/Office-PowerPoint-MCP-Serverの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# MCPでPowerPointを作る

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/tree/3631ba2ec0c24504476f78bf74d329c9be11caaa

- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/README.md
- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/ppt_mcp_server.py
- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/tools/presentation_tools.py
- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/tools/content_tools.py
- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/tools/structural_tools.py
- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/utils/content_utils.py
- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/requirements.txt

公式MCP stdioのcreate_presentation_from_template/add_slide/manage_text/add_table/add_chart/save_presentationを実行。表とネイティブチャートを含む日本語PPTX。

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.13（実測）
- PowerShell 7 / pwsh（描画スクリプト）
- Noto Sans JP
- Microsoft PowerPoint 16.0（PNG/PDF描画用）



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: くらし便 EC事業 9月報告

添付EC月次データをGongRzhe/Office-PowerPoint-MCP-Serverで6枚の日本語資料にしてください。売上増200万円と粗利率低下2ポイントを区別し、チャネル比較、粗利計算、担当と期限、次の判断を含めます。原典固有の制作入口を使用し、Noto Sans JPと講稿を設定。架空の数値と明記してください。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: GongRzhe / 原典条件: MIT

- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server/blob/3631ba2ec0c24504476f78bf74d329c9be11caaa/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
