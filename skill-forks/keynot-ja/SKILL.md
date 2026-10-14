---
name: keynot-ja
description: Keynotのブランド抽出と元HTML例のCSS・inline navigation/reveal/swipe/fullscreenを使い、日本語の単一HTMLスライドを作る。
license: MIT
---
# Keynot 日本語ガイド

原典: **shawnzam/keynot**、固定commit `d1f9e449ddb89da707b489cb69c520a64975b47c`、MIT ©2026 Shawn Zamechek。字体は別のOFL-1.1です。

このMDだけをAIへ渡す場合も、次の固定原典を読んで実物を取得してください。

- [全文SKILL](https://github.com/shawnzam/keynot/blob/d1f9e449ddb89da707b489cb69c520a64975b47c/skills/keynot/SKILL.md)
- [元HTML例・CSS・完全controller](https://github.com/shawnzam/keynot/blob/d1f9e449ddb89da707b489cb69c520a64975b47c/examples/keynot-for-zombies.html)
- [原文MIT](https://github.com/shawnzam/keynot/blob/d1f9e449ddb89da707b489cb69c520a64975b47c/LICENSE)

日本語再現には、同じ配布元の **keynot-ja.zip**（`downloads/keynot-ja.zip`）を取得し、`example/input/`のブランド/原稿、`example/source/`の原典原本・CSS・HTML・JS・rebuild.py、`example/source/fonts/`の実TTF/OFLを使います。[作例](example/index.html)と[一式ZIPへのサイト相対リンク](../../downloads/keynot-ja.zip)も利用できます。MD単独では日本語ソースや字体が添付されたとは仮定しないでください。

1. [BRAND](example/input/BRAND.md)を自分のブランド記述へ置換。原典Step1のprimary/accent/neutrals正確なhex、serif/sans組、色の使用比率、版式・声・文字wordmarkを、コードを書く前に[brand-record](example/input/brand-record.json)へ抽出する。
2. [依頼文](example/PROMPT.md)と[原稿](example/input/MANUSCRIPT.md)から各頁の一つの役目を決める。原典のtitle、split panel、approach rows、large display quote、feature bars、closeを内容に合わせ、同じカード列を反復しない。
3. 元HTMLのdeck/slide/nav/rotate/printとCSSを実使用する。[原本](example/source/upstream/)を保持し、和文サイズ・安全な行高・字間・ブランド色・SVG説明図は[local CSS](example/source/adaptation.css)へ分ける。
4. 完全inline JSを一つの単位で保存する。go()の`cur = (n + slides.length) % slides.length`、前後の±1、swipeの差、const slidesの宣言を改変しない。JSを含むHTMLへ一括文字置換をしない。日本語chromeの対象箇所だけを編集し、処理後にJS部を読む。
5. CDN字体は公式固定TTFのinline @font-faceへ置換し、元OFLを保持。作例のGoogle Fonts pinは `66928797f271fed5ee428544e7229685e2d90127`、[URL/hash](example/source/FONT-SOURCE.json)から取得可能。OS字体の抽出や商標・外部写真を流用しない。
6. `python example/source/rebuild.py` で単一HTMLを作る。元controllerの算術はそのまま、同一originの0-based yebisu-slide/pageは[末尾patch](example/source/controller.patch)だけ追加。字体/CSS/JS/原文条件を内包する。

編集はHTML/SVG/CSS/JS。作例は架空の体験案、日時・会場・費用・参加人数は未定で、実施実績・安全性能の実証を発明しません。承認済み自律制作でブランドと構成を判断し、工程ごとに新規確認を挟みません。確認は必要な梱包build、代表出力の初回表示と元navigation1→2、短いSKILL検証だけ。[QA](example/QA.json)に未実施の範囲を保持し、全頁詳細検査・独立採点・ZIP再実行を必須にしません。
