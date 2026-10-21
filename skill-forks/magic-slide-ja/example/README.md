# 同じ数字や持ち物を次頁へ引き継ぎ、前夜と朝の役割の変化を追える。

入力：朝の支度40分→30分を仮定する実験案、5頁のoutlineとBrief Lite。
出力：元のMagic Move・Overview・講稿を持つHTML。

この日本語作例は原典の固定ソースを使った紹介用の試作です。修復後の全5頁をCodexが実描画で確認しました。独立したKimi K3 / Opus5.5の再採点と人の採用判断は別です。

## 使い方

1. sources/outline.mdで結論・読み手・終わり方を決める
2. sources/brief.mdで題材・書体・配色と採らない表現を決める
3. 数字と持ち物に同じmagic-idを付け、各頁の意味に沿って置く
4. 原典mergeと認証scopeのみ派生したinjectorで生成する
5. 原典serveでOverview→通常再生→全境界の動きを確認する

## 生成・検査

`python source/build_magic_slide_repository_example.py --generate-only --source-dir sources --upstream source/upstream --font-dir assets/fonts --output-dir <new-directory>`
`python source/ja-runtime/scripts/serve.py index.html --no-open`

脚注を15→20px、本文色へ変更。全5頁と4境界の実Magic Moveを再確認。静止画のcursor/trailだけ撮影時に除外。 実行記録と画像hashはQA.json、出所はPROVENANCE.jsonと原典LICENSEを参照してください。

## 範囲

- 40・30・4・3・3分は仮定、短縮効果は未検証
- 認証付きQA関数のscope修正のみ。server認証と保存先制限は原典のまま
- 静的カタログiframeでは編集・保存が使えない
- agentの検証と人のrevision/adoptionは別。後者はpending
- 静止画だけcursorとtrailを非表示にして撮影。通常runtimeは保持

## 遷移の実撮影

原典serveで4つの境界を再生し、各境界の前・途中・後の12枚を保存しました。[実画像の一覧](render/motion-before-mid-after.jpg)と[状態・hash](source/motion-check.json)で、10分と準備品、30分・5日間の移動を確認できます。元の時間設定を変更せず、途中フレームを合成していません。人のRevision・端末ごとの滑らかさは未確認です。
