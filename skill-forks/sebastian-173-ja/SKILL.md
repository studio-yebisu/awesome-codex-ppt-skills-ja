---
name: sebastian-173-ja
description: deck-factoryの原典CSSと13スロットで日本語HTMLスライドを組み、ChromiumでPNG/PDFへ出力する。HTMLとSVGを編集する用途に使う。
license: MIT
---
# deck-factory 日本語ガイド

原典は kimsh-1/deck-factory、固定commit `11d456351763b0efbc2a4989da688334f709dd9b`。MIT、Copyright (c) 2026 kimsh-1。[原文SKILL](upstream/SKILL.md)、[reference](upstream/reference.md)、[未変更CSS](upstream/assets/styles.css)、[LICENSE](LICENSE)を保持しています。

[完成HTML](example/index.html)は「音を、地図にする。」という架空の文化イベント企画7頁。[入力BRIEF](example/input/BRIEF.md)と[依頼文](example/PROMPT.txt)を自分の題材へ置き換えて使えます。地図・波形は説明用SVGです。音源・実測波形・実在の移動記録や音声再生はありません。編集はHTML/CSS/SVGで、ネイティブPPTXは生成しません。

1. [入力](example/input/)から頁ごとの判断と主題を定める。1920×1080を維持し、cover/chapter/statement/bullets/two-col/cards-3/data-split/image-full/image-split/flow/chart-bar/kpi-3/closingの13スロットを選ぶ。
2. [原典styles.css](example/assets/styles.css)のトークンとクラスをそのまま使う。近黒`#08090A`または紙`#F7F4EC`、四隅の情報、eyebrow→句点で終わるaction-title→主オブジェクト→tailの骨格を保つ。塗りつぶしカードを増やさずhairlineで関係を示す。
3. 日本語のkeep-all/strict、紙面の墨色、印刷サイズなどの差分は[adaptation.css](example/assets/adaptation.css)に分離する。[build.py](example/source/build.py)は原稿HTMLを組む作例コード。`python -X utf8 example/source/build.py`で再生成する。
4. 字体はNoto Sans CJK JP / Noto Sans JPの環境側fallbackで、作例キットにOS字体は同梱していない。必要ならサイトの[公式Noto字体ZIP](../../downloads/fonts/notosanscjkjp.zip)を取得する。単独ZIPではこのサイト相対リンクが使えないため、[公式固定OTF](https://raw.githubusercontent.com/notofonts/noto-cjk/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf)と[OFL](https://raw.githubusercontent.com/notofonts/noto-cjk/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/LICENSE)から取得できる。字体置換により折返しが変わり得る。
5. 原典方式はHTML→Chromium PNG/PDF→Ghostscript軽量PDF。[render-pc.py](example/source/render-pc.py)は既存Chrome＋Playwright用。`CHROMIUM_EXECUTABLE`でブラウザを選べる。クラウドの[render.py](example/source/render.py)は既存gsの直接コマンドで`deck-lite.pdf`を作る。原典が言及するcompact-pdf.shとwork/premium例は固定取得物に無いため使っていない。これらを実行済みと記載しない。

[PNG](example/render/)、[原本PDF](example/deck.pdf)、[軽量PDF](example/deck-lite.pdf)は受領済み出力を保持しました。今回の取込みでは再生成・全頁目視・追加QA・gs再試行をしていません。**[QA-PC](example/QA-PC.json)には5頁目tailが作者の安全境界980pxを約8.69px超える警告があります。1080pxの画面内にはありますが、警告を合格へ読み替えません。** 原典の全QAも未実施。[制作記録](example/PROVENANCE.json)と[QA](example/QA.json)の条件・履歴を維持し、確認量は依頼に合わせます。
