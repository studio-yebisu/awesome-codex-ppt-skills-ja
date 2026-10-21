# 保存済み入力からの再実行

一式ZIPを新しいフォルダーへ展開し、このファイルのあるフォルダーをCWDにする。生成し直した出力へ以前の目視・独立評価を引き継がない。

- Python3.10+ / python-pptx / 原典deckkit
- 原典render/lintはLibreOffice。今回だけWindows PowerPoint16とYu Gothic、PDFiumを描画adapterとして使用。独立critic/blind readerも必要。原典criticの承認を制作側で偽装しない。

Python依存はsource/requirements.txtと原典の依存指定を参照する。PowerPoint描画はWindows PowerPointが必要。PDFからPNGを作る処理にはpypdfium2を使う。既存の固定依存を使い、新規インストールは今回検証していない。

最後の原典handoffは現在critic/blind-read待ちでexit1となる。古いconsentはsource/previous-deck-gates.jsonへ保存し流用しない。新しい独立レビューを原典形式で記録してから再検査する。

```powershell
python source/build_slide_maker_repository_example.py
python source/upstream/skills/slide-maker/scripts/lint_deck.py deck.pptx --json source/current-lint.json
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
python source/render_pdf_previews.py render
python source/upstream/skills/slide-maker/scripts/render_deck.py deck.pptx --gate-check
```

現在の配布再実行範囲はsource/distribution-replay.jsonとQA.jsonへ記録する。原典の未達gateを成功へ読み替えない。公式OSS字体の同梱にはOFLを保持し、Windowsの字体ファイルは抽出・同梱しない。

独立blind-readは`python source/prepare_blind_packet.py`で元CLI用のslide01.png形式をbytes不変で用意し、`blind_read.py compare . --render-dir qa/original-blind-render --answers 実回答.json --write`を使う。原典の検査ロジックは変更しない。

Codex原典追加ゲート（独立回答が揃うまでは失敗が正しい）：

```powershell
python source/upstream/skills/slide-maker/scripts/component_audit.py source/build_slide_maker_repository_example.py deck.pptx --json --out source/current-components.json
python source/verify_component_intent.py
python source/upstream/skills/slide-maker/scripts/codex_visual_contract.py deck.pptx --manifest visual-contract.json --build-script source/build_slide_maker_repository_example.py --renders qa/original-blind-render --crops qa/visual-contract-crops --out visual-contract-final.json
python source/upstream/skills/slide-maker/scripts/codex_delivery_gate.py --lint source/current-lint.json --components source/current-components.json --build-script source/build_slide_maker_repository_example.py --evidence .codex-deck-evidence.json --receipt codex-delivery-receipt.json
python source/upstream/skills/slide-maker/scripts/codex_handoff_guard.py --receipt codex-delivery-receipt.json --deck deck.pptx
```

component auditのexit2は配列をカード群と検出した助言。各頁の意図は原典の正式なwaiver欄に記録し、verify_component_intent.pyで原典check_componentsの受理を確認する。この確認は全deliveryの合格ではない。現在のCodex専用deliveryは独立回答・批評・局所画像の確認待ちで失敗し、PASS receiptを作らない。
