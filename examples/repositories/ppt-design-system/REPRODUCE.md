# 雨の日も迷わない、図書館イベント案内の日本語派生・再現キット

標準生成はPython3の標準ライブラリだけで実行します。Webの書体は端末の游明朝・游ゴシックなどを使用し、フォントファイルは配布しません。

1. ZIPを展開してPowerShellを開く。
2. `.\reproduce\Reproduce.ps1` を実行。
3. 出力は `reproduce/workspace/examples/repositories/ppt-design-system/deck.html`。新出力のQAは確認前です。
4. そのフォルダーで `python -m http.server 8000 --bind 127.0.0.1` を実行し、`http://127.0.0.1:8000/deck.html` で全ページを確認します。

`-Render` を追加すると、Node.js22以上とインストール済みChrome/EdgeでHTTP描画・原典操作を検査します。

原典template.html、Forest Ink配色、cover・cards・body・question・comparison・closingのレイアウトを使う。固有ナビゲーションJSを保持し、日本語の行間・字体・同じ重要度の比較欄を調整する。HTTPで全ページとキー・dot操作を確認。HTML生成CLIは原典にないため、同梱Pythonは原典テンプレートを埋める再現入口である。PPTX出力と印刷は今回未検証。

自分の内容にはinput/data.jsonの見出し・本文HTMLを更新し、日本語SKILLと原典レイアウトを使って調整します。6ページ・Forest Inkの再現用経路で、他テーマ・PPTX・印刷の対応を確認したものではありません。原典MIT表示を保持し、正式採用と公開は未実施です。
