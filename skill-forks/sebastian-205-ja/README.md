# 捨てる前の一目
食品在庫の可視化UIを考える、架空・未実施の研究計画。8頁の日本語PPTX。食品ロス削減や安全性を実証した資料ではありません。

## 開く
- deck.pptx：文字・図形・UIが編集可能
- index.html / render/：完成PPTXの実レンダリング
- SKILL.md / PROMPT.txt：日本語の使い方と頼み方
- input/：研究ノートと構造化内容

## 再生成
既存 Python / python-pptx 1.0.2+ を使い、python source/build.py を実行。deck.pptx と input/data.json を再生成します。新しい題材では原資料と主張の対応を先に更新してください。このコードは本作例の8頁を描く生成ソースで、任意論文を自動抽出する生成器ではありません。
レンダリング例：soffice --headless --convert-to pdf --outdir render-work deck.pptx。そのPDFをPyMuPDFでPNG化。配布previewはLibreOfficeで生成した実PPTXの画像です。

## 出典と変更
原典 wp-a/paper2ppt、固定commit bb98ce95ca5942fc6551dddc723cbdfe2d637d59、MIT LICENSE同梱。専用生成器のない原典が認めるpython-pptx fallbackを使用。原典統括workflow、notes-only分類、claim-to-source、話者ノート、出典、評価設計ルートを保持。日本語と独自図解を追加。
原典preflight / inspectorを実行せず自作の最小確認に置換。原典全quality gate passやPowerPoint実機確認は主張しません。詳細はPROVENANCE.jsonとQA.json。
Noto Sans CJK JPは環境書体。フォントファイルは同梱しません。
