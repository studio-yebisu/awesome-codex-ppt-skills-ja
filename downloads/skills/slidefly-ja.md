---
name: slidefly-ja
description: SlideFly原典の同一actorとposeを使い、日本語Morph状HTMLとPPTXを作る。
---

# 同じ形が、ページをまたいで動くスライド

1. upstream/SKILL.mdとreferences/co-che-morph.mdを読む。題材の移動・関係をnamed actorに割り当て、各ページで位置/大きさ/形を変えるposeを作る。
2. 原典morph-engine/nav/framesを使い、HTMLのstage/slide構造を保つ。独自layoutは原典free-layout指針で作る。本文は意味の切れ目で改行、明示改行はwhite-space:pre-line。
3. 見出し/本文はZen Kaku Gothic New、英数字はSpace Groteskなど役割を決める。図は内容を説明し、actorと文字が重ならないよう配置。
4. `python upstream/scripts/inline-assets.py source.html index.html` で単一HTML。PPTXが必要なら原典 `export-pptx.py index.html deck.pptx` を使う。通常Pythonだけで実行できる。
5. deck.auditと主画面・一回の動きを確認。PPTXの編集可能文字/actor、vector SVG、Morph設定と実再生を区別して報告する。

技能本文だけでruntimeは付属しない。一式ZIPと作品ZIPのsource/walk.cssを使用。原MITと使用原TTF/OFLを保持。書体の端末導入は手動。

## 単体の本文から使う

この本文は `skill-forks/slidefly-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/andyluu98/slidefly/tree/7de466df3f2e0199c4939ccbe4490688d4165fa3

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `slidefly-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: andyluu98 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/andyluu98/slidefly/blob/7de466df3f2e0199c4939ccbe4490688d4165fa3/LICENSE
