# 雨の日も迷わない、図書館イベント案内

架空の図書館・読書会を題材にした日本語6ページ。`deck.html`（`index.html`も同一内容）が完成物です。原典 att6113/ppt-design-system のHTMLテンプレート、Forest Ink配色、レイアウトとページ移動JSを実際に使用しています。

## 再生成

```sh
python source/reproduce.py --input input/data.json --render
```

Python 3、描画にはNode.js 22+とChrome/Edgeが必要です。生成だけなら`--render`を外せます。npm・APIキー・有料サービスは不要。ブラウザの自動検出ができなければ`--chrome`へ実行ファイルを指定します。

`input/data.json`の本文は信頼できるローカルHTMLとして扱います。原典テンプレートは`source/upstream/assets/template.html`に無改変で保持。日本語向けの文字サイズ・行間、端末フォント、配色を`source/reproduce.py`で適用します。原典の矢印キー、横スクロール、下部ドットを保持。カタログ用メッセージ橋渡しは別スクリプトです。

再生成時はQAを必ず`generated_awaiting_review`に戻します。自動描画が通っても目視レビュー済みにはなりません。完成物は6ページの全画像をエージェントが確認しました。人による採用・公開は未実施です。

`PROVENANCE.json`に原典コミット、参照SHA、実行ログを記載。`render/report.json`にページ境界と操作結果、`review/template-proof.json`に原典JS保持、`review/portable-proof.json`に別フォルダ再現結果があります。原典MIT通知は`licenses/LICENSE-upstream.txt`です。フォントは同梱しません。

確認範囲は1920×1080のHTTP表示。PPTX出力・印刷・スマートフォン縦画面は未検証です。
