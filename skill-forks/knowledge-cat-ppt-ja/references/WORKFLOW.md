# gnipbao/knowledge-cat-ppt-skillの日本語制作

原典: https://github.com/gnipbao/knowledge-cat-ppt-skill/tree/889c3dc00b356607fa9af935eb807056c3394886

原典deck-plan validator→build_native_pptx.mjs(@oai/artifact-tool)→再importと原典preview/inspection→出力日本語局所化→原典text/editability/probe。

原典native-pptx laneの専用build_native_pptx.mjsと原典plan/text/editability/probeを実行する。Codexのartifact-tool作業環境を指定し、本体は複製しない。日本語action-title警告を消さず、本文の命題を実読する。出力の固定デモラベルとNoto Sans JPを局所化。

## 作例

- 迷わない議事録のまとめ方 / 5枚 / pptx
- カタログ内の案内: repository.html?repo=gnipbao/knowledge-cat-ppt-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=gnipbao/knowledge-cat-ppt-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python + python-pptx/Pillow
- Node + @oai/artifact-tool workspace
- PowerPointとNoto Sans JPは最終描画に使用

## 元の制作コマンド

    python tools/build_knowledge_cat_repository_example.py --node "node.exeのパス" --workspace "artifact-tool workspaceのパス" --render

## 確認範囲

- artifact-toolをローカルで利用できる環境が必要。
- 原典の日本語action-title警告は意味を別途読む必要がある。
- 原稿・図表を外部AIサービスが生成した実証ではない。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
