# パンが、店先に届くまで。

原典Beatdeckのnpm run initでscaffoldした、架空パン店の概念資料。**6場面・15段階**（待機を含む）。素材から手渡すまでを共通stage worldにし、元Scene/Reveal、NodeBox+Arrow、Timeline、Typewriterで動かす。元engineは未変更。

完成物は[dist/index.html](dist/index.html)と`dist/assets/`の一式。HTML一ファイルだけでは動かない。配布ZIPを展開し、以下で開く。

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

`http://127.0.0.1:8000/#1.1`は待機、最初のクリックで本題。原典のstage click＝1beat、矢印/クリック/1〜6/O/P/Fなどの操作は[RUNBOOK](docs/RUNBOOK.md)。warm paper/ink/vermillionのbrand tokensと日本語字体を原典neutral＋lightへ重ねた。

## 編集・再生成

編集対象は`runtime/deck/`のReact/TSX、SceneDef[]とtimeline、CSS tokens、SVG。PowerPointは生成していない。原稿は[reference/SCRIPT.md](reference/SCRIPT.md)、対応は[CONTENT-AUDIT](docs/CONTENT-AUDIT.md)、ブランドは[input/BRAND.json](input/BRAND.json)。

```powershell
npm --prefix runtime ci --ignore-scripts --no-audit --no-fund
npm --prefix runtime run build
```

これはscaffold済みtalkの再build。完成一式は`runtime/dist/`へ出る。元initを再現する場合は[source/build.py](source/build.py)を、未変更原本から新しい私有pathへ実行する。

```powershell
python source/build.py --case . --workspace .build/bread-talk --upstream source/upstream
```

helperはworkspace内の絶対pathを確認し、未変更原本と別の新しいtalkに原典initを実行する。source→audit→authored deckをコピーし、原典npm run buildでtypecheck・bundle・offline checkする。`src/beatdeck/`は変更しない。出力は`dist/`へコピーする。initの私有pathと成功は[source/init-path.json](source/init-path.json)、実buildは[source/build-log.txt](source/build-log.txt)に記録。

## 出所と確認範囲

原典は[固定commit](https://github.com/borjaperfra/beatdeck/tree/329a971303bedd3eeaae7c5216317fafdf2ef6a3)、[MIT](LICENSE)、©2026 Borja Pérez Francés。`examples/kernel-panic/assets`の第三者素材はcopyにも配布にも含めない。未変更engine/scripts/themes/skill/必要templatesは`source/upstream/`、局所deck/brand/bridgeは[source/talk-local.diff](source/talk-local.diff)に保持。

依存のGSAP3.15.0はMITではなく[GSAP Standard No Charge License](https://gsap.com/community/standard-license/)が適用される。依存別の条件と元noticeは[source/dependency-licenses.json](source/dependency-licenses.json)と`source/licenses/`で区別する。公式Dela/BIZ/Manropeの実TTF/OFLは[fonts/](fonts/SOURCE.json)。原典theme由来のInter/JetBrains Mono local assetsにもOFLを保持し、OS字体を抽出しない。

原料・食品安全・時間・売上・科学値は作らず、図形と色変化は説明用。QR target未指定なのでQRなし。元APIへの小さな同一origin bridgeは全15beatを0-based indexへ対応させ、controllerを置き換えていない。

確認は原典build（typecheck/bundle/offline）、主要初回表示、元stageの一段移動、代表2PNGのみ。[SOURCE](SOURCE.json)、[PROVENANCE](PROVENANCE.json)、[QA](QA.json)を参照。原典verifyの全forward/back/direct/frame比較は、ユーザーの今回の範囲指定により実施していない。
