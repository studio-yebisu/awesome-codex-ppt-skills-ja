# 朝の20分を、組み直す。

架空の働き方ワークショップ案、4枚。20分は3+10+5+2分の例示行程、四週間は試行の計画です。改善効果の実績や健康主張はありません。

原典 Aham-AIAPP/aham-ppt の39 layoutID体系から SPC/E-03/E-04/A-90を実使用。themesの表紙・chrome、layouts.stage_flow/tri_layer、structures.swimlane_roadmapの凍結座標・接続をそのまま呼び、SVG唯一原稿から原典svg_to_native_pptxで編集可能なPPTXへ変換。汎用rendererへの置換ではありません。

変更は和文コピー、原TTFの書体指定、コバルト/黄色/墨への色置換、角丸除去。原典の白・単色を中心とするA/B/C規則とは異なるユーザー指定のskinです。

再生成: Python環境へ `pip install -r upstream/requirements.txt` → `python generate.py`。SVGはsvg_final/、完成ファイルdeck.pptx。原典lintは `python upstream/assets/tools/lint_svg.py svg_final`。PNG/PDFはPowerPointで書き出した閲覧用素材です。

原典MIT/NOTICE/ORIGINを保持。原典同梱のppt-master派生変換器は assets/svg_to_pptx/LICENSE_NOTE.md のMIT全文と帰属を保持。Python依存はpython-pptx(MIT)、CairoSVG(LGPL-3.0)、その依存の個別条件。依存バイナリ・venvはZIPへ含めません。TTFは公式原配布物・OFL同梱、端末への導入は手動です。

生成と表紙初回表示だけを確認し、全ページ詳細目視・独立レビュー・構造監査・ZIP再実行は行いません。

PowerPoint16で4枚として開き、PNG/PDFを1回書出しました。フォントを端末へ未導入の場合、指定書体は代替表示されることがあります。
