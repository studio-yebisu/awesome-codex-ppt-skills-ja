# Scenario: Academic and Research Posters (HTML/CSS)

Use this workflow when the deliverable is one physical poster page rather than a sequence of
slides. The browser canvas is the authoring surface; the synchronized compiler produces the PDF,
SVG, PNG, overview, and optional PPTX artifacts.

> **Scenario contract:** posters use a dedicated one-page source and review contract. Reusable
> palette, type, section, table, and page-frame rules belong in `template.css`; content and
> one-off single-page geometry belong in `content.html`. Do not apply the standard-slide TCS layout
> assumptions to the poster entry. Use the scenario profile and the checks below.

## Non-negotiable outcome

A usable poster:

1. produces exactly one `slide_01.svg` and one browser-rendered page;
2. contains only source-supported claims, numbers, citations, people, affiliations, logos, and
   links;
3. has one obvious primary result, decision, or question at thumbnail size;
4. remains readable at the intended physical size and viewing distance;
5. contains no browser overflow, hidden clipping, broken image, missing glyph, or font-induced
   reflow;
6. resolves the full canvas to a deliberate lower edge; and
7. does not force every column or final section to the same height merely to occupy space.

The page can use asymmetry and deliberate negative space. A footer, result field, continuing
visual, stable rule, or framed quiet zone must make that choice visibly intentional.

## Pipeline mapping

| Main pipeline responsibility | Poster equivalent | Output |
|---|---|---|
| Source processing | Step A: evidence intake | Verified content and asset inventory |
| Project initialization | Step B: project setup | Poster project with scenario entry |
| Strategy | Step C: poster decisions | Canvas, argument, density, and visual system |
| Image preparation | Step D: figure handling | Print-ready figures and optional decorative visuals |
| Execution | Step E: HTML/CSS authoring | `template.css` plus one-page `content.html` |
| Compile and review | Step F: browser-first QA | One-page synchronized build |

## Step A: Evidence intake

### A.1 Read the source

| User source | Action |
|---|---|
| Paper PDF | `python3 ${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py FILE.pdf --images all` |
| DOCX paper | `python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py FILE.docx` |
| Existing PPTX | `python3 ${SKILL_DIR}/scripts/source_to_md/ppt_to_md.py FILE.pptx` |
| URL | `python3 ${SKILL_DIR}/scripts/source_to_md/web_to_md.py URL` |
| Markdown, HTML, LaTeX, or notes | Read directly and inventory adjacent assets |
| Topic or verbal brief | Gather the structured fields below; research only when authorized |

Do not infer quantitative results from a title or abstract. Ask for the tables, figures, method
details, limitations, and citations needed to support the page.

### A.2 Required inventory

- exact title, authors, affiliations, venue, and contact route;
- primary question, result, or decision;
- evidence for each claim, including units, sample, comparison, uncertainty, and exclusions;
- method details required to interpret the result;
- limitations and unsupported inferences;
- references, acknowledgments, funding statements, and required logos;
- figures, tables, diagrams, photographs, icons, and QR-code destinations;
- physical size, orientation, bleed, safe area, and required output formats.

Use a claim-to-evidence ledger before layout:

| Poster statement | Source | Qualifier | Planned visual |
|---|---|---|---|
| Primary result | Figure/table/page | Scope and uncertainty | Hero metric, chart, or comparison |
| Method claim | Procedure/source | Sample and exclusions | Process or compact method block |
| Decision | Result plus operational rule | Stop condition | Decision band or conclusion field |
| Limitation | Discussion/source | Unsupported inference | Boundary box or footer note |

If evidence is absent, omit the statement or present it as a question. Never invent text or data to
equalize columns.

## Step B: Project setup

