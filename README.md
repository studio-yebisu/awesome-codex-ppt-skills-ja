# 八百万図AIツールボックス｜AIスライド

GitHubのスライドスキルを、何が改善するか・何を渡すか・何を作れるかから選ぶ日本語サイトです。作例では、その機能が表れたページを開いて確認できます。

## 現在の改訂

61スキルの効果と入力・出力を原典に照らし、該当ページと使い方へつなぎ直しています。Kimi K3とClaude Opus 5.5の独立評価で指摘を修正中です。初回の代表6件は76点と42点で、現在版の満点評価はまだ完了していません。

Claude Opus 5.5がサイト構成と一部作例の制作・修復を担当し、Codexが統合と確認を担当。以前のSol 6.1による作例の帰属は保持しています。

- スキルの機能・用途・形式から検索し、効果が分かるページを直接再生。
- 詳細で問題・入力・出力・必要環境・利用条件・実施範囲・使い方を確認。
- 日本語スキル本文と必要な一式ZIPを取得し、自分の原稿用の依頼文を作成。
- 公式フリーフォント30ファミリー・45ファイル、15組み合わせ。用途別4ZIP・個別ZIP・実見本・公式サイトへのリンク。
- 現在の掲載は61作例・341枚と23段階。通常の枚数と演出の段階は分けて集計。

[使い方](guide.html) · [制作・評価の状況](status.html) · [評価条件](docs/SKILL_EFFECT_REVIEW.md) · [原典・利用条件](licenses.html)

2026年10月21日、ユーザー依頼により全作業ブランチとローカル変更をmainへ統合しました。スライド品質の最終評価は継続中です。[統合時の未完了記録](docs/MAIN_INTEGRATION_20261021.json)を参照してください。

## ローカルで開く

```powershell
python -m http.server 8847 --bind 127.0.0.1
```

ブラウザーで http://127.0.0.1:8847/ を開いてください。

一覧の更新は、担当が独立fragmentを追加した後に次の順で実行します。

```powershell
python tools/build_repository_manifest.py
python tools/build_curated_collection.py
python tools/build_skill_effects.py
python tools/build_atelier_site.py
```

## 制作の方針と条件

[制作方針](docs/PROJECT.md) · [製品仕様](docs/PRODUCT_SPEC.md) · [現在の実行目標](data/project-goal.json) · [厳選掲載](data/product-collection.json)

今後の既定モデルはClaude Opus 5.5です。既存の掲載作例はSol 6.1の並列制作によるもので、その記録を保持します。Astraを使いません。209件をすべて制作することや、大規模QAを完了条件にしません。原カタログは [記録](data/skills.json) と [以前のREADME](docs/history/catalog-readme-before-atelier.md) に保存しています。制作履歴は71リポ・76冊で、現在の厳選掲載と区別します。

原作者、固定原典、LICENSE・NOTICEと書体のOFLを保持します。カタログのCC0は各スキル・コード・素材・書体の条件を変更しません。[原典・条件](licenses.html)を参照してください。

公開更新・merge・deployはローカル制作と別に扱います。

最新バッチ： [五つの点から、一本の線を。](examples/repositories/quarto-talks-showcase/README.md) · [町の手仕事を、ひらく。](examples/repositories/zhongguose-showcase/README.md) · [待つ時間にも、道しるべを。](examples/repositories/presentation-forge-showcase/README.md) · [一冊の本が、次の人へ。](examples/repositories/and-scene-showcase/README.md)。元Quartoの実renderと最小二乗の実計算、元字体subset生成と章ナビ、1頁1HTMLの原典ビルド、同じ本が移動する共通scene kitを使用。公式JetBrains Monoと技術発表指示を追加。[制作記録](docs/PRODUCTION_BATCH_20261014_11.md)。

前のバッチ： [香りを、贈る。](examples/repositories/cogine-templates-showcase/README.md) · [紙と、インクの休日。](examples/repositories/keynot-showcase/README.md) · [パンが、店先に届くまで。](examples/repositories/beatdeck-showcase/README.md) · [遠くの席へ、伝わる資料。](examples/repositories/scene-graph-showcase/README.md)。原典テンプレートの選択と差し替え、ブランド抽出と元controller、Reactの一段ずつ展開する舞台、元PPTX生成・美化を使用。[制作記録](docs/PRODUCTION_BATCH_20261014_10.md)。

前のバッチ： [ひとつの服を、もう一度。](examples/repositories/marp-mcp-showcase/README.md) · [文字のかたちを、観察する。](examples/repositories/sketch-note-showcase/README.md) · [星を待つ、夜の天文台。](examples/repositories/slide-wright-showcase/README.md) · [町の道具を、借り合う。](examples/repositories/design-dna-showcase/README.md)。原典の実MCP、手描きCSSとページ操作、2枚を保持して育てる独自テーマ、参考画像からのDNA抽出を使用。短い日本語本文と制作一式を直接取得できます。[制作記録](docs/PRODUCTION_BATCH_20261014_09.md)。

