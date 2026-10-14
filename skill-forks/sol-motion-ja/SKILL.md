---
name: sol-motion-ja
description: frontend-slides原典の固定stageで、日本語の広告・企画用モーションスライドを作る。
---

# 日本語モーションスライド

1. 原典 同梱 `upstream/SKILL.md`、`upstream/html-template.md`、`upstream/viewport-base.css` を読む。CSS全文と1920×1080 stage、SlidePresentationの構造を使う。
2. 読者に残す一言を決め、5〜6ページの役割と完成コピーを先に書く。架空の計画と実績を混同しない。
3. 墨紺・蛍光ライムなど少数の色、大きい和文見出し、広い余白、内容を示すSVG図形を使う。全ページを同じカード配置にしない。
4. 一枚の入場を段階表示で演出。矢印・スワイプ・ホイール、reduce motionを保ち、必要なページだけタブ等の操作を加える。
5. 日本語フルフォントとOFL、原典MIT帰属を添え、HTMLと依頼文、使用commitを渡す。生成と確認済みを分けて記録する。

実例: `examples/repositories/sol-motion-showcase/index.html`。再生成: `python tools/build_sol_motion_showcase.py`。本技能は frontend-slides のローカル制作用派生で、StarryKit Hosted MCP の代替を名乗らない。
