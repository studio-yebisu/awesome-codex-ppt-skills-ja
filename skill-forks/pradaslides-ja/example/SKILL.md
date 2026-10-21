---
name: pradaslides-ja
description: 読者にしてほしい行動を先に決め、必要な根拠と手順を図・記入欄・確認項目へ変える。
---

# 読者の次の行動から資料を設計する

読者に起こしたい変化と根拠を先に整理し、資料の構成・視覚表現・納品形式を選ぶ。

## 入力と出力

渡すもの：資料の読者・用途・読後にしてほしい行動、原稿や根拠資料、希望する出力形式。

得られるもの：読者の問いと主張・根拠を対応させた資料と、選択した形式の成果物・描画確認記録。

原典 [prodigeproject/pradaslides](https://github.com/prodigeproject/pradaslides/tree/b9219b238d812d0dd7b4ed9fb514effbad0d0928)、固定commit `b9219b238d812d0dd7b4ed9fb514effbad0d0928`。原文と利用条件を保存した日本語派生で、公式翻訳ではありません。

## 使う手順

1. project/brief.jsonで読者の現状・読後の行動・作る形式を決め、source-ledgerへ根拠を書く。
2. deck-planの各頁へ主張・必要な根拠・読者の次の行動を対応させ、構成とasset/layout manifestを検査する。
3. source/reproduce.pyで計画検査→native制作→PowerPoint描画→原典presenter生成まで実行する。
4. 全頁の文字・図・手順を確認し、HTMLのpresentモードとサムネイル操作も検査する。

## この作例で試した範囲

備品を借りる人の問いを6頁へ分け、申込み・受取りの記録・異常時の連絡・返却照合を異なる図と欄で示した。原典の計画検査とPPTX由来HTML presenterを実行。

**1頁：町内会の備品貸出を、迷わない手順に**：右の記録票の空欄と返却確認の□を見る。単なる項目一覧から、貸出番号・受取/返却数・日時を残す用紙へ変えた。 読者が最終的に取る行動をcommunication contractへ定め、見える記録欄へ落とす。

**3頁：受取りは、記録と現物を照合する**：3列の品名と数／貸出前の状態／受取記録を保存を見る。持ち帰る前の記録を、返却時の照合へ引き継ぐ。 各頁が答える読者の問いを先に置き、受取りと返却の役割を分ける。

**5頁：返却は、置くだけで終わらせない**：数量・付属品・状態・確認の4行を見る。受取記録との照合から、担当者の確認を残すところまで扱う。 主張・必要な証拠・次の行動に合うtopologyを選び、説明を確認項目に変える。

## 用意するもの

- Python3.10+ / python-pptx / PowerPoint16とYu Gothic（今回の描画）
- HTMLの検査にはNode22+とChromeまたはEdge。HTTPで表示。

## 制約と未実施

- この作例は架空の備品貸出手順。貸出の正式規則や運用効果を示さない。
- PPTX+実描画HTMLの経路を使用。redesign/critique/plan-onlyや他形式、AI画像・動画生成は未実施。
- 原典brief validatorの空白区切り単語数により、十分な日本語のjob文にもBRIEF_JOB_THIN助言が出る。抑制せず保存。
- Yu Gothicを使い字体ファイルは再配布しない。新しい出力の目視・独立評価は毎回必要。

現在版は制作側が全頁の実画像を確認しています。独立モデルの現在版再評価・人間の採用とは別です。自己採点はしていません。現在hashと検査は [QA.json](QA.json)、実行範囲は [PROVENANCE.json](PROVENANCE.json)、再実行は [REPRODUCE.md](REPRODUCE.md) を参照してください。
