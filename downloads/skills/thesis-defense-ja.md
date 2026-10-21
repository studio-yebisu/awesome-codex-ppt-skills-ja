---
name: thesis-defense-ja
description: 論文と図表を発表用に整理し、既存PPTXの書式を保った編集可能な研究発表を作る。
---

## このスキルでできること

研究メモを発表用の順へ整理し、元テンプレートの枠を保った図・表・比較を編集できるPPTXへ入れる。

- 困っている状況: 論文を要約するだけでは、指定テンプレートの書式や研究の根拠が保たれない。
- 必要な入力: 論文PDF・LaTeX・研究原稿と、使いたいPPTXテンプレート。使用できる図表・コード・比較条件・数値。
- 受け取るもの: 論文の問題・方法・比較・限界を整理し、元テンプレートの書式を保った編集可能なPPTXと検査記録。
- 必要環境: Python3.10以上と原典requirements。 / WindowsとPowerPointではCOM複製・描画・はみ出し検査。macOS/Linuxはpython-pptx部分のみでCOM検査を省略。 / 同梱例の全再実行はWindows PowerPointとPowerShell。字体は同梱TTF/OFLで別途導入。
- 作例で試した範囲: 通学経路の仮想研究6頁。元templateの濃赤navとcontent frameを保ち、JSONから経路図・露出比較・試算表を追加した。全6頁目視、overflow0、古い文言0。
- 制約: この作例は自作Markdownと学習用仮想データ。大学の実研究や観測値ではない。 / 元の無地templateを使用。実在大学templateやロゴは含まない。 / 6枚指定を優先。共有PowerPoint保全のためCOMのQuitだけを抑止し、検査内容・閾値は変更しない。


# 論文とテンプレートから研究発表を作る

論文PDF・LaTeX・原稿と、使いたいPPTXテンプレートを渡す。研究の問題・方法・比較・限界を発表用に整理し、元の配色・文字の階層・ナビゲーションを保った、編集可能なPPTXを受け取る。

原典はzouchenzhen/thesis-defense-pptx-skill、固定commit `7cf83b6fe264410aec39ab73d8cfa48f1c9a73bb`。Apache-2.0のLICENSEとNOTICE、未変更の原文を保持した非公式日本語版。

## 使い方

1. 論文・コード・表・図の説明を読み、問題、方法、比較条件、結果、限界を整理する。元資料があるのに題名だけから作らない。
2. LaTeXのincludegraphicsと説明、論文内の図、使用を許可された素材から図の使用一覧を作る。テンプレートに残る写真や古い図を勝手に流用しない。
3. 元PPTXを描画し、表紙・目次・ナビ・本文・結果・結びの書式と文字サイズを確認する。必要な枚数と順で、元の編集可能な頁を複製する。
4. 文字・図表を原典の置換・表・画像の部品操作で入れる。本文は短くし、まず元テンプレートの大きな枠や頁分割で収める。
5. 全頁を描画し、一覧と危険箇所を読む。文字のはみ出し、古い文言、出典、頁順とナビ、図の縦横比を確認し、修正後は再検査する。自動検査だけで見た目を合格にしない。

## 環境

Python3.10以上と原典requirementsを使う。WindowsとPowerPointでは、原典のCOM操作で複製・PNG書き出し・はみ出し検査を行う。macOS/Linuxではpython-pptxの処理だけを使い、COMの検査は省略される。今回の同梱rebuild.pyはWindows PowerPointの経路を実行する作例で、他OSでの全工程は未検証。

## 同梱する作例の範囲

自作の研究メモとJSONから、架空の通学経路を比べる6頁を作った。原典の無地テンプレート生成・COM複製・文字置換・表操作を使用し、日本語字体をBIZ UDPGothic/Shippori Minchoへ変更した。6頁はこの作例の指定で、一般の固定枚数ではない。

3頁は各辺の「移動時間t / 露出時間e」を元JSONと同じ値で表示する。Bの名称はアーケード。4頁の合計14/3/16分は図の各辺から足せる。6頁は仮定と次に測ることを分け、実測していないと明記する。

論文PDF/LaTeXからの抽出と、実在する大学のテンプレート保持は、この作例では試していない。地点・時間・計算結果は学習用の設定で、観測や実在経路の案内ではない。書体は未埋込みで、未改変TTFとOFLを同梱する。共有PowerPointは終了せず、開いた作例だけを閉じる。

再実行はexample/REPRODUCE.md、現在の検査はexample/QA.jsonとexample/reviews/。制作側の確認、独立評価、利用者の採用は別の状態として扱う。

## 単体の本文から使う

この本文は `skill-forks/thesis-defense-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/zouchenzhen/thesis-defense-pptx-skill/tree/7cf83b6fe264410aec39ab73d8cfa48f1c9a73bb

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `thesis-defense-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: zouchenzhen / 原典条件: Apache-2.0。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/zouchenzhen/thesis-defense-pptx-skill/blob/7cf83b6fe264410aec39ab73d8cfa48f1c9a73bb/LICENSE
- https://github.com/zouchenzhen/thesis-defense-pptx-skill/blob/7cf83b6fe264410aec39ab73d8cfa48f1c9a73bb/NOTICE
