---
name: mck-native-ja
description: 原典の図表・比較・工程メソッドと段階ごとの検査で、集計値や原稿から編集可能なPowerPointを作る。
---

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
| grouped_bar | 元5分類×日本語/欧文の実集計 | 2頁：6/6、5/3、4/0、2/1、0/3。0〜6の整数軸で比較 |
| data_table | 元5分類×言語と実書体名 | 3頁：合計17・13・30。言語ごとの先頭書体と「該当なし」を2行で照合 |
| value_chain | 五段階の保存ファイル | 4頁：番号と見出しの中心をそろえ、S3/S4実行とS5固定fixtureの再生を分ける |

原典は67高水準メソッドを案内するが、この例で使用したのは4種類。残り63種類・外部表紙画像API/Hunyuanを実証したとは扱わず、全種類の使用を要求しない。図・表は文字、棒、罫線、番号など個別編集可能な図形で、Officeのデータ連動チャートやネイティブ表ではない。分類はカタログ管理情報で、書体品質やglyph範囲の測定ではない。工程時間も未計測。

## この集計例を再制作する

Python、python-pptx、lxmlを用意し、`fonts/` の公式BIZ UDPGothic RegularをOFLに従って登録する。Boldファイルは同梱せずPowerPointの太字スタイルを指定し、字体はPPTXへ埋め込まない。実描画はWindows版PowerPoint、PDFからの画像化はpypdfium2を使う。

```powershell
python source/build_mck_native_showcase.py --out rebuild --render
python source/render_pdf_previews.py rebuild/render
```

同梱生成器は `input/oss-font-kit.json` の集計専用で、任意原稿の自動変換器ではない。`font-count-checks.json` は言語・分類・クロス集計、図の合計、表の合計を照合する。ファイル数はメタデータ中のfilesレコード数であり、全フォントの取得・導入・表示を検査した意味ではない。新しい原稿は上の一般手順で適切なAPIを選ぶ。

## 現在の検査と残る制約

原典の自動検査S3/S4は合格。S4は92点・user_code_errors=0・原典既定免除2・警告0。2頁の小見出し13ptと凡例12pt、4頁の番号Arialと見出しBIZ UDPGothicのpeer_font_inconsistencyを既存whitelistが除外する。新規免除はなく、独立評価や視覚品質の合格を意味しない。 詳細は[source/gate-exclusions.json](source/gate-exclusions.json)。書体指定だけを生成プロセス内で変更し、旧donutの百分率adapterは現版では使用しない。

表紙のtitle改行と表のcol_widths/セル改行は公開引数。元5分類×2言語をgrouped_barのdata/seriesと整数軸へ、実5工程をvalue_chainのstagesへ渡す。工程の番号と見出しは同じ中心へそろうが、中央下の余白と表の固定行高は残る。原典エンジン・QA・whitelistは未変更。

[S5交付記録](ppt-project-font-kit/delivery-and-refinement.json)と[経験記録](experiences/chart-limits.md)は、修復時にCodexが判断した固定fixtureを再生する。今回のS3/S4合否と成果物hashは実行結果だが、生成器は新しい修正の型を発見・判断しない。原典の経験4件と関連APIの読取範囲は[読取記録](source/reading-record.json)に記録し、初回Opus作者の過去の読取へ補完しない。

2頁の「集計結果」を別コピー上で「集計確認」へ変更し、保存した別PPTXを再openして描画した。[編集後PNG](qa/native-edit/edited-copy.png)・[別PPTX](qa/native-edit/edited-copy.pptx)・[確認記録](qa/native-edit/report.json)から照合でき、元PPTXは保存していない。両ZIPの再実行は[source/distribution-replay.json](source/distribution-replay.json)を参照。機械検査、作者の全4頁の目視、独立評価、利用者採用は別。

原典likaku/Mck-ppt-design-skill、commit e190e083b715b63172e1c4fea01bc5f9bb21a021。Apache-2.0のLICENSE・NOTICEを保持。初回script/planは実claude-opus-5-5。今回R13の集計・原典別API選択・公開引数調整・文書・実行・目視・梱包はCodexで、新しいOpus制作は行っていない。公式翻訳ではない。
