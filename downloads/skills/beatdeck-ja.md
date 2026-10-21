---
name: beatdeck-ja
description: 話す一歩ずつをクリックに割り当て、同じ図の位置を追いながら説明する。
---

## このスキルでできること

原稿を場面とクリックごとの段階へ分け、同じ図の変化で説明を進められる。

- 困っている状況: 工程を一枚に詰めると、話している箇所を聞き手が追いにくい。
- 必要な入力: 原稿・話者のメモ・出典と、各クリックで伝えたいこと。
- 受け取るもの: 場面ごとに段階表示するReact資料と、発表者用のノート・出典・場面と操作の対応表。
- 必要環境: Node.jsとruntime/package-lock.jsonの依存、対応ブラウザー。完成物はdistフォルダー一式。
- 作例で試した範囲: パンが店先へ届く工程を15段階で表示。混ぜる・形づくる・焼くで図の強調を移し、原典verifyで前進・逆戻り・直接移動を比較した。

# クリックに合わせて図を進める

固定原典・commit・利用条件は[SOURCE.json](SOURCE.json)と同梱LICENSE。字体等の別条件を保持する。原典の全契約は[未変更SKILL](source/upstream/skills/building-a-beatdeck/SKILL.md)を読む。以下は日本語の入口で、原典QAを省略する許可ではない。

## 手順

1. 原稿をreferenceへ保持し、何を舞台に置き何を講稿へ回すかCONTENT-AUDITで照合する。
2. sceneとbeatを定義し、各段階のref/source/noteと自動進行の要否を記録する。
3. 元Scene/Reveal等で段階を組み、戻りや直接URLでも同じ表示になるよう状態から描く。
4. 原典buildで型検査・bundle・外部URL検査を通し、原典verify --sourceで全beatを前進・逆戻り・直接表示で比較する。
5. contact sheetと重要フレームを開いて確認し、RUNBOOKと実施していない実機稽古を引き渡す。

## 検証と引き渡し

原典buildと未変更verifyを実行。15状態すべての前進・逆戻り・直接表示が既定0.1%で一致、layout/error/remote/warningは0。全15枚を個別に開いて目視。

上記は同梱作例の確認結果です。新しい題材では原典に指定された検査を実行します。検査失敗を閾値緩和や未実施の成功表記で解消しない。独立評価と実機発表の確認は別に記録する。

## 作例と制約

[再生成・実施範囲](README.md)と[QA](source/repair-qa.json)。

- 原典verifyは15段階、既定0.1%の閾値で一致。QR URL未指定でQRなし、Terminal/data-exact照合は0要素。
- 3.1〜3.3は同じ工程内で、ボウル→生地→天板と矢印へ図も変わる。材料量・温度・時間・実際の製パン方法は表現していない。
- 全キーの手動稽古、実機Wi-Fi切断、別端末・プロジェクターでの通し確認は未実施。

元SKILL・LICENSE・NOTICE・実素材と出所を配布に残す。秘密情報・モデル実行履歴・依存キャッシュを追加しない。

## 単体の本文から使う

この本文は `skill-forks/beatdeck-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/borjaperfra/beatdeck/tree/329a971303bedd3eeaae7c5216317fafdf2ef6a3

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `beatdeck-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: borjaperfra / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/borjaperfra/beatdeck/blob/329a971303bedd3eeaae7c5216317fafdf2ef6a3/LICENSE
