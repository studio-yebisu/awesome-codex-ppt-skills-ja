---
name: frontend-slides-ja
description: Frontend Slidesのプリセットと固定ステージを使って、日本語のHTMLプレゼンテーションを作る。Frontend Slidesやそのスタイルを指定されたときに使う。
metadata:
  license: MIT
  upstream: https://github.com/zarazhangrui/frontend-slides
  upstream_commit: 9906a34d640d2111f724544cbc50f7f130569ae1
---

# Frontend Slides 日本語版

[SKILL.upstream.md](SKILL.upstream.md)と選択したSTYLE_PRESETS.mdの項目を読む。元の指定書体・色・署名的な配置を使う。html-template.mdのHTMLとSlidePresentationを制作の土台にして、viewport-base.cssを**全文**含める。1920×1080の固定ステージを等比縮小し、スマートフォンでスライド内を再配置しない。

英字の指定書体に日本語用Noto Sans JP等を足す。日本語だけが別のシステム書体へ落ちないよう実字形を確認する。自然な改行と異なる字重・字号を使い、内容を詰め込まない。図形は抽象的な形にする。キーボード、タッチ、ホイールを実装する。元の編集仕様に従いE編集・localStorage保存・HTML出力を整える。

指示型スキルなので、存在しない生成CLIを実行したとは言わない。適用したプリセット、参照ファイル、改変点をSOURCE.jsonと出力の制作記録に残す。ブラウザーで全ページ、編集、保存、大小画面を確認する。

LICENSEはZara ZhangのMIT。書体のOFLは別に保持する。共通レンダラーで生成したスライドを、このスキルで作った作例として扱わない。