Create a new HTML project only when one does not already exist:

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py init PROJECT_NAME
```

Import source files using the project manager, and place figures, logos, and other required assets
in the project asset directory. Keep `content.html` as the scenario entry, `template.css` as the
reusable design layer, and `index-template.html` as the page shell.

Poster content may use documented one-off inline geometry when extracting a class would not make it
reusable. Do not copy that exception back into ordinary slide entries.

## Step C: Poster decisions

In a confirmation-driven workflow, gather the decisions below as one bundle. In Quick or YOLO
Mode, choose the best source-supported defaults and continue.

### C.1 Canvas and print contract

The venue specification is authoritative. Record:

- exact physical dimensions and orientation;
- pixel canvas used by the HTML renderer;
- bleed and safe area;
- print, digital display, or dual-use delivery;
- expected viewing distance;
- PDF, PNG, and optional PPTX requirements;
- printer requirements for color, transparency, embedded fonts, and image resolution.

Typical pixel presets are project conventions, not universal physical-print truth:

| Starting canvas | Example use |
|---|---|
| `3364 × 4756` | A0 portrait at 4 px/mm; preserves the ISO ratio |
| `4756 × 3364` | A0 landscape at 4 px/mm; preserves the ISO ratio |
| `2376 × 3364` | A1 portrait at 4 px/mm; preserves the ISO ratio |
| Custom | Venue-specific ratio or digital display |

Do not reuse a slide canvas merely because it is also landscape.

### C.2 Argument and composition route

| Route | Structure | Best use |
|---|---|---|
| Classic two-column | Question/method → evidence/interpretation | Conventional research poster |
| Three-column decision | setup → primary contrast → supported decision | Dense evidence with distinct column jobs |
| Asymmetric evidence | narrow context + wide result | Figure- or method-heavy argument |
| Result billboard | narrow context + dominant conclusion + narrow interpretation | One strong bounded result |
| Visual-first | hero diagram/image + compact evidence rail | Spatial, environmental, design, or systems work |
| Operational audit | windows, failures, stop rules, action | Service and implementation studies |

Every region needs a communication job. Regions do not need equal widths, equal numbers of cards,
or equal internal bottom edges.

### C.3 Density

- **Standard evidence-led:** one or two major figures, readable prose, visible result and limits.
- **Dense research:** more method and table detail, but still one dominant result and clear path.
- **Minimal billboard:** a conclusion owns most of the page; rails carry context and scope.
- **Visual-first:** a large prepared visual establishes the phenomenon; native HTML carries exact
  labels and evidence.

Density is not permission to shrink every element. Edit source material, column allocation, and
visual proportions before reducing typography.

### C.4 Visual language

Choose one coherent system:

- strict Swiss grid with one oversized plane and deliberate negative space;
- quiet editorial rules and serif/sans contrast;
- light scientific cards with a restrained semantic palette;
- dark operational panels with stable status colors;
- limited-color screen-print or zine treatment with native text over decorative texture.

Use a few large page-scale moves rather than many unrelated badges, shadows, and small cards. Keep
the primary result visually stronger than background, method, and acknowledgments.

## Step D: Figure handling

1. Inventory source figures and the project asset directory.
2. Keep required and argument-supporting visuals; record intentional exclusions.
3. Verify effective resolution at the actual placed print size.
4. Preserve aspect ratio, units, legends, error bars, and captions.
5. Prefer source SVG for diagrams and plots when the browser/PDF route renders it correctly.
6. Re-export or redraw blurry visuals instead of enlarging them to fill space.
7. Provide meaningful `alt` text for substantive images.

### Exact information versus decorative SVG

Keep exact and editable information as HTML text, CSS layout, accessible tables, or native inline
SVG labels:

- titles, authors, affiliations, citations, and contact information;
- values, units, axes, legends, table cells, and annotations;
- claim boundaries, limitations, and stop rules.

Decorative inline SVG is appropriate for a background waveform, abstract map texture, halftone
field, topographic lines, or non-semantic visual signature. Mark purely decorative SVG as hidden
from assistive technology:

```html
<svg class="poster-visual-signature"
     viewBox="0 0 1200 500"
     role="presentation"
     aria-hidden="true">
  <rect width="1200" height="500" fill="#102f36"></rect>
  <path d="M0 270 C160 40 320 470 480 220 S820 30 1200 250"
        fill="none" stroke="#f2c14e" stroke-width="34"></path>
</svg>
```

Do not convert a chart, table, or paragraph into a decorative SVG to make placement easier. If SVG
contains substantive data geometry, keep its labels and description accessible and validate it in
both browser and exported routes.

## Step E: HTML/CSS authoring

### E.1 Template-content separation

| File | Owns | Must not own |
|---|---|---|
| `template.css` | Canvas tokens, palette, typography, reusable columns, sections, tables, results, footer, visual utilities | Research prose and data values |
| `content.html` | Poster content, semantic section order, figures, tables, and documented one-off geometry | Duplicated theme dictionaries or scripts |
| `index-template.html` | Document shell, CSS link, viewport and export plumbing | Poster-specific content or repeated theme rules |

### E.2 Reusable CSS foundation

Scale these values for the confirmed canvas and viewing distance. The numbers below are one A0-like
starting point, not immutable minimums.

```css
:root {
  --poster-page-width: 3364px;
  --poster-page-height: 4756px;
  --poster-margin: 132px;
  --poster-gap: 42px;
  --poster-section-gap: 30px;
  --poster-inset: 38px;
  --poster-title-size: 94px;
  --poster-heading-size: 52px;
  --poster-body-size: 34px;
  --poster-caption-size: 26px;
  --poster-ink: #173139;
  --poster-paper: #f7f4ed;
  --poster-primary: #225e5a;
  --poster-accent: #d56a4c;
  --poster-rule: #cdd7d4;
}

