# Scenario: Social Covers and Cards (HTML)

Use this workflow for social covers, article headers, thumbnails, share squares, vertical stories,
and same-ratio card sequences authored as deterministic HTML/CSS. Treat the result as a
fixed-canvas publication graphic, not a shortened presentation deck or a responsive website.

The authoritative canvas definitions live in
[`../../scripts/config.py`](../../scripts/config.py). Follow
[`../shared-standards.md`](../shared-standards.md) for project structure, template-content
separation, settled-DOM export, asset rules, and synchronized delivery.

This workflow adapts useful planning and composition ideas from the
[Guizang social-card skill](https://github.com/op7418/guizang-social-card-skill) and the social
canvas model in PPT Master, but SeaSlides dimensions, compiler behavior, validation profiles, and
delivery artifacts remain authoritative here.

## Contents

1. [Scenario contract](#scenario-contract)
2. [Route the deliverable](#route-the-deliverable)
3. [Run the end-to-end workflow](#run-the-end-to-end-workflow)
4. [Build a content system](#build-a-content-system)
5. [Plan a card sequence](#plan-a-card-sequence)
6. [Choose the exact canvas](#choose-the-exact-canvas)
7. [Define safe zones](#define-safe-zones)
8. [Rewrite titles across ratios](#rewrite-titles-across-ratios)
9. [Choose a visual stance](#choose-a-visual-stance)
10. [Compose the whole vertical page](#compose-the-whole-vertical-page)
11. [Select a layout recipe](#select-a-layout-recipe)
12. [Handle images](#handle-images)
13. [Treat screenshots as evidence](#treat-screenshots-as-evidence)
14. [Use generated imagery safely](#use-generated-imagery-safely)
15. [Implement the HTML project](#implement-the-html-project)
16. [Build multiple ratios](#build-multiple-ratios)
17. [Validate and compile exact outputs](#validate-and-compile-exact-outputs)
18. [Run visual, DOM, and factual QA](#run-visual-dom-and-factual-qa)
19. [Correct problems proportionally](#correct-problems-proportionally)
20. [Deliver and record provenance](#deliver-and-record-provenance)
21. [Quick Mode defaults](#quick-mode-defaults)
22. [Non-negotiables](#non-negotiables)

## Scenario contract

- Keep editable content in semantic `content.html` and reusable visual rules in `template.css`.
- Preserve the three-file HTML architecture: `index-template.html`, `template.css`, and the content
  entry. Do not collapse delivery into an unvalidated standalone HTML file.
- Author one fixed numeric canvas or several pages that all share exactly one canvas.
- Give every additional ratio its own synchronized build. Share copy, tokens, and assets; do not
  share coordinates or crop the first artifact into the others.
- Keep every page in a settled static DOM state. Delivery content must not depend on scroll,
  animation progress, hover, focus, timers, network responses, or user interaction.
- Do not reveal required content through JavaScript. Runtime code belongs only in the approved
  project shell and must settle before capture.
- Preserve every factual claim, name, number, date, quotation, screenshot state, and call to
  action. Compression is not permission to invent or exaggerate.
- Compile and inspect every page. Source validation and a successful browser capture are necessary,
  but neither alone is visual approval.
- Approve the browser PNGs at full output size and feed size. Compare synchronized derivative
  artifacts only after the Chromium baseline passes.
- Make the full canvas feel resolved through the lower edge. Do not leave an accidental blank
  bottom band. Internal columns and modules do not need equal height or mechanical stretching.

### Divide responsibility across the reference systems

Use the local references as complementary layers, not as code to transplant unchanged.

| Reference | Take from it | Do not import blindly |
|---|---|---|
| [`local/guizang-social-card-skill`](../../../../local/guizang-social-card-skill/SKILL.md) | Content-first hook design, Editorial and Swiss identity tests, image-led quiet-zone rules, marginalia/ledger recipes, and lower-edge resolution | Platform-specific code, licensed source, or decorative motifs without the content job that justified them |
| [`local/ppt-master` canvas formats](../../../../local/ppt-master/skills/ppt-master/references/canvas-formats.md) | Exact social canvases, ratio-specific reading direction, safe zones, and the distinction between ratio and coordinate system | PowerPoint Master/Layout metadata or slide coordinates |
| [`local/ppt-master` image-layout catalog](../../../../local/ppt-master/skills/ppt-master/references/image-layout-patterns.md) | Full-bleed fields, side images, image bands, negative-space covers, evidence overlays, and deliberate crop/contrast relationships | Pattern coverage for its own sake or empty image frames when no qualified asset exists |
| [`local/ppt-master` visual review](../../../../local/ppt-master/skills/ppt-master/references/visual-review.md) | Full-size inspection, contrast and collision checks, focal-point review, and a separate thumbnail pass | Its SVG/PPTX-specific exporter mechanics |
| SeaSlides HTML templates and synchronized build | Semantic ownership, template/content separation, settled-DOM capture, browser baseline, DOM audit, and derivative fidelity | Responsive-web assumptions inside a fixed social canvas |

The working order is: use Guizang-style reasoning to decide the content job and genre, use PPT
Master-style planning to choose the canvas and image relationship, express the result through the
SeaSlides template/content contract, then judge the browser output at both native and feed size.

## Route the deliverable

Classify the request before writing copy or CSS.

| Deliverable | Structure | Communication job | Typical output |
|---|---|---|---|
| Cover or thumbnail | One page | Stop the scroll and make one accurate promise | Browser PNG, PNG, optional PDF |
| Article header | One wide page | Establish subject and tone at small preview scale | Browser PNG and PNG |
| Share square | One square page | Preserve the core object and action | Browser PNG and PNG |
| Carousel or card set | Several pages at one ratio | Move from hook to explanation, proof, and action | Ordered PNGs plus PDF |
| Story or vertical cover | One 9:16 page | Work inside platform interface-safe zones | Browser PNG and PNG |
| Cross-platform family | Sibling builds, one per ratio | Preserve the message while recomposing hierarchy | Separate receipts and outputs |

A cover usually needs one hook, one supporting cue, and optional identity metadata. It is not a
mini article. A carousel can carry a fuller argument, but every page must make one audience move.

Use several pages only when sequence helps: problem to mechanism, claim to evidence, old state to
new state, or steps to action. Do not pad a one-page idea into a fashionable page count.

## Run the end-to-end workflow

### 1. Prepare the project and source

Reuse the current SeaSlides project when one exists. Otherwise initialize a project through the
normal project manager. Keep original files under `sources/` and approved visual material under
`assets/`.

Convert PDF, DOCX, PPTX, spreadsheet, or URL input with the standard source tools before extracting
hooks. Preserve links, image captions, page references, and provenance beside the converted text.

Use one explicit content entry for a same-ratio set, such as `content-xhs.html`. Mixed-ratio work
should use sibling project directories or independent entries with independent template contracts
and output locations.

### 2. Resolve only artifact-changing decisions

Lock:

- deliverable type, target platform, and exact dimensions;
- required page count only when specified;
- exact names, dates, logos, handles, calls to action, and legal text;
- brand palette, font restrictions, and forbidden treatments;
- asset route: supplied, sourced, generated, screenshot-led, or type-led;
- language variants and whether each needs a sibling composition;
- requested delivery formats and filename convention.

Bundle genuine blockers into one question. In Quick Mode, use the defaults near the end of this
file and state assumptions in the handoff.

### 3. Audit source truth

Create a fact ledger:

| Item | Exact source-backed value | Source location | Allowed rewrite | Risk |
|---|---|---|---|---|
| Main claim | Verbatim meaning | Page, URL, or user message | Shorten without widening scope | High |
| Number | Value, unit, denominator, period | Table, figure, or record | Preserve definition | High |
| Quote | Speaker and context | Transcript or article | Paraphrase unless exact words matter | High |
| Product state | Version and date | Screenshot or release note | Describe visible behavior only | High |
| Identity | Approved name, title, handle, logo | User or brand source | Preserve spelling and marks | Medium |
| Call to action | Destination and label | Approved brief | Shorten label, not destination | Medium |

If a number is undefined, omit it. If a screenshot does not prove the copy, do not use it as
evidence. Surface source conflicts instead of choosing the more promotional value.

### 4. Compress and plan

Use the five-level compression ladder. Write a page-role table, assign evidence, select a visual
stance, and choose a recipe before writing DOM markup.

### 5. Establish the template contract

Define canvas tokens, safe zones, typography, palette, page shell, metadata, image treatment,
screenshot stage, and every content class in `template.css`. Keep `content.html` semantic and free
of ad hoc visual styling.

### 6. Author a representative pair

Build the cover and the densest planned page first. Use the actual longest title, label, CJK line,
screenshot, and font. Assemble, run the source gate, compile, and fix the system before filling all
pages.

### 7. Compile, inspect, and revise

Run a synchronized build at the exact canvas and scale. Inspect the Chromium baseline, DOM audit,
fidelity report, derivative PNGs, overview, and PDF. Make at least one measured correction pass for
a new design.

## Build a content system

### Use a five-level compression ladder

Compress in this order:

1. **Core claim** — one accurate sentence the complete artifact must preserve.
2. **Viewer promise** — what the reader will understand, verify, or be able to do.
3. **Section map** — four to eight ideas for a substantial carousel.
4. **Page hooks** — short, concrete lines carrying one audience move each.
5. **Body fragments** — only the words needed to interpret the visual or evidence.

The images form a visual outline, not the complete article. Put secondary explanation in the post
caption, source page, or linked article.

### Write consequential hooks

Prefer:

- a concrete transformation or user-facing change;
- a specific tension or common mistake;
- a defined number with meaning;
- a verb-led action;
- a question the sequence actually answers;
- a contrast the next page can prove.

Avoid production labels, unexplained hype, generic category words, and several unrelated claims on
one cover. `Recompose the message` is more useful than `Social design system` when the page teaches
cross-ratio work.

### Separate copy levels

| Level | Job | Typical length |
|---|---|---|
| Display hook | Carries the page at feed size | One to four short lines |
| Support line | Clarifies object, scope, or promise | One sentence |
| Metadata | Orients issue, page, date, source, or identity | A few compact labels |

Delete a support line that merely repeats the hook. Reduce metadata contrast when it competes with
the main message.

### Write semantic line breaks

Break at phrase boundaries. Keep verbs with objects, numbers with units, and product names intact.
Do not rely on browser wrapping to make an important display title look intentional.

Use `<br>` only for a deliberate display break, not to manufacture vertical spacing. Test every
language separately; translated copy will not keep the same geometry.

For a short CJK serif display hook, inspect the actual rendered font before accepting default
spacing. If two to eight large glyphs look cramped, test a small positive `letter-spacing` around
`0.02em-0.06em`; longer lines usually need less. Keep body copy at normal spacing, and do not copy
the same value onto bold sans or mono text. When CJK and italic Latin form one title, give the two
phrases an explicit gap of roughly `0.25em-0.35em` instead of relying on a typed space.

## Plan a card sequence

Use a planning table:

| Page | Role | Audience move | Hook or claim | Evidence | Recipe | Asset and safe-zone note |
|---:|---|---|---|---|---|---|
| 1 | Hook cover | Stop | Strongest source-backed promise | Optional cue | Cover | Protect title and subject |
| 2 | Problem or context | Recognize | Concrete tension | Scene, quote, or fact | Essay or scene | Keep context readable |
| 3 | Explanation | Understand | One mechanism | Diagram or fragments | Pipeline or split | One reading path |
| 4 | Evidence | Believe | Defined claim | Screenshot, table, or comparison | Evidence feature | Proof remains legible |
| 5 | Application | Act | What to do next | Checklist or example | Ledger | Action verbs visible |
| N | Close | Remember | Summary, question, or CTA | Source and identity | Closing note | Resolve lower edge |

Useful page roles:

- hook cover;
- problem scene;
- misconception versus reality;
- number with definition;
- screenshot evidence;
- before/after comparison;
- checklist or buying guide;
- three-to-five-step process;
- pull quote or thesis;
- section divider;
- summary, question, or action.

Five to nine cards is a useful range for a substantial carousel, not a quota. Merge weak pages,
split overloaded pages, and let source depth determine length.

### Create sequence rhythm

Use at least four or five distinct shapes in a seven-page sequence. Alternate dense and quiet,
type-led and evidence-led, full-width and stacked structures. Never place two full-bleed image
covers back-to-back; a strong image page benefits from a structured page after it.

Keep recurring orientation elements stable: issue label, category, page number, source, footer
position, and accent logic.

## Choose the exact canvas

Use the named HTML canvases in `scripts/config.py` unless the target platform specifies another
exact size.

| Format key | Browser canvas | Ratio | Typical use |
|---|---:|---:|---|
| `xiaohongshu` | 1242 × 1660 CSS px | 3:4 | Cover or same-ratio carousel |
| `moments` | 1080 × 1080 CSS px | 1:1 | Share square or social post |
| `story` | 1080 × 1920 CSS px | 9:16 | Story or vertical cover |
| `wechat` | 900 × 383 CSS px | 2.35:1 | WeChat article header |
| `banner` | 1920 × 1080 CSS px | 16:9 | Web banner or digital display |

At compiler scale `--ppi 1`, one CSS pixel maps to one output pixel in the browser PNG baseline.
Pass `--width` and `--height` explicitly for scenario builds even when CSS tokens already match;
the command then records the intended numeric canvas in the synchronized build.

Platform requirements override presets. If the user requests 1080 × 1440, use those exact values
rather than substituting 1242 × 1660 because both are 3:4.

Do not treat same-ratio canvases as the same coordinate system. A 1920 × 1080 banner and a 1280 ×
720 presentation require different type sizes, safe zones, and delivery checks.

## Define safe zones

Use these as conservative starting points, then verify in the target platform preview:

| Canvas | Starting safe zone | Common overlay risk |
|---|---|---|
| Xiaohongshu 3:4 | 7–9% left/right, 6–8% top, 8–12% bottom | Feed crop, account chrome, action area |
| Square 1:1 | 7–9% all sides; reserve more at bottom if needed | Share preview and action row |
| Story 9:16 | 10% top, 18–20% bottom, 10% right | Account header, reply field, controls |
| WeChat header 2.35:1 | 5–7% left/right | Small preview crop and title collision |
| Banner 16:9 | 6–8% left/right and 8–10% bottom | Platform badge or duration overlay |

Safe zones protect critical copy, faces, logos, proof, and actions. Backgrounds may bleed to the
edge. Keep the values as CSS custom properties in `template.css`, not inline style in content.

```css
:root {
  --slide-width: 1242px;
  --slide-height: 1660px;
  --safe-x: 96px;
  --safe-top: 108px;
  --safe-bottom: 150px;
}
```

## Rewrite titles across ratios

Cross-platform work is recomposition, not cropping. Preserve the core object, action, result, or
number while rewriting length and hierarchy.

### Derive the short title

Try:

1. verb plus object;
2. object plus change;
3. meaningful number plus object;
4. strongest clause from a two-clause title;
5. one strong noun or verb when metadata restores context.

For a Chinese square, four to ten characters or two short lines is a useful target, not a hard
limit. For English, prefer two to six stressed words with deliberate breaks.

```text
Wide title: Design for the ratio, not for the crop
Square hook: Recompose the message
Support: One promise. A new hierarchy for every ratio.
```

Do not copy the complete wide title into the square and shrink it. Do not obtain the square by
clipping the header. Write a new `<h1>` and assign a ratio-specific composition class.

### Audit the result

- Core object remains recognizable.
- Meaning and scope match the source.
- Title is readable at approximately 360 px preview width.
- `<br>` occurs at a semantic boundary.
- Support restores context without repeating the title.
- Sibling ratios look intentionally related, not mechanically cropped.

### Audit text flow, not only font size

Treat wrapping, column rhythm, and empty space as part of the copy edit. A card can use generous
type and still fail because its sentences break badly or its paragraphs have been forced into an
artificial layout.

- Let prose blocks keep natural height. Do not use equal `1fr` tracks or distributed flex spacing
  merely to make paragraphs fill a column; reserve equal tracks for genuinely parallel cards,
  stages, or time slots.
- Read every captured line. Rewrite or add an intentional `<br>` when a wrap strands a short CJK
  fragment, punctuation mark, unit, particle, or half of a mixed-language phrase.
- In a narrow rail, add real padding after an accent bar, rule, or panel edge. A visible border is
  not padding; confirm that two-digit markers, opening quotation marks, and first glyphs survive
  capture.
- If secondary copy disappears at feed size, first widen its measure, shorten the sentence, raise
  contrast, or simplify the hierarchy. A global font-size increase is only one possible repair.
- Let unused height become intentional quiet space only when it is held between meaningful
  anchors. A pull quote, decision follow-up, evidence caption, or closing strip is preferable to
  stretching unrelated paragraphs apart.

Review the full-resolution capture for exact line endings, then review the same page around 360 px
wide for hierarchy. Both views must pass; browser-level readability does not excuse a feed-size
rail that visually vanishes.

## Choose a visual stance

Style is a communication stance, not a topic lookup.

### Editorial

Use an authored hierarchy with serif or Songti display type, paper or ink atmosphere, strong image
wells, marginal notes, pull quotes, ledgers, rules, folios, and captions. Editorial is not a flat
cream page with a serif title inside generic cards. Include at least one real editorial structure:
photo well, marginalia column, pull quote, essay split, ledger, or atmospheric field.

#### Light Editorial and marginalia

A light page is not a low-contrast page. Use warm paper, decisive ink, one restrained accent, and a
real publication structure.

- Let one large photograph carry roughly half the active page when imagery is the subject. Move
  the title outside the image when no verified quiet zone exists.
- Pair Chinese serif display type with italic Latin only when both parts form one phrase. The
  italic word supplies cadence, not ornamental branding.
- Use fine rules, folios, captions, and issue metadata as secondary structure, with enough contrast
  to survive browser capture and derivative export.
- A marginalia layout needs two meaningful reading speeds: a main essay/evidence column and a
  narrow column containing useful schedule, source, caption, or observation notes. Empty sidebars
  are not atmosphere.
- Resolve the lower edge with a caption, closing thought, image continuation, or issue strip. Do
  not preserve a large white tail simply because the upper half already feels refined.
- Keep paper atmosphere subtle. At feed size, grain should nearly disappear rather than becoming
  a repeating CSS wallpaper.

### Swiss or system-led

Use a strict underlying grid, sans-serif hierarchy, large light-weight display type, one accent
color, hairlines, straight modules, explicit numbering, and disciplined alignment. The grid is a
layout system, not a mandatory graph-paper background; draw only the rules that organize content
or encode a real diagram. Avoid default shadows, inflated rounded cards, dashboard ornament, and
several accent hues.

### Image-led

Use the photograph as the composition. Map subject and quiet zones first, then place restrained
copy. Re-crop every ratio. If the subject fills the available region, move copy off-image or use a
framed image rather than masking the subject.

### Brand-led or expressive

Use approved brand palette, type, marks, illustration, and repeatable graphic devices. Preserve
identity without turning every module into a logo treatment. Never fabricate missing logos.

### Identity tests

An Editorial page needs more than serif type. A Swiss page needs more than blue and a grid. Remove
the style label mentally: if the page still looks like a generic slide or SaaS dashboard, strengthen
the structure rather than adding ornaments.

## Compose the whole vertical page

Tall canvases expose layouts copied from 16:9. Plan from top to bottom.

### Use vertical zones

For 1242 × 1660, treat these as diagnostics:

| Zone | Approximate share | Role |
|---|---:|---|
| Header and metadata | 5–8% | Category, issue, page, date |
| Display title and lead | 18–30% | Hook and promise |
| Evidence or main body | 40–55% | Image, screenshot, ledger, comparison, diagram |
| Closing or consequence | 8–15% | Takeaway, CTA, caption, issue strip |
| Footer and safety | 4–8% | Identity, source, page number, clearance |

Not every page needs five visible bands. The model reveals where the reading path stops.

### Resolve the lower edge without mechanical fill

The whole page must feel designed through the bottom. An empty lower band with no purpose fails.
Resolve it with real content or structure:

- conclusion, consequence, or action;
- large evidence image or screenshot;
- caption or source band;
- continuing photograph, texture, or color field;
- stable footer, identity, or page metadata;
- alignment between upper and lower anchors;
- a semantically rich module that can legitimately grow.

Do **not** require every column, card, or grid cell to have equal height. Unequal internal endings
are valid. Do not stretch a small reference block into an empty panel, inflate padding, enlarge
decoration, or invent copy to occupy space.

Active composition around 75–78% is a useful warning threshold for dense portrait cards, and an
unexplained blank band larger than roughly 15% deserves revision. These are diagnostics, not
mechanical quotas. A thesis page can be airy when top, middle, and bottom anchors make the pause
intentional.

### Avoid empty spacer hacks

Do not insert an empty `div` with `flex: 1` only to push the footer down. Use a grid or flex page
shell whose flexible region contains the actual main field. `margin-top: auto` is valid for a
footer when the complete composition has meaningful upper content and the footer visibly closes
the page.

Revise when the lower quarter is abandoned, a screenshot is too small to read, a short ledger sits
in the middle third, or every page repeats the same shallow title-and-cards pattern.

## Select a layout recipe

The codes below are planning shorthand, not required CSS classes.

### Editorial recipe matrix

| Code | Recipe | Best for | Minimum meaningful content |
|---|---|---|---|
| M01 | Issue cover | Carousel opening | Hook, cue or image, issue strip |
| M02 | Field-note photo | Place, object, observation | Evidence photo, caption, takeaway |
| M03 | Essay split | Nuanced explanation | Title plus two or three fragments |
| M04 | Pull quote or thesis | One core sentence | Thesis, context/source, top/bottom anchors |
| M05 | Checklist | Practical advice | Four to six consequential rows |
| M06 | Evidence wall | Several references or images | Readable grid plus interpretation |
| M07 | Closing note | Final summary | Takeaway, four to six substantive rows, closing block |
| M08 | Tall ledger | Roles, pros/cons, capabilities | Four to six deep rows |
| M09 | Atmospheric thesis | Sparse important point | Large thesis, notes, visible field |
| M10 | Evidence feature | One decisive asset | Large proof, headline, caption band |
| M11 | Marginalia essay | Moderate explanatory text | Main column plus real margin evidence |
| M12 | Section divider | Mid-sequence pause | Section name, promise, metadata |
| M13 | Hero question | Closing or pivot | Short question, prompt, anchors |
| M14 | Vertical pipeline | Three-to-five-step process | Verb and consequence per step |
| M15 | Before and after | Old/new or misconception/reality | Matched comparable fields |
| M16 | Image-led cover | One excellent photograph | Subject map, title, identity cue |

### Swiss recipe matrix

| Code | Recipe | Best for | Minimum meaningful content |
|---|---|---|---|
| S01 | Accent cover | Product, method, release, or system opening | One hook, system cue, metadata strip |
| S02 | Two signals | Two sources, options, or directions | Two matched modules and one explicit difference |
| S03 | Data layer | File, state, memory, or source of truth | One object plus three or four properties |
| S04 | Interface frame | UI, interaction, or output layer | One readable interface and functional cues |
| S05 | Trap rows | Problems and anti-patterns | Three consequential warning rows |
| S06 | Pipeline | Workflow or layered architecture | Three stages with action and consequence |
| S07 | Takeaway ledger | Final page or operational summary | Thesis plus three substantive ledger rows |
| S08 | Image hero | One strong photo, object, or product render | Large asset, overlay title, defined cues |
| S09 | KPI tower | Three or four comparable measures | Defined numbers, units, proportional encoding |
| S10 | Horizontal bars | Five to ten ranked items | Real or normalized values and consistent scale |
| S11 | Stacked ledger | Quantified inventory or expense rollup | Four to six number-label rows |
| S12 | Matrix and hero stat | Capability inventory | Eight to twelve cells and one supported total |

### Type-led cover

Use M01 or S01 when imagery is unnecessary. Place a compact issue row in the top safe zone, make
the hook dominant, add one support line only when it clarifies scope, connect the middle and lower
page with one field or rule, and close with identity or sequence metadata.

Do not scatter decorative pills around an otherwise empty canvas.

### Tall ledger or checklist

Use M05 or M08 for an Editorial list. In Swiss, use S05 for warning rows, S07 for a closing
takeaway ledger, or S11 when every row is genuinely quantified. Each row needs a number or
category, direct title, and consequence or example. Let rows respond to content while preserving a
rhythm. Prefer rules and alignment over a stack of rounded cards.

Two or three short items need a thesis, split, or comparison—not a thin ledger. More than six dense
items usually need a second page.

### Vertical pipeline

Use M14 or S06 for three to five steps. Give each step a verb-led title and one explanatory line.
Connect them through a rail, numbering, or alignment. Split six or more steps instead of shrinking
the process.

### Before and after

Stack states vertically on 3:4 unless both are short enough for balanced columns. Use matched labels
and evidence so the comparison is fair. State what changed and what remained constant.

### Evidence feature

Give the screenshot, image, or chart roughly 45–65% of the active page when it is the proof. Use
one claim above or beside it and a compact interpretation band below. Explanatory prose belongs in
the caption if it makes the evidence unreadable.

### Pull quote, thesis, or question

Airy pages need anchors: top kicker, large statement, bottom context or prompt, and a rule or issue
strip. Quiet space is intentional only when the page still has a complete reading path.

## Handle images

### Qualify before placement

Record subject, focal point, face or product feature, quiet zones, crop tolerance, minimum useful
resolution, intended role, source, creator, license, and attribution requirement.

Reject an image as a text background when it has no stable quiet zone or when copy must cross the
subject.

### Choose fit and focal position

- `object-fit: cover` is for photographic fields with a reviewed crop.
- `object-fit: contain` is for complete diagrams, UI, captions, or evidence.
- `object-position` must follow the mapped focal point.
- A framed image is better when the subject fills the source and leaves no safe copy region.
- Every ratio gets a new crop.

Never distort an image. Do not let a default center crop remove a face, hand, title, chart label,
hardware control, or product state.

### Try no mask first

Put copy in a genuine quiet zone. If contrast fails, use a localized, image-toned tint close to the
copy. Avoid a full-canvas black scrim. When no safe zone wider than roughly one third of the canvas
exists, move copy off-image, use a smaller photo well, or build a diptych.

### Define deterministic CSS treatments

Put treatments in `template.css`:

```css
.photo-well {
  min-height: 680px;
  overflow: hidden;
}

.photo-well > img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 35%;
}

.image-tint-left::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(23, 30, 36, 0.28), rgba(23, 30, 36, 0) 56%);
  pointer-events: none;
}

.image-tint-left {
  position: relative;
}
```

Use a project-specific focal class when images need different positions; do not add arbitrary
inline `object-position` to `content.html`.

## Treat screenshots as evidence

Clean accidental desktop background, partial windows, notifications, cursor trails, irrelevant
tabs, and status chrome before importing. Preserve chrome only when it is part of the claim.

### Screenshot contract

- Keep the screenshot orthographic: no perspective, skew, tilt, or 3D mockup unless requested.
- Use `object-fit: contain` by default.
- Use crop only when discarded pixels do not matter.
- Make interface labels readable at output size.
- Add one concise callout instead of shrinking the UI beside a paragraph.
- Use straight padding and a quiet stage.
- Device chrome is optional and should add context, not decoration.
- Use identical treatment for before/after screenshots.

```css
.shot-stage {
  min-height: 700px;
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  place-items: center;
  gap: 18px;
  padding: 32px;
  background: var(--surface-muted);
  border: 1px solid var(--rule);
}

.shot-stage > img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}
```

```html
<figure class="shot-stage">
  <img src="assets/product-state.png" alt="Verified product state showing the selected setting">
  <figcaption class="caption">The setting is visible in version 2.4.</figcaption>
</figure>
```

Do not use AI-generated UI as evidence. Use a clearly labeled schematic when the real interface is
unavailable.

## Use generated imagery safely

Generated imagery may provide atmosphere, a conceptual illustration, texture, or a missing
non-factual scene. It must never fabricate:

- product UI or release state;
- metrics, charts, maps, dashboards, or test results;
- testimonials or people represented as real users;
- logos, certificates, publications, tickets, receipts, or evidence screenshots;
- embedded text the audience may interpret as verified content.

Keep prompts role-specific and request no text or logos. Store prompt and generation route with
asset provenance. Inspect hands, faces, geometry, unwanted text, watermark-like marks, and crop
suitability.

Prefer a type-led composition when imagery would be decorative rather than explanatory.

## Implement the HTML project

### Preserve template-content separation

Use:

```text
project/
├── index-template.html
├── template.css
├── content-xhs.html
├── content_design_spec.md
├── assets/
│   ├── product-state.png
│   └── SOURCES.md
└── output/
```

`index-template.html` owns the shell and approved runtime. `template.css` owns tokens, page modes,
components, geometry, and visual treatments. `content-xhs.html` owns semantic audience content.

Do not put `<style>`, `<script>`, `<link>`, event handlers, or arbitrary inline style in content.
Only use the data-geometry allowlist from shared standards when a real chart value requires it.

### Define canvas and tokens

```css
:root {
  --slide-width: 1242px;
  --slide-height: 1660px;
  --safe-x: 96px;
  --safe-top: 108px;
  --safe-bottom: 150px;

  --paper: #f3f0e8;
  --ink: #141c2b;
  --muted: #687080;
  --accent: #2458f5;
  --rule: #aeb4be;
  --surface-muted: #e9ecef;

  --display: 132px;
  --title: 72px;
  --body: 32px;
  --small: 22px;
  --gap: 30px;
}

html,
body {
  margin: 0;
  background: #ddd;
}

* {
  box-sizing: border-box;
}

.slide {
  position: relative;
  width: var(--slide-width);
  height: var(--slide-height);
  overflow: hidden;
}

.slide.light {
  background: var(--paper);
  color: var(--ink);
}
```

The selected template can use different values. Keep roles semantic and declare every class used by
content.

### Use a page shell with a real lower anchor

```css
.social-frame {
  width: 100%;
  height: 100%;
  padding: var(--safe-top) var(--safe-x) var(--safe-bottom);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  row-gap: var(--gap);
}

.page-footer {
  align-self: end;
  padding-top: 18px;
  border-top: 2px solid var(--rule);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 24px;
  color: var(--muted);
  font-size: var(--small);
}
```

The middle `1fr` is an actual composition region. It may contain a title field, ledger, screenshot,
or image. Do not leave it empty merely to push the footer down.

### Keep complex SVG in the template layer

Use SVG when a visual field genuinely consists of many paths: contour atmosphere, RISO
misregistration, a fold diagram, route geometry, or a measured system diagram. Put reusable SVG in
`index-template.html`, a local asset, or a template-owned component. Do not rebuild the same art
from dozens of absolutely positioned content nodes.

SVG is not a hidden copy layer. Titles, labels, numbers, sources, and calls to action stay as
semantic HTML. Avoid `<text>` in decorative SVG, and never use schematic paths to impersonate a
real map, screenshot, chart, or product state. If the SVG communicates information, give it an
accessible name and keep the same information available in the semantic content.

Choose the smallest authoring layer that preserves meaning and appearance:

| Need | Preferred layer | Reason |
|---|---|---|
| Safe zones, columns, rules, cards, and simple geometry | CSS Grid/Flexbox and ordinary HTML elements | Layout stays content-aware and easy to audit |
| Contour atmosphere, paper grain, RISO registration, architectural linework, path-heavy diagrams | Template-owned inline SVG or local SVG asset | Complex vector geometry stays coherent without dozens of absolutely positioned DOM nodes |
| Titles, labels, quotations, metrics, sources, UI copy, and calls to action | Semantic HTML | Copy remains selectable, accessible, searchable, and fact-auditable |
| Real photographs, screenshots, or approved generated illustrations | Local image asset with provenance and explicit crop | Evidence and imagery remain distinct from decorative structure |
| Data-bearing diagram | Semantic labels/values over a reusable SVG or CSS skeleton | Geometry may be reusable; exact information remains explicit and verifiable |

Do not flatten the complete card into one SVG merely because the browser can render it. A sound
default is one template-owned atmosphere/diagram layer plus semantic normal-flow content. Add an
overlay only when it has a distinct compositional job and the settled DOM remains inspectable.

### Define semantic typography

```css
.kicker {
  margin: 0;
  color: var(--accent);
  font-size: var(--small);
  font-weight: 650;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.display-title {
  margin: 0;
  max-width: 10ch;
  font-size: var(--display);
  font-weight: 300;
  line-height: 0.94;
  letter-spacing: -0.035em;
}

.lead {
  margin: 0;
  max-width: 28ch;
  color: var(--muted);
  font-size: var(--body);
  line-height: 1.35;
}

.social-cover {
  font-family: "IBM Plex Sans", "Noto Sans SC", sans-serif;
}

.cover-header {
  align-self: start;
}

.cover-main {
  min-height: 0;
  display: grid;
  align-content: center;
  gap: 42px;
}

.system-cover .cover-main {
  border-left: 10px solid var(--accent);
  padding-left: 42px;
}
```

Use language-specific classes or entries when font metrics and line breaks differ. Do not rely on
`clamp()` to rescue an untuned fixed canvas; explicit values are easier to audit.

### Author semantic content

```html
<section class="slide light social-cover system-cover" data-notes="Xiaohongshu cover; source-backed hook; no narration required.">
  <div class="social-frame">
    <header class="cover-header">
      <p class="kicker">Design system · 01</p>
    </header>

    <main class="cover-main">
      <h1 class="display-title">Design for<br>the ratio</h1>
      <p class="lead">Preserve the promise; rebuild the hierarchy.</p>
    </main>

    <footer class="page-footer">
      <span>SeaSlides</span>
      <span>01 / 03</span>
    </footer>
  </div>
</section>
```

Every page remains a `.slide`, resolves to a documented light/dark mode, uses semantic headings,
has `data-notes`, and references only declared classes and local assets.

### Use layout components, not one-off inline geometry

Define reusable project-local classes for:

- issue row and footer;
- type-led cover;
- ledger and checklist rows;
- comparison stack;
- vertical pipeline;
- evidence feature;
- image well and localized tint;
- screenshot stage;
- pull quote and section divider.

Absolute positioning is valid for deliberate overlays, full-bleed media, or anchored metadata.
Keep primary reading content in grid or flex layout so growing copy remains auditable.

### Keep fonts and assets deterministic

Prefer locally available or bundled fonts and local asset paths. Do not rely on remote runtime data,
remote images, or a font request that may settle after capture. If the approved shell loads a font,
verify the browser has completed `document.fonts.ready` before the compiler captures.

Use alt text that describes evidence, not decorative style. Remove private notifications, account
details, source paths, and metadata from assets.

## Build multiple ratios

Use sibling projects when practical:

```text
social-family/
├── shared-assets/
├── xhs/
│   ├── index-template.html
│   ├── template.css
│   └── content.html
├── wechat-header/
│   ├── index-template.html
│   ├── template.css
│   └── content.html
└── wechat-square/
    ├── index-template.html
    ├── template.css
    └── content.html
```

Each project owns numeric canvas tokens, safe zones, title wording, line breaks, crop, and output
receipt. Keep shared assets in scope through reviewed relative paths or copy them into each project
if the compiler contract requires project-local assets.

For a WeChat pair:

- write the accurate wide title;
- derive a short square hook;
- assign separate composition classes;
- choose independent image crop or type field;
- compile and validate separately;
- create a pair preview only after individual artifacts pass.

Never put different-sized `.slide` elements in one synchronized build.

## Validate and compile exact outputs

### Run the source gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project> --source-only --profile scenario --entry content.html
```

Resolve shell, TCS, undeclared-class, remote dependency, inline style, event handler, and source
structure failures before rendering.

### Compile one exact canvas

For Xiaohongshu:

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project> --all --ppi 1 --width 1242 --height 1660 --entry content.html
```

For a WeChat header:

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project> --all --ppi 1 --width 900 --height 383 --entry content.html
```

For a share square:

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project> --all --ppi 1 --width 1080 --height 1080 --entry content.html
```

The synchronized build creates SVGs, route PNGs, Chromium browser PNGs, overview, PDF, DOM audit,
fidelity report, and compile receipt. The browser PNGs are the visual baseline.

Do not use `--include-pptx` unless editable PowerPoint is explicitly requested. When it is requested,
add the flag to the same final `--all` build rather than running an unrelated one-off conversion.

### Run the artifact gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project> --require-build --profile scenario --artifact-profile visual --entry content.html
```

Use `--artifact-profile delivery` when the final build includes the full requested delivery set.
Zero blockers is required. Understand and resolve or document every review item.

## Run visual, DOM, and factual QA

### Establish the browser truth

Inspect `output/browser_pngs/` first. Then inspect `output/pngs/`, `output/overview.png`, and the PDF.
If a derivative differs from Chromium, diagnose `output/render-fidelity.json` before delivery.

Do not approve from the overview alone. It can hide small text, thin rules, subtle crop errors, and
font substitution.

### Check dimensions and sequence

- every browser PNG has the exact requested pixel dimensions at `--ppi 1`;
- expected page count with no duplicate or accidental blank page;
- stable ordered filenames;
- all pages in one build use the same numeric canvas;
- compile receipt corresponds to current source;
- no stale output from another ratio.

### Read the DOM audit

Inspect `output/dom-audit.json` for:

- elements crossing the slide boundary;
- text or images clipping their boxes;
- overlaps between content and footer;
- layout below or outside the settled canvas;
- late font or image shifts;
- unexpected hidden or zero-area audience content.

Zero blockers is required. A visually plausible screenshot does not override a measured overflow.

### Inspect full size

Verify:

- no overflow, clipping, collision, or edge contact;
- semantic line breaks and complete glyphs;
- readable proof, labels, sources, and actions;
- intentional crop with protected faces and product features;
- stable alignment, rules, spacing, and metadata;
- sufficient contrast without a heavy default mask;
- one focal point and audience move per page;
- no production vocabulary or placeholders;
- a lower edge that feels resolved rather than abandoned.

### Inspect feed size

View each page around 360 px wide. The hook, number, object, or subject must remain immediately clear.
Body copy may require a closer look, but the promise cannot. Shorten the title before shrinking it.

### Run a four-band composition check

Divide portrait pages into four horizontal bands and classify each:

- **active** — meaningful text, image, evidence, rule, or field;
- **intentional quiet** — hero breathing or safe area anchored by the composition;
- **accidental empty** — no communicative or compositional role.

Any accidental empty lower band fails. An unexplained void greater than roughly 15% of the height
requires revision. Do not fix a small overflow by creating a larger bottom hole.

The check applies to the whole page, not whether every internal grid column or card reaches the
same baseline.

### Check facts

Compare against the fact ledger:

- names, spelling, dates, version numbers, units, denominators, and periods;
- quote wording and attribution;
- screenshot state and feature claims;
- chart and table labels and sources;
- visible CTA label and destination;
- page-to-page consistency;
- long/short title equivalence across ratios.

### Check style

- one coherent visual stance;
- one accent in Swiss/system-led work;
- real editorial structure in Editorial work;
- no random blobs, stickers, nested cards, or excessive rounding;
- consistent image and screenshot treatments;
- no page that looks like a generic presentation slide placed on a tall canvas.

### Check assets and privacy

- local asset exists and has sufficient resolution;
- aspect ratio preserved;
- source, creator, license, and attribution recorded;
- no private notification, account, tab, source path, or metadata;
- generated asset is not presented as proof;
- no watermark, fake logo, or unwanted generated text;
- alt text accurately describes meaningful content.

## Correct problems proportionally

Measure the actual problem before editing.

| Problem | First correction | Escalation |
|---|---|---|
| Poor title wrap | Rewrite or add semantic break | Reduce size modestly, then change recipe |
| Small overflow | Tighten one local gap or padding | Shorten one support line |
| Moderate overflow | Compress fragments and metadata | Use a higher-capacity recipe |
| Large overflow | Split page or reduce scope | Replan sequence |
| Thin ledger | Deepen meaningful rows and consequences | Switch to thesis, split, or evidence page |
| Small screenshot | Remove adjacent prose and enlarge proof | Give screenshot its own page |
| Empty lower band | Add real conclusion, proof, caption, or footer anchor | Merge pages or change recipe |
| Footer collision | Put footer in grid/flex flow | Rework page shell; do not hide overflow |
| Late font shift | Make font deterministic and wait for readiness | Replace font or bundle it |
| Browser/route mismatch | Inspect fidelity report and unsupported effects | Simplify effect or deliver browser baseline |
| Square title too small | Derive a shorter hook | Recompose square from scratch |

For measured portrait overflow, use relative severity rather than deleting content immediately:

- up to about 3% of canvas height: one local gap or padding correction;
- about 3–7%: compress local spacing and one nonessential support fragment;
- about 7–12%: reduce one display block or select a denser recipe;
- beyond about 12%: split the page or replan scope.

After every correction, rerun source validation when markup or classes changed, rebuild, and inspect
DOM plus browser PNGs. Avoid global type shrinking to solve one page.

## Deliver and record provenance

Deliver:

- `index-template.html`, `template.css`, and every content entry;
- final Chromium browser PNGs and synchronized PNGs at exact dimensions;
- PDF sequence when useful;
- current compile receipt, DOM audit, and fidelity report;
- local assets and source/license manifest;
- assumptions, font requirements, and known limitations;
- a note identifying independently composed ratios and their titles.

Use stable names:

```text
xhs-01-cover.png
xhs-02-problem.png
xhs-03-evidence.png
xhs-04-close.png
wechat-header.png
wechat-square.png
```

State verification performed: source gate, synchronized build, artifact gate, exact dimensions,
page count, full-size review, feed-size review, factual comparison, and platform/device preview if
available.

## Quick Mode defaults

When the user requests a fast social graphic without specifying platform or style:

1. Produce one Xiaohongshu cover at 1242 × 1660.
2. Derive one accurate hook from the source or topic.
3. Use type-led design when imagery is unnecessary for meaning.
4. Choose Swiss/system-led for structured product content and Editorial for authored or atmospheric
   content unless visible brand cues require another route.
5. Extend the selected template in `template.css`; keep content semantic.
6. Run the source gate.
7. Compile at `--ppi 1 --width 1242 --height 1660`.
8. Run the artifact gate and inspect at full and feed size.
9. Make one correction pass and report assumptions.

Quick Mode reduces discovery and iteration count. It does not waive template-content separation,
source truth, exact dimensions, deterministic rendering, or visual review.

## Non-negotiables

- Keep semantic HTML as content source and reusable CSS as visual source.
- Preserve the approved three-file project architecture.
- Use the requested or configured dimensions exactly.
- Use one numeric canvas per synchronized build and recompose every additional ratio.
- Keep delivery content static and settled without interaction or remote runtime data.
- Write one accurate hook for a cover and one audience move per card.
- Shorten and rewrite before shrinking display type.
- Preserve source truth; never invent evidence, product states, metrics, or testimonials.
- Map every image subject and crop; never cover a face or essential feature.
- Treat screenshots as legible evidence, not decoration.
- Make the full page feel resolved through the lower edge without forcing every internal region to
  equal height or adding filler.
- Require zero validation blockers and inspect the Chromium baseline at full and feed size.
- Deliver source, synchronized artifacts, build audits, and asset provenance together.
