# gonta223/japanese-corporate-pptx-skill の日本語実行例

公式15型PPTXから1・2・11・9・8・14枚目を選択し、SKILLの規約に従ってネイティブ図形・チャート・表を編集。専用生成APIは同梱されていない。

組織・数値・担当者は架空。input/data.json、PROMPT.txt、NOTES.mdに入力・依頼・講稿を保存。

## 再現手順

カタログ全体を取得し、そのrootで次を実行します。

```powershell
git clone https://github.com/gonta223/japanese-corporate-pptx-skill .build/actual-upstreams/gonta223__japanese-corporate-pptx-skill
git -C .build/actual-upstreams/gonta223__japanese-corporate-pptx-skill checkout 05480bfa2d8f097ab397861cbe390429e1dbb824
python -m venv .venv
.venv\Scripts\python -m pip install python-pptx lxml Pillow
.venv\Scripts\python tools/build_japanese_repository_examples.py --only gonta --render
```

- Python 3.13 / python-pptx / lxml / Pillow
- Microsoft PowerPoint 16.0 と PowerShell 7（PNG/PDF描画）
- 同梱の japanese-corporate-ponchi-template.pptx

元PPTXをpython-pptxで開き、source/template-map.jsonのページと図形を編集。source/build.logに実施操作。上流の15型テンプレートは保持したまま、選択6ページだけを書き出す。

## 根拠と制約

PROVENANCE.jsonにcommitと原典ファイルSHA、environment.jsonに依存、QA.jsonとrender/powerpoint-render.jsonに検査範囲を保存。LICENSEは原文を保持。

- 独立した生成プログラムではなく指示SkillとPPTXテンプレートを用いた制作。原典テンプレートの再配布はMIT LICENSEを保持。
