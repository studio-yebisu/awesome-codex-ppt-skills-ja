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
