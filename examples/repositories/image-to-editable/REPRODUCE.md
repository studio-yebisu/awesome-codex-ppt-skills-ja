# 画像から編集できるGit入門への再現キット

完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。

## Windowsで同じ作例を生成

1. ZIPを展開。PowerShellでこのフォルダーへ移動。
2. Python 3.13、Node.js、必要に応じてGit Bashを用意。
3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。

    .\reproduce\Reproduce.ps1

生成先: reproduce/workspace/examples/repositories/image-to-editable/

PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。

## 自分の題材へ

完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。

原典editpptのprepare→page worker→build/validate→record→finalizeで画像を再構成する。Codex内蔵image_genで分離したアイコンはbitmapとして保持し、本文・カード・単純な矢印をnative要素にする。新規案内ノートは元画像からの抽出と区別し、本文XMLと画像を保って追加する。再出力kitは保存済みmanifest・分離済み画像の再利用で、新規画像編集ではない。元画像との比較と実PowerPoint描画、編集範囲を確認する。

## 原典と権利

https://github.com/ningzimu/image-to-editable-ppt-skill/tree/b7be494e31a0ed56ef98716891db5474606b8cdf

原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。

この再出力は保存済みのpage manifestと分離済みアイコンを原典CLIで組み直します。新しい画像編集やworkerを再実行するものではありません。新規入力は日本語SKILLと原典のbuiltin-imagegen/worker契約から制作します。本文・図形とbitmapの編集範囲を区別し、元画像と比較してください。原典CLIのPyMuPDF等には個別の依存ライセンスがあります。
