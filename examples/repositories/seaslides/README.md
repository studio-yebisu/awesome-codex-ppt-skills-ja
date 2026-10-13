# SeaSlides: 読書会を月1回続けるには

原典HTML laneのeditorial-magazine / forest-inkで制作した日本語5ページです。架空の「ひだまり読書会」の企画案であり、実施結果ではありません。本文・講稿は手入力で、AI/API画像生成は使っていません。

`index.html`が原典の動くHTML。`output/`に同一buildのSVG、PNG2経路、PDF、DOM監査、差分評価、compile manifestがあります。PPTXは今回生成していません。HTML本文はcontent.htmlで編集し、再コンパイルします。

## 実行した入口

原典project_manager.py init/import-sources → validate_project.py --source-only --profile standard-project → html_compiler.py --all → validate_project.py --require-build --artifact-profile visual。原典validatorは無改変です。

Windowsでは原典compilerがmanifestにbackslashの相対パスを書き、原典validatorが拒否しました。source/logsに失敗ログを保存。source/windows-runtimeに、相対パスをas_posix()へ変えるcompilerと、任意の環境バージョン診断を文字化けで中断させないencoding補正、そのdiffがあります。検査の抑制や偽装はしていません。

## 再現

Python 3.13、Node 24で確認。Python依存はPillow、pypdf、python-pptx。HTML rendererのNode依存は原典scripts/html_to_svg/package-lock.jsonからnpm ciで導入し、同ディレクトリでnpx playwright install chromium --only-shellを実行します。今回のlockはPlaywright 1.60 / Chromium headless shell 1223です。Motion11.11.17は同梱motion.min.jsを利用できます。

配布kitの最小構造はtools/build_seaslides_repository_example.pyとexamples/repositories/seaslides/一式。原典ソースは後者のsource/upstreamに保持。元checkoutがない場合もそこを読みます。Node依存の導入先はsource/upstream/skills/seaslides-html-slides-skill/scripts/html_to_svgです。そのうえで `python tools/build_seaslides_repository_example.py` を実行します。Windowsの派生runtimeは.build/seaslides-ja-runtimeへ作り、元ソースは変更しません。再生成後は要レビューになり、既存QAの合格を引き継ぎません。

表示は `python -m http.server 8000` などのローカルHTTP経由で行います。ES moduleのためfile直開きではブラウザ制約によりアニメーションを読み込めない場合があります。

## 再生とQA

原典navは `#nav .dot[data-i]`、公開関数 `window.__go(0始まり)`、状態は `window.__currentSlideIndex`。矢印、Home/End、Escape一覧、B静止表示を原典が担当します。親の同origin yebisu-slideメッセージは最小bridgeで__goへ渡します。

5ページの原典browser PNGを個別に視認。原典source/visual gate、DOM blockers0、SVG比較pass。動く再生では全dot、Home/End、一覧切替、Motionの不透明度変化、親iframeから4枚目への移動、JS error0、外部通信0を確認。WebGLコードは保持していますが背景効果の見え方はブラウザ/GPUに依存します。

## ライセンスと素材

原典root MIT（OrangeX4）をLICENSEへ同梱。html_to_svg/package.jsonのISC表記もそのまま保存。独立した制限ファイルはありません。Noto Serif JP/Sans JPはOFLを同梱。Motion/framer-motion/motion-dom/motion-utilsは各MIT通知を同梱。原典写真・デモ画像は使っていません。
