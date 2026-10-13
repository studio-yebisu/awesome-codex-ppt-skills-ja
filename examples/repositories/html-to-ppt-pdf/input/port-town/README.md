# 週末の汐見港町 回遊企画提案

組織・店舗・計数は、制作手順を試すために作成した架空のサンプルです。外部調査・実績・見積書ではありません。

## 閲覧・再制作

フォルダーで python -m http.server 8000 を実行しindex.htmlを開きます。書体はHTML内蔵。Guizangの依存はassetsに同梱。CDN fallbackが残るためオフライン確認結果はQAを参照。

input/data.jsonとPROMPT.txtを日本語派生スキルへ渡します。NOTES.mdに講稿、PROVENANCE.jsonに原典、QA.jsonに実施状態。

## カタログ全体から再生成

リポジトリrootで python tools/build_case_studies.py。元テンプレートを用いた当地の制作処理です。

ZIPだけにはカタログ生成スクリプト・Python環境を含みません。再生成は同じ出力先を更新するため独自改稿は別の場所へ保存してください。

## 条件

LICENSEとlicenses/fontsを保持。改変ソースは本配布物と https://github.com/studio-yebisu/awesome-codex-ppt-skills-ja のskill-forks/guizang-ppt-skill-ja。原作者の公式作例ではありません。
