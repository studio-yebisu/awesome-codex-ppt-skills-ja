---
name: quarto-talks-ja
description: 固定Quarto Talksテンプレートと拡張の意味クラスで、日本語の議論と図・式・コードを組み、実Quarto CLIからReveal HTMLを作る。
---

## このスキルでできること

原稿・図・数式・短いコードをQMDにまとめ、発表用の配置を持つHTMLへ変換する。

- 困っている状況: 計算結果を別アプリから貼ると、原稿・コード・出力の関係が追いにくい。
- 必要な入力: 発表の目的・読み手・原稿・図の元データ・参考文献
- 受け取るもの: QMD・計算コード・SVGと、ブラウザーで発表するHTML
- 必要環境: Quarto >=1.4（本作例1.9.38） / 実計算用Python・NumPy・Matplotlib / 同梱OFL書体と原典MIT拡張
- 作例で試した範囲: 同じ合成5点を、表・散布図・直線式・実計算コード・当てはめ結果へ接続した。原典拡張でHTMLを生成し、コード枠の幅を局所SCSSで修正。全6頁を実表示で確認した。
- 制約: 出力はQMDからのHTML。PPTXの編集可能化は扱わない。 / 5分・6枚の作例として、原典の16〜24枚既定を短縮した。 / 表示コードとは別にPythonを実行した。Quartoのnotebook実行ではない。 / Quarto1.9.38の色変数書き出し警告は残る。HTML/CSS生成と全6頁表示は確認済み。


# 日本語 Quarto Talks

原典 [alfredo-hs/quarto-talks](https://github.com/alfredo-hs/quarto-talks) commit `60f69c3568181898767470382d5599d4bb86b7b6`、MIT ©2026 Alfredo H. Sanchez。完全原文は[upstream/SKILL.md](upstream/SKILL.md)、条件は[LICENSE](LICENSE)、出所は[SOURCE.json](SOURCE.json)。

## 実制作

1. 目的・読み手・時間を押さえ、argument spineを書き、素材から必要なページを選ぶ。
2. 原典[template.qmd](upstream/template.qmd)と[_extensions/quarto-talks](upstream/_extensions/quarto-talks/_extension.yml)を実制作へコピーする。`.statement`/`.question`/`.quote`/`.visual`/`.math`/`.code`と普通の表/列を選び、QMDを作る。元SCSSのwhite/blue・余白・semantic layoutを保持する。
3. 日本語見出し/本文/コードの字体役割は承認済みの局所SCSSで追加できる。公式実TTF/OFLを取得し、OSフォントを抽出しない。合字off、日本語はBIZ fallback。
4. 計算結果・出典を実確認する。合成データは合成と明記。実行していないコードや引用・観測・精度を作らない。普通のPython表示fenceと実行工程を区別する。
5. Quarto>=1.4を公式配布から用意し、`quarto render talk.qmd`。今回portable1.9.38を実使用。embed-resources/self-contained-math、1600×900、元Reveal APIを使う。独自renderer/controllerへ置換しない。
6. 原典Step6に従い、完成HTMLの全ページを通常の発表画面で確認する。文字・数式・コード・引用・図の欠け、はみ出し、投影時の大きさ、白青の配色と字体役割、説明順を確認し、問題を直して再renderする。

## この6枚の作例で変更した範囲

作例の5分・6枚指定を優先し、原典の16〜24枚既定を短縮した。数値は合成5点から実計算し、コード表示と計算実行を区別した。コード枠の幅を局所SCSSで補正し、原典拡張は変更していない。全6頁とページ移動を実表示で確認した。独立再評価は別途行う。

## MDだけを取得した場合

原典固定参照：[SKILL.md](https://raw.githubusercontent.com/alfredo-hs/quarto-talks/60f69c3568181898767470382d5599d4bb86b7b6/SKILL.md)、[template.qmd](https://raw.githubusercontent.com/alfredo-hs/quarto-talks/60f69c3568181898767470382d5599d4bb86b7b6/template.qmd)、[_extension.yml](https://raw.githubusercontent.com/alfredo-hs/quarto-talks/60f69c3568181898767470382d5599d4bb86b7b6/_extensions/quarto-talks/_extension.yml)、[SCSS](https://raw.githubusercontent.com/alfredo-hs/quarto-talks/60f69c3568181898767470382d5599d4bb86b7b6/_extensions/quarto-talks/quarto-talks.scss)、[Lua filter](https://raw.githubusercontent.com/alfredo-hs/quarto-talks/60f69c3568181898767470382d5599d4bb86b7b6/_extensions/quarto-talks/bluesky.lua)、[LICENSE](https://raw.githubusercontent.com/alfredo-hs/quarto-talks/60f69c3568181898767470382d5599d4bb86b7b6/LICENSE)。フォーク一式ZIPのupstream/は同じ未変更原本。

制作一式`quarto-talks-example-ja.zip`からtalk.qmd、_extensions/、input/data.csv、source/compute_fit.py、source/japanese.scss、source/fonts.html、source/bridge.html、references.bib、fonts/（実TTF/OFL/receipt）を取り、READMEの再生成コマンドを使う。本文・式・表・コードをQMDから編集し、図は実計算code/SVGから編集する。完成HTMLは字体/図/runtimeを内包。PPTXは生成していない。

CLIはZIPへ含めない。[公式取得](https://quarto.org/docs/download/)から[固定Windows portable1.9.38](https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.38/quarto-1.9.38-win.zip)を展開し、binをPATHへ。SHA256 `3dd3b22616dcae65f710b1d6c019b818027312c8cbf54a0a08fdd9842346375e`。字体はGoogle Fonts固定`66928797f271fed5ee428544e7229685e2d90127`のShippori Mincho/BIZ UDPGothic/JetBrains Mono（OFL）。実ファイルと固定URLは制作ZIPのfonts/SOURCE.json、フォークのFONT-SOURCES.jsonへ。

数値計算の一次資料：[NumPy公式linalg.lstsq](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)。依存の原文条件は制作ZIPのlicenses/とDEPENDENCIES.md。

## 単体の本文から使う

この本文は `skill-forks/quarto-talks-ja/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/alfredo-hs/quarto-talks/tree/60f69c3568181898767470382d5599d4bb86b7b6

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `quarto-talks-ja.zip` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は各作例の入手元と利用条件に従い、再配布できるファイルだけを添える。

原作者: alfredo-hs / 原典条件: MIT。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

- https://github.com/alfredo-hs/quarto-talks/blob/60f69c3568181898767470382d5599d4bb86b7b6/LICENSE
