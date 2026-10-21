# 再生成

この作例の現在の正本はsource内の入力・CSS・helperです。Node/Pythonと必要な依存・ブラウザーを別途用意します。依存キャッシュは配布に含めません。

PythonにはPyMuPDFが必要です。source/run_mcp.py --case . --runtime source/runtime --node <node> --marp-cli <marp-cli.js>で3形式を作ります。source/check_cli.pyは元CLIを別の2頁で確認する補助です。source/runtimeは原典に保存したWindows export adapterだけを適用しています。

全頁を実表示して字体・重なり・頁送りを確認し、実行ログを現在の出力へ束縛して保存します。
