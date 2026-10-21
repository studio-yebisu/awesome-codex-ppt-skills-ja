# 投稿案を「困りごと→記入例→行動」の順に整理し、制作ブリーフと確認画面にできる。

入力：架空ブランドの色・書体と引き継ぎメモの原稿。
出力：6枚の制作ブリーフと1080角のHTML構成確認プレビュー。

この日本語作例は原典の固定ソースを使った紹介用の試作です。修復後の全6頁をCodexが実描画で確認しました。独立したKimi K3 / Opus5.5の再採点と人の採用判断は別です。

## 使い方

1. 読む人・目的・掲載先とブランド条件をinput/data.jsonへ書く
2. 先に原稿を六つの役割へ分ける
3. carousel-brief.mdに各頁の文章・図案とBrand directionを書く
4. 専用builderで1080角の構成確認HTMLを生成する
5. 移動・進捗・最後の記入型を確認し、公開用仕上げは別に判断する

## 生成・検査

`python source/build_business_carousel_repository_example.py --input input/data.json --upstream-dir source/upstream --output-dir <new-directory>`

下端へ操作欄の余白を確保。図案と本文の寸法を調整し、最後まで移動・進捗が見えるよう修正。Brand directionと未設定の連絡先を明記。 実行記録と画像hashはQA.json、出所はPROVENANCE.jsonと原典LICENSEを参照してください。

## 範囲

- 原典は指示型の制作スキルで、原典製レンダラーは存在しない
- 本例の専用HTMLは原典の構成指示を実装したもの
- Canva/Figma仕上げ・LinkedIn PDF・公開・人の承認は未実施
- 連絡先は未設定。実績の代わりに架空の記入例を使う
