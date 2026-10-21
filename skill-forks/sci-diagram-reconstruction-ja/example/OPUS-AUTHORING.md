> 初回Opus執筆時点の記録。下記の「未実施」はその執筆時点を指す。後続のCodexによる実行・検査・配布再実行は現在のQA.jsonとsource/distribution-replay.jsonに分けて記録する。新規Opus制作とは扱わない。

# Opus 作成記録：SciDiagram PPTX 復元 pass-01

- モデル：`claude-opus-5-5`
- 上流スキル：HututuWorks/sci-diagram-pptx（`cc8f0030edf80eeab6e52849b8c39fe638466776`）
- ルート：Reconstruction／ランタイム：`pptxgenjs` 4.0.1（`SCI_DIAGRAM_RUNTIME=pptxgenjs` の明示指定）

## 実施したこと

1. **画像入力の解析**：`pass-01/source.png`（1600×900）を原寸のまま画像として読み、四つの箱、四本の有向矢印、タイトル、注記の文言・位置・色を読み取った。座標は PNG から読んだ値で、`authored-source.svg` は参照していない。
2. **上流ファイルの読解**：SKILL.md、reconstruction.md、runtime-pptxgenjs.md、pptxgenjs-build-template.mjs を読み、それぞれの指示を適用した。
3. **インベントリの作成**：`input/reconstruction-inventory.json` に、意味ノード 4、有向エッジ 4（from／to／座標／ラベル）、独立注記 2（タイトル・注記）を記録した。見えている語と矢印は、すべてネイティブ所有者にちょうど一つずつ割り当てている。
4. **ネイティブ復元用ビルドの作成**：`pass-01/build.mjs` を書いた。本体はテンプレートのままで、変えたのはデータとラベルの書式だけ。テンプレートの検証処理、変換関数 `toSlidePoint`／`toSlideBox`、`connectExactPath`／`connectOneWay`／`connectBothWays`、相対パスでの素材解決、既存ファイルを黙って上書きしない仕組みは残した。

## 書式と構造の判断

- スライドは 1 枚で、13.333333×7.5 in。1 px＝0.6 pt で換算し、タイトル 31.2pt、箱 21.6pt、矢印ラベル 19.2pt、注記 16.2pt とした。書体は Yu Gothic。
- 箱はネイティブの矩形と別個のテキストボックスで構成した。矢印は直線の line 図形 4 本で、矢じりは終点側の `endArrowType` に付けている。矢印ラベルは白地のテキストボックスにした。
- タイトルと注記は `type: "textbox"`、`role: "annotation"` とし、塗りの板を付けない。エッジがつなげるのは `role: "semantic"` のノードだけになるよう、検証処理を拡張した。
- `INSETS` は空にした。source.png はスライドに埋め込んでおらず、参照用やトレース用のスライド、非表示スライドも作っていない。

## 未実施・範囲外

- このモデルにはシェル実行の手段がないため、Opus は build.mjs を実行していない。`editable.pptx` の生成、LibreOffice での描画、`check_pptx.py` による検査は、作成とは別の工程で行う。現時点で成功は主張しない。
- 作業時間の短縮、任意の図の復元、ピクセル単位の一致、見た目の改善は示していない。
