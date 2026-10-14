---
name: ppt-design-skill-ja-entry
description: 企画をビジュアルにするを日本語で制作するときに使う。sunchaokun/PPT-Design-Skillの原典方式を使い、作例の作風を自分の題材へ展開する。
---

# 企画をビジュアルにする

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/sunchaokun/PPT-Design-Skill/tree/cbf7ef1324a026b29e2b77b71e2034554ddd3e22

- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/LICENSE
- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/README.md
- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/skill/SKILL.md
- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/skill/references/content-schema.md
- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/skill/references/design-direction-coach.md
- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/skill/references/design-principles.md
- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/skill/references/domain-paradigms.md
- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/skill/references/install-and-runtime.md

原典Build Mode / ThemeComposer / strict Presentation / published public helpers

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

- Python 3.10+ / pptx-designer1.0.0b11
- Noto Sans JP / Noto Serif JP
- PowerPointは表示QAのみ。生成はPythonだけ。



## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: 地域カフェの朝営業を試す

原典PPT-Design-SkillのBuild Modeを使い、「地域カフェの朝営業を試す」を日本語5枚にしてください。架空店舗の企画案と実績未収集を明記。2週間・平日10日・8〜10時・セット650円、15/25/35セットの売上試算を示し、利益と混同しないでください。原典テーマ合成と公開helperを使い、編集可能な文字・図形と講稿を残してください。

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: sunchaokun / 原典条件: MIT

- https://github.com/sunchaokun/PPT-Design-Skill/blob/cbf7ef1324a026b29e2b77b71e2034554ddd3e22/LICENSE

原文LICENSE・NOTICEと素材・依存物の条件を保持する。

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
