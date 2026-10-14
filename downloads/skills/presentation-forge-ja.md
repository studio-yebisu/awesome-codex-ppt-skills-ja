---
name: presentation-forge-ja
description: Presentation Forgeの1頁1HTML、未変更engine、obsidianテーマと標準Pythonビルドで、オフラインの日本語Web発表を作る。
license: MIT
---
# 一枚ずつ書いて、ひとつのHTMLへ

原典 **thmsgo18/presentation-forge**、固定commit `8268d3433af89a2f86e773ed8c84bbd9dd441896`、MIT ©2026 Thomas Gourmelen。iconsはLucide ISC/Feather MIT、字体は別のOFL-1.1。

- [元SKILL](https://github.com/thmsgo18/presentation-forge/blob/8268d3433af89a2f86e773ed8c84bbd9dd441896/SKILL.md)
- [作成script](https://github.com/thmsgo18/presentation-forge/blob/8268d3433af89a2f86e773ed8c84bbd9dd441896/scripts/new_deck.py)
- [固有templateとstdlib build](https://github.com/thmsgo18/presentation-forge/tree/8268d3433af89a2f86e773ed8c84bbd9dd441896/template)
- [書き方とlayout/components/motion](https://github.com/thmsgo18/presentation-forge/tree/8268d3433af89a2f86e773ed8c84bbd9dd441896/reference)

MDだけでは実装・素材・字体を含みません。同じサイトの **presentation-forge-ja.zip** を取り、example/input・source/deck・原本と実TTF/OFLを利用するか、固定原典を実取得してください。

1. 原稿、読み手、ひとつの主張と流れを決め、input/deck-plan.jsonへ記録。ユーザーが一度に制作を依頼した場合、原典の初回2質問と構成待ちは省略し、all at once / balancedを使う。
2. 新規なら `python scripts/new_deck.py 新規folder --title 題名 --lang ja --theme obsidian --motion balanced`。元template内へ作らない。複製済み作例ならexample/source/deckを使う。
3. slides/01-*.htmlから1ファイル1section.slideで書く。見出しはひとつの主張、本文はその説明だけ。長い話はaside.notesへ。原典のstats、steps、timeline、two-col、icons、data-anim/data-staggerを意味に合わせて選ぶ。
4. engineは変えず、色・字体はthemes、個別の日本語改行と行高はdeck.cssに置く。作例は元obsidianの紫とシアンを保持。短い明朝見出し、BIZ本文、Manrope英数字、JetBrains Monoコード役を分け、公式TTFと原文OFLを使う。コードには日本語fallbackと合字off。
5. 原典 `python build.py` が素材/CSS/JS/字体を内包した単独index.htmlを出す。配布作例では `python example/source/rebuild.py` で元buildを実行し、原文条件と0-based parent bridgeを末尾に加える。元DeckStage.show/indexに委ね、元engineを共通rendererへ替えない。
6. 既存deckのブラウザー編集を保全する。元buildは先にpullする。主な出力を初回表示して元ページ送りを確認。ユーザーが最小確認を指定した作例では、全頁検査/contact sheet・独立採点・全ZIP再実行を必須にしない。未実施範囲はQA.jsonへ。

編集対象はHTML/CSS/元JS、PPTXは生成しません。作例「待つ時間にも、道しるべを。」は架空の画面設計提案。進捗率、所要時間、製品効果を発明せず、処理で取れる状態と実装した行動を原稿にする。原典の編集保存、発表者、印刷などはcodeを保持し、個別検査済みと称しません。

## 単体の本文から使う

この本文は `skill-forks/presentation-forge-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/thmsgo18/presentation-forge/tree/8268d3433af89a2f86e773ed8c84bbd9dd441896

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `presentation-forge-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: thmsgo18 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/thmsgo18/presentation-forge/blob/8268d3433af89a2f86e773ed8c84bbd9dd441896/LICENSE
- https://github.com/thmsgo18/presentation-forge/blob/8268d3433af89a2f86e773ed8c84bbd9dd441896/template/LICENSE
