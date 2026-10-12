![AIスライド制作スキル集 日本語版](assets/banner.svg)

# AIスライド制作スキル集｜日本語版

CodexやClaude CodeなどのAIエージェントで利用できる、スライド制作スキル・ツールの日本語ガイドです。編集可能なPowerPoint、画像形式スライド、Webスライド、ビジネス資料、文書からの変換など、209件を用途別にお探しいただけます。

本ガイドは[zhuyansen/awesome-codex-ppt-skills](https://github.com/zhuyansen/awesome-codex-ppt-skills)を基に作成した非公式の日本語版です。原版の分類・比較結果を引き継ぎ、各ツールの機能情報を基に日本語で要約しています。原作者や掲載プロジェクトによる公式配布・推奨を示すものではありません。

**原版のデータ更新日：2026年10月11日／日本語版の作成日：2026年10月12日**

[原版の検索・絞り込みページ](https://agentskillshub.top/best/ppt-presentation/)は8時間ごとに更新されます。この日本語版は上記日付時点の内容をまとめたものであり、原版との自動同期は行われません。

**[作例を見ながら、6ジャンルから選ぶ →](https://studio-yebisu.github.io/awesome-codex-ppt-skills-ja/)**

ジャンル別のページでは、代表的なスライド作例・用途・編集できる場所を見比べられます。ジャンルを選ぶと、日本語の紹介文つきのプロジェクト一覧がGitHubスター数の多い順に表示され、各カードから元のリポジトリへ進めます。スター数は原版データ取得時点の数値です。全209件に画像を掲載しています。公開作例・紹介画像116件を優先し、残る93件はGitHub提供の紹介画像を表示します。GitHubの紹介画像は制作成果物ではありません。[画像の出典と利用条件](docs/プロジェクト作例の出典.md)に、元画像とライセンス原文をまとめています。

[用途から選ぶ](#choose) · [全209件を見る](#catalog) · [実測比較](docs/実測比較.md) · [出典とライセンス](docs/出典とライセンス.md)

<a id="choose"></a>

## まず、どれを選ぶ？

原作者は同一条件下で31件を実行検証し、27件から成果物を得ています。用途別の推奨候補として次の3件を挙げており、詳細な数値と検証条件は[実測比較](docs/実測比較.md)で確認できます。

| やりたいこと | 原版が挙げた候補 | 原版の実測結果 |
|---|---|---|
| 同僚がPowerPointで編集する資料を作る | [ppt-master](https://github.com/hugohe3/ppt-master) | 構造を保ったPPTX。編集可能性L3、内容評価100%、約11分。簡単な構造でよければ[claude-office-skills](https://github.com/tfriedel/claude-office-skills)も候補（L2、100%、約3分）。 |
| ブラウザで発表する資料を作る | [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | アニメーションと標準の表を含むWebスライド。L5、内容評価100%。編集はコードで行う。 |
| 見た目のインパクトを重視する | [rw-consulting-ppt](https://github.com/Pikapika260214/rw-consulting-ppt) | 内容評価100%の画像形式スライド。L0のため、文字変更には作り直しが必要。 |

後からテキストを修正したい場合は、出力形式が画像でないかを事前に確認してください。原版の実測では、gpt-image2-ppt-skillsおよびcodex-ppt-skillの出力はスライド全体が1枚の画像となっており、大幅な手直しが必要でした。[image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill)は、そうした画像形式のスライドを編集可能な要素へ再構成する際の候補となります。

なお、原版の実測では26件中10件が内容評価100%を記録しました。内容評価の高さだけで判断せず、出力後にどの要素を編集できるか（編集可能性）もあわせて確認すると、用途に適したツールを選びやすくなります。

## 作りたい資料から探す

| 種類 | 件数 | どんな資料を作るか |
|---|---:|---|
| [🧱 総合ツール・フレームワーク](#type-general) | 20 | 複数の制作方法をまとめたツール集や、エージェントによる制作システム。 |
| [📝 編集可能なPPTX](#type-pptx) | 83 | PowerPointで文字や図形を編集するための資料制作・変換ツール。 |
| [🖼 画像形式のスライド](#type-image) | 7 | ページ全体を画像として作る方式。文字の変更には再生成や再構成が必要。 |
| [🌐 Webスライド](#type-html) | 57 | ブラウザで表示する資料。reveal.js・Slidevなどによる制作や、動きのある演出。 |
| [💼 ビジネス・コンサルティング](#type-business) | 13 | 提案、報告、ピッチなど、ビジネス用途を重視した資料制作。 |
| [📄 文書からスライドへ](#type-convert) | 29 | 論文・PDF・記事・Markdownなどをもとに資料を作るツール。 |

<a id="catalog"></a>

## ツール一覧の読み方

各一覧表の★は、原版データ取得時点のスター数です。

**導入時のセキュリティ評価**は、元サイトのAgent Skills HubがREADMEや導入手順を自動チェックした結果です。安全性を保証するものではありません。

Webのプロジェクト一覧にも、同じ原版評価を「信頼度」として表示しています。各カードの「判定を見る」からAgent Skills Hubの詳細へ進めます。表示は2026年10月11日の原版データに基づき、作品の品質評価ではありません。

- 🟢 **問題なし**：原版のSAFEに相当。
- 🟡 **要注意**：原版のCAUTIONに相当。
- 🔴 **高リスク**：原版のUNSAFEに相当。
- ⚪ **未評価**：原版のpendingに相当。

紹介文の日本語化は、各ツール自体の日本語対応を示すものではありません。導入方法、動作要件、料金、必要なAPIキー、ライセンス条件などは、各リンク先の最新情報をご確認ください。

<a id="type-general"></a>

## 🧱 総合ツール・フレームワーク（20件）

複数の制作方法をまとめたツール集や、エージェントによる制作システム。

[原版のこの分類を見る](https://agentskillshub.top/best/ppt-presentation/#type-general)

| ツール | ★ | できること | 導入時のセキュリティ評価 |
|---|---:|---|---|
| [wuyoscar/GPT-Image2-Skill](https://github.com/wuyoscar/GPT-Image2-Skill) | 5,708 | GPT Imageによる画像生成・編集のプロンプト集と、エージェント向けスキル・CLI。 | [🟢 問題なし](https://agentskillshub.top/skill/wuyoscar/GPT-Image2-Skill/) |
| [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) | 837 | Claude CodeでPowerPoint、Word、Excel、PDFの作成・編集を行うスキル集。 | [🟢 問題なし](https://agentskillshub.top/skill/tfriedel/claude-office-skills/) |
| [mucsbr/ppt-agent-workflow-san](https://github.com/mucsbr/ppt-agent-workflow-san) | 645 | 対話を通じて段階的にプレゼンテーション資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/mucsbr/ppt-agent-workflow-san/) |
| [minhnv0807/ai-business-skills](https://github.com/minhnv0807/ai-business-skills) | 610 | マーケティング向けの多言語スキル138種。制作・デザイン・運用などの業務手順を収録。 | [🟢 問題なし](https://agentskillshub.top/skill/minhnv0807/ai-business-skills/) |
| [minorun365/minorun-marp-skill](https://github.com/minorun365/minorun-marp-skill) | 404 | Marpの登壇資料向けスキル集。ストーリー構成、図表、デザインのバランスと黒地テーマを扱う。 | [🟢 問題なし](https://agentskillshub.top/skill/minorun365/minorun-marp-skill/) |
| [rsrohan99/presenter](https://github.com/rsrohan99/presenter) | 186 | 複数のAIエージェントが連携し、音声ナレーション付きプレゼン資料を作成するツール。 | [🟢 問題なし](https://agentskillshub.top/skill/rsrohan99/presenter/) |
| [Sven-LI-sankyuu/presentation-skills](https://github.com/Sven-LI-sankyuu/presentation-skills) | 175 | 編集可能なPPTの共同作成や、Webデモの音声付き動画化に対応したCodex CLI向けスキル集。 | [🟢 問題なし](https://agentskillshub.top/skill/Sven-LI-sankyuu/presentation-skills/) |
| [StarryKit/starry-slides](https://github.com/StarryKit/starry-slides) | 95 | Codex、Claude Code、Cursorなどで、編集可能なスライドやポスター、SNS画像を制作するツール。 | [🟢 問題なし](https://agentskillshub.top/skill/StarryKit/starry-slides/) |
| [gnipbao/knowledge-cat-ppt-skill](https://github.com/gnipbao/knowledge-cat-ppt-skill) | 86 | ストーリー構成に基づきPPT・HTML・画像形式で資料を作成し、出力先の選択と品質確認を行うスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/gnipbao/knowledge-cat-ppt-skill/) |
| [SpaceZephyr/space-multi-design-ppt](https://github.com/SpaceZephyr/space-multi-design-ppt) | 81 | ブランドのデザインシステムに準拠して資料を作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/SpaceZephyr/space-multi-design-ppt/) |
| [appautomaton/presentation](https://github.com/appautomaton/presentation) | 62 | 構成設計からブランド設定、PDF制作、編集可能なPPTX制作までを一連で行うスキル集。 | [🟢 問題なし](https://agentskillshub.top/skill/appautomaton/presentation/) |
| [touying-typ/seaslides](https://github.com/touying-typ/seaslides) | 44 | TypstとTouyingを用いてプレゼン資料を作成するAIスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/touying-typ/seaslides/) |
| [wangzan101/html-to-ppt-pdf](https://github.com/wangzan101/html-to-ppt-pdf) | 37 | guizang-ppt-skillのHTML資料を、オフライン発表用PDFおよび画像形式のPPTXへ変換するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/wangzan101/html-to-ppt-pdf/) |
| [prodigeproject/pradaslides](https://github.com/prodigeproject/pradaslides) | 16 | 用途や環境に応じ、PPTX・HTML・PDFの作成と資料構成の組み立てを支援するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/prodigeproject/pradaslides/) |
| [ConnorRX56/presentation-delivery-skills](https://github.com/ConnorRX56/presentation-delivery-skills) | 12 | 短い依頼から編集可能なPPTXを作るスキル。見た目と、依頼内容に沿っているかを確認する。 | [🟢 問題なし](https://agentskillshub.top/skill/ConnorRX56/presentation-delivery-skills/) |
| [att6113/ppt-design-system](https://github.com/att6113/ppt-design-system) | 11 | 5種のテーマと10種のレイアウトを備え、HTMLとPPTXの双方を出力できるデザインシステム。 | [🟢 問題なし](https://agentskillshub.top/skill/att6113/ppt-design-system/) |
| [ThunderOne18/ppt-expert-team](https://github.com/ThunderOne18/ppt-expert-team) | 10 | 記事や原稿から8段階で資料を作成し、HTML・画像・PPTX形式で出力するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/ThunderOne18/ppt-expert-team/) |
| [zhuyansen/awesome-codex-ppt-skills](https://github.com/zhuyansen/awesome-codex-ppt-skills) | 10 | 本日本語版の原版。AIエージェント向けスライド作成ツールを用途別にまとめた一覧。 | [🟢 問題なし](https://agentskillshub.top/skill/zhuyansen/awesome-codex-ppt-skills/) |
| [xukp20/build-beamer-slides](https://github.com/xukp20/build-beamer-slides) | 8 | Beamer資料の構成設計、レンダリング、表示確認を行うCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/xukp20/build-beamer-slides/) |
| [chunyifish/soil-teaching-slides](https://github.com/chunyifish/soil-teaching-slides) | 6 | SOIL形式の授業資料を作成するスキル。PPTX、NotebookLM、オフライン用HTMLに対応。 | [🟢 問題なし](https://agentskillshub.top/skill/chunyifish/soil-teaching-slides/) |

[↑ 用途別の一覧に戻る](#choose)

<a id="type-pptx"></a>

## 📝 編集可能なPPTX（83件）

PowerPointで文字や図形を編集するための資料制作・変換ツール。

[原版のこの分類を見る](https://agentskillshub.top/best/ppt-presentation/#type-pptx)

| ツール | ★ | できること | 導入時のセキュリティ評価 |
|---|---:|---|---|
| [icip-cas/PPTAgent](https://github.com/icip-cas/PPTAgent) | 5,099 | 生成したスライドを自己評価しながら改善する、PowerPoint作成用エージェントフレームワーク。 | [🟢 問題なし](https://agentskillshub.top/skill/icip-cas/PPTAgent/) |
| [GordenSun/GordenPPTSkill](https://github.com/GordenSun/GordenPPTSkill) | 3,331 | 17種類の中国語PPTXテンプレートで、レイアウトを保って文字を編集するスキル。利用は個人・研究目的に限定。 | [🟢 問題なし](https://agentskillshub.top/skill/GordenSun/GordenPPTSkill/) |
| [ningzimu/image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill) | 2,864 | スライド画像、PDF、画像化されたPPTXを編集可能なPowerPointへ再構築するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/ningzimu/image-to-editable-ppt-skill/) |
| [GordenSun/GordenSuperPPTSkills](https://github.com/GordenSun/GordenSuperPPTSkills) | 2,068 | GPTで生成したスライド画像を、編集可能なPPTXに変換するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/GordenSun/GordenSuperPPTSkills/) |
| [GongRzhe/Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server) | 1,854 | python-pptxを利用し、MCP経由でPowerPoint資料の作成・編集を行うサーバー。 | [🟢 問題なし](https://agentskillshub.top/skill/GongRzhe/Office-PowerPoint-MCP-Server/) |
| [johnson7788/MultiAgentPPT](https://github.com/johnson7788/MultiAgentPPT) | 1,641 | A2A・MCP・ADKを連携させ、複数エージェントの協調と並列処理により資料を作成するシステム。 | [🟢 問題なし](https://agentskillshub.top/skill/johnson7788/MultiAgentPPT/) |
| [JuneYaooo/gpt-image2-ppt-skills](https://github.com/JuneYaooo/gpt-image2-ppt-skills) | 1,347 | 参考PPTXの配置をGPT Imageで再現し内容を差し替えるスキル。10種類のスタイルを収録。 | [🟢 問題なし](https://agentskillshub.top/skill/JuneYaooo/gpt-image2-ppt-skills/) |
| [sunbigfly/ppt-agent-skills](https://github.com/sunbigfly/ppt-agent-skills) | 907 | コードベースで、ソフトウェア開発のような工程に沿って資料を構築するフレームワーク。 | [🟢 問題なし](https://agentskillshub.top/skill/sunbigfly/ppt-agent-skills/) |
| [addsumtech/slides_maker](https://github.com/addsumtech/slides_maker) | 549 | 論文・コード・文書を編集可能なPPTXに変換。図表、数式、発表者ノート、アニメーション、独立レビューに対応。 | [🟢 問題なし](https://agentskillshub.top/skill/addsumtech/slides_maker/) |
| [AI272/speaker](https://github.com/AI272/speaker) | 460 | 既存PPTXの構造解析、OCR、画像確認をもとに、各スライドの発表原稿を作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/AI272/speaker/) |
| [barun-saha/slide-deck-ai](https://github.com/barun-saha/slide-deck-ai) | 377 | 対話形式でAIとやり取りしながらPowerPointプレゼン資料を作成するツール。 | [🟢 問題なし](https://agentskillshub.top/skill/barun-saha/slide-deck-ai/) |
| [sunchaokun/PPT-Design-Skill](https://github.com/sunchaokun/PPT-Design-Skill) | 321 | 多様なスタイル指定、AI画像生成、精密な配置調整により編集可能なPPTXを出力する制作スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/sunchaokun/PPT-Design-Skill/) |
| [zouchenzhen/thesis-defense-pptx-skill](https://github.com/zouchenzhen/thesis-defense-pptx-skill) | 267 | 論文PDFやLaTeXから、指定テンプレートを維持した編集可能な学位審査用PowerPoint資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/zouchenzhen/thesis-defense-pptx-skill/) |
| [thePlannerIvan/planners-ppt-hell](https://github.com/thePlannerIvan/planners-ppt-hell) | 234 | 企画職向けのPowerPoint資料制作スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/thePlannerIvan/planners-ppt-hell/) |
| [EveryInc/hands-on-deck](https://github.com/EveryInc/hands-on-deck) | 219 | JSON形式の編集指示により、CLIからPPTXの確認・作成・編集・検証を行うエージェント向けツール。 | [🟢 問題なし](https://agentskillshub.top/skill/EveryInc/hands-on-deck/) |
| [wwe-dog/ppt-image2-editable-rebuild](https://github.com/wwe-dog/ppt-image2-editable-rebuild) | 200 | 複雑な図は部分画像として残し、文字・図形・矢印などを編集可能なPowerPoint標準の要素に再構成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/wwe-dog/ppt-image2-editable-rebuild/) |
| [w1163222589-coder/slide-image-to-editable-pptx](https://github.com/w1163222589-coder/slide-image-to-editable-pptx) | 196 | スライドのスクリーンショットを編集可能なPowerPoint形式に変換するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/w1163222589-coder/slide-image-to-editable-pptx/) |
| [xdmlxdml/beamer2pptx](https://github.com/xdmlxdml/beamer2pptx) | 180 | BeamerのPDFを、編集可能な数式を含むPowerPoint資料に変換するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/xdmlxdml/beamer2pptx/) |
| [jinwyp/open-ppt-skill](https://github.com/jinwyp/open-ppt-skill) | 161 | 編集可能なPPTDおよびPPTXを生成し、ローカル環境でブラウザ編集画面も提供するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/jinwyp/open-ppt-skill/) |
| [Akxan/ppt-agent-skill](https://github.com/Akxan/ppt-agent-skill) | 159 | 26種のスタイルと18種の図表を備え、HTMLおよび編集可能なPPTXを作成するClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Akxan/ppt-agent-skill/) |
| [knight6669/knight-imagetopptx-skill](https://github.com/knight6669/knight-imagetopptx-skill) | 128 | スライド画像の内容と構造を解析し、編集可能なPPTXに変換するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/knight6669/knight-imagetopptx-skill/) |
| [Noi1r/powerpoint-skill](https://github.com/Noi1r/powerpoint-skill) | 124 | 数式やGraphviz・Mermaid・TikZの図を含むPowerPointを作成する、AIコーディング支援用スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Noi1r/powerpoint-skill/) |
| [Ayushmaniar/powerpoint-mcp](https://github.com/Ayushmaniar/powerpoint-mcp) | 119 | pywin32を用いてWindows上のPowerPointを自動操作するMCPサーバー。 | [🟢 問題なし](https://agentskillshub.top/skill/Ayushmaniar/powerpoint-mcp/) |
| [henryhyw/slidepoise](https://github.com/henryhyw/slidepoise) | 102 | 柔軟なビジュアル設計と編集可能なPowerPoint出力を両立したエージェント向けツール。 | [🟢 問題なし](https://agentskillshub.top/skill/henryhyw/slidepoise/) |
| [Hasasasa/html-to-editable-pptx](https://github.com/Hasasasa/html-to-editable-pptx) | 81 | HTML資料をPowerPointのテキストボックスなどに変換。エージェント向けスキルとPython CLIを提供。 | [🟢 問題なし](https://agentskillshub.top/skill/Hasasasa/html-to-editable-pptx/) |
| [ACTAshui/sjtu-ppt-template-skill](https://github.com/ACTAshui/sjtu-ppt-template-skill) | 78 | 上海交通大学スタイルのテンプレートで編集可能なPowerPointを作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/ACTAshui/sjtu-ppt-template-skill/) |
| [siril9/presentation-skill](https://github.com/siril9/presentation-skill) | 75 | JSONからの再生成、標準図表、画像確認に対応し、内容重視で編集可能なPowerPointを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/siril9/presentation-skill/) |
| [wiltonesten-web/codeximage-to-editable-ppt-v2-1](https://github.com/wiltonesten-web/codeximage-to-editable-ppt-v2-1) | 70 | 画像スライドを文字や図形が編集可能なPowerPointへ再構成する高精度版スキル。 | [🟡 要注意](https://agentskillshub.top/skill/wiltonesten-web/codeximage-to-editable-ppt-v2-1/) |
| [NeekChaw/mcp-server-okppt](https://github.com/NeekChaw/mcp-server-okppt) | 69 | MCP経由でSVGを生成してPPTXに配置し、図のベクター形式を保持するサーバー。 | [🟢 問題なし](https://agentskillshub.top/skill/NeekChaw/mcp-server-okppt/) |
| [gnuhpc/ppt-master-plus](https://github.com/gnuhpc/ppt-master-plus) | 65 | 編集可能なPPTX生成、デザイン調整、発表者ノート、プレビュー、テンプレートに対応したスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/gnuhpc/ppt-master-plus/) |
| [DSY-Xueai/image2editable](https://github.com/DSY-Xueai/image2editable) | 56 | 画像・PDF・画像化されたPPTXを編集可能なPowerPointに変換するCodex・Claude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/DSY-Xueai/image2editable/) |
| [wiltonesten-web/codeximage-to-editable-ppt-v1](https://github.com/wiltonesten-web/codeximage-to-editable-ppt-v1) | 51 | 画像スライドを編集可能なPowerPointに再構成する、トークン消費を抑えたv1版スキル。 | [🟡 要注意](https://agentskillshub.top/skill/wiltonesten-web/codeximage-to-editable-ppt-v1/) |
| [TianLin0509/img2ppt-lite](https://github.com/TianLin0509/img2ppt-lite) | 48 | 参考画像から編集可能なテキスト、個別移動可能な画像要素、補完された背景を含むPPTXを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/TianLin0509/img2ppt-lite/) |
| [opitaru-sys/deck-dna](https://github.com/opitaru-sys/deck-dna) | 44 | 参考資料のデザインとテキスト量を解析し、描画結果を確認しながらPPTXを作成するClaude向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/opitaru-sys/deck-dna/) |
| [huashu996/PPT-Framework-Skill](https://github.com/huashu996/PPT-Framework-Skill) | 43 | 参考図や論文をもとに、編集可能な学術用構成図や技術ロードマップを作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/huashu996/PPT-Framework-Skill/) |
| [qybaihe/codex-ppt](https://github.com/qybaihe/codex-ppt) | 42 | スライド画像を生成し、PDFへの結合や、文字・画像レイヤーを編集可能なPPTXへ再構成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/qybaihe/codex-ppt/) |
| [AIPMAndy/PPTskill](https://github.com/AIPMAndy/PPTskill) | 38 | AIを用いてPowerPoint標準の要素で構成された、編集可能なPPTXを生成するスキル。 | [🟡 要注意](https://agentskillshub.top/skill/AIPMAndy/PPTskill/) |
| [kongzhecn/image-svg-pptx-pro-skill](https://github.com/kongzhecn/image-svg-pptx-pro-skill) | 38 | スライドのスクリーンショットや生成画像をSVGへ再構成し、編集可能なPowerPointに変換するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/kongzhecn/image-svg-pptx-pro-skill/) |
| [2slides/mcp-2slides](https://github.com/2slides/mcp-2slides) | 34 | AIプレゼン資料作成サービス「2slides」と連携するMCPサーバー。 | [🟢 問題なし](https://agentskillshub.top/skill/2slides/mcp-2slides/) |
| [riteouschris-max/journal-club-ppt](https://github.com/riteouschris-max/journal-club-ppt) | 33 | 学術論文を基に、根拠を明記した文献紹介・輪読会向けのスライドを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/riteouschris-max/journal-club-ppt/) |
| [jiadizhunine/deepPPT](https://github.com/jiadizhunine/deepPPT) | 29 | 研究発表用の編集可能なPPTXを生成し、描画結果の品質確認まで行う軽量フレームワーク。 | [🟡 要注意](https://agentskillshub.top/skill/jiadizhunine/deepPPT/) |
| [HututuWorks/sci-diagram-pptx](https://github.com/HututuWorks/sci-diagram-pptx) | 27 | 科学分野の概念図・機構図・フロー図を、出典に基づく編集可能なPowerPoint標準の要素に再構成するスキル。 | [🟡 要注意](https://agentskillshub.top/skill/HututuWorks/sci-diagram-pptx/) |
| [LearnAIHubC/LearnDeck](https://github.com/LearnAIHubC/LearnDeck) | 26 | テーマ、メモ、教材、アウトラインから編集可能なPowerPoint資料を作成するCodex向けツール。 | [🟢 問題なし](https://agentskillshub.top/skill/LearnAIHubC/LearnDeck/) |
| [zairuilab/consulting-deck](https://github.com/zairuilab/consulting-deck) | 26 | 複雑な入力情報から、出典を追跡可能なコンサルティング調PPTXを作成。レイアウト設計と図表データの検証を重視。 | [🟢 問題なし](https://agentskillshub.top/skill/zairuilab/consulting-deck/) |
| [Mr-Q526/PPTMaker-skill](https://github.com/Mr-Q526/PPTMaker-skill) | 24 | テーマやMarkdown、原稿から資料を作成し、自然言語によるページやパーツの修正を経て編集可能なPPTXを出力するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Mr-Q526/PPTMaker-skill/) |
| [ewkzcz/bili-2-ppt](https://github.com/ewkzcz/bili-2-ppt) | 23 | Bilibili動画のURLから、内容とキャプチャ画像を抽出してPPTなどのドキュメントを生成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/ewkzcz/bili-2-ppt/) |
| [ziqihe10-droid/shuike-pptskill](https://github.com/ziqihe10-droid/shuike-pptskill) | 23 | 授業発表向けにPowerPoint資料とWordの発表原稿を同時作成。図表生成と5種類のスタイルに対応。 | [🟢 問題なし](https://agentskillshub.top/skill/ziqihe10-droid/shuike-pptskill/) |
| [liustack/pptwise](https://github.com/liustack/pptwise) | 19 | ローカル環境で編集可能なPowerPointを作成するスキルおよびDSHプラグイン。レンダリングにアカウントやAPIキーは不要。 | [🟢 問題なし](https://agentskillshub.top/skill/liustack/pptwise/) |
| [gonta223/japanese-corporate-pptx-skill](https://github.com/gonta223/japanese-corporate-pptx-skill) | 18 | 日本企業や官公庁の資料に特有のポンチ絵（一枚図）を、編集可能なPowerPoint標準の要素で作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/gonta223/japanese-corporate-pptx-skill/) |
| [mpuig/agent-slides](https://github.com/mpuig/agent-slides) | 15 | 組み合わせ可能な7種類のスキルと専用CLIで構成された、PowerPoint資料生成ツール。 | [🟢 問題なし](https://agentskillshub.top/skill/mpuig/agent-slides/) |
| [zsc58/ustc-ppt-template](https://github.com/zsc58/ustc-ppt-template) | 15 | 中国科学技術大学風の学術PPTテンプレート。15ページの基本骨格、ページ間ナビゲーション、LaTeX数式処理を収録。 | [🔴 高リスク](https://agentskillshub.top/skill/zsc58/ustc-ppt-template/) |
| [fengting124/paper-figure-pptx-skill](https://github.com/fengting124/paper-figure-pptx-skill) | 14 | 学術論文の図を編集可能なPPTXに再構成し、LibreOfficeで検証するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/fengting124/paper-figure-pptx-skill/) |
| [ABYR1206/claude-skill-hand-drawn-slides](https://github.com/ABYR1206/claude-skill-hand-drawn-slides) | 12 | 手描きスケッチ風のPowerPoint章扉スライドを作成するClaude向けスキル。40種類のSVGイラストを収録。 | [🟢 問題なし](https://agentskillshub.top/skill/ABYR1206/claude-skill-hand-drawn-slides/) |
| [Changhooo/ppt-image-redraw-skill](https://github.com/Changhooo/ppt-image-redraw-skill) | 12 | 研究用の図をPowerPointで描き直し、原図との対応を確認するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Changhooo/ppt-image-redraw-skill/) |
| [artifact-kit/html-to-pptx-skill](https://github.com/artifact-kit/html-to-pptx-skill) | 12 | HTMLページをPptxGenJSのJSX表現を経由して、編集可能なPowerPoint資料に変換するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/artifact-kit/html-to-pptx-skill/) |
| [Aham-AIAPP/aham-ppt](https://github.com/Aham-AIAPP/aham-ppt) | 10 | パラメータ化されたレイアウト集を基に、整った編集可能なPPTXを生成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Aham-AIAPP/aham-ppt/) |
| [algerchen2024/image-to-editable-pptx](https://github.com/algerchen2024/image-to-editable-pptx) | 10 | スライド画像をPageIRとPptxGenJSで、原図に沿う編集可能なPowerPointに再構成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/algerchen2024/image-to-editable-pptx/) |
| [fredliu168/html_to_editable_ppt_skill](https://github.com/fredliu168/html_to_editable_ppt_skill) | 10 | HTMLページを編集可能なPowerPoint形式に変換するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/fredliu168/html_to_editable_ppt_skill/) |
| [marcozhou26/one-slide](https://github.com/marcozhou26/one-slide) | 10 | 短いメモや完成原稿から、出典情報を保持した編集可能な1枚のスライドを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/marcozhou26/one-slide/) |
| [tangonho/iml-pptx](https://github.com/tangonho/iml-pptx) | 10 | テキストやスライド画像を、編集可能な文字・図形を含むPPTXに再構成。画像生成機能の利用にはOpenAIのAPIキーが必要。 | [🟢 問題なし](https://agentskillshub.top/skill/tangonho/iml-pptx/) |
| [YingYveltal/bento-ppt-skill](https://github.com/YingYveltal/bento-ppt-skill) | 9 | 入力テーマから16:9比率のBento Grid風SVGスライドを作成し、HTMLプレビューと編集可能なPowerPointを出力するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/YingYveltal/bento-ppt-skill/) |
| [bruc3van/bruce-pptx-generator](https://github.com/bruc3van/bruce-pptx-generator) | 8 | 指示内容に応じて、AIエージェントがプログラムからPowerPoint資料を構築するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/bruc3van/bruce-pptx-generator/) |
| [vedraut/slidesage](https://github.com/vedraut/slidesage) | 8 | ストーリー構成と学習設計をもとに静的なPPTXを作る、特定のモデルに依存しないスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/vedraut/slidesage/) |
| [Angel-Gril/Kimi-PPT-Skills](https://github.com/Angel-Gril/Kimi-PPT-Skills) | 7 | Kimi Slides形式のPPTDとPPTXを扱う非公式スキル。生成・編集・出力に対応し、作者は学習・研究用と案内。 | [🟢 問題なし](https://agentskillshub.top/skill/Angel-Gril/Kimi-PPT-Skills/) |
| [Categorytyy/ppt-master](https://github.com/Categorytyy/ppt-master) | 7 | 要件とデザイン方針を整理し、PptxGenJSのコードからPPTXを作るスキル。複数のテンプレートやテーマを収録。 | [🟢 問題なし](https://agentskillshub.top/skill/Categorytyy/ppt-master/) |
| [GX-Alex/html2pptx](https://github.com/GX-Alex/html2pptx) | 7 | ブラウザでレンダリングされたHTMLやWebDeckスライドを、編集可能なPPTXに変換するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/GX-Alex/html2pptx/) |
| [LY2260789/routegraph-skill](https://github.com/LY2260789/routegraph-skill) | 7 | 参考画像からフロー図や経路図を認識し、編集可能なPowerPoint図形として再構築するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/LY2260789/routegraph-skill/) |
| [astro-koko/ppt-lai](https://github.com/astro-koko/ppt-lai) | 7 | 2000年代風デザインのプレゼン資料を生成・リメイクするAIスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/astro-koko/ppt-lai/) |
| [dacnay816y62-hub/FANTASY-ppt-1](https://github.com/dacnay816y62-hub/FANTASY-ppt-1) | 7 | 企画案やコンセプトの初期提案向けプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/dacnay816y62-hub/FANTASY-ppt-1/) |
| [eluckydog/ppt-scene-graph](https://github.com/eluckydog/ppt-scene-graph) | 7 | PPTX内の要素座標、重なり順、空間関係を構造化データとして抽出し、AIによるレイアウト解析を支援するツール。 | [🟢 問題なし](https://agentskillshub.top/skill/eluckydog/ppt-scene-graph/) |
| [Brusdeylins/ppt-skill](https://github.com/Brusdeylins/ppt-skill) | 6 | スキーマ検証付き操作により、テンプレートに沿ったPPTXの作成・編集を実行するエージェント向けCLI。 | [🟢 問題なし](https://agentskillshub.top/skill/Brusdeylins/ppt-skill/) |
| [billLiao/PPT-Design-Skill](https://github.com/billLiao/PPT-Design-Skill) | 6 | 複数のデザインスタイルを適用し、PowerPointファイルを直接生成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/billLiao/PPT-Design-Skill/) |
| [huhuhu301/ppt-image-rebuilder](https://github.com/huhuhu301/ppt-image-rebuilder) | 6 | 参考画像をPowerPoint標準の編集可能な要素に再構成するCodexプラグイン。 | [🟢 問題なし](https://agentskillshub.top/skill/huhuhu301/ppt-image-rebuilder/) |
| [lirunjie0510/ppt-visual-reconstruction](https://github.com/lirunjie0510/ppt-visual-reconstruction) | 6 | 原図との対応を重視して、画像から編集可能なPPTXを作るCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/lirunjie0510/ppt-visual-reconstruction/) |
| [Enei7/ppt-rebuild-skills](https://github.com/Enei7/ppt-rebuild-skills) | 5 | PDF資料を、Office数式と原図の切り出し画像を含む編集可能なPPTXに変換するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Enei7/ppt-rebuild-skills/) |
| [Kevinyyy1/image-to-editable-pptx-v2](https://github.com/Kevinyyy1/image-to-editable-pptx-v2) | 5 | スライド画像を構成要素に分解して編集可能なPowerPointへ再構成し、スクリプトベースで表示品質を検証するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Kevinyyy1/image-to-editable-pptx-v2/) |
| [Liuguanyi2125/editable-pptx-skill](https://github.com/Liuguanyi2125/editable-pptx-skill) | 5 | レイヤー単位で編集可能なPowerPointを生成する、CodexおよびClaude向けスキルとNode.js製ツールのセット。 | [🟢 問題なし](https://agentskillshub.top/skill/Liuguanyi2125/editable-pptx-skill/) |
| [MiiKiyoshi/html-mcp-web](https://github.com/MiiKiyoshi/html-mcp-web) | 5 | AIが生成したスライドをブラウザ上でプレビューし、PowerPoint形式で出力するツール。 | [🟢 問題なし](https://agentskillshub.top/skill/MiiKiyoshi/html-mcp-web/) |
| [chenyu896235554-boop/lapian-storyboard](https://github.com/chenyu896235554-boop/lapian-storyboard) | 5 | 動画のショット解析と代表フレーム抽出を行い、横長レイアウトの絵コンテPPTを作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/chenyu896235554-boop/lapian-storyboard/) |
| [concertoy/glissando](https://github.com/concertoy/glissando) | 5 | AIエージェントによるコードベースのプレゼン資料作成を支援するツール。 | [🟢 問題なし](https://agentskillshub.top/skill/concertoy/glissando/) |
| [gtoxlili/deckforge](https://github.com/gtoxlili/deckforge) | 5 | AIエージェントからのインストールおよびスクリプト実行に対応したPowerPoint生成CLI。 | [🔴 高リスク](https://agentskillshub.top/skill/gtoxlili/deckforge/) |
| [qianmo-qp/zjlab-academic-pptx-sklls](https://github.com/qianmo-qp/zjlab-academic-pptx-sklls) | 5 | 研究室での技術報告や学術発表用のPPTXを作るスキル集。 | [🟢 問題なし](https://agentskillshub.top/skill/qianmo-qp/zjlab-academic-pptx-sklls/) |
| [xiongwenhao112/ppt-template-fill](https://github.com/xiongwenhao112/ppt-template-fill) | 5 | 手持ちのPPTXテンプレートにAIがコンテンツを流し込み、既存レイアウトを維持したまま資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/xiongwenhao112/ppt-template-fill/) |

[↑ 用途別の一覧に戻る](#choose)

<a id="type-image"></a>

## 🖼 画像形式のスライド（7件）

ページ全体を画像として作る方式。文字の変更には再生成や再構成が必要。

[原版のこの分類を見る](https://agentskillshub.top/best/ppt-presentation/#type-image)

| ツール | ★ | できること | 導入時のセキュリティ評価 |
|---|---:|---|---|
| [ningzimu/codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill) | 6,696 | GPT Imageでスライド全体の画像を生成し、画像形式のPowerPoint資料として構築するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/ningzimu/codex-ppt-skill/) |
| [NyxTides/ppt-image-first](https://github.com/NyxTides/ppt-image-first) | 1,225 | Codex、Claude Code、OpenCode環境で、画像主体のプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/NyxTides/ppt-image-first/) |
| [stevenjinlong/awesome-ppt-skills](https://github.com/stevenjinlong/awesome-ppt-skills) | 70 | 短いプロンプトからGPT Imageを用いてスライド全体の画像を生成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/stevenjinlong/awesome-ppt-skills/) |
| [moongiadventures-dev/handdrawn-ppt](https://github.com/moongiadventures-dev/handdrawn-ppt) | 8 | キャラクター画像を活かした手描き風スライドを作成するClaude向けスキル。文献調査、出典明記、図表描画に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/moongiadventures-dev/handdrawn-ppt/) |
| [Scott-Du/codex-ppt](https://github.com/Scott-Du/codex-ppt) | 7 | Codexの内蔵画像生成機能で各スライドの画像を1枚ずつ作成し、画像形式のPPTXとしてまとめるスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Scott-Du/codex-ppt/) |
| [rocsgh/ppt-zen](https://github.com/rocsgh/ppt-zen) | 3 | AIが生成したスライドのデザインや視覚的表現を評価・判断するための補助ツール。 | [🟢 問題なし](https://agentskillshub.top/skill/rocsgh/ppt-zen/) |
| [uuoov/ppt-image-share-builder](https://github.com/uuoov/ppt-image-share-builder) | 1 | スライド画像、確認用一覧、PPTX、時間配分付きの発表原稿を作るCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/uuoov/ppt-image-share-builder/) |

[↑ 用途別の一覧に戻る](#choose)

<a id="type-html"></a>

## 🌐 Webスライド（57件）

ブラウザで表示する資料。reveal.js・Slidevなどによる制作や、動きのある演出。

[原版のこの分類を見る](https://agentskillshub.top/best/ppt-presentation/#type-html)

| ツール | ★ | できること | 導入時のセキュリティ評価 |
|---|---:|---|---|
| [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) | 30,453 | コーディングエージェントのフロントエンド開発機能を活用し、Web形式のスライドを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/zarazhangrui/frontend-slides/) |
| [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | 27,606 | 雑誌風およびスイススタイルのHTMLスライドを生成。画像用プロンプト、SNS表紙、WebGLや軽量表示に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/op7418/guizang-ppt-skill/) |
| [chuspeeism/dashi-ppt-skill](https://github.com/chuspeeism/dashi-ppt-skill) | 9,375 | 複数のテーマからブラウザ上で編集可能なスライドを作成し、HTML・PDF・PPTX形式で出力するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/chuspeeism/dashi-ppt-skill/) |
| [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) | 8,635 | 24種のテーマ、31種のレイアウト、20種以上のアニメーションを備えたHTMLプレゼン資料作成スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/lewislulu/html-ppt-skill/) |
| [archlizheng/frontend-slides-editable](https://github.com/archlizheng/frontend-slides-editable) | 527 | ドラッグやリサイズ操作でHTMLスライドを編集可能。並べ替え、ローカル保存、出力、PPTXからWeb形式への変換に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/archlizheng/frontend-slides-editable/) |
| [ryanbbrown/revealjs-skill](https://github.com/ryanbbrown/revealjs-skill) | 415 | reveal.jsを用いたプレゼン資料を作成する、コーディングエージェント向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/ryanbbrown/revealjs-skill/) |
| [robonuggets/marp-slides](https://github.com/robonuggets/marp-slides) | 324 | Marp向けのClaude Codeスキル。22種の作例、SVG図表、明暗テーマ、ダッシュボード用パーツを収録。 | [🟢 問題なし](https://agentskillshub.top/skill/robonuggets/marp-slides/) |
| [daniel-style/magic-slide](https://github.com/daniel-style/magic-slide) | 172 | Magic Move風の滑らかな画面遷移を備えた、単独で動作するHTMLプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/daniel-style/magic-slide/) |
| [code-on-sunday/slide-deck-generator](https://github.com/code-on-sunday/slide-deck-generator) | 151 | React、Vite、Framer Motionを用いてブラウザ表示用のプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/code-on-sunday/slide-deck-generator/) |
| [Kuneosu/make-slide](https://github.com/Kuneosu/make-slide) | 132 | 単独で動作するHTMLプレゼン資料を作成する汎用AIスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Kuneosu/make-slide/) |
| [joeseesun/qiaomu-bento-ppt](https://github.com/joeseesun/qiaomu-bento-ppt) | 127 | 指示やメモをもとに、Bento形式のスライドを単一のHTMLファイルとして作成・編集するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/joeseesun/qiaomu-bento-ppt/) |
| [gongnyang/awesome-html-scrolline-deck](https://github.com/gongnyang/awesome-html-scrolline-deck) | 90 | スクロールに連動して展開するプレゼン資料集。6種のコンセプトと80種のアニメーションを収録。 | [🟢 問題なし](https://agentskillshub.top/skill/gongnyang/awesome-html-scrolline-deck/) |
| [borjaperfra/beatdeck](https://github.com/borjaperfra/beatdeck) | 80 | 1920×1080解像度のReact画面で、クリック操作により進行するプレゼンツール。オフライン表示や発表者画面に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/borjaperfra/beatdeck/) |
| [kaisersong/slide-creator](https://github.com/kaisersong/slide-creator) | 52 | AIによる構成設計とスタイル選定でHTML資料を作成し、PPTX形式での出力にも対応するClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/kaisersong/slide-creator/) |
| [arifszn/slide-wright](https://github.com/arifszn/slide-wright) | 49 | 指示に応じてデザインを構築し、reveal.jsでプレゼン資料を作成するAIエージェント向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/arifszn/slide-wright/) |
| [whiteg2030-alt/BWC-XIXI-PPT-HTML](https://github.com/whiteg2030-alt/BWC-XIXI-PPT-HTML) | 47 | 細身のデザインと独自フォントを用い、HTMLおよびテキスト編集可能なPPTを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/whiteg2030-alt/BWC-XIXI-PPT-HTML/) |
| [FeeiCN/slide-writer](https://github.com/FeeiCN/slide-writer) | 43 | アイデア、アウトライン、文書、発表原稿から、ビジネス向けのHTMLプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/FeeiCN/slide-writer/) |
| [dososo/blcaptain-ppt-skill](https://github.com/dososo/blcaptain-ppt-skill) | 33 | 7種類のデザイン方針を備えた単一HTML資料制作スキル。アクセシビリティ、余白、捏造防止などを確認。 | [🟢 問題なし](https://agentskillshub.top/skill/dososo/blcaptain-ppt-skill/) |
| [nghiahsgs/skills-slides](https://github.com/nghiahsgs/skills-slides) | 33 | 追加の依存関係なしで多彩なHTMLスライドデザインを適用できるClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/nghiahsgs/skills-slides/) |
| [OrangeViolin/presentation-skill](https://github.com/OrangeViolin/presentation-skill) | 30 | 62種のデザインスタイルに対応し、テーマから発表原稿と再生可能なHTMLプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/OrangeViolin/presentation-skill/) |
| [dakjdakd/PPT-Design-DNA](https://github.com/dakjdakd/PPT-Design-DNA) | 30 | 参考画像のデザインを再利用可能なスタイルとして保存し、HTMLスライドに適用するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/dakjdakd/PPT-Design-DNA/) |
| [sharptoolbox/consulting-html-ppt](https://github.com/sharptoolbox/consulting-html-ppt) | 27 | HTML、SVG、EChartsを用いて、コンサルティングファーム風のプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/sharptoolbox/consulting-html-ppt/) |
| [SlideSpeak/slide-design-skill](https://github.com/SlideSpeak/slide-design-skill) | 26 | 内容とデザインの指示に基づき、図表や画像を含む1920×1080解像度のHTML資料を作成するエージェント向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/SlideSpeak/slide-design-skill/) |
| [lqshow/neon-slides](https://github.com/lqshow/neon-slides) | 20 | アウトラインからネオン調のダークテーマHTMLスライドを作成するClaude向けスキル。技術配信や紹介ページにも対応。 | [🟢 問題なし](https://agentskillshub.top/skill/lqshow/neon-slides/) |
| [yevvonlim/kai-presentation](https://github.com/yevvonlim/kai-presentation) | 16 | KAIのプレゼンテーションデザインをHTMLで作成するClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/yevvonlim/kai-presentation/) |
| [BigSweetPotatoStudio/ai-ppt-tutorial](https://github.com/BigSweetPotatoStudio/ai-ppt-tutorial) | 15 | Claude Codeを活用してAIプレゼン資料を作成するためのチュートリアル。 | [🟢 問題なし](https://agentskillshub.top/skill/BigSweetPotatoStudio/ai-ppt-tutorial/) |
| [shawnzam/keynot](https://github.com/shawnzam/keynot) | 15 | 指示から単独で動作するHTML資料を作成するClaude Code向けスキル。KeynoteやPowerPointは不要。 | [🟢 問題なし](https://agentskillshub.top/skill/shawnzam/keynot/) |
| [caikankan/cyberbin-ppt-skill](https://github.com/caikankan/cyberbin-ppt-skill) | 14 | ローカル環境で動作するHTMLスライドを生成するCyberBin向け作成スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/caikankan/cyberbin-ppt-skill/) |
| [masaki39/marp-mcp](https://github.com/masaki39/marp-mcp) | 13 | 構造化された操作体系により、AIエージェントがMarpスライドの作成・編集を行うMCPサーバー。 | [🟢 問題なし](https://agentskillshub.top/skill/masaki39/marp-mcp/) |
| [young920/gz-ppt-skill](https://github.com/young920/gz-ppt-skill) | 13 | guizangスタイルのプレゼン資料作成手法を研究・学習するためのスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/young920/gz-ppt-skill/) |
| [andyqiu847-ai/high-quality-slides](https://github.com/andyqiu847-ai/high-quality-slides) | 12 | リサーチとストーリー構成を重視し、5段階の手順でスライドを作成するClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/andyqiu847-ai/high-quality-slides/) |
| [lanceli93/aws-html-slides](https://github.com/lanceli93/aws-html-slides) | 12 | アニメーション付きHTML資料の新規作成および、既存PowerPointからの変換に対応したスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/lanceli93/aws-html-slides/) |
| [Watermelon4000/sketch-note-ppt](https://github.com/Watermelon4000/sketch-note-ppt) | 11 | 手描きノート風のプレゼン資料を、ビルド不要の単一HTMLファイルで作成するAIスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Watermelon4000/sketch-note-ppt/) |
| [alingowangxr/guizang-ppt-skill](https://github.com/alingowangxr/guizang-ppt-skill) | 11 | Webスライド、挿絵、SNS向け表紙画像を作成するguizangスタイル向けスキル。繁体字・簡体字中国語に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/alingowangxr/guizang-ppt-skill/) |
| [lainshao/modern-ppt](https://github.com/lainshao/modern-ppt) | 11 | 12種のレイアウトと3種のテーマを備え、図表やアニメーションを含む単一HTML資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/lainshao/modern-ppt/) |
| [RDDcat/maro-ppt](https://github.com/RDDcat/maro-ppt) | 10 | 対話を通じて内容を整理し、説得力のある構成の単一HTML発表資料を作成するClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/RDDcat/maro-ppt/) |
| [icytra/fudan-html-ppt-template](https://github.com/icytra/fudan-html-ppt-template) | 10 | 復旦大学スタイルのHTMLプレゼン用テンプレートを扱うスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/icytra/fudan-html-ppt-template/) |
| [zhenwusw/orca-ppt-skill](https://github.com/zhenwusw/orca-ppt-skill) | 10 | 参考資料の再現と映像的な画面切り替えを備えたデスクトップ制作ツール。MCPとスキルを提供。 | [🟢 問題なし](https://agentskillshub.top/skill/zhenwusw/orca-ppt-skill/) |
| [alfredo-hs/quarto-talks](https://github.com/alfredo-hs/quarto-talks) | 9 | Quartoを利用してreveal.js形式のプレゼン資料を作成するエージェント向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/alfredo-hs/quarto-talks/) |
| [embabel/decker](https://github.com/embabel/decker) | 9 | プレゼンテーション資料を作成するAIエージェント。 | [🟢 問題なし](https://agentskillshub.top/skill/embabel/decker/) |
| [karem505/karem-arabic-presentation](https://github.com/karem505/karem-arabic-presentation) | 9 | アラビア語・英語のHTML資料を作るClaude Code向けスキル。右から左への表示とアニメーションに対応。 | [🟢 問題なし](https://agentskillshub.top/skill/karem505/karem-arabic-presentation/) |
| [theolundqvist/justshowme](https://github.com/theolundqvist/justshowme) | 9 | AIの回答をインタラクティブな図やスライドとして可視化し、プルリクエストへの添付にも対応するツール。 | [🟢 問題なし](https://agentskillshub.top/skill/theolundqvist/justshowme/) |
| [thmsgo18/presentation-forge](https://github.com/thmsgo18/presentation-forge) | 9 | 単独で動作するHTML資料を作成し、PowerPointや画像、テキストからブランドテーマを抽出・適用するClaude向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/thmsgo18/presentation-forge/) |
| [andyluu98/slidefly](https://github.com/andyluu98/slidefly) | 8 | PowerPointの変形（Morph）風トランジションと47種のスタイルを備えた、ベトナム語対応のHTML資料作成スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/andyluu98/slidefly/) |
| [bjoern2000/deckpipe](https://github.com/bjoern2000/deckpipe) | 8 | HTML、CSS、JavaScriptで記述されたスライドを描画し、共有用URLを発行するプレゼンエンジン。 | [🟢 問題なし](https://agentskillshub.top/skill/bjoern2000/deckpipe/) |
| [chenyangji666/html-ppt-skill](https://github.com/chenyangji666/html-ppt-skill) | 8 | HTML・CSS・JavaScriptのみで動作するプレゼンエンジンと、AI向けのスライド生成手順。 | [🟢 問題なし](https://agentskillshub.top/skill/chenyangji666/html-ppt-skill/) |
| [cogine-ai/ai-slide-templates](https://github.com/cogine-ai/ai-slide-templates) | 8 | 資料作成用のメタデータとエージェント向け指示を含む、単独で動作するHTMLテンプレート集。 | [🟢 問題なし](https://agentskillshub.top/skill/cogine-ai/ai-slide-templates/) |
| [AgentiaPT/vela-slides](https://github.com/AgentiaPT/vela-slides) | 7 | AIを活用したプレゼン資料作成アプリケーションおよびエージェント向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/AgentiaPT/vela-slides/) |
| [tjxj/dsh-wanghong-handwritten-ppt](https://github.com/tjxj/dsh-wanghong-handwritten-ppt) | 7 | 手書き学術ノート風のHTMLスライドを作成し、PNG形式での出力にも対応するDeepSeek Harness向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/tjxj/dsh-wanghong-handwritten-ppt/) |
| [tomacco/deckadence](https://github.com/tomacco/deckadence) | 7 | 単一HTML内でカメラワークのように空間を移動・展開する、アニメーション付きスライド作成スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/tomacco/deckadence/) |
| [alohays/paper2pr](https://github.com/alohays/paper2pr) | 6 | AI・機械学習の論文からBeamerおよびQuarto形式の発表資料を作成する、Claude Codeマルチエージェント向け手順。 | [🟢 問題なし](https://agentskillshub.top/skill/alohays/paper2pr/) |
| [severli93/moonland-deck](https://github.com/severli93/moonland-deck) | 6 | 鮮やかな配色とスイススタイルを融合したHTMLプレゼン資料向けデザインシステム。 | [🟢 問題なし](https://agentskillshub.top/skill/severli93/moonland-deck/) |
| [Codagent-AI/and-scene](https://github.com/Codagent-AI/and-scene) | 5 | 形状や配置が滑らかに変形・推移するアニメーション付きプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Codagent-AI/and-scene/) |
| [clearfunction/cf-devtools](https://github.com/clearfunction/cf-devtools) | 5 | Slidevによるプレゼン作成機能と開発支援ツールを統合したClaude Code向けスキルプラグイン。 | [🟢 問題なし](https://agentskillshub.top/skill/clearfunction/cf-devtools/) |
| [cskwork/pptx-to-html-updated](https://github.com/cskwork/pptx-to-html-updated) | 5 | PPTXをHTML形式に一括変換。Chart.jsによるグラフ描画、SVG図形、埋め込みフォント、アニメーションに対応。 | [🟢 問題なし](https://agentskillshub.top/skill/cskwork/pptx-to-html-updated/) |
| [joelbarmettlerUZH/slidev-mcp](https://github.com/joelbarmettlerUZH/slidev-mcp) | 5 | Slidev資料の生成・レンダリング・ホスティングを行うMCPサーバー。 | [🟢 問題なし](https://agentskillshub.top/skill/joelbarmettlerUZH/slidev-mcp/) |
| [tanglele110-hash/zhongguose-ppt-skill](https://github.com/tanglele110-hash/zhongguose-ppt-skill) | 5 | 中国の伝統色を取り入れた報告用プレゼン資料を作成するエージェント向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/tanglele110-hash/zhongguose-ppt-skill/) |

[↑ 用途別の一覧に戻る](#choose)

<a id="type-business"></a>

## 💼 ビジネス・コンサルティング（13件）

提案、報告、ピッチなど、ビジネス用途を重視した資料制作。

[原版のこの分類を見る](https://agentskillshub.top/best/ppt-presentation/#type-business)

| ツール | ★ | できること | 導入時のセキュリティ評価 |
|---|---:|---|---|
| [carnot-tech/jinba-consulting-pptx-skill](https://github.com/carnot-tech/jinba-consulting-pptx-skill) | 1,160 | Claude CodeやCodexを用いてコンサルティング向けPPTXを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/carnot-tech/jinba-consulting-pptx-skill/) |
| [Pikapika260214/rw-consulting-ppt](https://github.com/Pikapika260214/rw-consulting-ppt) | 473 | コンサルティング用資料を作成するCodex向けスキル。編集可能な形式での出力にも対応。 | [🟢 問題なし](https://agentskillshub.top/skill/Pikapika260214/rw-consulting-ppt/) |
| [likaku/Mck-ppt-design-skill](https://github.com/likaku/Mck-ppt-design-skill) | 297 | 70種類のレイアウトとフラットデザインを備え、python-pptxでコンサルティング風資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/likaku/Mck-ppt-design-skill/) |
| [Ronnie2025/codex-ppt-skill](https://github.com/Ronnie2025/codex-ppt-skill) | 220 | 中国語の法人向け報告資料を作成するCodex向けワークフロー。画像生成、要素の再構成、SVGの分解に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/Ronnie2025/codex-ppt-skill/) |
| [SenseTime-Copilot/raccoon-ppt-skill](https://github.com/SenseTime-Copilot/raccoon-ppt-skill) | 149 | OpenClawからリモートPPT生成APIを利用し、資料作成の依頼・継続・結果取得を行うスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/SenseTime-Copilot/raccoon-ppt-skill/) |
| [kimsh-1/deck-factory](https://github.com/kimsh-1/deck-factory) | 79 | 簡潔な指示からダークトーンの雑誌風HTMLプレゼン資料を作成するClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/kimsh-1/deck-factory/) |
| [FW1201/visual-presentation-production](https://github.com/FW1201/visual-presentation-production) | 33 | CodexやChatGPT Workで利用できる、16:9比率の画像形式プレゼン資料作成スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/FW1201/visual-presentation-production/) |
| [abxxvrv/spacex-ppt-skill](https://github.com/abxxvrv/spacex-ppt-skill) | 31 | 黒背景と写真を基調に、SpaceX風の発表資料をHTMLで作成しPDFやPNGに出力するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/abxxvrv/spacex-ppt-skill/) |
| [shenxiaofeng-pro/jiarui-svg-skills](https://github.com/shenxiaofeng-pro/jiarui-svg-skills) | 31 | 企業ロゴやテーマカラーを用いたSVG資料を作成し、PowerPointでパーツに分解して活用できるようにするスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/shenxiaofeng-pro/jiarui-svg-skills/) |
| [floflo11/mbb-decks](https://github.com/floflo11/mbb-decks) | 19 | 結論ファーストの見出しとMECEな箇条書きで、MBB風コンサルティング資料をPPTX化するClaude向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/floflo11/mbb-decks/) |
| [NomiciAI/mbb-page-maker](https://github.com/NomiciAI/mbb-page-maker) | 10 | HTML・CSS・JavaScriptを用いて、コンサルティング風のHTMLプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/NomiciAI/mbb-page-maker/) |
| [GZPengyuyan/PengyuyanPPT](https://github.com/GZPengyuyan/PengyuyanPPT) | 9 | SCR構成とスタイル確認を使い、情報量の多い編集可能なコンサルティング風PPTXを作るスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/GZPengyuyan/PengyuyanPPT/) |
| [MiraclePlus/pre-pp](https://github.com/MiraclePlus/pre-pp) | 5 | ピッチ資料を反復的に改善するためのClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/MiraclePlus/pre-pp/) |

[↑ 用途別の一覧に戻る](#choose)

<a id="type-convert"></a>

## 📄 文書からスライドへ（29件）

論文・PDF・記事・Markdownなどをもとに資料を作るツール。

[原版のこの分類を見る](https://agentskillshub.top/best/ppt-presentation/#type-convert)

| ツール | ★ | できること | 導入時のセキュリティ評価 |
|---|---:|---|---|
| [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | 60,118 | 文書やテーマからPowerPointを制作。標準の図形・図表・アニメーション、音声ナレーション、手持ちテンプレートに対応。 | [🟢 問題なし](https://agentskillshub.top/skill/hugohe3/ppt-master/) |
| [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) | 3,294 | AIでPPT用画像や動画を生成するスキル。スライド遷移やインタラクティブな再生に対応。 | [🟡 要注意](https://agentskillshub.top/skill/op7418/NanoBanana-PPT-Skills/) |
| [crazyykhllc-bit/CyberPPT](https://github.com/crazyykhllc-bit/CyberPPT) | 1,771 | SCR構成とスタイル確認を使い、編集可能なコンサルティング風PowerPointを作るCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/crazyykhllc-bit/CyberPPT/) |
| [Gabberflast/academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill) | 1,152 | 学会発表、セミナー、学位審査、助成金説明向けの資料を作成。論旨と引用を重視するClaude向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Gabberflast/academic-pptx-skill/) |
| [irenerachel/visual-style-ppt-skill](https://github.com/irenerachel/visual-style-ppt-skill) | 391 | 視覚的なスタイル設計を重視したPPT作成スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/irenerachel/visual-style-ppt-skill/) |
| [Noi1r/beamer-skill](https://github.com/Noi1r/beamer-skill) | 364 | BeamerやLaTeXの学術資料を作成、コンパイル、レビュー、推敲するClaude Code向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Noi1r/beamer-skill/) |
| [Faust-Donf/beamer-academic](https://github.com/Faust-Donf/beamer-academic) | 313 | 論文をもとに学位審査や研究発表用スライドを作成するClaude Code・Codex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/Faust-Donf/beamer-academic/) |
| [vigorX777/ppt-svg-generator](https://github.com/vigorX777/ppt-svg-generator) | 258 | Markdown原稿から複数のスタイルを選択し、PPTやPDF形式の資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/vigorX777/ppt-svg-generator/) |
| [M1n-n9/academic-ppt-master](https://github.com/M1n-n9/academic-ppt-master) | 237 | 学術論文から編集可能な研究発表用PPTXを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/M1n-n9/academic-ppt-master/) |
| [mujingquan835/dashiai-ppt-skill](https://github.com/mujingquan835/dashiai-ppt-skill) | 190 | 編集可能なPPTXの生成、ブラウザ上での編集、修正作業に対応した作成スキル。 | [🟢 問題なし](https://agentskillshub.top/skill/mujingquan835/dashiai-ppt-skill/) |
| [fangyuanopus/literature-report-ppt-builder](https://github.com/fangyuanopus/literature-report-ppt-builder) | 110 | 学術文献の報告資料を作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/fangyuanopus/literature-report-ppt-builder/) |
| [helloo1568/slidemuse](https://github.com/helloo1568/slidemuse) | 64 | 研究発表、論文審査、学生コンテスト、ピッチ向けに、4種のスタイルで編集可能なPPTXを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/helloo1568/slidemuse/) |
| [deathcats4/scholar-ppt-cn](https://github.com/deathcats4/scholar-ppt-cn) | 49 | 論文から構成案と参考レイアウトを作成し、編集可能な学術PPTXに仕上げるCodex・ChatGPT向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/deathcats4/scholar-ppt-cn/) |
| [joeseesun/qiaomu-ppt](https://github.com/joeseesun/qiaomu-ppt) | 36 | URL・PDF・NotebookLM・HTML資料から、編集可能で検証できるプレゼン資料を作る、中国語を中心にした制作手順。 | [🟢 問題なし](https://agentskillshub.top/skill/joeseesun/qiaomu-ppt/) |
| [hanlulong/econ-slides-skill](https://github.com/hanlulong/econ-slides-skill) | 22 | 経済学論文から時間配分付き発表原稿とBeamer資料を作成。学会、採用講演、討論者発表に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/hanlulong/econ-slides-skill/) |
| [DAIBird-0/pdf2ppt_skill](https://github.com/DAIBird-0/pdf2ppt_skill) | 12 | 論文PDFを読み込み、構成案の確認後に編集可能なPPTXとページ別の発表原稿を作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/DAIBird-0/pdf2ppt_skill/) |
| [moyoo0/paper-to-latex-ppt](https://github.com/moyoo0/paper-to-latex-ppt) | 11 | 論文からゼミや研究室発表に用いる原稿付きプレゼン資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/moyoo0/paper-to-latex-ppt/) |
| [doudou1337/deckset-claude-skill](https://github.com/doudou1337/deckset-claude-skill) | 10 | MarkdownでDeckset資料を作成するClaude Code向けスキル。29件のドキュメントと3種の作例を収録。 | [🟢 問題なし](https://agentskillshub.top/skill/doudou1337/deckset-claude-skill/) |
| [icgma/slide-skill](https://github.com/icgma/slide-skill) | 9 | 構成設計と分野別レイアウトを活用し、SVGを中心にスライドを作成するツール集。 | [🟢 問題なし](https://agentskillshub.top/skill/icgma/slide-skill/) |
| [SkillMelody/PPT-Smith](https://github.com/SkillMelody/PPT-Smith) | 8 | 特定モデルに依存せずプレゼン資料を組み立てるMeowClaw向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/SkillMelody/PPT-Smith/) |
| [zl190/md-slides](https://github.com/zl190/md-slides) | 8 | Markdownからスライドを作成するClaude Code向けスキル。 | [🟡 要注意](https://agentskillshub.top/skill/zl190/md-slides/) |
| [FA-T-T/codex-skill-academic-slides](https://github.com/FA-T-T/codex-skill-academic-slides) | 7 | GPT Imageで学術スライド、ポスター、確認用一覧、構成図を作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/FA-T-T/codex-skill-academic-slides/) |
| [ficooooo/Paper2ScholarSlides](https://github.com/ficooooo/Paper2ScholarSlides) | 7 | 論文や文献レビュー原稿から引用・図表・数式を整理し、出力を検証した学術発表資料を作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/ficooooo/Paper2ScholarSlides/) |
| [SHALINS428/Academic-PPT-Skill](https://github.com/SHALINS428/Academic-PPT-Skill) | 6 | 学位論文の資料から、構成計画と出典確認を経て編集可能な審査用PowerPointを作成するスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/SHALINS428/Academic-PPT-Skill/) |
| [wp-a/paper2ppt](https://github.com/wp-a/paper2ppt) | 6 | 学術論文を、編集可能で出典を追跡できる中国語PPTXに変換するスキル。CodexとClaude Codeに対応。 | [🟢 問題なし](https://agentskillshub.top/skill/wp-a/paper2ppt/) |
| [2654400439/Paper2Seminar](https://github.com/2654400439/Paper2Seminar) | 5 | 研究論文からセミナー・輪読会向けの編集可能なPPTXを作成するエージェント向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/2654400439/Paper2Seminar/) |
| [MURMURE11118586/codex-xkppt-skill](https://github.com/MURMURE11118586/codex-xkppt-skill) | 5 | テーマ、文書、PDF、Markdown、既存PPTから資料を作成。スタイル参照、単一ページの修正、出力と品質確認に対応。 | [🟢 問題なし](https://agentskillshub.top/skill/MURMURE11118586/codex-xkppt-skill/) |
| [demoolight/academic-image-ppt](https://github.com/demoolight/academic-image-ppt) | 5 | 学術発表向けの画像形式PowerPoint資料を作成するCodex向けスキル。 | [🟢 問題なし](https://agentskillshub.top/skill/demoolight/academic-image-ppt/) |
| [sujunmin/agy-ppt](https://github.com/sujunmin/agy-ppt) | 5 | Antigravity、Kiro、Codexの手順で報告書から資料を作成するスキル。繁体字が多いスライドにはGPT Imageを使用。 | [🟢 問題なし](https://agentskillshub.top/skill/sujunmin/agy-ppt/) |

[↑ 用途別の一覧に戻る](#choose)

## 原版の掲載基準

原版では、以下の基準に基づいて掲載対象を選定しています。

1. PPT・PPTX・Keynote・HTMLなどのプレゼンテーション資料を作成できること（単なる文書やポスターの生成のみは対象外）。
2. AIエージェントが利用するスキル、プラグイン、MCPサーバー、またはツールセットであること。
3. 評価対象となるREADMEが存在すること。
4. スター数が50以上の場合は対象領域に該当していること。50未満の場合はスター数5以上に加え、作例、一つのコマンドで始められる手順、具体的な成果物、十分なドキュメントが揃っていること。

選定判定はREADMEを解析するモデルが行っています。基準境界にあるツールの分類には揺らぎが生じる場合があり、掲載基準や評価に関する指摘は原版リポジトリへ直接フィードバックできます。本リポジトリの日本語表記に関する修正は、[修正提案](https://github.com/studio-yebisu/awesome-codex-ppt-skills-ja/issues/new/choose)までお寄せください。

## 関連する一覧

- [AI動画制作スキルの一覧（原作者の別リポジトリ）](https://github.com/zhuyansen/awesome-claude-video-skills)

## 修正・更新について

[参加方法](CONTRIBUTING.md) · [翻訳・説明文の修正を提案](https://github.com/studio-yebisu/awesome-codex-ppt-skills-ja/issues/new/choose)

機械処理向けの日本語データは[data/skills.json](data/skills.json)にあります。

## 出典・利用条件

原版の一覧と本リポジトリの日本語文章・データ編集部分はCC0 1.0です。掲載プロジェクトのコードや素材は、それぞれの利用条件に従います。詳細は[出典とライセンス](docs/出典とライセンス.md)と[LICENSE](LICENSE)をご覧ください。
