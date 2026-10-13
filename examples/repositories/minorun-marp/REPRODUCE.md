# Gitの変更、どこに保存された？の再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/minorun-marp/

PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

元の日本語3スキル（story・figures・dark design）を読み、問いと段階的な図解を作る。原典minorun-darkテーマでMarp CLIを実行し、check-ai-smellも実行する。

## 原典と権利

https://github.com/minorun365/minorun-marp-skill/tree/736fd5e9fafb80148a1e6eaa5ae5f9d859431257

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

固定npm依存の監査記録はsource/dependency-qa.jsonです。Marp CLI側の依存に未修正の検出項目があります。今回の再現は同梱した原稿のHTML生成を対象とし、サイトのHTTPサーバーではこのCLIを実行していません。
