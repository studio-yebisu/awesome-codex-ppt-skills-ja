---
name: and-scene-ja
description: 原典のReact scene kitを実scaffoldし、安定layoutIdの共通canvasでentityが移動・morphする日本語ブラウザ資料を作る。
---

# 日本語 and-scene

原典 [Codagent-AI/and-scene](https://github.com/Codagent-AI/and-scene)、固定commit `5ce44dff61f181db35b0c98a1cb86c71c7e062cb`、MIT ©2026 Codagent-AI。出所[SOURCE.json](SOURCE.json)、原文条件[LICENSE](LICENSE)、原典[SKILL](source/upstream/skills/presentation/SKILL.md)。

1. 題材・見た目・節・全Stepが指定済みなら再質問せず進む。Stepはcaption/titleとscene状態を持つ一つの移動可能な段階で、資料の独立した一枚と区別する。
2. 空の私有appへ原典[bootstrap](source/upstream/skills/presentation/templates/bootstrap/package.json)をコピーし、build setup・kit・registryのanchorを用意。runtime React/React-DOM/Motion/Lucideと元dev/build依存を実installする。既存共有appへ無断で上書きしない。
3. 原典[Stepテンプレート](source/upstream/skills/presentation/templates/single-step/step.tsx)とpresentationテンプレートからtyped stepsを作り、registryへ登録する。元types/Presentation/Stageを実使用。色や字体はpresentation-owned CSS、kitを一般rendererに替えない。
4. 同じ概念はstable layoutIdを保つ。一つの共通図は同じSceneとgroupKey、typed payloadで状態を変える。transform/opacityはlayoutIdノードへ直接載せず、非layoutの子/外側へ。新しい登場だけAppearを使う。固定canvas880×380と元chromeを尊重する。対象の追加・削除に合わせて自然に再中央揃えし、固定pixel/chで動きを凍らせない。固定座標を要する図は許容経路として選択を記録する。
5. `npm run build`（原典tsc -b && vite build）と主要初回表示/元1→2を確認する。公式実TTF/OFLをlocalへ、OS抽出なし。元TOC/progress active stateとattributionを読める見た目にする。
6. 原典の自己検証を省かない。build、初回表示、全Stepの前後移動、caption、stable entity、重要な重なり、最後・密度の高いStep、狭い画面とchromeを確認する。原典 `npm run verify` と `npm run inspect -- <slug>` を優先し、実行できなかった工程は別記する。Windows用の起動差分と当作例の実行記録は制作キットsource/にある。

## MD単独取得からの入口

固定原典：[SKILL](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/SKILL.md)、[bootstrap package](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/package.json)、[types](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/src/presentation-kit/types.ts)、[Presentation](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/src/presentation-kit/Presentation.tsx)、[Stage](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/bootstrap/src/presentation-kit/Stage.tsx)、[Step](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/skills/presentation/templates/single-step/step.tsx)、[LICENSE](https://raw.githubusercontent.com/Codagent-AI/and-scene/5ce44dff61f181db35b0c98a1cb86c71c7e062cb/LICENSE)。一式fork ZIPは必要な未変更原本をupstream/へ持つ。

制作一式`and-scene-example-ja.zip`のapp/（src、package/lock/config、public/fonts実TTF/OFL）、dist/完成runtime/assets/fonts、input/、source/原文/差分/conditionsとREADMEを取得する。app/で`npm ci && npm run build`。distをHTTPで一緒に配信してindex.htmlを開く。主出力は複数assetsを持つWebフォルダーで単独HTMLではない。PPTX/PDFは原典対象外、生成しない。編集はTSX Step/payload/SVG/CSSとcaption。

Google Fonts固定`66928797f271fed5ee428544e7229685e2d90127`のShippori Mincho/BIZ UDPGothic/Manrope（OFL1.1）を使用。必要未改変ファイル・原文URL/hashは制作ZIPのapp/public/fonts/SOURCE.json、フォークの[FONT-SOURCES.json](FONT-SOURCES.json)に示す。runtime依存原文条件は[DEPENDENCIES.md](DEPENDENCIES.md)/licenses/。

親プレイヤーへは元usePresentationNav/setStepのsame-origin0-based adapterだけを局所追加できる。step数をpage_count、page_unit=段階にし、原典modelにないscene数は作らない。

## 使うための入力と現在の修復

対象の一覧・安定ID・対象同士の関係と、各段階の位置・表示状態・captionを用意します。交換本棚以外でも、同じ対象が段階を通って動く説明へ適用できます。図形は薄くしても、その役割名は判読できる濃さに残します。今回の6・8段階を含む全8段階を再描画しました。

## 現在の作例の実施範囲（Round4）

共通Sceneと対象IDを保って、一冊の位置と役割を変えた。本棚や役割名に本が重ならない配置、方向付きの循環図、実際の移動途中を確認できる。

- 段階ごとに固定座標を与える経路を使用。原典の自動レイアウト再中央揃え、sync-kit、既存資料の編集、スワイプ操作は未実証。
- 狭い画面は原典canvas全体が縮小する。文字を読む用途には広い画面を推奨。PPTX/PDF出力は対象外。
- 自然な遷移の3時点を確認した範囲。連続動画全フレームやフレームレートの品質を保証しない。

全8頁の実描画と個別の動作証拠は制作側の確認。独立Kimi K3/Opus5.5の新しい版の評価は別に行う。過去の採点を新しい画像へ引き継がない。
