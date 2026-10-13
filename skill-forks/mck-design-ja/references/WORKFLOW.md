# likaku/Mck-ppt-design-skillの日本語制作

原典: https://github.com/likaku/Mck-ppt-design-skill/tree/e190e083b715b63172e1c4fea01bc5f9bb21a021

公式DeckBuilderからMckEngineのcover/two_stat/grouped_bar/data_table/action_items/closingを実行した日本語月次報告。

原典DeckBuilderとMckEngineを使う。原典の存在しないlayouts参照を前提にせず、同梱engine-apiと実コードを読む。今回のS3/S4検査はPASS、98点。自動採点をデザイン承認とは扱わない。

## 作例

- くらし便 EC事業 9月報告 / 6枚 / pptx
- カタログ内の案内: repository.html?repo=likaku/Mck-ppt-design-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=likaku/Mck-ppt-design-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13（実測）
- PowerShell 7 / pwsh（描画スクリプト）
- Noto Sans JP
- Microsoft PowerPoint 16.0（PNG/PDF描画用）

## 元の制作コマンド

    git clone https://github.com/likaku/Mck-ppt-design-skill .build/actual-upstreams/likaku__Mck-ppt-design-skill

    git -C .build/actual-upstreams/likaku__Mck-ppt-design-skill checkout e190e083b715b63172e1c4fea01bc5f9bb21a021

    python -m venv .venv

    .venv\Scripts\python -m pip install python-pptx lxml Pillow

    .venv\Scripts\python tools/build_native_repository_examples.py --only mck --render

## 確認範囲

- 上流references/layouts/は取得commitに存在しない。元engine/API参照で制作。画像生成APIは不使用。生成された固定語『负责人』を『担当』へ翻訳。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
