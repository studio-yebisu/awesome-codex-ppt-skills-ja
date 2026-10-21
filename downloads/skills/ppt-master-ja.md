---
name: ppt-master-ja
description: 目的に応じて新規スライド生成、再利用テンプレート制作、既存native PPTX編集を選び、SVGの文字と図を編集可能なPowerPointへ変換する日本語案内。
metadata:
  copyright: "Copyright (c) 2025-2026 Hugo He"
  license: "MIT"
  official_repository: "https://github.com/hugohe3/ppt-master"
  sponsors:
    - "SPONSORS.md"
    - "SPONSORS_CN.md"
  upstream: https://github.com/hugohe3/ppt-master
  upstream_commit: ca04346de145ed6462ddf34682848e71df5e20a2
---
# SVGの本文と図を編集可能PPTXへ変換する

原稿と図の関係をSVGへ分け、文字・線・帯を編集できるPowerPointへ変換する。新規制作、再利用するテンプレート、既存native PPTXの編集は、目的に合う経路を1つ選ぶ。

原典hugohe3/ppt-master、固定commit `ca04346de145ed6462ddf34682848e71df5e20a2`、MIT。著作権・スポンサー文書を保持する日本語派生。公式翻訳ではない。

## 一般の使い方

1. このSkillの絶対パスを保持し、`python <SKILL_DIR>/scripts/attribution_guard.py`を最初に実行する。非0なら停止し、ガードを修正・迂回しない。`SKILL.upstream.md`と`workflows/routing.md`を読み、選ばれた経路の資料だけを追加で読む。以下のパスはSkillルート基準。
2. 新規制作・画像からの再構築・既存資料の再デザインはGenerate。通常は`workflows/generate-pptx.md`、速成/直接SVGが明示された場合だけ`workflows/profiles/quick-generate.md`を使う。頁数はQuickを選ぶ理由にならない。画像の頁を復元する場合は`image-to-pptx.md`、語句・頁数・順序を1対1で保つ再デザインは`beautify-pptx.md`の条件に従う。両profileを混ぜない。
3. 繰り返し使うルールを作る場合は`workflows/create-template.md`。Brandは識別、Styleは表現、Layoutは用途に依存しない構造、Deckは用途と構造を持つ。元の参考ファイルを書き換えず別workspaceへ作る。生のPPTXをそのまま新規SVG生成の母版として継ぎ足さない。
4. 既存PPTXのnative意匠を保って差し替え・ページ選択・ノート/音声/動作を編集する場合は`workflows/edit-native-pptx.md`。元PPTXと差し替え資料を用意し、roundtrip workspaceを作る。未変更の原本部品を保ち、新しいPPTXを別出力へ保存する。
5. 選んだ経路で事実・根拠・読者・判断・言語・期間/単位を整理する。資料のない題材や不足する外部事実には条件付きtopic-research、画像等は出所と利用条件を付ける。Defaultの確認門、Quickの主担当による中断しない直接SVG制作と計画ファイルを持たない契約は元手順どおり。確認を実施していない過去の作例を承認済みと扱わない。
6. 図の関係は`references/executor-structure.md`、行列の交点で読む事実は`executor-table.md`、値や期間で長さ/位置が決まる図は`executor-chart.md`を追加で読む。原典の字体・意味ID・余白・native preset/Chart/Tableの契約に従い、主要情報を全頁の画像で置き換えない。データ連動Chart/Tableへの置換は対応metadataと原典export flagを別途用意する。
7. 値や期間で図形が変わる場合は`workflows/stages/verify-charts.md`で完成したSVGの軸・目盛りと元値を照合する。原典calculatorのスケールと端点を確認し、誤差を直してから経路のfinal checkerへ戻る。関係図の矢印を数量データと誤認しない。
8. Quickは7頁以上ならP05直後のearly checkerを行い、全頁完成後は`svg_quality_checker.py PROJECT --quick-generate --canonical-authoring --stage final --json`。一致した最終fingerprintで`svg_to_pptx.py PROJECT --quick-generate --primary-language ja-JP --with-notes -t fade -o OUTPUT.pptx`を実行する。Quickでは`finalize_svg.py`を挟まない。Default等は選ばれた元の計画/確認/後処理順を守る。
9. 明示的なプレビュー・視覚確認は元の`visual-review`/`live-preview`の適用条件を守る。ノート・動作・音声・録画には対応参照とstageを追加し、録画用のCustom Animations等を省かない。実アプリの全頁で文字・関係・単位・注記・切れを確認する。checkerの成功、実描画、独立評価、利用者の採用を区別する。

必要な依存は選ばれた原典routeの資料に従う。Python、対応ライブラリー、PPTX表示アプリ、使用字体が必要。画像/音声等は必要な機能だけ準備し、秘密情報を配布物へ含めない。

## 同梱例の範囲

`example/`は架空の喫茶店の8頁。元QuickのSVG契約と検査/変換を使う専用Python再現器であり、主エージェントの全頁手書き・init/import等を含む原典の全Quick工程の実証ではない。一般手順を固定の喫茶店原稿へ限定しない。

5頁は既存店から新店への仕込み支援と、両店の共通化。6頁はリスクごとの確認・判断材料。7頁は入力の1〜2週、3〜4週、5週を実際の期間へ対応させる。8頁は今回の調査判断と将来の契約/投資を分ける。原典guard・P05 early・final・Gantt座標calculator2回・native exporterを実行した。検査の字体助言は保持する。

原典コードは改変せず、`example/source/export_with_biz.py`で同梱BIZ UDPGothicだけを東アジア字体集合へ登録する。追加しない場合、日本語部分がYu Gothicに置き換わる。`fit_text_frames.py`はPowerPoint実測から文字枠幅だけを補う後処理で、文字・字号・基線・色は保持する。実修復前後の全8頁RGB一致を確認した。これらは原典の元機能と区別して開示する。

native文字141、文字を含む図形183、画像0。表・工程表は個別図形でOffice Table/Chartではない。全8頁の実PowerPoint描画と実PDF字体、SVG前後比較、代表のnative文字編集→保存→再表示を確認した。数値変更の実証は私的コピーだけで、正本は24席のまま。

再実行と依存は`example/REPRODUCE.md`、検査の実結果は`example/QA.json`。Default全工程、テンプレート/Brand制作、複雑な素材や動作、現版の独立再評価、採用と業務効果は未実証。

## 単体の本文から使う

この本文は `skill-forks/ppt-master-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/hugohe3/ppt-master/tree/ca04346de145ed6462ddf34682848e71df5e20a2

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `ppt-master-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: hugohe3 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/LICENSE
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/LICENSE
- https://github.com/hugohe3/ppt-master/blob/ca04346de145ed6462ddf34682848e71df5e20a2/skills/ppt-master/scripts/pptx_shapes/data/NOTICE.md
