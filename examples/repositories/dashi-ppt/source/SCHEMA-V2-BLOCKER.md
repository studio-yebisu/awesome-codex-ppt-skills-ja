# 標準3+1経路の未解消問題

固定commitでPageContentPack→goal-scaffold(schemaVersion 2)→validate-goal-spec→render:goalは成功。しかしvalidate-goal-copyはtemplate candidate.propsだけを基準にし、projection.structureの配列・補助欄を具体化せず、18候補を未記入と判定した。明示contentMapを追加するとdeterministic projectionの一致検査で拒否される。検証条件を削除・無視していない。

本作例では原典に実在する--layout-variants 1の経路を採用。全6ページをcopy propsで日本語化し、原典の検証4種を通した。3+1モードを動作済みと扱わない。標準経路のgoalとエラーログはschema-v2-blocked-goal.json / schema-v2-copy-failure.txt。
