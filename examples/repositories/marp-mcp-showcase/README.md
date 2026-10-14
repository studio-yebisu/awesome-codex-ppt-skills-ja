# ひとつの服を、もう一度。

原典masaki39/marp-mcpの実MCPサーバーで生成した、日本語6枚の架空ワークショップ企画。開催・効果・売上の実績はなく、120分の行程も企画設定。

主出力は[index.html](index.html)。[PDF](deck.pdf)は固定レイアウトで、[PPTX](deck.pptx)は各スライドを画像として収めたもの。PowerPointの文字・表・図形としての編集はできない。編集正本は[deck.md](deck.md)、[構造化入力](input/content.json)、[局所CSS](source/workshop.css)。

原典の`minimal`を選び、title / two-column / content / table / big-statementの実テンプレートと原典CSSを使用した。大見出し・細い区切り・表・明暗の構図を保持し、森色・生成り・土色へ変更。布と縫い目を思わせる図形はCSSで描いた。見出しはShippori Mincho、本文はBIZ UDPGothic、番号・時間はManrope。実TTFとOFLを[fonts/](fonts/SOURCE.json)に収録し、Marp出力には未改変字体をdata URLとして埋め込んだ。

## 再生成

Node.js 18以上、Python 3、PyMuPDF、Chrome/EdgeなどMarp CLI対応ブラウザが必要。`source/runtime/`は原典TypeScriptとコンパイル済みJSを保持し、node_modulesとブラウザ本体は含めない。

```powershell
npm --prefix source/runtime ci --ignore-scripts --no-audit --no-fund
npm --prefix source/runtime install --ignore-scripts --save-dev --save-exact @marp-team/marp-cli@4.4.0
node source/runtime/node_modules/typescript/bin/tsc -p source/runtime/tsconfig.json
python -m pip install PyMuPDF
python source/run_mcp.py --case . --runtime source/runtime --node node --marp-cli source/runtime/node_modules/@marp-team/marp-cli/marp-cli.js
```

`run_mcp.py`はstdio JSON-RPCでinitializeし、`list_themes_and_styles`、`list_layouts`、`create_presentation`、`set_frontmatter`、`manage_slide`、`generate_slide_ids`、`read_slide`、`export_slide`を実行する。操作記録は[source/logs/mcp-operations.json](source/logs/mcp-operations.json)。入力・出力パスは実行環境の絶対パスへ展開する。再生成時は前のdeck.mdをログ側へ保存して新規作成する。

## 原典と局所差分

原典は[固定commit](https://github.com/masaki39/marp-mcp/tree/2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f)、[MIT](LICENSE)。[未変更原本](source/upstream/skills/marp/SKILL.md)と[Windows adapter差分](source/windows-export-adapter.diff)を保存した。原典`spawn('marp')`はWindowsのnpm .cmd shimを直接実行できないため、`MARP_CLI_JS`指定時のみ同じMarp CLIのJSをNode実行する。生成器を別のbuilderへ置き換えていない。

日本語CSSと字体埋め込みはMCPで作ったMarkdownへ追加する局所拡張。HTML出力後には、同一originかつ親iframeからだけ受け付ける0-based `yebisu-slide`入力 / `yebisu-page`通知を追加した。bridgeは[source/run_mcp.py](source/run_mcp.py)に収録。

[SOURCE](SOURCE.json)、[制作記録](PROVENANCE.json)、[軽い確認](QA.json)に範囲を記録。原典build・MCP生成/export成功、PDF6枚、表紙PNGの初回表示まで。全頁詳細目視・独立レビュー・構造監査・ZIP再実行は実施していない。PPTXは原典exportが成功した画像版で、PowerPoint実機での表示確認は行っていない。
