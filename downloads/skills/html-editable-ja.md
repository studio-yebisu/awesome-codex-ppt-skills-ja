---
name: html-editable-ja
description: HTMLスライドをHasasasa原典converterで編集可能なPPTXへ変換する。
---

# HTMLから編集できる日本語PPTX

1. 同梱 `upstream/SKILL.md` を読み、原HTMLのページを `[data-pptx-slide]` で明示する。制作方式は原典convert.pyを使う。
2. 一頁一主張。見出しZen Kaku Gothic New、引用Shippori Mincho、英数字Manropeなど役割を分ける。日本語は意味のまとまりで改行し、過密ならページを分ける。
3. 単純なHTML背景・罫線・図形はPPTX編集を活かせる。複雑装飾とSVGは画像になる場合がある。全面画像へ平坦化しない。
4. `pip install -r upstream/requirements.txt`、`python -m playwright install chromium` の後 `python convert.py input.html --out output.pptx` を実行。OSへのフォント導入はユーザー判断。
5. 日本語フォントの局所登録例と入力は同梱referencesを参照。生成成功と主要画面の初回表示だけを確認し、採用や全ページQAとは区別する。

原典MITと使用フォントOFLを保持。技能本文だけでは変換器は付属しないため、一式ZIPのupstream/とPython依存が必要。

## この方式で気をつけること

- PowerPointで開ける配布版は、原典の --no-embed-fonts を使用。日本語書体は公式TTFを端末へ導入する。
- 原典FONT_PLANへの日本語フォント登録アダプターを使用。変換本体は原典の measure/assemble を維持。

## 単体の本文から使う

この本文は `skill-forks/html-editable-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Hasasasa/html-to-editable-pptx/tree/17c1dbb76e958543dc2741a7d50ca374354f33b7

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `html-editable-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: Hasasasa / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Hasasasa/html-to-editable-pptx/blob/17c1dbb76e958543dc2741a7d50ca374354f33b7/LICENSE
