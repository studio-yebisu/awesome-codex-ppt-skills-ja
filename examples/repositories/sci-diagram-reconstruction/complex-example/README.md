# 入れ子・双方向・破線・画像小図を含む復元例

編集元がない科学模式図でも、文字と関係を後から直せるPPTXへ復元する例。外側の領域、内側の2区画、記号をnative図形へ分け、双方向の実線と条件から区画へ向かう破線の意味を保持した。実験結果ではない自作の概念図を入力にしている。

- [入力PNG](input/source.png) / [入力の自作SVG](authored-source.svg)
- [編集できるPPTX](pass-04/editable.pptx) / [PowerPoint表示](render-pass04/powerpoint.png) / [PDF](render-pass04/powerpoint.pdf) / [LibreOffice表示](render-pass04/libreoffice.png)
- [所有対応表](ownership.json) / [実行コード](pass-04/build.mjs) / [来歴](PROVENANCE.json)

## 編集できる部分と画像として残す部分

23個のnative図形（うち文字12個）と、croppingした画像小図1個。包含は座標と親子対応で検証するが、PowerPointのグループ化ではない。可逆交換は両端に矢じりのある1本の線、条件uから区画Bへの調整は3本の破線の折れ線で、到着側だけに矢じりを置く。線は個別編集でき、箱の移動に自動追従する接続リンクはない。

右の小図は元PNGの該当範囲を`srcRect`で表示する。内部のグラデーション・円・「参考パネル」の文字はrasterのまま。小図の外枠と外側の「局所像（合成入力）」見出しはnativeで、内部要素を重ねて二重描画しない。PPTX内にはcrop元のPNGが入るため、不可視部分の削除や情報秘匿を保証する方式ではない。

[構造確認](qa/native-structure-pass04.json)では、文字数、両端矢じり、3破線と終端矢じり、crop範囲を確認した。[文字編集の別コピー](qa/current-nativeedit/edited-copy.pptx)では、PowerPoint16で`X`だけを`X*`へ変更しSaveCopyAsで保存、[描画](qa/current-nativeedit/edited-copy.png)と[記録](qa/current-nativeedit/edit-proof.json)を残した。採用版は不変。

## 原典既定2passと追加のauthor pass4

初稿の`pass-01/build.mjs`と対応表は実Claude Opus5.5が原典4文書と入力PNGを読んで作成。実行と描画はCodexが担当した。初回PowerPoint表示で太字階層とラベルの可読性に問題があり、Codexがpass-02でFONT定数だけを`Noto Sans JP`から既存の`Yu Gothic`へ修正した。配置・線の関係・cropは変えていない。原典の最大2passに従い、当時はこのpass-02で終了した。旧版のPPTXと実表示を履歴として保持する。

初稿の[checker記録](qa/check-pass-01.json)、[PowerPoint表示](qa/pass-01-render/powerpoint.png)、[LibreOffice表示](qa/pass-01-render/libreoffice.png)と[修正判断](qa/pass-01-evidence.json)を保持した。checkerの警告そのものをblockerとは扱わず、実表示で太字階層が失われた箇所を修正理由にした。pass-02のコード冒頭のpass-01コメントは初稿から保持しており、実行したpassはフォルダーと来歴で区別する。

その後の明示された追加改善で、Codexがpass-04を作成した。変更は元SVGのrx16/12/46に対応する角丸値と、native矢じりサイズのみ。途中のpass03は追加JSZip直接importが原典portability検査に不適合で不採用とし、実装を配布しない。原典標準は最大2passのまま、今回は追加author pass4として記録する。checkerの--pass-indexは1/2のみなので省略し、4を2と表示しない。[幾何と編集の記録](qa/geometry-and-edit-pass04.json)に差分と採用原本不変を記録した。

原典checkerはhard failure 0・warning 1、判断はcomplete。警告は12個の文字枠が`wrap=none`であり、他rendererで文字がreflowする可能性を示す。PowerPoint16とLibreOffice24.2.5.2の実表示を制作担当が確認した。独立評価や新しい環境での表示保証とは分ける。初稿作者はmath-and-fonts.mdを未読、書体修正時にCodexが確認した。

