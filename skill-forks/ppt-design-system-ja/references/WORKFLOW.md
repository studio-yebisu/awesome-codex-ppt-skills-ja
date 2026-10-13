# att6113/ppt-design-systemの日本語制作

原典: https://github.com/att6113/ppt-design-system/tree/9f39af607ab82da2827530c38b9dc86eb75768ee

原典HTMLテンプレート・Forest Ink配色・原典ナビゲーション

原典template.html、Forest Ink配色、cover・cards・body・question・comparison・closingのレイアウトを使う。固有ナビゲーションJSを保持し、日本語の行間・字体・同じ重要度の比較欄を調整する。HTTPで全ページとキー・dot操作を確認。HTML生成CLIは原典にないため、同梱Pythonは原典テンプレートを埋める再現入口である。PPTX出力と印刷は今回未検証。

## 作例

- 雨の日も迷わない、図書館イベント案内 / 6枚 / html
- カタログ内の案内: repository.html?repo=att6113/ppt-design-system
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=att6113/ppt-design-system
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3（生成。標準ライブラリのみ）
- Node.js 22+ と Chrome/Edge（任意の描画検証）
- 閲覧端末の日本語フォント

## 元の制作コマンド

    python source/reproduce.py --input input/data.json --render

## 確認範囲

- 実行したのはHTML出力経路。PPTX出力は未検証。
- 全6ページを1920×1080で確認。スマートフォン縦画面・印刷は未検証。
- 日本語フォントは端末依存。フォントファイルは再配布しない。
- 原典にHTML生成CLIはなく、同梱Pythonで原典テンプレートを埋める。
- エージェント確認済み。人による正式採用は未承認。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
