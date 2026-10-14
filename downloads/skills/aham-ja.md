---
name: aham-ja
description: Aham固有layoutIDと凍結座標のSVG部品を使い、編集可能な日本語PPTXを作る。
---

# 日本語の編集できる図解PPTX

1. upstream/SKILL.md、references/layout-library.mdと必要な骨格を読み、原39layoutIDから目的に合うものを選ぶ。例はSPC/E-03/E-04/A-90。
2. 原典themes/layouts/structuresの関数と定義済み座標を使い、SVGを唯一原稿にする。数字は入力正本から、試行案と実績を分ける。
3. 日本語の見出しを大きく、図内は短く。見出し・本文Zen Kaku Gothic New、英数字Manropeなど役割を指定。意味のまとまりで改行し、過密なら枚数を分ける。
4. 配色・書体のskin変更を記録。関数の座標と接続を保ち、原典svg_to_native_pptx_wrapperの経路でnative PPTXへ変換する。
5. `pip install -r upstream/requirements.txt` → `python generate.py`。原典lintと主画面初回表示だけ確認。技能本文だけでは変換器と入力は付属しないため、一式ZIPと作品ZIPの生成ソースを使用。

原MIT・NOTICE・ppt-master派生のLICENSE_NOTE・使用TTF/OFLを保持。OSへの書体導入は手動。API keyは不要。

## 単体の本文から使う

この本文は `skill-forks/aham-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/Aham-AIAPP/aham-ppt/tree/c2b4ece69bbac777557934f981457c1f98c2b73f

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `aham-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: Aham-AIAPP / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/Aham-AIAPP/aham-ppt/blob/c2b4ece69bbac777557934f981457c1f98c2b73f/LICENSE
- https://github.com/Aham-AIAPP/aham-ppt/blob/c2b4ece69bbac777557934f981457c1f98c2b73f/NOTICE.md
