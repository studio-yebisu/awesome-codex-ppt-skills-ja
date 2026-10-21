---
name: sol-motion-ja
description: 原稿やPPTXを、好みの見た目を比べて選べる単一HTMLの発表資料へ仕上げるfrontend-slidesの日本語入口。
---

# Frontend Slides 日本語入口

原典は `upstream/SKILL.md`。本文・画像・発表の目的から、見た目の比較、制作、全ページの確認までを扱う。HTMLはブラウザーだけで再生し、本文の編集と保存もできる。

1. 新規作成・PPTX変換・既存HTMLの改善のどれかを決める。目的、聴衆、枚数、素材、発表中心か配布中心かを確認する。既に決まっている内容は聞き直さない。
2. 新規作成では `upstream/STYLE_PRESETS.md` と `upstream/bold-template-pack/selection-index.json` から候補を選ぶ。基本形・表現の強い案・自由案の3つの表紙を実際の内容で作り、見て選べるようにする。候補のpreview.mdを先に読み、選択後にそのdesign.mdだけを読む。
3. PPTX変換では同梱 `upstream/scripts/extract-pptx.py` で抽出し、本文・画像・順序・ノートを保つ。今回の作例はこの枝を実行していない。
4. `upstream/html-template.md` と `animation-patterns.md` に従い、`viewport-base.css` 全文を含める。1920×1080のstage全体を等倍比率で拡縮し、スマートフォンでも内容の並び替えをしない。CSS/JS/必要な素材をHTMLへ内包する。
5. 矢印・Space・PageUp/Down・ホイール・スワイプを保つ。入場アニメーションは情報の順序に合わせ、prefers-reduced-motionを保つ。ロック指定がなければEキー/左上の編集ボタン、localStorageへの自動保存、編集済みHTMLの保存を付ける。
6. 全ページを1280×720とスマートフォンで表示する。本文・図の欠け、重なり、読める大きさ、ページ移動、本文編集→保存→再表示を確認する。問題を修正して再確認し、実行範囲と残る制限を記録する。
7. 完成HTML、編集用の原稿/CSS/JS、OFL書体、原典MIT、固定commit、入力、確認結果を渡す。制作と独立評価の合格を分ける。

## 同梱作例

`example/index.html` は架空の図書館企画6ページ。固定stage・段階表示・Eキー編集を適用した。墨紺/ライムの配色と4ページの選書タブは、この企画用の追加設計で、原典の既成テンプレートではない。

再組立: `cd example` → `python source/rebuild.py`。Python標準ライブラリのみ。見出し/本文は `source/slides.html`、配色/配置は `source/adaptation.css`、動作は `source/controller.js`。原典のCSSは変更せず、企画固有の変更を分ける。

この見本では3案からの選択、PPTX変換、画像フォルダー評価を実行していない。新規制作でそれらの工程が必要なら原典どおりに行う。修復後の独立再評価の状況は `example/QA.json` を参照。
