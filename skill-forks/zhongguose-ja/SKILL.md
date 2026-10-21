---
name: zhongguose-ja
description: 原稿の章立てと言葉を保ち、現在の章が分かる資料へ整える。
---
# 章扉と現在章をそろえる

固定原典・commit・利用条件は[SOURCE.json](SOURCE.json)と同梱LICENSE。字体等の別条件を保持する。原典の全契約は[未変更SKILL](example/source/upstream/skills/zhongguose-ppt-skill/SKILL.md)を読む。以下は日本語の入口で、原典QAを省略する許可ではない。

## 手順

1. 中国語内容、中国的な視覚表現の意図、またはスキルを使う明示指定がある時に適用する。原稿の文言と章立てをsource-logic・architectureへ対応付ける。
2. 原典templateフォルダーを複製し、見本の本文・リンク・画像を置換する。
3. 章の入口をS09章扉で示し、各本文へ同じ順の章ラベルを置く。現在章を一つだけ強調する。
4. 本文と配置の確定後、原典由来のcover-font処理を実行し、変更のたびにfontとmanifestを更新する。
5. 原典extract-deck-outlineとvalidate-deckを実行し、原稿と大綱を比較する。字体の読み込みを待って全頁を目視する。

## 検証と引き渡し

6本文を保持して原典S09章扉を追加した7頁。原典outline抽出・validateは7頁PASS・警告0。全7頁を原典静止モードで実描画・目視。締めの章ナビと表紙現在点も修復。

上記は同梱作例の確認結果です。新しい題材では原典に指定された検査を実行します。検査失敗を閾値緩和や未実施の成功表記で解消しない。独立評価と実機発表の確認は別に記録する。

## 作例と制約

[再生成・実施範囲](example/README.md)と[QA](example/source/repair-qa.json)。

- 中国語向け原典を日本語へ派生。QijiではなくShippori Minchoを使う局所subset処理と字体・色の差分を保存。
- この日本語作例では中国色の視覚体系を意図して指定し、章扉・本文・締めを実装。PPTXと実機タッチは未実証。
- 全7枚のPNGは原典Bキー相当の静止モードで確認。ASCII動画の品質を静止画だけで保証しない。

元SKILL・LICENSE・NOTICE・実素材と出所を配布に残す。秘密情報・モデル実行履歴・依存キャッシュを追加しない。
