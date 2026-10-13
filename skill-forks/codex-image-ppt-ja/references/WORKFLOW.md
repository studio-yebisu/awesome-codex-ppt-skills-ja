# ningzimu/codex-ppt-skillの日本語制作

原典: https://github.com/ningzimu/codex-ppt-skill/tree/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c

原典prepare_slide_prompts/dispatch/result/state CLIを使用し、Codex native image_gen.imagegenで全3ページを生成。原典assemble_ppt.pyが画像とspeech.mdからPPTXを構築。

原典spec/style/jobs/stateを経てCodex native image_genで各ページを実生成し、原典assemble_ppt.pyで組む。画像を個別編集可能なPPTXと呼ばない。toolが公開していないモデル名を推測しない。sample採用は制作エージェントの判断と記録し、人の承認と偽らない。

## 作例

- Gitの保存・記録・共有 / 3枚 / pptx
- カタログ内の案内: repository.html?repo=ningzimu/codex-ppt-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=ningzimu/codex-ppt-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Codex native image_gen.imagegen
- Python / python-pptx / Pillow / filelock
- PowerPointとPowerShell 7（実描画QA）

## 元の制作コマンド

    python tools/build_codex_image_repository_example.py assemble

## 確認範囲

- 本文と図はraster_slidesで個別編集不可
- 実モデル名はtool非公開
- sampleは制作agent判断で人の承認ではない
- 3頁を同一担当者が制作した運用差分を記録

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
