# MultiAgentPPT：日本語のローカルexport作例

架空の青葉デザインの新入社員向け4枚。原典の`backend/save_ppt/ppt_generator.py`の`start_generate_presentation`と同梱templateを実行した。JSONの原稿は制作担当が準備しており、multi-agent・調査・LLM・画像APIが生成した原稿ではない。

原典: johnson7788/MultiAgentPPT、固定commit ce8185cee83092290bdb913a528c6e3a72ee879e。READMEは現版の非メンテナンスを明記する。

## 自分の内容へ置き換える

1. Python、python-pptx、Pillow、requestsを用意する。確認バージョンはenvironment.json。キー・API・Web server・DBは不要。
2. input/data.jsonのtitleとsectionsを変更する。各sectionのcontentはh1/p/bulletsのblock。実装はdictを要求するため、原典末尾のlist形式exampleをそのまま渡さない。
3. `python source/run_export.py`で同梱した原典exportを実行する。出力はsource/upstream/backend/save_ppt/output_ppts/内。題名は出力ファイル名になるためWindowsで使えない文字や改行を避ける。
4. 日本語の書体・ノート・固定ラベルの局所化を行い、PowerPointで全ページ確認する。今回の補助コードのlocalize関数が実際の変更内容。新規原稿は別途目視が必要。

原典のcontent処理は最初の3sectionに限定される。今回の4頁は表紙、3項目、本文、終了頁。4番目以降のsectionを追加しても内容が出力されるとは限らない。この作例を通常のmulti-agent全経路・任意枚数の汎用生成の実証として扱わない。

原典のshape ID指定が同梱templateと一致しなかったため、run_export.pyがconfigデータを実placeholder対応へ補正する。元コードファイルの改変なし。ネットワーク要求はrunnerで拒否し、画像URLのない入力を使う。

## カタログ内での再制作

`python tools/build_multiagent_repository_example.py --render`

上記はカタログroot、.build/actual-upstreamsの固定原典、依存導入済みPython、Windows版PowerPoint、tools/render_powerpoint.ps1に依存する。画像を全頁確認してから`--finalize-only --reviewed`で確認記録を更新する。スクリプトの--reviewedは実視認を代行しない。

初期失敗・成功ログとraw-export.pptx、変更台帳はsource/。出力の本文はnative textで編集可能。背景・装飾は原典templateの要素で、画像化したページを貼ったものではない。Noto Sans JPは受け手にも必要。

root LICENSEはMIT Copyright 2025 johnson7788。frontend LICENSEはMIT Copyright 2024 ALLWEONE Team。両原文表示を保持する。原典templateも同梱リポ由来で、別の第三者素材の権利まで保証するものではない。外部画像は取得・使用していない。
