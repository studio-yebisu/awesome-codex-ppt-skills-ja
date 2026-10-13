# carnot-tech/jinba-consulting-pptx-skill の日本語実行例

公式new_deck.pyでb01,b09,m05,b06,b05,m35,b10を選択し、HTMLを組み直して公式html_to_pptx.pyで変換。

組織・数値・担当者は架空。input/data.json、PROMPT.txt、NOTES.mdに入力・依頼・講稿を保存。

## 再現手順

カタログ全体を取得し、そのrootで次を実行します。

```powershell
git clone https://github.com/carnot-tech/jinba-consulting-pptx-skill .build/actual-upstreams/carnot-tech__jinba-consulting-pptx-skill
git -C .build/actual-upstreams/carnot-tech__jinba-consulting-pptx-skill checkout 692556fb84ba5a0609575a671dff3d346fefa041
python -m venv .venv
.venv\Scripts\python -m pip install python-pptx lxml Pillow
.venv\Scripts\python tools/build_japanese_repository_examples.py --only jinba --render
```

- Python 3.13 / python-pptx / lxml / Pillow
- Microsoft PowerPoint 16.0 と PowerShell 7（PNG/PDF描画）
- Node 22以降 / Google Chrome（原典HTML→PPTX変換）

元CLIのnew_deck → deck.html編集 → check_deck → html_to_pptx → check_deckを実行。source/seed.htmlは選択直後、deck.htmlは完成HTML。source/part-selection.jsonに対応表。

## 根拠と制約

PROVENANCE.jsonにcommitと原典ファイルSHA、environment.jsonに依存、QA.jsonとrender/powerpoint-render.jsonに検査範囲を保存。LICENSEは原文を保持。

- HTML図形は編集可能なPPTX要素へ変換。SVG/画像は原典仕様で画像になる。作例の棒グラフはCSS矩形。
- 原典converterのCSS zoom未反映を、追加パーツ2枚のPPTX文字サイズ・行間0.8倍で補正。source/conversion-corrections.jsonに記録。
- 元check_layout.mjsのブラウザ検査は実行せず、PowerPoint全ページ視認と座標検査で確認。本文の充填率49%・裏表紙15%のWARNを受容。
