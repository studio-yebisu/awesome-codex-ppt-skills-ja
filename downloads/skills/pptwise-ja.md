---
name: pptwise-ja
description: 話の順序と頁の役割を決め、内容に合う部品やテーマ固有の図で、編集可能な資料へ組む。
---

## このスキルでできること

話の順序と頁の役割を決め、内容に合う部品やテーマ固有の図で、編集可能な資料へ組む。

- 困っている状況: 原稿と図形の配置を同時に決めると、内容を変えるたびに配置を直す必要がある。
- 必要な入力: 読者・目的・発表形式、原稿と見出し、根拠になる数値、必要な画像とその出典。
- 受け取るもの: 話の順序と頁の役割に合うテーマで組んだ編集可能PPTX、プレビュー、原典build/fitの検査記録。
- 必要環境: 固定runtimeを含む一式ZIP、Node22.19+、Python、runtimeの固定依存。新規インストールは今回未検証。 / 同梱の公式Zen Kaku Gothic NewとSpace GroteskをOFLに従い登録。PowerPoint実描画はWindows版PowerPoint、PDF画像化はpypdfium2。
- 作例で試した範囲: 実フォントカタログを題材に、6頁の順序と役割をspecへ固定。3頁は順序と実プリセット例、4頁は順序のない関連情報、5頁は実件数17・13をallotmentへ渡し、原典build/fitで検査する。


# 話の順序と頁の役割から配置を選ぶ

話の順序と頁の役割を決め、内容に合う部品やテーマ固有の図で、編集可能な資料へ組む。読者・目的・話の順序をspecで固定し、原稿に座標を書かず原典エンジンへ配置を任せる。

## 使い方

1. 原典schema/narratives/themesを読み、読者と目的から話の順序・themeを選び、deck.spec.jsonへtype/kind/headingを書く。
2. 構成とthemeを示した後、inspectで頁と部品の契約を読み、意味に合う部品へ原稿を渡す。
3. 元の内容が契約を満たす場合だけsignatureを使う。型を満たすための数値・画像は作らない。
4. 最大4頁ごとに原典buildを実行し、JSONのerrors/warningsと各頁fitを読み、入力を直す。
5. 原典が返したPPTXをその場所で渡す。別途の掲載確認として全頁を実描画し、文字・根拠・単位を確かめる。

## 実作例の対応

実フォントカタログを題材に、6頁の順序と役割をspecへ固定。3頁は順序と実プリセット例、4頁は順序のない関連情報、5頁は実件数17・13をallotmentへ渡し、原典build/fitで検査する。

- 3頁・順序と具体例：上の4本の矢印は条件→候補→組合せ→確認。下に実プリセット2例の見出し・本文書体を置き、「組合せを試す」操作に具体例を対応させた。
- 4頁・関連情報：中央の候補と、書体情報・元配布・利用条件・組合せの4項目を見る。番号と線は順序や品質順位ではないことを脚注で確認する。
- 5頁・実集計の構成比：橙17書体・墨13書体の横棒、欧文側の括弧、下の確認カードを照合。全30書体の内訳と出典が一致し、架空の比率や品質順位を加えていない。

現PPTXは[.pptwise/input/deck.pptx](.pptwise/input/deck.pptx)。原典の出力を後加工・改名しない。原典のself-checkはJSON reportだけを読む。ユーザー依頼による全頁のPowerPoint目視は、それと別の掲載確認として行った。

## 制約

- 5頁は実カタログの和文17・欧文13を原典allotmentへ渡す。提示された他4件のsignatureは未実施で、内容にない情報を足して埋めない。
- 図表は編集可能な図形と文字。Officeのデータ連動チャートやネイティブ表ではない。
- 画像を使わない現版。原典images generateやasset-briefの画像経路は今回実証していない。旧版の架空配分とAI概念画像は現版の根拠に含めない。
- Rallyのmenuを保持した橙・墨・紙色の派生theme。日本語書体allowlistをメモリー内で追加するadapterのみで、原典配置・QA・出力PPTXの後加工なし。
- 原典のself-checkはCLIのJSON report。全頁PowerPoint目視はユーザー依頼の掲載確認で、原典self-checkとは別。
- 日本語書体に原典の厳密な幅表はなく、保守的な推定へfallbackする通知を保持。実PDFは同梱のZen Kaku Gothic NewとSpace Groteskを確認。
- 既存固定依存で再実行。新規npm ci、代替themeへの再切替、過去の個別人間承認、利用者採用は未検証。

## 再制作

- 固定runtimeを含む一式ZIP、Node22.19+、Python、runtimeの固定依存。新規インストールは今回未検証。
- 同梱の公式Zen Kaku Gothic NewとSpace GroteskをOFLに従い登録。PowerPoint実描画はWindows版PowerPoint、PDF画像化はpypdfium2。

```powershell
python source/rebuild_pptwise.py --node <Node実体>
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath .pptwise/input/deck.pptx -OutputDirectory render
python source/render_pdf_previews.py render
```

元資料はinput/oss-font-kit.json、構成はinput/deck.spec.json、原稿はinput/pages/。5頁の棒は管理分類の件数で、実収録文字範囲や品質順位を保証しない。原典buildはstatus=ok・errors0・warnings0・allotment1件。書体の厳密な幅表がない通知は別途保持し、実PDFの字体も確認した。検査・描画・現在の独立再評価・利用者採用は別。配布再実行はsource/distribution-replay.json。

原典liustack/pptwise、固定commit65690bc705c1b5db41b5593015675945673da542、MITを保持。今回の修復はCodex。Opusによる新規制作と記載しない。

## 単体の本文から使う

この本文は `skill-forks/pptwise-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/liustack/pptwise/tree/65690bc705c1b5db41b5593015675945673da542

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `pptwise-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: liustack / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/liustack/pptwise/blob/65690bc705c1b5db41b5593015675945673da542/LICENSE
- https://github.com/liustack/pptwise/blob/65690bc705c1b5db41b5593015675945673da542/src/cli/packs/license.test.ts
- https://github.com/liustack/pptwise/blob/65690bc705c1b5db41b5593015675945673da542/src/cli/packs/license.ts
