# FAQを育てる4週間

原典en-context-engineeringのReact App、SlideLayout、useSlideScale、Framer Motion variantsを使った日本語5枚。原典のtraining-cycleとBold Signal配色を採用。4週間・10問は架空の企画目標です。

## 再現

Python3.13とNode.js24（npm同梱）を用意し、配布キットのreproduce/Reproduce.ps1を実行。制作ソースはsource/app/src/content.jsonとslides/deck.tsx。原稿に合わせた図の配置も編集します。スキルの質問工程は今回の依頼で承認された実例制作の目的から題材とスタイルを選び、input/BRIEF.mdに記録しました。

index.htmlはHTTPで配信してください。ファイルのダブルクリックによるES Module表示は保証しません。npm run devは開発用、npm run buildは配布用。外部AI APIや画像生成は使っていません。

原典の英字フォントを公式配布の日本語フォントへ替え、フォントを同梱。スライドの遷移と内部の週別タブはReactの実状態です。日本語の原稿、ノート、原典hash、局所diff、実行ログと表示QAを保存します。
