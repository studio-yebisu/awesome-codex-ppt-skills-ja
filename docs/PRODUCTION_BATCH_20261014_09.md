# MCPの生成、文字の観察、テーマと参考画像からの制作

Sol 6.1の2並列で、原典4件・4冊24枚を制作し、ローカルサイトへ接続したバッチ。親は題材とデザイン判断、統合、完成資料の取得名を担当した。Astraや独立レビューは使っていない。

## 原典ごとの方式

| 原典・固定commit | 日本語作例 | 使用方式 |
| --- | --- | --- |
| masaki39/marp-mcp / 2d3f635d5b7b8f03de4e44397c9a51c8b6f7c65f | ひとつの服を、もう一度。6枚 | 原典MCPへ実stdio JSON-RPC tools/call、minimalの構造化layout、export_slideからMarp CLI 4.4.0でHTML/PDF/画像PPTXを生成 |
| Watermelon4000/sketch-note-ppt / 0729098c28a2105b3e2f6225b3afe125e3959fb6 | 文字のかたちを、観察する。6枚 | 原典sketch-notes-base.css、demoのgo()、reveal CSS、吹き出し・手描き下線・decision tree等で直接HTML/SVGを著述 |
| arifszn/slide-wright / d95ba204c9e98488b86b76ced75765ab4ec5de96 | 星を待つ、夜の天文台。6枚 | 原典の独自テーマ・2枚の試作・同じHTMLへの追加、1920×1080 frameと元engineで動く資料へ |
| dakjdakd/PPT-Design-DNA / 5d1d84cf952f16920d893b6c04bd7cb7cff9d155 | 町の道具を、借り合う。6枚 | 自作Bauhausの実描画PNGからDNAを抽出し、原典schema・Design Contract・Blueprint・Page Specsと固有guardで別のHTML企画へ |

MCP作例は原典サーバーへの操作ログとexportログを保存。Windowsでnpm shimをspawnできない箇所だけ、同じMarp CLI JSをNodeで呼ぶ局所adapterを入れた。元のMCPと生成器を別builderへ置き換えていない。HTMLは字体とCSSを内包して単独取得できる。PDFは固定、PPTXの本文と図は画像で、編集正本はMarkdown/JSON/CSS。PowerPoint実機表示は確認していない。

手描き教材は、原典が認める直接HTML著述で、必須AI画像やCLIを省略したものではない。実フォントの和文字形を見せ、SVGの線と下線、余白、意味による改行を教材にする。原典のCSSとcontroller原本を保持し、日本語のclamp・書体役割・誌面・線の動き・same-origin bridgeを局所差分へ保存する。

夜の天文台は、題材から青黒・cyan・amberと観測の円を持つテーマを作る。親がテーマを指定し、原典の2枚を育てる工程を進める。ユーザーの自律制作指示に沿って確認待ちを増やしていない。ユーザーの美術承認済みとは表示せず、原典の対話ゲートへの派生変更を記録する。

Design DNAは、前バッチのAkxan由来native PPTXのPowerPoint描画を実際に見て、参考画像として使う。画像なしでテーマを発明したとする方式へ置き換えない。原典の対話・profile保存ゲートは自律制作に合わせ、抽出パネルと判断をプロジェクト内へ保存する。元の参考作例は変更しない。

MCP・手描き・独自テーマはMIT、DNAはApache-2.0の原文と必要な表示を保持する。書体は既存の公式固定配布TTFとOFLを役割分けして利用。OS書体の抽出・専有ホストSDKの使用はしていない。衣服の会・天文台・道具棚は架空企画。文字教材の書体と声の対応は選択案で、実測効果を主張しない。

## 題名のある取得ファイル

フロートと作例の詳細で、完成HTML・PDF・PPTXのdownload名を題名へ揃える。複数の資料を集めてもdeck.pptxやindex.htmlだけの名前にならず、資料を区別できる。Windowsで使えない記号を整え、拡張子を保持する。制作原本のパスとhash、日本語SKILL・制作ZIPの正規名は維持する。

単独HTMLを取得できる場合のボタンは「Webスライドをダウンロード」、複数ファイルのZIPなら「Webスライド一式」と表示する。「星を待つ、夜の天文台.html」の取得名をサイトの実リンクで確認した。

## 確認と統合

各制作担当が必要な原典生成と主要出力の初回表示を実施。手描き教材は元controllerの1→2、独自テーマは実2枚の初回表示→同じ2sectionを保持した6枚への追加、DNAは原典必須guardのPASSと1→2を確認した。MCPは元MCPの生成・exportとPDF表紙を確認した。

親はMCPと独自テーマのフロート1→2を実際に操作。独自テーマの子frameでも「みんなで、夜を見上げる。」が表示された。新しい取得名とJavaScriptの構文、一覧・サイトの生成と配布パッケージ作成だけを確認した。全頁詳細目視・独立採点・native構造監査・全キット再実行は追加していない。

厳選53スキル・53冊310枚。制作履歴は63リポ・68冊411枚で、現行掲載と区別する。作り方58件、直接Markdown55件、維持するfork65件、取得用成果物214件。OSS書体は9ファミリー16ファイル、組み合わせ7種。DNA作例から元のBauhaus資料を開く導線を追加し、元資料から動くHTML版への導線は保持した。

全体の制作は継続中で、原209件は資料として保持する。公開push・main merge・deployは行っていない。[軽い確認の記録](../data/atelier-light-check-20261014-09.json)。
