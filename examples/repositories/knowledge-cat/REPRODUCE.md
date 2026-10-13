# 迷わない議事録のまとめ方の再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1 -ArtifactWorkspace "artifact-tool workspaceのパス" -NodePath "node.exeのパス"

生成先: reproduce/workspace/examples/repositories/knowledge-cat/

PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典native-pptx laneの専用build_native_pptx.mjsと原典plan/text/editability/probeを実行する。Codexのartifact-tool作業環境を指定し、本体は複製しない。日本語action-title警告を消さず、本文の命題を実読する。出力の固定デモラベルとNoto Sans JPを局所化。

## 原典と権利

https://github.com/gnipbao/knowledge-cat-ppt-skill/tree/889c3dc00b356607fa9af935eb807056c3394886

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

原典native出力には、Codexに同梱される@oai/artifact-toolを解決できる既存workspaceが必要です。Codexのload_workspace_dependenciesで確認し、node_modules/@oai/artifact-toolを持つNode workspaceを指定してください。本体・node_modulesはZIPに複製していません。任意のpublic npm installで代替する案内ではありません。
