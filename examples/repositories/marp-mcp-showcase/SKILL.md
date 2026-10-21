---
name: marp-mcp-ja
description: 箇条書きや表を資料へ整え、ページIDで指定した内容だけを更新する。
---
# Marpのページ作成とID指定更新

原典の固定commit・利用条件は[SOURCE.json](PROVENANCE.json)。[未変更の元SKILL](source/upstream/skills/marp/SKILL.md)と必要な参照を保持しています。

## 手順

1. marp-mcp --versionでCLIを確認する。list-layoutsで版式と必須項目を調べ、-tで基本テーマ、-sで追加スタイルを選ぶ。-s指定時は原則-t defaultになる。
2. createで資料を作り、set-frontmatterで見出しや頁番号を設定する。manageのlayoutとparamsへ原稿を渡して頁を追加する。
3. generate-idsでIDを付け、readで対象IDを調べる。manage --mode replace/deleteと--slide-idで変更箇所を指定する。既存IDは再発行しても変わらない。
4. export -f htmlまたは-f pdfで書き出す。generate-agendaとadd-image-transitionはHTML用の機能として必要な時に使う。MCP経由も選べるが、原典SKILLの主な入口はCLI。
5. 出力した全頁を開き、文字・表・改行・ID指定の変更箇所を確認する。PPTXの出力方式と編集できる範囲を分けて伝える。

## CLIの基本形

```text
marp-mcp --version
marp-mcp -t default -s minimal list-layouts
marp-mcp -s minimal create <file.md> --title <title>
marp-mcp -s minimal set-frontmatter <file.md> --paginate
marp-mcp -s minimal manage <file.md> -l <layout> -p <JSON>
marp-mcp generate-ids <file.md>
marp-mcp read <file.md>
marp-mcp -s minimal manage <file.md> --mode replace --slide-id <id> -l <layout> -p <JSON>
marp-mcp manage <file.md> --mode delete --slide-id <id>
marp-mcp export <file.md> -f html
marp-mcp export <file.md> -f pdf
```

generate-agendaは章見出しから議題頁、add-image-transitionは対象頁の前に画像の遷移頁を追加するHTML用機能です。今回の完成作例では未実施です。MCP経由は同じリポジトリの別の入口で、元SKILLのCLI案内を置き換えません。

## 同梱作例の実施範囲

元MCPで全6頁を再生成しHTML/PDF/PPTXを書出し。元CLIでも作成・ID更新・ID保持・HTML/PDF出力を実行。HTML6頁・PDF6頁を実描画し目視。3頁の4動作、4頁の表幅、6頁の文字コントラストを修復。

- 6頁の主作例は同梱MCP実装で制作。CLIだけで6頁を制作した例ではない。原典CLIは別の2頁で実操作確認した。
- 原典SKILLのCLI exportはHTML/PDF。今回のPPTXはREADME・MCP実装の画像出力で、文字・表・図形を個別編集できない。
- 工程図と3列図はcontentへ追加したHTML/CSS。generate-agenda・add-image-transition、編集可能PPTX、PowerPoint実機表示は未実証。

今回の修復はCodex。自動検査と作者の目視は独立評価・人間の承認と分けて記録します。[現行QA](source/repair-qa.json)と[原典工程の記録](source/round5-original-gates.json)を参照。元LICENSE、NOTICE、字体のOFLを残します。
