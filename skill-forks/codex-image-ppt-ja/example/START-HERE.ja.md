# 自分の原稿から最初の見本へ

各頁は画像1枚になる。文字・図形をPowerPoint上で個別に直したい資料には使わない。話者ノートと頁画像の差し替えは可能。

## 最初に読む

1. [構成・書式・見本](source/upstream/skills/codex-ppt/docs/outline-style-and-sample.md)：頁の見出し、3〜5要点、役割、必須画像を決める。
2. [段階の確認と進捗](source/upstream/skills/codex-ppt/docs/workflow-gates-and-progress.md)：構成→書式→生成環境→見本→全頁の順を確認する。

固定原典：[構成・書式・見本](https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/docs/outline-style-and-sample.md)、[段階の確認と進捗](https://github.com/ningzimu/codex-ppt-skill/blob/941dcafe2f23ea4ae61de99e9b22fb0ef3d9e06c/skills/codex-ppt/docs/workflow-gates-and-progress.md)。後続段階のbackend・頁分担・統合は原典SKILLのReference Mapに従って該当資料を読む。

## AIへ渡す最初の例

以下の原稿部分を自分の内容に置き換え、スキル本文と一緒に渡す。

```text
読者：会議資料を初めて共有する社内メンバー
目的：共有前に確かめる項目を伝える
原稿：ファイルの版、共有先、参照元の3点を確かめる。
まず構成案を作り、各頁の見出し・要点・役割・必要な画像を示してください。
画像1枚/頁の出力でよく、本文要素を個別編集する必要はありません。
まだ頁画像やPPTXは作らず、構成を確認する段階で止めてください。
```

最小の構成案は[input/outline-first.draft.md](input/outline-first.draft.md)。これは説明用の未実行草案で、この作例の確定構成ではない。構成を確認してから書式・生成環境を決め、代表的な内容頁を1枚だけ見本にする。見本を確認してから残りの頁を担当エージェントへ分ける。確認省略を明示された場合は委任として記録し、過去の人間承認に置き換えない。

## 保存済み作例との違い

`source/reproduce.py`は同梱のGit入門画像を再統合する入口で、自分の原稿を画像生成するコマンドではない。現在の作例は原典手順の部分実行で、初回の頁分担・個別人間承認と修復の厳密な割当順序は未実施。`slide_jobs.json`の`workflow_compliance`がその履歴を示す。
