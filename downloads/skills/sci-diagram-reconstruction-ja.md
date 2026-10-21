---
name: sci-diagram-reconstruction-ja
description: 科学模式図の画像を、元の文言・包含・方向を保つ編集可能なPowerPointへ復元する。既存科学図PPTXの修復・変更しない検査は別経路。統計グラフ、一般業務図、組織図、通常のデッキ制作、OCRのみ、画像貼付のみには使わない。
---

## このスキルでできること

画像にまとまった科学模式図を、元の文言・包含・方向を保つ編集可能な文字・図形・線へ分ける。

- 困っている状況: 科学図を画像で貼ると、ラベル・領域・矢印を個別に直せない。
- 必要な入力: 復元する科学模式図の画像、または修復・検査するPPTXと対象箇所。文字と方向を判読できる資料。
- 受け取るもの: 復元では編集可能なPPTXと実行用ソース。修復では変更したPPTX、検査では元のPPTXを変更しない検査結果。
- 必要環境: 復元用の模式図画像、または修復・検査するPPTXと対象箇所。文字と関係を読める資料。 / PptxGenJS経路は準備済みNode.js20+、PptxGenJS4.0.x。原典の検査・表示にはPython3.10+、LibreOffice、pdftoppm。本例のR13実測はNode24.19.0/PptxGenJS4.0.1/Python3.13.7/LibreOffice24.2.5.2。 / --renderのPowerPoint工程と編集保存の確認はWindows PowerPoint16、Yu Gothic、PATH上のPowerShell7（pwsh）。R13実測PowerShell7.6.6。依存・書体の新規導入は今回未検査。
- 作例で試した範囲: 入れ子・双方向・破線をnative部品へ復元し、合成画像小図だけをrasterに分ける。Xだけの保存編集と3ファイル再生を実証。単純4箱は最小方向保持の補足。


# 科学模式図を、文字と関係を編集できるPPTXへ復元する

元の編集ファイルがなくても、科学模式図の文言・包含・矢印の方向を保ち、文字・図形・線を個別に修正できる状態へ復元する。既存PPTXの修復と、変更しない検査は別経路で扱う。

