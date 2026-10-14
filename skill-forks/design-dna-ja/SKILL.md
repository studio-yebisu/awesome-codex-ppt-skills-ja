---
name: design-dna-ja
description: PPT-Design-DNAで指定参考画像の5層DNAを抽出し、tokens・Contract・Page Specsへ再利用して日本語の固定stage HTMLスライドを作る。
license: Apache-2.0
---
# PPT-Design-DNA 日本語ガイド

原典は dakjdakd/PPT-Design-DNA、commit `5d1d84cf952f16920d893b6c04bd7cb7cff9d155`、Apache-2.0 ©2026 dakjdakd。[原文SKILL](example/source/upstream/SKILL.md)と[LICENSE](LICENSE)を保持。参考の自作Akxan作例は[MIT](example/input/reference/LICENSE)、実字体はOFL-1.1です。

1. 指定された実画像を先に表示し、入力へ原本保存する。この例は[自作PPTXの実描画PNG](example/input/reference/slide-01.png)。[出所](example/input/reference/PROVENANCE.json)を保持し、共有原本を変更しない。画像を見ずに別テーマを発明してDNAと呼ばない。
2. 原典[schema](example/source/upstream/references/design-dna-schema.md)に従いMood/Composition/Visual/Content Strategy/Presentationの5層、固定10パラメータ、10以上のsemantic tags、sourceのallowed traits/forbidden subjectsを抽出する。[DNAパネル](example/input/DNA-PANEL.md)と[active candidate](example/input/design-dna.json)が作例。数値は見た目の調整用で、効果の測定スコアではない。
3. 参考はstyle evidenceとして扱い、新作にその画像・固有の文章・被写体を流用しない。静止参考から動きは推定できないため、新しい内容に必要な控えめな演出を別途定義する。この例の道具SVGは新作原稿に由来する。
4. [依頼文](example/PROMPT.md)と[原稿](example/input/MANUSCRIPT.md)を自分の題材へ置き換える。DNA→[Contract](example/specs/design-contract.json)→[Blueprint](example/specs/ppt-blueprint.json)→[数値Page Specs](example/specs/page-specs.json)の順で、文字高・余白・surface/ink・nav safe zoneを確保する。長い情報を小さい字や隠しoverflowへ押し込まない。
5. 原典[HTML生成契約](example/source/upstream/references/html-generation-rules.md)の1920×1080固定stageと均等scaling式を使う。原典に完成renderer/controllerはない。作例のナビゲーションとJSON→HTML梱包はこの契約に沿った自作。[局所CSS](example/source/adaptation.css)と[bridge patch](example/source/controller.patch)を区別して保存する。
6. `python example/source/rebuild.py` で単一HTMLを生成する。Python標準ライブラリのみ。その後 `node example/source/upstream/scripts/ppt-layout-guard.js example/index.html --report example/layout-guard-report.json` を実行する。この未改変の原典guardは必須で、P0があればPage Specsから修正して再実行する。外部SDKや汎用rendererへの代替はしない。

実字体は[公式固定TTF/OFL](example/source/fonts/)を未改変で同梱し、単一HTMLへ埋め込む。OS字体を抽出配布しない。編集はDNA/Page Specs、HTML、SVG、CSS、JS。PPTXは生成しない。

現行の承認済み自律制作指示に従い、原典のuser-turn確認・保存選択ゲートを記録パネルへ置き換えました。確認回答があったと捏造せず、canonical design-profilesも作っていません。再生成入力candidateを専有作例に保存し、原典のoutputs配置を専有パスへ変更しました。今回の確認は必須guardと代表2頁の初回表示・ページ送りのみ。全頁詳細目視・独立review・追加採点・ZIP再実行を必須にしません。[QA](example/QA.json)の範囲を保持します。
