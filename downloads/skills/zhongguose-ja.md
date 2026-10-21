---
name: zhongguose-ja
description: 原稿の章立てと言葉を保ち、現在の章が分かる資料へ整える。
---

## このスキルでできること

確定した章立てを全ページのナビゲーションへ反映し、資料内の現在位置を示せる。

- 困っている状況: 長い原稿をページに分けるだけでは、章の位置や話のつながりが分からない。
- 必要な入力: 章立てが決まった原稿、発表の用途、テーマ色。
- 受け取るもの: 章のナビゲーション、紙色の本文、テーマ色の表紙を持つHTML資料とローカル素材。
- 必要環境: Python 3/fontTools/Brotli、Node.js、ブラウザー。HTMLとassetsを一緒に保持。
- 作例で試した範囲: 町の手仕事を紹介する原稿を7頁へ分け、章扉と各頁の章ナビを配置。日本語のShippori Minchoへの派生差分を保存した。

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

## 単体の本文から使う

この本文は `skill-forks/zhongguose-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/tanglele110-hash/zhongguose-ppt-skill/tree/f4c2af8ff832133822afdce87ed2d6d760631ef4

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `zhongguose-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: tanglele110-hash / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/tanglele110-hash/zhongguose-ppt-skill/blob/f4c2af8ff832133822afdce87ed2d6d760631ef4/LICENSE
- https://github.com/tanglele110-hash/zhongguose-ppt-skill/blob/f4c2af8ff832133822afdce87ed2d6d760631ef4/skills/zhongguose-ppt-skill/LICENSE.txt