## 保存例の再生

作例ZIPは展開root、日本語スキルZIPは`example/`をCWDにする。Windowsでは短い展開先を使う。準備済みホストruntimeの`node_modules`を祖先から解決できる場所に展開し、下記を**採用版とは別のコピー**で実行する。依存・字体ファイルは同梱せず、新規導入もしない。

```powershell
python source/reproduce_complex.py --overwrite --render --node <既存Node.js実体> --soffice <既存soffice> --pdftoppm <既存pdftoppm>
```

LibreOfficeの一時profileはOS一時フォルダーへ置き、完了PDF/PNGをcaseのqaへコピーして保持する。原典probe→自己完結した同じpass-04のbuild→原典checker（--pass-index省略）→例固有の構造確認→原典の隔離LibreOffice renderer→PowerPoint PDF→PNGの順。再生は保存したpass-04実装の実行で、新たなauthor passを制作しない。必要環境はNode20+・PptxGenJS4.0.x・Python3.10+・LibreOffice・pdftoppm。現在のR13再生実測はNode24.19.0/PptxGenJS4.0.1/Python3.13.7/LibreOffice24.2.5.2/PowerPoint16。Node24.18の旧実行記録は履歴。--renderはWindows PowerPoint16とYu Gothic、PATH上のpwsh（PowerShell7）が必要。今回の実測はPowerShell7.6.6。PowerPoint全体は終了せず、処理が開いたpresentationだけを閉じる。

## 制約と条件

- 数式、実験写真、既存PPTXのRepair/Inspection、線同士の交差、自動接続は未実証。小図は合成画像で、実験画像の忠実復元を示さない。
- pass-04は元SVGのrx値をroundRectのrectRadiusへ反映し、X/X·Rの丸みを保持した。PptxGenJS4.0.1の使用APIで指定できない矢じりサイズは、現在のbuild.mjs内で生成PPTXの3個のtriangle headのw/lenをlg/lgへ補正する。旧Python helperは履歴で、現在の再生では呼ばない。破線パターン、色・線幅・字体の細部は画素単位の一致ではない。
- 任意の画像を受け取る自動変換器、科学的正しさの判定、見た目の改善や時短の比較ではない。
- 原典は[HututuWorks/sci-diagram-pptx固定cc8f0030](https://github.com/HututuWorks/sci-diagram-pptx/tree/cc8f0030edf80eeab6e52849b8c39fe638466776)、Apache-2.0。PptxGenJSはMIT。入力はStudio Yebisuの自作CC0-1.0概念図。Yu GothicはWindows同梱の字体を参照するだけで再配布しない。


## R13：3ファイルの自己完結した引き渡し

形と内容を変えず、追加改善pass04の保存プログラムを整理した。build.mjs内の補正はPptxGenJSが生成した非ZIP64・非圧縮STORE形式だけに限定する。fsとBufferでCRC・central offset・entry数を検証し、slide1.xmlの矢じり3個だけを変更する。node:zlibやJSZipの追加import、Python補正は使わない。異なる形式は推測して変換せず失敗させる。原典checkerは未改変。

[自己完結検査](qa/self-contained-handoff-r13.json)に、独立した3ファイル再生、原典checker H0/W1、ZIPの負制御、native構造、PowerPoint/LibreOfficeの旧採用表示とのRGB差0を記録した。生成日時を除く40の部品は旧採用版と同一。現在のX→X*編集コピーは改めて保存・再表示した。[R13以前の所有対応・build・検査](history/pre-r13/README.md)は当時の記録として保持する。

描画順plates→edgesは塗りのある入れ子領域が線を隠さないための作例判断で、原典の既定edges→insets→plates/labelsを一般に置き換える規則ではない。標準2pass終了後の追加改善は継続依頼の範囲で行ったもので、個別ページの人間承認やchecker pass-indexによる承認を示さない。
