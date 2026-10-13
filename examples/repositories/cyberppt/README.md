# 商店街のイベント案内を、一つにまとめる

CyberPPTの原典手順と補助スクリプトを使った、日本語派生の制作例です。架空の「こもれび商店街」の課題仮説、掲載項目、担当分担、試行計画を5枚で説明します。

**原典の厳密1:1再現ゲートは未達です。** 画像の設計見本と編集可能なPowerPointでは字形・アイコン・線に差があります。原典の不合格結果を保持し、日本語の内容・読みやすさ・編集性を別に確認しました。

- [PowerPoint](deck.pptx)／[PDF](render/deck.pdf)／[全ページプレビュー](index.html)
- [日本語派生のQA方針](source/JAPANESE-FORK-POLICY.md)／[QA](QA.json)／[出典](PROVENANCE.json)
- [入力](input/outline.json)／[再実行手順](REPRODUCE.md)

原典: [crazyykhllc-bit/CyberPPT](https://github.com/crazyykhllc-bit/CyberPPT/tree/980e5576565f0673c67ee41b01d20ed66cb8417c)。MIT。原文と補助スクリプトを `source/upstream/` に保存しています。

内容をlockし、全5枚のImageGen設計見本を生成してから、PptxGenJSで単頁ずつ再構築しました。全ページをMicrosoft PowerPoint 16.0で描画・実見しています。確認済み単頁を統合し、原典の統合前後比較も通過しました。

主要文字・表のセル・罫線・矢印は編集可能なネイティブオブジェクトです。表は文字と罫線の組み合わせで、PowerPointの専用Tableオブジェクトではありません。表紙の3つの小アイコンにはTabler SVGを使い、画像blueprintをページ背景として貼り付けていません。

日時・場所・費用・商店街名・運用体制はすべて架空の例です。利用者数、時間短縮、集客効果などの実績はありません。正式採用・外部公開は未実施です。小さな脚注は手元で読む用途を想定し、会場後方からの投影可読性は未確認です。

## 生成用依存の補正

PptxGenJS 4.0.1の間接依存image-sizeを修正版2.0.3へ固定。検出前後の監査と差分は[依存補正の記録](review/dependency/README.md)を参照。配布ZIPの再生成確認とは分けて記録する。
