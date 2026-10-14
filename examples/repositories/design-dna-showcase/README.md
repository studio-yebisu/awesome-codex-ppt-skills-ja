# 町の道具を、借り合う。

架空の地域の道具棚を説明する日本語6枚のWebスライド。[index.html](index.html)は実字体・CSS・JS・Apache/OFL原文を内包し、ネット接続なしで開けます。編集はHTML/SVG/CSSとDNA/Page SpecsのJSON。PPTXは生成していません。

原典は dakjdakd/PPT-Design-DNA、commit `5d1d84cf952f16920d893b6c04bd7cb7cff9d155`、Apache-2.0 ©2026 dakjdakd。[LICENSE](LICENSE)、[未変更SKILL/参照/guard](source/upstream/)を保持。上流に単独のrendererや完成controllerはなく、schemaとHTML生成契約に沿った直接authoringと必須Node guardが実行経路です。元固定stage CSSとscaling式を実使用し、ナビゲーションは契約に沿った自作です。

[参考画像](input/reference/slide-01.png)は既存の自作Akxan/ppt-agent-skill由来native PPTXのPowerPoint実描画。元の[出所](input/reference/PROVENANCE.json)と[MIT ©2025 sunbigfly](input/reference/LICENSE)を保存しました。実画像を表示した後、色・構図・階層・情報密度を[5層DNA](input/design-dna.json)と[パネル](input/DNA-PANEL.md)へ抽出。参考は証拠用の入力で、新作HTMLには埋め込んでいません。台車・机・椅子は新しい原稿から自作した説明SVGです。

再生成はPython 3標準ライブラリで `python source/rebuild.py`。抽出DNAのtokensと[数値Page Specs](specs/page-specs.json)から、1920×1080固定stageを組みます。その後Nodeで `node source/upstream/scripts/ppt-layout-guard.js index.html --report layout-guard-report.json` を実行します。上流guardは外部依存なし、未改変です。実際の[報告](layout-guard-report.json)はPASS、6枚・27区画、P0/P1なし。

原典のuser-turn確認ゲートは、承認済み自律制作の指定に従い記録パネルと内部判断へ置き換えました。ゲートでユーザー回答を得たとは表現せず、canonical design-profilesを作っていません。今回のactive candidateは再生成入力として保存。専有作例配置へ出力パスを変更しました。局所CSS、新作原稿/図と自作controller、[bridge patch](source/controller.patch)を分けて保管しています。

字体は公式固定Google Fonts pin `66928797f271fed5ee428544e7229685e2d90127`のZen Kaku Gothic New Black/Regular、BIZ UDPMincho Regular、Manrope。実TTFは未改変、原文OFLと[source/fonts](source/fonts/)へ同梱し、[出所/hash](source/FONT-SOURCE.json)を記録。OS字体の抽出、評価限定artifact-tool SDKは使っていません。

単体操作は←/→・↑/↓・Space・Home/End・swipe。全体を均等縮小し、内部の再流し込みやスクロールはしません。同一origin親の0-based yebisu-slideを受け、yebisu-pageを通知する小差分を追加しました。親サイト統合はここでは未確認。

必須guardに加え、表紙と道具一覧をChromeで初回表示し、ArrowRightで01/06から02/06へ送りました。代表PNG2枚を表示し、page errorはありません。全頁詳細目視・独立review・追加採点・全ZIP再実行は未実施です。[QA](QA.json)はこの範囲だけを示します。企画の日時・会場・費用・参加者数は未定、安全性・運用効果は未検証です。
