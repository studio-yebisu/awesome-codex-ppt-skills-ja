# 技術発表、文字と色、連続する一冊

Sol 6.1の並列担当がQuarto、色彩の企画、共通画面の原典方式を完成した。親は1頁1HTMLの発表と書体・サイト統合を担当。通常18枚と、共通画面の8段階を追加した。Astra、独立レビュー、全頁詳細検査、全ZIP再実行は使っていない。

## 原典の制作方式

| 原典 | 日本語作例 | 実際に使う方式 |
| --- | --- | --- |
| alfredo-hs/quarto-talks | 五つの点から、一本の線を。6枚 | 原典template.qmdと拡張0.4.1を実Quartoでrender。合成5点はNumPy lstsqで実計算 |
| tanglele110-hash/zhongguose-ppt-skill | 町の手仕事を、ひらく。6枚 | 元template、文字・章・配色、元pagerとASCII背景、確定HTMLからの元字体subset生成 |
| thmsgo18/presentation-forge | 待つ時間にも、道しるべを。6枚 | 元new_deckで独立folder、1頁1HTML、元obsidianとcomponents、未変更engine/build.pyで単独HTML |
| Codagent-AI/and-scene | 一冊の本が、次の人へ。8段階 | 元bootstrap、安定IDのentity、共通Scene、型付きStepで同じ本の位置と関係を変える |

Quartoは公式portable1.9.38を私有.buildへ取得し、配布ZIPにCLI binaryを含めない。元QMD・意味クラス・1600×900・白青の拡張を利用。5点は単位を持たない教材用の合成値。実計算の傾き0.8、切片1.4、SSE3.6をJSON/SVGと資料に対応させた。コード欄は実計算と同じ処理を示し、QMDの実行を装わない。非致命的SCSS color-variable export warningを原ログとQAに残す。元Reveal5.1.0と数式、図、字体を内包したHTMLを生成。

手仕事の企画では元template、CSS、Motion、Lucide、縦pagerとASCII背景を保持する。元の中国色「绛缨」#9E3B3Bとaccent-on白を選び、日本の伝統色と表示しない。原稿→source logic→architecture→確定文言→元subset generatorの順を使う。日本語のかなを含む入力と公式Shipporiのための局所patchを保存し、生成字体に実copyright・OFL・hashを付ける。実TTF/OFLと元runtimeが必要なためWeb一式ZIPで案内する。架空の企画で、人物・実在会場・日時・費用・実績は未定。

画面設計案は原典のassertion-evidence、speaker notes、1頁1HTML、original stats/count、steps、timeline、icons、balanced motionを使う。obsidianの青黒・紫・シアン、元のtype scale・blocksを保持し、日本語字体と字間だけをtheme/deck.cssへ分けた。初回表示でローカルの仕上げ処理がengine内のbody終了文字列へも追記する不具合を見つけ、最終document closeだけへ追記するよう修正。元engineと元build.pyは未変更。原典checkerのscreenshot helperで代表2頁を生成し、実ブラウザーの元Next slideで1/6→2/6。全頁check_deck/contact sheetはユーザーの確認範囲に合わせ実施していない。

共通画面は空の私有appへ元bootstrapを複製し、元が指定するnpm dependenciesを実install。元tsc -bとvite buildが成功した。Presentation/Stage/types/Step/registry、同じBookWorld/groupKeyとlayoutIdを使い、880×380の共通canvasで一冊の本を移動・縮尺変更する。初回1600×900と元1→2では同じbook DOMが保持され、runtime/consoleエラーなし。元usePresentationNav/setStepへの最小bridgeと、配布先に合わせたhost/static entry、作例CSSだけを変更。元kitの原本/hash/diff、MIT、runtime条件、3ファミリーの実TTF/OFLを保存。dist/index.html＋assets/fontsを必要とするためWeb一式ZIPで案内する。原典fullverify/inspectのlast/dense/mobileは実施していない。

## コード用の書体を加える

Google Fonts公式固定commit `66928797f271fed5ee428544e7229685e2d90127` から未改変JetBrainsMono[wght].ttfとOFLを取得。10ファミリー17ファイル、用途別8セットになった。ユーザー用Windows字体へ今回の1ファイルだけ登録した。

「コードと技術発表」はBIZ UDPMincho見出し、BIZ UDPGothic本文、Manrope英数字、JetBrains Monoコード。実字体の見本とAI向けコピー、配布ZIP・OFLをつなぐ。コードの等幅、合字off、日本語コメントのBIZ fallbackを指示し、Quarto作例で実際に同じコード字体を使用する。サイトの依頼文にも4番目の役割を含める。

元に場面区分のない共通画面の演出は、8段階を8枚・8場面へ読み替えない。依頼フォームの入力も希望段階数で組み立てる。

## 統合状況

manifest・厳選集・直接Markdown・配布記録・サイトを更新した。厳選61スキル・61冊346枚＋23段階。制作履歴は71リポ・76冊447枚＋23段階、作例の使い方66件、直接MD63件、維持するfork73件、取得用成果物237件。

親はAndSceneのフロートで1/8→2/8を操作し、元02/08と2段階目の題名へ同期した。Web一式・直接SKILL・固定原典の取得を表示。原典に場面区分がないため依頼フォームは希望8段階、技術発表の書体を選ぶとコードJetBrains Monoも依頼文へ入る。新しい字体見本を表示した。コピー成功の表示は確認し、session clipboard読戻しが当該指示を反映しないため、clipboard内容の検証済みとは記録していない。

軽い確認の記録は[こちら](../data/atelier-light-check-20261014-11.json)。具体的な仕上げ不具合の修復以外に確認を広げていない。ユーザーの現行条件に沿ったローカル改修は完了し、未掲載原典の全件制作と大量QAを完了条件に戻していない。公開push・main merge・deployは行っていない。
