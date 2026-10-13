# carnot-tech/jinba-consulting-pptx-skillの日本語制作

原典: https://github.com/carnot-tech/jinba-consulting-pptx-skill/tree/692556fb84ba5a0609575a671dff3d346fefa041

公式new_deck.pyでb01,b09,m05,b06,b05,m35,b10を選択し、HTMLを組み直して公式html_to_pptx.pyで変換。

原典new_deckで固有パーツを展開してから日本語を組み、原典html_to_pptxで変換する。追加パーツ2ページの文字サイズ・行間の0.8補正は作例のconversion-corrections.jsonに記録。原典の検査を削除しない。

## 作例

- くらし便 EC事業 9月報告 / 7枚 / pptx
- カタログ内の案内: repository.html?repo=carnot-tech/jinba-consulting-pptx-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=carnot-tech/jinba-consulting-pptx-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13 / python-pptx / lxml / Pillow
- Microsoft PowerPoint 16.0 と PowerShell 7（PNG/PDF描画）
- Node 22以降 / Google Chrome（原典HTML→PPTX変換）

## 元の制作コマンド

    git clone https://github.com/carnot-tech/jinba-consulting-pptx-skill .build/actual-upstreams/carnot-tech__jinba-consulting-pptx-skill

    git -C .build/actual-upstreams/carnot-tech__jinba-consulting-pptx-skill checkout 692556fb84ba5a0609575a671dff3d346fefa041

    python -m venv .venv

    .venv\Scripts\python -m pip install python-pptx lxml Pillow

    .venv\Scripts\python tools/build_japanese_repository_examples.py --only jinba --render

## 確認範囲

- HTML図形は編集可能なPPTX要素へ変換。SVG/画像は原典仕様で画像になる。作例の棒グラフはCSS矩形。
- 原典converterのCSS zoom未反映を、追加パーツ2枚のPPTX文字サイズ・行間0.8倍で補正。source/conversion-corrections.jsonに記録。
- 元check_layout.mjsのブラウザ検査は実行せず、PowerPoint全ページ視認と座標検査で確認。本文の充填率49%・裏表紙15%のWARNを受容。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
