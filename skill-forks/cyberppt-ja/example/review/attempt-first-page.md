# 履歴: 1枚目の原本忠実度ゲート未達時点

この文書は1枚目の比較直後に保存した経過記録です。その後、日本語派生の方針を明示して5枚の出力を完成しました。現在状態は上位の `README.md` と `QA.json` を参照してください。以下の「現時点」はこの経過記録を保存した時点を指します。

固定commit `980e5576565f0673c67ee41b01d20ed66cb8417c` のCyberPPTを使用した制作記録です。完成例として数えないでください。

架空の「こもれび商店街」を題材に5枚分の入力・内容ロックを作り、ImageGenで5枚の設計見本を生成しました。原本の `build_content_lock.py`、`build_component_signature.py`、`measure_blueprint.py` を実行しています。

1枚目だけをPptxGenJSで編集可能なオブジェクトに再構築し、Microsoft PowerPoint 16.0でPNG/PDFへ実描画しました。文字の可読性を実見していますが、原本の `compare_render.py` は失敗しました。局所画像から測った位置・寸法も原本許容を超えています。原本はこの段階で後続ページと最終統合へ進むことを禁じているため、現時点では2〜5枚のPPTXと統合PPTXは作成していません。

原本側の比較プログラムは、入力にrender bboxがない場合にblueprint bboxとdelta=0を補います。本例はこの既定値を実測とみなさず、別の画像解析でrender ink bboxを記録しています。局所閾値処理は限定的な測定であり、完全な字形検証ではありません。

## 現在の成果

- `input/outline.json`: 架空情報・課題仮説・掲載例・運用提案・試行提案を分離した入力
- `design/slide-01-blueprint.png` ～ `slide-05-blueprint.png`: ImageGen設計見本
- `pages/slide-01.pptx`: 1枚だけの再構築試作
- `render/page-01/slide-01.png`: 実際のPowerPoint描画
- `review/slide-01-original-diff.json`: 原本の比較結果（失敗）
- `review/slide-01-numeric.json`: 局所ink位置・寸法の測定結果
- `review/slide-01-side-by-side.png`: 見本と再構築結果の比較

所有者: 本制作担当。次工程: 1枚目の文字・アイコン・罫線の忠実度を改善し、原本ゲートを通過してから後続ページへ進む。採用状態: 未採用・制作途中。外部公開なし。

## 実行

内容ロックの再作成: `python tools/build_cyberppt_repository_example.py`

測定登録: `python examples/repositories/cyberppt/source/prepare_measurements.py`

1枚目の試作: `node examples/repositories/cyberppt/source/reconstruct.cjs 1`

PowerPoint描画: `powershell -NoProfile -ExecutionPolicy Bypass -File tools/render_powerpoint.ps1 -PresentationPath examples/repositories/cyberppt/pages/slide-01.pptx -OutputDirectory examples/repositories/cyberppt/render/page-01`

比較: `python examples/repositories/cyberppt/source/audit_page.py 1`

Node.js + PptxGenJS、Python + Pillow/numpy、Windows + Microsoft PowerPointが必要です。設計見本の生成にはCodex組み込みImageGenを使用しました。Pythonのみで画像生成を再現するものではありません。
