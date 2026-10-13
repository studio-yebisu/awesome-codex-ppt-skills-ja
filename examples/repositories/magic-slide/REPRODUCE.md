# 朝の支度を10分短くする企画の再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/magic-slide/

PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典のoutline/Brief Lite、モジュールHTML/CSS、merge、inject、serveとMagic Moveを使う。隣接ページで数字・準備品を意味に沿って受け渡す。認証関数のscopeだけを修正した日本語派生injectorを使い、原典と差分を保持する。cursor、dock、Overview、動き、serverの認証と保存先制限を保持する。表示用iframeと、原典serverでの編集・保存を案内し、agent QAと人のrevision/adoptionを区別する。

## 原典と権利

https://github.com/daniel-style/magic-slide/tree/e29d87cb315eb0afc939820b100d870eabf43f89

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

表示・編集・保存には、生成フォルダーで `python source/ja-runtime/scripts/serve.py index.html --no-open` を実行し、表示された /deck/ のURLを開きます。静的サイトのフロートは表示とページ移動の確認用です。原典の人によるrevision/adoptionはpendingとして残し、今回のagent QAを人の承認とは扱いません。
