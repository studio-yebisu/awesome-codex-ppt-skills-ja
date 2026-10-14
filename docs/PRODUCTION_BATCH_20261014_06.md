# 数式を編集する教材と、テンプレートを使う研究発表

Sol 6.1の並列制作で、原典2リポから日本語PowerPoint2冊・11枚を完成し、サイトへ接続した。Astraは使っていない。公開push・main merge・deployは行っていない。

| 原典・固定commit | 完成物 | 実際に使った方式 |
| --- | --- | --- |
| Noi1r/powerpoint-skill / a39cd8cfba332741a96d52bebd2bb378b638364e | 平均の、その先。5枚 | Sandwichテーマと原典helpers、render_latex.pyのmanifest、inject_omml.pyのPandoc→DOCX→OMML注入 |
| zouchenzhen/thesis-defense-pptx-skill / 7cf83b6fe264410aec39ab73d8cfa48f1c9a73bb | 雨の日の、通学ルート。6枚 | 原典build_template.py、COMのDuplicate/MoveTo、Markdown parserとreplace/add_text/rect/write_table |

## 編集できる範囲と入力

数式教材は原典処理で9個のOMML数式を注入。文字・図形・グラフ・表・数式をPowerPointで編集できる。A=[4,5,6]、B=[0,5,10]という学習用の仮想データで、同じ平均と異なる散らばりを説明する。分散の分母は全3件を全体としてn。実測した調査ではない。

研究発表は原典の無地テンプレートを1,2,3,4,4,3の順で複製し、文字・経路図・表をnative要素で配置した。原典のgeometry・濃赤・文字サイズを維持し、日本語書体のみ対応。経路と時間は自作の仮想設定で、雨にさらされる時間を加味する評価式の試算として表示する。

両方に完成PPTX、PDF、PNG、入力、依頼文、再生成コード、原典の未変更原本と必要な差分、短い日本語SKILL、原文条件、制作一式とスキル一式のZIPを用意した。サイトの主ダウンロードはPPTX本体で、制作ソースZIPは作り方から取得する。

## 書体と原典条件

数式教材はShippori明朝・BIZ UDPGothic・Manrope、研究発表はBIZ本文・Shippori見出しを役割別に使った。書体アトリエの8ファミリー14ファイル・6セットも維持し、AIへコピーする書体と日本語改行の指示につながる。

Noi1rの原典はMIT、研究発表の原典はApache-2.0でLICENSEとNOTICEを保持。使用した公式TTFとOFLをキットへ同梱する。数式注入に使った公式Pandoc 3.12.1はGPL-2.0-or-laterの別取得runtimeとして案内し、runtime binaryをキットへ入れていない。Officeの書体やXSLファイルを抽出・再配布していない。

PowerPointの共有インスタンスにApplication.Quitを呼ばず、自分のデッキだけを閉じる局所対応を記録した。

## サイトへの接続と軽い確認

一覧へ「編集したいもの」を追加。「文字・図形」「数式」「画像・ノート」「Web・TeXの原稿」で選べる。作例の編集範囲を小さい説明として表示し、数式教材と研究発表のフロートにも実際の範囲を記す。過去の画像スライドを文字編集可能とは扱わない。

制作担当が原典の生成工程とPowerPoint 16によるPNG/PDF出力、代表完成ページの初回表示を確認。親は新しい数式フィルターが1冊5枚に絞られ、フロートの3/5ページに式と図表が表示され、PPTX本体へのリンクが出ることを確認した。JS構文確認と通常のmanifest・サイト生成を行った。全ページ詳細目視、独立レビュー、構造監査、全ZIP再実行を追加していない。

現在は厳選38スキル・38冊214枚。43件の作例別recipe、40種類の直接Markdownを接続。制作履歴は48リポ・53冊315枚、50の維持forkと164の取得ファイル。元209件の記録は保存している。全体の制作目標は継続中。

画面: [数式教材のフロート](assets/atelier-native-math-float.png)。
