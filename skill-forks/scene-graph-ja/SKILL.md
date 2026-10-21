---
name: scene-graph-ja
description: ppt-scene-graphのOutlineSpec/SlideSpec→create_from_outline→beautifyで、日本語の編集可能PPTXを作る。原典APIの制約と同版vendor修復を保持する。
license: MIT
---
# PPT Scene Graph 日本語ガイド

原典: eluckydog/ppt-scene-graph、固定commit `646e3dc4b72a444278d320c8984d5986d7fbf4bb`。MIT ©2026 PPT Scene Graph Contributors。vendorのpython-pptxはMIT ©2013 Steve Canny、字体は個別のOFL-1.1です。

このMDだけをAIへ渡す場合も、[固定SKILL](https://github.com/eluckydog/ppt-scene-graph/blob/646e3dc4b72a444278d320c8984d5986d7fbf4bb/SKILL.md)、[実pipeline.py](https://github.com/eluckydog/ppt-scene-graph/blob/646e3dc4b72a444278d320c8984d5986d7fbf4bb/ppt_scene_graph/pipeline.py)、[DesignSystem](https://github.com/eluckydog/ppt-scene-graph/blob/646e3dc4b72a444278d320c8984d5986d7fbf4bb/ppt_scene_graph/design.py)、[原文MIT](https://github.com/eluckydog/ppt-scene-graph/blob/646e3dc4b72a444278d320c8984d5986d7fbf4bb/LICENSE)を読んでください。日本語再現は同じ配布元の **scene-graph-ja.zip**（`downloads/scene-graph-ja.zip`）から`example/input/`、`example/source/runtime/`、`example/source/fonts/`と`rebuild.py`を取得します。MD単独で修復済みsourceや実字体が付属すると仮定しません。

1. [原稿](example/input/MANUSCRIPT.md)と[大綱](example/input/outline.json)を自分の題材へ置換。元OutlineSpec/SlideSpecのcover/section/content/endingを選び、1頁の主題と少ない本文を決める。coreに概念図factoryがないため、別のアートengineを原典機能として追加しない。
2. `python example/source/rebuild.py`で元create_from_outlineを実行しdraftを保存。その同じ原稿を元beautifyへ通し、projection deckを作る。theme引数は原典の表示名検証に合わせ`load_theme('projection').name`を使う。[マッピング](example/input/theme-source-map.json)に実設定を残す。
3. 原典vendorのparts/欠落は、同版公式python-pptx1.0.2から8ファイルだけ補完済み。元原本と[補完URL/version/hash/一覧](example/source/vendor-parts-repair.json)、[個別MIT](example/source/dependencies/python-pptx-wheel-LICENSE.txt)を保持する。別engineへ切り替えない。lxml/Pillow/typing_extensions/XlsxWriterは[実行依存](example/source/dependencies/REQUIREMENTS.json)。
4. [局所diff](example/source/design-ja.patch)でDesignSystemをBIZ UDPGothicに対応し、[font diff](example/source/pipeline-ja.patch)でa:ea/a:cs/langを設定する。元palette・FONT_SIZES・factoriesを保持。章番号と章題の余白は明示したtheme_layout_adapterで補正し、公式[TTF/OFL](example/source/fonts/)を使う。pt値は原典コードの設定であり、距離に対する最適値の実証ではない。
5. PowerPoint通常exportは[case exporter](example/source/render_powerpoint.ps1)を使う。Application.Quitを呼ばず、明示した作例だけCloseする。PPTXの文字/長方形枠が編集正本、PNGは表示用。

原典のparse_slide宣言はこのcommitで未実装/exportなし。使ったとは記録しない。元beautifyは非文字図形の既存色を残すため、このforkはsource/theme_layout_adapter.pyで旧primary/accentを選択テーマへ移行し、帯の重複を除く。これは原典外の局所修正です。装飾後の型検出でcover/sectionがcontentになることがある。notesフィールドもPPTX speaker notesへは書かれない。実装と宣言を混同しない。

この自作教材は可読性改善や最適pt値の実測ではありません。修正依頼に基づき全頁をPowerPointで描画し、番号/見出しの接触、字形、旧テーマ色、本文同一性を確認します。draftと完成の同頁を並べて、どこが元API、どこが局所補正かを明記。元evaluateは粗い診断として実行して警告を残し、独立評価の点数へ流用しません。QA.jsonに実行・目視・未実施を分け、独立レビューやZIP再実行を未了のまま合格としません。
