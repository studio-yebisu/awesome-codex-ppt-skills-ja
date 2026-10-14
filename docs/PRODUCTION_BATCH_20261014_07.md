# Bauhausの版式、AI画像からの復元、研究資料とNoto CJK

Sol 6.1の2並列で原典2リポの日本語新作8枚を完成。別制作セッションの原典4リポ32枚を取り込み、原典方式・制作環境・編集範囲を保持してサイトへ接続した。Astraと独立レビューを使っていない。公開push・main merge・deployは行っていない。全体の制作は継続中。

## このPCで実行した原典方式

| 原典・固定commit | 完成物 | 実際の制作工程 |
| --- | --- | --- |
| Akxan/ppt-agent-skill / 01825dee2ad40a8c719824252605396b9a570d57 | 小さな展示を、ひとつの体験に。5枚 | 原典bauhaus_blockのmock/style、html_packager→dom-to-svg→svg2pptxのnative OOXML変換 |
| henryhyw/slidepoise / 481a028486b528e65706c4e14aa9b74a5e340f12 | クリックを減らす、予約の流れ。3枚 | prepare_generation→builtin image_gen→原典normalizer→semantic map→OpenCV→contract→constructor→固有render-deck |

Bauhausは三原色の硬い幾何と大きな和文見出しを、編集可能な文字・形状へ変換した。Zen Kaku Gothic New Black、BIZ UDPMincho、Manropeを役割別に使用。外部font importの除去処理でpaletteが落ちたため局所修正し、原典の同じ3工程で再生成した。原典Webプレビューも保存している。

SlidePoiseはAI生成画像3枚を入力として保全し、原典の画像計測・復元工程を省略せずnative文字・freeform・connectorsへ組み直した。画像の代わりにsceneを書くだけの経路は採用していない。Windowsの書体計測がArialへfallbackする箇所のみ、同梱OSS TTFへのfamily対応を補足。見出し末尾の折返しはsemantic targetを直して、原典から再構成した。

両方にPPTX、PowerPoint 16で出力したPNG/PDF、入力、依頼、再生成コード、未変更原典と局所差分、短い日本語SKILL、SOURCE、字体条件、制作とスキルの2ZIPを揃えた。原典はMIT。AkxanのPuppeteer依存はApache-2.0原文も保持。ホストartifact-tool SDKや別の汎用deck builderを本制作へ使っていない。共有PowerPointにQuitを呼ばず、自分のdeckだけを閉じた。

## 別制作の取り込み

| 原典・固定commit | 完成物と制作範囲 |
| --- | --- |
| wp-a/paper2ppt / bb98ce95ca5942fc6551dddc723cbdfe2d637d59 | 捨てる前の一目。8枚。原典evidence-first・notes-only分類・主張対応と、原典が認めるpython-pptx fallback。プレビューはLibreOfficeによるPPTX→PDF描画 |
| ficooooo/Paper2ScholarSlides / 207f2b6c8493c569f6caf466c87d868c42936cf6 | 静けさを選べる図書館。8枚。原典academic-templateのmaster/layoutを再利用。プレビューは完成PPTXのSDK描画 |
| deathcats4/scholar-ppt-cn / 6fca3dc0f0fd6033279cc1bd29467967cc185272 | 小さな道案内。8枚。原典Route Bの作者方式とdefaultテンプレートnative部品を保持。プレビューは完成PPTXのSDK描画 |
| helloo1568/slidemuse / 7034412b4c19915c17f8d7206e3723e9e53cf8d2 | 夏の余白。8枚。原典の4作風比較・頁別AI画像生成。プレビューは生成PNGでPPTX実描画ではない。本文・図は画像、画像差替えと話者ノートを編集可 |

全て架空・未実施の研究計画。研究成果・実測効果・引用を補完しない。4件の原MIT原文と原作者を確認してforkへ保存した。原典のQA script未実行、192のoverview内部比率未達など、元PROVENANCE・QAの範囲を保持。PowerPoint実機表示や原典全QA合格へ読み替えない。画像生成の実モデル名が露出されないケースは、特定モデルを指定したと表示しない。

205の配布example/をforkルートへ整え、本文に記載されたsource/・input/と再生成コードを同じ場所で使えるようにした。193の日本語本文にfrontmatterを追加。取り込み3件には書体取得の案内を追加し、元の制作記録とソースは保持した。

## OSS書体と利用導線

Noto CJK公式リポジトリ固定commit f8d157532fbfaeda587e826d4cd5b21a49186f7c からNoto Sans CJK JP Regular/Boldの未改変OTFを取得。Sans/LICENSEのOFL-1.1原文、出所、hash、2ファイルを個別ZIPと全書体ZIPへ保存した。OSの書体を抽出していない。Windowsユーザー環境へ2ファイルを登録し、内部font familyは変更していない。

書体アトリエは9ファミリー16ファイル、7セット。新しい「研究と図表」はNoto Sans CJK JPとManrope。Noto Sans JPとのfont名の違いをAI指示へ明記し、研究作例3件のヘッダーへ「作例の書体を取得」を接続した。以前の公式配布物は取り直さず保持した。

## サイトと確認範囲

現在は厳選44スキル・44冊254枚、49件の作例別recipe、46種類の直接Markdown。制作履歴は54リポ・59冊355枚、56の維持forkと184の取得ファイル。元209件の資料は保持。

LibreOffice描画と生成PNGのフロート経路を追加。画像主体のPPTXを「画像・ノート」の絞り込みに含めた。研究資料の短い説明は「効果がない」と断定せず、未実施の研究提案であることを示す。

制作担当は原典の生成工程と代表完成物の初回表示のみ確認。親は205の2/8表示と描画元、Notoセット・fontの読込・書体取得リンク、Bauhausの自動再生が1→5へ進んで停止することを確認した。取り込み担当が4件のページ送り・取得参照を確認した報告も受領し、親は同じ全件確認を繰り返していない。JS構文と通常のmanifest・サイト生成を実施。全ページ詳細目視、独立採点、構造監査、全ZIP再実行を追加していない。

旧8847サーバーのhandleは消失し、HTTP応答もなかったため、端末管理のhttp.serverを同じroot/portで起動して表示へ接続した。新しいbackground起動・権限・ファイアウォール変更はない。

画面: [Bauhausのフロート](assets/atelier-bauhaus-float.png) · [Notoの書体セット](assets/atelier-noto-research.png)。
