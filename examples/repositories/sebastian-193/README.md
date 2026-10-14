# 小さな道案内

公共施設の入口から受付までを扱う、架空・未実施のデザイン研究提案。8頁の日本語本文・図解は編集可能なPowerPoint要素。実測値、参加者数、研究成果、引用文献を捏造しない。

## 再生成
Node.js、PptxGenJS 4.0.1、Python 3、lxmlとNoto Sans CJK JPが必要。自動インストールはしない。

node source/build.cjs
python source/preserve_master.py

完成ファイルはdeck.pptx。input/BRIEF.mdとdata.jsonが入力、PROMPT.txtが依頼文。source/template-dna.jsonとlayout-plan.jsonが原典から研究内容への構成変換を記録する。source/native-template-parts.zipは原典defaultテンプレートの汎用master/theme/layout等を抽出したネイティブ部品。原典全体・未使用の見本画像は含まない。source/upstreamには固定commitの必要な参照文書を収録。

プレビューは完成PPTXをartifact-toolへimportして実描画したPNG。PowerPoint実機で開いた確認ではない。source/render.mjsは@oai/artifact-toolがある環境で実行する。環境のNoto書体は同梱していない。

日本語派生は原典QAを自作最小検査へ置換。原典全QA合格や厳密なPowerPoint表示互換性を保証する表現はしない。
