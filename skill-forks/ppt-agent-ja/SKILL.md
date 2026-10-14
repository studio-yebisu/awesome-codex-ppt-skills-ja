---
name: ppt-agent-ja
description: 原典Bauhaus BlockとHTML/DOM/SVG/native PowerPoint生成経路を使う日本語展示資料。
---

# 日本語PPT Agent

Akxan/ppt-agent-skill `01825dee2ad40a8c719824252605396b9a570d57` / MIT。原典の26作風から実在するstyle/mockを読み、そのCSSと本文を日本語へ局所対応する。

1. input/requirements.json、planning.json、style.jsonへ企画と5枚構成を保存。今回はユーザーが内部判断と軽い確認を指定済み。必須interview/承認待ち、カード数の固定、追加reviewを適用しない。
2. `bauhaus_block` の三原色・巨大和文・硬い幾何・余白を保つ。本文は短い明朝、英数字はManrope。使用TTF/OFLのみを同梱し、OS字体を抽出しない。
3. 原典html_packager→html2svg(dom-to-svg/Puppeteer)→svg2pptx(native OOXML形状)を実行。WindowsfileURL/cache/字体待ちadapterはsourceの差分へ記録。原典DOM失敗時に別方式へ黙って替えない。
4. このpinのconverterはSVG文字・rect/circle/line/pathをnative形状にする。編集範囲はtext/shapesと説明し、native chart/table/数式を称しない。
5. PowerPoint16で完成PPTXのPNG/PDFを描画。Application.Quitは禁止、自deckだけClose。確認は生成成功と代表完成物初回表示まで。
6. .pptx本体、Web preview、HTML/SVG、入力/依頼/原稿、原典/差分/license/font/短いQAを渡す。backendや重いcacheをZIPへ入れない。全ページ詳細目視・独立review・構造監査・ZIP再実行を追加しない。

## quick_validate

`python source/build.py --node C:/path/to/node.exe --chrome C:/path/to/chrome.exe` の成功後、完成PPTXをPowerPointで代表1ページ表示。日本語欠けや明白な生成欠損があれば局所修正する。
