---
name: beatdeck-ja
description: 原典BeatdeckのinitとReact stageで、日本語talkをsceneとbeatへ組む。content audit、SceneDef、local fonts、原典buildを使う。
---
# Beatdeck・日本語制作

原典[borjaperfra/beatdeck（固定commit）](https://github.com/borjaperfra/beatdeck/tree/329a971303bedd3eeaae7c5216317fafdf2ef6a3)、`329a971303bedd3eeaae7c5216317fafdf2ef6a3`、[MIT原文](https://github.com/borjaperfra/beatdeck/blob/329a971303bedd3eeaae7c5216317fafdf2ef6a3/LICENSE)、©2026 Borja Pérez Francés。[SOURCE](SOURCE.json)に個別依存条件を区別する。Kernel Panic assetsは原典MITの対象外で、使わず同梱しない。

## MDだけを取得した場合

このMDだけではengineと資材は揃わない。[一式キットZIP](../../downloads/beatdeck-ja.zip)から`runtime/`のscaffold済みtalk、`source/upstream/`の未変更engine/scripts/themes/skill/templates、`source/authored/`の局所deck、`input/`・`reference/`・`docs/`、公式`fonts/`と依存noticeを取得する。この相対リンクはサイト用。単独取得したAIは以下の固定参照を使い、原典sourceを新しい私有folderへ取得する。

- [原典SKILL](https://github.com/borjaperfra/beatdeck/blob/329a971303bedd3eeaae7c5216317fafdf2ef6a3/skills/building-a-beatdeck/SKILL.md)
- [authoring](https://github.com/borjaperfra/beatdeck/blob/329a971303bedd3eeaae7c5216317fafdf2ef6a3/skills/building-a-beatdeck/references/authoring.md)、[API](https://github.com/borjaperfra/beatdeck/blob/329a971303bedd3eeaae7c5216317fafdf2ef6a3/skills/building-a-beatdeck/references/api.md)、[beat model](https://github.com/borjaperfra/beatdeck/blob/329a971303bedd3eeaae7c5216317fafdf2ef6a3/skills/building-a-beatdeck/references/beat-model.md)
- [init script](https://github.com/borjaperfra/beatdeck/blob/329a971303bedd3eeaae7c5216317fafdf2ef6a3/scripts/init.mjs)、[src/beatdeck](https://github.com/borjaperfra/beatdeck/tree/329a971303bedd3eeaae7c5216317fafdf2ef6a3/src/beatdeck)

## 原典経路を使う

1. init対象の絶対pathがworkspace内の私有copyであり、未変更原本と別だと確認してから原典npm run initを一度実行する。初期化はコピー側を削除・再編する。scaffold後のAGENTSを読む。
2. 原稿を`reference/`へ保持し、[content audit](docs/CONTENT-AUDIT.md)を先に作る。未提示の数値・仕様・URLを発明しない。
3. [SceneDef入力](input/scene-plan.json)から各beatにref/source/noteを入れる。最初はcalm standby、1click＝1beat、段階は`#scene.beat`から構成できるようにする。
4. Scene/Reveal、NodeBox+Arrow等の元componentsで組む。state-driven motionはinitialLive/timelineへ、自足する演出はTypewriter等へ。全layersをStageへ登録し、元src/beatdeckを私有controllerに置換しない。
5. 原典neutral/lightに指定brand tokensを重ねる。日本語字体はlocalの実TTF/OFLとfonts定義を使い、巨大な文字・hairline・余白を生かす。reduce motionを保持する。
6. 原典npm run buildでtypecheck・bundle・offline checkを実行する。主出力はdist/index.html＋assetsのフォルダーで、単独HTMLとは称さない。

今回の資料は6場面・15段階（待機込み）。QR targetは未指定なので、最終段階にQRを置かない。小さな同一origin bridgeをdeck側から元APIへ接続し、カタログのindexは全beatをflattenした0-basedにする（[CatalogBridge](source/authored/deck/CatalogBridge.tsx)）。

## 編集・確認範囲・条件

[README](README.md)の再build方法を使う。編集対象はReact/TSXの文字・SVG・scene/beat・timeline・CSS。PPTXは生成していない。原典ソース/文章はMIT、字体はOFL、依存GSAPは[Standard No Charge License](https://gsap.com/community/standard-license/)でMITとは区別する。[依存一覧](source/dependency-licenses.json)を保持する。

原典はnpm run verifyで全forward/back/direct/frame比較を要求するが、今回ユーザーはbuild・主要初回表示・一段移動までを明示指定したため、それに限定した。verify・全beat詳細検査・包括QA済みとは称さない。別の依頼ではその依頼の確認範囲に従う。
