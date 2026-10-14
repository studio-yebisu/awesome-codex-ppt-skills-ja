# 引き継ぎは、次の一手まで。

原典 Visual Deck Studio のHTML-first Path Aで制作した日本語6枚。社内資料の引き継ぎを説明する、架空の記入例です。

編集可能な正本はdeck.pptx。HTMLはindex.htmlとslides/、元HTMLのPDFはdeck.pdf、PowerPoint実描画PDFはrender/deck.pdfです。本文と単純な線・背景はnative要素。画像スライド化していません。HTML/PPTXには字間・太さ・br行間差があります。pixel一致は主張しません。

## 同じ作例を生成

Python3の標準ライブラリ、Node.js22以上とnpmが必要です。初回は固定npm依存と公式Chromiumを取得します。

    python source/reproduce.py --powerpoint

NodeがPATHにない場合は --node に実行ファイルの絶対パスを指定します。PowerPoint描画にはWindows / Microsoft PowerPoint / PowerShell7とインストール済みBIZ UDPGothicが必要です。この環境では登録済みのBIZ UDPGothicを確認しました。配布フォントはGoogle FontsのOFL原本で、OSのフォントを抽出していません。

生成後はこのフォルダーで `python -m http.server 8000 --bind 127.0.0.1` を実行し、http://127.0.0.1:8000/index.html を開きます。原典の概覧・gallery・矢印キー・Home/End・ページ記憶を使えます。新しい再現出力は全ページレビュー待ちになり、前回のQAを引き継ぎません。

## 原典を実行した範囲

固定commit 06ddac077030c62f0118b225860cac46fbf658ea のSKILL、Path A、deck_index.html、html2pptx.jsの寸法/overflow/文字条件検査と要素変換、export_deck_pptx.mjs、PDF結合、縮略図を使用。変換コードのローカルHTTP入口、字体待ち、Windows環境継承、日本語ノートだけを明示adapterで補いました。source/runtime-adapter.diffと原文を保持します。

既存の紙色・深緑の設計文脈を使い、2ページを先に制作・表示確認してから全6枚を制作。人の早期承認、3方向Fallback、file URL、動画、音声、全機能の検証は行っていません。外部APIや課金は使いません。

archive全体取得は読み取りtimeoutで終了。必要22ファイルを固定commitのGit blobと照合して取得し、紹介画像・BGMは収録していません。source/upstream/ACQUISITION.jsonに記録しています。

## 依存と権利

原典MITの著作権表示、BIZ UDPGothicのOFL、使用依存の原文通知をlicenses/に保存。未使用のアニメーション素材の権利を保証する記録ではありません。

PptxGenJS4.0.1とPlaywright1.60.0を保持し、検出されたimage-sizeとsharpを2.0.3/0.35.5へ固定。初期lock・監査、修正後の0件監査、全12画像と本文/ノートの変化がない記録はreview/dependency/。この再現キット以外の依存監査へ読み替えません。
