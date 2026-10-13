# ryanbbrown/revealjs-skillの日本語制作

原典: https://github.com/ryanbbrown/revealjs-skill/tree/d0ccd344c4aaf9f045e5a15be6a2ab67b595796f

原典create-presentation.jsで6ページの骨格とbase-styles.cssを生成。原典のpt単位・2カラム・section構造に日本語本文を組み、reveal.jsの公式ナビゲーションで再生。

原典create-presentation.jsで骨格を作る。元スキルのpt単位とsection構造を守り、reveal.jsの実ナビゲーションを使う。

## 作例

- 社内検索を4週間で試す / 6枚 / html
- カタログ内の案内: repository.html?repo=ryanbbrown/revealjs-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=ryanbbrown/revealjs-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Node.js 24.18（今回使用）
- reveal.js 5.2.1（公式MIT版を同梱）
- スキルを読んでHTML/CSSを書けるエージェント

## 元の制作コマンド

    node skills/revealjs/scripts/create-presentation.js --structure 1,1,1,1,1,1 --title "社内検索を4週間で試す" --output my-deck.html

## 確認範囲

- 今回確認したのは横6ページの再生・表・日本語書体・ノート。チャートプラグインは使っていません。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
