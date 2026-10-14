# 一枚の企画書、図形のモーション、選んだ作例の使い方

2026-10-14。Sol 6.1の並列制作で原典2リポの新作7枚を完成し、ローカルサイトへ統合。Astraは使用していない。

| 原典 | 作例 | 実際に使った方式 | 出力 |
| --- | --- | --- | --- |
| mpuig/agent-slides | 土曜日を、街の作業場に。 | 原典Python CLIのextract → preflight → plan/ops dry-run → render。空の16:9容器から契約を抽出し、すべての表示要素を元のadd_text/rectangle/oval/line_shape/notes操作で生成 | 独立1枚のnative PPTX・PowerPoint PNG/PDF |
| andyluu98/slidefly | 街を歩く、寄り道を選ぶ。 | 原典morph-engine/nav/frames/free-layout、inline-assets.py、export-pptx.py。旅人・道・目印の同じnamed actorが6つの姿勢を移動・変形する | 単一HTML6枚・原典exporterのPPTX・静止PDF・PNG |

企画・道・地点は創作。行程と条件は仮案で、実績や営業情報、天気予報を主張しない。入力、依頼文、固定原典、改変点、原文条件、必要runtime、指定書体の未改変TTF/OFL、日本語SKILL、作品ZIPを揃えた。

## 原典と変更

- agent-slides: `820782a5fb8cb8f251d7c0750e4299c321cd068c`、MIT。Python3.12+、python-pptx/pydanticの原native CLI。資料は一枚の企画書として独立しており、複数枚を一枚と数えていない。全冊用の自動構造ページはこの一枚指定で明示的に省略。
- SlideFly: `7de466df3f2e0199c4939ccbe4490688d4165fa3`、MIT。標準Pythonの原inliner/exporter。日本語コピー・独自actor・姿勢・SVG・書体を作者側に追加。原nav本体を保持し、作者adapterで前後操作のaria-label/titleを日本語へ変更。

SlideFlyのPPTXは文字とactor図形を編集可能、SVGはベクトル画像として収録。Morph設定の書き出しと、PowerPoint内でのMorph実再生は別。後者は未確認と案内している。TTFはPPTXへ埋め込まず、受け手への手動導入を案内。

最初の一枚資料候補marcozhou26/one-slideは、原典Apache-2.0と必須ホストSDKの使用条件を分けた。原runtime contractはartifact-tool継続使用を明記し、別Python APIへの置換を認めない。この環境のSDK条件は内部評価・テストに用途を限定するため、製品作例・fork・ZIPを作っていない。条件と再開条件は `data/sol-runtime-boundary-repository-guides.json` と `data/product-exclusions.json` に記録。

## 作例と使い方を一致させる

同じ原典に複数の作例がある場合、利用画面が常に掲載代表例の依頼文・スキルZIPを表示していた。浮遊プレイヤーと作例一覧の「作り方」は `case` を渡すよう変更。利用画面に「参考にする作例」を追加し、選んだ作例の表紙、依頼文、入力、スキル本文、ZIP、固定原典を表示する。

掲載31リポの36作例を `case_recipes` へ対応付け、33種類の固有日本語Markdownを単体取得できる。同じforkを使う作例は本文を共用。原典一覧を広げたり、未生成の技能を制作済みに見せたりする変更ではない。

Web資料の付属PPTXとPDFは浮遊プレイヤーから取得でき、PPTXを持つWeb作例はPowerPointの形式絞り込みにも含める。

## 必要な確認

原典のbuild/必要audit、agent-slidesの唯一の主出力のPowerPoint書き出し・初回表示、SlideFlyの表紙と1→2ページの一回の動きを確認。新しい2スキルのfrontmatter、変更したサイトJSの構文を確認した。

親は「夜の図書館」から「喫茶つむぎ」への作例切替で表紙・依頼文・本文/ZIPのURLが切り替わることを確認。SlideFlyのフロートで実HTMLの1→2ページ移動、日本語操作、PPTX/PDFリンクを確認。全ページ詳細目視、独立モデルレビュー、native構造監査、完全ZIP再実行は実施していない。

画面: `docs/assets/atelier-case-recipe.jpg`、`docs/assets/atelier-slidefly-float.jpg`。

## 状態

厳選31スキル・31冊168枚。制作履歴41リポ・46冊269枚。新作2件と利用導線の制作バッチが完了し、プロジェクト全体のgoalは継続。外部公開・push・merge・deployなし。
