---
name: sol-editorial-ja
description: 原典MckEngineを編集誌風へ明示拡張し、大胆な日本語タイポでブランド提案を作る。
---

# 日本語の編集誌風ブランド提案

1. 読者、企画の約束、一日の体験を短く決める。実績のない数値は作らない。
2. upstreamのSKILL.mdとengine-api、core、DeckBuilderを読む。入力は `[{"type":"cover","data":{"title":"..."}}]` という原典schemaを使う。
3. `input/storyline.json`を編集する。cover / quote / section_divider / timeline / big_number / closing の順で6ページ。コード内のMckEngine派生版がネイティブ文字・図形を生成する。
4. Zen Kaku Gothic New、Shippori Mincho、Space Groteskを用意する。書体変更時はJP/SERIF/ENを更新する。
5. ZIP展開先で `python source/rebuild.py --input input/storyline.json --output deck-rebuilt.pptx` を実行。python-pptx/lxmlが必要。原典runtimeと公式TTF/OFLは同梱済み。fonts/の3書体を導入し、PNG描画にはWindowsのMicrosoft PowerPointとsource/render_powerpoint.ps1を使う。詳細はREADME.mdを読む。
6. PPTXと表紙PNGが開くことを確認。今回のlight checkを全ページの品質承認や原典gate通過と扱わない。

原典：likaku/Mck-ppt-design-skill、commit e190e083b715b63172e1c4fea01bc5f9bb21a021。Apache-2.0のLICENSE/NOTICEを保持。これはStudio Yebisuの日本語編集誌レイアウト派生例で、原作者の公式日本語版ではない。


