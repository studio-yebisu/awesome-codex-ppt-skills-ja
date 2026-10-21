---
name: ppt-agent-ja
description: 需要調査、資料収集、構成、ページ計画、26作風での設計を通してHTMLとPPTXを作る。
---

## このスキルでできること

企画の根拠と頁の内容を先に固め、用途に合わせた作風でスライドへ設計できる。

- 困っている状況: 同じカード型を全ページに使うと、関係・順序・工程の違いが伝わらない。
- 必要な入力: テーマ・目的・受け手・発表条件・元資料・必須/禁止・枚数
- 受け取るもの: HTMLプレビューと頁別SVG/PPTX。変換環境が無い場合は原典の降級条件を確認する。
- 必要環境: Node.js 24+ / puppeteer 25.13.0 / dom-to-svg 0.12.2 / esbuild 0.28.2 / Python 3.12 / python-pptx / lxml / Pillow / Chrome / Microsoft PowerPoint 16（PNG/PDF書き出し） / Zen Kaku Gothic New Black / BIZ UDPMincho / Manrope（OFL）
- 作例で試した範囲: 指定済み展示企画を5頁へ計画し、原典Bauhaus BlockのCSSと幾何で設計。原典HTML→DOM/SVG→native PPTXを実行し、全5頁と出力書体を確認。追加interview・外部検索・カード数規則は今回の指定に合わせて不適用。
- 制約: 今回の指定で追加interview・外部検索・カード数規則を適用していない。原典の全工程合格ではない。 / native chart/table/数式、全26作風と配図生成は未実施。 / 修復後の独立再評価は未了。


# 調査と構成を固めてから、ページを設計する

原典 Akxan/ppt-agent-skill / 01825dee2ad40a8c719824252605396b9a570d57 / MIT。非公式の日本語案内。upstream/SKILL.mdとreferencesを読む。

1. 目的・場面・読み手・求める行動・内容・枚数・必須/禁止を調査する。原典は3問または7問のinterviewと回答待ちを必須にする。既にユーザーが指定・委任した範囲は引き継ぎ、不足と実際の変更範囲を記録する。
2. 外部情報を検索・整理し、入力資料と照合する。情報取得能力が無ければユーザーの材料に依拠する。根拠の無い数値・実績を作らない。
3. 結論と根拠、Part、頁数へ大綱を構成する。原典の章2頁以上などの自己確認を行う。8頁以下では原典の軽量化が使える。
4. 内容とカード種類・位置・layout_hintをページ計画JSONへ分け、必要な確認を行う。原典は内容頁に3カード以上・2種類以上・dataカード1つ以上を求める。根拠不足を架空データで埋めない。規則を変える場合は用途とユーザー指定に基づく差分を明示する。
5. 実在する26作風から選び、style.jsonを作る。必要な意味のある画像を用意し、原典のHTML設計規範に沿って1280×720の頁を作る。HTMLは計画の後に作り、同じカード配置だけで全頁を埋めない。
6. 原典html_packager→html2svg（Puppeteer/dom-to-svg）→svg2pptxを実行する。Node/変換依存が使えない場合の原典の降級はHTMLのみで、PPTX成功と説明しない。実装差分がある場合は原本とdiffを残す。
7. 原典quality self-checkと全頁の実描画を行い、情報・書体・配置・図の対応を確認して直す。原典文書はPowerPoint365でSVGを「図形に変換」と説明するが、この固定pinの実converterは文字・rect/circle/line/pathをnative OOXMLへ直接解析する。納品の編集範囲は実物で確認する。

## この5枚の作例

指定済みの展示企画・Bauhaus Block・3書体・5頁で制作したため、追加interviewと外部調査、原典カード数/dataカードの割当、カード数に基づくquality条件は適用していない。幾何中心の構成と実変換経路の作例で、原典の全工程への適合や全26作風の制作を示すものではない。この差分を一般の手順へ拡張しない。

文字・図形はnative、chart/table/数式は使用していない。原典3変換の実行記録はsource/executed-route-receipts.json。Windows fileURL・font待ち・cacheのadapterと原本を同梱する。欠落していたBIZ UDPMinchoを公式TTFから導入し、現在PDFの実書体を確認。全5頁を見て3頁のlabel位置を確認した。独立再評価は別記録。

## 再現と書体

Node.js24+、puppeteer25.13.0/dom-to-svg0.12.2/esbuild0.28.2、Python＋python-pptx/lxml/Pillow、Chrome。PowerPoint描画にはWindows＋Microsoft PowerPoint。同梱fontsのZen Kaku Gothic New Black、BIZ UDPMincho、Manropeと各OFLを確認し、作成者・受け手の端末へ導入する。指定名だけでは置換を防げないので、PDF/実表示の書体も確認する。

`npm ci --ignore-scripts`、既存Python依存を用意して `python source/build.py --node <node.exe> --chrome <chrome.exe>`。新出力の全頁を確認する。再現コードは現在のHTML5頁を変換する処理で、任意テーマを自動企画するアプリではない。

原典: https://github.com/Akxan/ppt-agent-skill/tree/01825dee2ad40a8c719824252605396b9a570d57

## 単体の本文から使う

この本文は `skill-forks/ppt-agent-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Akxan/ppt-agent-skill/tree/01825dee2ad40a8c719824252605396b9a570d57

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `ppt-agent-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: Akxan / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Akxan/ppt-agent-skill/blob/01825dee2ad40a8c719824252605396b9a570d57/LICENSE
