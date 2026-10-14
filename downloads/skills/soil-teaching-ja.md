---
name: soil-teaching-ja
description: SOIL原典の認知的ページ役割とMode CオフラインHTMLで、大きな日本語と意味のある段階図を持つ教材を作る。
---

# SOIL 日本語教材スライド（非公式）

最初に各ページの題名、教える一点、学習者の作業、認知的役割、図の関係、短いラベル、結論を計画する。既定は計画確認を待つ。ユーザーが内部計画・題材・Mode C・styleを明示承認済みなら、その承認をinput/PLANに記録し、工程ごとの再確認は省略する。本作例はこの条件で制作した。

1. 同梱upstream/SKILL.mdとreferences/html-slide-deck.mdを必要範囲で読む。全体/部分、比較、順序、練習など、そのページの思考関係に合わせて図を決める。
2. assets/html-deck-templateを出力へコピー。1600×900 stage、semantic section、見出しとのaria-labelledby、unique data-slide-id、local styles.css/slides.jsを保つ。元テンプレートを直接変更しない。
3. 日本語を大きく短く配置。HTML/SVGの区画・線・数値で関係を示す。原典.fragmentを使い、題名・学習者の作業は最初から、根拠・答えは教える順で段階表示する。
4. 元controllerのadvance/retreatとfragment count、矢印/Space/Home/End/hash、全画面、reduce motion、印刷全段表示を保持する。CDN・remote font・analytics・新frameworkは不要。
5. 完成物を一度開き、依頼された範囲で生成成功と主要画面を確認する。追加検査の量はユーザー指定を優先し、未確認の授業品質や印刷互換性を保証しない。

実例はexample/、依頼と計画はexample/input/。index.htmlを直接開いて使える。大きい日本語の書体を変えるときは、配布許諾のある実TTFと原文ライセンスを含める。

SOIL Teaching Slides Skill by 李俊儀。原典 https://github.com/chunyifish/soil-teaching-slides 。この日本語改変SKILLと元の方法説明はCC BY-NC-SA 4.0（非商用・帰属・継承）、実行HTML template/JS/CSSはMIT、書体はOFL。原典の公認ではない。LICENSE-CONTENT.md/NOTICE.md/原MITを保持。

## 単体の本文から使う

この本文は `skill-forks/soil-teaching-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/chunyifish/soil-teaching-slides/tree/ebeb43ce0e4360ba2ffc91dcfb4be5ba203bb09f

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `soil-teaching-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: chunyifish / 原典条件: MIT (software / HTML template); CC BY-NC-SA-4.0 (SOIL content / adapted skill)。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/chunyifish/soil-teaching-slides/blob/ebeb43ce0e4360ba2ffc91dcfb4be5ba203bb09f/LICENSE
- https://github.com/chunyifish/soil-teaching-slides/blob/ebeb43ce0e4360ba2ffc91dcfb4be5ba203bb09f/NOTICE.md
- https://github.com/chunyifish/soil-teaching-slides/blob/ebeb43ce0e4360ba2ffc91dcfb4be5ba203bb09f/LICENSE-CONTENT.md
