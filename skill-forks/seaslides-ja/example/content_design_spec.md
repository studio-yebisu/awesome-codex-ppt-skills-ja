# 読書会 - Content Design Specification
## I. Project Information
Page Format: 16:9 / Canvas: 1280x720 / Page Count: 5 / Style Objective: General
Target Audience: 地域の小さな読書会。Language: 日本語。未検証の架空企画。
## II. Theme Selection
Catalog Theme ID: editorial-magazine / Palette: forest-ink
読書・文化という用途に合う明朝見出しと紙面風の構成を選ぶ。日本語見出しはNoto Serif JP、本文はNoto Sans JP。ローカルOFLフォントを同梱。
## III. Narrative Framework
一緒に集まる目的→日程・条件→60分の流れ→役割→次回。input/BRIEF.mdを唯一の内容根拠とする。
## IV. Visual Direction
表紙と終端はhero dark、説明3枚はlight。中央へまとまった本文群、上下に静かな誌面メタ情報。引用風の終端は自作コピーで、外部引用ではない。
## V. Content Outline
1 cover / hero dark / frame / h-hero / 中央群: 月に一度、本の話を。
2 content / light / frame grid-3 / pillar: 日程・長さ・参加条件。
3 content / light / frame / rowline: 10/35/15分で合計60分。
4 content / light / frame roles-stack / pillar: 案内・会場・進行を横一列ずつ比較。
5 ending / hero dark / frame / reading-quote: 次回日程・担当・記録。
## VI. Image Resource List
画像なし。デモ写真・原典サンプル文・Lucide・数式・コード依存は不使用。WebGL背景とMotion11.11.17の原典アニメーションを維持。
## VII. Speaker Notes Plan
各ページ2〜3文をdata-notesとNOTES.mdへ収録。本文は自作日本語、API生成なし。
## Executor Handoff Checklist
unattended mode: 上記9決定は依頼の範囲で確定。TCSを保持しsource gate、all build、全頁視認、visual gateを順に実行する。
