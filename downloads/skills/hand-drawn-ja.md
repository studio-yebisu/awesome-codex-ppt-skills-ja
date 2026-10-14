---
name: hand-drawn-ja
description: 原典の手描きSVGとPptxGenJS雛形で日本語の章扉PPTXを作る。
---

# チーム向け手描き章扉

1. `upstream/hand-drawn-chapter-slides/SKILL.md` と `scripts/illustrations.md` を読む。章扉5枚など、タイトルと章の役割を先に決める。フル資料とは区別する。
2. 原典PptxGenJS＋sharp雛形を使う。13.333×7.5、オフ白の図形、太い墨線、右側の象徴、左下の章題、右下の番号を保つ。
3. 観察には虫眼鏡、対話には吹き出し、試行には階段など意味に合う原SVGを選ぶ。新しい図形も不均一なBezier線と単色塗りで。
4. 日本語見出しZen Maru Gothic、表紙Dela Gothic One、英数字Manropeなど役割を分ける。意味のまとまりで改行し、説明を詰め込まない。書体・配色を変更したら原典との差分を短く記す。
5. 同梱 `references/build.cjs` と入力を参考に `npm install pptxgenjs sharp` → `node build.cjs`。原MITと使用SVGの帰属、フル書体TTFのOFLを残す。

本文だけで生成器は付属しません。一式ZIPの原典・build.cjs・inputを利用してください。フォントは手動導入が必要。確認は生成成功と代表画面の初回表示に絞り、採用とは区別します。

## この方式で気をつけること

- 表紙と4章の章扉サンプル。全文の業務資料ではない。
- 見出し・ノートはPPTXで編集できる。手描きイラストは原典SVGからの画像で、原SVGはキットに収録。

## 単体の本文から使う

この本文は `skill-forks/hand-drawn-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/ABYR1206/claude-skill-hand-drawn-slides/tree/322a265344e73cd54f77f3f07b6a9f15bb7d2d99

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `hand-drawn-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: ABYR1206 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/ABYR1206/claude-skill-hand-drawn-slides/blob/322a265344e73cd54f77f3f07b6a9f15bb7d2d99/LICENSE
