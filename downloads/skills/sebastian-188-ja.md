---
name: ppt-svg-generator-ja
description: Markdownをページ構成とデザインに分け、文字・図形をソースで編集できるSVGへ組み立てる。
---

## このスキルでできること

原稿をページ構成とデザインに分け、文字・図形をソースで調整できるSVG資料へ組める。

- 困っている状況: 原稿を図版にしても、画像に焼き込むと文字や配置を直しにくい。
- 必要な入力: Markdown原稿と作風（5プリセット・自定義・AI推薦のいずれか）
- 受け取るもの: 頁別SVG。任意で/ppt-exportによるPDF・PPTX
- 必要環境: Python＋PyMuPDF / Node.js＋playwright1.62.1/pdf-lib1.17.1 / Chrome/ChromiumとNoto Sans CJK JP
- 作例で試した範囲: 原稿から7頁の構成・目的とSwissデザインを先に保存し、生成器がそれを読んでSVGへ著述。日本語書体を優先し、原典PDF exporterと全7頁の実表示を確認した。
- 制約: 今回の出力はSVGとPDF。PowerPointへの挿入・図形変換と原典PPTX exportは未確認。 / 固定7頁の著述コード。任意Markdownの自動解析器ではない。 / 原典PDF exporterへChrome実行ファイルを選ぶadapterを追加。原本と差分を同梱。 / 原典の中国語字体順を、日本語字形を優先するNoto Sans CJK JPへ変更。書体は別途導入。 / 修復後の独立再評価と新環境へのnpm ciは未実施。


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

## 単体の本文から使う

この本文は `skill-forks/sebastian-188-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `sebastian-188-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: vigorX777 / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/vigorX777/ppt-svg-generator/blob/c873b61673ab0ada5c09f863bff89c8f1b3248fb/LICENSE
