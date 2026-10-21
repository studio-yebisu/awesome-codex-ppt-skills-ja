# 元のMCPと、この日本語作例の局所調整

`build_mcp.py`は固定版の`ppt_mcp_server.py`をstdioで起動し、実際のMCPツールを95回呼ぶ。`mcp-calls.json`に引数と返答を保存する。PPTX作成、文字、2表、2データ連動チャート、`before_after_comparison`の適用は原典のツールで行う。原典ファイルは改変しない。

生成後の`language_and_notes`は次だけを明示的に補う。これらを元MCPの実装済み機能と読み替えない。

- 日本語の固定表示と講稿：`负责人`を`担当`へ変更し、ja-JPとBIZ UDPGothicを指定する。講稿は同梱の架空入力から加える。
- `add_chart`が引数`legend_position`を反映しないため、python-pptxで凡例を下に置き、plot領域への重なりを止める。系列の斜線・塗り分けと数値表示、差額チャートの軸サイズも同じ互換層で指定する。データは変更しない。
- `format_table_cell`が`vertical_alignment`を保存しないため、セルを縦中央にする。
- `manage_text(format_runs)`が先頭へ空段落を残すため、4頁の対象3文字箱の空段落だけを除く。
- 原典比較テンプレートは横幅10インチの固定座標なので、13.333インチ幅への水平比例変換を行う。テンプレートの左右見出し・本文・データを維持する。原典APIに削除/座標変更の操作がないため、意味を担わない中央の楕円と「比較」文字、下の行き先のない矢印を除去し、見出しと注記の位置を他頁へ合わせる。この調整は原典API単独の機能とは扱わない。
- python-pptxのチャート`Font.name`はLatinしか設定しない。チャートの既存文字属性へEast Asian familyとja-JPを加え、日本語がMS Gothicへフォールバックするのを防ぐ。

編集性は`check_native_edit.py`で別コピーを開き、本文変更、チャート1点220→221、保存、文字抽出を元MCPの5操作で検証する。`native-edit-check.json`は元PPTXのSHAが変わらないことも検査する。GUIからの編集検査は実施していない。
