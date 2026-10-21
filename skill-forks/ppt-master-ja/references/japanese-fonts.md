# 日本語字体と配布

同梱作例はBIZ UDPGothicの公式static Regular/BoldとOFLを`example/fonts/`へ保持する。Web用subsetやOS字体の抽出ではない。PPTXには字体を埋め込まないため、編集する端末には同じ字体が必要。未導入端末で同じ見た目になるとは主張しない。

原典の固定版ではBIZが東アジア字体リストにない。作例の局所wrapperは実在するBIZ familyだけを実行時に追加し、原典ファイルは変更しない。実PDFの全頁でBIZのRegular/Boldを確認する。PPT-safe字体の助言は消さない。

別題材では指定した字体と実PDFの字体が一致するか、全角括弧・句読点・英数混在・太字・矢印を実描画で確認する。ブラウザーはdocument.fonts.ready後に描画し、PPTXは実アプリで確認する。PDFは固定表示用でありPPTX編集性の代わりではない。
