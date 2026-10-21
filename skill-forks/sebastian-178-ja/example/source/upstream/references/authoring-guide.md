# Authoring Guide

This guide defines the end-to-end workflow for authoring HTML presentation decks with this skill.

Reference materials must be abstracted into neutral patterns. Do not copy source logos, company names, confidentiality language, client names, or identifying marks into generated HTML.

Generated user decks should not show MBB Page Maker, archetype, agency, or placeholder brand marks. Use no visible logo unless the user supplies one. Keep footers to page number plus an optional neutral deck title; do not add source notes, "prepared by" text, consulting-firm-style footers, or archetype footer copy unless supplied by the user.

## System Layers

The design system is layered by responsibility:

1. `assets/css/fonts.css`: webfont imports and font-family variables.
2. `assets/css/base.css`: 16:9 slide canvas, typography defaults, footer, runtime controls, print rules, and shared tokens.
3. `assets/css/layouts.css`: page shells, regions, slots, grids, split areas, and blank layout structures.
4. `assets/css/components.css`: reusable semantic blocks such as agenda grids, tables, charts, cards, profiles, and objective lists.
5. `assets/css/illustrations.css`: neutral illustration primitives and asset slots.
6. `assets/themes/*.css`: color tokens, light/dark mode values, accent behavior, and theme-level visual direction.
7. `assets/media/`: optional static resources such as supplied images, screenshots, generated visuals, diagrams, and showcase-only filler assets.
8. `templates/`: editable composed pages, snippets, full-deck archetypes, and showcase patterns.
9. `examples/`: independent public demo decks.

Keep the base library structure-first. Components and blank layouts should not hard-code brand colors, image treatment, decorative effects, or source-specific marks. Themes and showcase/full-deck examples carry the visual treatment.

Generated decks must load the static files in that order: fonts, base, layouts, components, illustrations, exactly one theme file, then `assets/js/runtime.js`. Do not create a CSS bundle, inline duplicate CSS, add deck-specific remote font imports, or add a build step. Use the shared local font declarations in `assets/css/fonts.css`; `scripts/render.sh --package` inlines those local font files for delivery.

Dark backgrounds must always activate a dark token context. Use `.dark`, `[data-mode="dark"]`, `[data-tone="dark"]`, `.dark-cover`, or `[data-variant="dark-cover"]`; do not set a dark background alone. The token context is what flips text, muted text, rules, panels, and accents for every theme.

The runtime adds a slide-level `auto-dark` safety class when it detects a dark slide background without a dark token context. Treat this as a guardrail, not an authoring pattern: authors should still declare the mode explicitly and run the contrast audit before delivery.

## Template Roles

- `templates/starter-deck.html`: default generation starting point for new decks. It stays light: title cover, simple agenda/context, blank content page, and ending page.
- `templates/deck.html`: design-system gallery and review tour, not the default generation template.
- `templates/full-decks/`: complete deck archetypes for agent-facing storyline and composition reference.
- `examples/`: independent public demo decks; do not use them as authoring sources unless explicitly recovering demo content.
- `templates/neutral-skeleton.html`: structure-first baseline.
- `templates/light-skeleton.html`: default analytical pages.
- `templates/dark-skeleton.html`: dark cover, divider, and high-emphasis shell.
- `templates/mixed-skeleton.html`: mixed dark/light narrative example, not the default choice for generated decks.

Skeletons do not need identical page inventories. They must share the same CSS/JS load order, 16:9 fit rules, and ordinary slide contract, and each should contain at least one page where a component can be inserted safely.

When the user does not specify a visual style, start from a light or neutral analytical body and keep the deck tonally consistent. Dark pages are deliberate exceptions for the cover, closing, section dividers, or a few high-emphasis narrative moments. Do not use the mixed skeleton or alternate dark and light body pages simply to make the deck feel more lively.

When the user explicitly specifies a tone, make it consistent across the deck. Use mixed dark/light pacing only when requested or clearly supplied as a reference, not as the default way to add energy.

## Composition Order

Use this order when building a deck:

