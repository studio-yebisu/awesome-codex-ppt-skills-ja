# 商店街のイベント案内を、一つにまとめるの日本語派生・再現キット

Windows、Microsoft PowerPoint、Python 3.13、Node.js、游ゴシック・游明朝・Times New Romanが必要です。フォント本体は配布しません。

1. ZIPを展開して、このフォルダーでPowerShellを開きます。
2. ` .\reproduce\Reproduce.ps1 ` を実行します。新しいPython仮想環境と固定Node依存を用意し、PowerPointの全ページ描画まで常に実行します。
3. 出力は `reproduce/workspace/examples/repositories/cyberppt/deck.pptx`。再生成したQAは確認前となるため、全5枚を改めて表示確認します。

保存済み5見本からの再構築で、ImageGenの新規生成は含みません。異なる入力は旧見本と一致しないため停止します。自分の題材へ変える際は、日本語派生SKILLと原典から新しい内容lock・見本・測定・再構築を作成します。

原典の内容lock、ImageGen設計見本、要素の測定・対応登録、PptxGenJS単頁再構築、PowerPoint描画、比較、統合を使う。日本語派生は読みやすさと編集性を確認し、原典の厳密な画像一致ゲート全頁不合格を成功へ読み替えない。画像の字形差と内容の数字の欠落は別に確認する。派生mergeの背景保持と差分を残す。再現は固定した5見本からのreplayで、新規画像生成や異なる原稿への自動再構築ではない。

元のsource/reproduce.pyを直接使う方法、元ゲート未達、派生方針と実行記録はREADME.md、source/JAPANESE-FORK-POLICY.md、PROVENANCE.jsonを確認してください。原典のMIT、SVGアイコンの個別MIT条件を保持します。人による採用と公開は未実施です。

生成用lockはPptxGenJS4.0.1を保持し、間接依存image-sizeを修正版2.0.3に固定しています。検出前後のnpm auditはreview/dependency/に保存しています。このキット以外の依存監査へ読み替えません。
