---
name: html-scrolline-ja
description: gongnyang/awesome-html-scrolline-deckの方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。
---

# html-scrolline-ja

Studio Yebisuの日本語派生版。原作者の公式翻訳ではありません。

## 原典を読む

- upstream/SKILL.md

同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。

## 固有の制作方式

原典deck.yaml・plan・Vite build・Scrolline engineとrail-advance/era-shiftで6停止点を連続的につなぐ。engine/moves/conceptsは原典と一致。内部localeはen、HTMLの表示は日本語。Windows Chrome探索だけを明示adapterで補正する。原典全体CIのWindowsパス3件不合格を保持し、HTTP上のcore・smoke・操作確認と分ける。GSAP独自条件と各MITの原文通知を分けて保持。

## 連続する日本語の資料を作る

原典CONTRACTSとrailの例を読み、deck.yamlで停止点、時間、項目、handoffを設計する。原典plan、Vite build、smokeを使い、engine・moves・conceptsを改変せず、deck側のCSSと本文で日本語へ合わせる。内部schemaのlocaleはen、HTMLのlangはja。日本語locale機能を実装したとは呼ばない。

原典全体CIのWindowsパス3件不合格は保持する。中核424テスト・HTTP smoke・キー・ホイール・補間の確認と区別し、原典の全ゲート通過を主張しない。捕捉用Chrome探索のadapterは原文と差分を残す。直接file://の禁止を別経路で回避しない。

原典コードのMIT、LenisのMIT、GSAP独自の無償標準ライセンスを分けて読む。Viteが削除する通知は配布bundleと単一HTMLへ復元する。GSAPへMITやカタログのCC0を付け直さない。フォントは端末の日本語書体を使う当作例の条件を記し、新しい字形と全停止点を実際に確認する。

## 日本語で完成させる

- 先に読み手、目的、結論、必要なページ、出力形式を決める。
- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。
- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。
- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境を案内し、主要な完成ファイルが開くことを確認する。
- 原典の方式で実ファイルを生成し、主要な出力の初回表示を確認する。原典の必須ビルド確認は維持し、明白な欠けだけ直す。

## 再現と利用条件

完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。

## 単体の本文から使う

この本文は `skill-forks/html-scrolline-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/gongnyang/awesome-html-scrolline-deck/tree/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `html-scrolline-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: gongnyang / 原典条件: MIT（原典） / GSAPは独自の無償標準条件 / LenisはMIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/gongnyang/awesome-html-scrolline-deck/blob/d17200400a6b9cd7e1e42929e4edef5b0f69c1cc/LICENSE
