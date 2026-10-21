---
name: sebastian-178-ja
description: NomiciAI mbb-page-makerのstarterとCSSを使い、主張・根拠・図解を日本語のHTMLスライドへ組む。原典runtimeとGolden Pathで検査・出力する。
license: Apache-2.0
---
# mbb-page-maker 日本語ガイド

原典は NomiciAI/mbb-page-maker、固定commit `36074669b8041783d9637a87dfed2a8733d47357`。**rootの[LICENSE](LICENSE)はApache-2.0、[原文SKILL](example/source/SKILL.md)はMITと記載しており、不一致は未解決です。** 両原文とSaitop at NomiciAIの帰属を保持します。全体をMITとして再許諾しません。

[完成HTML](example/index.html)は「動画一本を、教材へ。」という架空の教材化企画7頁。[入力](example/input/)と[依頼文](example/PROMPT.txt)を自分の題材へ置き換えて使えます。編集対象はHTML/CSS/JavaScriptで、PPTXは生成していません。

1. 読者が行う判断を定め、答え・根拠・次の行動を[入力](example/input/)へ書く。数字や効果は根拠を添え、仮定を実測にしない。
2. [authoring-guide](example/source/references/authoring-guide.md)、[content-to-exhibit-router](example/source/references/content-to-exhibit-router.md)、[components](example/source/references/components.md)から内容に合うexhibitを選ぶ。工程・比較・判断構造を同じカード列へ押し込まない。
3. [未変更starter](example/source/UPSTREAM_STARTER.html.txt)の1600×900、`section.slide`→header/content/footerを維持し、fonts/base/layouts/components/illustrations/themeの6層を使う。作例の日本語調整は[deck-ja.css](example/source/assets/css/deck-ja.css)、原稿は[source/index.html](example/source/index.html)にある。
4. [build.py](example/source/build.py)で日本語本文と公式固定OTFの必要字形を作る。字体ファイルとOFLを保持し、デッキの全フォント役割を同じ同梱Noto Sans CJK JPへ結ぶ。更新後は必ず実描画し、字体メトリクス一致だけで古い画像を再利用しない。
5. 未変更の原典runtime.jsを読み込み、元のキー・一覧・縮尺・監査・書出しを使う。親プレイヤー接続だけは原典キー操作へ変換する局所bridgeを使う。自作navigation-ja.jsは過去の実装で現在の入口ではない。
6. 原典Golden Pathのquality、contrast、fit、renderを実行し、全頁を目視する。Windowsではfile URL/PDF出力パスだけを変換するsource/windows-paths.diffが必要だった。検査条件・閾値は変更しない。実行ログはsource/golden-path-original-receipt.jsonとgolden-path-windows-receipt.jsonに分ける。

現作例は原典runtimeのまま全4工程が成功し、同梱字体で全7頁PNG/PDF/単体packageを再生成した。工程矢印を本文外へ移し、実演の語中改行と二重ページ番号を修正。HTML/CSSは原稿と元6層を保持する。作者の実行検査と独立評価・人による採用を区別する。

## 現在の作例の実施範囲（Round4）

数値の根拠がない箇所は、工程図・比較表・判断の分岐を選んだ。判断図には接続線を入れ、小テストは3欄の幅をそろえ、日本語を句のまとまりで読めるようにした。

- 架空の企画。学習効果・制作時間・収益の実績は含まない。原典のroot LICENSEとSKILLの記載不一致は解消していない。
- 原典runtimeを置き換えた初期実装は旧履歴。現在は元runtimeと局所catalog bridgeを使用。
- 日本語用CSSは原典CSSの後に追加。新しい原稿では同じ4検査と全頁の実描画をやり直す。

全7頁の実描画と個別の動作証拠は制作側の確認。独立Kimi K3/Opus5.5の新しい版の評価は別に行う。過去の採点を新しい画像へ引き継がない。
