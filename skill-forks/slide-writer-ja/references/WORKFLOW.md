# FeeiCN/slide-writerの日本語制作

原典: https://github.com/FeeiCN/slide-writer/tree/3c4524c4abb3310fdee106282d0a64f156fd4ff6

原典template.htmlを複製し、Mode A1の構成・コンポーネントで日本語原稿を配置。無改変のapply-template-branding.py、inline-images.py、smoke-test.shを実行。固有MiniSlidePresentationで再生。

原典template.htmlを複製し、Mode A1の構成・密度・コンポーネントで日本語をまとめ、無改変のbranding・inline-images・smoke-testを実行する。自作しおりテーマとlogo、OFL書体の別名サブセット、意味で区切る改行、原典revealとスクロールを用いる。file://直接起動は安全ポリシーで未確認で、原典の全工程完走とは扱わない。

## 作例

- 朝会は、判断と相談の入口に / 8枚 / html
- カタログ内の案内: repository.html?repo=FeeiCN/slide-writer
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=FeeiCN/slide-writer
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13 / fontTools 4.66.1 / Brotli 1.2.0
- Git Bash（原典のsmoke-test.sh）
- 作成したHTMLを表示できるブラウザー
- 初回の公式OFL書体取得にはネット接続

## 元の制作コマンド

    python tools/build_slide_writer_repository_example.py --input examples/repositories/slide-writer/input/data.json

## 確認範囲

- 単一HTMLの日本語8枚と通常の原典ナビゲーションをlocalhostで確認。
- 直接ローカルファイル起動はブラウザーの安全ポリシーに拒否され未確認。原典の全工程完走とは扱わない。
- 原典14企業テーマは未試行。使用素材は自作logoと、個別MIT表示を保持したFeather SVG。
- 2週間は架空チームの試行期間の提案。改善効果は未測定。
- 人による採用と外部公開は未実施。再生成出力には新たな全ページ確認が必要。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
