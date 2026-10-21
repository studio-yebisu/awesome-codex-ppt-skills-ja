# 説明原稿をブラウザーで順に見せる資料にし、同じ内容をPDFでも配れる。

入力：社内文書30件を4週間で試す架空の検索企画と講稿。
出力：reveal.jsのHTML・原典Decktapeの6頁PDFと画像。

この日本語作例は原典の固定ソースを使った紹介用の試作です。修復後の全6頁をCodexが実描画で確認しました。独立したKimi K3 / Opus5.5の再採点と人の採用判断は別です。

## 使い方

1. 話す順番と枚数を決め、create-presentation.jsで骨格を作る
2. 本文はp要素、2列はinline gridで書く
3. 項目の関係は矢印、表の見出しと行は色と罫線で分ける
4. 原典check-overflow.jsを実行する
5. Decktapeで全頁画像とPDFを出し、実表示を確認する

## 生成・検査

`node source/upstream/skills/revealjs/scripts/check-overflow.js index.html`
`npm ci --prefix source/qa --ignore-scripts`
`node source/qa/node_modules/decktape/decktape.js reveal --chrome-path <browser> --screenshots --screenshots-directory render/decktape <HTML-URL> deck.pdf`

二列の見出し間隔、関係図の線と矢印、表の見出し色と行罫線を修正。原典overflowとDecktapeを実行し6頁を確認。 実行記録と画像hashはQA.json、出所はPROVENANCE.jsonと原典LICENSEを参照してください。

## 範囲

- 原典scaffold後の日本語組版は専用の手作業実装
- fragment・縦方向の入れ子・PDFからの逆変換は未実演
- 企画の数値は架空の条件と目標で、効果実績ではない
- Decktape3.16.1を同caseのQA依存へ固定。ブラウザーは既存Edgeを指定

## 実行環境

Node 24、既存Chrome/Edge。PUPPETEER_SKIP_DOWNLOAD=trueとしてnpm ci --prefix source/qa --ignore-scriptsを実行する。python source/verify.py --browser <Chrome/Edge実行ファイル>で無改変の原典overflowとDecktapeを実行できる。puppeteer25.13.0とDecktape3.16.1をlockへ固定。QA用依存でありHTML配信時は不要。

配布ZIPの展開後再実行はsource/zip-replay.jsonに記録。依存の導入・ブラウザーの実行パスは受け手の環境へ合わせる。
