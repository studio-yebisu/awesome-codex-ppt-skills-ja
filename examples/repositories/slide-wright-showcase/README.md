# 星を待つ、夜の天文台。

[完成HTML](night-observatory.html)は6枚の架空イベント提案。テーマ名はNight Orbit。日時・会場、運用の確定条件は未定で、観測データや実施成果は含まない。円/軌道は説明用の図形。

矢印キー・Space・スワイプで移動、Fで全画面、Esc/Oで一覧、Sで発表者表示、?でキー一覧。HTMLとSVG/CSSをソースで編集する。PPTXは生成していない。

字体・テーマCSS・図形はHTML内に埋め込み済み。原典のエンジン5.1.0とnotes機能は固定CDNから読み込むためネット接続が必要。オフライン完結とは称していない。テーマ色は`:root`、文字と図形は各section、noteは`aside.notes`にある。[実TTF/OFLと出所](fonts/SOURCE.json)も同梱。

## 同じファイルを育てる

原典[deck-template](source/upstream/slide-wright/references/deck-template.md)のskeletonを直接使い、1920×1080、背景section・内部frame、notes、inline CSS、既製テーマなしという構造を保持した。[build.py](source/build.py)がテンプレートから実表紙と実content2枚を`night-observatory.html`へ書く。そのファイルをブラウザで開き、2枚を保持して4枚追加する。[stages.json](source/stages.json)へ初回と追加の記録を保存。局所差分では字体の大きなbase64 payloadだけを表示用placeholderに省略し、完全な実データは完成HTMLとTTFへ保持した。

```powershell
python source/build.py --stage preview --case . --upstream source/upstream
python -m http.server 8000 --bind 127.0.0.1
```

ブラウザで`http://127.0.0.1:8000/night-observatory.html`を開く。方向を確認した後、`source/stages.json`の`preview_opened`をtrueへ更新し、続ける。

```powershell
python source/build.py --stage append --case . --upstream source/upstream
```

今回の方向はユーザーの自律判断指定と親のテーマ指定により進行承認済み。追加の承認待ちは行わず、ユーザーの美術承認済みとも称していない。[デザイン決定](source/DESIGN.md)と[制作依頼](PROMPT.md)にこの変更を記録。

[原典](source/upstream/SKILL.md)は[MIT](LICENSE)、固定commit `d95ba204c9e98488b86b76ced75765ab4ec5de96`。[局所差分](source/template-local.diff)にskeletonからの変更を保存した。元controllerへ0-based同一origin bridgeを接続し、別controllerへ置き換えていない。

保存PDFが必要ならURLへ`?print-pdf`を付け、印刷で横向き・余白なし・背景ONを選ぶ。今回PDFは生成していない。アニメーションはPDFでは静止する。

確認は原典2枚のブラウザ初回表示、代表2PNG、エンジン5.1.0稼働・0→1の移動、同じHTMLへappend後の6枚表示まで。全頁詳細目視・独立レビュー・構造監査・ZIP再実行は行っていない。代表PNGは保持した最初の2枚のもの。
