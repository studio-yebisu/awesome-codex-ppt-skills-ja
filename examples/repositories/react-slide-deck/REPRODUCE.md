# FAQを育てる4週間の再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/react-slide-deck/

React版はHTTPで表示します。生成先へ移動して `python -m http.server 8000 --bind 127.0.0.1` を実行し、表示されたlocalhostのURLを開いてください。PPTX・PowerPoint描画の-Renderには対応しません。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典en-context-engineeringのReact App、SlideLayout、useSlideScale、Motion variantsで制作する。training-cycleとBold Signalを保持し、CJK字体、reduced-motion、週別タブ、ページ同期を補う。原典依存のVite8/Tailwind4.2.1衝突はTailwind4.2.2への最小補正で解消し、元lockと差分と固定再現lockを保存。HTTPで表示する。

## 原典と権利

https://github.com/code-on-sunday/slide-deck-generator/tree/a6369f31b0cc4dd5830796455326777a8fe4c7c6

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

Windowsではフォント用のnative DLLが深いパスで読み込めないことがあります。ZIPを短いパス（例 M:\slides\react-deck）へ展開してください。NodeがPATHにない場合は `-NodePath "node.exeの絶対パス"` を指定します。元Vite8を保持し、互換性のあるTailwind4.2.2と記録したlockでnpm ciを実行します。
