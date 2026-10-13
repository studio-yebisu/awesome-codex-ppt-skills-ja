# EC月次報告：売上と粗利を確かめる

原典: https://github.com/chuspeeism/dashi-ppt-skill/tree/21dc7e5fc8c3a0d7f6a94948153dd1ee954f4e64

原典のgoal-scaffold --layout-variants 1・inspect-layout・props-safe・validate-goal-spec・React/tsx render-goalを実行。theme05の4種類の実テンプレートで6ページを制作。標準3+1経路の検証不整合を記録し、原典が備える1案経路を採用。

    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\source\build-ja-runtime.mjs
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\goal-scaffold.mjs --title EC月次報告：売上と粗利を確かめる --goal 架空EC事業の売上・粗利・返品を日本語で共有する --theme theme05 --pages 6 --layout-variants 1 --seed yebisu-ec-single --out M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\goal.json
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\inspect-layout.mjs --compact theme05_page001 theme05_page009 theme05_page010 theme05_page018
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\write-safe-props.mjs --goal M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\goal.json
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\validate-goal-spec.mjs M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\goal.json
    npm.cmd --prefix M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project run render:goal -- M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\goal.json M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\index.html
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\validate-swiss-deck.mjs M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\index.html
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\validate-goal-copy.mjs M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\goal.json M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\index.html
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\validate-swiss-deck.mjs M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\index.html
    node M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\dashi-ja-source\skills\dashi-ppt\project\scripts\validate-goal-copy.mjs M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\goal.json M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\dashi-ppt\index.html

入力: input/data.json。出典・実行の記録: PROVENANCE.json。確認範囲: QA.json。原典の条件: LICENSE.upstream。日本語書体: fonts/OFL.txt。

## 再現と日本語化

このカタログのルートで `python tools/build_dashi_repository_example.py` を実行します。単独のPythonファイルだけでは再現できません。原典固定commit、data/case-inputs.json、共通フォント資産とrepository_example_support.pyが必要です。原典projectで `npm ci --ignore-scripts` を済ませてください。

日本語の派生runtimeを含めて再生成する場合はこのPython生成器を使います。元runtimeだけでHTMLを生成する場合は同梱goal.jsonを使い、原典projectから `npm run render:goal -- <goal.jsonの絶対パス> <index.htmlの絶対パス>` を実行できますが、原典そのままのグラフではラベルと実際の図形寸法が一致しない問題が再発します。本文はgoal.jsonのslides[].props.copyです。001表紙、009棒グラフ、010構成比、018結論の実テンプレートを使っています。構成比のvは金額でなく百分率（20、32.5、17.5、30）です。棒グラフの1000/1200は原典のサンプル推定範囲を超える警告が2件ありますが、ハード制約ではなく値を縮小していません。

標準3+1経路はsource/SCHEMA-V2-BLOCKER.mdに記録した問題により未採用。採用した1案経路では取得原本とvalidatorは変更していません。派生コピーのtheme05モジュールでは、棒・ドーナツの寸法計算へ入力copy propsを反映し、固定項目ラベルと副系列の単位表示を修正しています。変更前後はsource/runtime-changes.json、読解用差分はsource/theme05-runtime.diff、適用手順はPython生成器に保存しています。全候補切替やPPTX/PDF書出しを動作済みとはしていません。

ブラウザの左右キーでページ移動できます。カタログ内の静的previewは閲覧用です。編集保存やPPTX/PDF書出しには原典のpreview:startサーバーとシステムブラウザを使ってください。原典のSKILL.mdに起動手順があります。

原典AGPL条件はLICENSE.upstream。PPTXエンジンはLICENSE.export-engine.txtの専有条件で、今回そのパッケージを抽出・再配布していません。HTMLのテーマ資産は原典生成物です。入力数値は全て架空です。
