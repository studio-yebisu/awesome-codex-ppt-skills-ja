# gonta223/japanese-corporate-pptx-skillの日本語制作

原典: https://github.com/gonta223/japanese-corporate-pptx-skill/tree/05480bfa2d8f097ab397861cbe390429e1dbb824

公式15型PPTXから1・2・11・9・8・14枚目を選択し、SKILLの規約に従ってネイティブ図形・チャート・表を編集。専用生成APIは同梱されていない。

原典の15型PowerPointテンプレートから必要な型を選び、図形・文字・表・グラフを編集する。企画の結論、担当、期日、確認方法を日本語で書く。原典の図形を勝手に共通HTMLへ置き換えない。

## 作例

- くらし便 EC事業 9月報告 / 6枚 / pptx
- カタログ内の案内: repository.html?repo=gonta223/japanese-corporate-pptx-skill
- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo=gonta223/japanese-corporate-pptx-skill
- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。

## 環境

- Python 3.13 / python-pptx / lxml / Pillow
- Microsoft PowerPoint 16.0 と PowerShell 7（PNG/PDF描画）
- 同梱の japanese-corporate-ponchi-template.pptx

## 元の制作コマンド

    git clone https://github.com/gonta223/japanese-corporate-pptx-skill .build/actual-upstreams/gonta223__japanese-corporate-pptx-skill

    git -C .build/actual-upstreams/gonta223__japanese-corporate-pptx-skill checkout 05480bfa2d8f097ab397861cbe390429e1dbb824

    python -m venv .venv

    .venv\Scripts\python -m pip install python-pptx lxml Pillow

    .venv\Scripts\python tools/build_japanese_repository_examples.py --only gonta --render

## 確認範囲

- 独立した生成プログラムではなく指示SkillとPPTXテンプレートを用いた制作。原典テンプレートの再配布はMIT LICENSEを保持。

## 権利

原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。
