---
name: and-scene-ja
description: 原典のReact scene kitを実scaffoldし、安定layoutIdの共通canvasでentityが移動・morphする日本語ブラウザ資料を作る。
---

# 日本語 and-scene

原典 [Codagent-AI/and-scene](https://github.com/Codagent-AI/and-scene)、固定commit `5ce44dff61f181db35b0c98a1cb86c71c7e062cb`、MIT ©2026 Codagent-AI。出所[SOURCE.json](SOURCE.json)、原文条件[LICENSE](LICENSE)、原典[SKILL](upstream/skills/presentation/SKILL.md)。

1. 題材・見た目・節・全Stepが指定済みなら再質問せず進む。Stepはcaption/titleとscene状態を持つ一つの移動可能な段階で、資料の独立した一枚と区別する。
2. 空の私有appへ原典[bootstrap](upstream/skills/presentation/templates/bootstrap/package.json)をコピーし、build setup・kit・registryのanchorを用意。runtime React/React-DOM/Motion/Lucideと元dev/build依存を実installする。既存共有appへ無断で上書きしない。
3. 原典[Stepテンプレート](upstream/skills/presentation/templates/single-step/step.tsx)とpresentationテンプレートからtyped stepsを作り、registryへ登録する。元types/Presentation/Stageを実使用。色や字体はpresentation-owned CSS、kitを一般rendererに替えない。
4. 同じ概念はstable layoutIdを保つ。一つの共通図は同じSceneとgroupKey、typed payloadで状態を変える。transform/opacityはlayoutIdノードへ直接載せず、非layoutの子/外側へ。新しい登場だけAppearを使う。固定canvas880×380と元chromeを尊重する。
5. `npm run build`（原典tsc -b && vite build）と主要初回表示/元1→2を確認する。公式実TTF/OFLをlocalへ、OS抽出なし。元TOC/progress active stateとattributionを読める見た目にする。
6. この日本語派生ではユーザーが全step/designを指定して自律制作と軽い確認を選択済み。原典fullverify/inspectの全段階・last/dense/mobile/独立レビュー/ZIP再実行を追加しない。必須install/buildと初回runtime表示は維持し、未実施をQAへ明記する。

## MD単独取得からの入口

固定原典：[SKILL](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/SKILL.md)、[bootstrap package](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/package.json)、[types](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/src/presentation-kit/types.ts)、[Presentation](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/src/presentation-kit/Presentation.tsx)、[Stage](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/src/presentation-kit/Stage.tsx)、[Step](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/single-step/step.tsx)、[LICENSE](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/LICENSE)。一式fork ZIPは必要な未変更原本をupstream/へ持つ。

制作一式`and-scene-example-ja.zip`のapp/（src、package/lock/config、public/fonts実TTF/OFL）、dist/完成runtime/assets/fonts、input/、source/原文/差分/conditionsとREADMEを取得する。app/で`npm ci && npm run build`。distをHTTPで一緒に配信してindex.htmlを開く。主出力は複数assetsを持つWebフォルダーで単独HTMLではない。PPTX/PDFは原典対象外、生成しない。編集はTSX Step/payload/SVG/CSSとcaption。

Google Fonts固定`66928797f271fed5ee428544e7229685e2d90127`のShippori Mincho/BIZ UDPGothic/Manrope（OFL1.1）を使用。必要未改変ファイル・原文URL/hashは制作ZIPのapp/public/fonts/SOURCE.json、フォークの[FONT-SOURCES.json](FONT-SOURCES.json)に示す。runtime依存原文条件は[DEPENDENCIES.md](DEPENDENCIES.md)/licenses/。

親プレイヤーへは元usePresentationNav/setStepのsame-origin0-based adapterだけを局所追加できる。step数をpage_count、page_unit=段階にし、原典modelにないscene数は作らない。

## 単体の本文から使う

この本文は `skill-forks/and-scene-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Codagent-AI/and-scene/tree/5ce44dff61f181db35b0c98a1cb86c71c7e062cb

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `and-scene-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: Codagent-AI / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Codagent-AI/and-scene/blob/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/LICENSE
