# PPT-Design-Skill：地域カフェの朝営業を試す

原典の Build Mode と公開 `pptx-designer==1.0.0b11` を実行した日本語5枚です。原典 initializer → brief / page plan / theme lock → ThemeComposer → strict Presentation → 公開 text / shapes / bar_chart → 保存 → 原典 inspect の順で制作。共通テンプレートへの流し込みではありません。

架空の店舗の企画案です。販売数・価格は仮定で、売上は利益ではありません。実績は未収集。編集可能な文字・図形、図形ベースの棒グラフ、講稿をPPTXに保持しています。記録表もnative text/shapeです。

## 再生成

Python 3.10+（検証は3.13）で `pip install -r source/requirements.txt`。APIキーとPowerPointは生成に不要です。原典のソースは `source/upstream`、入力は `input/data.json`、和文フォントはNoto Sans JP / Noto Serif JPです。

リポジトリから: `python tools/build_ppt_design_repository_example.py --output-dir 任意の新規フォルダ --input examples/repositories/ppt-design-skill/input/data.json`。

このフォルダ単体から: `python source/build_ppt_design_repository_example.py --upstream source/upstream --input input/data.json --output-dir ../cafe-regenerated`。

入力JSONの価格・仮定販売数・見出し・講稿を編集できます。`--output-dir` は入力と異なる場所を推奨。再生成のQAは必ずawaiting_visual_review。生成成功は表示の合格を意味しません。実PowerPointによるPNG/PDFは今回同梱。再検査は原典 `source/upstream/skill/scripts/render_pptx.ps1 -InFile <deck.pptx> -OutDir <render>` でも可能です。

## テーマと根拠

terracotta / serif-editorial / accent-bar / standard / seed42。原典のThemeComposerの全resolved themeを保存し、日本語フォントのみ明示調整。写真・AI画像・外部APIなし。元リポジトリMITとエンジンMITを同梱。元リポジトリの巨大な広告画像デモは未使用・未同梱です。

PROVENANCE.jsonに固定コミット・原典参照hash・入力/出力hash、sourceに実行ログとruntime file hash、QA.jsonに表示レビュー状態があります。今回の自律制作を人間による正式採用とは扱っていません。
