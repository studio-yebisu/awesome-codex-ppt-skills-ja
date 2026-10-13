# StarryKit 固定版の実行条件

固定commitはローカルスライドアプリではなく、Hosted MCP用のMITプラグインです。原典Skillを読んで日本語5ページ分の本文・デザイン指示・講稿を準備し、原典nodeテストだけを実行しました。スライド生成は0ページです。

生成にはStarryKitのHosted MCP接続とユーザーOAuth、その環境でのformat取得・document作成・insert_pages・job追跡・ユーザーDraft受諾が必要です。今回の外部API禁止により実行しません。未確認の料金や無料利用条件は推測していません。

旧アプリは別のarchive branchですが、指定commitの代用にはしていません。ローカルCLI、公開ページ移動API、HTML wrapperは存在するものとして扱っていません。日本語の原稿はinput/authoring-plan.jsonに保存。原典HTML exportのlanguage列挙はen-US/zh-CNのみで、日本語本文のexport品質も未検証です。
