# Beatdeck・日本語キット

[SKILL](SKILL.md)から始める。6場面・15段階の架空パン店概念資料。元npm initでscaffoldした`runtime/`、未変更原本、局所deck、原稿/audit/brand、字体/OFLと依存noticeを含む。

```powershell
npm --prefix runtime ci --ignore-scripts --no-audit --no-fund
npm --prefix runtime run build
python -m http.server 8000 --bind 127.0.0.1 --directory runtime/dist
```

`http://127.0.0.1:8000/#1.1`を開く。元stageの1clickで1beat進む。完成distとassetsを一式で使い、HTML一ファイルと称さない。編集対象はruntime/deck/のReact/TSX、scene/timeline、CSSとSVG。

元initから再現する場合は、workspace内の新しい私有copyを指定する。

```powershell
python source/build.py --case . --workspace .build/bread-talk --upstream source/upstream
```

helperは絶対pathを確認して未変更原本と別のcopyへ元initを実行し、内容auditと局所deckを置いて元buildを行う。完成物はdist/へ出る。第三者Kernel Panic素材を入れない。

原典[MIT](LICENSE)、公式字体OFL、GSAPの個別Standard Licenseを[SOURCE](SOURCE.json)で区別する。QR URL未指定でQRなし。実証値なし。確認は元buildと主要初回表示・一段移動のみで、原典verifyの全段階比較は未実施。

完成Webと代表2PNGは[制作一式ZIP](../../downloads/beatdeck-example-ja.zip)で配布する。この相対リンクはサイト配置用。
