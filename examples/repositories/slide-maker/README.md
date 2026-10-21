# 原稿から図表を作り、読み手の指摘で直す

原稿・データ・既存資料を、読者に必要な頁順と図表へ整理する。受け取るものは編集可能PPTX、全頁の描画、根拠、実施した検査と読解・批評の記録。

原典addsumtech/slides_maker、固定commit3767cc346d63ef1646082c87f15fbf0be582b152。元SKILLとMIT LICENSEを保持した日本語派生で、公式翻訳ではない。

## 用意するもの

- Python3.10+、python-pptx、原典deckkit。
- 原典render/lint環境のLibreOffice。今回だけWindowsのPowerPoint16→PDF→PDFiumを描画adapterとして使った。Yu Gothicの字体ファイルは再配布しない。
- 内容と設計を確認する独立critic、原稿を見ない独立読解者。

## 入力から仕上げる手順

1. 読者の知識と読む目的を決め、各頁の主張と根拠を対応させる。
2. 複数の構成・図案を比較し、比較条件、文字の役割、色や印の意味を定める。
3. 原典deckkitの編集可能な文字・図形・グラフを使い、判断理由を読み手に必要な位置へ置く。
4. 全頁を描画しlint・component・visual contractを確認する。独立読解と内容/設計の批評を原典CLIへ記録し、指摘を修正する。
5. 修正した版を新しい独立評価へ渡し、原典の承認とdelivery/handoffの条件を満たすまで合格扱いしない。

原典interview→content/design checkpoint→制作→render/lint→critic/blind read→修正→consentの順序を省かない。Codexでは同梱codex-runtime.mdに従い、palette/component、全頁render_selfcheck、visual contract、delivery evidence/receipt、handoff guardも実行する。批評は内容と設計の両観点を持ち、blindは計画・原稿を見る前に実画像から答える。実行不足を納品承認へ読み替えない。

適用外・注意：独立読解者を用意できない場合は原典のno-reader carve/unverifiedへ記録する。Codex adapterをClaude Code/Kimiで動かす用途、PPTX以外の納品はこの実証の対象外。

## 原典の主な使い分け

既存PPTXの修正・再設計にも使えます。まず既存資料を読んで問題を整理し、指定された内容とテンプレートを基準に直します。新しい資料では、元のコード・論文・図・データを読み、材料がなければ調査と事実確認を行います。

構成や見た目を途中で選びたい場合は共同制作モードで、方向案→構成→残りの頁の順に確認します。画像が必要な資料では生成画像と画像シリーズの規則、外部の主張や数値には引用・出典の規則を使います。大きい資料でも一つの主張を無関係な作業者へ分割せず、素材準備など独立する作業を並列化します。詳細は同梱の固定原典 `source/upstream/skills/slide-maker/SKILL.md` と、その分岐で指定される参照を読みます。

## 作例の実施範囲

探索教材5頁。線形=青、二分=紫、目的値13=茶はこの作例の割当てで、一般手順の固定値ではない。実Opusの旧版critic/blindを原典CLIへ記録し、各段に判断理由が欠けるという指摘を修復した。現在版は全5頁を制作側で実読した候補。新しい独立critic/blindとconsentは未取得で、最終gateは失敗を保持している。

1頁の配列直下では「1回」を16ptで定義する。2頁は訪問順と配列直下の16pt凡例、3頁は24ptの大小比較→左右判断、4頁は全条件グラフと1〜3の反例を見る。5頁は比較回数と未計測の秒数を分ける。

- 原典はLibreOfficeで描画する。今回のWindows作例はPowerPoint16→PDF→PDFiumを局所adapterとして使った。
- 独立読解者がいない環境は原典のno-reader carve/unverified。Codex専用adapterをClaude Code/Kimiで動かす用途や、PPTX以外の納品はこの実証の対象外。
- 実Opus Round4の指摘とblind回答は旧SHAb8f099a3…へ束縛して原典CLIに記録済み。現在版の新しい独立評価・consentは待機中で、旧承認を流用しない。
- 初回の構成・図案比較は制作後の補完。テンプレート、発表時間、質疑用頁、画像シリーズは未実施。
- component auditは固定15値の配列をカード群と検出しexit2。頁ごとの意図は原典deliveryの正式なwaiver欄へ記録し、元のcheck_components関数が受理することを確認。これは全deliveryの合格ではない。
- 作例は既に昇順の1〜15から存在する値を探す計測。回数は訪問要素数で、秒数・整列費用・未発見条件は測っていない。

現在の実行結果はQA.jsonとPROVENANCE.json、再実行はREPRODUCE.md。旧レビューは対象SHAを保持し、修正した別版へ承認を引き継がない。
