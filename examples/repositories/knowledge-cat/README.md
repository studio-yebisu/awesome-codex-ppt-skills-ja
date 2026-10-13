# Knowledge Cat：迷わない議事録のまとめ方

原典のnative-pptx laneと専用 `scripts/build_native_pptx.mjs` で、架空の青葉企画向けに日本語5枚を制作。計画JSONを原典validatorで確認し、@oai/artifact-toolでnative text/shape/table/notesへ出力した。原典ビルダーは出力PPTXを再importしてpreviewとinspectionも作る。

固定原典: gnipbao/knowledge-cat-ppt-skill / 889c3dc00b356607fa9af935eb807056c3394886。MIT Copyright 2026 Knowledge Cat contributors。原文LICENSEを保持。ランタイム依存@oai/artifact-tool本体はこのキットへ複製せず、利用環境で用意する。

## 再制作

Python + python-pptx/Pillow、Node、@oai/artifact-toolを解決できるworkspaceが必要。今回の利用環境はenvironment.json。外部API・キー・画像サービスは不要。PowerPointを使う場合はNoto Sans JPも導入する。

キット内の配置は `tools/build_knowledge_cat_repository_example.py` と `examples/repositories/knowledge-cat/input/data.json`、同case内の `source/upstream/`（原典scripts、references、assets、LICENSE）。カタログの固定原典が存在しない場合は同梱source/upstreamを使う。

```text
python tools/build_knowledge_cat_repository_example.py --node <node.exe> --workspace <artifact-workspace>
```

上記だけならPPTXと原典preview・検査結果を生成し、QAはgenerated_awaiting_reviewとなる。input/data.jsonの各頁を自分の内容へ変更する。原稿は人名・日程とも架空の教材で、実在組織の規則ではない。

Windows版PowerPointとtools/render_powerpoint.ps1がある環境では `--render` を追加し、完成PPTXを描画する。全頁を目視した後だけ `--finalize-only --reviewed` で記録を確定する。既存のPNGを新しい原稿の確認証拠として流用しない。

固有の表紙・statement・table・process・closingを使い、原典ビルダー自体は無変更。表紙の固定技術デモ文と出力書体だけ日本語教材に合わせて補正した。変更範囲はsource/local-changes.json。原典plan validatorの日本語action-title警告は抑制せず保持し、内容を実読して確認した。

## 検証

原典extract_pptx_textでplaceholder検査、check_pptx_editabilityで5枚・native table・notes・image-only排除を確認。probe_pptx_editabilityは一時ファイルの文字を編集して再読込し、原本不変を確認する。構造検査は目視品質の保証ではない。PowerPoint UIでの手編集試験はしていない。

原典previewは日本語局所化前の出力、render/は局所化後のPowerPoint描画。両者の役割を分けて保持している。PPTX・原稿・講稿・原典・実行ログを同梱し、元のMIT表示を保持する。
