# 同じ本文をHTML・SVG・PNG・PDFへ揃え、用途に合う紙面を保てる。

入力：読書会の日程・参加条件・60分の進行・担当と講稿。
出力：TCSから生成したHTMLと同じbuildのSVG・PNG2経路・PDF。

この日本語作例は原典の固定ソースを使った紹介用の試作です。修復後の全5頁をCodexが実描画で確認しました。独立したKimi K3 / Opus5.5の再採点と人の採用判断は別です。

## 使い方

1. content_design_spec.mdで5頁の役割を決める
2. content.htmlの本文と講稿、template.cssの再利用部品を編集する
3. source/rebuild.pyで原典source gate・--all・visual gateを実行する
4. overviewから全browser PNGを確認し、HTMLプレーヤーの移動も試す

## 生成・検査

`python source/rebuild.py`

脚注を20px相当へ拡大し、透過を解除。4頁は担当ごとの横一行へ変更。原典の全形式compilerを再実行。 実行記録と画像hashはQA.json、出所はPROVENANCE.jsonと原典LICENSEを参照してください。

## 範囲

- この作例はHTML lane。Typst・PPTX・画像生成は未実施
- Windowsの相対パスと診断文字コードだけ派生補正。validatorは無改変
- 静止画像とプレーヤーの操作UIは別の証拠
- 架空の読書会の企画で、開催実績ではない
