# johnson7788/MultiAgentPPTの日本語制作

原典: https://github.com/johnson7788/MultiAgentPPT/tree/ce8185cee83092290bdb913a528c6e3a72ee879e

原典start_generate_presentation(dict)と同梱PPTX templateのlocal export。LLM/研究agent/画像API/通常Web frontendは未実行。

原典のstart_generate_presentationと同梱templateのAPI不要exportを実行する。実関数はdict入力を要求し、本文処理はsectionのindex1/2に限定。通常のmulti-agent、LLM、画像API経路の成功を示さない。shape IDの設定補正、Noto Sans JP・講稿・固定ラベルの局所化を記録する。

## 作例

- 青葉デザイン はじめの一週間 / 4枚 / pptx
- カタログ内の案内: repository.html?repo=johnson7788/MultiAgentPPT
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=johnson7788/MultiAgentPPT
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python + python-pptx/Pillow/requests
- Noto Sans JP
- 描画検証にはWindows版PowerPoint

## 元の制作コマンド

    python tools/build_multiagent_repository_example.py

    python tools/build_multiagent_repository_example.py --render

## 確認範囲

- API不要のexport関数のみ実行。multi-agent生成/画像APIの証明ではない。
- 原典の処理対象sectionに制約があり、任意枚数を保証しない。
- 同梱templateへのshape ID対応はrunnerで補正。原典は非メンテナンス。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
