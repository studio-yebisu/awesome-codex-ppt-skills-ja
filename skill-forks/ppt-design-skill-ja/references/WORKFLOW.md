# sunchaokun/PPT-Design-Skillの日本語制作

原典: https://github.com/sunchaokun/PPT-Design-Skill/tree/cbf7ef1324a026b29e2b77b71e2034554ddd3e22

原典Build Mode / ThemeComposer / strict Presentation / published public helpers

原典Build Modeのtask初期化、ThemeComposer、strict Presentationと公開text/shapes/bar_chartを使う。日本語の色名aliasと見出しフォントを明示解決し、入力JSON・テーマlock・講稿を残す。売上試算と利益、未収集とゼロを区別する。原典と公開engineは無改変。編集可能な本文と図形をPowerPoint本体で描画して確認する。

## 作例

- 地域カフェの朝営業を試す / 5枚 / pptx
- カタログ内の案内: repository.html?repo=sunchaokun/PPT-Design-Skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=sunchaokun/PPT-Design-Skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.10+ / pptx-designer1.0.0b11
- Noto Sans JP / Noto Serif JP
- PowerPointは表示QAのみ。生成はPythonだけ。

## 元の制作コマンド

    python tools/build_ppt_design_repository_example.py --output-dir cafe-regenerated

## 確認範囲

- 架空の企画案で、実績データなし。
- ライブラリ自動デザイン生成APIは使わず、原典Build Modeで公開部品を配置。
- 再生成後は要レビュー。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
