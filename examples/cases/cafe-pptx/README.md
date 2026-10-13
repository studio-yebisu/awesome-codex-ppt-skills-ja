# 喫茶つむぎ 2号店出店提案

組織・店舗・計数は、制作手順を試すために作成した架空のサンプルです。外部調査・実績・見積書ではありません。

## 閲覧・再制作

deck.pptxをPowerPointで開きます。Noto Sans JPが必要です。閲覧用はrender/deck.pdf。

input/data.jsonとPROMPT.txtを日本語派生スキルへ渡します。NOTES.mdに講稿、PROVENANCE.jsonに原典、QA.jsonに実施状態。

## カタログ全体から再生成

リポジトリrootで python tools/make_business_pptx.py。上流依存を導入した .build/ppt-master-venv が必要。
PowerPoint導入済みWindowsで powershell -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/cases/cafe-pptx/deck.pptx -OutputDirectory examples/cases/cafe-pptx/render

ZIPだけにはカタログ生成スクリプト・Python環境を含みません。再生成は同じ出力先を更新するため独自改稿は別の場所へ保存してください。

## 条件

LICENSEとlicenses/fontsを保持。改変ソースは本配布物と https://github.com/studio-yebisu/awesome-codex-ppt-skills-ja のskill-forks/ppt-master-ja。原作者の公式作例ではありません。
