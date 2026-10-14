---
name: slidemuse-ja-image-first
description: 原典SlideMuseの画像優先ワークフローを日本語の8頁作例で実行する限定派生。
---
# SlideMuse 日本語派生
原典 helloo1568/slidemuse、固定commit 7034412b4c19915c17f8d7206e3723e9e53cf8d2、MIT。

1. 原資料・参考方向・用途/受け手・頁数・交付範囲を決める。題材の事実、仮説、未実施を分ける。
2. 完全な頁別内容稿と話者ノートを作り、根拠・可視注記・進行を自己点検。明確な内容代定がなければ確認を待つ。
3. 同じ頁順/内容から4つのスタイルoverviewを、独立4callの宿主imagegenで作る。選択または委任に基づく選択を記録。
4. Page Specに正確な文字、出典、安定ID、配色/字体意図/余白、ノートを固定。
5. 各頁を順にimagegenで生成し、その直後に画幅・見出し・重要注記・切れ・図の意味を確認。全頁同じ背景を避ける。
6. 独立source/build_images.pyで画像主体PPTXを包装。文字・図はラスタ、話者ノートは編集可。画像を編集可能スライドと呼ばない。
7. 頁数・画像画幅・ノート一致・PPTX内画像バイト一致をチェックし、実施していない検証は明記。

## この実行の差分
原典validator/packer/renderスクリプトは未実行。独立の最小構造チェック/包装へ置換した日本語派生。原典全QA合格とは表示しない。今回のoverview内部縮略頁は16:9条件を満たさず、方針比較用として保持。最終単頁は16:9（1px丸め内）。
宿主native imagegenはモデル選択を露出していないため、GPT Image2.5またはその子モデルを指定したとは言わない。外部課金APIを呼ばない。
生成画像の加工は行わず、PPTX内配置の等比縮尺のみ。プレビューはAI PNGで、完成PPTX実レンダリングではない。

## 単体の本文から使う

この本文は `skill-forks/sebastian-192-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/helloo1568/slidemuse/tree/7034412b4c19915c17f8d7206e3723e9e53cf8d2

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-192-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: helloo1568 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/helloo1568/slidemuse/blob/7034412b4c19915c17f8d7206e3723e9e53cf8d2/LICENSE
- https://github.com/helloo1568/slidemuse/blob/7034412b4c19915c17f8d7206e3723e9e53cf8d2/showcase/competition-portfolio/LICENSE.lucide
- https://github.com/helloo1568/slidemuse/blob/7034412b4c19915c17f8d7206e3723e9e53cf8d2/showcase/editable-irena/NOTICE.md
