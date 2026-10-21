---
name: cyberppt-ja
description: 根拠資料から論点と画像案を作り、主要な文字・表・図を編集可能なPPTXへ再構築する。原典は逐頁の画像一致と利用者確認まで要求する。同梱5頁はその未達を残す部分例。
---

## このスキルでできること

画像案と内容を照合し、主要な文字・表・フローを編集可能なPPTXへ組み直せる。

- 困っている状況: 画像案の主要文字や表・フローを、見た目と照合しながらPowerPointで編集できる部品へ戻したい。
- 必要な入力: 目的・読み手・根拠資料と、内容を確定した原稿。再構築段階では生成した頁別の画像設計案。
- 受け取るもの: 画像設計案の見た目を参考に、主要な文字・図表を編集可能に組み直したPPTXと、対応・比較の記録。
- 必要環境: Windows / PowerPoint / Node / PptxGenJS4.0.1、Python / pywin32 / Pillow / numpy / pypdfium2。 / 新しい題材の制作には画像生成手段と新規測定が必要。固定作例のreplayは保存済み5原図を使用。 / Windows字体Yu Gothic・Yu Mincho・Times New Roman。OS字体本体は同梱しない。
- 作例で試した範囲: 保存済みImageGen bitmapを要素へ分け、主要文字・表・フローをnativeへ再構築。原図との一致、内容、編集性を別々に検査する。
- 制約: 実証は保存済みImageGen原図5枚からの再構築を中心とする部分例。元の資料分析・MBB証拠表・2〜3のSCR案・8スタイル選択・利用者の段階/逐頁承認は未実施。 / 原典のpixel/bbox比較と全指定付きstrictを実行したが全5頁で未達。文字・図形の編集性、はみ出し0、読みやすさの確認は原典合格の代わりにしない。 / 新題材では自分の根拠資料、内容の固定、ImageGen原図、要素/座標/署名が必要。同梱の測定コードはこの5原図用で、別原稿へそのまま使えない。 / 主要文字・表・線・フローはnative。表紙の小さなSVGアイコン3点だけが画像で、Officeのデータ連動Chart/Tableではない。 / 原図の紙の明暗、字形・字重、ヘッダー形式の差を保持/開示。原図のpixel一致・ユーザー承認・現版独立再評価・実業務効果は未取得。


# 画像案を測って編集可能な図表へ組み直す

元資料から論点・図表・画像案を作り、見た目を照合しながら主要情報を編集可能なPPTXへ戻す。文字が編集できることと、原図の見た目が保たれることの両方を検査する。

原典はcrazyykhllc-bit/CyberPPT、commit `980e5576565f0673c67ee41b01d20ed66cb8417c`、MIT。日本語派生であり公式翻訳ではない。原典の合格条件は変えない。

## 用意するもの

- DOCX/PDF/TXT/XLSX等の根拠資料、読者と判断、必要な頁数。値・単位・期間・出所と未提供事項を区別する。
- 実画像を生成できるImageGen、Node/PptxGenJS、PowerPoint、Python/Pillow/numpy/pywin32。元の固定8スタイル画像と参照群は`upstream/`に保持。
- 作例の再生成はPptxGenJS4.0.1、Yu Gothic/Yu Mincho/Times New Roman、PDFiumを使う。OS字体は同梱しない。

## 新しい題材で使う

各段階の前に、`upstream/SKILL.md`と対応する参照を全文読む。第1段階は`references/source-analysis.md`と`storyline.md`、第2段階は`visual-system.md`、第3段階は`ppt-production.md`と`quality-assurance.md`。以下のパスは原典SKILLからの相対パス。

