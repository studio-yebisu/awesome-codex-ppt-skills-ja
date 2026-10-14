# ブランド抽出後の版式選択

原典Step1のbrand guide extractionをBRAND.mdから行い、brand-record.jsonへ固定しました。

| 頁 | 一つの役目 | 実使用する原典pattern |
|---|---|---|
| 1 | 企画の入口 | s1 title/wordmark + 大見出し + 自作紙SVG |
| 2 | 文字を眺める体験 | s2 split-panel + pain rowsを観察ポイントへ変更 |
| 3 | 選ぶ→並べる→刷る | s3 approach-grid/approach-num/body、3段階 |
| 4 | 余白を眺める | s4 dark statement + large display quote、紙の対比図 |
| 5 | 紙とインクを眺める | s5 split-panel + feature-bar、ローラーSVG |
| 6 | 自分の一枚を持ち帰る | light close、元display/label/reveal、短い問い |

原典exampleのCSS全文、deck/slide/nav/rotate-overlay/print構造を使う。inline JSは算術・fullscreen・hash/session・dots・auto-hide・swipeを変更しない。親への小bridgeはcontroller末尾へ追加する。

原典のremote Cormorant/DM Sansは、ブランド指定の実TTFを埋め込むlocal @font-faceへ変更。日本語の行高・字間と本文サイズ、色、薄い赤の使い方だけをlocal CSSへ分ける。画像API・生成API・共通rendererは使わない。

確認: 必要な単一HTML梱包、初回表紙/主要内部頁の表示、元navigation1→2、短いSKILL quick_validateのみ。全頁詳細検査・採点・ZIP再実行はしない。