* { box-sizing: border-box; }

.poster-page {
  width: var(--poster-page-width);
  height: var(--poster-page-height);
  padding: var(--poster-margin);
  display: flex;
  flex-direction: column;
  gap: var(--poster-gap);
  color: var(--poster-ink);
  background: var(--poster-paper);
  font-size: var(--poster-body-size);
}

.poster-header,
.poster-footer {
  flex: 0 0 auto;
}

.poster-body {
  min-height: 0;
  flex: 1 1 auto;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--poster-gap);
}

.poster-column {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--poster-section-gap);
}

.poster-section {
  padding: var(--poster-inset);
  border-top: 5px solid var(--poster-primary);
  background: #ffffff;
}

.poster-section h2 {
  margin: 0 0 0.45em;
  font-size: var(--poster-heading-size);
  line-height: 1.05;
}

.poster-section p,
.poster-section li {
  line-height: 1.35;
}

.poster-footer {
  padding: 24px 32px;
  color: #ffffff;
  background: var(--poster-primary);
}
```

Do not add `overflow:hidden` to conceal layout defects. Use the DOM audit and visual review to find
the overflowing node and fix it.

### E.3 Semantic page skeleton

```html
<section class="slide poster-page" aria-labelledby="poster-title">
  <header class="poster-header">
    <p class="poster-kicker">Illustrative study contract or venue</p>
    <h1 id="poster-title">A Claim-Level Poster Title</h1>
    <p class="poster-authors">Authors · affiliations</p>
  </header>

  <main class="poster-body">
    <div class="poster-column">
      <section class="poster-section">
        <h2>Question and measurement contract</h2>
        <p>Source-supported context and method.</p>
      </section>
      <section class="poster-section poster-section--figure">
        <h2>Defining evidence</h2>
        <img src="assets/result.svg" alt="Description of the result and comparison">
        <p class="poster-caption">Caption with units, sample, and qualifier.</p>
      </section>
    </div>

    <div class="poster-column">
      <section class="poster-section poster-section--result">
        <h2>The result</h2>
        <p class="poster-result-number">2.6 °C lower</p>
        <p>Bounded interpretation.</p>
      </section>
      <section class="poster-section">
        <h2>What this does not establish</h2>
        <p>Limitations and unsupported inference.</p>
      </section>
    </div>
  </main>

  <footer class="poster-footer">
    Contact · source · acknowledgment · verified QR destination
  </footer>
</section>
```

Generic academic headings are acceptable, but job- or claim-based headings often scan better:
“The peak followed cars, not the bell,” “Evidence that could change the decision,” and “What the
pilot supports.” Use them only when the source supports the wording.

### E.4 Composition patterns

#### Conventional columns

Use CSS grid for page-level column ratios and flex inside each column. Allow content to determine
individual section heights.

```css
.poster-body--three-column {
  grid-template-columns: 1fr 1.05fr 1fr;
}

.poster-body--result-heavy {
  grid-template-columns: 0.8fr 1.2fr;
}
```

#### Optional meaningful stretch

Use `flex:1` only when a substantive final region should own the remaining column height:

```css
.poster-section--height-owner {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
}
```

Do not apply this class to acknowledgments or references simply to make two columns equal.

#### Result billboard

```css
.poster-page--billboard .poster-body {
  grid-template-columns: 0.8fr 1.9fr 0.65fr;
}

.poster-focus {
  min-height: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 72px;
  color: #ffffff;
  background: #43375d;
}

.poster-focus .poster-result-number {
  margin: 0;
  font-size: 180px;
  line-height: 0.95;
  font-weight: 800;
}

.poster-rail--interpretation {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
```

The upper quiet space in the interpretation rail is valid because the full-height focus plane
frames it. Do not fill it with low-value method prose.

#### Visual-first field

```css
.poster-hero {
  display: grid;
  grid-template-columns: 1.5fr 0.8fr;
  gap: var(--poster-gap);
  min-height: 0;
}

.poster-visual-signature {
  width: 100%;
  height: 100%;
  min-height: 720px;
}
```

Keep exact labels and interpretation outside the decorative visual or in accessible SVG text.

### E.5 Result, table, and figure patterns

#### Result callout

```html
<div class="poster-result-callout">
  <strong class="poster-result-number">84%</strong>
  <span>correct interpretation within 45 seconds</span>
</div>
```

#### Three-line table

```css
.poster-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92em;
}

