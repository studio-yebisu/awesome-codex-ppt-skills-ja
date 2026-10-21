# OPUS-F05 修正記録

- 修正担当モデル: `claude-opus-5-5`（元の制作モデル `gpt-6.1-sol` の記録は残し、`repair_authoring_model` として追記）
- 状態: source修正のみ。コードの実行・再生成・描画・採点は行っていません。

## 変更したファイル

- `workspace/slides/tools/build_presentation_skill_showcase.py`（正本の生成コード）
- `source/OPUS-F05-REPAIR.md`（この記録。新規）

生成済みPPTX・PNG・PDF、`upstream/`、`data/`、サイトasset、他の作例には触れていません。次の生成物は、生成コードを実行したときに作り直されます: `runtime/templates/pptxgenjs/slides.js`、`input/outline.json`、`source/legibility.diff`。

## sourceの修正内容

1. **表紙見出し** — `outline()` の1枚目を `引き継ぎメモを\n一枚にまとめる`（1行7字、句読点なし）に変更。`TITLES[0]`、PROMPT・BRIEF・READMEの題名を `引き継ぎメモを一枚にまとめる` にそろえました。MANUSCRIPTの見出しは改行を除いた1行にします。
2. **本文見出しと上端bar** — `addDarkTitleBar` の `const titleTop` を、対象を限定した複数行ブロックに置き換えました。適用されるのはoperations-gridで、header_modeが `bar` 以外のときだけです。値は0.34in以上で、上端barの終わり（0.19in）より下になります。`headerMetrics` のtopPadにこの値が渡るため、本文の `contentTop` も見出しと一緒に下がります。他のgrammarの挙動は変わりません。
3. **6枚目の補助枠** — outlineに次を追加: `kicker='最終確認'`、`cycle='担当変更前'`、`control='記録を確認'`、`stage_labels={cycle:'確認時点', control:'着手条件'}`。`renderContractStage` は `stage_labels` を表示ラベルに使い、指定がなければ原典のslot名に戻ります。slot ID（`cycle` / `control`）、objectName、native図形は変えていません。
4. **文字色のコントラスト**（`renderContractStage` 内のみ）
   - mutedの選択基準を3.0から4.5に上げました。
   - kickerとvalueの色は、原典の `firstReadableColor` で選びます。候補は「原典の色 → 同じ色相を明るくした色（暗い背景）／暗くした色（明るい背景）→ 本文色」の順です。
   - footerは `addFooter(..., { dark, background })` を呼び、実際の暗い背景に対して色を選びます。`addFooter` 本体は変えていません。
   - 紫と青緑は装飾の線・帯として残しています。
5. **差分の記録** — `source/legibility.diff` を新しく出力します。中身は `numeric-font.diff` 適用後のslides.jsとの差分です。各置換は、対象関数の範囲内でちょうど1回一致することを確認し、一致しなければ例外で止まります（何もせずに通過することはありません）。対象範囲は次のとおりです。
   - `renderContractStage`: 関数の宣言から `function renderTitle(` まで
   - `addDarkTitleBar`: 関数の宣言から次の関数まで
6. **仕上げとZIP**
   - `finish(write_catalog=True)` を追加しました。
   - CLIに `--finish --case-only`（ROOT/dataの2ファイルを書かない）と `--package-only`（ZIP 2つだけを作り直す）を追加しました。
   - ZIPには `node_modules`、`.private`、`.build`、`logs`、`cache`、`__pycache__`、`*.pyc` を入れません。symlinkやjunctionもたどりません。
   - ZIPは `.partial` に書き出してから置き換えます。
   - `source/*.log` は根拠記録なのでZIPに残します。
7. **QAと案内文** — `QA.json` のreview項目は、実行結果の記録（同じreview_modeで記録されたもの）がなければ `null` にします。SKILL/READMEからは、ユーザーが最小確認を指定しfinalizeを禁止した、という過去の記述を削除しました。代わりに、独立reviewと修正loopが必須であること、source確認と実行確認の違いを書いています。Python data/asset runtimeは準備完了と称しない、という記述は残しました。

## 未実施の実行確認（Rootが実施）

- `--node` で生成し、`prepare()` がどこでも例外を出さずに完了すること。完了後、`source/legibility.diff` に5か所の置換と、titleTopのブロックが出ていること
- 原典Node builderの終了コードが0であること。render-plan diagnosticsに新しい警告や溢れがないこと
- PowerPoint16で6枚のPNG/PDFを描画し、次を目視で確認すること
  - 1枚目が2行で、句読点だけの行がない
  - 2〜5枚目の見出しが上端barに触れていない。本文・要約・captionがfooterと重ならない
  - 6枚目に `最終確認`／`確認時点: 担当変更前`／`着手条件: 記録を確認` が表示され、CYCLE・CONTROL・01が出ない
- 1枚目と6枚目のkicker・label・value・footerが、背景に対して4.5:1以上であること
- 独立reviewと修正loop、原典finalizeを実行し、結果を `QA.json` に記録したうえで `--finish --case-only` と `--package-only` を実行すること
