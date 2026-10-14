# AIスライドアトリエ / Studio Yebisu

GitHubの原典スキルを実際に使い、魅力ある日本語資料・短い日本語スキル・OSS書体・頼み方をひと組にした、Studio Yebisu独自のプロジェクトです。

制作例をフロートで再生し、気に入った作風のスキル本文をそのままダウンロード。原典コードが必要なら一式ZIPから取得して、自分の原稿で作れます。

## 現在のアトリエ

- 厳選44スキルと、日本語の作例44冊・254枚。
- Sol 6.1の2並列で、原典Bauhausの変換器とAI画像の計測・復元処理による新作2冊8枚を追加。別制作4冊32枚も、制作方式と編集範囲を保持して接続。
- 各派生スキル固有の本文を直接Markdown取得。サイトで本文を開いてコピーでき、原典・テンプレート・入力の一式ZIPも取得。
- OSS書体9ファミリー・16ファイルと、7作風の実フォント見本・AI向け指示コピー。Noto Sans CJK JPの公式OTF/OFLを追加し、研究作例から同じ書体を直接取得。

原典のSKILL、固有テンプレート・controller・生成器を使います。日本語向けの改良と実施範囲は各作例に記載。主な出力が開く範囲の軽い確認を行い、制作を中心に進めています。

## ローカルで開く

```powershell
python -m http.server 8847 --bind 127.0.0.1
```

ブラウザーで http://127.0.0.1:8847/ を開いてください。

一覧の更新は、担当が独立fragmentを追加した後に次の順で実行します。

```powershell
python tools/build_repository_manifest.py
python tools/build_curated_collection.py
python tools/build_atelier_site.py
```

## 制作の方針と条件

[制作方針](docs/PROJECT.md) · [製品仕様](docs/PRODUCT_SPEC.md) · [現在の実行目標](data/project-goal.json) · [厳選掲載](data/product-collection.json)

Sol 6.1の並列制作を中心とし、Astraを使いません。209件をすべて制作することや、大規模QAを完了条件にしません。原カタログは [記録](data/skills.json) と [以前のREADME](docs/history/catalog-readme-before-atelier.md) に保存しています。制作履歴は54リポ・59冊で、現在の厳選掲載と区別します。

原作者、固定原典、LICENSE・NOTICEと書体のOFLを保持します。カタログのCC0は各スキル・コード・素材・書体の条件を変更しません。[原典・条件](licenses.html)を参照してください。

公開更新・merge・deployはローカル制作と別に扱います。

最新バッチ： [小さな展示を、ひとつの体験に。](examples/repositories/ppt-agent-showcase/README.md) · [クリックを減らす、予約の流れ。](examples/repositories/slidepoise-showcase/README.md)。原典のBauhaus変換とAI画像→OpenCV→native図形の復元を実行。[制作記録](docs/PRODUCTION_BATCH_20261014_07.md)。

別制作の取り込み： [捨てる前の一目](examples/repositories/sebastian-205/README.md) · [静けさを選べる図書館](examples/repositories/sebastian-203/README.md) · [小さな道案内](examples/repositories/sebastian-193/README.md) · [夏の余白](examples/repositories/sebastian-192/README.md)。研究提案3冊の文字・図形は編集可。夏の余白は本文と図が画像で、画像差替え・話者ノートを編集できます。描画元と確認範囲を各ガイドへ記載。

前のバッチ： [平均の、その先。](examples/repositories/native-math-showcase/README.md) · [雨の日の、通学ルート。](examples/repositories/thesis-defense-showcase/README.md)。原典で9個の数式をPowerPointへ注入し、研究テンプレートの複製・置換で6枚を生成。「編集したいもの」の絞り込みとPPTX本体・日本語本文の直接取得を接続。[制作記録](docs/PRODUCTION_BATCH_20261014_06.md)。

前のバッチ： [割合は、全体との比べ方。](examples/repositories/soil-teaching-showcase/README.md) · [待ち時間のしくみ](examples/repositories/beamer-showcase/README.md) · [花を、一本から。](examples/repositories/learndeck-showcase/README.md)。原典のHTML段階表示、Beamer、DOMからのPPTX変換を実使用。PDFの絞り込みとフロート表示にも対応しました。

別制作セッションの取り込み： [まちを、余白から。](examples/repositories/sebastian-207/README.md) · [雨の図書室](examples/repositories/sebastian-208/README.md)。制作元は各PROVENANCEへ記録。前者の原典美術QAは80.7点FAILを維持。後者の本文・図は画像で、ノートと画像差替えを編集できます。両方ともPowerPoint実機表示は未確認です。

SOILは実行ソフトウェアがMIT、設計文・スキルの派生がCC BY-NC-SA 4.0です。本文の取得前と日本語キットへ非商用・帰属・継承条件を表示し、独自の教材出力を一括で非商用と解釈しません。Beamerの欧文書体は同梱のGFL／LPPL、和文と書体アトリエはOFLの原文を保持します。

前のバッチ： [土曜日を、街の作業場に。](examples/repositories/agent-slides-showcase/README.md) · [街を歩く、寄り道を選ぶ。](examples/repositories/slidefly-showcase/README.md)。作例選択に合わせて依頼文・本文・ZIPを切り替え、Web作例のPowerPoint版も取得できます。PPTX内のMorph実再生は未確認です。

ひとつ前のバッチ： [本の向こうへ。](examples/repositories/slidespeak-showcase/README.md) · [ひらく、街の作業場。](examples/repositories/pptwise-showcase/README.md) · [朝の20分を、組み直す。](examples/repositories/aham-showcase/README.md)。

前のバッチ： [雨が、地下水になるまで](examples/repositories/sci-diagram-showcase/README.md) · [小さな店の、ひとつの旗。](examples/repositories/html-editable-showcase/README.md) · [チームのアイデアを、育てる。](examples/repositories/hand-drawn-showcase/README.md)。

原典の条件と実行SDKの条件を分け、科学図解の配布版は原典のOSS portable経路を使用。既存のホスト専有SDKによる評価作例は現行推奨から外し、履歴へ保管しています。
