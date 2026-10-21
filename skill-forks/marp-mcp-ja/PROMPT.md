# 再制作の指示

箇条書きや表を資料へ整え、ページIDで指定した内容だけを更新する。

入力: ページごとの見出し・本文・箇条書き・表と、変更したい内容。
出力: 編集元のMarkdownとHTML・PDF。MCP実装のPPTX出力は各頁の画像を収めた形式。

1. marp-mcp --versionでCLIを確認する。list-layoutsで版式と必須項目を調べ、-tで基本テーマ、-sで追加スタイルを選ぶ。-s指定時は原則-t defaultになる。
2. createで資料を作り、set-frontmatterで見出しや頁番号を設定する。manageのlayoutとparamsへ原稿を渡して頁を追加する。
3. generate-idsでIDを付け、readで対象IDを調べる。manage --mode replace/deleteと--slide-idで変更箇所を指定する。既存IDは再発行しても変わらない。
4. export -f htmlまたは-f pdfで書き出す。generate-agendaとadd-image-transitionはHTML用の機能として必要な時に使う。MCP経由も選べるが、原典SKILLの主な入口はCLI。
5. 出力した全頁を開き、文字・表・改行・ID指定の変更箇所を確認する。PPTXの出力方式と編集できる範囲を分けて伝える。

同梱作例の範囲: 元MCPで全6頁を再生成しHTML/PDF/PPTXを書出し。元CLIでも作成・ID更新・ID保持・HTML/PDF出力を実行。HTML6頁・PDF6頁を実描画し目視。3頁の4動作、4頁の表幅、6頁の文字コントラストを修復。

制約: 6頁の主作例は同梱MCP実装で制作。CLIだけで6頁を制作した例ではない。原典CLIは別の2頁で実操作確認した。
制約: 原典SKILLのCLI exportはHTML/PDF。今回のPPTXはREADME・MCP実装の画像出力で、文字・表・図形を個別編集できない。
制約: 工程図と3列図はcontentへ追加したHTML/CSS。generate-agenda・add-image-transition、編集可能PPTX、PowerPoint実機表示は未実証。
