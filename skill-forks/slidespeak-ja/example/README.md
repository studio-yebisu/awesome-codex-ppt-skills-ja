# 本の向こうへ。

架空の独立書店「余白書店」の仮リブランディング案、6ページ。緑のベタ、生成り、大きな和文、開いた本のコード図形、長い罫線で、店の言葉から試行の順序へつなぎます。実在書店の実績・実施決定・効果の主張は含みません。

原典SlideSpeak engineを実使用。独自briefからtokens/chrome/components/grammarを作者が設計し、Solが作成したslide-treeをLLMClientインターフェースへ渡し、原典loadSkill/generateDeck/validateSlideTree/rendererで生成。外部LLM/API/FALは呼びません。既存presetの名前借りや共通rendererへの置換ではありません。

`deck.html` は原典renderer出力。`index.html` は同じ出力に1920×1080再生とサイトframe連携だけを追加。書体はフルTTFを内包し、OFL原文をfonts/に同梱。原典MIT・engine sourceはupstream/に保持。

再生成: `cd upstream` → `npm ci` → `cd ..` → `node upstream/node_modules/tsx/dist/cli.mjs build.mts`。styleを変えるときはstyles/green-book-editorialの6ファイルとinput/slide-tree.jsonを編集。スタイルgate: `node upstream/node_modules/tsx/dist/cli.mjs upstream/scripts/validate-skill.ts styles green-book-editorial`（stylesを絶対パス指定可）。必要なruntimeは通常Node OSS依存だけ。

原典gateを実行し、全ページの改行・図・ページ移動を確認して直す。現在の実施範囲はQA.jsonへ記録する。独立再評価と区別する。

## 2026-10-15 修復と確認

引用・工程・結びの文章を意味単位で改行し、上下の罫線幅を統一。全6頁を1280×720で確認した。原典style検査1/1、occupancy/legibility6/6、richness4/4を現HTMLで再実行し通過。元engineのhashはsource/original-source-check.jsonへ記録。Windowsの実行パス/file URLだけをadapterへ分け、採点関数は変更していない。

ブリーフから、この作例専用の6ファイルstyleとslide-treeを作者が用意し、原典APIへ渡した。外部LLMへ原稿生成を依頼する部分、AI/stock画像、編集可能PPTXは実行していない。独立再評価は未了。ZIP再実行の結果はQA.jsonを参照。
