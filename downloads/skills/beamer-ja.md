---
name: beamer-ja
description: 原典Warm EditorialのBeamerを日本語教材・数式・TikZ資料に使う。
---

# 日本語Beamer

原典xukp20/build-beamer-slides `e63b61b140a00596e5260ec7611e42bfde7efb5f` (MIT)。PDFを主成果とし、.texを編集用に渡す。PPTXと称しない。

1. `upstream/styles/warm-editorial/template-169.tex` から構図を作り、`theme.tex` のmacroを直接使う。色・余白・線・数学字体は原典を基本にする。
2. `xeCJK` を読み、Shippori MinchoとZen Kaku Gothic Newの同梱TTF/OFLを相対パスで指定。見出しは明朝、本文はゴシック。
3. 題材の仮定、式、図の意味を定義し、図はTikZ、数式はLaTeXで実装。ユーザーの構図指定を優先。
4. XeLaTeXを2回、またはTectonicのXeTeXベースエンジンで同じソースをコンパイル。PDFとページPNGを生成。
5. 確認の量はユーザー指定を優先。この派生の作例では生成成功、5ページ、代表完成物の初回表示のみ。独立reviewや全ページ詳細監査を必須にせず、未実施範囲をQAへ記録する。原典のreview選択質問と詳細監査は今回の明示指定により省略した。
6. .tex/PDF/PNG/入力/依頼/原典とMIT/fontとOFL/ガイドを渡す。TeXエンジン・cacheを含めない。

## quick_validate

`python build.py --tectonic C:/path/to/tectonic.exe` を実行し、生成PDFと代表PNGを一度開く。実行していない検査を完了と記載しない。

## 単体の本文から使う

この本文は `skill-forks/beamer-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/xukp20/build-beamer-slides/tree/e63b61b140a00596e5260ec7611e42bfde7efb5f

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `beamer-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: xukp20 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/xukp20/build-beamer-slides/blob/e63b61b140a00596e5260ec7611e42bfde7efb5f/LICENSE
