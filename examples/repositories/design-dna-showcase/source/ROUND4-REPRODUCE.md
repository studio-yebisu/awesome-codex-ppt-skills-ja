# 再生成

展開した作例フォルダーで実行します。固定原典・素材・字体・利用条件を同梱し、既存のREPRODUCE/requirementsの必要環境を使います。依存は別配布のNode/Python環境が必要です。

```text
python source/rebuild.py
node source/upstream/scripts/ppt-layout-guard.js index.html --report layout-guard-report.json
```

この入口が現在の本文・図・講稿の正本です。元の初回収集用generatorを再実行して古い作例へ戻さないでください。検査はsource/round4-original-gates.jsonを参照。配布ZIP再実行の実施有無はsource/round4-zip-replay.jsonに記録します。
