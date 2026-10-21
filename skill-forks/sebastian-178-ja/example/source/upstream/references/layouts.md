# Layout Catalog

Use simple layouts when the message is the point. Use complex layouts only when the audience must understand multiple moving parts on one page.

## Composition Model

Layouts are page shells. Components are inserted into layout content areas. Themes are applied last.

The base layout and component library should stay visually neutral. Color, decorative line fields, image treatment, and dark/light effects belong to theme files, showcase pages, or deliberate layout variants.

When adding a layout, read `references/adding-patterns.md` first. Add a new layout only when existing bounded slots cannot support a recurring communication job. Every ordinary layout must preserve the slide contract, provide safe insertion slots, and validate at 16:9 without relying on viewport reflow.

Slides are fixed 16:9 canvases. Browser present mode scales the whole slide to the viewport; it must not reflow the slide internals based on viewport width. Do not add mobile breakpoints that collapse grids, sidebars, charts, or component layouts inside `.slide`.

Default ordinary slides use a 64px horizontal safe area and 36px top/bottom safe area. A single direct child inside `.content` should normally fill the available content height so the page has a clear bottom boundary near the footer. Multi-child content areas should let the component own vertical allocation. Use `.content.is-vertically-centered`, `.content[data-align-y="center"]`, `.is-fit-content`, or `data-fit-height="content"` only for deliberately compact exhibits.

Dense evidence pages can opt into `section.slide.is-dense` or `templates/layouts/dense-content.html`. Use this for chart, table, matrix, risk-register, and similar pages that need a stable header band, body band, and footer rule. Dense content keeps the footer border as the bottom seal and reserves 24px of bottom clearance so x-axis labels or bottom captions do not touch the footer line. Do not use dense mode for sparse, centered, or small narrative pages.

Line economy matters. The default page should not feel boxed in:

- The title rule is a subtle separator below the title, not a tight underline.
- Region layouts do not draw an outside border by default. Add `.has-border` only when the page needs a deliberate framed tool surface.
- Prefer whitespace and alignment over extra box outlines.
- Use internal separators only when they clarify comparison, table structure, or region boundaries.

Choose pages by communication job and data shape, not by a fixed template map. A layout can host many component combinations:

- A `blank-right-sidebar` page can hold a chart plus implications, a table plus decisions, or a diagram plus risks.
- A `blank-split-even` page can compare two options, two markets, two operating models, or two evidence blocks.
- A `data-dashboard` page can combine metrics, charts, tables, and callouts depending on the user's data.
- A simple centered page can be better than a specialized page when the input is sparse.

Layout selection router:

- Single exhibit: use `blank-content.html` when one chart, table, matrix, diagram, quote, or roadmap owns the page.
- Evidence plus implication: use `blank-right-sidebar.html`, `blank-right-rail.html`, or `mixed-evidence-implication.html` when the exhibit needs interpretation beside it.
- Balanced comparison: use `blank-split-even.html` when two options, segments, markets, or operating models need equal weight.
- Wide table or chart: use `blank-content.html` or `blank-right-rail.html`; do not place dense tables or long-axis charts in narrow sidebars.
- Decision page: use `blank-content.html` or `blank-right-sidebar.html` with `decision-log`, `comparison-table`, `pros-cons-table`, `outcome-support`, or `callout`.
- Roadmap/workplan page: use `blank-content.html`, `roadmap-swimlane.html`, `phase-roadmap`, `milestone-track`, `gantt-workplan`, or a right-rail layout for compact risks or decisions.
- Sparse concept page: use `statement`, `default-center-message`, `outcome-support`, `framework-map`, `cause-effect`, or `callout`; do not force a chart, table, matrix, or roadmap without required fields.
- Data dashboard: use `data-dashboard` only when the page has multiple related metrics or exhibits that support one message. If the page has one exhibit, use `blank-content.html`.
- Section-intro page: in long decks, use a divider only for pacing; in short decks, prefer a section intro with 2-4 proof points, assumptions, or decisions.

If the source evidence is sparse, choose a simpler statement, callout, cards, or outcome-support page rather than forcing a complex layout.

Alignment rule: the component's visual mass should match the slide grid. Compact tables, short roadmaps, small scorecards, and paired lightweight exhibits should be vertically centered rather than pinned to the top with empty lower space. Dense tables, tall timelines, dashboards, and pages with deliberate top/bottom staging should stay top-aligned.

Use:

1. `templates/starter-deck.html` for a new generated deck.
2. `templates/neutral-skeleton.html` for structure-first drafting.
3. `templates/layouts/blank-content.html` for the simplest full-content component page.
4. `templates/layouts/*.html` for page shells.
5. `templates/components/*.html` for reusable blocks.
6. `assets/themes/*.css` for final color direction.

