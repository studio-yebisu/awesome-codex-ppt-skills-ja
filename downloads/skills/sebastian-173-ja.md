---
name: sebastian-173-ja
description: deck-factoryの原典CSSと13スロットで日本語HTMLスライドを組み、ChromiumでPNG/PDFへ出力する。HTMLとSVGを編集する用途に使う。
license: MIT
---

## このスキルでできること

一頁の主題を絞り、数値の意味と補足を大きさ・罫線・余白で読み分ける。

- 困っている状況: 色や装飾を足しても、主役の情報と補足の区別がつかない。
- 必要な入力: 各頁で伝える一文、根拠や図の原稿、発表条件と希望する見た目。
- 受け取るもの: 見出し・本文・注記の階層と内容に合う版式を持つHTML資料、描画と検査の記録。
- 必要環境: Python3とPlaywright/PyMuPDF/pypdf、Chrome/Chromium、作例の日本語書体 / 原典圧縮はGhostscript。本作例では存在しないcompact-pdf.shを使わずpypdfへ局所置換
- 作例で試した範囲: 原典の13スロットから一頁の主オブジェクトを選び、全頁を紙色に統一。表の末尾罫線を外して脚注と離し、締めの3数値は見出し→値→意味の順へ直した。

# deck-factory 日本語ガイド

原典は kimsh-1/deck-factory、固定commit `11d456351763b0efbc2a4989da688334f709dd9b`。MIT、Copyright (c) 2026 kimsh-1。[原文SKILL](upstream/SKILL.md)、[reference](upstream/reference.md)、[未変更CSS](upstream/assets/styles.css)、[LICENSE](LICENSE)を保持しています。

[完成HTML](example/index.html)は「音を、地図にする。」という架空の文化イベント企画7頁。[入力BRIEF](example/input/BRIEF.md)と[依頼文](example/PROMPT.txt)を自分の題材へ置き換えて使えます。地図は説明用SVGです。音源・波形・実在の移動記録や音声再生はありません。編集はHTML/CSS/SVGで、ネイティブPPTXは生成しません。

1. [入力](example/input/)から頁ごとの判断と主題を定める。1920×1080を維持し、cover/chapter/statement/bullets/two-col/cards-3/data-split/image-full/image-split/flow/chart-bar/kpi-3/closingの13スロットを選ぶ。
2. [原典styles.css](example/assets/styles.css)のトークンとクラスをそのまま使う。既定の近黒`#08090A`または紙`#F7F4EC`、四隅の情報、eyebrow→句点で終わるaction-title→主オブジェクト→tailの骨格を保つ。大きな数値はラベル→値→文脈の順へ置く。塗りつぶしカードを増やさずhairlineで関係を示す。
3. 日本語のkeep-all/strict、紙面の墨色、印刷サイズなどの差分は[adaptation.css](example/assets/adaptation.css)に分離する。[build.py](example/source/build.py)は原稿HTMLを組む作例コード。`python -X utf8 example/source/build.py`で再生成する。
4. 字体はNoto Sans CJK JP / Noto Sans JPの環境側fallbackで、作例キットにOS字体は同梱していない。必要ならサイトの[公式Noto字体ZIP](../../downloads/fonts/notosanscjkjp.zip)を取得する。単独ZIPではこのサイト相対リンクが使えないため、[公式固定OTF](https://raw.githubusercontent.com/notofonts/noto-cjk/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf)と[OFL](https://raw.githubusercontent.com/notofonts/noto-cjk/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/LICENSE)から取得できる。字体置換により折返しが変わり得る。
5. 原典方式はHTML→Chromium PNG/PDF→Ghostscript軽量PDF。[render-pc.py](example/source/render-pc.py)は既存Chrome＋Playwright用。`CHROMIUM_EXECUTABLE`でブラウザを選べる。同梱の旧render.pyはGhostscript前提で、今回実行していない。現在の軽量PDFはsource/compress_current_pdf.pyによるpypdf代替。原典が言及するcompact-pdf.shとwork/premium例は固定取得物に無いため使っていない。これらを実行済みと記載しない。

提案書の作例は全頁paper-lightを選ぶ。通常の制作で頁ごとにdark/lightを交互にせず、原典の混合表示はスタイル検査用と区別する。

原典の合格チェックリストを省かない。プロフィール、no_box、巨大数値の階層、四隅情報、句点で終わる見出し、一頁一主題、一か所のaccent、日本語改行、表紙/データ頁のhero画像とscrim/glow、軽量PDFを確認する。一つでも未達なら原典の全条件達成と呼ばない。

当作例は全7頁を再描画・目視し、4頁の無意味な01/抽象波形を外して三欄の表へ統一、5頁tailの安全境界超過を修正した。元CSSは不変。hero写真とscrim/glowは未実装のため原典チェックリスト全合格ではない。固定取得物にcompact-pdf.shがなく、WindowsにGhostscriptもないため、今回の軽量PDFはpypdf圧縮の局所代替である。原典Ghostscript実行とは記載しない。QAとsource/original-checklist-repair.jsonを読む。

## 現在の作例の実施範囲（Round4）

原典の13スロットから一頁の主オブジェクトを選び、全頁を紙色に統一。表の末尾罫線を外して脚注と離し、締めの3数値は見出し→値→意味の順へ直した。

- 原典の既定はdark editorial。今回実証したのは全頁paper-lightで、既定暗色の完成作例は未制作。
- hero写真・scrim/glowを実装していないため、原典チェックリストの全条件合格ではない。
- 固定取得物にcompact-pdf.shがなく、Ghostscriptも未使用。軽量PDFはpypdfの局所代替で、同じ処理と称さない。音声再生も未実装。

全7頁の実描画と個別の動作証拠は制作側の確認。独立Kimi K3/Opus5.5の新しい版の評価は別に行う。過去の採点を新しい画像へ引き継がない。

## 単体の本文から使う

この本文は `skill-forks/sebastian-173-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/kimsh-1/deck-factory/tree/11d456351763b0efbc2a4989da688334f709dd9b

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-173-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: kimsh-1 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/kimsh-1/deck-factory/blob/11d456351763b0efbc2a4989da688334f709dd9b/LICENSE