1. 元資料から事実・比較・推奨・条件を抽出し、出所位置、期間、単位、確度、矛盾、不明、含意、図示方法を証拠表へ置く。2〜3のストーリーとissue/hypothesis treeを比べ、SCR、頁数、各頁の主張・図表・密度・部品を提案して確認する。生成画像の文字や数値で根拠を補わない。
2. `assets/palette-samples/palette-01.png`〜`08.png`の独立16:9画像8枚を会話で提示する。HTMLや合成一覧だけでは代用しない。選択後に色・網目・文字階層・図表・頁眉脚・密度を固定し、内容を`slide_content_lock`へ置いてから、全頁のImageGen bitmapを作る。言語は指定→元資料→会話の順で決め、実行用の言語metadataを紙面へ出さない。
3. 原図の確認後、構成署名と全可視要素のregistryを固定し、元画像・内容・署名・座標をhashで対応させる。新題材ではその原図用の要素JSONを新たに作り、本文、表の行列、重要数値、注釈、結論、脚注を登録する。同梱`prepare_measurements.py`の固定5頁の座標を別資料へ流用しない。
4. 現在の1頁だけの再構築計画、複雑素材の判定、画布換算、要素/文字/矢印/容器の測定を用意してからPptxGenJSで単頁を作る。正式な生成をpython-pptx、HTML変換、全頁画像へ切り替えない。主要文字・単純な図表・表・注釈・結論・脚注はnative。必要な複雑素材だけを小さな非文字画像/SVG等として登録する。アイコンは原典の検索器で単一ライブラリーから選ぶ。
5. PowerPointでその頁を開き描画する。原図と全体/局所を比較し、bbox/pixel、ラベルの衝突、実際の容器内のはみ出し、連続文の改行、表の文字役割と密度を確認する。曲線等は裁図→幾何分析→点/制御点→debug→再構築→局所描画の順。元P0/P1/P2の容差を緩めず、主要文字を画像化して一致させない。
6. `slide_manifest.json`と外部証拠に基づく`visual_qa_gate.json`をそろえ、原典のvalidatorを`--manifest --visual-qa --strict`付きで実行する。`--strict`だけの成功は原典の完全なゲートではない。編集性と視覚の両方が通り、利用者がその頁を確認してから次頁へ進む。失敗を自己申告の合格へ書き換えない。
7. 全頁通過後に確認済みの単頁PPTXを取り込み、再生成・再配置せずに統合する。全頁を再描画して対応する単頁と比較する。正式な最終確認にはPPTX、原図、全描画、局所比較、manifest、各gate、差分と編集できる範囲を添える。

## 同梱の5頁で行ったこと

`example/`は架空の商店街企画。実施の中心は**保存済みImageGen原図→内容と要素の登録→PptxGenJS単頁→PowerPoint描画→比較**。左の比較画像はImageGen bitmap、右はnative PPTXのPowerPoint/PDF由来描画であり、HTMLではない。原図5枚と出自を保持し、今回新しいモデル生成はしていない。

原典の元資料分析、完全なMBB証拠表、SCR複数案、固定8スタイルの利用者選択、段階/逐頁の利用者確認は実証していない。8見本画像は一般手順で使えるよう元の固定版を同梱したが、選択済みとは扱わない。

主要native文字90、文字を含むnative図形154、小アイコン画像3。Officeのnative Chart/Tableは0。全5原図と全5出力を実サイズで比較し、文字枠90個の実PowerPoint測定ではoverflow0。3頁は結論/脚注の間隔、5頁は表の自然な改行を修復した。

原典のpixel/bboxは全5頁未達。全指定strictも不合格を保持する。構成署名・全要素の測定・再構築計画・容器/連続文/表・局所比較を現入力と実描画で補ったが、失敗した位置・字形・紙面の明暗、未実施の利用者確認は合格にしない。`review/repair-strict-receipt.json`を参照する。

単頁と統合後の直PNG比較はindexed paletteの差による不合格を保持する。同じPowerPoint出力PDFからのRGB比較は別記録であり、原図への一致とは別物。今回の可読性修復を原典の受入条件の変更と呼ばない。現版の独立再評価・採用・実業務効果は未取得。

固定例の再実行は`example/REPRODUCE.md`。新題材には自分の資料、実画像生成、当該原図専用の測定と確認が必要。

## 単体の本文から使う

この本文は `skill-forks/cyberppt-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/crazyykhllc-bit/CyberPPT/tree/980e5576565f0673c67ee41b01d20ed66cb8417c

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `cyberppt-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: crazyykhllc-bit / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/LICENSE
- https://github.com/crazyykhllc-bit/CyberPPT/blob/980e5576565f0673c67ee41b01d20ed66cb8417c/assets/icons/tabler-outline/license.svg
