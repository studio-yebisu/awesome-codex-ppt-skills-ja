---
name: marp-mcp-ja
description: 箇条書きや表を資料へ整え、ページIDで指定した内容だけを更新する。
---

## このスキルでできること

識別IDで指定した箇所だけを更新し、Marp原稿と書き出す資料の対応を保てる。

- 困っている状況: Markdownを直接編集するだけでは、ページ追加や書式変更の操作をエージェントに任せにくい。
- 必要な入力: MarpのMarkdown原稿、作成・更新したい内容、対象を指定する識別ID。
- 受け取るもの: 更新したMarkdownと、原典の書き出し機能で作るHTML・PDF・画像主体のPPTX。編集は元原稿で行う。
- 必要環境: Node.js18以上、固定原典runtimeと互換依存、Marp CLI4.4.0、Chrome/Edge。再生成helperのPDF描画にはPython3とPyMuPDFが必要。
- 作例で試した範囲: 衣服の修理会を題材にMCPで6頁を制作し、HTML・PDF・画像型PPTXを出力。原典CLIは別の2頁で操作した。

# Marpのページ作成とID指定更新

原典の固定commit・利用条件は[SOURCE.json](SOURCE.json)。[未変更の元SKILL](source/upstream/skills/marp/SKILL.md)と必要な参照を保持しています。

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

## 単体の本文から使う

この本文は `skill-forks/marp-mcp-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/masaki39/marp-mcp/tree/2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `marp-mcp-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: masaki39 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/masaki39/marp-mcp/blob/2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f/LICENSE
