# crazyykhllc-bit/CyberPPTの日本語制作

原典: https://github.com/crazyykhllc-bit/CyberPPT/tree/980e5576565f0673c67ee41b01d20ed66cb8417c

原典の内容lock・画像blueprint・測定比較＋日本語派生のネイティブ再構築

原典の内容lock、ImageGen設計見本、要素の測定・対応登録、PptxGenJS単頁再構築、PowerPoint描画、比較、統合を使う。日本語派生は読みやすさと編集性を確認し、原典の厳密な画像一致ゲート全頁不合格を成功へ読み替えない。画像の字形差と内容の数字の欠落は別に確認する。派生mergeの背景保持と差分を残す。再現は固定した5見本からのreplayで、新規画像生成や異なる原稿への自動再構築ではない。

## 作例

- 商店街のイベント案内を、一つにまとめる / 5枚 / pptx
- カタログ内の案内: repository.html?repo=crazyykhllc-bit/CyberPPT
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=crazyykhllc-bit/CyberPPT
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Node.js / PptxGenJS 4.0.1
- Python / Pillow, numpy, pywin32
- Windows / Microsoft PowerPoint
- Yu Gothic / Yu Mincho / Times New Roman
- 新規設計見本にはImageGen

## 元の制作コマンド

    python examples/repositories/cyberppt/source/reproduce.py

## 確認範囲

- 原典の厳密な画像一致は全5枚で未達。日本語派生版の確認済み作例として掲載。
- エージェントが全ページを確認。独立審査・人による採用・公開は未実施。
- 商店街・日付・会場・料金・運営案は架空の例。実施効果は未測定。
- 再現キットは保存済み見本からの再構築。別原稿には新しい設計見本と測定が必要。
- 新しく生成した出力は、全ページを改めて表示確認する。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
