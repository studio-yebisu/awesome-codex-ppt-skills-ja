# 並べておくと、探し方が変わるの再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13を用意。PowerPoint描画を行う場合はPowerPointとpwshも必要。
3. 次を実行（キット内の原典と新しいPython仮想環境で生成します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/slide-maker/

PowerPoint本体でPNG/PDFを描画する場合は、游ゴシック（Yu Gothic）が利用できるWindows / PowerPoint / pwshを使用し、-Renderを指定します。生成したdeck.pptxをPowerPointで開きます。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典deckkit/native_chartでnative図とグラフを作る。入力のPython実探索、1〜15の全15通り、グラフ全30値、PowerPoint全5枚と独立critic/blind readを照合する。計画比較は制作後に追加した記録。完成例はselfread用途で、人による正式採用・投影可読性・全時系列工程の完走を主張しない。

## 原典と権利

https://github.com/addsumtech/slides_maker/tree/3767cc346d63ef1646082c87f15fbf0be582b152

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。
