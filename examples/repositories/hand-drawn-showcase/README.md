# チームのアイデアを、育てる。

表紙＋「見つける／話してみる／試してみる／振り返る」の5枚。架空のワークショップ用の**章扉サンプル**です。フル業務資料ではありません。

原典 ABYR1206/claude-skill-hand-drawn-slides の SKILL にあるPptxGenJS＋sharp雛形と原SVGを直接適用。13.333×7.5、オフ白の図形、太い黒線、右側イラスト、左下章題、右下ページを保持。原demoも参照として同梱。日本語書体と朱赤の手描き枠は今回の指定による変更です。

再生成: `npm install` → `npm run build`。依存はPptxGenJS（MIT）とsharp（Apache-2.0、libvips等の個別条件を含む）。原典MIT・利用SVGの帰属はLICENSE/upstream、依存の原文条件はdependency-licenses/を参照。依存バイナリやnode_modulesはZIPに含めません。

PPTXの文字は編集可能、手描き図形は原典方式のSVG→PNG。書体は埋込みません。指定書体で編集・表示するには fonts/ の原TTFを手動導入してください。SIL OFL同梱。

閲覧素材はPowerPointから書き出したPNG/PDF。生成と主画面の初回確認のみ実施し、全ページ詳細検査・構造監査・ZIP再実行は行いません。
