# テンプレート、ブランド、段階のある話と編集する資料

Sol 6.1の2並列で4件の原典を実制作し、ローカルサイトへ統合した。通常資料18枚と、6場面・15段階のモーション資料を追加。親は題材と統合、一覧の検索を担当した。Astra・独立レビュー・全頁詳細目視は使っていない。

## 制作した原典

| 原典 | 作例・狙い | 原典の方式 |
| --- | --- | --- |
| cogine-ai/ai-slide-templates | 香りを、贈る。6枚 | template metadataを比べ、editorial-luxuryを複製し、原稿を元HTMLの領域へ差し替える |
| shawnzam/keynot | 紙と、インクの休日。6枚 | ブランドの色・書体・使用比率を抽出し、原典shell/CSS/inline controllerで組む |
| borjaperfra/beatdeck | パンが、店先に届くまで。6場面・15段階 | 原典init→content audit→scene/beat map→React stageとtimelineを利用 |
| eluckydog/ppt-scene-graph | 遠くの席へ、伝わる資料。6枚 | 原典OutlineSpec/create→同一本文のbeautify projectionを利用 |

茶の企画ではeditorial-luxuryの版式、石色・金の細線・装飾・controllerを保持し、字体を公式日本語字体へ置き換える。原典JSONにlayout_slotsが未定義のため、元HTMLのDOM領域へ内容の対応を保存する。未定義のmetadataを取得済みと称しない。

活版印刷の企画では独自のBRAND.mdを先に作り、紙・墨・赤の比率と書体役割を原典方式で抽出する。原典のnavigation/reveal/swipeを使い、字体を内包した単独HTMLへ日本語化する。両企画は架空で、日時・会場・費用・実施効果を発明しない。

PPTXの原典は同梱python-pptx1.0.2のparts/が固定treeで欠落しており、そのままではimportで停止した。同版の公式PyPI配布から8ファイルだけをruntime copyへ補い、元APIのcreate_from_outline→draft、beautify→projectionを実行して6枚を生成した。元原本は変更していない。公式wheelのhashとMIT、補った一覧を制作一式に記録する。

原典が宣言するparse_slideは実装・package exportに存在せず、使ったとは表示しない。beautifyのtheme引数は短いkeyではなく、元load_themeから得る表示名で実行する。採点APIは使っていない。PowerPoint16の通常exportで完成6PNGとPDFを生成し、表紙だけを初回表示。ほかの文書へ触れず、作例のみCloseしてApplication.Quitを呼んでいない。

Beatdeckは原典init、content audit、SceneDefのref/source/note、Scene/Reveal、共通worldのNodeBox+Arrow、TimelineとTypewriterを実利用。元engineを改変せず、元buildのtypecheck・bundle・offline checkが成功した。原典MITに加え、GSAP3.15のStandard No Charge Licenseを個別に保持する。Kernel Panicの第三者assetsは使用・同梱していない。

待機込み6場面15段階で、元runtimeの#1.2→#2.1と代表2PNGを担当が初回表示。QR先は指定されていないためQRなし。単独HTMLと偽らず、dist/index.html＋assetsを制作ソースと同じZIPに同梱。ユーザーの確認範囲に合わせ、元verifyの全forward/back/direct/frame比較は実施していない。

## 作例を探す

完成資料の一覧に題材・作風・スキル名の検索を追加。資料名、読み方、ページの見出し、原典名、紹介文を対象とし、形式・編集対象・作風の絞り込みと合わせて使える。入力は画面内だけで使い、保存・送信しない。

実ブラウザーで「文字のかたち」を入力し、該当1冊6枚へ絞り込めることを確認した。制作一覧の再検査は追加していない。

縦横比は元preview canvasから取り、1600×1000のKeynotが16:9の窓で切れないようにした。親のフロートと元counterが1/6→2/6へ同期することを確認した。段階表示の資料は枚数へ加算せず、場面数・段階数で案内する。依頼フォームも希望する場面数から組み立てる。

親はBeatdeckのフロート1/15→2/15を操作し、原典の題名画面が表示された。詳細に6場面/15段階、依頼フォームに初期6場面、主取得ボタンにWeb一式が表示されることを確認。PPTX美化の変更前ファイルも直接取得でき、完成版と別の取得名・hashで案内する。

## 選定時に確認した配布条件

実行未着手の候補4件に、原文と実施範囲を対応させた。[条件の記録](../data/sol-source-conditions-repository-guides.json)。実行失敗・制作済みと表示しない。

- Glissandoは固定treeにLICENSE等がなく、実取得したpackage.jsonにもlicense指定がないため、原作者の派生・再配布許諾を確認していない。
- DeckForgeは独占バイナリと埋め込まれた方法論等の改変・配布を許諾していない。repositoryファイルはインストールと使用の案内に限られ、出力物の条件とengineの条件を分ける。
- Slidev MCPはFSL-1.1-ALv2で、Permitted PurposeとCompeting Useの条件を持つ。無条件OSSと表示しない。
- VelaはELv2で、使用・派生等に許諾があるがhosted/managed serviceの機能提供に制限がある。runtime/CDNの依存はNOTICEの区分を保持する。

今回は上記4件のエンジンを実行・配布していない。現在の制作を止める理由や、全環境での実行不能という判断へ読み替えない。原文は各固定原典のURLへリンクし、制限されたコードを一式ZIPへ取り込まない。

## 統合結果

厳選57スキル・57冊328枚＋15段階。制作履歴は67リポ・72冊429枚＋15段階で、現行掲載と分ける。作り方62件・直接Markdown59件・維持するfork69件・取得用成果物227件。OSS書体は9ファミリー16ファイル、組み合わせ7種。

各原典の入力、再生成案内、短い日本語SKILL、原本・局所差分・個別条件を同梱。manifest・厳選集・サイト生成、source hashとZIPの配布作成が成功した。新しいJavaScriptの構文だけを確認し、全ZIP再実行は追加しなかった。[軽い確認の記録](../data/atelier-light-check-20261014-10.json)。全体の制作は継続中。公開push・main merge・deployは行っていない。
