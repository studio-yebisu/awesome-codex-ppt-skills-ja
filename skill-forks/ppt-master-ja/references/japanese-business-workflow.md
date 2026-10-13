# 日本語の提案・報告をnative PPTXへ

このファイル内の上流コマンドはスキルrootで実行する。PROJECTとOUTPUT.pptxは制作先へ置換する。後半の作例再現だけはカタログ全体が必要。

## 入力と計算

入力は「読者／説明時間／今日決めること／確認済みの事実／仮定／比較基準／元数値と単位／担当と期限」を一組にする。

提案例：「店舗経営者へ8分で説明。今日の判断は候補地Bの調査開始。契約決裁は後日。客単価1,100円、82人/日、26日/月、変動費率35%、固定費110万円/月は仮定。候補比較・採算・リスク・日程・決裁事項を8枚に。」

報告例：「2026年9月と前年同月を比較。売上1,200万円／前年1,000万円、粗利率36%／前年38%。数字、原因の仮説、確認作業、担当と期限、次回判断を7枚に。」

- 円と万円を入力で区別。上記売上は234.52万円、簡易営業利益は42.438万円。損益分岐は110÷0.65÷0.11÷26≒59.172人/日。必要客数は切り上げて60人/日と表示する。丸め前の値と算式を保存。
- 1,000→1,200万円は前年比20%増、前年差200万円。38%→36%は2ポイント低下。「2%低下」と書き換えない。期間・母数・単位を表とグラフで揃える。
- 複数方式で同題材を作る場合、入力と計算結果を共有する。未定の数値や仮説を実績・原因として補完しない。

## 組版と講稿

1280×720で本文26px前後、見出し42px前後は今回の出発点であり固定規則ではない。長文は意味のまとまりで分ける。「1,200万円」「36%」「10/16」などの単位を保持。SVGでは自動禁則を期待せず、行頭の句読点・閉じ括弧、行末の開き括弧を実表示で確認して明示改行する。

Noto Sans JPで日本語を明示。表は見出し・数値・注記の階層を分け、単位を列見出しに置く。意味グループとboundsは上流のsemantic SVG契約を維持する。書体の選択・配布は[japanese-fonts.md](japanese-fonts.md)。

notes/01.mdのようにSVGと講稿を対応させる。講稿は主張、数字の読み方、仮定、次の判断を説明する。ノートの存在確認は音声生成・読み上げ確認を意味しない。

## 変換と確認

制作前の帰属ガードはSKILL.mdの記載に従う。上流checker/converterを無改変で使う。

```sh
python scripts/compact_svg_styles.py PROJECT/svg_output --inplace
python scripts/svg_quality_checker.py PROJECT --quick-generate --canonical-authoring --stage final --json
python scripts/svg_to_pptx.py PROJECT --quick-generate --primary-language ja-JP --with-notes -t fade -o OUTPUT.pptx
```

PPTXをPowerPointで開き、全ページをPNG/PDFへ出して確認。入力SVGのブラウザ表示だけでPPTX確認済みにしない。文字欠け、フォント置換、図形のずれを出力側で調べる。native文字・図形・ノートの構造確認も別途行う。警告は記録し、実アプリが使えなければ構造確認までと明記する。

## カタログ作例の再現

リポジトリrootから実行する。.build/ppt-master-venvは当地で準備済みのvenvで、配布ZIPに含まれる前提ではない。他環境では上流依存を準備したPythonへ置換する。

```powershell
& ./.build/ppt-master-venv/Scripts/python.exe tools/make_business_pptx.py
powershell -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/cases/cafe-pptx/deck.pptx -OutputDirectory examples/cases/cafe-pptx/render
powershell -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/cases/ec-monthly/deck.pptx -OutputDirectory examples/cases/ec-monthly/render
```

正本はdata/case-inputs.json。各examples/cases/<id>/のsource/、calculations.json、build-log.json、render/powerpoint-render.jsonを成果と照合。再生成は同じ出力先を更新するので、独自改稿は別の出力先に保存してから試す。Microsoft PowerPoint 16.0での出力実績はこの2冊の記録で確認し、全PPTXへの互換性保証としない。
