# 音を、地図にする。

7頁の日本語HTMLスライド。街を歩いて音の種類と場の印象を記録する、架空の文化イベント企画です。学術成果・実測値・実施実績を示す資料ではありません。

## 開く
index.htmlをブラウザで開きます。左右キー、PageUp/PageDown、画面下部の前後ボタンで移動。全7頁。HTML/CSS/SVGのソースを直接編集できます。PowerPointのネイティブ編集形式ではありません。

同一originのiframeでは yebisu-slide / yebisu-page の0-based頁メッセージと接続。file://のorigin=nullでは親連携を無効にし、内部操作だけを使います。

日本語表示にはNoto Sans CJK JPまたはNoto Sans JPを推奨。制作環境の既存OSSフォントを使用し、フォントファイルは配布していません。閲覧環境で代替フォントになると改行が変わる場合があります。

## 再生成
python source/build.py
python source/render.py

レンダリングにはPython、Playwright、既存Chromium、Ghostscriptが必要です。CHROMIUM_EXECUTABLE環境変数でChromiumのパスを設定できます。styles.cssは原典をそのまま利用。adaptation.cssが日本語組版、スロット構図、画面縮小、印刷に対応します。

原典のwork/premium/slides実例は今回の固定repo内に存在せず、使用していません。原典のcompact-pdf.shも実行していません。必要な既存gsコマンドをsource/render.pyに直接記述しました。原典の全チェック自動化と同等とは主張しません。QA.jsonに実施状態を記録します。

音源未収録。再生ボタン・音声ファイルはありません。架空地図は個人の現在地を扱いません。内容の入力はinput/、依頼文はPROMPT.txt、由来と変更はPROVENANCE.jsonを参照。

## 今回の確認
既存PC Chromeで初回表示、左右キー送り、PNG7枚と7頁PDFを実出力。紙色頁の文字色を修正して4/6頁を再確認。cloud既存gsでdeck-lite.pdfを作成。5頁tailの内側安全境界8.7px超過warningを保持していますが、1080px内に表示され見切れ・重複はありません。QAは最小範囲です。

PDF用紙サイズも作者HTMLの1920×1080pxへ合わせ、外側白余白を解消。最終litePDFの4頁を確認しました。
