---
name: slidefly-ja
description: 同じ図形を頁間で動かし、話をつなぐHTMLと編集可能なPPTXを作る。
---

# 同じ図形が、次のページへつながる

原典andyluu98/slidefly / 7de466df3f2e0199c4939ccbe4490688d4165fa3 / MIT。非公式の日本語案内。upstream/SKILL.mdと必要referencesを読む。

1. 目的・読み手・元資料・枚数・文字量・作風を整理する。原典は85作風、21頁型、17フレームを備える。作風指定がなければpick-styles.pyの3候補を参考にする。34の二層作風では対応.art.mdを読み、主張ごとの専用SVGを用意する。
2. 頁ごとの主張と型を計画する。同じ形がどの関係を引き継ぐかを決め、named actorとposeへ対応させる。原典engineがactorsを作るため、独自の.actorsブロックで代替しない。独自作風は原典のfree-layoutとMorph契約を読む。
3. 原典CSS/engine/nav/frames等を決められた順に読み込み、本文をreveal要素へ置く。同じ図形やdata-morph-idの要素が、移動・拡縮・形状変化で次の頁につながる。文字の配置と図形の動線を分ける。
4. inline-assets.pyで単一HTMLへまとめる。ブラウザーで全頁を開き、文字・重なり・余白・型の反復とdeck.audit()を確認し、動きの途中も見て直す。見た目の合格は監査結果だけで決めない。
5. PPTXが必要ならexport-pptx.pyで出力する。文字とactorは編集可能、inline SVGはvector画像。変換器が認識するクラス/タグ・明示改行・SVGの配置条件を守り、PowerPointでも全頁を開く。Morph設定があることと実際のアニメーション再生は分けて確認する。

## この作例で試したこと

独自walk作風の6頁。道・地点は創作で、実在の案内ではない。元の3actorが全5区間で移動・拡縮する。元の次頁ボタンでbefore/100ms中間/1400ms後を記録し、同じIDを保持することを確認。全6頁のWeb描画と原典監査も確認した。

独自h1/h2が原典exporterで除外されるため、同じ見た目のrole=heading付きdivへ変更。改行はbr、SVGは原典対応の直接配置へ移し、currentColorを同じ明示色へ解決した。原典コードは未改変。現在の全6頁をPowerPointで開き、見出しと分岐図の欠落がないことを確認。別コピーのnative文字変更・保存・再表示も実施した。Webの英数字Space GroteskはPPTXでは原典body字体のZen Kaku Gothic Newへ置換される。

## 入力と再現

Python3.10+標準ライブラリ、モダンブラウザー。PPTX表示はPowerPoint2019/365と使用字体。原典Google Fontsのオンライン読込とは異なり、この作例は公式TTF/OFLをHTMLに内包している。PPTXは字体非埋込。fonts/を利用端末へ導入する。

`python upstream/scripts/inline-assets.py source.html index.html` → `python upstream/scripts/export-pptx.py index.html deck.pptx`。別題材では入力・各頁の主張・作風・actor/pose・必要な図を先に設計する。再現コードは保存済み作例の梱包・変換で、任意の原稿を自動企画するアプリではない。

85作風の比較、二層作風の全頁専用イラスト、PowerPoint内の実Morph再生、独立した最終再評価は未実施。
