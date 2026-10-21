# 操作の説明を問いと段階図に変え、保存・選択・記録・共有の違いを追える。

入力：Gitを初めて使う人への5分の導入原稿と4段階の図。
出力：minorun-darkのMarp原稿・HTML・9頁PDFとPNG。

この日本語作例は原典の固定ソースを使った紹介用の試作です。修復後の全9頁をCodexが実描画で確認しました。独立したKimi K3 / Opus5.5の再採点と人の採用判断は別です。

## 使い方

1. 5分の導入範囲と読み手をinput/BRIEF.mdで確定する
2. deck.mdで問いと回答を続け、見出しを一行にする
3. 段階SVGで既存の箱の位置を保って一要素ずつ足す
4. source/rebuild.pyへMarp CLIとブラウザーの場所を渡す
5. check-ai-smell --allとPDF全頁を確認する

## 生成・検査

`python source/rebuild.py --marp <marp-cli.js> --node node --browser <Chrome-or-Edge>`

2頁の孤立文字を一行の問いへ修正。図のラベル・矢印を拡大して埋込書体を適用。表紙の白文字を黒地内へ移動。 実行記録と画像hashはQA.json、出所はPROVENANCE.jsonと原典LICENSEを参照してください。

## 範囲

- 元35分教材のうち5分の導入抜粋。元依頼は入力内へ保存
- 20分演習・ブランチ・レビュー・競合解消は扱わない
- Gitコマンドは説明例で、リモート送信はしていない
- 本文を変えたときは埋込サブセット書体の収録文字も更新する

## 実行環境

Python 3、Node 24、@marp-team/marp-cli 4.4.0、既存Chrome/Edge。元themeとフォントを含むdeck.md・imagesを入力にする。HTMLの言語とサイト用bridgeのみ再付与する。

配布ZIPの展開後再実行はsource/zip-replay.jsonに記録。依存の導入・ブラウザーの実行パスは受け手の環境へ合わせる。
