# Design and visual system

## Design from communication

Visual design should make relationships, emphasis, sequence, and evidence easier to perceive. A visually striking page that obscures the intended inference is a failure.

Define one system before slide-by-slide styling:

- `communication_mode`: speaking, hybrid, or reading;
- `visual_character`: 3–5 specific adjectives with behavioral implications;
- grid, margin, safe area, alignment anchors, and spacing scale;
- type roles and fallbacks;
- color roles and contrast rules;
- image, chart, table, diagram, icon, and motion grammar;
- layout families and rules for variation.

## Four structural principles

Use these in order:

1. **Proximity:** group related items and separate unrelated groups.
2. **Alignment:** make every element belong to a visible structure.
3. **Repetition:** repeat meaningful roles—type, color, geometry, and placement—to build coherence.
4. **Contrast:** create unmistakable hierarchy through size, weight, color, form, direction, or space.

Group the information before decorating it. Contrast must be decisive; weak variation looks accidental.

## Grid, flow, and whitespace

- Use consistent outer margins and a small set of column structures.
- Define `safe_x` and `safe_y` once in the design system. For a 16:9 slide, use at least `3%` of slide width and `4%` of slide height as the default audience-text exclusion zone; increase it for projection, print trim, or branded furniture.
- Treat the safe area as a measurable boundary. Titles, paragraphs, labels, and captions must remain inside it after real fonts load. Full-bleed images, background color, and intentional decoration may extend beyond it.
- Use shared grid anchors, CSS Grid/Flexbox, or measured content flow for adjacent regions. Avoid independently guessing absolute `top`, `left`, `width`, and `height` for text blocks whose line count can change.
- When absolute positioning is justified, reserve the preceding block's rendered height plus an explicit gap. Re-run bounding-box checks after copy, font, viewport, or token changes.
- Choose reading flow deliberately: left-to-right, top-to-bottom, Z, F, radial, or guided sequence.
- Use whitespace to reveal grouping and priority.
- Keep focal elements away from accidental edge tension unless full bleed is intentional.
- Do not fill empty regions with decorative objects merely to “balance” the slide.
- Vary composition across the deck while preserving anchors such as title position, page number, or grid.

## Typography

Default projected minimums:

| Role | Minimum | Typical live range |
|---|---:|---:|
| Hero/cover | 44 pt | 54–80 pt |
| Slide title | 35 pt | 38–52 pt |
| Subhead | 24 pt | 26–32 pt |
| Body | 16 pt | 18–28 pt |
| Source/footer | 9 pt | 10–12 pt |

These are safety defaults, not targets. Use larger type whenever the room or content permits.

Use type contrast intentionally across six axes: size, weight, structure, form, direction, and color. Avoid too many type families. Use fonts that exist or can be embedded/licensed; declare fallbacks. Keep line lengths readable and test actual rendering because browser and PowerPoint metrics differ.

Never solve overflow by repeatedly shrinking text. Edit, split, reframe, or move detail to notes/appendix.

### Text geometry contract

For every rendered slide:

- no audience-facing text crosses the declared safe area;
- no independent text rectangles overlap by more than antialiasing tolerance;
- no sibling text enters a figure or another protected evidence/layout region;
- no text box clips, overflows, or leaves the slide;
- the gap between a title/subtitle region and the next independent region remains visible at the final font metrics;
- footer/furniture exceptions are explicit and never silently inherited by content.

In HTML, use shared custom properties such as `--safe-x` and `--safe-y`. Figures are protected by default; mark other independently positioned diagrams, charts, process rows, or card groups with `data-no-text-overlap`. Mark only intentional exceptions with `data-edge-safe="ignore"` or `data-text-overlap="allow"`. In PPTX, apply the same coordinates in slide units and verify them from the final render. These exception markers are for deliberate furniture or designed text-on-media interaction, not for silencing a failed layout.

## Color

- Assign semantic roles: background, primary text, secondary text, accent, positive, warning, negative, and data series.
- Use one dominant accent and reserve strong color for meaning.
- Maintain contrast under projection and grayscale where relevant.
- Do not use hue alone to encode a category or status; add labels, shapes, or patterns.
- For data, keep unrelated series subdued and highlight the series that carries the claim.
- Distinguish screen RGB choices from print/PDF behavior when both outputs matter.

## Images

An image must do at least one job: prove, explain, locate, compare, humanize, establish tone, or create a meaningful metaphor.

For user-supplied photos, video, logos, screenshots, charts, and illustrations, follow [media-intelligence.md](media-intelligence.md) before selecting a layout.

- Prefer real, relevant, high-resolution assets when they exist.
- Crop for the slide's claim, not simply for visual drama.
- Keep faces, products, and evidence out of text-safe zones.
- Use `contain` for evidence that must be fully visible and `cover` for atmospheric/full-bleed treatment.
- Add a contrast mask behind text over photography.
- Credit or license assets as required.
- Never use generic handshake, meeting, rocket, target, or lightbulb imagery as a substitute for thinking.
- Do not generate an image containing core copy, exact metrics, tables, or chart labels.

### Visual evidence retention

