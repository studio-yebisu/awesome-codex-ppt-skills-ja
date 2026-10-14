# Marp MCP・日本語キット

[SKILL.md](SKILL.md)から始める。原典MIT、字体は各OFL、出所は[SOURCE.json](SOURCE.json)。原典TypeScript・build済みJSと局所adapter、6枚の構造化入力、CSS、実TTF/OFL、stdio操作用Pythonを収録する。node_modules、ブラウザ、キャッシュは含めない。

必要条件はNode.js 18以上、Python 3/PyMuPDF、Chrome/EdgeなどMarp CLI対応ブラウザ。

```powershell
npm --prefix source/runtime ci --ignore-scripts --no-audit --no-fund
npm --prefix source/runtime install --ignore-scripts --save-dev --save-exact @marp-team/marp-cli@4.4.0
node source/runtime/node_modules/typescript/bin/tsc -p source/runtime/tsconfig.json
python -m pip install PyMuPDF
python source/run_mcp.py --case . --runtime source/runtime --node node --marp-cli source/runtime/node_modules/@marp-team/marp-cli/marp-cli.js
```

`input/content.json`と`source/workshop.css`を編集する。実MCPサーバーのtools/callでdeck.mdを作り、原典export_slideでHTML/PDF/画像主体PPTXを出力する。HTMLには同一originの小さなbridgeを加える。画像PPTXの文字・表・図形はnative編集不能。実験的editable PPTXは使っていない。

このキットは架空の衣服お直しワークショップ作例。開催・効果・売上の実績はなく、120分は仮の企画設定。完成物と今回の操作ログはサイト側の[制作一式ZIP](../../downloads/marp-mcp-example-ja.zip)で別配布する。この相対リンクはサイト配置用。
