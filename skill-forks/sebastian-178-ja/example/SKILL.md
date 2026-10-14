---
name: mbb-page-maker-ja
description: 日本語コンサルティング型HTMLデッキの派生制作ガイド
license: Apache-2.0
---
# 日本語派生ガイド

原典: NomiciAI/mbb-page-maker、commit 36074669b8041783d9637a87dfed2a8733d47357。
原典root LICENSEはApache-2.0、SKILL frontmatterと末尾はMITという不一致がある。配布はroot Apache条件を維持し、source/SKILL.mdに原文を保存。MITとして塗り替えない。

1. 読者と判断、答え、根拠、行動を定義する。
2. 原典authoring-guide、consulting-thinking、content-to-exhibit-router、componentsと適切なshowcaseを読む。
3. 主張を入力資料・明示した仮定へ対応。数字がなければ定性exhibitを使う。
4. starter-deckを出発点に、fonts/base/layouts/components/illustrations/themeの順でCSSを使う。1600×900、section.slide、header/content/footer契約を保持。
5. 工程はprocess-flow、比較はcomparison-table、判断構造はissue-tree、変換はinput-process-output-layers、公開ゲートはdecision-logへルーティング。
6. 原典webfontは配布license確認ができないため使わない。公式固定OTF由来のNoto Sans CJK JP subset（SIL OFL、source/fonts/OFL.txt）を使う。
7. 原典runtime/QA/exportコードは実行せず自作navigation-ja.jsを使う。arrow/swipe/overview/printとPC同一origin連携を実装。原典runtime使用済みと表現しない。
8. 実ブラウザで初回表示とページ送りを確認し、PNG/PDFを書き出す。未実施検査はQAに残す。

この例は架空・未実施。実績・収益・学習効果を主張しない。


2026-10-14 字体置換: Noto Sans CJK JPは公式 notofonts/noto-cjk固定commit f8d157532fbfaeda587e826d4cd5b21a49186f7c のOTFをsource/fonts/へ未変更保存し、そこからsubset・HTML埋込みを作り直しました。OFLはsource/fonts/OFL.txt、出所はsource/FONT-SOURCE.json。旧クラウド制作記録はPROVENANCE-CLOUD.jsonに保存しています。使用326字のglyph輪郭・横幅・縦メトリクスが一致するため、既存PNG/PDFを保持しています。現在の配布物にOS抽出字体は含みません。