## Simple Layout Families

- Cover: title, subtitle, date/meta, optional client mark.
- Starter deck: four-page generation base with title cover, simple agenda/context, blank content page, and ending.
- Simple title cover: title, optional subtitle/meta, optional abstract visual. Must include a main title.
- Default opening: simple first page with optional neutral visual treatment. Must include a main title.
- Default opening with visual: title page with one image or product/context visual slot.
- Centered message: one conclusion centered on the page.
- Centered list: 3-5 short points for a transition or focus page.
- Centered metric: one headline number when there is not enough data for a chart.
- Default ending: clean closing page with optional next-step or contact note.
- Dark cover: section-opening or high-emphasis narrative page.
- Statement: one conclusion, one support line, no exhibit.
- Quote: stakeholder voice or customer evidence.
- Media split: short message plus neutral illustration.
- Visual support page: one repo-native visual primitive plus a short implication, caveat, or use rule.

Default simple snippets:

| file | use when |
| --- | --- |
| `blank-content.html` | One component or a small component stack should occupy the main content area. |
| `dense-content.html` | One dense chart, table, matrix, or register needs a fixed body band and footer clearance. |
| `simple-title-cover.html` | Basic deck title page. Do not use a brand-only page as the default title cover. |
| `default-opening.html` | Deck or section start. |
| `default-opening-visual.html` | Opening page with one relevant supplied/generated visual. |
| `default-center-message.html` | One conclusion, transition, or decision prompt. |
| `default-center-list.html` | A short set of parallel points. |
| `default-center-metric.html` | One verified number plus meaning. |
| `default-ending.html` | Closing, next-step, or appendix pointer. |

Selection guidance:

- Use simple pages when the point is stronger than the exhibit.
- Use centered pages for emphasis, not for dense explanation.
- In short generated decks, do not use centered section dividers as a substitute for content pages. If a section has data, open it with a data-bearing page or a compact section-intro page.
- Use visual opening pages only when the visual adds meaning. Otherwise keep the opening clean.
- A blank/brand-only cover is not a valid default cover. Use it only as a deliberate divider or showcase page.
- Use `templates/showcase/visual-patterns.html` when a page needs a supportive visual. Do not add visuals to data-rich pages by default; use evidence components first.

## Blank Structured Layouts

Use these when the page needs an ordinary business-slide shell before the exact component is known. They are layout slots, not content templates.

| file | use when |
| --- | --- |
| `blank-left-rail.html` | Narrow context/navigation rail plus wide primary exhibit. |
| `blank-split-even.html` | Two comparable modules with equal weight. |
| `blank-left-sidebar.html` | Setup, definitions, or assumptions on the left; analysis on the right. |
| `blank-right-sidebar.html` | Main evidence on the left; implications, risks, or decisions on the right. |
| `blank-right-rail.html` | Very wide exhibit plus a compact legend, caveat, or summary rail. |
| `blank-three-column.html` | Three comparable segments, options, phases, or evidence groups. |

The simplest shell, `blank-content.html`, uses `.blank-content-slot` inside `.content`. Use it before adding sidebars, rails, or split regions.

Structured blank shells use `.region-layout`, `.region`, `.region-body`, and `.safe-stack`. Insert components from `templates/components/` inside `.region-body`.

Ordinary layout snippets should keep the contract `section.slide > header + .content + footer`. Use cover, ending, or full-bleed variants only when that page type requires it.

Composition examples:

- `blank-content` + `catalog-grid`: one contents/catalog component owns the page.
- `blank-content` + `agenda-table`: one timed workshop agenda owns the page.
- `blank-content` + `safe-stack`: several small components support the same message in one content area.
- `blank-left-rail` + `objective-list` + primary exhibit: context/navigation on the left, evidence on the right.
- `blank-split-even` + parallel components: compare two options, markets, operating models, or evidence blocks.
- `blank-right-sidebar` + primary component + supporting component: evidence on the left, implications or decisions on the right.
- `blank-right-rail` + wide component + compact support: wide table/chart/timeline with legend, caveat, or source note.
- `blank-three-column` + comparable components: segments, options, phases, or profile groups.
- Add `.region-body.is-compact` only when multiple lightweight components share one region and the default region padding crowds the content.

Overflow rules:

