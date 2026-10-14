# 町の手仕事を、ひらく。

中国色Zhongguose原典テンプレートから作った、日本語6枚の架空回遊体験案です。左上の3章ナビゲーション、朱に近い中国色「绛缨」、大きな漢字、ledgerと二列の観察、原典ASCII背景を使います。日本の伝統色として紹介する例ではありません。

`index.html` と `assets/` を同じフォルダに保ち、Webサーバーで開きます。字体・Motion・Lucideはlocal配布、正常な一式ではCDNやAPI不要。HTMLは単体ファイルではありません。代表PNGは表紙と2頁目だけです。

元操作: 下/右/Space・クリック・wheelで次頁、上/左で前頁、Home/End、Escで索引、Bで動きを停止。0-based catalog adapterは元`__jumpToPage`を呼びます。

再生成: Python3.10+、FontTools、Brotliを用意して `python source/rebuild.py`。入力は `input/MANUSCRIPT.md`、出力文面は `source/slides.html`、生成専用コードは `source/rebuild.py` にあります。原稿を変えるときは入力とslide生成部を合わせて編集します。CSSは `source/adaptation.css` の記録から生成コードのCSS文字列へ反映。生成のたびに元subset generatorの日本語patchを、最終確定HTMLへ実実行します。fonttools未導入環境は `python -m pip install "fonttools[woff]"`。Node18+は原典の任意outline/validation scripts用、閲覧に不要です。

原稿→source-logic→slide-architecture→原典templateコピー→和文/色の局所diff→字体subset。原本は `source/upstream/`、差分は `template-ja.patch` と `subset-japanese.patch`、固定URL/hashはPROVENANCE。日本語不足に対処するためqijiではなくShippori Minchoの完全配布TTFを入力。原典parser/subsetter/rename/manifestは保持し、cover欠落検査を漢字から全字（kanaを含む）へ、copyright/OFL/hashを実入力へ変更しました。原典のqiji seed WOFF2・noticeは保存原本内に残し、未使用の巨大source archiveは取得していません。

原典MIT ©2026木渡川（root/nested両方原文同梱）。実表示の字体はOFL-1.1、MotionはMIT、LucideはISC/Feather MIT。完全な未改変TTF/OFLと由来はsource/fonts/、FONT-SOURCE.json。

必要build、初回表紙・2頁目、元ArrowRight1→2、短いSKILL検証を実施。全頁詳細QA・独立採点・ZIP再実行・親bridge統合・touch/Esc/Bの個別操作は未実施。QA.jsonを参照。
