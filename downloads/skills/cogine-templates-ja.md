---
name: cogine-templates-ja
description: 原稿の量と場面に合うテンプレートを選び、枠を保って内容を埋める。
---

## このスキルでできること

内容の量と用途に合う版式を選び、文字量の上限と元の操作を保ってWeb資料へ組める。

- 困っている状況: 見た目だけでテンプレートを選ぶと、必要な文章量や図版を収められない。
- 必要な入力: 読み手・用途・原稿の量と、希望する見た目。
- 受け取るもの: 内容に合う原典テンプレートを使い、文字量の上限と元の操作を保ったHTML資料。
- 必要環境: Python 3、ブラウザー。原典visual validatorはNode.js24以上と互換Chromeを使う。
- 作例で試した範囲: 香りを贈る6頁の内容を原典テンプレートへ反映。日本語のために字体・文字寸法・縦余白を意図的に変更し、原典validatorで検査した。

# 原稿に合うテンプレートを選ぶ

固定原典・commit・利用条件は[SOURCE.json](SOURCE.json)と同梱LICENSE。字体等の別条件を保持する。原典の全契約は[未変更SKILL](source/upstream/skills/ai-slide-templates/SKILL.md)を読む。以下は日本語の入口で、原典QAを省略する許可ではない。

## 手順

1. 原典AGENTSを読み、全templates/*/template.jsonのscheme・density・用途・避ける場面を比較する。
2. content_limitsと必要版式を確認し、合うテンプレートのフォルダー全体を複製する。
3. 実HTMLの埋める場所を対応付ける。今回の原典JSONにはlayout_slotsがないため局所のDOM対応表を使う。
4. 見本の文字・数字・画像をすべて置換し、本文やカードの上限を越える場合は頁を分ける。
5. 全頁をブラウザーで確認し、カウンターと章番号を区別する。利用可能な原典validate-visualも実行する。

## 検証と引き渡し

3候補比較の実画面を追加。2頁の手順、3頁の見出し間隔、5頁の三つの選択肢を調整し全6頁を実描画・目視。未変更の原典visual validatorは現HTMLで1280×720 PASS。

上記は同梱作例の確認結果です。新しい題材では原典に指定された検査を実行します。検査失敗を閾値緩和や未実施の成功表記で解消しない。独立評価と実機発表の確認は別に記録する。

## 作例と制約

[再生成・実施範囲](README.md)と[QA](source/repair-qa.json)。

- 原典は字体・主要レイアウトの保持を求める。今回は日本語化と可読性の保守依頼により、字体・文字寸法・縦余白を意図的に変更した。原典どおりの字体保持は今回の実証範囲に含めない。
- layout_slotsは原典JSONに未定義。局所DOM対応表を原典の機能と称さない。
- 原典validator自体は未変更。今回の日本語資料を検査し、60テンプレート全体の検査や保守はしていない。

元SKILL・LICENSE・NOTICE・実素材と出所を配布に残す。秘密情報・モデル実行履歴・依存キャッシュを追加しない。

## 単体の本文から使う

この本文は `skill-forks/cogine-templates-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/cogine-ai/ai-slide-templates/tree/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `cogine-templates-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: cogine-ai / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/cogine-ai/ai-slide-templates/blob/8a7a59d39f059a7e58da9c3471014ba7fe3b98eb/LICENSE
