# 既存PPTXの文字と図形を保ち、ブラウザーで順に再生できる資料へ変えられる。

入力：Akxan方式で制作した自作5頁PPTXの保存コピー。
出力：元extract結果とネイティブ図形を補助変換したHTML/SVG。

この日本語作例は原典の固定ソースを使った紹介用の試作です。修復後の全5頁をCodexが実描画で確認しました。独立したKimi K3 / Opus5.5の再採点と人の採用判断は別です。

## 使い方

1. 入力PPTXを保存し、原典extract-pptx.pyで文字・画像・notesを抽出する
2. 図形が意味を持つ入力はOOXMLのgeometryと色を別に記録する
3. 元Neon controllerへ固定viewBoxのSVGを載せる
4. 必要な出力だけの配置変更をadapterへ記録する
5. 元PPTXの全頁描画と変換後を比べ、頁移動・ラベル・番号を確認する

## 生成・検査

`python rebuild.py --case-only`
`python source/check_label_alignment.py`

2頁の「場所・作品・言葉」を図形中央へ合わせ、3頁と合わせ15ラベルを検査。二重のHTML頁番号を非表示にし、元PPTXの番号を一つ残す。 実行記録と画像hashはQA.json、出所はPROVENANCE.jsonと原典LICENSEを参照してください。

## 範囲

- ネイティブ図形のSVG化と中央揃えは作例の補助実装で、原典extractor単体の機能ではない
- 入力PPTXは無改変。変換後2・3頁の15ラベルだけx/anchorを変更
- この入力に画像と講稿はなく、それらの抽出を実証した例ではない
- HTML/SVG編集用。新しい編集可能PPTXは出力しない
- AWS/原作者との公認・提携ではない

## 実行環境

Python 3 + python-pptx/lxml。元extractor、保存した入力PPTX、TTF/OFL、出力限定adapterを同梱。python rebuild.py --case-onlyは入力を入れ替えず再生成する。

配布ZIPの展開後再実行はsource/zip-replay.jsonに記録。依存の導入・ブラウザーの実行パスは受け手の環境へ合わせる。