.poster-table thead tr {
  border-top: 3px solid currentColor;
  border-bottom: 1.5px solid currentColor;
}

.poster-table tbody tr:last-child {
  border-bottom: 3px solid currentColor;
}

.poster-table th,
.poster-table td {
  padding: 0.42em 0.55em;
  text-align: left;
  vertical-align: top;
}
```

Padding must remain readable at the final canvas; it does not need one universal `em` minimum for
all posters. Reduce rows or columns before making a dense table illegible.

#### Figure

```css
.poster-figure {
  margin: 0;
}

.poster-figure img,
.poster-figure svg {
  display: block;
  width: 100%;
  height: auto;
}

.poster-caption {
  margin: 0.45em 0 0;
  font-size: var(--poster-caption-size);
  color: #5c696b;
}
```

### E.6 Typography and color

The correct body size depends on canvas pixels, physical page size, and viewing distance. A fixed
`33px` rule cannot govern every A0, A1, custom, or billboard poster. Begin with the canvas preset,
render at physical scale, and conduct a distance test.

- Use a small number of clearly separated type roles.
- Avoid justification in narrow columns when it creates rivers or distorted spacing.
- Verify loaded web/local fonts and the browser/PDF fallback actually used.
- Use one dominant field color, a supporting neutral, and one or two semantic accents.
- Do not use color alone to encode status or series identity.
- Keep contrast sufficient in both browser and exported SVG/PDF routes.

## Full-canvas composition without forced equal columns

### The actual rule

The whole page must look complete. It needs a deliberate lower-edge resolution and cannot contain
an accidental void that reads as missing content. Valid resolutions include:

- a full-width footer or decision band;
- aligned final evidence or conclusion regions;
- a background, image, or color plane continuing to the edge;
- a stable baseline or closing rule;
- a clearly framed quiet zone within an asymmetric billboard composition.

The following are not universal requirements:

- both columns ending at the same internal y-coordinate;
- the last section in every column using `flex:1`;
- all cards sharing one height;
- filling whitespace with references, logos, icons, or repeated prose;
- increasing padding until the page appears full.

### Recomposition sequence

When the page feels unfinished:

1. Confirm that evidence, limitations, citations, contact details, and required assets are present.
2. Increase the useful area of the primary result or figure.
3. Move complete semantic sections between columns.
4. Change column ratios, count, or page orientation.
5. Merge related short sections or split an overlong section at a semantic boundary.
6. Let one meaningful final region own remaining height when appropriate.
7. Add or strengthen a footer, decision band, closing rule, or continuing visual field.
8. Adjust gaps and insets modestly.
9. Reduce type only after the structure is sound and the distance test still passes.

If filler is still necessary, select a different composition route.

### CSS closure patterns

Use a footer to close conventional columns:

```css
.poster-page {
  display: flex;
  flex-direction: column;
}

.poster-body { flex: 1 1 auto; }
.poster-footer { flex: 0 0 auto; }
```

Use a full-height field to close an asymmetric page:

```css
.poster-focus {
  align-self: stretch;
  min-height: 100%;
}
```

Use `margin-top:auto` only when the lower-aligned element is semantically intended to sit at the
bottom, such as an interpretation rail or contact block:

```css
.poster-rail__closing-note { margin-top: auto; }
```

Do not hide residual whitespace with a transparent, empty, or background-colored element.

## Step F: Compile and review

### F.1 Source gate and synchronized build

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py PROJECT --source-only --profile scenario --entry content.html
python3 ${SKILL_DIR}/scripts/html_compiler.py PROJECT --all --entry content.html
```