- Keep each region to one primary component or a small stack of lightweight components.
- If a table, chart, or profile grid does not fit, choose a wider shell, split the page, or reduce the visible data.
- Do not shrink text below legible slide scale just to force content into a region.
- Do not add filler content to occupy empty regions. If the user did not provide enough data, use a simpler layout.
- If a single table, timeline, roadmap, flow, framework, or compact region layout only occupies the upper half of the content area, use `.content.is-vertically-centered`, `.content[data-align-y="center"]`, `.is-fit-content`, or `data-fit-height="content"` to opt out of the default fill-height behavior.
- If both sides of a two-column content page are compact primary exhibits, center the pair vertically as one block. For custom split wrappers, add `data-fit-height="content"` or `.is-fit-content` and avoid `height: 100%`.
- For sparse individual regions, use `.region-body.is-centered`.

## Medium Layouts

- Agenda: 3-9 numbered sections.
- Content catalog: numbered section grid for a deck table of contents.
- Meeting objectives: objective list plus optional summary/objectives panel.
- Workshop agenda: time/topic/outcome agenda table.
- Simple agenda: numbered agenda grid without time blocks.
- Content primitives: cards, callouts, and evidence blocks.
- KPI strip: 3-5 executive metrics with short labels.
- Table plus roadmap: dense content with structured hierarchy.
- 2x2 matrix: prioritization or segmentation.
- Risk matrix plus register: use a wide content area or right-sidebar shell only when action tracking is needed.
- Range/competency chart: use a wide content area because row labels, gaps, and scale markers need horizontal space.
- Dot-scale or range comparison: use a wide content area; add a sidebar only for interpretation notes.
- Pie/donut split: use split-even or blank-content when the total and legend can remain legible.
- Contact roster: only when the user provides enough real contact data and one group is clearly primary while another is supporting.
- Contact network: when the user provides named experts or contacts grouped by geography, practice, capability, industry, function, or expertise. Use peer group sections rather than a sidebar when the groups have equal weight.
- Chart and takeaways: one chart plus 2-4 implications.
- Heatmap assessment: capability/maturity/fit data with row and column categories.
- Diverging heatmap: use blank-content and keep rows/columns bounded; split across pages if labels or cells overflow.
- Data dashboard: headline metrics plus 1-2 supporting exhibits.
- Structure pages: use blank-content for one framework or diagram, split-even for balanced contrasts, and right-sidebar only when implications must sit beside the concept.
- Flows and funnels: use blank-content for the main sequence, right-rail only for a compact result or caveat.
- Timelines and journeys: use blank-content for one chronology or roadmap, split-even only for side-by-side comparisons.
- Tables, lists, and quotes: use wide blank-content for tables, sidebars for small quotes, and full blank pages for large quotes.

Medium pages usually combine one dominant component with supporting components. Keep the page logic top-down: title first, exhibit second, implications third.

Agenda and objectives snippets include `content-catalog.html`, `meeting-objectives-list.html`, `workshop-agenda.html`, and `simple-agenda.html`. They should be treated as examples of component composition, not fixed outputs.

## Complex Layouts

- Issue tree: root question, drivers, and evidence branches.
- Waterfall bridge: baseline-to-target value movement.
- Roadmap swimlane: workstreams across phases.
- Split light/dark shell: contrast page or transition page.
- Profile grid: team, expert, or stakeholder roster.
- Framework map: one core concept with surrounding operating elements.
- Compass choice: strategic directions around one decision.
- From-to multi: multiple current-to-target shifts.
- Process flow: ordered activity sequence.
- Stage gate: phases plus decision checkpoints.
- Value chain: linked operating activities.
- Phase roadmap: staged implementation path.
- Journey map: stakeholder experience across phases.

Use complex layouts only when the source material has enough structure. If the user gives prose without drivers, values, phases, or dimensions, use cards, statement, or a blank structured shell instead.

Structure composition rules:

- Use `pyramid-stack` for hierarchy, not for unordered categories.
- Use `cause-effect` only when the causal link is the point of the page.
- Use `outcome-support` when the answer should lead and the support points are parallel.
- Use `diverging-textboxes` for two prose positions; use `comparison-table` when criteria need row-level precision.
- Use `framework-map` for conceptual systems; use `process-flow` or roadmap components when sequence matters.
- Use `process-flow` for sequence, `stage-gate` for decision checkpoints, and `value-chain` for handoff logic.
- Use `funnel-steps` or `filter-cascade` only when the source has narrowing logic.
- Use `timeline`, `phase-roadmap`, `milestone-track`, or `horizon-bands` when timing or staged progress is the organizing logic.

Process, time, and text composition rules:

