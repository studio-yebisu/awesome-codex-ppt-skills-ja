---
name: sebastian-178-ja
description: NomiciAI mbb-page-makerのstarterとCSSを使い、主張・根拠・図解を日本語のHTMLスライドへ組む。原典runtimeを使った作例ではない。
license: Apache-2.0
---
# mbb-page-maker 日本語ガイド

原典は NomiciAI/mbb-page-maker、固定commit `36074669b8041783d9637a87dfed2a8733d47357`。**rootの[LICENSE](LICENSE)はApache-2.0、[原文SKILL](example/source/SKILL.md)はMITと記載しており、不一致は未解決です。** 両原文とSaitop at NomiciAIの帰属を保持します。全体をMITとして再許諾しません。

[完成HTML](example/index.html)は「動画一本を、教材へ。」という架空の教材化企画7頁。[入力](example/input/)と[依頼文](example/PROMPT.txt)を自分の題材へ置き換えて使えます。編集対象はHTML/CSS/JavaScriptで、PPTXは生成していません。

1. 読者が行う判断を定め、答え・根拠・次の行動を[入力](example/input/)へ書く。数字や効果は根拠を添え、仮定を実測にしない。
2. [authoring-guide](example/source/references/authoring-guide.md)、[content-to-exhibit-router](example/source/references/content-to-exhibit-router.md)、[components](example/source/references/components.md)から内容に合うexhibitを選ぶ。工程・比較・判断構造を同じカード列へ押し込まない。
3. [未変更starter](example/source/UPSTREAM_STARTER.html.txt)の1600×900、`section.slide`→header/content/footerを維持し、fonts/base/layouts/components/illustrations/themeの6層を使う。作例の日本語調整は[deck-ja.css](example/source/assets/css/deck-ja.css)、原稿は[source/index.html](example/source/index.html)にある。
4. [build.py](example/source/build.py)は頁原稿を組み、公式字体をsubset化して単一HTMLへ埋め込む自作packager。Python＋fontToolsを使い、`python -X utf8 example/source/build.py`で再生成できる。元の字体OTFとOFLは[fonts](example/source/fonts/)に同梱。出所とhashは[FONT-SOURCE.json](example/source/FONT-SOURCE.json)。OS字体を抽出して配布しない。
5. 操作は[自作navigation-ja.js](example/source/navigation-ja.js)への差替え。原典runtime/QA/exportは実行していない。←/→、Space、Oの一覧、Escape、swipeで操作できる。必要なら既存Chromium＋Playwrightで[source/render.py](example/source/render.py)を使う。Windows版[render-pc.py](example/source/render-pc.py)はlocalhost:8178の配信を前提とする。

[PNG](example/render/)と[PDF](example/deck.pdf)は受領済み出力です。今回の取込みでは全面再生成・追加の全頁検査は行っていません。2026-10-14に公式notofonts固定OTFへ字体経路を変更し、使用326字の輪郭・幅・縦メトリクス一致を確認したため既存PNG/PDFを保持しました。[旧クラウド制作記録](example/PROVENANCE-CLOUD.json)と[現行出所](example/PROVENANCE.json)を分けて保存。字体はOFL-1.1、subsetは改変物、同梱公式OTFは未変更です。

未実施の原典QAや原典runtimeを「成功」と表現しない。[QA](example/QA.json)と[実行条件](example/README.md)の範囲を保ち、依頼で必要になった表示・出力だけ確認します。

## 単体の本文から使う

この本文は `skill-forks/sebastian-178-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/NomiciAI/mbb-page-maker/tree/36074669b8041783d9637a87dfed2a8733d47357

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-178-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: NomiciAI / 原典条件: Apache-2.0 / SKILL内MIT記載。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/NomiciAI/mbb-page-maker/blob/36074669b8041783d9637a87dfed2a8733d47357/LICENSE
