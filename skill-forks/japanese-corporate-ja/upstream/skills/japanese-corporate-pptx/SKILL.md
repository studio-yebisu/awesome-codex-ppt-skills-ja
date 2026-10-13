---
name: japanese-corporate-pptx
description: Create or edit information-dense, componentized, and fully editable Japanese corporate PowerPoint decks (.pptx) and one-page ポンチ絵 in the style of Japanese manufacturers, industry associations, ministries, technical committees, and large-enterprise internal briefings. Use for JEITA風, 経産省風, 霞ヶ関ポンチ, 曼荼羅資料, 事業スキーム, 技術ロードマップ, 全体像, レイヤー図, 関係者図, 業務フロー, 稟議資料, 講演資料, コンポーネント化, or when the user asks for “日本のトラディショナルなPPT”, “さっきみたいなポンチ”, “大企業っぽい資料”, “情報量のある一枚図”, “画像ではなく編集できる部品”, or a slide that combines diagrams, photos, charts, annotations, assumptions, and sources.
---

# Japanese Corporate PPTX

Create editable PowerPoint decks that resemble real Japanese industry-association, manufacturing, ministry, and large-company working documents.

The target is not a clean startup pitch. A successful slide closes the discussion on one page: it states the point, shows the whole system or evidence, identifies actors and flows, includes exceptions or assumptions, and leaves a traceable source.

## Required host capabilities

Use the host agent's presentation or PPTX authoring tools. The toolchain must be
able to inspect, edit, export, and render PowerPoint files while preserving
native objects.

1. Read the host's presentation-tool instructions before editing.
2. Use native text boxes, shapes, connectors, tables, and charts.
3. Keep image frames and every added annotation independently selectable.
4. Render and inspect every slide before delivery.
5. Reopen or reimport the exported PPTX to check compatibility.

If the available tool can only generate a picture of a slide, stop and explain
that an editable PPTX cannot be produced in the current environment. Never
silently flatten the requested diagram.

## Required resources

- Always read [research-backed-patterns.md](references/research-backed-patterns.md) and [jtc-authenticity.md](references/jtc-authenticity.md).
- Always read [visual-style.md](references/visual-style.md) and [writing-and-density.md](references/writing-and-density.md).
- Read [layout-catalog.md](references/layout-catalog.md) before selecting layouts.
- Read [qa-checklist.md](references/qa-checklist.md) before validation.
- Inspect [japanese-corporate-ponchi-layouts.png](assets/japanese-corporate-ponchi-layouts.png) before using the bundled template.

## Reference-first rule

Do not begin by drawing generic boxes.

Use this reference order:

1. User-provided PPTX, PDF, screenshot, or image.
2. Closest official material from the relevant Japanese industry, ministry, company, or association.
3. The bundled template.

If the user provides a reference, inspect every relevant page at full size before authoring. If the user asks for web research, or if no suitable reference exists, perform a visual research pass first:

- run at least three distinct image searches;
- gather at least six useful references;
- include at least two government or association references;
- include at least two corporate or industry references;
- include at least two references close to the requested topic;
- inspect the actual image or PDF page, not only search snippets.

Use online references to extract composition, hierarchy, density, and diagram vocabulary. Do not copy copyrighted artwork into the output unless it is licensed, supplied by the user, or used as a properly attributed source excerpt.

Record a compact style ledger:

- header and footer furniture;
- title hierarchy;
- dominant diagram logic;
- block count and occupancy;
- line and arrow language;
- photo, screenshot, chart, and caption treatment;
- emphasis colors;
- smallest legible text tier;
- source and caveat placement.

## Originality and reference-use guard

Use a reference to identify the communication grammar, not to trace its coordinates.

- Extract the general mechanism: timeline, layer stack, annotated evidence, stakeholder flow, issue table, or decision closure.
- Do not reuse distinctive wording, data, illustrations, chart artwork, icons, or a source-specific arrangement unless the user owns it or reuse is explicitly permitted.
- When a single screenshot is the visual reference, change at least three structural choices: macro layout, reading order, emphasis location, annotation geometry, color roles, or implication placement.
- Keep source excerpts intact and attributed when they are used as evidence; do not disguise copied artwork as a native reconstruction.
- Record internally what came from the reference and what was newly designed.
- Reject a result that would be recognizable as a near-trace after removing the text.

Matching the broad conventions of Japanese corporate documents is allowed. Reproducing the distinctive expression of one document is not.

## Component-first rule

Build recreated diagrams as selectable PowerPoint components.

