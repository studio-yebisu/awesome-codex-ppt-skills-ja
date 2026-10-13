# chuspeeism/dashi-ppt-skillの日本語制作

原典: https://github.com/chuspeeism/dashi-ppt-skill/tree/21dc7e5fc8c3a0d7f6a94948153dd1ee954f4e64

原典のgoal-scaffold --layout-variants 1・inspect-layout・props-safe・validate-goal-spec・React/tsx render-goalを実行。theme05の4種類の実テンプレートで6ページを制作。標準3+1経路の検証不整合を記録し、原典が備える1案経路を採用。 日本語派生theme05では入力値から図形寸法を計算する修正を適用。原典とvalidatorは保全。

原典の1案経路でJSON→React/tsx→HTMLを実行する。theme05の日本語派生ではcopy値を図形寸法計算へ反映する。3+1経路のcopy検証不整合を記録し、検査を弱めて回避しない。PPTXエンジンは専有条件を持ち、別製品へ抽出しない。

## 作例

- EC月次報告：売上と粗利を確かめる / 6枚 / html
- カタログ内の案内: repository.html?repo=chuspeeism/dashi-ppt-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=chuspeeism/dashi-ppt-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Node.js 20以降（実行時24.18.0）とnpm
- 原典projectでnpm ci --ignore-scripts
- このカタログの生成補助はPython / fontTools / Brotliと共通フォント資産を使用

## 元の制作コマンド

    npm --prefix <upstream>/skills/dashi-ppt/project ci --ignore-scripts

    python tools/build_dashi_repository_example.py

## 確認範囲

- 標準3+1モードは原典の検証不整合があり、本例は原典CLIが提供する1案経路を使用。全3+1機能の検証完了を意味しない。
- 派生theme05で入力値がグラフ寸法に反映されるよう修正。原典そのままのruntimeではない。変更差分を同梱。
- HTMLの本文とページ移動が対象。PPTX/PDF書出しは未検証。
- 原典はAGPL-3.0、内蔵PPTXエンジンは別の専有条件。エンジンを抽出・再配布していない。
- カタログ内の静的previewでは原典の保存/API書出しは利用できない。編集保存/書出しには原典preview serverを使う。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。

Dashiのexport engineはこの派生パッケージへ分離収録していません。完全な原典を固定commitで取得して、同じDashi skill内だけで使用します。AGPL対象の対応ソースとtheme05局所差分を保持。専有エンジンは変更しません。
