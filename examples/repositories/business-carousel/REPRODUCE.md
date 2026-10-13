# 引き継ぎ、何を書けばいい？の再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13を用意。
3. 次を実行（キット内の原典指示を使った専用ソースとPython仮想環境で生成します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/business-carousel/

生成先で `python -m http.server 8000 --bind 127.0.0.1` を実行し、localhostのURLで正方形HTMLを開きます。原典の出力は構成確認用プレビューで、PPTX・PowerPoint描画は対象外です。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典43-carousel-brief-globalの指示型工程で、読み手とブランド条件、HookからCTAまでの構成、1枚1論点の原稿、図案と背景をブリーフにし、1080×1080のHTML構成確認プレビューを作る。原典に自動生成CLIやPowerPoint出力はない。SNS公開用の制作データ、人の承認、公開とは区別する。実績の証拠がない箇所は、架空の記入例を明示する。

## 原典と権利

https://github.com/minhnv0807/ai-business-skills/tree/0360adced422a08f70c3eff8905b81962872105d

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

自分の内容にはreproduce/workspace/examples/repositories/business-carousel/input/data.jsonの6枚の見出し・本文・ノートを変更して再実行できます。原稿確認と図案の調整を行い、公開用の仕上げ・人の承認は原典の次の工程として別途実施します。
