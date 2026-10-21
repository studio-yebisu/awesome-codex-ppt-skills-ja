---
name: ppt-svg-generator-ja
description: Markdownをページ構成とデザインに分け、文字・図形をソースで編集できるSVGへ組み立てる。
---

# MarkdownからSVGの資料を作る

原典 vigorX777/ppt-svg-generator / c873b61673ab0ada5c09f863bff89c8f1b3248fb / MIT。非公式の日本語案内。source/upstreamのSKILLとcommands/specs/stylesを読む。

1. /ppt-analyze @原稿.mdで、見出し・要点・頁型・密度をページ構成にする。目的と読み手に合わせて直す。
2. /ppt-designで、ミニマル・コンサルティング・暗色技術・Swiss・ブランド青の5プリセット、自作、AI推薦から選ぶ。配色・書体・余白・寸法を生成前に固定する。
3. /ppt-generateで、その構成と設計から頁別SVGを作る。原典のSVG互換規範に従い、UTF-8、style属性の書式、6桁色、左寄せ座標、filterなし、1920×1080を確認する。角丸が必要ならrxの代わりにpathを使う。
4. 全頁を描画して、元原稿との対応、日本語、文字・図の欠け、重なり、余白を確認し直す。PPT向けの互換規範を守ることと、実際にPowerPointへ取り込めることを区別する。
5. 必要なら/ppt-exportでPDF/PPTXを作る。PowerPointでSVGを挿入して「図形に変換」する場合は、文字位置・書体・図の編集性を実機で確認する。プリセットでまとめて進める場合は/ppt-quick @原稿.md --style=…を使う。

## この7枚の再現

架空のAI依頼例集をSwissの赤・黒・白でSVGへ組んだ。今回の修復では、原稿とinput/data.jsonから構成・目的を先に保存し、design.jsonの日本語書体・配色を生成器が読んでからSVGを作る。固定原稿用の著述コードで、Markdownを任意に自動解析するアプリではない。

原典の中国語font stackは、日本語字形を優先するNoto Sans CJK JPへ明示変更。原典PDF exporterを使用し、WindowsではSVG_CHROME_EXECUTABLEで既存Chromeを選べる1か所だけを追加。原本とdiffを同梱する。全7頁のPDF実画像とHTMLプレイヤーの7頁送り・戻りを確認した。PowerPointへの挿入・図形変換、原典PPTX export、独立再評価は未実施。

## 環境

Python＋PyMuPDF、Node.js＋playwright1.62.1/pdf-lib1.17.1、利用可能なChromeまたはPlaywright Chromium、Noto Sans CJK JP。書体は公式Noto CJKのOFL配布物を別途導入し、OSフォントを抽出しない。

キットのルートで `npm ci --prefix source`。既存Chromeなら環境変数SVG_CHROME_EXECUTABLEに実行ファイルを指定し、`python source/build.py`。構成・デザイン・SVGとPDFを作る。新出力の全頁を再確認する。修復の再現検査は既存依存を使用し、新しい環境へのnpm ciは未実施。

原典: https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb
書体: https://github.com/notofonts/noto-cjk
