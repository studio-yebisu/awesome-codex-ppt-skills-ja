# 固定作例の再生成

このフォルダーで `python source/reproduce.py --input input/outline.json --render` を実行する。変更した原稿は保存済み原図と一致しないため停止する。

Windows PowerPoint、Node/PptxGenJS4.0.1、Python/pywin32/Pillow/numpy、Yu Gothic/Yu Mincho/Times New Romanが必要。PDFiumが別の既存Pythonにある場合は`--preview-python C:/path/to/python.exe`を付ける。Node依存はsource/package.jsonの固定版。既存依存を使うか、新しい導入先ではnpm install --prefix source --ignore-scripts --no-audit --no-fundを使う。

処理は1頁ずつ内容→測定→今回の再構築計画→PptxGenJS→PowerPoint→比較を実行する。最後に統合、全描画、局所比較、文字枠測定、全指定strictを記録する。原典の未達は正常終了扱いの合格ではなく、各receiptのexit1として保持する。pipelineの終了0と原典合格を区別する。

保存済みの原図・閾値・原典validatorを変更しない。新しい題材では一般SKILLの元資料分析、実画像生成、新しい要素測定と確認工程が必要。作例ZIPのupstreamは再実行用抜粋、新規の全工程は日本語Skill ZIPのupstream一式を使う。

PowerPointは自分が開いた資料だけを閉じ、アプリQuitは呼ばない。再生成直後はQAを要レビューへ戻す。過去の目視・独立評価を引き継がず、全頁を実サイズで確認する。
