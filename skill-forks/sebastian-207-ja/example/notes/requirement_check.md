# 要求と実行

- 日本語の架空企画8頁。開催実績・定量効果は示さない。
- inputのspec/plan/asset/notes/referenceを原典nativeビルダーへ渡した。
- 原典reference選択CLI、plan validator、PPTX validator、aesthetic_qaを実行。QAコード・閾値の変更なし。
- PowerPoint16で全8頁を実描画し全頁目視。比較・番号位置・語途中改行を修復した。原典可能overlap警告は背景面や囲み面と文字の包含によるものも含むため抑制せず、実画像と照合。
- 初回80.7/FAILは履歴へ保管。現在85.7/PASSは原典機械指標であり、独立モデルの100点とは異なる。