- Use native text boxes for every title, label, note, source, and callout.
- Use native shapes and connectors for boxes, arrows, markers, rails, and decision flows.
- Use native charts with editable data when the values and units are verified.
- Use native tables for comparisons and issue matrices.
- Use raster images only for authentic photographs, screenshots, logos, or attributed source excerpts whose visual fidelity must be preserved.
- Never use a screenshot or rendered slide as the background of a recreated diagram.
- When a source excerpt must remain an image, keep every added title, marker, translation, interpretation, and decision statement as a separate editable object.
- Give important objects stable names and keep related components grouped or jointly selectable where the authoring API supports it.

The PNG previews are QA artifacts only. They are never the editable deliverable.

## Choose the correct ポンチ grammar

Choose one dominant grammar per slide:

1. **主張＋根拠** — large claim, emphasized phrases, explanatory notes, evidence box.
2. **年代・技術動向** — chevron timeline plus two to four horizontal swimlanes and future callouts.
3. **レイヤー構造** — stacked platform, technology, organization, or value-chain layers with side inputs and outputs.
4. **関係者・価値交換** — central mechanism surrounded by stakeholders, money, data, goods, responsibility, and feedback arrows.
5. **事業・政策スキーム** — purpose, content, target, execution structure, funding or information flow, outcomes, and conditions.
6. **業務プロセス** — stages across the top and role swimlanes down the side, with handoffs, decisions, pain points, and systems.
7. **現状→変革→目指す姿** — before, intervention, future state, enabling foundation, and measurable effect.
8. **ロードマップ** — phases, milestones, decision gates, dependencies, risks, owners, and target state.
9. **データ＋解釈** — chart or official-source excerpt, direct annotations, implications, assumptions, and action.
10. **人物・組織・事業紹介** — portrait or documentary photos, roles, history, business portfolio, and proof points.
11. **原典抜粋＋読み解き** — two or more bounded source excerpts, red callouts, processing notes, comparison, and decision implication.
12. **論点・対応方針** — issue, confirmed fact, proposed response, owner, due date, status, decision, and continuing discussion.
13. **引用グラフ＋注釈オーバーレイ** — one dominant source chart, an editable conclusion band, time or threshold markers, explanatory overlays, processing note, source, and bottom-line implication.

Do not reduce every request to three clean cards. A traditional Japanese ポンチ often needs six to twelve connected blocks because the page must preserve actors, exceptions, and decision conditions.

## Build workflow

### 1. Define the communication job

Write one internal sentence:

> By the end, [audience] should [understand, discuss, decide, or approve] because [central takeaway].

Identify:

- audience and meeting context;
- the primary question;
- the one conclusion or model the page must support;
- actors, inputs, outputs, decisions, dependencies, and exceptions;
- what is confirmed, estimated, proposed, illustrative, or unknown;
- required evidence, units, dates, and sources.

### 2. Create a content-and-relationship ledger

Collect:

- slide purpose and takeaway title;
- entities and their roles;
- directional relationships;
- evidence and source;
- visual asset;
- caveat or unresolved issue;
- intended next action.

Never invent organizations, figures, quotes, outcomes, dates, or client examples.

### 3. Select a reference and layout

Map each output slide to one layout in [layout-catalog.md](references/layout-catalog.md).

When using the bundled template:

`assets/japanese-corporate-ponchi-template.pptx`

- inspect all source slides;
- create a frame map;
- duplicate only the required source slides;
- preserve blue rails, compact footer, page marker, title hierarchy, source position, and density tier;
- replace every `{{...}}` placeholder;
- delete unused sample images and annotations explicitly.

### 4. Draw relationships before decoration

For diagrams:

1. place connectors and flow arrows first;
2. place entity boxes and labels above them;
3. add evidence, photos, charts, and caveats;
4. add only the minimum highlight colors needed for reading order.

Use native PowerPoint:

- simple connectors and block arrows;
- native tables for exact comparisons;
- native charts for numeric data;
- text boxes for conclusions, annotations, notes, and sources;
- raster images for actual people, facilities, products, screenshots, or official source excerpts.

Do not flatten the whole slide to an image.

For an annotated source chart:

- preserve the original chart image when exact source fidelity matters and the underlying data is unavailable;
- redraw it as a native chart only when the values, units, series, periods, and forecast status are available and verified;
- keep the conclusion band, red time or threshold markers, interpretation text, source, and processing note as separate editable PowerPoint objects;
- distinguish original chart content from added interpretation through position and a consistent color code;
- never place an annotation over an essential axis, legend, data label, or source line.
- redesign the surrounding composition rather than copying the source page's exact chart size, annotation positions, color blocks, or footer treatment.

