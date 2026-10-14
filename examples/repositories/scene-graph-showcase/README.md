# 遠くの席へ、伝わる資料。

会場で読む資料の構成を提案する、自作の日本語教材6枚。[編集用PPTX](deck.pptx)、[PDF](deck.pdf)、[変換前draft](draft.pptx)、[PNGプレビュー](index.html)を保存しました。文字と長方形の枠はネイティブ要素です。可読性改善・理解度・最適pt値の実測はありません。

原典: eluckydog/ppt-scene-graph、commit `646e3dc4b72a444278d320c8984d5986d7fbf4bb`、MIT ©2026 PPT Scene Graph Contributors。[未変更原本](source/upstream/)と[LICENSE](LICENSE)を保持。元OutlineSpec/SlideSpec→create_from_outline(designhub_warm)→draft→元beautify(projection)→deckを実行し、[theme/sourceマップ](input/theme-source-map.json)と[BUILD](source/BUILD.json)を記録しました。汎用builderや別engineへ置き換えていません。

再生成は `python source/rebuild.py`。同梱のsource/runtimeをimportし、そのvendorのpython-pptx1.0.2を使用します。外部実行依存はlxml/Pillow/typing_extensions/XlsxWriterで、[versions・個別条件](source/dependencies/REQUIREMENTS.json)と[requirements.txt](source/dependencies/requirements.txt)を保存。依存バイナリは再配布していません。

原典vendorにはparts/が丸ごと欠けていたため、最初のimportは停止しました。[初回失敗記録](source/INITIAL-FAILURE.json)は履歴です。その後、同版公式[PyPI wheel](https://files.pythonhosted.org/packages/d9/4f/00be2196329ebbff56ce564aa94efb0fbc828d00de250b1980de1a34ab49/python_pptx-1.0.2-py3-none-any.whl)から必要なparts8ファイルだけをruntimeへ補完し、生成に成功。配布SHA256は`160838e0b8565a8b1f67947675886e9fea18aa5e795db7ae531606d68e785cba`。補った一覧・ファイルhash・URLは[vendor-parts-repair](source/vendor-parts-repair.json)、追加記録は[patch](source/vendor-parts-repair.patch)。元原本は変更していません。python-pptxのMIT ©2013 Steve Cannyも[原文](source/dependencies/python-pptx-wheel-LICENSE.txt)を補っています。

原典の制約も保持しています。

- parse_slideはSKILL/READMEに宣言されていますが、このcommitのpackage export/実装にはありません。使っていません。
- beautifyはlist_themesの表示名だけを検証するため、`theme='projection'`を直接渡すと拒否されます。`load_theme('projection').name`を元APIへ渡しました。
- createはcover/section/content/endingを作りますが、beautifyは装飾追加後のheuristicにより最初の5頁をcontent、最後をendingと判定しました。工場由来の構造は残ります。
- 既存の非文字図形の塗りは置換しないため、draftの暖色accentも完成版に残ります。既存font sizeも原典の条件に従い保持します。
- SlideSpec.notesは受理しても元createはPPTXのspeaker notesへ書きません。原稿の補足はinputに保存しています。

日本語の局所変更は[DesignSystem字体diff](source/design-ja.patch)と[a:ea/a:cs/lang diff](source/pipeline-ja.patch)。元palette、座標、FONT_SIZES、factories、beautify検出は維持。BIZ UDPGothic Regular/Boldは公式Google Fonts固定pin `66928797f271fed5ee428544e7229685e2d90127`の実TTF/OFLを[source/fonts](source/fonts/)へ同梱しています。PPTXへの字体埋込みはしていないため、編集時は公式字体を登録して使います。OS字体は抽出していません。

PowerPoint16.0で6PNG/PDFを通常exportし、表紙だけ初回表示しました。Application.Quitは呼ばず、自分のdeckだけClose。再開後に生成/export/表示をやり直していません。全頁詳細検査・独立review・evaluate採点・構造監査・ZIP再実行は未実施。[QA](QA.json)はこの範囲です。PNG viewerはプレビュー用で、制作方式は元PPTX APIです。
