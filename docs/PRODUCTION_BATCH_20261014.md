# 日本語スライドアトリエ：2026-10-14

最新のユーザー指示で制作方針を変更。Sol 6.1の並列制作を中心にし、Astraと大規模検査を停止した。

## 制作した新作

- 夜の図書館：Web、6ページ。frontend-slidesの固定stage、controller、原典CSSを使い、墨紺と蛍光ライム、SVG図形、段階表示、選書タブへ展開。日本語はNoto Sans/Serif JP、英数字はSpace Grotesk。
- 余白を買う：編集可能PPTX、6ページ。MckのDeckBuilderとMckEngineを使い、native core primitivesで誌面風の6版式を明示拡張。Zen Kaku Gothic New、Shippori Mincho、Space Grotesk。

両方に完成ファイル、入力、依頼文、原典commit、変更点、原文LICENSE・NOTICE、必要な書体の条件を同梱した。各生成担当がビルドと主要出力を初回表示。状態はlight_check_complete。追加の全ページ詳細目視、独立レビュー、構造監査、完全ZIP再実行はしていない。

## サイトと配布

原209件は資料として保管し、トップは24スキル・24冊135枚の厳選集へ。作風で絞り込める完成資料、フロート再生、日本語スキル本文の直接Markdown取得、一式ZIP、GitHub原典を結び付けた。

OSS書体キットは6ファミリー10ファイル。未改変の公式配布TTFとOFLを保存し、このWindowsユーザーに導入。4つの書体プリセットで見本を切り替え、AIへのデザイン指示をコピーできる。日本語スキル本文は各5KB以下で、実装は原典・ZIPから別途取得すると明記した。

親による確認は新しいトップの初回表示、Web新作のフロートとページ送り、スキル本文1件の実ダウンロード、書体プリセットの切り替えと指示コピー。過去の巨大QAを再実行しない。

方針と実行目標はdocs/PROJECT.md、docs/PRODUCT_SPEC.md、data/project-goal.jsonを正本とする。アプリのgoal APIはobjective編集に対応していないため、アプリの旧objectiveを更新済みとは扱わない。209件消化の旧方針はこの改訂で撤回している。

外部公開・push・main merge・deployはこのバッチに含まない。
