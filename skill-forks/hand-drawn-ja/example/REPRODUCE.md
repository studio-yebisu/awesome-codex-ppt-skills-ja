# 作例の再実行

作例単体ZIPのroot、または一式ZIPのexample/で実行します。

1. 用意済みNode.js24、PptxGenJS4.0.1、sharp0.35.5とPython3を参照できる環境を使います。`package.json`は依存の宣言です。今回、fresh npm install/npm ciは実行していません。
2. `node build.cjs` でPPTXを作ります。`HANDDRAWN_PYTHON`に既存Pythonの実行ファイルを指定できます。Georgiaに日本語文字がないため、小adapterが日本語のa:eaだけYu Minchoにします。Calibri/Yu Minchoは受取側の既存書体を参照します。
3. `python source/reproduce.py --render --node <node> --soffice <soffice> --pdftoppm <pdftoppm>` で原典Step6のLO PDF→全頁JPEG150dpiを実行します。参照先の外部soffice.pyは同梱されていないため、既存LibreOffice CLIを直接呼びます。
4. 追加のWindows PowerPoint PDF、pypdfium2の全頁PNG、別コピーのnative章題編集も同コマンドに含みます。PowerPointのQuitは呼びません。書体・アプリを持たない環境ではこの追加検査は実行できません。
5. 新しい全頁画像を自分で読み、切れ・重なり・図の位置・配色・番号を確認します。既存のQAや独立評価は再生成した別入力へ引き継ぎません。

原典SVG4点はsource/check_recipe.pyで原文と比較します。表紙の小sparkleだけは原典が許可するBezierの新規図形です。PNG挿絵の線は個別編集できません。章題の変更はPowerPointで行うかinput/data.jsonを修正して再生成してください。
