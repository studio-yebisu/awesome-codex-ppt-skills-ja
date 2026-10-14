---
name: pptwise-ja
description: 原典pptwise CLIとIR v5で、企画の関係をnative図形と大きな日本語見出しのPPTXへ制作する。
---

# 日本語の拠点提案

1. 読者、提案の目的、時間、架空条件を決める。実績や予算を作らない。
2. upstream/SKILL.mdと必要なspec/components/validate referenceを読む。schema、narratives、themesの元CLI出力から始める。
3. input/deck.jsonはv5。kindとtyped componentsを意味で選び、flowchartは方向、hub_spokeは中心との関係、architectureは構成を表す。
4. input/theme.jsonは原典Rallyからの明示派生。色・OSS書体・ruled surfacesを設定。IRに座標やface指定を加えず、PPTXを後加工しない。
5. Node22.19+を用意しruntime/でnpm ci。展開rootで `node runtime/dist/cli.js validate input/deck.json`、次に `node runtime/dist/cli.js render input/deck.json -o deck-rebuilt.pptx --no-git-ignore`。
6. fonts/のZen Kaku Gothic NewとSpace Groteskを導入。PowerPointで主出力が開くことを確認し、PNG/PDFはsource/render_powerpoint.ps1を使う。

SKILL本文だけでは生成できず、input、theme、原典runtimeが必要。原典MIT、commit65690bc705c1b5db41b5593015675945673da542。原作者の公式日本語版ではありません。