1. Inspect the user's material and identify the communication task.
2. For strategy, board, investment, pitch, transformation, or full-deck work, use `references/consulting-thinking.md` to define the audience, decision, answer, evidence, and action.
3. Draft the storyline and answer-first page messages.
4. Build an evidence inventory and use `references/content-to-exhibit-router.md` to check whether the input has enough data for specialized components or combination showcases.
5. For full decks, inspect relevant archetypes in `templates/full-decks/` after reading `references/full-decks.md`; adapt or diverge based on the user's material.
6. Create a slide plan before writing HTML.
7. Choose the simplest layout that can hold the message.
8. Place one primary component, or a small stack of related components, inside the layout's content slot.
9. Apply one theme file.
10. Add static assets only when the user supplies them, approves external data use, or the deck explicitly needs them.
11. Render and verify the slide at 16:9.
12. Run `scripts/check-deck-quality.sh path/to/deck.html` and fix empty section pages or missing evidence components.
13. Run `scripts/check-deck-contrast.sh path/to/deck.html` and fix any failed text/background contrast pairs.
14. Run `scripts/check-deck-fit.sh path/to/deck.html` and fix clipped content or out-of-bounds elements.
15. Render the default package, PDF, and PNG with `scripts/render.sh path/to/deck.html` unless the user requested HTML only.

Do not start from color, effects, or images. Start from message, data shape, layout, and component fit.

When the user's material is sufficient, infer the authoring choices and generate the complete deck plus default exports. Do not stop at recommendations, a suggested outline, or a page-by-page menu unless the user explicitly asks for planning output.

## Slide Planning Gate

Before writing deck HTML, make a compact internal plan. For every slide, define:

- Message: the answer-first title or section purpose.
- Evidence source: user-provided material, clearly marked assumption, or approved external data.
- Evidence shape: numeric, categorical, comparison, time, risk, decision, qualitative, quote, contact, or mixed.
- Layout: the shell from `templates/layouts/` or starter/skeleton variant.
- Selected component: the reusable component(s) from `templates/components/`.
- Selected showcase pattern: the closest page combination from `templates/showcase/README.md` when a full-page pattern is useful.
- Fallback: the simpler qualitative component or omitted page to use if evidence is insufficient.
- Output role: cover, executive answer, data evidence, comparison, roadmap, decision, appendix, or closing.

The slide plan is an internal authoring aid unless the user explicitly asks to see or approve a plan.

Do not proceed to HTML when a body slide has no component choice. The only valid component-light pages are cover, closing, and deliberate section dividers in longer decks. Deliberate pure dividers must use `data-allow-divider="true"` so quality checks can distinguish intent from accidental empty pages.

For short decks, avoid pure section dividers. If the user asks for three sections, each section should usually start with an evidence page or a section-intro page that contains 2-4 metrics, a mini catalog, or a clear summary. A page that only says "Section 02 / Data support" is too weak when the source contains enough data to chart, rank, compare, or tabulate.

If useful structured data exists, do not replace it with only prose cards. Cards are acceptable for synthesis, but evidence pages should show the data structure with an appropriate component.

If structured data does not exist, do not fabricate it. Pick a qualitative layout and make the uncertainty explicit through a callout, issue tree, decision log, or hypothesis page. A sparse source should become a clear qualitative deck, not a data-looking deck with invented metrics.

## Source Fidelity And External Data

The user's material is the primary source of truth. Every claim, number, comparison, risk, decision, date, quote, owner, and contact used in the deck must trace to one of these:

- user-provided material
- a clearly marked assumption, hypothesis, risk, or open question
- external data the user explicitly requested or approved

Do not browse or add public market data by default. If public or current data would materially improve the deck and the user has not authorized it, ask for permission before searching. If permission is not granted, proceed with the supplied context and make the gap visible as an assumption or open question.

When external data is approved, keep it separate in the slide plan and use it only to support the specific page where it improves the argument. Do not add generic source footers or consulting-style provenance text. If provenance is necessary, use a compact appendix, assumption page, or user-supplied note.

## Question Gate

Do not ask the user to choose page layouts, component names, or full-deck page sequences. Those are authoring decisions the skill should infer.

Ask only when the missing answer materially changes the deck:

