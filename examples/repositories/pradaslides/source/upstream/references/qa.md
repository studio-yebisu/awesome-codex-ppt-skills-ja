# Quality assurance

QA is part of authoring. A deck is not complete until the final artifact is rendered, inspected, repaired, and rechecked.

## Severity

| Severity | Meaning | Ship? |
|---|---|---|
| `blocking` | Broken artifact, false claim, unreadable content, overlap, clipping, missing asset, incorrect chart, or violated invariant | No |
| `major` | Audience comprehension, credibility, accessibility, or visual system is materially weakened | Repair before delivery |
| `minor` | Polish issue with limited impact | Repair when practical; record if accepted |

## Gate 1: brief and truth

- Communication contract is complete.
- Intent, audience, delivery mode, output format, and editability are known or recorded assumptions.
- Existing-deck invariants are explicit.
- Every decision-critical claim is verified, labeled, or excluded.
- Calculations, units, periods, populations, and definitions are consistent.
- Confidential material is handled according to the brief.

## Gate 2: narrative and content

- The opening earns attention or supplies necessary orientation.
- The sequence changes the audience's mental state deliberately.
- Every substantive slide has one job and one claim.
- Claim titles match the evidence.
- Objections and limitations are handled at the right depth.
- No slide exists only because the source had a chapter on the topic.
- The close resolves the central tension and names the next action.
- Slide copy, notes, and appendix play distinct roles.

Run `scripts/lint_deck_plan.py` and resolve all blocking findings before visual production.

## Gate 3: visual system

Deck-level montage review:

- coherent palette, typography, grid, and image treatment;
- intentional pacing between dense, sparse, visual, and synthesis slides;
- no monotonous sequence of identical cards;
- section changes are legible;
- no accidental outlier in color, margins, title location, or density;
- cover and closing feel related to the body.
- material language, edge language, and furniture behave as one system rather than isolated decorative choices;
- planned slide families show intentional variation in macro composition, image occupation, density, and tone;
- a reference-led deck has not drifted into a generic palette/card approximation of its selected quality floor.

Slide-level full-size review:

- title hierarchy and reading order are immediate;
- headline and body scale use available whitespace deliberately; sparse slides do not leave presentation-critical copy at caption size while adding decorative geometry;
- one dominant visual idea;
- alignment and proximity expose the structure;
- whitespace is intentional;
- text is readable at target display size;
- normal text holds at least 4.5:1 contrast against its actual surface; muted/support text holds at least 3:1; verify this after backgrounds, masks, local panels, and image scrims are applied;
- images are sharp, correctly cropped, and not distorted;
- each image visibly performs its declared hero, process, product, context, detail, evidence, texture, or cutout role;
- background texture, masks, curves, overlaps, and shadows preserve contrast and do not compete with facts or copy;
- every decorative curve, crop, or illustration has an explicit compositional or semantic job; remove elements that merely slice a relevant photo or leave an unexplained fragment;
- frame choices follow the asset role and vary across the deck; portrait, process, full-garment, detail, collection, and evidence photos are not forced into one recurring shell;
- attached-media placement follows the reviewed focal point, safe region, crop tolerance, rights, and sensitivity constraints;
- browser QA reports no broken/missing-alt/distorted images and no video missing controls, poster/fallback, or accessible labeling;
- charts/tables communicate the stated claim;
- source screenshots, products, devices, charts, diagrams, and annotated artifacts retain an equivalent visual teaching job; prose-only substitution is treated as a major issue unless explicitly justified;
- instructional slides pass the three-second test: the object/system, action/distinction, and reading order are identifiable without narration;
- repeated screens remain concrete comparison units when channel/state comparison is the lesson; they are not abstracted into visually unrelated bars or cards;
- sources, footers, and page numbers fit safely;
- every audience-facing text box remains inside the declared outer safe area after final fonts load;
- independently positioned text blocks have a visible positive gap; their rendered rectangles do not intersect;
- sibling text does not enter protected figures, diagrams, charts, process rows, or card groups;
- no overlap, clipping, wrapping surprise, orphan, or placeholder;
- contrast and color encoding are accessible.

## Gate 4: technical artifact

For PPTX:

