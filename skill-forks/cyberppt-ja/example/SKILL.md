---
name: cyberppt-ja
description: 根拠資料から論点と画像案を作り、主要な文字・表・図を編集可能なPPTXへ再構築する。原典は逐頁の画像一致と利用者確認まで要求する。同梱5頁はその未達を残す部分例。
---

# 画像案を測って編集可能な図表へ組み直す

元資料から論点・図表・画像案を作り、見た目を照合しながら主要情報を編集可能なPPTXへ戻す。文字が編集できることと、原図の見た目が保たれることの両方を検査する。

原典はcrazyykhllc-bit/CyberPPT、commit `980e5576565f0673c67ee41b01d20ed66cb8417c`、MIT。日本語派生であり公式翻訳ではない。原典の合格条件は変えない。

## 用意するもの

- DOCX/PDF/TXT/XLSX等の根拠資料、読者と判断、必要な頁数。値・単位・期間・出所と未提供事項を区別する。
- 実画像を生成できるImageGen、Node/PptxGenJS、PowerPoint、Python/Pillow/numpy/pywin32。元の固定8スタイル画像と参照群は`source/upstream/`に保持。
- 作例の再生成はPptxGenJS4.0.1、Yu Gothic/Yu Mincho/Times New Roman、PDFiumを使う。OS字体は同梱しない。

## 新しい題材で使う

各段階の前に、`source/upstream/SKILL.md`と対応する参照を全文読む。第1段階は`references/source-analysis.md`と`storyline.md`、第2段階は`visual-system.md`、第3段階は`ppt-production.md`と`quality-assurance.md`。以下のパスは原典SKILLからの相対パス。

1. 元資料から事実・比較・推奨・条件を抽出し、出所位置、期間、単位、確度、矛盾、不明、含意、図示方法を証拠表へ置く。2〜3のストーリーとissue/hypothesis treeを比べ、SCR、頁数、各頁の主張・図表・密度・部品を提案して確認する。生成画像の文字や数値で根拠を補わない。
2. `assets/palette-samples/palette-01.png`〜`08.png`の独立16:9画像8枚を会話で提示する。HTMLや合成一覧だけでは代用しない。選択後に色・網目・文字階層・図表・頁眉脚・密度を固定し、内容を`slide_content_lock`へ置いてから、全頁のImageGen bitmapを作る。言語は指定→元資料→会話の順で決め、実行用の言語metadataを紙面へ出さない。
3. 原図の確認後、構成署名と全可視要素のregistryを固定し、元画像・内容・署名・座標をhashで対応させる。新題材ではその原図用の要素JSONを新たに作り、本文、表の行列、重要数値、注釈、結論、脚注を登録する。同梱`prepare_measurements.py`の固定5頁の座標を別資料へ流用しない。
4. 現在の1頁だけの再構築計画、複雑素材の判定、画布換算、要素/文字/矢印/容器の測定を用意してからPptxGenJSで単頁を作る。正式な生成をpython-pptx、HTML変換、全頁画像へ切り替えない。主要文字・単純な図表・表・注釈・結論・脚注はnative。必要な複雑素材だけを小さな非文字画像/SVG等として登録する。アイコンは原典の検索器で単一ライブラリーから選ぶ。
5. PowerPointでその頁を開き描画する。原図と全体/局所を比較し、bbox/pixel、ラベルの衝突、実際の容器内のはみ出し、連続文の改行、表の文字役割と密度を確認する。曲線等は裁図→幾何分析→点/制御点→debug→再構築→局所描画の順。元P0/P1/P2の容差を緩めず、主要文字を画像化して一致させない。
6. `slide_manifest.json`と外部証拠に基づく`visual_qa_gate.json`をそろえ、原典のvalidatorを`--manifest --visual-qa --strict`付きで実行する。`--strict`だけの成功は原典の完全なゲートではない。編集性と視覚の両方が通り、利用者がその頁を確認してから次頁へ進む。失敗を自己申告の合格へ書き換えない。
7. 全頁通過後に確認済みの単頁PPTXを取り込み、再生成・再配置せずに統合する。全頁を再描画して対応する単頁と比較する。正式な最終確認にはPPTX、原図、全描画、局所比較、manifest、各gate、差分と編集できる範囲を添える。

## 同梱の5頁で行ったこと

`このフォルダー`は架空の商店街企画。実施の中心は**保存済みImageGen原図→内容と要素の登録→PptxGenJS単頁→PowerPoint描画→比較**。左の比較画像はImageGen bitmap、右はnative PPTXのPowerPoint/PDF由来描画であり、HTMLではない。原図5枚と出自を保持し、今回新しいモデル生成はしていない。

原典の元資料分析、完全なMBB証拠表、SCR複数案、固定8スタイルの利用者選択、段階/逐頁の利用者確認は実証していない。8見本画像は一般手順で使えるよう元の固定版を同梱したが、選択済みとは扱わない。

主要native文字90、文字を含むnative図形154、小アイコン画像3。Officeのnative Chart/Tableは0。全5原図と全5出力を実サイズで比較し、文字枠90個の実PowerPoint測定ではoverflow0。3頁は結論/脚注の間隔、5頁は表の自然な改行を修復した。

原典のpixel/bboxは全5頁未達。全指定strictも不合格を保持する。構成署名・全要素の測定・再構築計画・容器/連続文/表・局所比較を現入力と実描画で補ったが、失敗した位置・字形・紙面の明暗、未実施の利用者確認は合格にしない。`review/repair-strict-receipt.json`を参照する。

単頁と統合後の直PNG比較はindexed paletteの差による不合格を保持する。同じPowerPoint出力PDFからのRGB比較は別記録であり、原図への一致とは別物。今回の可読性修復を原典の受入条件の変更と呼ばない。現版の独立再評価・採用・実業務効果は未取得。

固定例の再実行は`REPRODUCE.md`。新題材には自分の資料、実画像生成、当該原図専用の測定と確認が必要。

作例ZIPのsource/upstreamは再実行用の抜粋。新題材の全工程には日本語Skill ZIPのupstream一式を使う。