- audience or decision
- hard constraints such as length, language, confidentiality, format, deadline, or tone
- permission to use external data
- required fields for a promised chart, table, timeline, matrix, quote, or contact page

If the user provides enough material, continue without asking and choose conservative defaults.

## Evidence Extraction

When the user provides a report, notes, transcript, or raw text file, extract the deck substance before choosing slides:

- Claims: management conclusions, analyst views, user asks, and stated recommendations.
- Quantitative facts: revenue, growth, margin, valuation, share, count, timing, ranges, and rankings.
- Comparisons: peers, segments, regions, customers, alternatives, industries, historical periods.
- Causal drivers: why performance changed, why the opportunity exists, why risk matters.
- Uncertainty: missing verification, rumors, assumptions, dependencies, or conflicting signals.
- Decisions: what the audience should approve, monitor, defer, or investigate.
- Voices and gaps: real quotes, stakeholder objections, missing proof, and open questions.

If external data is approved, extract it separately from the user's material and label it as external in the slide plan.

Then route the extracted material through `references/content-to-exhibit-router.md`. The router should decide whether the page needs a primitive component, a combination showcase pattern, or a simpler qualitative fallback. Use the strongest evidence as exhibits and put weaker or repetitive details into notes, appendix, or omit them. Do not make a slide for every paragraph in the source.

For sparse prompts, produce a qualitative deck with explicit assumptions, open questions, and decision points. For data-rich prompts, make the structure visible with evidence components instead of flattening the material into prose cards.

## Storyline Logic

Build decks as a coherent executive argument, not a collection of pages. The deck should answer the audience's question, then support that answer with the minimum necessary evidence.

Storyline workflow:

1. Define the audience and decision: who is reading, what decision or understanding do they need, and what will they do next?
2. State the governing answer: the top-level recommendation, finding, or conclusion.
3. Group supporting points into 2-5 mutually distinct, non-overlapping pillars.
4. Sequence pages so each page advances the argument.
5. Use exhibits to prove or clarify claims, not to decorate.
6. End with implications, decisions, next steps, or appendix as appropriate.

Preferred narrative shape:

1. Context: why this matters now.
2. Answer: the main conclusion or recommendation.
3. Evidence: facts, data, comparisons, or qualitative support.
4. Implication: what the evidence means.
5. Action: decision, roadmap, owner, or next step.

## Slide Title Rules

Content slide titles should be answer-first. A reader should understand the page's point from the title before studying the exhibit.

Good title behavior:

- Use a complete, meaningful sentence for content pages.
- State the conclusion, contrast, implication, or decision.
- Keep one main message per slide.
- Make titles specific enough to distinguish pages from each other.
- Keep section divider titles short when the page is only a divider.

Avoid:

- Generic content titles such as "Overview", "Analysis", "Findings", "Data", "Chart", or "Discussion" on evidence pages.
- Question titles unless the slide is deliberately framing an unresolved decision.
- Titles that describe the exhibit type rather than the insight.
- Multiple unrelated messages in one title.

Examples:

- Weak: "Market overview"
- Strong: "Demand is growing fastest in the two segments where the company already has channel access"
- Weak: "Cost analysis"
- Strong: "Labor and logistics explain most of the margin gap versus priority peers"
- Weak: "Next steps"
- Strong: "The team should validate three assumptions before committing to full rollout"

## Page Message Discipline

Every content page needs a clear page message:

- Claim: what the page is saying.
- Evidence: what proves or supports it.
- Implication: why it matters for the audience.

If a page has evidence without a claim, write the claim before choosing the layout. If a page has a claim without evidence, use a statement/callout page or ask for the missing evidence.

## Content Sufficiency Gate

Before selecting a specialized page, inspect the user's input:

1. Identify the data type: contacts, metrics, time series, categorical values, prose themes, decisions, roadmap steps, or mixed records.
2. Choose the component family, then choose the variant from record count, group labels, semantic roles, density, and layout hierarchy.
3. Check whether required fields exist.
4. If fields are missing, choose a simpler layout or omit the page.
5. Never invent names, numbers, roles, dates, sources, or group labels.

Examples:

