---
name: paper2ppt-ja-example
description: 研究論文・研究ノートを、根拠と限界を保持した編集可能な日本語PPTXにする。
---
# 日本語の研究資料をつくる
原典 wp-a/paper2ppt の固定commitとMIT条件を保持する。原典SKILL・evidence-first workflow・paper-types・tool-routingを読む。参照は source/upstream-references と source/UPSTREAM_SKILL.md に同梱。
1. 入力を full-paper / partial-paper / notes-only に分類する。架空・未実施を隠さない。
2. 主張を原資料の節へ対応させる。数値・引用・実験結果を補完しない。
3. 1頁1主張で、提案・仮説・評価計画・限界を分ける。全頁に出典と話者ノート。
4. 専用生成器のない原典で認められた fallback として python-pptx 1.0.2+ を使う。source/build.py はこの作例の独自生成ソース。
5. 完成PPTXを実レンダリングし、欠け・重複・誤解を直す。未検証は明記する。
この作例は8頁の研究計画。結果頁を捏造せず、Methods/toolsの評価設計部分を資料量に合わせて使う。墨緑、ライム、穏やかな橙。棚・時間帯・天秤・UI・工程・評価マトリクスで構成を変える。
フォントは環境のNoto Sans CJK JP。OSフォントは配布しない。既存python-pptx、PyMuPDF、LibreOfficeを使用。自動インストールしない。
原典 https://github.com/wp-a/paper2ppt/tree/bb98ce95ca5942fc6551dddc723cbdfe2d637d59

## 作例の書体を揃える

Noto Sans CJK JPのRegular/Boldは、サイトの「作例の書体を取得」から公式配布物とOFL原文を取得できる。原稿とPPTXに指定したフォント名を揃える。Noto Sans JPとは名前が異なる。OSの書体は抽出せず、作成者と受け手の端末に公式フォントを導入する。

固定配布元: https://github.com/notofonts/noto-cjk/tree/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/OTF/Japanese

## 単体の本文から使う

この本文は `skill-forks/sebastian-205-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/wp-a/paper2ppt/tree/bb98ce95ca5942fc6551dddc723cbdfe2d637d59

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-205-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: wp-a / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/wp-a/paper2ppt/blob/bb98ce95ca5942fc6551dddc723cbdfe2d637d59/LICENSE
