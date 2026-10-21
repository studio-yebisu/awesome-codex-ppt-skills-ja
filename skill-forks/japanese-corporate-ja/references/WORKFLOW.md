# 日本語会議資料の制作

原典はMITの指示Skillと15型PPTX。一般の制作工程は上位SKILL.md、原典全工程はupstream/skills/japanese-corporate-pptx/SKILL.mdを読む。

新規の題材では原典6参照・15型・参照優先順・視覚調査・style ledgerから始める。実値と仮説/提案/目標を区別し、担当間の受け渡しと判断条件をnative部品で示す。全頁の互換描画、実サイズ目視、overflow、contact、package、再読込とJTC判定までを残す。

今回の6頁は架空EC月次会議の例。現在の再生成入口はexample/source/rebuild.py、手順はexample/REPRODUCE.md。references/example-source/build_japanese_repository_examples.pyは初回制作コードの保存であり現版の再生成器ではない。

修復前の調査は3画像検索0件を記録したうえで、公式6資料の実図/PDFを確認。公開物へ外部画像・文言・数値を取り込んでいない。全6頁の実表示、nativeチャート1/表2、代表セルの編集・保存・再表示と配布再実行はexample/QA.jsonと各receiptを確認する。独立JTC17/20受理と再評価は未完了。

原典の固定commit・LICENSEを保持する。外部資料やOSフォントの再配布権を一括で保証しない。
