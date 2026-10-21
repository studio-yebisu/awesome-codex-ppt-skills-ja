---
name: sol-editorial-ja
description: 原典MckEngineを編集誌風へ明示拡張し、大胆な日本語タイポでブランド提案を作る。
---

# 日本語の編集誌風ブランド提案

1. 読者、企画の約束、一日の体験を短く決める。実績のない数値は作らない。
2. upstreamのSKILL.mdとengine-api、core、DeckBuilderを読む。入力は `[{"type":"cover","data":{"title":"..."}}]` という原典schemaを使う。
3. `input/storyline.json`を編集する。作例はcover / quote / section_divider / timeline / big_number / closing の6ページ。目的と原稿に合わせて対応するページ種別・順序・枚数を変える。コード内のMckEngine派生版がネイティブ文字・図形を生成する。
4. Zen Kaku Gothic New、Shippori Mincho、Space Groteskを用意する。書体変更時はJP/SERIF/ENを更新する。
5. ZIP展開先で `python source/rebuild.py --input input/storyline.json --output deck-rebuilt.pptx` を実行。python-pptx/lxmlが必要。原典runtimeと公式TTF/OFLは同梱済み。fonts/の3書体を導入し、PNG描画にはWindowsのMicrosoft PowerPointとsource/render_powerpoint.ps1を使う。詳細はREADME.mdを読む。
6. PPTXと表紙PNGが開くことを確認。今回のlight checkを全ページの品質承認や原典gate通過と扱わない。

原典：likaku/Mck-ppt-design-skill、commit e190e083b715b63172e1c4fea01bc5f9bb21a021。Apache-2.0のLICENSE/NOTICEを保持。これはStudio Yebisuの日本語編集誌レイアウト派生例で、原作者の公式日本語版ではない。

## この方式で気をつけること

- 同梱専用生成器の再生と、自分の原稿から適切な高水準APIを選ぶ一般手順を区別する。
- 原典固定パス ~/.workbuddy/skills/mck-ppt-design を同梱upstreamへ切り替える。references/layoutsは固定原典にも存在しないため、API/容量表/公開引数を読む。

## 単体の本文から使う

この本文は `skill-forks/sol-editorial-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/likaku/Mck-ppt-design-skill/tree/e190e083b715b63172e1c4fea01bc5f9bb21a021

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sol-editorial-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: likaku / 原典条件: Apache-2.0。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/LICENSE
- https://github.com/likaku/Mck-ppt-design-skill/blob/e190e083b715b63172e1c4fea01bc5f9bb21a021/NOTICE
