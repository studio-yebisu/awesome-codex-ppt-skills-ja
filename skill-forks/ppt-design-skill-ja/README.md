# ブリーフとテーマを定めてnative PPTXを作る

構成と見た目の条件を先に定め、テーマを固定して公開APIで制作し、実画像を条件ごとに確認して修正する。

## 入力と出力

渡すもの：読者・目的・原稿・根拠資料、希望する編集性、必須条件と見た目の条件、参考やブランド指定。

得られるもの：固定したテーマで組んだ編集可能PPTX、PDF/PNG、条件IDごとの検査記録。最終承認は別途行う。

原典 [sunchaokun/PPT-Design-Skill](https://github.com/sunchaokun/PPT-Design-Skill/tree/cbf7ef1324a026b29e2b77b71e2034554ddd3e22)、固定commit `cbf7ef1324a026b29e2b77b71e2034554ddd3e22`。原文と利用条件を保存した日本語派生で、公式翻訳ではありません。

## 使う手順

1. 原典task初期化を使い、source/task/cafe-pilotへbrief・構成・MUST/SHOULD/NICEの合格条件を置く。
2. recommend_stylesの候補と公開ThemeComposer atomsを比較し、theme lock・書体・配色を定める。
3. source/build_ppt_design_repository_example.pyから公開APIだけで役割図・試算・10日表を生成する。
4. 原典inspectとPowerPoint描画を実行。全頁を視覚効果→重大欠陥の順に見て、theme aliasや字体fallbackを直す。

## この作例で試した範囲

公開ThemeComposerとstrict Presentation、文字/図形/bar_chartで架空のカフェ試行計画を5頁制作。暖色・和文書体・頁構成を固定し、受入条件R1–R7を実画像へ対応。人間承認R7は未達を保持。

**1頁：朝の2時間を、2週間だけ試す**：暖色の用紙、和文明朝、右のカップと店舗名、左下の営業時間/期間/仮価格を見る。店舗名は価格ラベルから離してカップ内へ寄せた。 先に決めたvisual thesisを、色だけでなく視線の順・見出し・余白の役割へ反映する。

**3頁：売上は仮定を変えて比べる**：左の15/25/35セットと右の9,750/16,250/22,750円を照合。棒も数値も編集可能で、下に利益ではない旨を示す。 公開bar_chartを使い、受入条件R2の計算と仮定の明示をPNGとnative要素で確かめる。

**5頁：2週間後に、続ける条件を確かめる**：需要・負担・廃棄と、右の「開始前に記入（未合意）」の空欄を見る。未収集や未合意を達成済みと誤認させない。 必須/推奨条件をID別にPASS/NEEDS_REVISION/BLOCKEDと証拠で記録し、未達を残す。

## 用意するもの

- Python3.10+ / pptx-designer1.0.0b11 / python-pptx1.0.2
- PowerPoint、公式Shippori Mincho/BIZ UDPGothic。原典task toolsはsource/upstream/。

## 制約と未実施

- 作例はBuild Modeと公開helperによる5頁。原典FreeStyle/VI Build/外部画像生成は未実施。
- 初回の構成・方向と最終結果の個別の人間承認は未取得。今回の自律制作委任とは区別し、納品版の人間承認R7はBLOCKED。
- R1–R6は実PPTXと全頁PNGで確認し、R7は未達のまま条件ID別に記録。原典runtime trace検証の成功は人間承認や独立採点の代わりではない。
- 販売数・価格は架空の仮定、売上は利益ではなく実績未収集。判断基準の欄は未合意で、実店舗で開始前に決める。

現在版は制作側が全頁の実画像を確認しています。独立モデルの現在版再評価・人間の採用とは別です。自己採点はしていません。現在hashと検査は [example/QA.json](example/QA.json)、実行範囲は [example/PROVENANCE.json](example/PROVENANCE.json)、再実行は [example/REPRODUCE.md](example/REPRODUCE.md) を参照してください。

原文は upstream/、現在作例は example/。再実行CWDは example/ です。
