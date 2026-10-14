# AIスライドアトリエ / Studio Yebisu

GitHubの原典スキルを実際に使い、魅力ある日本語資料・短い日本語スキル・OSS書体・頼み方をひと組にした、Studio Yebisu独自のプロジェクトです。

制作例をフロートで再生し、気に入った作風のスキル本文をそのままダウンロード。原典コードが必要なら一式ZIPから取得して、自分の原稿で作れます。

## 現在のアトリエ

- 厳選24スキルと、日本語の作例24冊・135枚。
- Sol 6.1の並列制作による新作「夜の図書館」（Web、6枚）と「余白を買う」（編集可能PPTX、6枚）。
- 日本語スキルの直接Markdown取得と、原典・テンプレート・入力を含む一式ZIP。
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

Sol 6.1の並列制作を中心とし、Astraを使いません。209件をすべて制作することや、大規模QAを完了条件にしません。原カタログは [記録](data/skills.json) と [以前のREADME](docs/history/catalog-readme-before-atelier.md) に保存しています。制作履歴は33リポ・38冊で、現在の厳選掲載と区別します。

原作者、固定原典、LICENSE・NOTICEと書体のOFLを保持します。カタログのCC0は各スキル・コード・素材・書体の条件を変更しません。[原典・条件](licenses.html)を参照してください。

公開更新・merge・deployはローカル制作と別に扱います。
