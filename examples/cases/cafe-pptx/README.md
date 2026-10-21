# SVGの本文と図を編集可能PPTXへ変換する

文章で並んでいた店舗の関係・リスク・工程を、文字や数値を直せる図と表へ組み替える8頁の例。

- 5頁：既存店→新店の仕込み支援と、両店につながる購買・品質・日報。
- 6頁：3つのリスクを、それぞれの確認方法と投資判断へ出す材料につなぐ。
- 7頁：1〜2週、3〜4週、5週を週末の目盛りに対応させ、延期条件も残す。
- 8頁：今回の調査・交渉と、後に判断する契約・初期投資を分ける。

比較画像`review/slide-05-svg-native.png`〜`07`は、左が入力SVGのChromium描画、右が実PPTXのPowerPoint/PDF描画。左右の入力とhashは`review/svg-native-sources.json`。完成後の雰囲気だけでなく、変換で文字・関係・条件が残るかを見る。

実生成はhugohe3/ppt-master @ ca04346de145ed6462ddf34682848e71df5e20a2のQuick技術契約を使う日本語専用器。原典のguard・P05 early・全8頁final・Gantt座標calculator2回・native変換を実行した。元の全Quick/Default工程を実行したとは扱わない。

原典コードは不変。日本語のBIZ字体登録と、PowerPoint実測からの文字枠幅の補正だけを局所adapterとして開示する。補正前後8頁RGBは同一。最終141文字枠overflow0。native図形183（文字141を含む）、画像0、Office Chart/Tableは0。SVGの文字は全てnative出力に残る。

入力は架空の組織・数値・計画。調査、契約・投資の承認、実績を主張しない。今回の修復はCodex、追加モデル生成なし。全8頁を制作側が実画像で確認した。独立の現版評価と採用は未完了。

原典Quick手順は`source/upstream/workflows/profiles/quick-generate.md`、一般案内は`SKILL.md`、再生成は`REPRODUCE.md`、現検査は`QA.json`と`PROVENANCE.json`。元MIT/著作権・スポンサー文書、BIZのOFLを保持する。
