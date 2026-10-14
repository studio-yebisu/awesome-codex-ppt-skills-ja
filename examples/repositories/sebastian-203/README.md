# 静けさを選べる図書館

架空の公共図書館を題材にした、未実施研究提案の8頁。実績・測定結果・実在の発言は含みません。

## 原典方式

ficooooo/Paper2ScholarSlidesのacademic-review-decksmithは研究アウトラインに対応しています。同梱academic-template.pptxをpython-pptxで読み、既存マスター・レイアウト・青いタイトル線・下部帯・余白・ページ番号を保持。見本データを除去し、日本語文字と図解をネイティブ要素として追加しました。専用上流生成器はなく、source/build_deck.pyは本作例の自作コードです。上流実行スクリプトは走らせていません。

原稿の8頁を、原典の研究ロジックに合わせて背景、空間モデル、仮説、比較条件、試行、評価、実施条件へ再編しました。原稿の装飾的本アイコンやサイン見本は、研究の関係と比較を説明する図へ置き換えています。data.jsonのtitlesとnotesは完成物と対応します。

## 再生成

Pythonとpython-pptx、Noto Sans CJK JPがある環境で python source/build_deck.py を実行。PPTXはdeck.pptxへ出力。Node.jsと@oai/artifact-toolが利用できる環境では node source/render.mjs で実PPTXをimportしてPNGを再生成します。自動依存インストールなし。

PowerPoint実機確認ではありません。プレビューはartifact-toolのPPTX import renderです。別ソフトでのフォント置換や線・余白の見え方には差があり得ます。環境書体は同梱していません。添付テンプレと上流本文のMIT LICENSEを保持しています。

原典固定版：https://github.com/ficooooo/Paper2ScholarSlides/tree/207f2b6c8493c569f6caf466c87d868c42936cf6