原典は[HututuWorks/sci-diagram-pptx固定cc8f0030](https://github.com/HututuWorks/sci-diagram-pptx/tree/cc8f0030edf80eeab6e52849b8c39fe638466776)。Apache-2.0の非公式日本語派生。原典SKILL・参照文書・checkerはupstream/に未改変で保持する。

## 入力と出力

入力は判読できる科学模式図の画像、または修復・検査するPPTXと対象箇所。復元では図1点から編集可能なPPTX1枚と実行ソースを渡す。修復では変更したPPTX、検査では元PPTXを変更しない結果を返す。

## 自分の資料で使う

1. 科学模式図の画像からの復元、既存PPTXの修復、変更しない検査を選び、原典SKILLと該当する参照文書を読む。
2. 元の解像度で文言・包含・関係の方向を読み、NODES/EDGES/INSETSへ所有を一つずつ割り当てる。混在書体や式があればmath-and-fonts.mdも確認する。
3. 利用可能なruntimeを一つ選び、準備済みホスト配下でprobeする。PptxGenJS復元では新しいpass-01にsource.pngとbuild.mjsを置き、欠けた依存を制作中に導入しない。
4. 原典checkerへ実際のsource.pngとbuild.mjsを渡し、元図と実表示の文言・包含・方向・欠落を照合する。原典標準は最大2passで、全blockerをまとめて一度だけ直す。
5. PptxGenJSによる復元ではbuild.mjs・元画像・PPTXの3ファイルと検査結果を渡す。修復・検査は各経路の成果物を返す。必要な編集は別コピーで保存・再表示し、元の意味や方向を変えない。

科学的意味、文言・式、包含・順序・方向を見た目の都合で書き換えない。重要部分をrasterにする代替や意味の変更が必要なら判断を求める。原典の適用対象外は統計グラフ、一般業務図、組織図、通常のデッキ制作、OCRのみ、全面画像の貼り付けのみ。詳細は[START-HERE.ja.md](START-HERE.ja.md)。

## 主な効果を確認する複合例

[入力PNG](example/complex-example/input/source.png)の入れ子2区画、可逆交換の両端矢じり、条件u→区画Bの破線終端を[PowerPoint表示](example/complex-example/render-pass04/powerpoint.png)と比べる。23個のnative図形（文字12個を含む）とcroppingした画像小図1個へ所有を分けた。[PPTX](example/complex-example/pass-04/editable.pptx)では文字と線を個別に編集できる。小図内部はrasterで、外側見出しと二重描画しない。

[別コピー](example/complex-example/qa/current-nativeedit/edited-copy.pptx)ではXだけをX*へ変更し、PowerPointで保存・再表示した。図全体の画像置換ではない。包含は座標対応でありPowerPointのグループではなく、線は箱移動へ自動追従しない。描画順をplates→edgesへ変えたのは、この入力で塗りのある親領域が線を隠さないための作例判断。原典雛形の既定edges→insets→plates/labelsと区別する。

## 補足：最小の方向保持と編集

水循環の[入力](example/input/source.png)から4箱・4方向を保持した[PPTX](example/pass-01/editable.pptx)を作った。原典checkerのconnector 0はp:cxnSpがないという意味で、4本の標準線は幅または高さが0のため集計対象外。別の[XML検査](example/qa/native-line-topology.json)で線と矢じり・方向を確認した。[文字変更](example/qa/editability/native-label-edited.png)と[箱・線の変更](example/qa/editability/native-shapes-edited.png)は別コピーの保存・再表示で確かめた。単純例の矢じりは元図よりやや小さい。

## 現行と履歴

初稿コードと対応表は実Claude Opus5.5が原典4文書とPNGを読んで作成した。実行はCodex。標準制作はCodexがFONTだけをYu Gothicへ直したpass02で終了した。その後の明示された継続改善で、Codexが元SVGの角丸とnative矢じりを調整したpass04を作成した。原典既定の最大2passを変更したり、追加改善を元のpass02と表示したりしない。個別ページの人間承認を取得したという記録ではない。

現在のpass04/build.mjsは、生成時に矢じり3個をlg/lgへ補正する処理まで内包する。保存例のbuild.mjs・source.png・editable.pptxだけで準備済みruntimeに再生でき、Pythonの矢じりhelperを必要としない。原典checkerの--pass-index省略はこの保存PPTXの構造検査であり、追加passの承認証明ではない。[現在の自己完結検査](example/complex-example/qa/self-contained-handoff-r13.json)と[旧引き渡しの履歴](example/complex-example/history/pre-r13/README.md)を分けて残す。

## 検査と制約

- 掲載した2例は自作PNGのReconstruction。既存PPTXのRepairとInspection、数式、実験写真の復元は未実施。PptxGenJSで既存PPTXを保ったRepairは行わない。
- 主な効果の証拠は複合例の入れ子・双方向線・破線の折れ線・合成画像insetの所有分離。単純4箱の例は原文と最小方向保持の補足。PowerPointのグループ化、線同士の交差、箱移動への自動追従は未実証。
- 単純例の原典checkerはhard failure 0・warning 0。複合例はhard failure 0・warning 1で、12文字枠wrap=noneのrenderer間reflow警告が残る。PowerPoint16とLibreOfficeの実表示を制作担当が確認した。
- 小図内部はrasterで「参考パネル」は文字編集できない。srcRectでcrop元PNGを表示するため、不可視部分の削除や情報秘匿は保証しない。
- 複合例pass04の角丸と3個のlg/lg矢じりを保持。現在のbuild.mjsは矢じり補正まで自己完結する。生成した非ZIP64・STORE形式PPTXだけを扱う局所処理で、汎用PPTX変換器ではない。
- 原典既定の最大2passは変更しない。標準制作はpass02で終了した履歴を残し、明示された継続改善によるpass04と区別する。checkerのpass-index省略は構造検査の指定で、pass04の承認証明ではない。
- Yu GothicはWindows同梱の字体を参照し、字体ファイルは配布しない。別環境は対応字体が必要。依存や字体の新規installは検査していない。入力との画素一致、見た目の改善、時短は主張しない。

原典checker、構造検査、制作担当の実表示確認、独立モデル評価は別の工程。現在の変更へ過去の独立点数を引き継がない。

## 保存例を再生する

作例ZIPは展開root、日本語スキルZIPはexample/をCWDにし、採用版と別のコピーで[REPRODUCE.md](REPRODUCE.md)を実行する。作業フォルダーの祖先から既存PptxGenJSを解決できるようにする。依存や字体を同梱・新規installしない。

```powershell
python source/reproduce_complex.py --overwrite --render --node <既存Node.js実体> --soffice <既存soffice> --pdftoppm <既存pdftoppm>
```

R13の実測はNode24.19.0、PptxGenJS4.0.1、Python3.13.7、LibreOffice24.2.5.2、PowerPoint16、PowerShell7.6.6。--renderはWindowsのPowerPointとPATH上のpwsh（PowerShell7）を使う。元のNode24.18による実行記録は履歴として保持する。PowerPoint全体を終了せず、自分が開いたpresentationだけを閉じる。

## この方式で気をつけること

- 掲載効果の主証拠は複合例。単純例の4箱・4方向は最小復元と文字・箱・線の編集を確かめる補足。
- 初稿のコードと対応表は実Claude Opus5.5。標準制作pass02のFONT修正、継続改善pass04の角丸・矢じりと現在の自己完結化、実行・検査はCodex。
- 複合例の標準2pass終了と追加改善pass04、R13の保存プログラムの引き渡し修正は異なる工程。--pass-index Noneを追加改善の承認証拠にしない。
- 現在のpass04/build.mjsに矢じり補正を内包し、準備済みruntimeでbuild.mjs/source.png/editable.pptxの3ファイルだけを再生。旧Python補正と旧profileのpass02終端・角丸近似は履歴で、現在の仕様ではない。

## 単体の本文から使う

この本文は `skill-forks/sci-diagram-reconstruction-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/HututuWorks/sci-diagram-pptx/tree/cc8f0030edf80eeab6e52849b8c39fe638466776

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sci-diagram-reconstruction-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: HututuWorks / 原典条件: Apache-2.0。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/LICENSE
- https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/skills/sci-diagram-pptx/LICENSE
