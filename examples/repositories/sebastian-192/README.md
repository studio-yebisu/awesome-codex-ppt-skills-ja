# 夏の余白｜SlideMuse 日本語作例
日陰をつなぐ小広場の架空・未実施デザイン研究、8頁。測量図・施工図・実測温度・環境効果・健康効果を示す資料ではありません。

## 見る
- deck.pptx：画像主体のPowerPoint。各頁の文字と図はPNG、話者ノートは編集可能です。
- pages/index.html：8頁の生成PNGプレビュー。完成PPTXに埋めた画像とのバイト一致を確認しました。PPTXレンダラーによる出力ではありません。
- input/BRIEF.md、data.json：日本語入力と頁別ノート
- input/deck-spec.md、page-spec.json：内容、選択、正確な文字、安定ID
- source/styles：同内容の4style overview。03を委任に基づき親が選択
- PROVENANCE.json、QA.json：由来、実行差分、最小QAの範囲と限界

## 再包装
Python 3、python-pptx、Pillowが利用可能な環境で、作例ディレクトリから次を実行します。

python source/build_images.py reproduced.pptx

生成モデルの再実行には宿主imagegenが必要です。source/prompts/に4styleと8単頁の実際のプロンプトを保存。入力を変えた場合は内容稿から作り直し、旧PNGを新内容の結果と扱わないでください。

## 原典と変更
helloo1568/slidemuse の commit 7034412b4c19915c17f8d7206e3723e9e53cf8d2、MIT LICENSEを同梱。原典の内容稿→同内容4独立overview→選択→Page Spec→逐頁生成の順序を実行。原典のvalidator/packer/render codeは実行せず、自作最小チェックと包装へ変更しました。原典テキストはsource/upstreamに保持しています。

## 限界
原典全QAは未実行。overview内部縮略頁の16:9要件は未達、方針比較のみに使用。最終単頁は1672×941、16:9の1px丸め内。初回目視で主要本文、ラベル、境界、切れを確認しましたが完全OCR照合ではありません。AI図内の補助説明が加わる頁があります。模型や矢印は概念表現です。PowerPoint実機確認・実レンダリングは未実施。モデル名は宿主非露出、指定したと主張しません。
