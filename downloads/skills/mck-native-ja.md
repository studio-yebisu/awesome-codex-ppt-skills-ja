---
name: mck-native-ja
description: 原典の図表・比較・工程メソッドと段階ごとの検査で、集計値や原稿から編集可能なPowerPointを作る。
---

## このスキルでできること

根拠のある値を同じ書式の図・表・工程へまとめ、原稿と完成PPTXを段階ごとに検査する。

- 困っている状況: 一枚ずつ図形を配置すると、書式や間隔をそろえる作業が繰り返しになる。
- 必要な入力: 原稿・元データ、読者・目的・時間、集計値の単位・分母・出典、必要な実行環境と書体。
- 受け取るもの: 編集可能なPowerPoint、制作ソース、S3/S4検査JSONと、実施した確認・残る制約の記録。
- 必要環境: Python、python-pptx、lxml、固定原典と制作ソースを含む一式ZIP。一般の制作では原稿・元データと目的を用意する。 / 描画に使う書体と個別の利用条件。例では公式BIZ UDPGothic RegularとOFLを同梱し、環境へ登録する。 / この例の実描画はWindows版PowerPoint、PDF由来PNGはpypdfium2。PowerShellで自動化する場合は対象ファイルだけを開閉する。
- 作例で試した範囲: 実カタログ30字体を4群の円と元5分類の表にし、制作の保存ファイルを原典vertical_stepsで対応させた。S5は固定修復記録の再生。
- 制約: 原典は67高水準メソッドを案内する。この作例はcover/donut/data_table/vertical_stepsの4種類を実行し、残り63種類・外部表紙画像API/Hunyuanは未実証。全67種類の使用を完成条件にしない。 / 図表は個別編集可能な図形で、Officeのデータ連動チャートやネイティブ表ではない。 / 今回の原典S3/S4は合格。S4は98点・警告1件・user_code_errors=0・原典免除0。中心文字箱16%重複警告を保持し、実文字の接触とは区別する。 / 原典SKILLの固定場所は ~/.workbuddy/skills/mck-ppt-design 。この配布物は同じ固定commitの upstream/ を読む。元のホームへ自動導入せず、原典のgateが別QAを先に読まないよう既存ホームがある場合は生成器が停止する。 / references/layouts/*.md は固定取得した原典全体にも同梱原典にも存在しない。想像で補わず、存在するengine-api.md・layout-matrix.yamlと実engineの公開引数を参照する。 / 表紙のtitle改行と表のcol_widths/セル改行は公開引数。donutのリング半径・太さ・縦位置、data_tableの行高、vertical_stepsの番号位置は公開引数で指定できず、余白や番号の位置を完全に解消したとは表示しない。 / BIZ UDPGothicと凡例の小数1桁表記は局所adapter。原典本体・QA・免除一覧は未変更。RegularとOFLのみ同梱、Boldは太字スタイル指定でPPTXへ埋め込まない。 / S5は修復時の固定経験fixtureを再生し、実行時の新規診断やPATTERN判断は自動化しない。TaskCreate/TaskUpdateとFast Trackは未実行。 / 同梱生成器はoss-font-kit.jsonの集計専用。family/file/presetのレコード数を検査し、任意原稿の自動変換や全フォントの描画品質・glyph範囲の検査は行わない。


# 集計値から図・表・工程をそろえる

元データを、内容に合う原典MckEngineのメソッドへ渡して編集可能なPowerPointを作る。配置・色・文字サイズは原典がそろえる。主張と根拠、集計方法は制作担当が決める。

## 自分の資料に使う

1. 読者・目的・主張・時間・元資料をbriefへ書き、実データの単位・分母・集計時点を確認する。
2. 原典ブランド・guard・experiencesを読み、API/容量表から入力に合う版式を選びoutline/contentへ整理する。原典固定ホームと同梱upstreamの違い、存在しないlayouts文書の扱いを確認する。
3. 原典S3のJSONがpassed=trueになった同じcontentを高水準メソッドへ渡し、PPTXを生成する。図・表に使う集計値や補足は元データから計算する。
4. 原典S4のJSONと全頁の実描画を確認する。公開引数の範囲で文量・列幅・セル改行を修正し、固定配置の制約と機械警告を残す。
5. 成果物・制作ソース・検査結果を交付し、その資料で実際に判断した修正の型を経験へ残す。作例生成器のS5固定fixtureを新しい自己改善判断と扱わない。

## 固定原典と実行場所

原典SKILLは `~/.workbuddy/skills/mck-ppt-design` の配置を前提とし、同じ場所にあるS3/S4を呼ぶ。この配布物は自動でそこへ導入せず、`upstream/` の固定commitを読む。生成器は配布ZIPの `upstream/`、repoの固定取得物、同一commitの保存物の順に、必要ファイルのある原典を探す。元のホームに別のmck_pptがある場合は、原典gateが別QAを優先しないよう停止する。既存環境を上書きしない。

原典がS4で参照する `references/layouts/*.md` は、固定commitの取得原典全体にも同梱原典にも存在しない。この欠落を同梱漏れや実読済みとして扱わず、実在する [API](upstream/references/framework/engine-api.md)、[容量表](upstream/references/layout-matrix.yaml)、選んだメソッドの公開引数を使う。原典TaskCreate/TaskUpdateはこの例で未使用。Fast Trackは5頁以下・データ図表なし・明示した短時間制作が条件で、この図表例は対象外。

## この作例で確かめる箇所

| 原典機能 | 実入力 | 実ページと見る位置 |
|---|---|---|
| cover | 実カタログのレコード数 | 1頁：30字体・45ファイル・15プリセット、日本語17・欧文13を元JSONから計算 |
| donut | 元5分類から4群への集計 | 2頁：12・8・3・7字体。補足の「装飾4＋等幅3＝7」も元JSONから計算 |
| data_table | 元5分類×言語と実書体名 | 3頁：合計17・13・30。言語ごとの先頭書体と「該当なし」を2行で照合 |
| vertical_steps | 五段階の保存ファイル | 4頁：S3/S4実行とS5固定fixtureの再生を分ける |

原典は67高水準メソッドを案内するが、この例で使用したのは4種類。残り63種類・外部表紙画像API/Hunyuanを実証したとは扱わず、全種類の使用を要求しない。図・表は文字、罫線、BLOCK_ARCなど個別編集可能な図形で、Officeのデータ連動チャートやネイティブ表ではない。分類はカタログ管理情報で、書体品質やglyph範囲の測定ではない。工程時間も未計測。

## この集計例を再制作する

Python、python-pptx、lxmlを用意し、`fonts/` の公式BIZ UDPGothic RegularをOFLに従って登録する。Boldファイルは同梱せずPowerPointの太字スタイルを指定し、字体はPPTXへ埋め込まない。実描画はWindows版PowerPoint、PDFからの画像化はpypdfium2を使う。

```powershell
python source/build_mck_native_showcase.py --out rebuild --render
python source/render_pdf_previews.py rebuild/render
```

同梱生成器は `input/oss-font-kit.json` の集計専用で、任意原稿の自動変換器ではない。`font-count-checks.json` は言語・分類・クロス集計、図の合計、表の合計を照合する。ファイル数はメタデータ中のfilesレコード数であり、全フォントの取得・導入・表示を検査した意味ではない。新しい原稿は上の一般手順で適切なAPIを選ぶ。

## 現在の検査と残る制約

原典S3/S4は今回実行してpassed=true。S4は98点、user_code_errors=0・原典免除0・警告1。2頁の中心文字箱が16%重なる警告を保持し、実文字は接触していないことを実PowerPoint描画で確認した。原典エンジン・QA・免除一覧は未変更。書体指定と小数1桁の凡例表記は局所adapter。

表紙は公開titleの改行、表は公開col_widthsとセル内容で読みやすさを調整した。donutの凡例xを6.5inへ移す試行では原典が57%空白の警告を追加したため、7.2inへ戻した。リングの半径・太さ・縦位置、表の行高、工程番号の位置は当該高水準APIの公開引数にない。2頁左下の余白と細い輪、4頁の番号位置は原典由来で残り、視覚品質の最終合格を意味しない。

[S5交付記録](ppt-project-font-kit/delivery-and-refinement.json)と[経験記録](experiences/chart-limits.md)は、修復時にCodexが判断した固定fixtureを再生する。今回のS3/S4合否と成果物hashは実行結果だが、生成器は新しい修正の型を発見・判断しない。原典の経験4件と関連APIの読取範囲は[読取記録](source/reading-record.json)に記録し、初回Opus作者の過去の読取へ補完しない。

2頁の「収録字体」を別コピー上で「収録書体」へ変更し、保存した別PPTXを再openして描画した。[編集後PNG](qa/native-edit/edited-copy.png)・[別PPTX](qa/native-edit/edited-copy.pptx)・[確認記録](qa/native-edit/report.json)から照合でき、元PPTXは保存していない。両ZIPの再実行は[source/distribution-replay.json](source/distribution-replay.json)を参照。機械検査、作者の全4頁の目視、独立評価、利用者採用は別。

原典likaku/Mck-ppt-design-skill、commit e190e083b715b63172e1c4fea01bc5f9bb21a021。Apache-2.0のLICENSE・NOTICEを保持。初回script/planは実claude-opus-5-5。今回R13の集計・公開引数調整・文書・実行・目視・梱包はCodexで、新しいOpus制作は行っていない。公式翻訳ではない。

## この方式で気をつけること

- 同梱専用生成器の再生と、自分の原稿から適切な高水準APIを選ぶ一般手順を区別する。
- 原典固定パス ~/.workbuddy/skills/mck-ppt-design を同梱upstreamへ切り替える。references/layoutsは固定原典にも存在しないため、API/容量表/公開引数を読む。

## 単体の本文から使う

この本文は `skill-forks/mck-native-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/likaku/Mck-ppt-design-skill/tree/e190e083b715b63172e1c4fea01bc5f9bb21a021

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `mck-native-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: likaku / 原典条件: Apache-2.0。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/LICENSE
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/NOTICE
