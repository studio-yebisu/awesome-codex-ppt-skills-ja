# 既存PPTXを検査し、JSON差分で編集する

既存PPTXをstable IDで差分編集し、保持部分を照合する。

## 入力と出力

渡すもの：編集する既存PPTX、変更したい文章・書式・配置、必要に応じて追加する素材。

得られるもの：差分を適用した編集可能なPPTXと、適用patch・変更前後のdiff・描画確認の記録。

原典 [EveryInc/hands-on-deck](https://github.com/EveryInc/hands-on-deck/tree/a24b996ecff6393ccf39c4fee2b88c493fb0b693)、固定commit `a24b996ecff6393ccf39c4fee2b88c493fb0b693`。原文と利用条件を保存した日本語派生で、公式翻訳ではありません。

## 使う手順

1. 元PPTXを原典deck.py inspectへ渡し、0始まりの頁とstable shape ID、現在の書式・配置を調べる。
2. 対象IDへset-text/set-style/move/resizeなど必要な変更だけをJSON patchに書く。
3. 原典apply→fix→inspect→diffを実行し、実際に適用された操作と残るalignment助言を読む。
4. 元資料と変更版を描画し、文字・図表の読みやすさと対象外の部品を照合する。

## この作例で試した範囲

既存5頁の同じ要素IDに203操作を適用。表紙の来訪者図を点検基準として説明し、表と脚注の位置を調整した。master/layoutはXML内容、theme/mediaはbyteで保持を照合した。

**1頁：イベント案内の公開前チェック**：右の副題「来訪者の行動を、点検の基準にする」と下の要点を見る。元の3アイコンは点検担当者の工程ではなく、案内を読む人の行動として説明した。 既存のアイコン・矢印を作り直さず、stable shape IDへのset-textとノート更新で内容を改める。

**3頁：見つけた問題を、次の対応につなげる**：変更後の表の左右余白、2本の注記、下の要点帯を見る。原稿更新と表全体の位置/サイズ変更を分けて適用した。 set-textとmove/resizeで対象要素を変更。対象外の部品はXML内容と画像byteを分けて照合する。

**4頁：原稿の確認と、公開後の更新を分担する**：右の表の最下行と、その下の「この表は担当を決めるための案」の間隔を見る。脚注を0.10インチ下げ、要点帯に触れず表から離した。 原典のapply→fix→diff→render loopで変更箇所を確認し、機械のalignment助言と実文字の読みやすさを区別する。

## 用意するもの

- Python3.10+ / python-pptxほか原典requirements
- PowerPoint、元資料と同じOS字体。元資料をinput/donor.pptxへ固定。

## 制約と未実施

- 作例は既存5頁へ203操作を適用。set-text79・set-style21・move50・resize47・set-notes5・set-props1。新規制作、html2patch、merge、画像交換は未実施。
- 元資料はカタログ内の過去CyberPPT派生作例を固定SHAで保存した架空資料。実際の地域の運用規則ではない。
- 元と結果の34部品を比較し、theme/media8部品はbyte一致。master/layoutとその参照26部品はXML再保存でbyteが変わるが、要素・属性・文字と参照ID/対象は一致。
- 原典fixは0修正/残留0だが、inspectのalignment助言は残る。表は文字と図形で構成し、native chart編集は未対応。OS字体は非再配布。

現在版は制作側が全頁の実画像を確認しています。独立モデルの現在版再評価・人間の採用とは別です。自己採点はしていません。現在hashと検査は [example/QA.json](example/QA.json)、実行範囲は [example/PROVENANCE.json](example/PROVENANCE.json)、再実行は [example/REPRODUCE.md](example/REPRODUCE.md) を参照してください。

原文は upstream/、現在作例は example/。再実行CWDは example/ です。
