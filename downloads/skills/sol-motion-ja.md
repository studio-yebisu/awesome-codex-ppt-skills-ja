---
name: sol-motion-ja
description: 原稿やPPTXを、好みの見た目を比べて選べる単一HTMLの発表資料へ仕上げるfrontend-slidesの日本語入口。
---

## このスキルでできること

内容と見た目を分けて検討し、ブラウザーで発表・本文編集できる単一HTMLへ組む。

- 困っている状況: 原稿だけでは、発表の見せる順番や画面構成を確かめにくい。
- 必要な入力: 目的・聴衆・枚数・発表/配布の密度・原稿や画像。変換時は元PPTX。
- 受け取るもの: 固定16:9の単一HTML、編集用CSS/JS/原稿、書体・帰属・確認記録
- 必要環境: 原典SKILLを読める制作エージェント / モダンブラウザー / 同梱例の再組立はPython3標準ライブラリ
- 作例で試した範囲: 6頁を固定stageへ組み、段階表示と本文編集を適用。企画固有の選書タブは本文と本の強調を連動。全6頁・3タブを確認し、実際に文字を直してHTML保存・再表示した。
- 制約: 出力は単一HTML。PPTXの編集可能化は扱わない。 / 3案からの選択・PPTX変換・画像フォルダー評価は今回未実行。 / 選書タブと配色/SVGは本作例の追加設計。原典既成テンプレートではない。 / 本文の編集・自動保存・HTML保存と再表示を実確認。修復後の独立再評価は未了。


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

## 単体の本文から使う

この本文は `skill-forks/sol-motion-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/zarazhangrui/frontend-slides/tree/9906a34d640d2111f724544cbc50f7f130569ae1

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sol-motion-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: zarazhangrui / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/LICENSE
