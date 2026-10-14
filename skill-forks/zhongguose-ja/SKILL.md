---
name: zhongguose-ja
description: 中国色Zhongguoseの原稿構造・左上章ナビ・元HTML templateを使い、日本語の対話式スライドを作る。HTMLとassets一式を生成し、PPTXは生成しない。
license: MIT
---
# 中国色Zhongguose 日本語ガイド

原典: tanglele110-hash/zhongguose-ppt-skill、固定commit `f4c2af8ff832133822afdce87ed2d6d760631ef4`。MIT ©2026 木渡川。字体とlibrariesの条件は別添原文を保持。中国色・framework navigation・manuscript workflow・templateは木渡川、製品と対話概念は帰蔵のguizang-ppt-skillに着想。日本語案内と字体adapterを追加しました。

MDだけをAIへ渡す場合も、[原典全文SKILL](https://github.com/tanglele110-hash/zhongguose-ppt-skill/blob/f4c2af8ff832133822afdce87ed2d6d760631ef4/skills/zhongguose-ppt-skill/SKILL.md)と[template](https://github.com/tanglele110-hash/zhongguose-ppt-skill/tree/f4c2af8ff832133822afdce87ed2d6d760631ef4/skills/zhongguose-ppt-skill/assets/template-zhongguose)を読み、実物を取得してください。自分の原稿から原典content-architecture/layout-patterns/visual-systemの順に必要な契約を参照します。

日本語再現のファイルと全字体は同配布の `zhongguose-ja.zip` 内の[example](example/index.html)にあります。MD単独でassets添付済みとは仮定しません。[SOURCE](SOURCE.json)にURL/hash、[一式ZIP](../../downloads/zhongguose-ja.zip)を用意しています。

1. 原稿の固定文言・根拠・章を[原稿](example/input/MANUSCRIPT.md)とsource-logicへ記録してlock。章は原稿から決め、版式を先に当てはめない。承認済み自律制作では追加confirmationを挟まず、その判断をinput/theme.jsonへ記録する。
2. 1頁1役割のslide-architectureを先に決め、日本語主題、短い英語label、階層、元patternを選ぶ。各頁はtop-level section.slide、section-tabsはflat span.tabにする。
3. 原典 `assets/template-zhongguose/` を丸ごと複製。元indexのCSS・縦pager・Esc/B・ASCII・Motion helpersを保持し、原稿と日本語font/color/layoutだけ局所diff。accent/accent-rgb/accent-onは原典表の一行から対で選び、中国色を日本の伝統色と表示しない。
4. 全文面確定後に原典 `subset-cover-font.py` を実行する。日本語例では完全配布Shippori Mincho TTFを渡し、kanaを含むcover欠落検査、copyright・OFL・hashだけ[局所patch](example/source/subset-japanese.patch)。qiji seedは保存原本に残す。日本語の通常本文はBIZ UDPGothic、英字はManrope、全TTF/OFLと固定取得URL/hashを同梱。
5. `python example/source/rebuild.py`。Python3.10+とFontTools/Brotliが必要（`python -m pip install "fonttools[woff]"`）。原典Node scriptsはNode18+、閲覧はブラウザだけ。index.htmlとassets/を一式でWeb配信し、単体HTMLと称さない。
6. 必要buildと代表出力の初回表示、元navigation1→2、SKILL quick_validateを確認。全頁詳細目視、独立review、採点は依頼された場合だけ。実施/未実施を[QA](example/QA.json)へ正確に残す。

題材変更ではMANUSCRIPT/source-logic/architecture、source/rebuild.py内のslide文面と色を同時に更新し、最終HTMLでsubsetを再生成します。作例は6枚・3章の架空回遊案。実在人物・会場・日程・費用・実績を発明していません。