### 5. Use images as evidence or context

Before sourcing an image, define its role:

- documentary evidence;
- official source excerpt;
- process or facility context;
- person or organization identification;
- illustrative context.

Prefer:

- user-supplied or consent-cleared photographs;
- official organization photos and diagrams;
- screenshots from traceable primary sources;
- generated generic illustrations only when the image is illustrative rather than evidence.

Use one to three images on a slide. Give each image a border, crop, caption, or source line. Do not use a full-bleed stock-photo hero unless the reference deck clearly does.

The photographs embedded on slide 3 of the bundled template are fictional and
exist only to demonstrate photo handling. Replace them in real company
materials when authentic, permission-cleared photographs are available. Never
present the embedded samples as a real event or client engagement.

### 6. Apply the visual language

Default:

- 16:9, 1280 × 720;
- BIZ UDPゴシック, Yu Gothic, or Meiryo;
- dark JEITA-like blue top rail;
- white canvas with black or dark navy body text;
- cyan or bright blue for structural emphasis;
- red for risk, current point, or decisive annotation;
- green for target state or outcome;
- mostly square boxes, thick outline layers, chevrons, straight arrows, and underlined emphasis;
- compact page number and organization footer.

Use the exact size tiers in [visual-style.md](references/visual-style.md). Do not force all supporting text to 16pt when the reference uses a compact annotation tier; protect readability through hierarchy, alignment, and grouping.

### 7. Run the JTC authenticity pass

Use [jtc-authenticity.md](references/jtc-authenticity.md). Add only controls that serve the meeting:

- document number, date, version, status, or handling class;
- scope, assumptions, exclusions, definitions, and legend;
- source title, organization, page, date, and processing note;
- red callouts tied to a decision, risk, exception, or verification item;
- owner, due date, gate, status, and unresolved issue.

Authenticity comes from traceable evidence and decision closure rather than arbitrary visual disorder.

### 8. Close the page

A completed one-page ポンチ should normally contain:

- section or topic rail;
- conclusion-bearing title;
- one dominant visual model;
- actors, steps, or layers;
- evidence or examples;
- implication or decision;
- caveat, assumption, or boundary when relevant;
- source and date.

### 9. Validate

Follow [qa-checklist.md](references/qa-checklist.md).

At minimum:

- compare the output against the selected reference images;
- render every slide through the host's compatibility renderer;
- inspect every slide individually at full size;
- run overflow detection;
- inspect the contact sheet for rhythm;
- verify arrows, labels, image crops, citations, page numbers, and unresolved placeholders;
- verify PPTX package integrity and editable objects.

## Hard stops

Do not deliver when:

- the result looks like a generic SaaS dashboard or startup pitch;
- the main diagram has been simplified into unrelated cards;
- the page has no actors, flow, decision, or explanatory relationship;
- references were requested but only text search snippets were inspected;
- decorative imagery replaces evidence;
- source excerpts lack attribution;
- a reference page has been near-traced rather than transformed into a new composition;
- generated photos could be mistaken for real client evidence;
- arrows cross labels or the direction is ambiguous;
- important exceptions or assumptions are omitted merely to make the page cleaner;
- text wraps unexpectedly or the compact tier is unreadable at full size;
- the slide is flattened when editable objects are expected;
- a recreated diagram is a single raster image or its main logic cannot be edited component by component;
- a chart that should be native has no editable data series;
- the host toolchain cannot preserve native, selectable PPTX components;
- compatibility rendering, overflow, or package validation fails.

## Bundled assets

- `assets/japanese-corporate-ponchi-template.pptx`: editable 15-layout template.
- `assets/japanese-corporate-ponchi-layouts.png`: overview of the 15 layouts.
- `assets/annotated-source-chart-layout.png`: full-size preview of the annotated source-chart layout.

The PPTX is the portable source template. Its text boxes, shapes, connectors,
tables, annotations, and charts are intended to remain editable. The preview
PNGs are for selection and QA only.

## Public-reference and affiliation note

Names such as JEITA, Japanese ministries, and JTC are used descriptively to
identify broad document conventions. This skill is not affiliated with,
endorsed by, or distributed by those organizations. Public materials may be
studied for composition and communication grammar, but their distinctive
wording, figures, illustrations, logos, and layouts must not be copied without
permission or a valid quotation basis.
