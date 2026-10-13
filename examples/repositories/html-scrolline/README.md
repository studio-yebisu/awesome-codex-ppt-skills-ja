# Scrolline v2 日本語実行例

原典 [gongnyang/awesome-html-scrolline-deck](https://github.com/gongnyang/awesome-html-scrolline-deck/tree/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc) の連続スクロールエンジンで作った6停止点の資料です。静止画を切り替える方式ではなく、レール・月の数字・注目項目が原典のmoveで移り、前後の段階をhandoffでつなぎます。

[資料を開く](deck.html) / [説明付きプレビュー](index.html) / [入力](input/data.json) / [再実行](REPRODUCE.md) / [QA](QA.json) / [個別ライセンス](licenses/README.md)

スクロール、左右矢印、Home、Endで進めます。localhost HTTPで全6停止点と実キー・ホイール操作を確認しました。原典コードのengine、moves、conceptsは無改変。日本語の文章・フォント・開始位置をdeck側で指定しています。

原典の全体CIはWindowsパスに関する3テストが失敗しました（499成功）。日本語資料のsmokeは全項目0、原典エンジン・動作・コンセプトの424テストは成功しています。原典の全ゲート完了とは区別した、日本語派生の確認済み作例です。

写真展と年月は架空です。MP4出力、印刷、スマートフォン縦画面、人による正式採用は未確認です。原典MITと、組み込まれたGSAP独自ライセンス・Lenis MITはそれぞれ保持しています。
