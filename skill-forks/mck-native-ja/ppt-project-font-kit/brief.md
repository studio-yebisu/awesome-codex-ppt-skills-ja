# フォント構成と制作手順 — brief

- 受け手（audience）: Studio Yebisuのフォントキットを使って資料を作る人
- 目的（goal）: 収録フォントの言語・分類の内訳と、この資料を作った順序を4ページで示す
- 時間: 4分 / 4ページ
- 主要メッセージ（key_messages）:
  1. 収録は30字体（日本語17・欧文13）
  2. 分類別の最多はゴシック系の12字体
  3. 装飾は日本語のみ、等幅は欧文のみ
  4. 制作は要件→構成→原稿→描画・検査→交付・経験記録の順。所要時間は計測していない
- データ: input/oss-font-kit.json の families[].family / language / category と presets[]（2026-10-15更新）
- 扱わないもの: 効果・所要時間・成果の数値は扱わない。データにない値を作らない。
- 書体: 原典constantsの FONT_HEADER=BIZ UDPGothic / FONT_BODY=BIZ UDPGothic / FONT_EA=BIZ UDPGothic をこの生成プロセス内でだけ指定
