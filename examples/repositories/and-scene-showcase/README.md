# 一冊の本が、次の人へ。

架空の交換本棚を提案する8段階。資料の「8枚」ではなく、ひとつの共通canvasを進める8 Step。人名・住所・料金・営業実績は設定していない。

主出力はdist/index.html＋assets＋fontsのWebフォルダー一式。単独HTMLではないため、主downloadはand-scene-example-ja.zip。本文・caption・Step payloadはapp/src/presentations/book-exchange/、図はScene.tsxの自作SVG、色・字体はstyle.cssから編集する。PPTX/PDFは原典の対象外で生成しない。

## 開く / 再生成

制作ZIPを展開して、そのルートで `python -m http.server 8000 --bind 127.0.0.1 --directory dist`、ブラウザで `http://127.0.0.1:8000/index.html` を開く。HTTPでdistを一緒に配信する。次へは元nextボタン、→/Space/PageDown、前へは←/PageUp。Pで元browse/present切替。

Node.js/npmを公式配布から用意する。今回Node24.18.0、npm11.16.0。app/で:

```powershell
npm ci
npm run build
npm run preview -- --host 127.0.0.1
```

原典package.jsonのbuildは `tsc -b && vite build`。全runtime/dev依存をinstallし、実build成功。実解決versionはpackage-lock.json、logはoutput/npm-install.log / npm-build.log。compiler/node_modulesは配布しない。

repository内の準備入口は `python tools/build_and_scene_showcase.py --prepare`。source/build.pyは同じ準備入口の保存原本で、repo構造とacquired原典・fonts receiptを使用する。独立制作ZIPではapp/から上のnpm ci/buildを使う。原典runtimeのコピーを共通rendererに取り換えない。

## 原典・差分・確認範囲

原典固定commitの未変更bootstrap/Step/skillとkit原本はsource/upstream、kit SHA256はsource/UPSTREAM-KIT-SHA256.json。unused demo画像は同梱しない。core Presentation/Stage/typesを保持し、usePresentationNavの元setStepへsame-origin0-based adapterだけを加えた。source/local.diffに差分を保存。新しい8 Stepは同じScene/groupKeyとstable namespaceを共有する。1→2では同じbook DOMを保持した移動を確認。

Rootの入口は静的配布のindex.htmlから元PresentationRouterをregistered book-exchangeへ接続する局所host差分。navigation/controllerは元kit。diagram canvas880×380、代表viewport1600×900。元TOC/progress/attributionは保持し、見た目はpresentation-local CSS。

実npm install/build、主要初回表示、元nextによる1→2、代表2PNG、短SKILL quick_validateだけ。全段階詳細・last/dense/mobile・fullverify/inspect・独立レビュー・ZIP再実行は最新指示で実施していない。最初のexportでfavicon404が出たため、自作SVGfaviconを追加して解消した。

条件はLICENSE、source/DEPENDENCIES.md / licenses / DEPENDENCY-LICENSES.json、fonts各OFLを保持。未改変font source URL/hashはdist/fonts/SOURCE.json。
