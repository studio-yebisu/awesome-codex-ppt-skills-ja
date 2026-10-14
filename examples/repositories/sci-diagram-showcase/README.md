# 雨が、地下水になるまで。

USGSの一次解説に基づく、日本語5ページの科学概念図。縮尺・定量値・実験結果は示しません。

## 原典方式

HututuWorks/sci-diagram-pptxの公式`assets/pptxgenjs-build-template.mjs`を直接使ったPptxGenJS4.0.1経路です。原典のsource-to-slide座標変換、NODES/EDGES/INSETS、native所有、map検証、connectExactPath/connectOneWay/connectBothWaysを保持しています。意味を持つ断面、砂粒、注釈、矢印は全てnativeで編集可能です。

ユーザー指定の新作に合わせ、単一画像の忠実再構成から新規概念図5枚へ拡張。地表の模式形状は標準長方形と河道の切り欠きで表現し、地形の実測を意味しません。科学的関係と矢印の方向はinput.jsonに明示しています。地層のnative plateを先に描き、線・矢印、文字の順に重ねます。

## 再制作

Node.js20+を用意。ZIP展開先で実行します。PptxGenJSはMIT、4.0.1をpackage-lock.jsonに固定。ホスト専用・専有runtimeは不要です。

```powershell
cd source
npm ci --ignore-scripts --no-audit --no-fund
node build.mjs
# 既存の生成物を意図的に置き換える場合だけ
node build.mjs --overwrite
```

実際の入力はsource/input.json、実行コードはsource/build.mjs。出力はsource/deck.pptx。rootのdeck.pptxは完成例、render/は公開プレビューです。Windows Microsoft PowerPointで描画する場合:

```powershell
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath source/deck.pptx -OutputDirectory render-new
```

原典のportable rendererを使う場合はPython3.10+、LibreOffice/soffice、pdftoppmを用意し、upstream/scripts/render_pptx.pyへ`--soffice`で実exeを渡します。LibreOffice付属の古いPythonがPATHで先にならないよう注意します。

## 書体と条件

fonts/のZen Kaku Gothic NewとSpace GroteskをTTFからインストールし、PowerPointを開き直します。前者は和文、後者は英数字。受け手にも導入してください。Google Fonts公式未改変TTFとOFLを同梱。WindowsFontsからの抽出はありません。PPTXに書体自体は埋め込んでいません。

原典Apache-2.0のLICENSEと、PptxGenJSの原文MIT条件をdependencies/pptxgenjs/LICENSEに保持。原典取得物にNOTICEはありません。原作者の公式日本語版ではありません。専有runtimeのコード・条件ファイルは配布版に含めません。

## 出典・確認

- https://water.usgs.gov/ogw/unsaturated.html
- https://water.usgs.gov/outreach/Posters/groundwater/middle_school/Page2.html

図は新規制作し、USGS画像のコピーは含みません。公開portable版は生成後のPowerPoint描画1回と主ページ確認のみ。全ページ詳細目視、構造監査、独立レビュー、ZIP再実行は未実施。古いホスト専用試用物とQAは内部履歴に退避済みで、現行版の確認結果には数えません。