- Contacts: use a contact roster only with enough contact records.
- Contact networks: use grouped sections when people are organized by region, practice, capability, or expertise; use a sidebar roster only when one group is clearly secondary.
- Numeric categories: use a bar chart only with labels and values.
- Exact multi-field data: use a table.
- Sparse prose: use statement, cards, or callout.
- Ordered phases: use timeline or roadmap.

## Layout And Component Fit

Blank layouts are designed to prevent components from resizing the slide canvas, but they cannot make unlimited content fit. `.content`, `.region-body`, `.safe-fill`, and `.safe-stack` provide bounded slots; if content is too large, the correct response is to simplify, split, or choose another layout.

Fit rules:

- Ordinary slides use `section.slide > header + .content + footer`. Cover, ending, and full-bleed pages are deliberate variants.
- Insert components only inside `.content`, `.region-body`, `.safe-fill`, or `.safe-stack`.
- A single direct child of ordinary `.content` fills the available content height by default; multi-child content areas should let their component CSS allocate vertical space. Mark compact exhibits with `.is-fit-content`, `data-fit-height="content"`, or a centered content class.
- Prefer `blank-content.html` when one component owns the page. Its `.blank-content-slot` is the default ordinary-page entry point for generated content.
- Use region layouts only when the page needs separate zones.
- Keep one primary component per region.
- Use `safe-stack` only for small components that support the same message.
- If text or data overflows, reduce fields, split the page, or use a wider layout.
- Do not shrink typography below legible slide scale to force content into a region.

Alignment and visual balance:

- Keep title, content, and footer aligned to the same page grid unless the layout deliberately creates separate regions.
- Preserve enough whitespace around dense tables, charts, and agendas.
- Vertically center compact single-component pages and compact region layouts with `.content.is-vertically-centered` or `.content[data-align-y="center"]` when the content would otherwise sit in the top half of the slide.
- Treat paired short exhibits as compact too. If both sides of a two-column body page are primary content and both are short, such as a 3-5 row table beside a 3-4 row ranked bar chart, two compact scorecards, or a small roadmap beside a short implication stack, center the whole content block vertically.
- When a custom split wrapper sits inside centered content, do not let the wrapper or its direct child stacks force `height: 100%`; use `height: auto`, `.is-fit-content`, or `data-fit-height="content"` so the centered content height is based on the exhibit, not the full safe area.
- Keep dense tables, tall timelines, multi-section dashboards, and pages with intentional top/bottom staging top-aligned.
- For sparse individual regions, use `.region-body.is-centered` so cards, callouts, and supporting notes sit in the visual middle of their safe slot.
- Keep separator lines sparse. The title rule should have breathing room below the title, and ordinary region layouts should not use an outer border unless framing is the point.
- Do not let a small component float alone in a large region; use a simpler centered page or add a relevant supporting component.
- Do not fill empty space with invented content.
- Keep repeated components visually consistent: same heading length, similar line count, and parallel field order.

## Browser Presentation

`assets/js/runtime.js` is the only runtime required for interactive HTML decks:

- Arrow keys, PageUp/PageDown, and Space move through slides.
- Left/right click areas move backward or forward.
- Touch horizontal swipe and trackpad horizontal wheel move slides.
- Slide changes use a short transition and edge bump so click, keyboard, touch, and trackpad navigation feel responsive without adding dependencies.
- `o` toggles overview thumbnails; Escape exits overview.
- `?print=1` activates print/export mode, shows all slides, and hides controls.
- `?preview=N&export=1` renders one slide without chrome for iframe galleries and screenshot automation.
- `?slide=N&export=1` is the canonical browser screenshot mode for one slide. Use a 1600x900 viewport when capturing from `index.html`.

Present mode uses a fixed 1600x900 slide canvas that scales as a whole to the browser viewport. Do not add runtime behavior or CSS breakpoints that reflow slide internals for narrow browser widths.

## Quality Audit

Run the quality audit before contrast and export:

```bash
scripts/check-deck-quality.sh path/to/index.html
```

The script fails section-like or low-density body slides that have no evidence/component structure. This catches the common failure mode where an agent creates a page such as "Section 02 / Data support" even though the section should contain charts, tables, rankings, matrices, or metrics.

