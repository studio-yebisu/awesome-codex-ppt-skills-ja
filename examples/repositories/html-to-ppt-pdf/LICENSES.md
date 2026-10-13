# ライセンスの範囲

| 対象 | 原典・条件 | 同梱位置 |
|---|---|---|
| HTML変換スクリプト | wangzan101/html-to-ppt-pdf / MIT / Copyright 2026 王赞 (BolynWang) | `licenses/MIT-converter.txt`, `source/upstream/LICENSE` |
| 入力Guizang HTML、派生テンプレート、書き出し互換版とその対応ソース | op7418/guizang-ppt-skill / AGPL-3.0 | `licenses/AGPL-3.0-input.txt`, `input/port-town/LICENSE`, `source/input-corresponding-source/` |
| HTMLに埋め込んだ日本語・欧文書体 | OFL-1.1。個別原文・メタデータを保持 | `licenses/fonts/`, `source/input-corresponding-source/data/{fonts,preset-fonts}.json` |
| 入力のMotion/Lucide | 各依存のライセンス通知 | `input/port-town/assets/*LICENSE*` |
| npm依存 | 各パッケージの条件。固定package-lockから取得 | `source/runtime/package-lock.json` |

変換器のMITを入力HTMLの再許諾に使いません。PNG/PDF/PPTXだけを元テンプレート・入力の出典や条件と切り離して配布せず、本ケースのライセンス通知と対応ソースを一緒に保持します。

対応ソースには現在の`tools/build_case_studies.py`、本文生成用`tools/business_web_content.py`、入力データ、CSS、書体、原典参照ファイル、Guizang派生スキルを保存しています。`python source/reproduce-input.py`で入力HTMLを再生成し、原文とのバイト一致を検証できます。変換用`export.html`の追加コードは`source/reproduce.py`の`ADAPTER`にあります。
