# ningzimu/image-to-editable-ppt-skillの日本語制作

原典: https://github.com/ningzimu/image-to-editable-ppt-skill/tree/b7be494e31a0ed56ef98716891db5474606b8cdf

Original editppt CLI + page workers + built-in image editing

原典editpptのprepare→page worker→build/validate→record→finalizeで画像を再構成する。Codex内蔵image_genで分離したアイコンはbitmapとして保持し、本文・カード・単純な矢印をnative要素にする。新規案内ノートは元画像からの抽出と区別し、本文XMLと画像を保って追加する。再出力kitは保存済みmanifest・分離済み画像の再利用で、新規画像編集ではない。元画像との比較と実PowerPoint描画、編集範囲を確認する。

## 作例

- 画像から編集できるGit入門へ / 2枚 / pptx
- カタログ内の案内: repository.html?repo=ningzimu/image-to-editable-ppt-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=ningzimu/image-to-editable-ppt-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python3.10+ / 原典editppt CLI
- 新規入力には内蔵画像編集とpage worker対応エージェント
- PowerPoint（今回の表示QA）

## 元の制作コマンド

    python source/build_image_editable_repository_example.py --replay --source-dir . --output-dir ../replayed --upstream-dir source/upstream

## 確認範囲

- アイコンはbitmapで個別の線を編集できない
- OCR外部APIは未使用
- 元画像の画素を完全一致させる変換ではない

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
