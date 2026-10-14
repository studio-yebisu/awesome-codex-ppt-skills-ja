# slide-wright・日本語キット

[SKILL.md](SKILL.md)から始める。架空の6枚企画「星を待つ、夜の天文台。」用に、原典13ファイル、専用CSS、2枚と追加4枚のHTML原稿、実字体/OFL、再生成helperを収録する。原典は[MIT](LICENSE)、出所は[SOURCE](SOURCE.json)。

```powershell
python source/build.py --stage preview --case . --upstream source/upstream
python -m http.server 8000 --bind 127.0.0.1
```

ブラウザで`http://127.0.0.1:8000/night-observatory.html`を開く。方向を確認し、`source/stages.json`の`preview_opened`をtrueへ更新してから、別のターミナルで続ける。

```powershell
python source/build.py --stage append --case . --upstream source/upstream
```

2枚と完成版は同じHTMLで、最初の2sectionを保持して4枚追加する。主出力はHTML。HTML/SVG/CSSをソース編集する。PPTXは生成していない。PDFが必要なら完成HTMLのURLへ`?print-pdf`を付け、印刷の横向き・余白なし・背景ONで保存する。今回PDF出力は未実施。

字体・CSSはinline、エンジン5.1.0とnotes機能は固定CDNを使うためネット接続が必要。Nodeやnpmは主制作に不要。`source/render_preview.cjs`は代表PNGを出すための任意補助で、Node・Playwright・Chromeが必要。ユーザープロファイルへ接続せず新しいheadlessブラウザで同じ実HTMLの最初の2枚だけを出力する。

完成HTML・代表2PNG・初回操作記録はサイト側の[制作ZIP](../../downloads/slide-wright-example-ja.zip)で別配布。この相対リンクはサイト配置用。原典停止工程の派生変更とデザイン判断は[source/DESIGN.md](source/DESIGN.md)へ記録する。