- `blank-content` is the default safe shell for a single flow, funnel, roadmap, table, or large quote.
- `blank-right-rail` works when a wide exhibit needs a compact legend, implication, or result note.
- `blank-split-even` works only for balanced comparisons, such as two journeys or two lists.
- Tables should not be placed in narrow sidebars. Use a wide region or split into multiple pages.
- Small quotes can sit in sidebars; large quotes should own the page.

## Illustration Rules

- Use neutral illustrations only: abstract orbit, stacks, flows, systems, or placeholder avatar forms.
- Do not copy source deck logos, company names, client names, confidentiality text, or identifying marks.
- The illustration must support the title's business message.
- Keep illustrations secondary to the conclusion unless the page is explicitly a conceptual visual.

`templates/starter-deck.html` is the default generation base. It contains a cover, simple agenda/context page, blank content page, and ending page. The blank content page is the default ordinary page before the agent decides whether the source material needs a chart, table, matrix, diagram, or other component.

Current gallery layouts live in `templates/deck.html`: cover, dark cover, section divider, agenda, split shell, content primitives, statement, media split, quote, table/roadmap, KPI strip, 2x2 matrix, issue tree, waterfall, roadmap swimlane, and profile primitives.

Structure-pattern showcase pages live in `templates/showcase/structure-patterns.html`: pyramid stack, cause-effect, outcome-support, diverging textboxes, from-to multi, compass choice, and framework map.

Conceptual-variant showcase pages live in `templates/showcase/conceptual-variants.html`: issue tree, iceberg model, capability coverage map, and framework-map comparison.

Process-pattern showcase pages live in `templates/showcase/process-patterns.html`: process flow, stage gate, funnel steps, filter cascade, loop cycle, value chain, cycle/cascading flow, decision flowchart, fishbone, vertical process takeaway, process deep dive, triangle steps, and screen filter grid.

Flow and workplan variant showcase pages live in `templates/showcase/flow-workplan-variants.html`: chevron ribbon, swimlane process map, customer journey loop, input-process-output layers, dense Gantt, and phase meeting plan.

Time-pattern showcase pages live in `templates/showcase/time-patterns.html`: timeline track, horizon bands, journey map, phase roadmap, milestone track, horizon curve, journey arc/wave, Gantt workplan, stair-step timeline, calendar workplan, and schedule list.

Data-visualization variant showcase pages live in `templates/showcase/data-visualization-variants.html`: line chart, combo chart, paired bars, Likert bars, waterfall bridge, and checkmark-bar table. Classic consulting data story variants live in `templates/showcase/data-classic-consulting-variants.html`: competency gap range table, benchmark range narrative, tornado bars, chart pairs, stacked bridges, and part-to-whole explanation pages.

Text-pattern showcase pages live in `templates/showcase/text-patterns.html`: large quote, small quote, quote insight, quote grid, numbered list grid, dense list, contents card grid, six-column list, conversion list, story block list, step explanation strip, icon outcome grid, wide data table, status table, decision log, and pros-cons table.

Analysis-table variant showcase pages live in `templates/showcase/analysis-table-variants.html`: ranked evidence table, driver recap columns, matrix table, and wide analytical table.

People-variant showcase pages live in `templates/showcase/people-variants.html`: contact roster, contact network, team wall, and bio card grid.

Dedicated skeleton starters do not need identical pages; they demonstrate different roles while sharing the same output contract:

- `templates/neutral-skeleton.html`: opening, centered message, blank analytical shell, ending.
- `templates/light-skeleton.html`: default analytical pages plus blank and simple evidence shells.
- `templates/dark-skeleton.html`: dark cover, divider, dark blank emphasis page, split shell.
- `templates/mixed-skeleton.html`: dark cover, light analytical page, evidence/implication, visual concept, roadmap, dark transition.

Upcoming validation work should use full-deck examples to test cross-section component combinations, storyline continuity, and visual balance.

Current full-deck validation files live in `templates/showcase/full-deck-operating-case-mono.html` and `templates/showcase/full-deck-operating-case-blue.html`. They are review fixtures, not the default generated demo deck.

Reusable layout snippets include `templates/layouts/contact-roster.html` for primary/supporting contact pages and `templates/layouts/contact-network.html` for grouped expert-network pages.

Blank structured layout snippets include `templates/layouts/blank-left-rail.html`, `blank-split-even.html`, `blank-left-sidebar.html`, `blank-right-sidebar.html`, `blank-right-rail.html`, and `blank-three-column.html`.

Layout and component CSS are separated:

- Layout shells: `assets/css/layouts.css`
- Components used inside layouts: `assets/css/components.css`
- Illustration primitives and asset slots: `assets/css/illustrations.css`
