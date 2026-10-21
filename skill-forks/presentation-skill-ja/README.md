# 引き継ぎメモを一枚にまとめる

架空の社内運用を説明する6枚。引継ぎメモそのものを一枚に整える方法を、関係・順番・表・判断条件に分けて説明します。人名・会社名・実測値を使用せず、期限は相対的な仮案、状態は説明用の例です。

## 使用した原典と編集範囲

[siril9/presentation-skill](https://github.com/siril9/presentation-skill/tree/efd899c5ddf866af2ce0001c4c9340af775d4d55) / MIT / `efd899c5ddf866af2ce0001c4c9340af775d4d55`。
原典 `present.py brief` で選んだ `lavender-ops / operations-grid` 候補とreadability contractをJSONへ引き継ぎ、原典 `build_deck_pptxgenjs.js` に入力します。原典のrender-plan、role-layout contracts、templates/pptxgenjsを実際に実行したnative PPTXです。Python-pptxの別generatorやホストartifact-tool SDKは使っていません。

`flow_steps` は原典schemaが対応するnative図解、timelineはnative図形、状態表はnative table、比較はnative文字/形状。PowerPoint内で本文・図形・線・表を直接編集できます。native chart/数式は使用していません。PDF/PNGは閲覧用です。原稿を直して再生成するなら `input/outline.json` を編集します。

原典のOperating Gridを一貫したdesign systemとして使い、暗い表紙・結論、関係のbands、開いたtimeline、表、判断条件の2列を選択。手書き座標や生成後PPTX修正を避けています。原典未変更原本は `upstream/`、字体roleと表の注記を日本語化したruntime差分は `source/font-pair.diff` と `source/numeric-font.diff`。

可読性の修正もsource側だけで行い、`source/legibility.diff` に記録しています（`source/numeric-font.diff` 適用後のslides.jsとの差分）。operations-gridの本文見出しを上端bar（0.08〜0.19in）から離して0.34inから開始し、本文も測定した見出し高さに合わせて下げます。`renderContractStage` 内だけで、section補助枠の表示ラベル（`stage_labels`、未指定時は原典のslot名）と、背景に対し4.5:1以上の文字色・footer色を選びます。紫と青緑の線は装飾として残します。表紙見出しは「引き継ぎメモを／一枚にまとめる」の2行に改めました。

原典が許可する `editorial_serif_v1`（serif見出しとsans本文）を日本語の対応書体へ割り当てています。独自のfont_pair列挙値は使いません。Windows Python3.12のctime差を明示的birthtimeで比較し、native pdfinfoの日本語診断を置換付きで読み取る互換修正を加えています。差分は `source/windows-hash-guard.diff` と `source/windows-native-output.diff`。file identity・size・mtime・前後比較、return code、ページ数、QA閾値は維持します。

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

原典Python doctorによる科学データ依存の不足とpin差は `QA.json` に記録します。原文ログは公開物に含めません。科学データ・asset依存一式の準備完了とは報告しません。native作例のfinalize結果は `qa/finalize/finalize_receipt.json` が正本です。今回の原典既定Node rendererのnative flow/table/comparisonには、それらのPython科学依存は不要です。画像や実データの解析を追加する場合は原典のpinned Python環境を整備してください。

確認は二層に分けて記録します。source確認は、`input/outline.json`、再生成コード、`source/*.diff` に上記の修正が入っていることです。実行確認は、原典Node builderでの再生成、PowerPoint16での6枚PNG/PDF描画、全ページ目視、独立review、原典finalizeです。現在の依頼では独立reviewと修正loopが必須です。実行確認の結果は実行後に `QA.json`、`source/BUILD.json`、`render/powerpoint-render.json` へ記録され、記録前の項目は未確認として扱います。包括QA合格やProduction採用とは、記録された結果が示すまで称しません。

表のmetadataは表本体の列名を繰り返さず件数を示し、日本語captionを合成斜体にしません。今回の追加修正はCodexによるsource/table-legibility.diff。元builder・finalizeを再実行し、全6頁を実描画・目視しました。独立再評価は未了です。
