# 企画から作風をそろえたHTMLとPPTXへ

需要調査・資料収集・大綱・頁計画・26作風の選択を経て、原典3変換で編集可能PPTXを作るスキル。一般の手順はSKILL.md、固定出典はSOURCE.json、利用条件はLICENSEとfontsのOFLを参照。

## 作例の条件

指定済み展示企画・Bauhaus Block・3書体・5頁。追加interview・外部検索・原典カード数規則はこの作例に適用していない。任意テーマを自動企画するアプリではない。全26作風・配図生成・native chart/table/数式は未実施。

## 現在版の確認

原典html_packager→html2svg→svg2pptxを再実行し、全5頁をPowerPointで描画して見た。3頁のラベル位置は先行改訂で修復済み。今回、公式BIZ UDPMinchoを導入し、出力PDF内のZen Kaku Gothic New・BIZ UDPMincho・Manropeを実確認した。指定書体名だけで実使用を判断しない。

source/executed-route-receipts.jsonが実変換記録、source/current-native-font-proof.jsonが現在の書体とnative要素。source/zip-replay.jsonは配布ZIPを展開し、同梱buildで3変換を再実行した記録。5頁のnative slide XMLが一致した。独立再評価は別記録。

## 再現

SKILL.mdの環境と字体を用意して `npm ci --ignore-scripts`、`python source/build.py --node <node.exe> --chrome <chrome.exe>`。新出力の全頁・実書体・編集範囲を確認する。
