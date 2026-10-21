# 当日の操作 — パンが、店先に届くまで。

6場面・15段階（待機を含む）の架空パン店概念資料。完成フォルダーは`dist/`。index.htmlだけを抜き出さずassetsと一緒に使う。

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

`http://127.0.0.1:8000/#1.1`で待機画面。紙色と小さな題名を表示し、最初のクリックで本題へ。stageのクリック・矢印・PageDown/PageUpで一段ずつ移動、1〜6で場面へ、Home/Endで先頭/末尾、Fで全画面、Oでoverview、Pでpresenter、B/ピリオドでblackout。

原典のURLは`#場面.段階`（それぞれ1-based）。カタログbridgeだけは全15段階をflattenした0-based index。親iframeとの同一origin通信以外は受け付けない。

字体・JS・CSSはbuildのlocal assets。外部CDNやAPIは不要だが、ES moduleのためlocal HTTPで開く。接続不要という意味のoffline buildであり、HTML一ファイルではない。

未提示のQR URLは作らず、QRなしで閉じる。原料・温度・工程時間・安全・売上・科学値は含まない。演出のミリ秒はmotionの設定で、工程の実測ではない。

原典 `npm run verify -- --source=reference/SCRIPT.md` を実施する。全15段階の前進・後退・URL直接表示を比較し、contact sheetを確認する。実施済みの結果はQA.jsonとrender/verify/report.jsonに記録し、全キーの手動稽古・物理Wi-Fi断・別端末での通し確認は別の未実施項目として残す。
