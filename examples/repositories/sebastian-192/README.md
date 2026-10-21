# 内容と見た目を決めて画像スライドを作る

SlideMuseは、内容稿から同じ内容の4スタイルを比較し、選んだ見た目で頁別画像を作るスキルです。明示依頼があれば、その画像版から編集可能なPPTXへ再構築します。

この8頁は、架空・未実施の日陰と動線の研究計画。source/styles/の4独立総覧から案3を委任選択し、Page Specと頁別生成で作りました。文字・図は画像、話者ノートのみ編集可能です。S6のnative再構築はしていません。

現在PPTXは原典strict validatorとbuild_image_ppt.pyで承認済みPNGを無加工で再包装し、原典render_deck.pyのPowerPoint backendで全8頁を実描画して見比べました。render/slide-NN.pngはPowerPoint実PDFのRGB描画、pages/は元の生成PNGです。reviews/original-renderに原典の比較記録があります。

再現はPython＋python-pptx/Pillow/jsonschemaで `python source/build_images.py reproduced.pptx`。新画像の生成には宿主imagegenが必要です。原稿を変える場合は内容稿とスタイルから作り直してください。このコマンドは既存画像の再包装です。自分の原稿から始める5段の手順と総覧依頼例はsource/REUSE.mdへ。

総覧の外枠と候補数・hashは原典検査を通りましたが、内部縮略頁の16:9は未適合です。完全なevaluate_delivery、S6、厳密OCR照合、独立再評価は未実施。初回の独自包装・未実描画からの変更はPROVENANCEに保持しています。原典MITとモデル名非露出を明記し、特定の生図モデルを使ったとは説明しません。
