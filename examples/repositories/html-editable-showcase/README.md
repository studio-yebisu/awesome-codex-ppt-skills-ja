# 小さな店の、ひとつの旗。

架空の焙煎所「ひと旗」のブランド提案、5ページ。レモン色・コーヒー茶・墨黒、和文タイポと編集誌の余白で、店の姿勢から配色、看板と袋、次の試作へつなぎます。

`index.html` は元HTML、`deck.pptx` は原典 Hasasasa/html-to-editable-pptx による編集可能なPPTX。文字と単純な図形を編集する制作方式です。OOXMLの表現制約があるため全要素の完全一致を保証しません。

原典 commit: 17c1dbb76e958543dc2741a7d50ca374354f33b7 / MIT。原文LICENSE、upstream固有converter、入力、依頼文、フルOSS日本語・英数字フォントとOFLを同梱。`convert_local_fonts.py` は日本語TTFを原典FONT_PLANへ登録し、中国語フォントの自動種子を日本語へ対応させる薄いアダプター。核心のmeasure/assemble/embed処理は変更していません。

再変換: Python環境へ `pip install -r upstream/requirements.txt` と `python -m playwright install chromium`、次に `python convert_local_fonts.py index.html --out deck.pptx --keep-screenshots --no-embed-fonts --no-verify --no-visual-audit`。OSへのフォントインストールはしません。PPTX閲覧ソフトによって内包フォントの扱いが異なり、利用端末で手動インストールが必要な場合があります。

閲覧プレビューは完成PPTXからPowerPointで1回書き出した全5ページのPNG、PDFです。pptx-preview.htmlで再生できます。index.htmlは制作HTMLとして別リンクに保全しています。原典のフォント埋込版はPowerPoint COMで開かなかったため、原典の --no-embed-fonts 経路を配布。PowerPointは5枚として開けました。端末に書体が無ければ代替書体で表示されます。全ページ詳細目視、構造監査、ZIP再実行、正式採用は未実施。実施した軽い確認だけをQA.jsonに記録します。依存条件はDEPENDENCIES.mdを参照。

PPTXへのフォント埋込みは無効です。指定書体で編集するには、fonts/の原TTFを利用端末へ手動導入してください（OFL同梱）。
