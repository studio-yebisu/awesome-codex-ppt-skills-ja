---
name: presentation-delivery-ja
description: Visual Deck StudioのHTML-firstとDOMからの要素変換を使い、日本語のHTML・編集可能なPPTX・PDFを同じ原稿から制作するときに使う。
---

# Visual Deck Studio 日本語の資料制作

Studio Yebisuの独自派生。原作者の公式翻訳ではない。固定commit `06ddac077030c62f0118b225860cac46fbf658ea` の原典コードとMIT表示を保持する。

## 実例から始める

「引き継ぎは、次の一手まで。」日本語6枚。用途・場所・次の行動、用途と版がわかるファイル名、完了／保留をまとめた資料である。本文・単純図形・ノートをPowerPointで編集できる。HTMLの概覧からも再生できる。

完成例ZIPの `input/data.json`、`slides/`、`source/runtime-adapter.diff`、`deck.pptx` と全ページのPowerPoint描画を対応させる。この作例は架空の記入例で、社内規則や実績ではない。

## 原典の制作経路

1. `upstream/skills/visual-deck-studio/SKILL.md` と `references/slide-decks.md`、`references/editable-pptx.md` を読む。原典のHTML-firstを守り、先に出力と編集範囲を決める。
2. 新しい資料では読み手・目的・根拠・字体・配色を決める。実在製品を取り上げる場合は、原典の事実確認・ブランド素材の工程が必要。この実例では実在ブランドを取り上げていない。
3. 原典Path Aで、独立したページHTMLを作る。5枚以上では構造の異なる2枚を先に制作・確認してから全体へ進む。人の早期承認を受けていない場合は、制作側の仮定として記録する。
4. 原典 `assets/deck_index.html` を複製し、manifestを自分のページへ設定する。概覧・gallery・scale・ページ記憶・キー操作を別のplayerで置き換えない。
5. 原典 `html2pptx.js` とexporterを使う。手書きの別PPTX rendererへすり替えない。HTTP入口、字体待ち、日本語ノートのadapterと差分を保持する。
6. 原典PDF結合と縮略図を生成し、全ページのHTMLと実PowerPointを見比べる。字間・字体の太さ・br行間は一致しないことがある。内容の一致とpixel一致を分ける。

## 編集可能なHTMLの条件

- bodyは `960pt × 540pt`（1280×720pxと等価）にする。
- 主な文字をpまたはh1〜h6へ入れる。divの裸文字やspanだけの主本文を使わない。
- 文字タグに背景・border・shadowを付けず、必要なら外側のdivへ置く。
- divのbackground-imageやgradientを使わない。複雑なWeb表現を残す必要がある場合はHTML/PDFを正本にする。
- 合わせて編集する段落には原典の `data-pptx-merge` を使う。PPTX側の見た目を全ページ確認する。
- 原典の寸法・overflow・下余白・文字条件の検査は弱めない。

## 日本語と字体

見出しは意味で改行し、値と単位・版番号を分断しない。架空の値や状態は記入例と明示する。日本語ノートには、数値の意味と読み手の次の行動を書く。

実例はBIZ UDPGothicのOFL原本をWebで配信し、PowerPointには同じ書体のインストールを前提とする。OSのフォントを抽出して再配布しない。別の書体へ変えた場合は全ページを再描画する。

## 再現

完成例ZIPではPython3の標準ライブラリとNode.js22以上・npmを使う。固定lockから依存と公式Chromiumを用意する。

```powershell
python source/reproduce.py --powerpoint --node "node.exeの絶対パス"
python -m http.server 8000 --bind 127.0.0.1
```

localhostのindex.htmlを開く。PowerPoint描画にはWindows / Microsoft PowerPoint / PowerShell7とBIZ UDPGothicが必要。新出力はレビュー待ちになり、前回のQAを引き継がない。

PptxGenJS4.0.1とPlaywright1.60.0を保ち、sharp0.35.5とimage-size2.0.3を固定した。元manifest・初期lock・監査・表示比較は完成例に保存する。原典MIT、字体OFL、依存の各通知を個別に読む。動画・音声・file URL・原典全機能・正式採用を検証済みとは扱わない。

## 単体の本文から使う

この本文は `skill-forks/presentation-delivery-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/ConnorRX56/presentation-delivery-skills/tree/06ddac077030c62f0118b225860cac46fbf658ea

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `presentation-delivery-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: ConnorRX56 / 原典条件: MIT原典 / OFL BIZ UDPGothic / 各Node依存の原文通知。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/LICENSE
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/LICENSE
