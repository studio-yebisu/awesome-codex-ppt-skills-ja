# 紙と、インクの休日。

架空の活版印刷ワークショップ企画を説明する日本語6枚。[index.html](index.html)は字体・CSS・JSとMIT/OFL原文を内包し、ネット接続なしで取得・表示できます。編集対象はHTML/SVG/CSS/JS、PPTXは生成していません。

原典は shawnzam/keynot、commit `d1f9e449ddb89da707b489cb69c520a64975b47c`。MIT ©2026 Shawn Zamechek。[未変更原本](source/upstream/)と[LICENSE](LICENSE)を保持しました。[独自BRAND](input/BRAND.md)から、原典Step1の色・書体・使用比率・版式・wordmarkを[brand-record](input/brand-record.json)へ先に抽出し、[architecture](input/ARCHITECTURE.md)で6頁の役割を決めています。

原典exampleのCSS全文、deck/slide/nav/rotate-overlay/print構造と完全inline controllerを実使用。元JSは一字も置換せず、算術・hash/session・dots・auto-hide・swipe・fullscreenを維持して末尾に同一origin bridgeを追加しました。[controller.patch](source/controller.patch)にその小差分だけを記録。日本語ラベルは[chrome.patch](source/chrome.patch)、ブランド・和文サイズ・図と版式の調整は[local CSS差分](source/brand-and-layout.patch)に分けています。

使い方は→/↓/Spaceで次、←/↑で前、Fまたは全画面ボタンでfullscreen。dotsで移動、50pxを超えるswipeで送り、navは1.8秒で隠れて操作時に戻ります。`#slide-1`等のhashは1-based、内部のcurと親bridgeは0-basedです。選択頁は元のkeynot-slide session keyへ保存します。狭い縦画面では原典の横向き案内を日本語で表示します。

再生成は `python source/rebuild.py`。Python3標準ライブラリのみで、原典部品と[slides.html](source/slides.html)、[adaptation.css](source/adaptation.css)、抽出brand-recordを単一HTMLへ梱包します。原典にnpmや外部APIの必須buildはありません。汎用renderer・評価SDKを使っていません。単独MDや一式ZIPから使う導線は日本語SKILLに記載しています。

公式Google Fonts固定pin `66928797f271fed5ee428544e7229685e2d90127`のShippori Mincho Regular、BIZ UDPGothic Regular/Bold、Space Grotesk variableを未改変で同梱し、元CDN字体をinline @font-faceへ置換。[TTF/OFL](source/fonts/)と[URL/hash](source/FONT-SOURCE.json)を保持、OS字体は抽出していません。色の70/28/2比率は設計目標で、測定ではありません。

図は自作SVGの説明記号で、実物・製品仕様・印刷結果の写真ではありません。日時・会場・費用・参加人数は未定。実施実績・安全性能を実証したとする主張はありません。

確認はHTML梱包成功、Chrome1600×1000で表紙とsplit-panelの初回表示、元navigation1/6→2/6、page errorなし。表紙の「休日」が折れていたため表紙だけclamp/nowrapを調整し、そのPNGを表示し直しました。全頁詳細検査・独立採点・ZIP再実行は未実施。fullscreen/swipe/printの元コードは保持していますが各操作の別検査はしていません。親サイトbridge統合も未確認です。[QA](QA.json)はこの範囲です。
