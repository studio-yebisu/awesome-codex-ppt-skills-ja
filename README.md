# AIスライドアトリエ / Studio Yebisu

GitHubの原典スキルを実際に使い、魅力ある日本語資料・短い日本語スキル・OSS書体・頼み方をひと組にした、Studio Yebisu独自のプロジェクトです。

制作例をフロートで再生し、気に入った作風のスキル本文をそのままダウンロード。原典コードが必要なら一式ZIPから取得して、自分の原稿で作れます。

## 現在のアトリエ

- 厳選29スキルと、日本語の作例29冊・161枚。
- Sol 6.1の並列制作で、科学図解・HTML変換・手描き章扉に続き、書店のWeb資料・作業場の企画書・時間配分の図解の新作3冊16枚を制作。
- 各派生スキル固有の本文を直接Markdown取得。サイトで本文を開いてコピーでき、原典・テンプレート・入力の一式ZIPも取得。
- 新しいOSS書体6ファミリー・10ファイルと、4作風の実フォント見本・AI向け指示コピー。

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

Sol 6.1の並列制作を中心とし、Astraを使いません。209件をすべて制作することや、大規模QAを完了条件にしません。原カタログは [記録](data/skills.json) と [以前のREADME](docs/history/catalog-readme-before-atelier.md) に保存しています。制作履歴は39リポ・44冊で、現在の厳選掲載と区別します。

原作者、固定原典、LICENSE・NOTICEと書体のOFLを保持します。カタログのCC0は各スキル・コード・素材・書体の条件を変更しません。[原典・条件](licenses.html)を参照してください。

公開更新・merge・deployはローカル制作と別に扱います。

最新バッチ： [本の向こうへ。](examples/repositories/slidespeak-showcase/README.md) · [ひらく、街の作業場。](examples/repositories/pptwise-showcase/README.md) · [朝の20分を、組み直す。](examples/repositories/aham-showcase/README.md)。

前のバッチ： [雨が、地下水になるまで](examples/repositories/sci-diagram-showcase/README.md) · [小さな店の、ひとつの旗。](examples/repositories/html-editable-showcase/README.md) · [チームのアイデアを、育てる。](examples/repositories/hand-drawn-showcase/README.md)。

原典の条件と実行SDKの条件を分け、科学図解の配布版は原典のOSS portable経路を使用。既存のホスト専有SDKによる評価作例は現行推奨から外し、履歴へ保管しています。
