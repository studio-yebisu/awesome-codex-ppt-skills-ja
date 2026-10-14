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

## 単体の本文から使う

この本文は `skill-forks/pptwise-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/liustack/pptwise/tree/65690bc705c1b5db41b5593015675945673da542

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `pptwise-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: liustack / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/liustack/pptwise/blob/65690bc705c1b5db41b5593015675945673da542/LICENSE
- https://github.com/liustack/pptwise/blob/65690bc705c1b5db41b5593015675945673da542/src/cli/packs/license.test.ts
- https://github.com/liustack/pptwise/blob/65690bc705c1b5db41b5593015675945673da542/src/cli/packs/license.ts
