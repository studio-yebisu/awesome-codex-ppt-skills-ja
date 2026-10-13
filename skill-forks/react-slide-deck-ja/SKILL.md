---
name: react-slide-deck-ja
description: 原典React/ViteとFramer Motionで、日本語の図解・操作を含むWebスライドを制作する。
---

# 日本語で動くWebスライドを作る

原典は code-on-sunday/slide-deck-generator。upstream/skills/slide-deck/SKILL.md と slide-guidelines.md、references/WORKFLOW.mdを読む。原典en-context-engineeringのApp、SlideLayout、useSlideScale、animation variantsを使い、別の共通rendererへ置き換えない。

## 日本語で渡す入力

読み手、説明したいこと、実際の資料・数値、話す時間、雰囲気をまとめる。見出しは短く、問題→問い→概念→例→持ち帰りをひとつの流れにする。実例の4週間・10問は架空の企画目標で、実績として流用しない。

## 制作

1. 原典presetを一つ選び、色と動きの理由を原稿へ記録する。日本語は公式配布のNoto Sans JP等を使い、OFLと参照元を保持する。
2. Reactのページと図解を組む。単純な図はSVGとnative要素、週別タブ等は独立stateで作り、操作中にページが飛ばないようにする。新しい本文の字形をfont subsetへ含める。
3. 元のVite8/Tailwind4.2.1にはpeer衝突がある。この固定版の再現にはTailwind4.2.2と記録したlockを使う。npmの検査を--forceで無効化しない。
4. npm ci、TypeScript、Vite buildを実行。動くページ状態・クリック・キー・reduced-motionを確認し、全ページをブラウザーで見る。
5. index.htmlとassetsとfontsをひと組でHTTP配信する。Windowsの再現キットは短い展開先を使う。

## 確認と条件

原典sourceと日本語diff、入力、実行ログ、全頁の描画を保存する。外側プレイヤーと接続する場合はparentのsourceとoriginを両方確認する。PPTXは生成しない。内蔵・外部AI APIを必須にする工程ではない。制作QA、人による正式採用、外部公開を分ける。原典MIT、依存のLICENSE、書体OFLを保持する。
