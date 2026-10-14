---
name: sol-motion-ja
description: frontend-slides原典の固定stageで、日本語の広告・企画用モーションスライドを作る。
---

# 日本語モーションスライド

1. 原典 同梱 `upstream/SKILL.md`、`upstream/html-template.md`、`upstream/viewport-base.css` を読む。CSS全文と1920×1080 stage、SlidePresentationの構造を使う。
2. 読者に残す一言と必要な枚数を決め、各ページの役割と完成コピーを先に書く。作例は6枚。架空の計画と実績を混同しない。
3. 墨紺・蛍光ライムなど少数の色、大きい和文見出し、広い余白、内容を示すSVG図形を使う。全ページを同じカード配置にしない。
4. 一枚の入場を段階表示で演出。矢印・スワイプ・ホイール、reduce motionを保ち、必要なページだけタブ等の操作を加える。
5. 日本語フルフォントとOFL、原典MIT帰属を添え、HTMLと依頼文、使用commitを渡す。生成と確認済みを分けて記録する。

作例「夜の図書館」は制作一式ZIPの `index.html` に完成ソースを収録。そのままブラウザーで開き、原典の固定stageとcontrollerを保ってコピー・SVG・演出を自分の題材へ変える。原典を読む日本語スキルZIPと、完成ソースの制作一式ZIPは別に用意している。

原典: zarazhangrui/frontend-slides、commit 9906a34d640d2111f724544cbc50f7f130569ae1。原典MITと使用書体のOFLを保持。Studio Yebisuの日本語派生で、公式日本語版ではない。

## 単体の本文から使う

この本文は `skill-forks/sol-motion-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/zarazhangrui/frontend-slides/tree/9906a34d640d2111f724544cbc50f7f130569ae1

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sol-motion-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: zarazhangrui / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/LICENSE
