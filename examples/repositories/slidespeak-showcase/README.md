# 本の向こうへ。

架空の独立書店「余白書店」の仮リブランディング案、6ページ。緑のベタ、生成り、大きな和文、開いた本のコード図形、長い罫線で、店の言葉から試行の順序へつなぎます。実在書店の実績・実施決定・効果の主張は含みません。

原典SlideSpeak engineを実使用。独自briefからtokens/chrome/components/grammarを作者が設計し、Solが作成したslide-treeをLLMClientインターフェースへ渡し、原典loadSkill/generateDeck/validateSlideTree/rendererで生成。外部LLM/API/FALは呼びません。既存presetの名前借りや共通rendererへの置換ではありません。

`deck.html` は原典renderer出力。`index.html` は同じ出力に1920×1080再生とサイトframe連携だけを追加。書体はフルTTFを内包し、OFL原文をfonts/に同梱。原典MIT・engine sourceはupstream/に保持。

再生成: `cd upstream` → `npm ci` → `cd ..` → `node upstream/node_modules/tsx/dist/cli.mjs build.mts`。styleを変えるときはstyles/green-book-editorialの6ファイルとinput/slide-tree.jsonを編集。スタイルgate: `node upstream/node_modules/tsx/dist/cli.mjs upstream/scripts/validate-skill.ts styles green-book-editorial`（stylesを絶対パス指定可）。必要なruntimeは通常Node OSS依存だけ。

初回の生成・原典gate・主画面だけを確認。全ページ詳細目視・独立レビュー・ZIP再実行はしません。
