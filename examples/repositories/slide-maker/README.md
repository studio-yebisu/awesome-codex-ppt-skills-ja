# 並べておくと、探し方が変わる

addsumtech/slides_maker の固定commit `3767cc346d63ef1646082c87f15fbf0be582b152` にある、未改変の `deckkit`、`native_chart`、`title_bar`、`footer`、`takeaway_rail` を実行した5枚の日本語教材です。MITの原典コードとライセンスをsource/upstreamへ保持しています。

配列1〜15をPythonで実際に探索し、全15ターゲットの訪問要素・範囲・比較回数をinput/data.jsonへ保存。13の探索は線形13回、二分4回（8→12→14→13）。全15通りの最大は線形15回、二分4回です。秒数、整列コスト、大規模データの性能は測定していません。

## 再実行

Python 3.10+へ `python-pptx pymupdf Pillow matplotlib numpy` を導入し、作例フォルダで次を実行します。

```powershell
python source/build_slide_maker_repository_example.py --upstream-dir source/upstream --output-dir ../slide-maker-replay
```

Python 3.13環境で再実行し、入力JSONと全スライド・chart・notes XMLの一致を検証しました。ZIPの時刻情報等を含むPPTX全体のbyte一致は主張しません。字体はYu GothicとConsolas。表示先に同じ字体がない場合は代替フォントになります。

## 確認した範囲

PowerPoint 16.0で全5枚をPNG/PDFへ出力し、実視認しました。文字・数字・図はnative object、グラフは編集可能なchartと埋込Excelデータ、発表者ノートは全5枚。図を全面画像に置き換えていません。読み上げ用タイトルも追加しています。

原典lint_deck、trace_composed、helper signatures、validate_reviewを使用。独立criticによる内容・視覚レビューと修正はreview/に記録します。これは技術・内容QAであり、人間による正式採用ではありません。

初回render_deck --gate-checkは計画とblind readの欠落を検出しました（source/logs/gate-check.logを保全）。その後、構成3案の比較、実描画した方向5案の比較、別担当による画像だけのblind read、計画と完成版の追加監査を実施。最終引き渡し検査はexit0です（source/logs/gate-check-cwd-resolved.log）。ただし計画は制作後の追加実施で、事前承認だったとは扱いません。URLを要求する出典ゲートはローカル実行入力へ適合しないため理由付き適用除外にし、代わりに実行コード・入力SHA・独立再計算を保存しています。レジストリやtasteへの書込、外部画像API、課金はしていません。

## 証跡

input/data.jsonが数値の一次入力、source/build_slide_maker_repository_example.pyが実行コードです。source/object-proof.jsonにチャート数値とXML再現性、source/commands.jsonに検査コマンド、PROVENANCE.jsonに原典と変更点、QA.jsonに最終状態があります。初回の失敗と最終の解決は別ログで保持しています。


追加選定：図中心、静的5枚、既存テンプレートなしの明るい配列図を採用候補にしました。方向Bの端末、Cの棒のみ、Dの木状配置、Eの原典黒板は実描画で比較し、同じ配列位置を保てるAを選定。正式な人間の採用は未実施です。小さい脚注は独習用の補足として受容し、教室後方からの投影可読性は保証しません。
