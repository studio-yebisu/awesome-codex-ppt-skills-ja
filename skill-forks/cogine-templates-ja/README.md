# Cogine AIテンプレート・日本語キット

[SKILL.md](SKILL.md)から始める。原典の選択folderとmetadata、対応入力、再生成コード、局所CSS、茶葉/包み/結びのSVG、未改変実TTF/OFLを収録する。[SOURCE](SOURCE.json)と[MIT原文](LICENSE)を保持する。

```powershell
python source/build.py --case . --upstream source/upstream
python -m http.server 8000 --bind 127.0.0.1
```

ブラウザで`http://127.0.0.1:8000/template.html`を開く。Nodeやnpmは主制作に不要。`input/content.json`を編集すると、選択templateをコピーしてdemoを差し替える。完成HTMLでは文字・SVG・CSSを編集できる。PPTX/PDFは生成していない。

原典の字体保持規則への変更は、今回の日本語派生・字体変更に対するユーザー承認に基づく。原典版式・palette・装飾・元navigationを保持し、字体をShippori/Zen Kaku/Manropeへ役割別に変える。原典JSONにlayout_slotsはなく、実DOMに基づく局所mappingを保存している。

完成HTMLと代表2PNGはこのキットにも同梱する。実行記録を含む[制作一式ZIP](../../downloads/cogine-templates-example-ja.zip)も別配布する。この相対リンクはサイト配置用。キットの未変更原典は`source/upstream/`、字体出所は[fonts/SOURCE.json](fonts/SOURCE.json)。
