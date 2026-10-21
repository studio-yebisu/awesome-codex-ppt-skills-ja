# MarkdownをSVGのページへ組む

原稿を「ページ構成→デザイン→SVG」に分けるスキルです。本作例はSwissの赤・黒・白を使った架空例集7頁。文字・図形はsvg/で編集でき、PDFは固定レイアウトです。

今回の修復では構成と設計を先に保存し、生成器が日本語font stackと配色を読みます。全7頁の実PDFを見て、HTMLでも全7頁の送り戻りを確認。原典PDF exporterを実行し、既存Chromeを選ぶ1行のadapterを加えました。原本・diff・実行記録はsource/にあります。PowerPointへの挿入・図形変換と原典PPTX exportは未確認です。

再現: Python＋PyMuPDF、Node.jsとsource/package-lock.jsonの依存、Chrome/Chromium、Noto Sans CJK JPを用意。`npm ci --prefix source` → 必要ならSVG_CHROME_EXECUTABLEを設定 → `python source/build.py`。新しい環境へのnpm ciは未実施。現在の固定7頁を作り直すコードであり、題材変更時は構成・デザイン・著述内容を変更します。再生成後は全頁を確認してください。

初回は構成と設計を生成後に書き出し、InkscapeでPDF化していました。その履歴はPROVENANCE.jsonに保持。今回の検査と混同しません。独立再評価・正式採用は別です。原典MITと帰属を保持し、OSの書体ファイルは同梱しません。
