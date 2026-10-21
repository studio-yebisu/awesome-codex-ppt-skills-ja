# 大綱から作り、同じ内容のテーマを変更する

日本語の大綱から6枚の編集可能PPTXを作り、暖色版からprojection版へ変更する作例です。本文を変えず、見出し・本文・帯・線の色がどう変わるかを同じ頁で比較できます。実会場での可読性や理解度の改善率は測っていません。

1. `input/outline.json`のcover/section/content/endingと本文を編集する。
2. `python source/rebuild.py`で元create_from_outline→draft.pptx→元beautify→deck.pptxを実行する。表示名検証の制約に合わせ`load_theme('projection').name`を渡す。
3. `source/render_powerpoint.ps1`でdraftと完成PPTXを描画する。`render/theme-compare-page-01.png`〜03.pngは、その実描画を同頁で並べた証拠です。
4. `source/theme-layout-repair.json`で局所補正を確認する。元beautifyは既存の非文字色を変えないため、旧帯・旧線の色移行を追加。章番号と章題・表紙副題の余白も補正しています。未改変の原典だけの効果とは区別します。

原典eluckydog/ppt-scene-graph、commit646e3dc4b72a444278d320c8984d5986d7fbf4bb、MIT。未変更原本はsource/upstream/、同版vendor補完8ファイルのURL/hash/条件はsource/vendor-parts-repair.jsonと各MITに保存。元vendorのparts欠落だけを公式python-pptx1.0.2から補完し、別engineへ切り替えていません。Pythonとlxml/Pillow/typing_extensions/XlsxWriterが必要です。source/dependencies/requirements.txtを参照。

BIZ UDPGothicの実TTF/OFLはsource/fonts/に同梱。PPTX字体未埋込のため編集端末にも導入します。日本語字体対応のdiff、nativeレイアウト補正コード、実行記録をsource/に保存しています。Application.Quitを呼ばず自分のdeckだけをCloseします。

このpinにparse_slideの実装/exportはありません。scene graph抽出は示していません。notesフィールドも元createはspeaker notesへ書きません。元evaluateは実行済みですが、文字有無・背景数・英中keywordなどによる粗い診断で、人の視覚評価や独立採点ではありません。source/original-evaluate-receipt.jsonへ警告を保存しています。SKILLが言及するtest_skill_simple.pyはpinに存在せず、実行したとは記録しません。

完成6頁・変換前3頁・比較3枚を作者が目視しました。検査記録はQA.jsonとsource/output-audit.json。独立Kimi K3/Opus5.5再評価とZIP再実行は未了です。文字と帯・線はnative、プレビューPNGは編集正本ではありません。
