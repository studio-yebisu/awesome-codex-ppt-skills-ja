# prodigeproject/pradaslidesの日本語制作

原典: https://github.com/prodigeproject/pradaslides/tree/b9219b238d812d0dd7b4ed9fb514effbad0d0928

原典計画契約とlint → native PPTX → PowerPoint実描画 → 原典render-parity presenter

原典のbootstrap、brief・出典・設計・レイアウト等の契約validatorとstrict plan lintを使い、native PPTXを作る。原典はauthoring engineを固定しないため、この作例では専用python-pptxソースを使用する。PowerPoint実描画から無改変の原典build_pptx_preview.pyでrender-parity presenterを作り、原典由来HTTP QAを実行する。ブラウザー表示の本文は画像、編集正本はPPTX。OS游ゴシックは配布せず、MITの原文を保持する。

## 作例

- 町内会の備品貸出を、迷わない手順に / 6枚 / pptx
- カタログ内の案内: repository.html?repo=prodigeproject/pradaslides
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=prodigeproject/pradaslides
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Windows / Microsoft PowerPoint / PowerShell 7
- Python 3.10+ / python-pptx 1.0.2
- Node.js 22+ / ChromeまたはEdge
- Yu Gothic（OSフォント）

## 元の制作コマンド

    python source/reproduce.py

    python source/qa.py

## 確認範囲

- 架空の手順案。実在の貸出ルールではない。
- HTMLのスライド部分は描画画像。PPTX内の文字と図形は編集可能。
- HTML QAは原典の検査を保持したHTTP入口の派生。file URLは未実行。
- 再出力は新しい確認前状態になる。人の正式採用は未承認。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
