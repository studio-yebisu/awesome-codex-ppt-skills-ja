# 引き継ぎのnative図表と、PPTXから動くWeb資料へ

Sol 6.1の2並列で、原典の既定PptxGenJS経路による6枚の日本語PowerPointと、既存5枚のPPTXからのモーションHTMLを制作。親は自分の原稿とOSS書体から依頼文を組み立てる画面を担当した。Astra・独立レビューは使用していない。

## 実際に使った原典

| 原典・固定commit | 作例 | 制作工程 |
| --- | --- | --- |
| siril9/presentation-skill / efd899c5ddf866af2ce0001c4c9340af775d4d55 | 仕事の引き継ぎを、迷わない一枚に。6枚 | 原典outline JSON→render-plan・role-layout contract→既定PptxGenJS 4.0.1と原典nativeテンプレート |
| lanceli93/aws-html-slides / 5ae3d68b66277e8a0d0b6ceea479a4b5117f16b2 | 小さな展示を、ひとつの体験に。動く展示案内。5枚 | 原典PPT conversion extractor→入力OOXML形状の補助抽出→元Neon controller・viewport CSS・animationでHTML化 |

引き継ぎ資料はnativeの流れ、日程、表、比較を使う。原典の既定Node rendererを使い、Python doctorが指摘したデータ系パッケージの不足は本経路の依存へ読み替えていない。長い和文を止める原典guardには入力JSONの改行で対応。表見出しの和文欠けは局所font adapterでBIZ UDPGothicへ割り当て、同じ原典で再生成した。生成器を別の汎用rendererへ置き換えていない。

HTML変換は、前バッチのAkxan由来native PPTXを入力として原本保全。原典extract-pptx.pyを実行し、抽出テキスト・ノートに加えて、実OOXMLの円・四角・三角・線の位置、色、pathと字体をSVGへ補助変換した。原典のNeon controller、段階表示、edge animationを使う。gen-content.pyは原典で新規制作専用のため、この変換経路では実行していない。

新しいPPTXを作ったと表示せず、編集対象をHTML/SVG/CSSと案内する。原典PPTXと動くHTMLの間を、詳細とフロートの比較リンクで行き来できる。Web資料は字体を含めた単一HTMLでネット接続なしに開ける。SVGの文字位置がPowerPointと完全一致するとは表示しない。

どちらも原典MITを原文で保持。AWSの公式性や提携を持ち込まず、派生の表示をStudio Yebisuへ置換した差分を保存。変換入力のAkxan固定原典とMITも記録する。フォントは既存の公式配布TTFとOFLを再利用し、入力・依頼・原本・局所差分・再生成ソース・短い日本語SKILL・SOURCE・2種類のZIPを揃える。

## 別制作セッションの3件

| 原典・固定commit | 完成物と使用範囲 |
| --- | --- |
| vigorX777/ppt-svg-generator / c873b61673ab0ada5c09f863bff89c8f1b3248fb | AIに任せる前の設計図。7枚。原典Markdown→structure/design→作者SVGとSwiss preset、InkscapeのPDF出力。PDFは固定、SVGソースを編集可能。原典のPPTX変換は未実行 |
| NomiciAI/mbb-page-maker / 36074669b8041783d9637a87dfed2a8733d47357 | 動画一本を、教材へ。7枚。原典starter・CSS6層・図解部品とcontent router。navigationは自作へ差替え、完成HTMLを既存ChromiumでPNG/PDF化 |
| kimsh-1/deck-factory / 11d456351763b0efbc2a4989da688334f709dd9b | 音を、地図にする。7枚。原典CSSと13slotで作者HTMLを組み、ChromiumのPNG/PDFと既存Ghostscriptのlite PDFを制作 |

3件は届いた完成資料と制作原本を利用し、制作元を別セッションと表示する。原典export/QAの未実行、173の内側安全境界warningなどの範囲を保持し、既知の完成物を再生成していない。SVGのソース編集を「編集したいもの」の原稿絞り込みへ追加。Noto公式配布を各作例から取得できる。

178のroot LICENSEはApache-2.0、SKILL本文はMITと記載される。原文双方を保持し、rootのApache条件を配布へ残して、一括MITへ読み替えない。188と173はMIT。全件が架空・未実施で、実測や収益実績・音の再生機能を作例へ補完しない。

178の受領版はcloudのOS上にあったOFL Notoをsubsetしていたため、配布版は公式notofonts固定commitのOTFから作り直した。元OTFとOFL、公式由来subset、buildの変更、過去のcloud制作記録を保持する。使用326文字の輪郭・横幅・縦メトリクスが一致したため、既存PNG/PDFを再描画せず保持した。現行の字体とHTML埋め込みは公式配布由来で、以前の字体バイナリは配布しない。

## 自分の内容で使う入口

作例の詳細に、題材・原稿・読み手と目的・希望枚数の入力を追加。OSS書体の7セットから選んで、選択した作例の短いSKILL、固定原典、固有方式、作風、出力形式を含む依頼文へ組み立てる。生成後の依頼文は編集してコピーできる。入力は画面内でのみ使用し、保存・送信しない。

実際に作例を作った依頼文は折りたたみに保存し、新しい依頼文と混同しない。原典が必要とする論文・画像・PPTX等は別途添付する案内を入れる。原稿だけで画像復元やPPTX変換の前提を省略できるように表示しない。

## 確認と統合

制作担当は必要な原典生成と主要出力の初回表示だけを確認。既知の和文欠けを直した。親は新しい依頼文フォームで、原稿と書体を組み立て、コピーした本文へ固定原典・制作方法・書体が入ることを確認した。変換前後のフロート切替と最初のページ送りでは、親とiframeの双方が2/5へ進むことも確認。取り込み担当から3件のページ移動・親子同期と取得参照の確認報告を受け、親では繰り返していない。全ページ詳細目視、独立採点、native構造監査、全ZIP再実行は追加していない。

現在は厳選49スキル・49冊286枚、54件の作例別recipe、51種類の直接Markdown。制作履歴は59リポ・64冊387枚、61の維持forkと200の取得ファイル。書体は9ファミリー16ファイル・7セット。全体の制作は継続中。元209件は資料として保持する。公開push・main merge・deployは行っていない。

画面: [原稿から依頼文を作る](assets/atelier-request-composer.png) · [PPTXから動くHTMLへ](assets/atelier-pptx-to-motion.png)。最小確認の記録は [atelier-light-check](../data/atelier-light-check-20261014-08.json)。
