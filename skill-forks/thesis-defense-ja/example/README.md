# 雨の日の、通学ルート。

学部生向けゼミの仮想研究発表、全6枚。地点・辺・移動時間・露出時間は学習用設定です。input/research.mdが入力正本、routes.jsonが計算データ。実在ルート、行動調査、雨天実測ではありません。

原典minimal_markdown/build_template.pyを未変更で実行し、生成した無地templateの文字・図形・geometry・サイズを使います。日本語の字体だけBIZ/Shipporiへ対応。原典COM clone helperで1,2,3,4,4,3を複製し、元pptx_template_toolsのreplace_exact_text/set_text_preserve_style/add_text/rect/write_tableを実使用しました。元build_deck.pyのMarkdown section parserも日本語メモに使っています。大学ロゴや既存大学のbinary templateは配布していません。

図と表もnativeです。文字、図形、connector、経路ノード、棒、native tableを編集できます。頁を画像として再利用していません。既存navとcontent framesは保持し、追加の角丸cardを量産せず、図/表/試算/仮定で役割を変えました。

近道14分/露出14分、屋根道18分/露出3分、川沿い16分/露出16分。J=t+λeでλ=0なら近道、λ=0.5なら屋根道が最小です。calculation-results.jsonはこのコードから計算します。図出所のallowlistに入力と生成箇所を記録しています。

再生成: Python3.10+、python-pptx/Pillow、Windows PowerPointを用意し、展開folderで `python rebuild.py`。続いて `powershell -NoProfile -File runtime/export_case.ps1 -PresentationPath deck.pptx -OutputDirectory render`。index.htmlはPowerPoint表示のPNGを見せます。日本語依頼文はPROMPT.mdで、題材を置き換えて使えます。

原典Apache-2.0のLICENSEとNOTICE、未変更原本を保持。非公式作例で大学との提携や公認を意味しません。共有PowerPointを守るためlocal clone/exportはApplication.Quitを呼ばず、自分で開いたdeckだけCloseします。残る無文書PowerPointはユーザーが終了できます。

使ったGoogle Fontsの未改変実TTF/OFLだけ同梱。PPTXはフォント未埋込、別端末ではfonts/を手動導入。原典Quality gateとしてPowerPointで全6頁をPNG/PDFへ描画し、contact sheetと全頁画像、overflowとstale text scanを確認します。2頁の比較は両候補の露出時間にそろえ、3頁の辺ラベルを線から離しました。実施結果はreviews/quality-gate.jsonとQA.json。独立評価は別記録とし、未実施を完了扱いにしません。
