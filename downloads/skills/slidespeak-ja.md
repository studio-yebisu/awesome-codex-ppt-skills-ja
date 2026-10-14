---
name: slidespeak-ja
description: SlideSpeak原典engineでbrief由来の日本語styleを作り、実HTMLを生成する。
---

# 日本語の編集誌スライド

1. 同梱upstream/SKILL.md、docs/INTEGRATION.md、docs/SKILL-FORMAT.mdを読む。題材と見た目のbriefを決め、既存preset名で代用しない。
2. tokens、chrome、components、layout grammar、image-style、SKILLの6ファイルを作る。原典templates規約とgateに合わせる。見出し・本文・英数字の書体役割を決め、日本語は意味単位で改行し、過密ならページを分ける。
3. 原典loadSkill→generateDeck→wrapAsStandaloneHtmlを使う。LLMClientに完成slide-treeを渡し、原典検証・brand guard・rendererを通す。無料のコード図形だけでも制作できる。
4. build.mtsと独自style/入力を作品ZIPから利用。Node20+と `npm ci` が必要。原典gateと主画面初回表示だけを確認し、実行範囲を記録する。
5. 原典MIT、使用フォントの原TTF/OFLを保持。ホスト専有runtimeやAPI keyをZIPへ含めない。

技能本文だけではengineを含みません。一式ZIPのupstream sourceと作品ZIPのstyle/入力/build.mtsを使用。

## 単体の本文から使う

この本文は `skill-forks/slidespeak-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/SlideSpeak/slide-design-skill/tree/5e87d8ae71f6306e0c88f4910e6c09114581d91b

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `slidespeak-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: SlideSpeak / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/SlideSpeak/slide-design-skill/blob/5e87d8ae71f6306e0c88f4910e6c09114581d91b/LICENSE
