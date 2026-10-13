# EC月次報告：売上と粗利を確かめるの再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/dashi-ppt/

PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典の1案経路でJSON→React/tsx→HTMLを実行する。theme05の日本語派生ではcopy値を図形寸法計算へ反映する。3+1経路のcopy検証不整合を記録し、検査を弱めて回避しない。PPTXエンジンは専有条件を持ち、別製品へ抽出しない。

## 原典と権利

https://github.com/chuspeeism/dashi-ppt-skill/tree/21dc7e5fc8c3a0d7f6a94948153dd1ee954f4e64

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

Dashi専有エンジンを分離再配布しません。スクリプトは完全な原典を固定commitで取得し、そのDashi skill内のHTML生成を実行します。PPTX/PDFエンジンの動作検証は今回の作例に含みません。
