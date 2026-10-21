---
name: presentation-forge-ja
description: ページを一枚ずつHTMLで編集し、講稿と発表者画面を備えた資料へまとめる。
---

## このスキルでできること

一枚ずつ編集した本文と話す講稿を、発表者画面付きHTMLへまとめる。

- 困っている状況: 長い単一HTMLを直接編集すると、ページの原稿と発表用機能が混ざる。
- 必要な入力: 原稿、頁ごとのHTML、発表者用の講稿、使用するテーマや素材。
- 受け取るもの: 各頁のHTMLと講稿、素材と字体を内包した単一HTML。現在頁・次頁・講稿を発表者画面で確認できる。
- 必要環境: Python 3標準ライブラリーとChrome/Edge。check_deckの--outはWindowsでは絶対パスにする。
- 作例で試した範囲: 待ち時間のUI説明を6頁のHTMLにし、各頁の講稿を添付。Pキーで開く発表者画面と講稿の対応をheadlessで確認した。

# 本文と講稿を一つの発表資料へまとめる

固定原典・commit・利用条件は[SOURCE.json](SOURCE.json)と同梱LICENSE。字体等の別条件を保持する。原典の全契約は[未変更SKILL](example/source/upstream/SKILL.md)を読む。以下は日本語の入口で、原典QAを省略する許可ではない。

## 手順

1. 新規資料はnew_deck.pyで作る。既存ブランドからのtheme作成では原典のimport-theme手順を使い、完成themeを.pfstyle.jsonへpackして引き渡す。再利用はunpackする。
2. 1ファイル1section.slideに分け、本文と話す説明・進行合図をaside.notesへ書く。見た目はthemeへ置き、motionはnone/subtle/balanced/lively/extraから選ぶ。engineは変えない。
3. 原典build.pyでCSS・JS・字体・素材を単独index.htmlへまとめる。
4. ブラウザーが使える場合は原典check_deck.pyを必ず実行し、問題を直してcontact sheetと全頁を見る。
5. Pキーで現在頁・次頁・講稿を確認する。編集保存や実機接続は実行できた範囲だけを記録する。

## 検証と引き渡し

未変更の原典check_deck --slides allで6頁・問題0。全6実PNGを目視。Pキーで現在4頁・次5頁・4頁の新しい話す説明と進行合図が一致することを確認。

上記は同梱作例の確認結果です。新しい題材では原典に指定された検査を実行します。検査失敗を閾値緩和や未実施の成功表記で解消しない。独立評価と実機発表の確認は別に記録する。

## 作例と制約

[再生成・実施範囲](example/README.md)と[QA](example/source/repair-qa.json)。

- 未変更の原典engine/builderを使用。日本語の字体・改行と末尾の同一origin bridgeは局所差分。
- 今回Pキーの発表者画面と講稿の一致をheadlessで実確認。実機プロジェクター、手動通し稽古、保存編集は未確認。
- HTML出力。native PPTXは生成しない。
- 今回は既存obsidianテーマとbalancedを使用。theme import、.pfstyle.jsonのpack/unpack、5段階motionの比較は未実証。

元SKILL・LICENSE・NOTICE・実素材と出所を配布に残す。秘密情報・モデル実行履歴・依存キャッシュを追加しない。

ブラウザーが使える環境では、原典の「buildとcheck_deckなしで引き渡さない」を保持する。engineは編集せず、theme/contentを分ける。標準Pythonのみのbuildにシステム全体へのpip追加は不要。

## 単体の本文から使う

この本文は `skill-forks/presentation-forge-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/thmsgo18/presentation-forge/tree/8268d3433af89a2f86e773ed8c84bbd9dd441896

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `presentation-forge-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: thmsgo18 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/thmsgo18/presentation-forge/blob/8268d3433af89a2f86e773ed8c84bbd9dd441896/LICENSE
- https://github.com/thmsgo18/presentation-forge/blob/8268d3433af89a2f86e773ed8c84bbd9dd441896/template/LICENSE
