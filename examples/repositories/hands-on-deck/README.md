# hands-on-deck 日本語実行例

既存の日本語PPTXを、原典の原子的JSON patchで編集する5枚の作例です。原典が新規デザインを生成したと主張するものではなく、当プロジェクトで作った編集元を使い、79箇所の本文とノート・書式・プロパティを94操作で変更しました。

原典: [EveryInc/hands-on-deck](https://github.com/EveryInc/hands-on-deck/tree/a24b996ecff6393ccf39c4fee2b88c493fb0b693)（MIT）。改変していないdeck.pyのinspect、apply、fix、diff、renderを実行。PowerPoint本体でも全ページを描画し、独立エージェント2組が5枚を確認しました。fixの表外注記の整列advisoryは、視覚上の問題がないため保持しています。

[完成PPTX](deck.pptx) / [全ページ](index.html) / [再実行](REPRODUCE.md) / [入力](input/data.json) / [原典patch](input/patch.json) / [出所](PROVENANCE.json) / [QA](QA.json)

用途は、既存の承認済み書式を保った日本語資料の更新です。別テンプレートで試すときは原典inspectで図形を確かめてからpatchを作成します。架空の運用案であり、公開・利用者テスト・人による採用は未実施です。ドナーとアイコンの著作権表示はinputに同梱しています。
