---
name: thesis-defense-ja
description: 原典Thesis Defense PPTXの無地native template、clone/replace helperとMarkdown入力で日本語の編集可能研究発表を作る。
---

# Thesis Defense 日本語版（非公式）

1. Markdown/PDF/LaTeXなど実際の研究入力を読み、問題・方法・比較・限界・展望へ絞る。仮想研究なら設定と仮想試算を明示し、観測結果へ読み替えない。
2. 入力に由来する図のallowlistを先に記録。第三者写真や大学ロゴを勝手に持ち込まない。本例は自作JSONとnative diagramだけ。
3. 同梱upstreamのminimal_markdown/build_template.pyを実行して無地templateを作る。原典clone_template_deck.ps1のDuplicate/MoveToを使い、native template pagesを必要な順で再利用する。
4. 原典pptx_template_toolsのreplace_exact_text/set_text_preserve_style/add_text/rect/write_tableで内容を入れる。templateのgeometry・サイズ・濃赤・nav/content framesは保持し、日本語字体を局所対応する。文字やnative tableを画像にしない。
5. ユーザーの枚数・確認範囲を優先。本例は6枚で、原典12–16枚/contact sheet/overflow反復の既定を省き、生成成功と代表完成物初回表示のみ。確認した範囲と未確認を区別する。

共有PowerPointの保全のためlocal runtime clone/exportはApplication.Quitを呼ばず、このcaseのdeckだけClose。未変更原本をupstreamに保持。example/rebuild.pyとexample/PROMPT.mdが具体的な入力→生成の入口。

原作者zouchenzhen、Apache-2.0。https://github.com/zouchenzhen/thesis-defense-pptx-skill 。LICENSE/NOTICEを保持。公式・大学の公認ではない。書体は同梱原TTFとOFL、PPTXフォント未埋込時は別端末で導入する。
