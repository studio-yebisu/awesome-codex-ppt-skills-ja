# minorun365/minorun-marp-skillの日本語制作

原典: https://github.com/minorun365/minorun-marp-skill/tree/736fd5e9fafb80148a1e6eaa5ae5f9d859431257

原典のslide-story・slide-figures・slide-design-darkを適用。黒地テーマ本体を保持し、作業・ステージ・記録・共有の図を段階的に開示するMarp原稿を制作。Marp CLIで実HTMLを生成。

元の日本語3スキル（story・figures・dark design）を読み、問いと段階的な図解を作る。原典minorun-darkテーマでMarp CLIを実行し、check-ai-smellも実行する。

## 作例

- Gitの変更、どこに保存された？ / 9枚 / html
- カタログ内の案内: repository.html?repo=minorun365/minorun-marp-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=minorun365/minorun-marp-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Node.js 24.18
- Marp CLI 4.4.0
- 元スキルを読めるエージェント
- PDF書出しにはChrome系ブラウザと原典の検査ツール

## 元の制作コマンド

    npx @marp-team/marp-cli@4.4.0 --no-stdin deck.md --html --theme minorun-dark.css --allow-local-files -o index.html

    python tools/check-ai-smell.py deck.md

## 確認範囲

- 原著自体が日本語。今回の派生は再制作用の入力・図と公式OFL由来のNoto Sans JPを添付。Marp原稿からのHTML再生を検証。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
