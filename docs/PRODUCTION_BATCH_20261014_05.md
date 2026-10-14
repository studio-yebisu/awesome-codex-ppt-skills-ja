# 日本語教材・数式・花の企画書とOSS書体

Sol 6.1の並列制作で原典3リポの日本語新作16枚を完成。別制作セッションの原典2リポ19枚を取り込み、原典方式・編集範囲・制作環境を保持してサイトへ接続した。公開push・main merge・deployは行っていない。全体の制作は継続中。

## このPCでの新作

| 原典・固定commit | 完成物 | 実際に使った方式 |
| --- | --- | --- |
| chunyifish/soil-teaching-slides / ebeb43ce0e4360ba2ffc91dcfb4be5ba203bb09f | 割合は、全体との比べ方。6枚 | Mode Cの1600×900 stage、HTML template、render/advance/retreat/fragmentを日本語の割合教材へ拡張 |
| xukp20/build-beamer-slides / e63b61b140a00596e5260ec7611e42bfde7efb5f | 待ち時間のしくみ。PDF5枚と編集用.tex | Warm Editorialの原典template/theme/TikZと数式、公式Tectonic 0.17.0でコンパイル |
| LearnAIHubC/LearnDeck / d5ea12ca88f9a87edaf20b6bb48847790baed698 | 花を、一本から。編集可能PPTX5枚 | 原典HTML-to-PPT aliasとDOM converterを--no-previewで実行。CSS書体の保持と日本語を局所対応 |

SOILにはBIZ UDPGothic、花の企画書にはDela/Shippori/BIZの役割別指定を使用。LearnDeckの文字・基本図形はネイティブ、花は原典変換器の個別PNG画像で、元SVGも保存。BeamerはPDF/.tex専用で、PPTXを生成したとは表示しない。欧文書体が未登録だったため同じ公式TeX Gyreファイルを明示するパスへ原典themeの1行だけ変更し、未変更原本も同梱した。

各作例に完成資料、PNG、入力、依頼文、原典runtime/source、短い日本語SKILL、個別条件、原典・制作のZIPを揃えた。

## 別制作セッションの取り込み

| 原典 | 完成物と保持する範囲 |
| --- | --- |
| MURMURE11118586/codex-xkppt-skill / 978b46d116fd8fd971f9cd963f745da62f7f1f26 | 原典native生成器の8枚PPTX。SDKによる完成PPTX描画PNG。文字・図形編集可、表紙挿絵は画像。原典美術QA80.7点FAILを保持し、85点qualifiedやPowerPoint実機確認と表示しない |
| demoolight/academic-image-ppt / 2aac1a711ff658ab67d79a0e98cc54b5a0468751 | 原典imagegen方式の11枚をノート付き原典包装器でPPTX化。本文・図は画像。画像差替えと話者ノート編集可、PowerPoint実機確認なし |

原制作物を再生成せず、配布ZIPを独立forkへ展開し短い日本語本文と出所を接続。SDKの実装は同梱されていない。PNGプレビューを実機描画と混同しない。元QAを上書きしない。

## フォントと使い方

Google Fonts固定commit 66928797f271fed5ee428544e7229685e2d90127 のBIZ UDPGothic/BIZ UDPMincho、Regular/Bold各2ファイルとOFL原文を追加。既存公式字体は再取得せず保持した。書体アトリエは8ファミリー14ファイル、6セット。「業務と数字」「説明と教材」を追加し、見出し・本文・英数字と日本語改行の指示をAIへコピーできる。全14ファイルをWindowsユーザー環境へ登録した。

SOIL原典NOTICEのsoftware=MIT、content=CC BY-NC-SA 4.0を個別に保持。LICENSE-CONTENTの原文と出所を監査記録へ補足し、本文取得前とフロート画面へ日本語の非商用・帰属・継承条件を表示した。独自の教材出力が自動的に同条件になるとは解釈しない。Beamerに同梱する欧文書体はGFL/LPPL原文を保持する。

## サイトと確認範囲

厳選36スキル・36冊203枚。作例の依頼文と41件のcase recipe、38種類の直接Markdownを接続。制作履歴は46リポ・51冊304枚で、旧209件カタログを保持している。少数の新作バッチを全体完了とは扱わない。

PDFの形式フィルター・表示・取得を追加。SDK描画PNGと画像ページをフロート内でページ送りできるようにし、描画方法と編集範囲の説明を保持。原典URLのsource_refsもリンク先として正しく扱う。

制作担当は原典の生成・必要なビルドと代表出力の初回表示を確認。親はBIZセットの切替・コピー表示、SOILの1→2枚目と図の表示、PDFフィルターと1→2枚目、花のPowerPoint表紙のフロート表示を確認した。取り込み2件のPNGページ送りは取り込み担当セッションの確認を受領し、重複検査していない。全ページの詳細目視、独立レビュー、全ZIP再実行、構造監査は追加していない。

8847の旧サーバーは停止していた。Start-Processによるバックグラウンド起動は自動承認審査にblocked by policyで拒否された。端末の管理下で127.0.0.1へbindする通常のhttp.serverコマンドは実行でき、実際のブラウザー表示へ接続した。秘密情報・権限・ファイアウォールの変更はない。

画像: docs/assets/atelier-flower-float.jpg、docs/assets/atelier-biz-fonts.jpg。