When redesigning source material, preserve the communication job of every visual carrier. A screenshot may establish procedure, a product image may make a category concrete, a device may identify a channel, and a chart may prove a behavior. Keeping the words while removing those carriers is content loss.

Use this order: supplied factual artifact → sanitized/annotated artifact → rights-cleared equivalent → faithful native reconstruction → simplified diagram → prose-only fallback. Document why a lower-evidence form is necessary.

## Chart selection by question

| Audience question | Preferred form |
|---|---|
| What is the exact value? | Table |
| How did it change over time? | Line; bars for a small number of periods |
| Which items rank higher? | Sorted horizontal bars or dot plot |
| How far from target/baseline? | Diverging bar, bullet graph, or variance table |
| What is the distribution? | Histogram, box plot, strip/dot plot |
| Are two measures related? | Scatter plot |
| How do categories contribute to a total? | Stacked bar only when comparison remains legible |
| What is the flow or conversion? | Stage bars or labeled flow; use a funnel only when width encodes a valid quantity |

Chart rules:

- State the message in the title.
- Label units, time period, population, and comparison basis.
- Start bar axes at zero unless a clear and justified exception is disclosed.
- Avoid 3D, perspective, unnecessary gradients, shadows, and decorative data ink.
- Use direct labels when possible; reduce legend lookup.
- Do not use a pie chart when precise comparison matters.
- Highlight the evidence needed for the claim; mute the rest.
- Verify that chart type, data, labels, and verbal conclusion agree.

## Tables

Use tables for lookup and exact comparison. Create hierarchy with alignment, whitespace, subtle rules, and number formatting—not heavy boxes around every cell. Right-align numbers, align decimal precision, keep units consistent, and highlight only decision-relevant rows or columns.

## Diagrams

Use native shapes for simple relationships and process flows. Use a graph-layout engine for complex networks when available, then simplify the result for slide reading.

Diagram rules:

- Give each node a short label and a defined role.
- Make arrow direction and semantics unambiguous.
- Use spatial position to encode a relationship, not arbitrary decoration.
- Keep process order, hierarchy, ownership, state, or feedback loops visually distinct.
- Avoid equal-card layouts when the elements are not equal.
- Label assumptions at system boundaries.

## Icons and illustration

- Use icons to improve scanning or encode repeated categories, not as filler.
- Keep stroke, fill, optical size, and corner language consistent.
- Prefer one icon family.
- Use illustration when a scene, mechanism, or metaphor is difficult to source and materially helps understanding.
- Keep image-generation prompts free of copyrighted-style imitation and avoid embedding required text.

## Motion

Use motion to reveal sequence, preserve focus, or demonstrate change. Avoid motion when it merely decorates. Build a static fallback and test export because browser animation, PowerPoint transitions, and PDF have different capabilities.

## Layout families

Maintain a limited but flexible set:

- cover/hero;
- section divider;
- claim + single visual;
- split claim/evidence;
- comparison;
- timeline or process;
- chart-led analysis;
- table-led decision;
- case-study before/after;
- quote/testimonial;
- synthesis/summary;
- decision or call-to-action;
- appendix/detail.

Do not force every slide into cards. Select layout from the information relationship.

## Reference-derived visual directions

The supplied reference set clusters into reusable directions. Treat these as principles, not templates to copy:

| Direction | Useful for | Defining behavior | Risk to control |
|---|---|---|---|
| Editorial fashion | Portfolio, brand, lookbook | asymmetric crops, restrained type, tactile neutrals | style overpowering proof |
| Corporate technical | Strategy, product, report | blue/white clarity, diagrams, measured grid | generic template feel |
| Dark cinematic tech | Fintech, launch, keynote | deep field, luminous focal object, sparse copy | weak readability or cliché glow |
| Bold creator | Creative portfolio | oversized condensed type, black + vivid accent, collage | density and inconsistent hierarchy |
| Minimal case-study | Portfolio, async case | strong whitespace, modular proof, precise captions | looking empty without a claim |
| Warm personal brand | Creator/social portfolio | portrait-led identity, burgundy/red, approachable structure | repetitive biography cards |
| Visual teaching studio | Workshops, creator education, product training | concrete devices/artifacts, color-coded steps, annotation, friendly texture | busy collage, tiny screenshots, or prose replacing proof |
| Product UI system | Product/UX | device frames, interface details, system components | tiny screenshots and UI-wall effect |
| Sustainability editorial | ESG, innovation, proposal | natural imagery, acid accent, clean data | decorative “green” claims |
| Sculptural luxury | Fashion/product launch | art-directed still life, serif display, large whitespace | low information density |
| High-energy startup | Pitch/portfolio | strong accent, big numbers, modular rhythm | visual noise and unverified metrics |

## Visual reference method

For every reference, record:

1. intent it appears to serve;
2. composition and reading order;
3. typography roles;
4. palette roles;
5. media treatment;
6. density and pacing;
7. transferable pattern;
8. anti-pattern or constraint.

Keep source-specific visual audits outside the runtime skill. This file contains only the synthesized directions and rules needed during slide production.