The script also fails obvious generic body-slide titles such as "Overview", "Analysis", "Findings", "Data", "Chart", "Discussion", "Market overview", or "Cost analysis". A content page title must communicate the conclusion or decision implication, not just name the topic or exhibit type.

The script fails remote runtime, stylesheet, image, font, or media references in the source deck file. Generated decks and delivery packages must remain self-contained.

When the audit fails:

- Add a real evidence component to the slide.
- Merge the divider into the next evidence page.
- Or, only for longer decks where pacing genuinely needs a pure divider, add `data-allow-divider="true"`.
- Rewrite generic content titles as answer-first messages.
- Replace remote dependencies with local, embedded, generated, or repo-native assets.

## Fit Audit

Every generated deck should pass the browser fit audit:

```bash
scripts/check-deck-fit.sh path/to/index.html
```

The script opens each slide in headless Chrome at 1600x900 with `?slide=N&export=1&fitAudit=1`, then fails when visible text-bearing elements are clipped by bounded containers or when visible elements render outside the slide. This catches the screenshot failure mode where a page looks acceptable in source HTML but a card, table, title, or footer is cut off in the delivered `index.html`.

If the audit fails:

- Reduce fields, rows, columns, or text length.
- Split dense evidence across slides.
- Choose a wider or denser layout that has a bounded slot for the component.
- Remove fixed heights from custom wrappers unless the component deliberately owns the full content height.
- Do not solve failures by adding mobile breakpoints, making the slide scroll, shrinking text below legible scale, or hiding overflow that contains real content.

## Contrast Audit

Every generated deck should pass the built-in visibility audit:

```bash
scripts/check-deck-contrast.sh path/to/index.html
```

The script opens the deck in headless Chrome with `?print=1&audit=1`, computes real browser styles, and fails on text/background contrast below WCAG-style thresholds: 4.5:1 for normal text and 3:1 for large or bold text. Use it after changing themes, adding dark section dividers, inserting image overlays, or writing inline styles.

If the audit fails:

- Add `.dark`, `[data-mode="dark"]`, `[data-tone="dark"]`, `.dark-cover`, or `[data-variant="dark-cover"]` to dark slides.
- Move dark panels into a proper dark token context or choose a lighter panel token.
- Do not patch failures by hiding text, shrinking text, or hardcoding one-off colors in components.
- Prefer theme tokens over inline colors so the same deck works across `mono`, `blue`, `red`, `green`, and custom themes.

## Next Pattern Pass

Future passes should add only neutral, reusable patterns that are justified by real deck-generation cases. Keep source-inspired taxonomy out of visible page headers and public showcase titles.

## Asset Path Rule

When copying snippets into a real deck, normalize asset paths to the deck location:

- `templates/*.html`: usually `../assets/...`
- `examples/<name>/index.html`: usually `../../assets/...`, independently maintained public demo.
- generated deck folders from `scripts/new-deck.sh`: usually `assets/...`

Before delivery, use `scripts/render.sh path/to/index.html`. The default export creates `dist/package/index.html`, `dist/package/index.pdf`, `dist/index.pdf`, and `dist/png/` for browser, WeChat file preview, and WeChat image preview use cases. When package and PDF export are both enabled, the generated PDF is also copied to `dist/package/index.pdf` so the share folder exposes the browser and printable files together. The package step rewrites local paths and inlines local CSS, JavaScript, and media into `dist/package/index.html`, so that final HTML file can be opened directly by a browser without the source asset tree.

The delivery package must not depend on remote runtime resources. Do not use CDN chart libraries, remote images, deck-specific remote font imports, dynamic script/module loaders, or stylesheet imports in generated decks. The exporter intentionally fails if the package still contains external stylesheets, external scripts, CSS `@import`, remote font URLs, or non-embedded media URLs.

## Static Asset Rule

Use static assets only as content or showcase material:

- Supplied photos, screenshots, diagrams, or generated images belong in `assets/media/`.
- Generic components should not require images.
- Showcase-only assets can demonstrate visual possibilities but should not become default generation behavior.
- If an image is required, use a layout with an explicit media slot and verify that cropping does not hide the subject.
