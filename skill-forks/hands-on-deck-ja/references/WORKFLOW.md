# EveryInc/hands-on-deckの日本語制作

原典: https://github.com/EveryInc/hands-on-deck/tree/a24b996ecff6393ccf39c4fee2b88c493fb0b693

原典deck.pyのinspect・JSON patch・apply・fix・diffを実行

原典deck.pyのinspect・atomic JSON patch・apply・fix・diffで既存PPTXを編集する。自作日本語ドナーの図形構造を保って本文・文字サイズ・ノートを更新。元shape ID、入力と差分を残し、全ページを独立レビューする。fix advisoryと実際の見切れを区別し、新しい出力へ元QAを移さない。

## 作例

- イベント案内の公開前チェック / 5枚 / pptx
- カタログ内の案内: repository.html?repo=EveryInc/hands-on-deck
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=EveryInc/hands-on-deck
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.10+ / python-pptx / Pillow
- 描画: Windows / Microsoft PowerPoint
- 原典render: LibreOffice / Poppler
- Yu Gothic / Yu Mincho / Times New Roman

## 元の制作コマンド

    python source/reproduce.py --input input/data.json --render

## 確認範囲

- エージェントのレビュー済み。人による採用は未承認。
- 架空の運用案であり実際の公開・確認・利用者テストは未実施。
- 新しい本文で再実行した場合は全ページの再レビューが必要。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
