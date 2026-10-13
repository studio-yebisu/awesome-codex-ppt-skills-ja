# Scenario: CV and Resume (HTML/CSS)

Use this scenario only when the user explicitly requests HTML/CSS, an existing browser-based CV
must be maintained, or CSS-specific styling is a delivery requirement. Prefer the Typst CV
scenario for an ordinary print-first résumé or a long academic CV: Typst provides native physical
pagination and a simpler print-document model.

For this route, semantic HTML and reusable CSS are the editable source of truth. Do not introduce a
YAML, TOML, JSON, or form-generator layer as the required editing interface.

## Contents

1. [Scenario contract](#scenario-contract)
2. [Choose the route](#choose-the-route)
3. [Run the workflow](#run-the-workflow)
4. [Build the content system](#build-the-content-system)
5. [Define physical pages and pagination](#define-physical-pages-and-pagination)
6. [Implement a complete HTML CV](#implement-a-complete-html-cv)
7. [Handle variants, links, icons, and photos](#handle-variants-links-icons-and-photos)
8. [Build, inspect, and correct](#build-inspect-and-correct)
9. [Quick Mode defaults](#quick-mode-defaults)
10. [Non-negotiables](#non-negotiables)

## Scenario contract

- Treat the CV as a print document rendered through a fixed-page HTML pipeline, not as a slide
  presentation.
- Keep facts and narrative content in semantic HTML. Keep canvas rules, tokens, and reusable
  components in template.css.
- Use one physical paper size per build. Create separate builds for A4 and US Letter.
- Paginate deliberately with one section.slide.cv-page element per output page. Do not expect
  browser auto-pagination to flow content between slide containers.
- Keep every page in settled, static DOM state. Do not depend on scrolling, hover, animation,
  timers, remote APIs, or interaction to reveal content.
- Use real text, real anchors, and a logical DOM order. Do not render body copy as an image.
- Never add invisible keywords, white-on-white text, hidden prompt injection, or content intended
  to manipulate an ATS, recruiter, or reviewer.
- Never invent dates, titles, degrees, metrics, publications, affiliations, skills, awards, or
  credentials.
- Keep fonts, images, and icons local and deterministic.
- Compile, visually inspect, and text-extract the PDF before delivery.

Use the scenario validation profile. Do not evaluate a CV with slide-specific title-count,
speaker-note, or presentation-density heuristics.

## Choose the route

### Prefer Typst when HTML is not intentional

Use the Typst CV workflow when:

- the user has no implementation preference;
- the document needs natural multi-page pagination;
- the document is a long academic CV;
- exact print behavior is more important than CSS styling;
- browser PDF text extraction is unreliable;
- a local HTML/browser toolchain would add unnecessary dependencies.

When routing to Typst, start from the reviewed CV catalogue under
`skills/seaslides-typst-slides-skill/templates/scenarios/cv/`: use a conservative single-column
example for normal screening, a
two-column example only when its extraction order is acceptable, and an academic package for a
cumulative record. Do not translate a mature Universe template into a parallel CSS theme merely
to reproduce its appearance.

Use this HTML route when:

- HTML/CSS is explicitly requested;
- an existing HTML CV project must be preserved;
- a design depends on CSS Grid, browser preview, or CSS-specific art direction;
- manual page composition is acceptable;
- the user needs both a fixed PDF and an inspectable browser artifact.

PDF is the primary artifact. Do not offer PPTX by default for a CV.

### Distinguish document types

| Document | Typical emphasis | Length rule | HTML suitability |
|---|---|---|---|
| Professional résumé | Relevant experience and measurable evidence | Usually one or two pages | Good with manual pages |
| Student résumé | Education, projects, internships, skills | Often one page | Good |
| Academic CV | Publications, teaching, grants, service, appointments | Content-driven | Prefer Typst |
| Research-industry CV | Research plus production evidence | One to three pages as allowed | Acceptable with careful mapping |
| Creative CV | Portfolio evidence and visual identity | Audience-dependent | Good when CSS is intentional |

Application instructions override every default.

## Run the workflow

### 1. Preserve and convert source material

Accept an existing PDF, DOCX, Markdown file, portfolio, publication list, job description, or
structured notes. Keep the original files under sources/. Convert them only to create working text;
do not overwrite the originals.

```bash
python3 ${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py sources/cv.pdf -o sources/cv-extracted.md
python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py sources/cv.docx -o sources/cv-extracted.md
```

Treat extracted text as unverified. Multi-column PDFs often scramble entry order and detach dates
from their titles.

### 2. Build a fact inventory

Record:

| Field | Required record | Verification |
|---|---|---|
| Identity | Exact name and preferred display form | User or authoritative source |
| Contact | Approved email, phone, location, portfolio, profiles | Test every anchor |
| Target | Role, program, grant, award, or academic purpose | Request or application brief |
| Experience | Employer, title, location, dates, evidence | Reconcile conflicts |
| Education | Institution, degree, field, dates, distinctions | Preserve official names |
| Projects/research | Role, method, output, impact, links | Separate individual/team claims |
| Skills | Truthful and supportable abilities | Remove unsupported proficiency |
| Publications | Author order, title, venue, year, DOI/URL | Compare with canonical record |

Mark consequential facts as verified, user-confirmed, ambiguous, or missing. Never silently choose
between conflicting dates or titles.

### 3. Resolve only decisions that change the document

Bundle missing blockers into one question:

- target role or application purpose;
- locale and paper size;
- language and spelling convention;
- application page limit;
- conservative, balanced, or expressive direction;
- whether a photo is explicitly required or desired;
- which private contact details may be published.

In Quick Mode, use the defaults below and state the assumptions in the handoff.

### 4. Map target requirements to evidence

Extract repeated responsibilities, domain vocabulary, and evaluation criteria from the target.
Map each important requirement to source-backed evidence. Tailoring may change emphasis, order, and
wording; it may not copy unsupported requirements into the CV.

| Target requirement | Existing evidence | Planned location | Action |
|---|---|---|---|
| Production ownership | Ranking-service rollout | Experience entry 1 | Lead bullet |
| Evaluation rigor | Benchmark and release criteria | Project + experience | Remove repetition |
| Leadership | Four product teams | Experience entry 1 | State exact scope |

### 5. Plan sections and manual pages

Choose section order from the target and strongest evidence:

- experience-first for an experienced professional;
- education-first for a student when education is strongest;
- project-first when projects provide the clearest proof;
- academic sections only when appropriate to the document;
- no empty, weak, irrelevant, or unapproved private sections.

Create a page map before writing fine CSS:

| Page | Sections | Intended break | Density risk | DOM-order check |
|---|---|---|---|---|
| 1 | Header, summary, experience | After complete entry | Long header | One top-to-bottom flow |
| 2 | Projects, education, skills | After complete section | Dense skill list | Dates follow titles |

Do not split one entry across two slide elements. Repeat a short continuation label on page two
instead of relying on browser flow.

### 6. Implement, compile early, and revise

Build once after the header, one representative entry, one long bullet, one link, and one CJK line
are present. This exposes missing fonts, incorrect date columns, and overflow early. After all
content is present, perform at least one full revise-and-rebuild pass.

## Build the content system

### Write evidence-led bullets

Connect action, scope, method, and result. Include a metric only when it exists in the source and
its meaning is clear.

```text
Reduced model-serving latency 31% by batching feature retrieval and profiling the hot path.
```

Avoid:

```text
Responsible for AI systems and helped improve performance significantly.
```

Use this drafting sequence:

1. State the action and owned object.
2. Add scope or audience.
3. Add a distinguishing method.
4. Add an outcome or artifact.
5. Add a verified metric when available.

Do not force every bullet into one formula. Research, leadership, design, teaching, and operations
evidence have different useful shapes.

### Normalize carefully

Normalize date formats, dash style, tense, punctuation, institution naming, degree naming,
technology capitalization, locations, URLs, and publication styling. Do not erase factual
distinctions: intern, contractor, assistant, and employee are not interchangeable; submitted,
accepted, and published are not interchangeable.

### Keep headings conventional when scanning matters

Prefer headings such as Experience, Education, Projects, Skills, Publications, Teaching, Awards,
and Service. Creative labels may be appropriate for a portfolio, but reduce scanning clarity in a
conservative hiring flow.

### Correct content before shrinking

When a page overflows:

1. remove duplicated summary claims;
2. remove weak or irrelevant bullets;
3. shorten repeated context and long link labels;
4. merge closely related bullets;
5. move a complete low-priority entry or section to page two;
6. tighten local spacing slightly;
7. reduce type by a small step only at the end.

Do not clip content, scale the full page, or push body text below approximately 12 CSS px.

### Protect privacy and integrity

- Publish only approved contact details.
- Do not expose source notes, prompts, comments, or internal annotations.
- Do not add a headshot by default.
- Do not create fake logos, certifications, testimonials, publications, or employer marks.
- Do not add hidden keywords or invisible text.
- Remove unintended names or local paths from document metadata.

## Define physical pages and pagination

### Use 96-CSS-pixel physical canvases

Chromium maps CSS pixels at 96 px per inch. Use:

| Paper | CSS canvas | Physical page |
|---|---:|---:|
| A4 | 794 × 1123 px | Approximately 210 × 297 mm |
| US Letter | 816 × 1056 px | 8.5 × 11 in |

The HTML skill's a4 raster preset is 1240 × 1754 and is useful for image-oriented output, but it is
not the physical A4 canvas for this PDF route. For a print CV, declare the canvas above and pass the
same dimensions to the compiler.

Start near 57–76 CSS px side margins for A4 and 62–77 CSS px for Letter. Verify the resulting PDF
page box; do not rely on the preset name alone.

### Use one page element per output page

```html
<section
  class="slide cv-page light"
  data-notes="Print résumé page 1"
  aria-label="Résumé page 1"
>
  <!-- One complete physical page -->
</section>
```

The compiler captures each slide element independently. CSS break-inside may keep an entry
together inside one page, but it cannot move overflow into a new slide. Add a second slide in the
source and allocate content deliberately.

### Preserve logical DOM order

Keep DOM order identical to intended reading order. Use CSS Grid only for alignment; do not use the
order property to create a visual order that differs from extraction order. Keep:

1. name and headline;
2. contact labels;
3. section heading;
4. title and dates;
5. organization and location;
6. evidence.

Absolute positioning is acceptable for a page number or non-essential ornament. Do not absolutely
position résumé paragraphs, entry titles, or dates unless text extraction has been verified.

## Implement a complete HTML CV

Use this project shape:

```text
project/
├── index-template.html
├── content.html
├── template.css
├── assets/
├── sources/
└── output/
```

The following implementation is complete and uses no remote assets. It provides the page canvas,
header, summary, section, entry, skills, publication, photo, continuation, and page-number rules.

### index-template.html

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1"
  >
  <title>{{TITLE}}</title>
  <link rel="stylesheet" href="template.css">
</head>
<body class="cv-document">
  <main id="deck">{{CONTENT}}</main>
</body>
</html>
```

Do not add remote font, icon, analytics, or application scripts to this shell. The CV must settle
immediately and build offline.

### template.css

```css
:root {
  --slide-width: 794px;
  --slide-height: 1123px;
  --page-x: 60px;
  --page-y: 56px;
  --ink: #17212b;
  --muted: #5b6670;
  --accent: #1f4e79;
  --paper: #ffffff;
  --rule: #b9c4cc;
  --body-size: 14px;
  --body-leading: 1.32;
  --font-sans:
    "IBM Plex Sans",
    "Noto Sans SC",
    Arial,
    sans-serif;
}

* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
  background: #dfe3e6;
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: var(--body-size);
  line-height: var(--body-leading);
  text-rendering: geometricPrecision;
}

#deck {
  display: grid;
  gap: 24px;
  justify-content: center;
}

.slide.cv-page {
  position: relative;
  width: var(--slide-width);
  height: var(--slide-height);
  padding: var(--page-y) var(--page-x);
  overflow: hidden;
  background: var(--paper);
}

.cv-page :where(h1, h2, h3, p, ul, ol, dl, dd) {
  margin: 0;
}

.cv-page a {
  color: var(--accent);
  text-decoration-line: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
}

.cv-header {
  padding-bottom: 10px;
  border-bottom: 2px solid var(--accent);
}

.cv-header.has-photo {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 96px;
  gap: 24px;
  align-items: center;
}

.cv-identity h1 {
  font-size: 36px;
  line-height: 1.02;
  letter-spacing: -0.025em;
}

.cv-headline {
  margin-top: 5px !important;
  color: var(--muted);
  font-size: 16px;
  font-weight: 600;
}

.cv-contact {
  display: flex;
  flex-wrap: wrap;
  gap: 3px 16px;
  margin-top: 7px;
  color: var(--muted);
  font-size: 12.5px;
  font-style: normal;
}

.cv-photo {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  object-fit: cover;
}

.cv-summary {
  margin-top: 12px !important;
  padding-left: 11px;
  border-left: 2px solid var(--accent);
}

.cv-section {
  margin-top: 15px;
}

.cv-section > h2 {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 10px;
  align-items: center;
  font-size: 16px;
  line-height: 1.1;
  letter-spacing: 0.045em;
}

.cv-section > h2::after {
  display: block;
  height: 1px;
  background: var(--accent);
  content: "";
}

.cv-entry {
  margin-top: 8px;
  break-inside: avoid;
}

.cv-entry-header,
.cv-entry-subhead,
.cv-publication-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) max-content;
  gap: 16px;
  align-items: baseline;
}

.cv-entry h3,
.cv-publication h3 {
  font-size: 14.5px;
  line-height: 1.2;
}

.cv-entry time,
.cv-date,
.cv-publication time {
  font-weight: 600;
  white-space: nowrap;
}

.cv-entry-subhead,
.cv-publication-meta {
  margin-top: 1px;
  color: var(--muted);
  font-size: 12.5px;
}

.cv-entry ul {
  margin-top: 3px;
  padding-left: 20px;
}

.cv-entry li + li {
  margin-top: 2px;
}

.cv-skill-list {
  display: grid;
  grid-template-columns: 124px minmax(0, 1fr);
  gap: 4px 12px;
  margin-top: 8px !important;
}

.cv-skill-list dt {
  font-weight: 700;
}

.cv-skill-list dd {
  min-width: 0;
}

.cv-publication {
  margin-top: 8px;
}

.cv-page-number {
  position: absolute;
  right: var(--page-x);
  bottom: 26px;
  color: var(--muted);
  font-size: 11px;
}

.cv-continuation {
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--rule);
  color: var(--muted);
  font-size: 12px;
}

@media print {
  html,
  body {
    background: var(--paper);
  }

  #deck {
    gap: 0;
  }
}
```

Keep project-level component additions in template.css. Do not put a style block or arbitrary
inline style declarations in content.html.

### content.html

```html
<section
  class="slide cv-page light"
  data-notes="Print résumé page 1"
  aria-label="Résumé page 1"
>
  <header class="cv-header">
    <div class="cv-identity">
      <h1>Jane Smith</h1>
      <p class="cv-headline">
        Machine Learning Engineer
      </p>
      <address class="cv-contact">
        <a href="mailto:jane@example.com">
          jane@example.com
        </a>
        <a href="https://example.com">
          example.com
        </a>
        <span>Shanghai</span>
      </address>
    </div>
  </header>

  <p class="cv-summary">
    Builds reliable retrieval and serving systems for
    multilingual products. Strongest evidence: production
    ownership, latency reduction, and cross-functional delivery.
  </p>

  <section
    class="cv-section"
    aria-labelledby="experience-heading"
  >
    <h2 id="experience-heading">Experience</h2>

    <article class="cv-entry">
      <header class="cv-entry-header">
        <h3>Senior Machine Learning Engineer</h3>
        <time datetime="2022">2022–Present</time>
      </header>
      <div class="cv-entry-subhead">
        <span>Example Company</span>
        <span>Shanghai</span>
      </div>
      <ul>
        <li>
          Reduced retrieval latency by 31% after profiling the
          hot path and batching feature access.
        </li>
        <li>
          Led the production rollout of a multilingual ranking
          service used by four product teams.
        </li>
      </ul>
    </article>

    <article class="cv-entry">
      <header class="cv-entry-header">
        <h3>Machine Learning Engineer</h3>
        <span class="cv-date">
          <time datetime="2020">2020</time>–<time
            datetime="2022"
          >2022</time>
        </span>
      </header>
      <div class="cv-entry-subhead">
        <span>Sample Labs</span>
        <span>Remote</span>
      </div>
      <ul>
        <li>
          Built evaluation tooling that shortened weekly model
          review from two days to four hours.
        </li>
        <li>
          Partnered with product and data teams to define release
          criteria and incident playbooks.
        </li>
      </ul>
    </article>
  </section>

  <section
    class="cv-section"
    aria-labelledby="projects-heading"
  >
    <h2 id="projects-heading">Selected Projects</h2>
    <article class="cv-entry">
      <header class="cv-entry-header">
        <h3>Multilingual Retrieval Benchmark</h3>
        <time datetime="2024">2024</time>
      </header>
      <p class="cv-entry-subhead">
        Open-source project
      </p>
      <ul>
        <li>
          Designed a reproducible benchmark and documented
          dataset limits, scoring, and failure cases.
        </li>
      </ul>
    </article>
  </section>

  <section
    class="cv-section"
    aria-labelledby="education-heading"
  >
    <h2 id="education-heading">Education</h2>
    <article class="cv-entry">
      <header class="cv-entry-header">
        <h3>M.S. in Computer Science</h3>
        <span class="cv-date">
          <time datetime="2018">2018</time>–<time
            datetime="2020"
          >2020</time>
        </span>
      </header>
      <div class="cv-entry-subhead">
        <span>Example University</span>
        <span>Beijing</span>
      </div>
      <p>
        Thesis: Efficient representation learning for
        low-resource retrieval.
      </p>
    </article>
  </section>

  <section
    class="cv-section"
    aria-labelledby="skills-heading"
  >
    <h2 id="skills-heading">Skills</h2>
    <dl class="cv-skill-list">
      <dt>Languages</dt>
      <dd>Python, Rust, SQL</dd>
      <dt>ML systems</dt>
      <dd>
        PyTorch, retrieval, evaluation, model serving
      </dd>
      <dt>Languages spoken</dt>
      <dd>English, 中文</dd>
    </dl>
  </section>

  <section
    class="cv-section"
    aria-labelledby="publications-heading"
  >
    <h2 id="publications-heading">
      Selected Publication
    </h2>
    <article class="cv-publication">
      <header class="cv-publication-header">
        <h3>
          A Reproducible Evaluation Protocol for
          Multilingual Retrieval
        </h3>
        <time datetime="2024">2024</time>
      </header>
      <p class="cv-publication-meta">
        Jane Smith and A. Collaborator.
        Example Systems Workshop.
        <a href="https://doi.org/10.0000/example">
          doi:10.0000/example
        </a>
      </p>
    </article>
  </section>
</section>
```

Replace every sample fact. Do not deliver placeholders or fictional metrics.

### Add a second page explicitly

```html
<section
  class="slide cv-page light"
  data-notes="Print résumé page 2"
  aria-label="Résumé page 2"
>
  <p class="cv-continuation">
    Jane Smith · Resume continued
  </p>

  <section
    class="cv-section"
    aria-labelledby="page-2-publications"
  >
    <h2 id="page-2-publications">Publications</h2>
    <!-- Complete publication entries -->
  </section>

  <span class="cv-page-number" aria-hidden="true">2</span>
</section>
```

Use a visible continuation label when pages may be separated. Keep the page number
aria-hidden because it is navigation, not résumé content.

## Handle variants, links, icons, and photos

### Use explicit variant entries

```text
content.html              # canonical CV
content-resume-ml.html    # targeted professional version
content-letter.html       # Letter pagination
content-zh.html           # Chinese version
template.css              # shared A4 defaults
template-letter.css       # optional Letter override
```

Do not maintain contradictory copies of facts. If variants share extensive content, use a
documented build-time include mechanism already supported by the project; do not introduce an
opaque external schema solely for reuse.

For a small number of variants, explicit HTML files are easier to audit. Compare all repeated
dates, organization names, and publication metadata before delivery.

### Typography

At the A4 canvas, start near 14–15 CSS px body text with 1.25–1.4 line height. Inspect font metrics,
not only the number. Edit content, spacing, or page allocation before reducing body text below
approximately 12 px.

Use explicit local fallbacks. Verify CJK punctuation, numerals, medium/bold faces, URL wrapping, and
line breaks. Do not load Google Fonts or an icon CDN at build time.

### Links

Use semantic anchors for email, phone, portfolio, DOI, ORCID, and profile URLs. Show readable
labels. Test the final PDF links; a working browser anchor does not guarantee a preserved PDF
annotation.

```html
<a href="mailto:jane@example.com">jane@example.com</a>
<a href="https://orcid.org/0000-0000-0000-0000">
  ORCID 0000-0000-0000-0000
</a>
```

Avoid raw tracking links and icon-only contact controls.

### Icons

Text labels or separators are the default. If icons improve scanning:

- use a local inline SVG or local SVG file;
- pair it with readable text;
- mark a redundant decorative icon aria-hidden;
- verify it in the PDF;
- keep a text-only fallback.

Do not depend on emoji, an icon font, or Font Awesome merely for basic contact details.

### Photos

Do not include a headshot by default. Add one only when requested or explicitly expected. Use a
local image and meaningful alt text in the source.

```html
<header class="cv-header has-photo">
  <div class="cv-identity">
    <!-- Name, headline, and contact information -->
  </div>
  <img
    class="cv-photo"
    src="assets/photo.jpg"
    alt="Portrait of Jane Smith"
  >
</header>
```

Confirm consent, inspect the crop, and verify that removing the image also removes the has-photo
class so the header does not retain an empty column.

### Multilingual variants

Use explicit language entry files such as content-en.html and content-zh.html. Share tokens and
components, but allow language-specific line breaks, section names, date widths, and type settings.
A literal translation does not have the same geometry.

Set the document lang attribute correctly for each build. Verify:

- glyph coverage;
- CJK bold and medium weights;
- punctuation and Latin/CJK spacing;
- translated institution and degree names;
- link wrapping;
- extracted text order.

## Build, inspect, and correct

### Run the source gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project> --source-only --profile scenario
```

Resolve missing shell, forbidden inline behavior, remote dependency, and source-structure errors
before rendering.

### Compile with the physical canvas

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project> --all --ppi 2 --width 794 --height 1123 --entry content.html
```

For US Letter, synchronize the CSS variables and command:

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project> --all --ppi 2 --width 816 --height 1056 --entry content-letter.html
```

Do not use --include-pptx unless editable PowerPoint is explicitly requested.

### Run the artifact gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project> --require-build --profile scenario --artifact-profile visual
```

Inspect output/dom-audit.json and output/render-fidelity.json. Zero blockers is required; review
items must be understood and resolved or documented.

### Inspect visually

Use output/browser_pngs/ as the browser truth, then compare output/pngs/ if necessary. Inspect:

- the overview;
- every page at full size;
- the PDF at 100%;
- a typical laptop width;
- grayscale or a physical print when practical.

Check:

- correct paper size, orientation, margins, and page count;
- no overflow, clipping, collision, accidental blank page, or stranded heading;
- stable date and location alignment;
- readable body text and deliberate density;
- no large hole caused by an entry kept together unnecessarily;
- no late font or image shift;
- complete glyph rendering;
- natural photo crop and consent when present.

### Inspect the PDF as a document

When available:

```bash
pdfinfo <project>/output/slides.pdf
pdffonts <project>/output/slides.pdf
pdftotext <project>/output/slides.pdf <project>/output/cv-extracted.txt
```

Verify:

- A4 near 595 × 842 PDF points or Letter at 612 × 792 points;
- embedded or reproducibly available fonts;
- name, headings, dates, bullets, and publications in logical order;
- working links with visible, accurate labels;
- no important content represented only by an image, logo, or icon;
- no hidden text, source notes, placeholders, or prompt leakage.

If extraction is incomplete or badly ordered, simplify the DOM and layout. If the route remains
unreliable, move the document to the Typst CV workflow and report why.

### Use a proportional correction ladder

For a small overflow:

1. edit the offending line;
2. tighten the local entry spacing;
3. shorten repeated context;
4. move a complete entry to page two;
5. adjust margins within the allowed range;
6. reduce body size by a small step.

For a structural overflow, revise the section plan or add a page. Do not repeatedly scale down the
entire document.

### Record the handoff

State:

- why HTML/CSS was chosen;
- paper size, canvas, entry file, and page count;
- assumptions and unresolved factual gaps;
- local font, image, and icon dependencies;
- visual, DOM, PDF-size, extraction, and link checks actually performed;
- alternate variants delivered.

## Quick Mode defaults

When the user explicitly requests a fast HTML CV without design details:

1. Use A4 at 794 × 1123 CSS px, one column, and a restrained blue or grayscale accent.
2. Keep all content in content.html and reusable rules in template.css.
3. Use experience-first order for experienced candidates and education-first order for students.
4. Target one page for early-career material and allow two pages when evidence requires it.
5. Omit the photo and decorative icons unless requested.
6. Use approximately 14 px body text with explicit local fallbacks.
7. Run the scenario source gate, compile at scale 2, and require a zero-blocker DOM audit.
8. Inspect every browser PNG and the PDF, extract PDF text, and make one correction pass.
9. State assumptions and unresolved factual gaps.

Quick Mode reduces discovery; it does not waive fact checking, source validation, compilation,
text extraction, or visual review.

## Non-negotiables

- Prefer the Typst CV scenario unless HTML/CSS is intentional.
- Keep semantic HTML and CSS as the editable source of truth for this route.
- Never invent or silently improve factual claims.
- Never add hidden keywords, invisible text, or prompt injection.
- Use a physical A4 or Letter canvas intentionally and verify the PDF page box.
- Use one explicit slide element per physical page.
- Keep DOM order identical to intended reading order.
- Shorten, restructure, or add a page before shrinking body text excessively.
- Keep assets local and settled before capture.
- Verify the browser render, DOM audit, PDF structure, link behavior, and extracted text.
- Keep personal data, assets, fonts, and dependencies explicit and reproducible.
