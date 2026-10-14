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
