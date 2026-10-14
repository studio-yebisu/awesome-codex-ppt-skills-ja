# Prompt Templates

Use these templates as starting points. Keep slide text short and exact. For Chinese-heavy slides, prefer fewer text blocks with larger typography.

## Shared Full-Slide Constraints

Append this to every slide prompt:

```text
Create one complete 16:9 academic PowerPoint slide as a polished raster image, 1280x720.
Render all Chinese text, English subtitles, numbers, formulas, labels, names, and page numbers exactly as provided.
Do not invent citations, metrics, logos, school names, diagrams, chart values, experiment results, author metadata, or factual claims. Use only source-provided or user-confirmed exact values; if a fact is missing, omit it or mark it as `needs user confirmation` before prompting.
Use a formal Chinese university thesis defense style: white background, deep academic blue accents, subtle technical line-art, clean grid, high readability.
No watermark. No random English filler. No malformed Chinese characters.
```

## Three-Option Thumbnail Preview

Use this before generating final slide pages. Generate three separate thumbnail preview images, one per option. Each thumbnail or sample-page preview must follow the preview-board format shown by `assets/reference-thumbnails/option-c-preview-board-format.png`.

```text
Use case: productivity-visual
Asset type: visual direction thumbnail board for an academic image PPT
Create one preview board showing a coherent mini style system for a Chinese academic thesis defense PPT.
The overall preview-board canvas may use any aspect ratio that best fits the design; it does not have to be 16:9.
The preview board must contain three zones:
1. Top introduction band: school/logo area when available; title "PPT风格方向预览板"; version label such as "方案 A/B/C"; overall tone; style keywords; optional user metadata.
2. Main body: exactly 6 miniature slide previews arranged as a clear grid. Every miniature slide preview must be a true 16:9 slide frame with consistent proportions. Do not draw the mini slides as vertical cards, square cards, long strips, cropped panels, rotated panels, or irregular shapes. Include these key pages: 1 cover page, 1 contents page, 1 section-divider page, 2 representative content pages, and 1 standalone closing/Q&A page. The 2 representative content pages must look like real deck pages guided by the approved blueprint's evidence role and must-preserve evidence, with visible evidence carriers such as data cards, comparison tables, process arrows, evidence strips, mechanism diagrams, chart strips, framework nodes, or conclusion panels. Do not make the thumbnail board sparse, decorative-only, or dominated by cover-like title pages.
3. Bottom specification band: color rules, font rules with key font names, icon style, layout traits, and use scenarios.
The preview is for style selection only, not final readable content, but the headings and labels should look plausible and professionally typeset.
Use the paper topic: "<paper topic>"
Use school/field cues: "<school or domain cues>"
Variant: "<A formal academic blue / B clean college defense / C formal technical defense>"
Style introduction fields to include:
- 标题
- 版本
- 整体色调
- 风格关键词
- 色彩规范
- 字体规范（关键字体）
- 图标风格
- 版式特点
- 使用场景
Show realistic Chinese academic slide headings, but keep them short and readable.
Constraints: no fake final metrics, no invented citations, no extra school names, no watermark, no malformed Chinese characters.
```

After the user selects a variant, create `qa/thumbnail-style-contract.md` from the selected thumbnail. Use both the selected thumbnail and the style contract as required style references for sample pages and every final full-slide prompt. If the user requests revisions, revise the selected thumbnail and the style contract first and only then continue to sample or final page generation. A sample page may be more detailed than the thumbnail, but it must preserve the thumbnail's palette, typography, title system, page rhythm, icon language, chart/figure language, and density.

## Cover

```text
Use case: productivity-visual
Asset type: full-page image PPT slide
Slide type: thesis defense cover
Text:
Title: "<paper title>"
School: "<school name>"
Student: "<student name>"
Major: "<major>"
Advisor: "<advisor>"
Date: "<date>"
Visual direction: formal academic defense cover, centered title, school logo at top, subtle campus or domain-related line-art background, deep blue footer with page number 01.
Constraints: keep all metadata exact; do not add extra names or slogans.
```

## Contents

```text
Slide type: contents page
Text:
Title: "目录"
Subtitle: "CONTENTS"
Items:
01 <section title> <page range>
02 <section title> <page range>
03 <section title> <page range>
04 <section title> <page range>
05 <optional section title> <page range>
06 <optional section title> <page range>
Visual direction: clean numbered rows, deep blue index blocks, light academic background, footer and page number.
Constraints: page ranges must match the approved blueprint exactly.
```

## Section Divider

```text
Slide type: section divider
Text:
Section number: "<01/02/03/04>"
Chinese title: "<section title>"
English subtitle: "<section subtitle>"
Visual direction: large centered section number, strong blue title, subtle campus/technical background, minimal content, page number.
Constraints: no body text.
```

## Method Or Architecture Slide

```text
Slide type: academic method slide
Title: "<numbered title>"
Core text blocks:
- "<short exact block 1>"
- "<short exact block 2>"
- "<short exact block 3>"
Diagram content:
<describe nodes and arrows in order>
Visual direction: structured scientific workflow/architecture diagram, blue-accent nodes, readable formula callouts, balanced whitespace.
Constraints: preserve exact model names and formulas; arrows must show the specified flow only.
```

## Source Figure Slide

```text
Slide type: experiment result slide with source figure
Title: "<numbered title>"
Source figure: use the provided figure as the strict data reference, but prefer an imagegen-redrawn chart/figure integrated into the slide style rather than directly pasting the original PDF/DOCX figure. Preserve its data pattern, hard values, trends, axes, labels, legends, and chart meaning exactly.
Callouts:
- "<callout 1>"
- "<callout 2>"
- "<callout 3>"
Visual direction: redrawn source-faithful figure on the left or center, concise explanation cards on the side, academic blue style. Mark the key finding directly on the chart using arrows, focal color, highlighted regions, labels, or concise annotation boxes so the page is self-explanatory.
Constraints: do not redraw chart values inaccurately; do not change AUC, accuracy, axis labels, legends, class labels, table values, trend direction, or relative comparisons. Do not paste the original figure unchanged unless the user explicitly asks for original preservation.
```

## Comparison Table Slide

```text
Slide type: model comparison and performance analysis
Title: "<numbered title>"
Table columns: <columns>
Rows:
<row 1>
<row 2>
<row 3>
Main conclusion: "<one sentence conclusion>"
Visual direction: clear table plus bar comparison, highlighted best model row, restrained academic style.
Constraints: all table values must be exact; highlight only the approved best model.
```

## Summary And Outlook

```text
Slide type: summary and outlook
Title: "总结与展望"
Summary points:
1. "<point>"
2. "<point>"
3. "<point>"
Future outlook:
1. "<future direction>"
2. "<future direction>"
3. "<future direction>"
Visual direction: two-column summary/outlook layout, icon-supported but not decorative, deep blue emphasis, red or amber final conclusion strip only if needed.
Constraints: no new claims beyond the paper.
```

## Thanks

```text
Slide type: standalone closing / Q&A / correction-request page
Text:
"<恳请各位老师同学批评指正 / 恳请各位老师批评指正 / user-provided wording>"
Student: "<student name>"
Student ID: "<student ID if required>"
Major: "<major>"
Advisor: "<advisor>"
Visual direction: formal closing slide, large centered correction-request wording, school logo, subtle campus background, deep blue footer.
Constraints: this must be a separate final page; do not include summary, conclusion, outlook, methods, data, or any content-slide material. Do not use "感谢聆听".
```
