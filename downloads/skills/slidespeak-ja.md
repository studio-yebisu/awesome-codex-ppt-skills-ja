---
name: slidespeak-ja
description: SlideSpeak原典engineでbrief由来の日本語styleを作り、実HTMLを生成する。
---

## このスキルでできること

題材と見た目の条件から、その資料専用の書体・配色・レイアウトを持つHTMLへ組む。

- 困っている状況: 既成テーマを選ぶだけでは、ブランドの色・書体・ページ構成が合わない。
- 必要な入力: 題材・原稿・聴衆と、見た目の説明・ブランドURL・参考画像などの手掛かり。
- 受け取るもの: 資料専用の配色・書体・配置定義、頁ごとの内容データ、ブラウザーで発表するHTML。
- 必要環境: Node20+とnpm依存 / 原典engineと6ファイルstyle / 新規制作時はホストLLM。画像APIは任意。
- 作例で試した範囲: 書店の仮ブリーフから専用6ファイルstyleを作り、保存したslide-treeを原典engineでHTML化。全6頁を確認し、原典style/occupancy/legibility/richness検査を通した。
- 制約: 主出力は1920×1080のHTML。編集可能PPTXの出力例ではない。 / 原典engineへ、作者が用意したslide-treeをLLMClientで渡した。ライブLLMの生成は未実行。 / FAL/AI画像/stock画像は未使用。コード図形だけで制作した。 / 全6頁と原典検査を確認。独立再評価は修復後に実施予定。


# ブリーフから独自デザインを作る

1. 同梱upstream/SKILL.md、docs/INTEGRATION.md、docs/SKILL-FORMAT.mdを読む。題材と見た目のbriefを決め、既存preset名で代用しない。
2. tokens、chrome、components、layout grammar、image-style、SKILLの6ファイルを作る。原典templates規約とgateに合わせる。見出し・本文・英数字の書体役割を決め、日本語は意味単位で改行し、過密ならページを分ける。
3. 原典loadSkill→generateDeck→wrapAsStandaloneHtmlを使う。LLMClientに完成slide-treeを渡し、原典検証・brand guard・rendererを通す。無料のコード図形だけでも制作できる。
4. build.mtsと独自style/入力を作品ZIPから利用。Node20+と `npm ci` が必要。原典gateを実行し、全頁の本文・図・改行・ページ移動を確認して直す。確認範囲を記録する。
5. 原典MIT、使用フォントの原TTF/OFLを保持。ホスト専有runtimeやAPI keyをZIPへ含めない。

同梱 `example/` のstyle/入力/build.mtsと原典engineを使う。今回のslide-treeは作者が用意してLLMClientへ渡したもの。ライブLLM呼出しの実行例とは区別する。自分の資料ではbriefとstyleを作り直し、原典gate・全ページ確認を行う。

## 単体の本文から使う

この本文は `skill-forks/slidespeak-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/SlideSpeak/slide-design-skill/tree/5e87d8ae71f6306e0c88f4910e6c09114581d91b

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `slidespeak-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: SlideSpeak / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/SlideSpeak/slide-design-skill/blob/5e87d8ae71f6306e0c88f4910e6c09114581d91b/LICENSE
