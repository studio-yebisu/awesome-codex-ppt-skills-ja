# 地域カフェの朝営業を試すの再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/ppt-design-skill/

PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。reproduce/workspace/examples/repositories/ppt-design-skill/input/data.jsonの価格、日数、仮定販売数、見出し、講稿を変えて再実行できます。別の構成や題材には、原典Build Modeのbrief/page-plan/theme-lockを作り、公開部品でページを配置します。

原典Build Modeのtask初期化、ThemeComposer、strict Presentationと公開text/shapes/bar_chartを使う。日本語の色名aliasと見出しフォントを明示解決し、入力JSON・テーマlock・講稿を残す。売上試算と利益、未収集とゼロを区別する。原典と公開engineは無改変。編集可能な本文と図形をPowerPoint本体で描画して確認する。

## 原典と権利

https://github.com/sunchaokun/PPT-Design-Skill/tree/cbf7ef1324a026b29e2b77b71e2034554ddd3e22

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。
