---
name: html-to-ppt-pdf-ja
description: Guizang形式のHTMLを原典html-to-ppt-pdfで画像PPTX・PDFへ変換する。日本語の実変換例と、ページ抜け・重複・個別条件を確認する派生手順を使う。
---

# 日本語HTMLを画像PowerPointとPDFへ

Studio Yebisuの日本語派生版。原作者の公式日本語版ではありません。
upstream/SKILL.mdとupstream/scripts/build.mjsを読む。入力はGuizangのsection.slide、#nav .dot、静止操作に対応する既存HTML。原典CLIで実際に撮影・梱包し、別の共通rendererへ置き換えない。

## 変換前にそろえる

- 入力HTMLまたはHTTPのURL、画像・書体の依存、出力先、画面比率を確認する。原稿を新しく構成する工程とは分ける。
- 画像主体PPTXでは本文・図表・文字を個別編集できない。日本語の発表者ノートは別途付けられる。動きは静止画像になる。
- 既存の港町例は架空の企画。数値・予算・目標を実績にしない。
- 原典の標準scale3で日本語を撮影する。軽量化する場合はscale2を選び、実際の表示で文字を確認する。

## 原典CLIで変換する

references/WORKFLOW.mdとキットのREPRODUCE.mdを読む。Windowsのnpmランチャーが失敗した場合は、Node.exeと同梱npm-cli.jsで依存を導入する。今回の固定lockはPptxGenJS3.12を保持し、image-size2.0.3だけをoverrideした。

ページ成功数だけを信頼しない。原典の撮影間隔より入力資料の700ms操作待ちが長いとページが重複する。元HTMLを残し、変換用export.htmlのdotから既存go(i,{force:true})を呼ぶ補正を用いた。原典変換器は変更していない。すべてのページの順序と異なる内容を確認する。

## 引き渡しを確認する

- PNG、PDF、PPTXのページ数・順序・日本語を全ページ確認する。PPTXはPowerPoint本体で描画する。
- ノートを後処理で追加する場合は原典出力を保存し、本文画像とslide XMLが一致することを確認する。
- この作例の再現CLIは既存7ページの変換用。新しいHTMLや異なるページ数には、原典手順から別の変換とレビューを行う。
- 再生成のQAは確認前。制作エージェントの確認を、人による正式採用や外部公開へ読み替えない。

## 原文の条件を区別する

変換器はMIT。Guizang入力ソースはAGPL-3.0で、対応ソースを事例キットに保持している。埋込書体はOFL。原文表示を保存し、カタログのCC0をこれらへ一括適用しない。
