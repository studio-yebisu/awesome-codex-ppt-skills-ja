# まちを、余白から。

小さな書店の週末編集室。架空の地域文化企画を8ページの日本語資料にしたサンプルです。開催実績、調査データ、第三者の発言は含みません。4週間は仮定です。

## ファイル
- deck.pptx：編集可能なPowerPoint。見出し・本文・比較・工程・ロードマップはネイティブ要素。表紙の挿絵は画像です。
- index.html：完成PPTXを読み込んだ実レンダリングPNGのプレイヤー。
- preview.pdf：同じPNGをまとめた画像ベースのプレビューPDF。編集可能PDFではありません。
- input/：日本語入力、原典入力JSON、画像と画像用プロンプト。
- source/upstream-adapted/：固定commitの原典生成器と日本語差分。MIT LICENSE保持。
- SKILL.md：日本語派生の短い使い方。

## 原典と方式
MURMURE11118586/codex-xkppt-skill、commit 978b46d116fd8fd971f9cd963f745da62f7f1f26。原典build_native_pptx.mjs、native design-system、editorial-inkを実際に利用しました。日本語固定ラベル、言語、コピー、改行、書体、締めのプレースホルダー、図形・文字主体ページの画像計画を改変しています。

## 再現
Node.jsとpptxgenjsを事前に用意し、source/upstream-adapted/package.jsonの依存条件を確認してください。自動installは行いません。このフォルダをカレントディレクトリにして実行します。画像・プロンプトは同梱の相対パスを使います。

node source/upstream-adapted/codex-ppt-skill/scripts/build_native_pptx.mjs --spec input/spec_lock.json --slides input/slides_plan.json --asset-plan input/asset_plan.json --notes input/speaker_notes.json --style-card source/upstream-adapted/codex-ppt-skill/assets/style-cards/editorial-ink.json --output reproduced.pptx

生成器とnative design-systemの両方が必要です。SKILL本文だけで生成コードが揃うわけではありません。画像再生成は表紙のページ固有プロンプトをbuilt-in imagegenへ渡します。表紙画像を差し替えても文字は編集可能です。

## 書体と表示
PPTX指定はNoto Serif CJK JP、Noto Sans CJK JP、DejaVu Sans。環境内書体を表示に利用しましたが、OS書体は抽出・配布していません。別の環境では書体の導入、または配布元のOSS書体に合わせたJSON更新が必要です。artifact-toolの日本語レンダリングは見出しがゴシック調に見えるため、明朝の厳密再現は保証しません。

## 確認と限界
原典生成・構造validation成功。8頁の実PPTX import PNGを表示確認。PowerPointやLibreOfficeで開いたとは主張しません。artifact-toolの直接PDF出力はruntime依存不足で失敗し、実PNGから画像PDFを作成しました。

原典aesthetic_qaは80.7点でFAILです。紙色の背景占有と文字主体ページ2・3の右余白を警告しました。機械報告を保持し、今回の最小確認仕様では意図した誌面の静けさとして目視判断しています。原典85点以上のqualified final判定を通過したとは表示しません。
