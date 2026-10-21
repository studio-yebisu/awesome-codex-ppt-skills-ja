# 実装の指定

紙白・黒・朱のeditorial-ink。Shippori Mincho見出し、BIZ UDPGothic本文、Manrope英数字。公式OFL字体を同梱し、実PDFの使用名をqa/current-pptx-inspection.jsonで確認。

8頁に原典cover-editorial/agenda-clean/three-point-summary/before-after/case-study/process-linear/roadmap/closing-echoを使用。共通dispatch、native部品と原典QAを維持。case-studyのvisual_examples、processのstep_labels、roadmap_noteはこの派生で明示した入力拡張。配置・ラベル・文字サイズの日本語差分はsource/runtime-adapter.diffが正本。


## 2・5頁の縦配置

2頁は4条件の第2行を0.4in下げ、5頁は3手順・右側の例を下へ均等に広げる。内容は増やさず、上段のタイトルと本文の余裕、下端の共通フッターの区切りを保つ。native_vertical_spreadは派生入力で、原典の図形APIとQA閾値を変えない。
