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
