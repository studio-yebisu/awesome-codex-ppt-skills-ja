# 仕事の引き継ぎを、迷わない一枚に。

架空の社内運用を説明する6枚。引継ぎメモそのものを一枚に整える方法を、関係・順番・表・判断条件に分けて説明します。人名・会社名・実測値を使用せず、期限は相対的な仮案、状態は説明用の例です。

## 使用した原典と編集範囲

[siril9/presentation-skill](https://github.com/siril9/presentation-skill/tree/efd899c5ddf866af2ce0001c4c9340af775d4d55) / MIT / `efd899c5ddf866af2ce0001c4c9340af775d4d55`。
原典 `present.py brief` で選んだ `lavender-ops / operations-grid` 候補とreadability contractをJSONへ引き継ぎ、原典 `build_deck_pptxgenjs.js` に入力します。原典のrender-plan、role-layout contracts、templates/pptxgenjsを実際に実行したnative PPTXです。Python-pptxの別generatorやホストartifact-tool SDKは使っていません。

`flow_steps` は原典schemaが対応するnative図解、timelineはnative図形、状態表はnative table、比較はnative文字/形状。PowerPoint内で本文・図形・線・表を直接編集できます。native chart/数式は使用していません。PDF/PNGは閲覧用です。原稿を直して再生成するなら `input/outline.json` を編集します。

原典のOperating Gridを一貫したdesign systemとして使い、暗い表紙・結論、関係のbands、開いたtimeline、表、判断条件の2列を選択。手書き座標や生成後PPTX修正を避けています。原典未変更原本は `upstream/`、字体roleと表の注記を日本語化したruntime差分は `source/*.diff`。

見出しShippori Mincho、本文とnative表の見出しBIZ UDPGothic、native flow/timeline番号とページ番号Manrope。初回PowerPoint表示でShipporiの表見出しだけ和文が欠けたため、表見出しはBIZのboldに割り当てました。公式未変更TTF/OFLを `fonts/` に同梱。OS/Office字体を抽出していません。PowerPointの表示時にはこれらの字体をWindowsへ登録してください。

## 再生成

原典が既定と明記するNode/PptxGenJS route。Node.js、PptxGenJS4.0.1、jszip3.10.1、PowerPoint16（プレビュー生成用）が必要です。

```powershell
npm install
node runtime/scripts/build_deck_pptxgenjs.js --outline input/outline.json --output deck.pptx --style-preset lavender-ops
powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
```

`source/build.py --node C:/path/to/node.exe` は同じ原典Node CLIを呼び出す補助入口で、PPTXを描画する別generatorではありません。原典・字体・依存のLICENSEを保持。Node_modules、Office、venv/cacheをZIPへ含めません。共有PowerPoint ApplicationをQuitせず、自分が開いたdeckだけCloseします。

## 実行環境と確認範囲

原典Python doctorも一度実行し、科学データ依存（pandas/pyarrow等）の不足とpin違いを `source/python-doctor.log` に保存しています。Python data/asset/finalize pipelineは準備完了とは報告しません。今回の原典既定Node rendererのnative flow/table/comparisonには、それらのPython科学依存は不要です。画像や実データの解析を追加する場合は原典のpinned Python環境を整備してください。

原典の生成・内蔵enum/role contract/text fit解決、PowerPoint16の6枚PNG/PDF生成、代表完成物の初回表示まで。ユーザー指定により全ページ詳細目視、独立review、包括finalize/構造監査、ZIP再実行は未実施。包括QA合格やProduction採用とは称しません。
