# joeseesun/qiaomu-bento-pptの日本語制作

原典: https://github.com/joeseesun/qiaomu-bento-ppt/tree/55c63c836f42bc9175757d077428c395cd93effe

原典の固定Bento shell・文書スキーマを使用。bento_deck.pyでJSONを検証し、シェルを変えずに編集版と再生版の.bento.htmlを構築。検索の同一要素が権限確認から回答へ移るmorphを制作。

固定Bento shellを変えない。日本語本文・字体・要素IDを文書JSONへ入れ、原典bento_deck.pyで検証・buildする。編集版とreadonly再生版を作り、morphに同一IDを使う。

## 作例

- 社内検索を4週間で試す / 6枚 / html
- カタログ内の案内: repository.html?repo=joeseesun/qiaomu-bento-ppt
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=joeseesun/qiaomu-bento-ppt
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13
- スキルに同梱されたBento shell v1.0.10
- ブラウザ

## 元の制作コマンド

    python scripts/bento_deck.py locate

    python scripts/bento_deck.py build deck.json --output deck.bento.html --new-document --report validation.json

## 確認範囲

- 編集版と再生版を別ファイルで同梱。既存文書を再構築するときは--identity-sourceでdocIdを保持する。ネット上の最新版へ差し替えない。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
