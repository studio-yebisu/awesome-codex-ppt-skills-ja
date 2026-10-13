# daniel-style/magic-slideの日本語制作

原典: https://github.com/daniel-style/magic-slide/tree/e29d87cb315eb0afc939820b100d870eabf43f89

原典merge-slides / auth scopeのみ派生injector / original serve / native Magic Move

原典のoutline/Brief Lite、モジュールHTML/CSS、merge、inject、serveとMagic Moveを使う。隣接ページで数字・準備品を意味に沿って受け渡す。認証関数のscopeだけを修正した日本語派生injectorを使い、原典と差分を保持する。cursor、dock、Overview、動き、serverの認証と保存先制限を保持する。表示用iframeと、原典serverでの編集・保存を案内し、agent QAと人のrevision/adoptionを区別する。

## 作例

- 朝の支度を10分短くする企画 / 5枚 / html
- カタログ内の案内: repository.html?repo=daniel-style/magic-slide
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=daniel-style/magic-slide
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python3 / 原典serve.py
- Node（injectorのJS構文検査）
- Playwright（表示QA）

## 元の制作コマンド

    python tools/build_magic_slide_repository_example.py --output-dir morning-regenerated

## 確認範囲

- 架空の試行計画で短縮効果は未検証。
- 静的iframeは表示用。編集・保存には原典serve.pyが必要。
- Agent QA完了でも原典human revision/adoption gateはpending。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