When PPTX is requested:

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py PROJECT --all --include-pptx --entry content.html
```

Do not run `assemble.py` separately and do not treat direct `svg_to_pptx.py` conversion as a
delivery build. The synchronized compiler owns root `index.html`, `output/svgs/`,
`output/pngs/`, `output/browser_pngs/`, `output/overview.png`, `output/slides.pdf`, and current
receipts.

### F.2 Exactly one page

`output/svgs/` must contain only `slide_01.svg`. `slide_02.svg`, even if blank or footer-only, is a
P0 failure. Fix the overflowing source rather than deleting the second artifact.

Typical causes:

- a fixed-height page plus margins, gaps, and content whose total height exceeds the canvas;
- a late footer outside the main page flex container;
- an image or table with an unbounded intrinsic size;
- a missing `min-height:0` on a flex/grid child;
- font fallback changing line breaks;
- absolute positioning calculated from the wrong canvas.

### F.3 Browser-first visual review

Inspect `output/overview.png` and `output/browser_pngs/slide_01.png` first. The browser PNG and DOM
audit are layout truth. Use `output/pngs/slide_01.png` and render-fidelity receipts to diagnose
SVG-route differences.

At full size, verify:

- no clipping, collision, off-canvas element, hidden overflow, or footer obstruction;
- readable body text, captions, references, tables, and figure labels;
- sharp figures at their actual placed dimensions;
- correct values, units, labels, uncertainty, citations, links, and QR destinations;
- clear title/result/body hierarchy and logical reading order;
- deliberate lower-edge closure;
- reviewed fonts and matching browser/PDF line breaks.

At thumbnail or overview size, verify:

- the primary result or question is immediately visible;
- title, evidence, and decision form a coherent visual path;
- the page is not a uniform wall of equal-weight cards;
- no region appears abandoned;
- negative space reads as intentionally framed;
- the footer or continuing field visibly closes the composition.

After fixes, rerun the source gate, synchronized build, and browser-first review.

### F.4 Final artifact gate

For visual delivery:

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py PROJECT --require-build --profile scenario --artifact-profile visual --entry content.html
```

For PPTX delivery, build with `--all --include-pptx`, then validate with the `delivery` artifact
profile and the same entry.

## Quality gates

### P0: blocker

- More or fewer than one compiled page.
- Any clipped, overlapping, hidden-overflow, off-canvas, or footer-obscured content.
- Invented or mislabeled claim, value, citation, author, affiliation, logo, or link.
- Missing primary result, limitation, required figure, required logo, or contact route.
- Unreadable text or evidence at the intended viewing distance.
- Broken image, missing glyph, or unreviewed font reflow.
- Accidental bottom void or stranded region that makes the page look unfinished.

### P1: review required

- Primary result is not distinguishable at overview size.
- Equal-weight boxes obscure the reading path.
- Units, uncertainty, legend, or caption are separated from the figure.
- Color is the only carrier of meaning.
- A stretched final region contains little real content.
- Negative space lacks a page-scale field, grid, baseline, or compositional purpose.
- Browser and SVG/PDF routes differ materially.
- A substantive chart or table has been baked into inaccessible decorative SVG.

### P2: refinement

- Replace generic headings with source-supported job- or claim-level headings.
- Align repeated rules, insets, baselines, and caption spacing.
- Reduce decorative color variety and strengthen semantic accent consistency.
- Simplify tables to decision-relevant rows and columns.
- Replace fragile collections of absolutely positioned decorative shapes with one maintainable,
  non-semantic SVG visual field where appropriate.

## Common failures

| Failure | Likely cause | Correct response |
|---|---|---|
| Second SVG page | Flow height exceeds the fixed canvas | Find the overflowing node; edit content/geometry instead of deleting the page |
| Equal columns still look padded | `flex:1` was applied mechanically | Remove empty stretch and use a meaningful footer, field, or asymmetric rail |
| One column appears abandoned | Weak allocation or no framing field | Restore evidence, move a section, enlarge a real figure, change ratios, or frame the quiet zone |
| Text wraps differently in PDF | Font load or fallback differs | Resolve fonts and rebuild all routes before retuning layout |
| Chart is unreadable | Source figure is too dense or too small | Re-export, simplify, redraw natively, or give it more page area |
| Browser looks right but SVG differs | Unsupported CSS or asset behavior | Inspect the SVG-route render and fidelity receipt; simplify the incompatible treatment |
| Visual-first poster is inaccessible | Facts were placed in decorative SVG | Restore native HTML/SVG text and descriptions; keep decoration non-semantic |
| Page is full but illegible | Density was solved by shrinking type | Remove secondary material or choose another canvas/composition |

## Quick and YOLO Mode defaults

When no design preferences are provided:

- obey the venue canvas; otherwise begin with an A1-like portrait ratio;
- use a two-column evidence-led route unless one clear result earns a billboard layout;
- use a restrained light field, dark title/result color, and one semantic accent;
- organize content as question → measurement contract → primary evidence → interpretation →
  limitation → decision/contact;
- keep exact content native and use decorative SVG only for non-semantic visual fields;
- close the canvas with a meaningful footer, result region, rule, or continuing visual field;
- compile to exactly one page and inspect both browser full-size and overview renders before
  delivery.
