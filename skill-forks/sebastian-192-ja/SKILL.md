---
name: slidemuse-ja
description: 本・論文・報告・原稿から、四つのスタイルを比較して画像主体のスライドを作る。明示依頼時は画像版から編集可能なPPTXへ再構築する。
---

# 内容と見た目を決めてから、ページを画像で作る

原典 helloo1568/slidemuse / 7034412b4c19915c17f8d7206e3723e9e53cf8d2 / MIT。非公式の日本語案内。source/upstream/SKILL.mdと参照文書を読む。

1. 原資料、参考方向、用途と受け手、頁数、納品範囲を確認する。既存の指定・委任を引き継ぎ、不足だけを確認する。任意の編集済みPPTXを直接修正する用途とは分ける。
2. 原資料を読み、全体の答えと頁ごとの主張・根拠・説明・限界・話者ノートを含む内容稿を作る。内容自検を行い、内容を確認するか、既存の代定権限を記録する。
3. 同じ内容と頁順の4スタイルを、独立した4回の宿主imagegenで総覧にする。8頁以下は全頁、それより多い場合は6〜8代表頁を同じ組で示す。総覧は横長、縮略頁も指定比率・等大・余白・外側頁番号を保つ。validate_style_options.pyと目視を行い、選択または委任による代選を記録する。明示的な固定参照・省略は原典の条件に従う。
4. 確認済み文字・データ・出典・要素意図・安定ID・書体/色/余白をPage Specへ固定し、validate_page_spec.py --strictを実行する。画像版を飛ばして編集用PPTXへ直行しない。
5. 頁別imagegenで画像を作り、直後に文字・数字・図の意味・欠け・指定比率・全体の統一を確認する。誤りは該当頁だけ直す。原典の内容監査と画像/台帳のhash対応を使い、機械チェックを目視の代わりにしない。
6. 全頁が確認できたら、validate_page_spec.py --require-images --strict → build_image_ppt.py → render_deck.py。画像版PPTXを実描画して全頁を見比べる。画像の文字を個別編集できるとは説明しない。生図能力がない場合はその段階で止める。
7. 明示的に編集版が必要な場合だけS6へ進む。既知の文字/数値は再OCRせず、画像を層分けしScene v1へ記す。文字・単純図形・表・可靠データ図をnative、複雑な絵を分離画像にする。全面画像を編集用の底絵として残さない。
8. 編集版はbuild_editable_ppt.pyとaudit_editability.py、全頁の原図比較、文字変更・図表編集・移動で確認する。リリースの完全合格はevaluate_delivery.pyの現出力に紐づく記録で判断する。未実施を合格と記載しない。

## この8頁の作例

架空・未実施の日陰と動線の研究計画。内容稿→4独立総覧→委任による案3選択→Page Spec→8画像の制作を実行した。完成頁の画像は16:9の丸め1px内。画像本体の文字・図はラスタ、話者ノートは編集可能。宿主のモデル名は非露出で、特定のImage2.5子モデルを指定したとは記さない。

今回の修復ではPage Specを原典schemaへ整え、原典の総覧検査、画像付きstrict検査、画像PPTX packer、PowerPoint render_deckを実行し、全8頁を確認した。画像は再生成・再圧縮せず、承認済みPNGをそのまま埋めた。総覧の内部縮略頁は指定16:9に未適合で、外枠の構造検査合格と全視覚条件の合格は分ける。S6編集版と完全なevaluate_deliveryは未実施。原稿を変える場合は内容稿からやり直し、旧画像を新しい原稿の出力として扱わない。

## 再現

Python、python-pptx、Pillow、jsonschema。PowerPoint描画にはWindowsとMicrosoft PowerPoint。新しい画像を作るには宿主imagegenが必要で、原典script自体は生図/OCR/課金APIを提供しない。`python source/build_images.py reproduced.pptx` は承認済み8画像を原典validator/packerで再包装する。画像を作り直す処理ではない。

原典: https://github.com/helloo1568/slidemuse/tree/7034412b4c19915c17f8d7206e3723e9e53cf8d2
