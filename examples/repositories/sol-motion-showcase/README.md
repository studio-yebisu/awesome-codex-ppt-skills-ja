# 夜の図書館

仕事帰りに出会う、次の一冊。架空の図書館企画を6ページの広告・提案スライドにしました。実在施設、開館時間、利用実績は含みません。

`index.html` を開き、矢印・スペース・ホイール・スワイプで移動。4ページの気分別の棚はクリックで切り替えられます。墨紺と蛍光ライム、和文ゴシックと明朝、SVGの本・窓・棚で構成。フル日本語フォントを内包し、CDNや外部AI APIは使いません。

制作は zarazhangrui/frontend-slides の MIT 原典（commit 9906a34d640d2111f724544cbc50f7f130569ae1）。原典固定stageのCSS全文、HTML構造、SlidePresentation、段階表示を直接使用・拡張しています。`source/` に使用ファイル、`PROVENANCE.json` にハッシュ、`PROMPT.txt` にAI依頼文を保存。元スキルを共通rendererで置き換えていません。

再生成: repoルートで `python tools/build_sol_motion_showcase.py`。軽い確認の範囲は `QA.json`。正式採用・全ページ視覚QA・配布ZIP検証は未実施です。

英数字はSpace Groteskを併用（フルTTF・OFL同梱）。HTMLは6ページ、静止プレビューは代表2枚です。サイトとの同一origin postMessageページ送りを接続済み。ZIPを展開してindex.htmlを開けばオフライン再生できます。