- file opens without repair warning;
- expected slide count and order;
- aspect ratio matches brief;
- titles/text are present as intended;
- notes exist where required;
- images, media, charts, hyperlinks, fonts, and relationships resolve;
- embedded/linked video uses a compatible codec, poster frame, caption/transcript when required, and a tested static fallback;
- no empty placeholders or duplicated hidden slides;
- editability matches the promised route;
- essential copy, exact labels, charts, tables, annotations, page furniture, and source lines are native objects when the deck promises editability;
- raster assets are limited to the declared photos, texture, approved art, or complex visual detail; the page is not a flattened slide image;
- package does not depend on missing local paths or remote assets.

Use `scripts/inspect_pptx.py` for a structural preflight, then open/render with an office application when available.

For web slides:

- fixed-stage layout is stable at supported viewport sizes;
- rendered text respects the slide-safe area, independent text rectangles do not collide, and text does not obstruct protected media/layout regions;
- keyboard navigation and focus work;
- presenter and audience views do not leak private notes;
- local assets load without network dependencies unless documented;
- PDF/export matches browser output closely;
- no console errors that affect presentation.

For PDF:

- correct page count and dimensions;
- fonts embedded or rendered correctly;
- selectable text when expected;
- links and accessibility tags when required;
- no crop or transparency artifacts.

## Gate 5: accessibility

- Language is declared consistently.
- Reading order is logical.
- Meaning is not encoded by color alone.
- Text/background contrast is sufficient.
- Images have alt text or a notes equivalent when the runtime permits.
- Videos have captions/transcript when required.
- Logos preserve aspect ratio, clear space, approved color treatment, and optical balance.
- Charts have a textual takeaway and source.
- Acronyms and domain language fit the audience.

## Render-and-repair protocol

1. Export the current authoring source.
2. Render all pages at final aspect ratio.
3. Create a labeled montage and review deck rhythm.
4. Inspect each page at full resolution.
5. For reference-led work, compare silhouette, focal mass, type-role contrast, material/edge language, image staging, card discipline, slide-family rhythm, native fidelity, and anti-copy integrity against the declared quality floor.
6. Inspect rendered text geometry: edge distance, title/subtitle-to-evidence gap, pairwise text intersections, text-to-protected-region intersections, clipping, and out-of-bounds coordinates.
7. Record issues with slide ID, severity, category, observation, and repair.
8. Repair the owned authoring source.

For exhaustive reference-led HTML fixtures, inspect `composition_diversity` in the browser-QA report. It must show meaningful variation in topology, registered layout, tone, density, and combined signatures without long runs of the same macro-composition. Also confirm that every slide's `referenceIds` matches the benchmark coverage mapping; `HTML_REFERENCE_TRACE` indicates a missing, extra, or swapped rendered response. Treat these as anti-regression gates; still inspect whether the variation supports the slide's communication job.

For presenter-console QA, require the transformed 16:9 stage bounding box to remain entirely inside `.stage-viewport`. `HTML_CONSOLE_STAGE_FIT` means the canvas is clipped, distorted, or drifting underneath the rail/inspector despite valid slide-internal geometry.
9. Re-export and re-render every affected slide; rerender all slides if global tokens changed.
10. Repeat until all blocking and major issues are closed.

Do not accept an issue merely because it is inherited from a template when it makes the delivered deck unusable. Escalate invariant conflicts instead of silently breaking them.

## Content stress tests

- Can the audience repeat the main takeaway after seeing only the titles?
- Can a reviewer trace every important metric?
- Does removing a slide break the argument? If not, consider removing it.
- Does every visual change what the audience understands?
- Are the strongest counterargument and limitation represented fairly?
- Are recommendations linked to owners, timing, and consequences?

## Delivery check

- filenames are clear and versioned;
- `exports/` contains no scratch files;
- final deck, source, preview, source ledger, and QA report agree;
- editability limitations and required fonts/assets are stated;
- links use final artifact paths;
- original user files remain unchanged unless explicitly authorized.

## QA report statuses

Use `qa-report.json` with:

- `not_run`: required check has not happened;
- `passed`: evidence recorded and no issue;
- `failed`: blocking issue remains;
- `accepted`: user explicitly accepted a non-blocking trade-off;
- `not_applicable`: check does not apply, with reason.

Never mark a render check `passed` from code inspection.
