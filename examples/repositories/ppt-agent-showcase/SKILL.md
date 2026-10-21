---
name: ppt-agent-ja
description: 需要調査、資料収集、構成、ページ計画、26作風での設計を通してHTMLとPPTXを作る。
---

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
