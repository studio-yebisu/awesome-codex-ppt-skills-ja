---
name: presentation-delivery-ja
description: HTML deckを正本として視覚構成を作り、概覧とページ操作で読む。PPTXは必要な場合だけ4条件の範囲で派生し、内容と表示の違いを検査する。
---

## このスキルでできること

画面で読むHTML資料を先に作り、必要なときだけ本文や図形を編集できるPPTXも出せる。

- 困っている状況: HTMLの見た目だけを確認しても、相手が編集するPPTXの仕上がりは分からない。
- 必要な入力: 資料の目的・読み手・原稿やデータ、頁の役割と配色・文字・図の指定。
- 受け取るもの: 正本のHTML資料とPDF。依頼がある場合だけ、変換できる範囲を明示したPPTX派生も作る。
- 必要環境: Python、Node22以上、固定Node依存とChromium。 / PPTX確認にはWindows / PowerPoint / PowerShellと公式BIZ UDPGothic。PDF由来RGBプレビューにはpypdfium2。
- 作例で試した範囲: 原典のHTML-first Path Aで6頁を作り、4条件に合う要素を元DOM変換器でPPTXへ派生。HTMLとPPTXを並べて内容と表示差を確認する。


# HTMLを正本にして資料を作る

原典はHTMLで高精細なプロトタイプ・スライド・アニメーション・可視化を制作する。スライドはHTML deckを正本にPDFを出し、依頼がある場合だけPPTXをbest-effort派生として出す。

原典のHTML-first Path Aで6頁を作り、4条件に合う要素を元DOM変換器でPPTXへ派生。HTMLとPPTXを並べて内容と表示差を確認する。

原典は [ConnorRX56/presentation-delivery-skills](https://github.com/ConnorRX56/presentation-delivery-skills/tree/06ddac077030c62f0118b225860cac46fbf658ea)、固定 commit `06ddac077030c62f0118b225860cac46fbf658ea`。日本語派生であり公式翻訳ではない。

## 用意するもの

- Python、Node22以上、固定Node依存とChromium。
- PPTX確認にはWindows / PowerPoint / PowerShellと公式BIZ UDPGothic。PDF由来RGBプレビューにはpypdfium2。

## 使い方

1. 読者・題材・資料の役割と出力形式を確認する。
2. HTML正本の見本と書式を確認してから残りを作る。
3. 必要な場合だけ4条件に合わせてPPTXを派生する。
4. HTMLとPPTXの実表示と内容を比較し、変換損失を明記する。

## この作例で確認する箇所

- **2頁・HTMLからの派生**：左のHTMLと右のPowerPointを比べ、3項目の本文が一段落の通常行間で読めるか確認。 4条件内のp/h要素を変換し、複数行の段落は外側DIVのdata-pptx-mergeで同じ編集枠へまとめる。
- **3頁・内容に合う図示**：上の例を用途・版・状態の3行へ分けたHTMLとPPTXを比較する。元の3列骨格を繰り返さない。 HTMLの視覚構成を正本にし、頁の役割へ図示を合わせる。対応する図形と本文を派生PPTXにも残す。
- **4頁・正本と派生を照合**：暗色の背景と2欄、本文の意味が両方で残るか確認。字幅や太さのpixel一致は主張しない。 HTMLを先に完成し、変換で保持できる内容と表現を確認する。PPTXはbest-effortとして損失を記録する。

## 適用範囲と未実施

- 原典visual-deck-studioはHTMLを正本とし、PPTXは依頼時のbest-effort派生。PPTXの制約のためにHTML設計を下げない。
- 今回の自律制作では早期の利用者承認と3方向Fallbackを実施していない。2頁showcaseは保持するが利用者の選択済みとは扱わない。
- HTTP入口・字体待ち・日本語ノート・Windows環境継承を局所adapterで補う。原典の寸法・overflow検査は維持。
- file URL、動画、音声/TTS、生産用Webアプリ・バックエンドはこの例の対象外。
- HTML全6頁の寸法・overflow・字体と、PPTX本文・全頁の実画像を確認。pixel一致・利用者採用・独立再評価は未完了。

全頁を制作側が実画像で確認した。修復版の独立再評価・利用者の採用は未完了。検査の内容・現在のPPTX hashは `QA.json`、原典の保持範囲と変更は `PROVENANCE.json` を参照する。

入力と現在の生成器を含む。再実行は [example/REPRODUCE.md](example/REPRODUCE.md) を参照する。

## 単体の本文から使う

この本文は `skill-forks/presentation-delivery-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/ConnorRX56/presentation-delivery-skills/tree/06ddac077030c62f0118b225860cac46fbf658ea

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `presentation-delivery-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: ConnorRX56 / 原典条件: MIT原典 / OFL BIZ UDPGothic / 各Node依存の原文通知。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/LICENSE
- https://github.com/ConnorRX56/presentation-delivery-skills/blob/06ddac077030c62f0118b225860cac46fbf658ea/skills/visual-deck-studio/LICENSE
