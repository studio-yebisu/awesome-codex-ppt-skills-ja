---
name: rain-library-academic-image-ppt-ja
description: 原典academic-image-pptに基づく日本語の画像版研究提案スライド
---

# 日本語・画像版研究提案

原典: https://github.com/demoolight/academic-image-ppt/tree/2aac1a711ff658ab67d79a0e98cc54b5a0468751 。MIT、LICENSE保持。

入力と構成を先に整え、各頁の主張・正確なコピー・図の目的・根拠・ノートを記す。架空提案と実績を区別する。3案のstyle boardをbuilt-in imagegenで作り、選んだ方向の契約を記録する。原典は各段階のユーザー承認を求める。本作はユーザーの自律完遂指示により制作担当が判断する派生で、承認を取得したとは記録しない。

1. input/data.jsonとqa/deck-blueprint.mdを入力にする。
2. 紙白・深紺・雨灰、大きな明朝見出し、細線図版、暗い区切りを使う。
3. built-in imagegenで一頁一画像。ローカル描画で代用しない。文字・ラベル・頁番号・未検証表記を確認する。
4. 機械的な寸法調整のみ許可。完成PNGは1600×900。
5. source/package_image_pptx_with_notes.mjsで画像とNOTES.mdを包装する。
6. 頁数・画像数・ノート数を照合し、主な出力の表示と明白な欠けを確認する。

本文・図は画像、ノートと画像差替えは編集可能。個別図形編集可能PPTXと称さない。
