---
name: marp-mcp-ja
description: 原典Marp MCPサーバーの構造化レイアウト操作で日本語スライドを作り、HTML・PDF・画像主体PPTXへ出力する。
---
# Marp MCP・日本語制作

原典は[masaki39/marp-mcp](https://github.com/masaki39/marp-mcp/tree/2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f)、固定commit `2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f`、[MIT](LICENSE)。[SOURCE](SOURCE.json)と[原典SKILL](source/upstream/skills/marp/SKILL.md)を必要に応じて読む。

## 実MCPで制作する

原典はCLIでも同じ操作が可能。この派生作例は実MCPのstdio JSON-RPC `tools/call`を使う。[再生成ガイド](README.md)の環境を用意し、[run_mcp.py](source/run_mcp.py)から原典サーバーを起動する。

1. `list_themes_and_styles`でテーマ・スタイルを調べ、`list_layouts`を必ず先に呼んで有効なレイアウトとparamsを取得する。
2. `create_presentation`でfrontmatter・表紙・IDsを作る。既存資料を使う場合は先に`set_frontmatter`を呼ぶ。
3. `manage_slide`へ構造化paramsを渡して追加する。replace/deleteでは`read_slide`で取得したslide IDを使う。
4. `generate_slide_ids`で安定したIDを保存し、`read_slide`で編集対象を取得する。
5. 日本語字体と色の局所CSSを原典レイアウトへ重ね、`export_slide`からHTML/PDFを出す。画像主体PPTXも同じ原典MCPで出力できる。

作例は原典`default`＋`minimal`のtitle / two-column / content / table / big-statementを実使用。[入力](input/content.json)と[局所CSS](source/workshop.css)を編集する。表・行程・持ち帰るものの構図を変え、全頁を同じカード列にしない。架空企画や仮の時間を実績として書かない。必要な原典layout実装は`source/upstream/src/styles/minimal/`。

## 出力の編集範囲

HTMLは字体・CSSを埋め込んだ主出力。編集正本はMarkdownと構造化入力・CSS。PDFは固定レイアウト。PPTXは各頁の画像を収めた版で、文字・表・図形のnative編集はできない。原典の実験的`pptxEditable`はこの作例では使用していない。PowerPoint実機表示も未確認。

[原典との差分](source/windows-export-adapter.diff)はWindowsの`spawn('marp')`を、環境変数`MARP_CLI_JS`指定時だけ同じMarp CLI JSのNode実行へ対応する。生成経路を別builderへ置き換えない。HTMLには原典hash controllerへ接続する0-based同一originの`yebisu-slide` / `yebisu-page` bridgeだけを追加する（[run_mcp.py](source/run_mcp.py)）。

## 字体・確認範囲

公式の未改変Shippori Mincho（見出し）、BIZ UDPGothic（本文）、Manrope（番号・時間）の実TTF/OFLを`fonts/`へ収録。[字体出所](fonts/SOURCE.json)を保持し、OS付属字体を抽出しない。MCP操作の入力と応答は再生成時に`source/logs/`へ保存する。

作例は原典build・生成/export成功、PDF6枚、主要出力の初回表示だけを確認した。ユーザーの範囲指定を優先し、全頁詳細目視・独立レビュー・構造監査・ZIP再実行を追加していない。原典のテーマ選択や編集用IDの工程は維持する。

## 単体の本文から使う

この本文は `skill-forks/marp-mcp-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/masaki39/marp-mcp/tree/2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `marp-mcp-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: masaki39 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/masaki39/marp-mcp/blob/2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f/LICENSE
