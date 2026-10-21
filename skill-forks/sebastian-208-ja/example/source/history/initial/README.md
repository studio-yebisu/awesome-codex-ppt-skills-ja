# 雨の図書室

架空の空間デザイン研究提案、11頁。原典academic-image-pptのbuilt-in imagegen→画像1枚/頁→ノート付きPPTX方式。

index.htmlで完成PNGを再生、deck.pptxをPowerPointで開く。本文・図はページ画像であり個別テキストや図形として編集できない。画像差替えと話者ノートの編集は可能。

入力はinput/BRIEF.md、data.json。全体依頼はPROMPT.txt。原典固定commit、変更点と確認範囲はPROVENANCE.jsonとQA.json。

再包装: npm install --ignore-scripts --cache /tmp/slide208-npm-cache、node source/package_image_pptx_with_notes.mjs --images image_pages --notes NOTES.md --out deck.pptx --title 雨の図書室。依存pptxgenjs 4.0.1。画像生成はbuilt-in imagegenを使い、課金APIを追加利用していない。

書体名は画像生成時の意図。実フォント使用・埋込・再配布は確認していない。画像には架空の構想を描く。施工図や研究成果ではない。
