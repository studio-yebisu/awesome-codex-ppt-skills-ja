# addsumtech/slides_makerの日本語制作

原典: https://github.com/addsumtech/slides_maker/tree/3767cc346d63ef1646082c87f15fbf0be582b152

原典deckkit・native_chart / Pythonで実行した探索トレース

原典deckkit/native_chartでnative図とグラフを作る。入力のPython実探索、1〜15の全15通り、グラフ全30値、PowerPoint全5枚と独立critic/blind readを照合する。計画比較は制作後に追加した記録。完成例はselfread用途で、人による正式採用・投影可読性・全時系列工程の完走を主張しない。

## 作例

- 並べておくと、探し方が変わる / 5枚 / pptx
- カタログ内の案内: repository.html?repo=addsumtech/slides_maker
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=addsumtech/slides_maker
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.10+ / python-pptx, pymupdf, Pillow, matplotlib, numpy
- Yu Gothic / Consolas
- PowerPoint（今回の描画QA）

## 元の制作コマンド

    python tools/build_slide_maker_repository_example.py

## 確認範囲

- 読んで学ぶ教材として全5枚を確認。大きな会場での投影可読性は未確認。
- Pythonで1〜15の全15通りを実行。探索回数の比較で、秒数や並べ替えの費用は測定していない。
- 構成・デザインの比較は初回制作後に補完して記録。原典が求める制作前の全工程を完走した表示ではない。
- 別エージェントの内容・表示レビューと、制作の経緯を知らせない読み取りレビューを実施。原典の引き渡し検査を通過。
- 正式採用・外部公開は未実施。自分の原稿で作り直した出力は、改めて全ページを確認する。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
