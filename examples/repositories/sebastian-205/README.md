# 根拠から組み立てる研究発表

paper2pptは、論文・研究ノートの主張を根拠と限界に対応させ、編集できるPPTXへ整理するスキルです。この作例は、架空・未実施の食品在庫UI研究計画8頁。実測結果はありません。

## 使い方

presentation_ja.pptxをPowerPointで開きます。deck.pptxは同じ内容の互換名。render/には現在PPTXから実描画した全8頁があります。notes/claim-to-source.jsonで、各頁の主張とBRIEFの節・固有の留保を確認できます。

再現はPythonとpython-pptx1.0.2以上、Noto Sans CJK JPで `python source/build.py`。入力台帳を先に読み、PPTXとinput/data.jsonを生成します。任意論文を自動抽出するコードではないため、自分の資料ではBRIEF・台帳・構成・生成器の本文を変更してください。

原典の検査: `python source/upstream-scripts/preflight.py input/BRIEF.md --output . --json` → `python source/upstream-scripts/inspect_pptx.py presentation_ja.pptx --require-notes --json`。新しく作ったPPTXは全頁を描画し直し、台帳と照合します。元のQAを新出力の合格として引き継ぎません。

## 確認範囲と条件

今回の修復は原典preflight、inspector、8頁の内容対応とPowerPoint16の全頁表示まで確認。独立再評価、他環境の表示、食品ロス削減効果は未確認。初回の最小QAからの変更はPROVENANCE.jsonに保持しています。原典の既定納品PPTX＋qa_reportに、依頼された制作ZIPとPNGを加えました。PDFは表示用の私的中間物で配布しません。

原典 wp-a/paper2ppt、固定commit bb98ce95ca5942fc6551dddc723cbdfe2d637d59、MIT。原典SKILLとreferences、変更していない2QA scriptを同梱。フォントは環境書体で本体を同梱しません。公式取得先はSKILL.mdに記載。
