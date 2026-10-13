# Gitの保存・記録・共有の再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/codex-image-ppt/

PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典spec/style/jobs/stateを経てCodex native image_genで各ページを実生成し、原典assemble_ppt.pyで組む。画像を個別編集可能なPPTXと呼ばない。toolが公開していないモデル名を推測しない。sample採用は制作エージェントの判断と記録し、人の承認と偽らない。

## 原典と権利

https://github.com/ningzimu/codex-ppt-skill/tree/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

このスクリプトは生成済みの3画像を原典assemble_ppt.pyで組み直すだけです。画像を新たに作るには、promptsとstyleを添えてCodex native image_genへ依頼し、原典のjobs/result記録と画像確認を行ってください。APIや画像生成をこのスクリプトから自動実行しません。