前のバッチ： [仕事の引き継ぎを、迷わない一枚に。](examples/repositories/presentation-skill-showcase/README.md) · [小さな展示を、ひとつの体験に。動く展示案内](examples/repositories/aws-html-showcase/README.md)。原典のJSON・role contract・PptxGenJSで文字・図形・表を生成し、原典extractor・Neon controllerでPPTXをHTMLへ変換。変換前後の資料を行き来できます。[制作記録](docs/PRODUCTION_BATCH_20261014_08.md)。

別制作の取り込み： [AIに任せる前の設計図](examples/repositories/sebastian-188/README.md) · [動画一本を、教材へ。](examples/repositories/sebastian-178/README.md) · [音を、地図にする。](examples/repositories/sebastian-173/README.md)。SVG→PDF、原典CSSの図解部品と教材化、13slotのHTML編集誌面。178のroot Apache-2.0とSKILL内MITの記載差を保持し、埋め込み字体は公式固定配布のNotoへ揃えました。

前のバッチ： [小さな展示を、ひとつの体験に。](examples/repositories/ppt-agent-showcase/README.md) · [クリックを減らす、予約の流れ。](examples/repositories/slidepoise-showcase/README.md)。原典のBauhaus変換とAI画像→OpenCV→native図形の復元を実行。[制作記録](docs/PRODUCTION_BATCH_20261014_07.md)。

別制作の取り込み： [捨てる前の一目](examples/repositories/sebastian-205/README.md) · [静けさを選べる図書館](examples/repositories/sebastian-203/README.md) · [小さな道案内](examples/repositories/sebastian-193/README.md) · [夏の余白](examples/repositories/sebastian-192/README.md)。研究提案3冊の文字・図形は編集可。夏の余白は本文と図が画像で、画像差替え・話者ノートを編集できます。描画元と確認範囲を各ガイドへ記載。

前のバッチ： [平均の、その先。](examples/repositories/native-math-showcase/README.md) · [雨の日の、通学ルート。](examples/repositories/thesis-defense-showcase/README.md)。原典で9個の数式をPowerPointへ注入し、研究テンプレートの複製・置換で6枚を生成。「編集したいもの」の絞り込みとPPTX本体・日本語本文の直接取得を接続。[制作記録](docs/PRODUCTION_BATCH_20261014_06.md)。

前のバッチ： [割合は、全体との比べ方。](examples/repositories/soil-teaching-showcase/README.md) · [待ち時間のしくみ](examples/repositories/beamer-showcase/README.md) · [花を、一本から。](examples/repositories/learndeck-showcase/README.md)。原典のHTML段階表示、Beamer、DOMからのPPTX変換を実使用。PDFの絞り込みとフロート表示にも対応しました。

別制作セッションの取り込み： [まちを、余白から。](examples/repositories/sebastian-207/README.md) · [雨の図書室](examples/repositories/sebastian-208/README.md)。制作元は各PROVENANCEへ記録。前者の原典美術QAは80.7点FAILを維持。後者の本文・図は画像で、ノートと画像差替えを編集できます。両方ともPowerPoint実機表示は未確認です。

SOILは実行ソフトウェアがMIT、設計文・スキルの派生がCC BY-NC-SA 4.0です。本文の取得前と日本語キットへ非商用・帰属・継承条件を表示し、独自の教材出力を一括で非商用と解釈しません。Beamerの欧文書体は同梱のGFL／LPPL、和文と書体アトリエはOFLの原文を保持します。

前のバッチ： [土曜日を、街の作業場に。](examples/repositories/agent-slides-showcase/README.md) · [街を歩く、寄り道を選ぶ。](examples/repositories/slidefly-showcase/README.md)。作例選択に合わせて依頼文・本文・ZIPを切り替え、Web作例のPowerPoint版も取得できます。PPTX内のMorph実再生は未確認です。

ひとつ前のバッチ： [本の向こうへ。](examples/repositories/slidespeak-showcase/README.md) · [ひらく、街の作業場。](examples/repositories/pptwise-showcase/README.md) · [朝の20分を、組み直す。](examples/repositories/aham-showcase/README.md)。

前のバッチ： [雨が、地下水になるまで](examples/repositories/sci-diagram-showcase/README.md) · [小さな店の、ひとつの旗。](examples/repositories/html-editable-showcase/README.md) · [チームのアイデアを、育てる。](examples/repositories/hand-drawn-showcase/README.md)。

原典の条件と実行SDKの条件を分け、科学図解の配布版は原典のOSS portable経路を使用。既存のホスト専有SDKによる評価作例は現行推奨から外し、履歴へ保管しています。
