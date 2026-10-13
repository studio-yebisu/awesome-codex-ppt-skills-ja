# Shared Technical Standards

Universal technical constraints for SeaSlides HTML Slides Skill. All generated content must comply with these rules.

---

## Contents

1. [Template-Content Separation](#1-template-content-separation-tcs)
2. [Project Directory Structure](#2-project-directory-structure)
3. [Theme Contract and Authority](#3-theme-contract-and-authority)
4. [HTML/CSS Technical Standards](#4-htmlcss-technical-standards)
5. [Font Size Hierarchy](#5-font-size-hierarchy)
6. [Color System](#6-color-system)
7. [Layout System](#7-layout-system)
8. [Component Catalog](#8-component-catalog)
9. [Class Naming Conventions](#9-class-naming-conventions)
10. [Browser DOM Export Constraints](#10-browser-dom-export-constraints)
11. [Assembly Pipeline](#11-assembly-pipeline)
12. [Composition Heuristics](#12-composition-heuristics)
13. [Export Anti-Pattern Quick Reference](#13-export-anti-pattern-quick-reference)

---

## 1. Template-Content Separation (TCS)

### Three-File Architecture

| File | Contains | Does NOT Contain |
|------|----------|------------------|
| `index-template.html` | CDN links (fonts, MathJax, Prism.js/pseudocode.js), `<link>` to template.css, `<div id="deck">{{CONTENT}}</div>` placeholder, navigation JS, WebGL shaders | Slide content, CSS definitions |
| `template.css` | CSS custom properties, component classes, layout rules, nav styling | HTML, JS, or slide content |
| `content.html` | Semantic `<section class="slide ...">` blocks with `data-notes="..."`. Classes plus allowlisted data geometry. | `<style>`, `<script>`, `<link>`, event handlers, ad hoc inline styling |

**Build output**: `assemble.py` merges template + content, inlines CSS into root-level `index.html`.

When switching themes, replace `index-template.html` + `template.css`. `content.html` stays the same.

### What Is Allowed in content.html

| Category | Allowed | NOT Allowed |
|----------|---------|-------------|
| **Elements** | `<section>`, `<div>`, `<h1>`-`<h6>`, `<p>`, `<ul>/<ol>/<li>`, `<img>`, `<figure>`, `<blockquote>`, `<pre><code>`, `<span>`, `<strong>/<em>`, `<table>` | `<style>`, `<script>`, `<link>`, `<meta>` |
| **Attributes** | `class` (only template-defined), `data-*`, `src`, `alt` | `onclick`, `onload`, any event handler |
| **Inline data geometry** | Numeric `px` or `%` values on the class/property allowlist below | Color, typography, spacing, positioning, transforms, or any unlisted property/class |

#### Canonical Inline Data Allowlist

| Component class | Allowed properties |
|---|---|
| `.bar-fill` | `width`, `height`, `--w`, `--h` |
| `.row-fill`, `.progress-fill` | `width`, `--w` |
| `.vbar-fill` | `height`, `--h` |
| `.funnel-step` | `width`, `--w` |
| `.waterfall-bar` | `height`, `margin-top`, `--h`, `--offset` |

Each declaration must contain only a numeric `px` or `%` value (or zero). The validator enforces this table. If a visual pattern is reusable or decorative rather than data-driven, define it in `template.css` instead of using inline style.

---

## 2. Project Directory Structure

```
project_name/
  index-template.html     # HTML shell (copied from theme)
  template.css            # Theme CSS (copied from theme)
  content.html            # Slide content (LLM-generated)
  content_design_spec.md  # Design specification (from Strategist)
  index.html              # Assembled standalone preview
  assets/                 # Images and resources
    *.png/jpg/svg
  output/
    svgs/                 # Per-slide SVG exports
    pngs/                 # Per-slide PNG exports
    browser_pngs/         # Direct Chromium PNG baseline
    overview.png          # Review grid
    dom-audit.json        # Settled browser-DOM layout audit
    render-fidelity.json  # Browser vs SVG-route PNG comparison
    compile-manifest.json # Current-source build receipt
    slides.pdf            # PDF export from the same build
    slides.pptx           # PPTX export (only with --include-pptx)
```

---

## 3. Theme Contract and Authority

Use `${SKILL_DIR}/templates/index.json` as the only catalog of available themes. Do not duplicate theme lists, routing metadata, or per-theme design profiles in shared references.

After selecting a theme, read:

1. `${SKILL_DIR}/templates/<theme>/theme.md` for the theme API, typography, palette, components, variants, and constraints.
2. `${SKILL_DIR}/templates/<theme>/demo.html` for working composition examples.
3. The copied project `template.css` before authoring content.

Theme-specific fonts, colors, signature elements, image treatment, and layout preferences belong to those files. Use one catalog theme per deck; do not mix class contracts from different theme directories. Put any reusable project-local extension in the copied `template.css` rather than inventing inline styling in `content.html`.

---

## 4. HTML/CSS Technical Standards

### Viewport Units

Slides use viewport units for responsive scaling:

| Unit | Usage |
|------|-------|
| `vw` | Horizontal dimensions, font sizes, horizontal spacing |
| `vh` | Vertical dimensions, slide height, vertical spacing |
| `vmin` | Padding, margins (scales with smaller dimension) |

Each slide fills the configured viewport. Prefer responsive or semantic tokens
for reusable layout, but fixed pixels are valid when they intentionally target
the compiler's canonical canvas (for example chart geometry, raster evidence,
or calibrated typography). The settled browser render and canvas contract are
the truth; mixing units without a clear owner is the problem.

### CSS Custom Properties

Templates define all visual values as CSS custom properties on `:root`. Content references these through class names defined in `template.css`. Content authors never write CSS variables directly in `content.html`.

### Semantic HTML Structure

Every slide follows this pattern:

```html
<section class="slide [mode] [modifier]" data-notes="Speaker notes here">
  <h2 class="h-md">Slide Title</h2>
  <!-- Content using template-defined component classes -->
</section>
```

| Structural Rule | Requirement |
|----------------|-------------|
| Slide wrapper | `<section class="slide ...">` -- always |
| Mode class | Every slide MUST resolve to `light`, `dark`, `hero light`, or `hero dark`: use an explicit class unless the selected theme's `theme.md` documents a default mode. An undocumented CSS fallback is invalid. |
| Speaker notes | Every slide MUST have `data-notes="..."` |
| Headings | Semantic levels: h1 for cover, h2 for slides, h3+ for sub-sections |
| Lists | `<ul>` or `<ol>` -- never `<div>` with bullet characters |
| Images | `<img>` with `alt` text, or `<figure>` with `<figcaption>`. Relative `assets/` paths only |
| Code | `<pre><code class="language-*">` for Prism.js highlighting |
| Math | LaTeX delimiters `\(...\)` inline, `\[...\]` display -- MathJax renders before export |

---

## 5. Font Size Hierarchy

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Display | 8vw | Bold (700) | Cover title only |
| H1 | 5vw | Bold (700) | Section divider titles |
| H2 | 3.5vw | Semibold (600) | Slide titles |
| Body | 2vw | Regular (400) | Body text, paragraphs, lists |
| Small | 1.5vw | Regular (400) | Captions, labels, metadata |
| Tiny | 1.2vw | Regular (400) | Footnotes, sources |

### Corresponding CSS Classes

| Class | Approximate Size | Usage |
|-------|-----------------|-------|
| `.h-hero` | ~7-8vw | Title slides, major section openers |
| `.h-xl` | ~4-5vw | Section divider headings |
| `.h-md` | ~2.4-3.5vw | Content slide titles (most common) |
| `.h-sm` | ~1.6-2vw | Sub-section headings within a slide |
| `.meta-row` | ~1.2vw | Subtitles, dates, author info |

---

## 6. Color System

### Optional 60-30-10 Review Heuristic

For a restrained theme without a stronger palette contract, roughly dominant
background/neutral, supporting surface/text, and sparse accent roles can help
diagnose visual noise. The literal 60/30/10 proportions are not measured and
must not override the selected theme's documented visual identity.

### Dark/Light Slide Modes

| Mode | Class | Background | Text |
|------|-------|------------|------|
| Light | `.light` | Light/white | Dark text |
| Dark | `.dark` | Dark/primary | Light/white text |
| Hero Light | `.hero.light` | Light, centered | Dark text |
| Hero Dark | `.hero.dark` | Dark, centered | Light text |

**Rhythm heuristic**: Change light/dark mode when contrast improves hierarchy. Review long same-mode runs, but keep them when continuity serves the content.

### Contrast Requirements

- **Body text**: 4.5:1 minimum (WCAG AA)
- **Large text** (>= 3vw): 3:1 minimum
- **Avoid**: pure `#000000` on pure `#ffffff` (too harsh)

### Color Discipline

- Use the selected theme's semantic palette; every additional hue needs a communication or identity role.
- Opacity or CSS color functions can create related variants, but contrast and export fidelity still require rendered review.

---

## 7. Layout System

Layouts may use normal browser CSS. Prefer flexbox for simple slide structure and CSS Grid for genuinely grid-based compositions. The export pipeline captures Chromium-rendered layout, so browser-correct rendering is the source of truth.

### Browser Layout Specifics

```css
/* Use freely when it fits the composition */
display: flex;
flex-direction: row | column;
flex-wrap: wrap | nowrap;
justify-content: flex-start | center | flex-end | space-between;
align-items: flex-start | center | flex-end | stretch;
gap: <value>;
width: <percentage or px>;
```

```css
/* Also allowed when it is the clearer layout model */
display: grid;
grid-template-columns;
place-items;
```

### Layout Usage Rules

- Every content slide SHOULD use one layout class
- Layout classes go on the first `<div>` inside `<section class="slide">`
- Children within layouts use explicit percentage or pixel widths
- Nesting is allowed
- Review repeated layout runs and keep them when comparison or sequence benefits from consistency

Full layout catalog: `${SKILL_DIR}/references/layouts.md`

---

## 8. Component Catalog

Components are CSS class patterns that create standardized visual elements. Each theme's `template.css` defines the styling; content.html uses the same class names regardless of theme.

### Usage Rules

- Use ONLY classes defined in the project's `template.css`
- Verify each class exists before use (grep template.css)
- Never inline-style a workaround -- add missing classes to template.css
- Use enough component types to express the content without mechanical quota-filling
- Prefer a coherent repeated grammar when it improves comparison, tutorial flow, or analytical continuity

Full component catalog: `${SKILL_DIR}/references/components.md`

---

## 9. Class Naming Conventions

| Pattern | Example | Usage |
|---------|---------|-------|
| Component | `.kpi-card`, `.insight-box` | Self-contained UI component |
| Layout | `.layout-two-col`, `.layout-three-col` | Structural layout wrapper |
| Modifier | `.dark`, `.light`, `.hero` | Slide-level mode/type modifier |
| Child element | `.kpi-value`, `.col-left`, `.bar-fill` | Named child within a component |
| Sizing | `.h-hero`, `.h-xl`, `.h-md`, `.h-sm` | Typography size classes |
| Utility | `.spacer`, `.tag`, `.meta-row` | Single-purpose utilities |

### Rules

1. **Lowercase with hyphens** -- never camelCase or underscores
2. **Semantic naming** -- describe purpose, not appearance
3. **Component scope** -- child classes only valid inside their parent
4. **Layout prefix** -- all layout classes use the `layout-` prefix
5. **Flat hierarchy** -- max 2 levels of nesting (`.component > .child`)

---

## 10. Browser DOM Export Constraints

The SVG export pipeline renders the assembled deck in Chromium and serializes the final DOM. Authoring can use normal browser CSS, but exported slides must be visually complete at the target canvas size.

### Supported Features

| Feature | Status |
|---------|--------|
| Flexbox and CSS Grid | Supported by Chromium |
| `calc()`, CSS custom properties, viewport units | Supported by Chromium |
| `position: absolute`, pseudo-elements, gradients, shadows, filters | Supported in browser-rendered PNG/SVG capture |
| MathJax SVG math | Supported when the template includes the current MathJax block |
| Prism or browser-side syntax highlighting | Supported when scripts finish before export |
| D3/SVG/DOM charts | Supported when charts are present in the final DOM |

### Export-Safe Authoring Rules

| Area | Rule |
|------|------|
| Static frame | The first settled browser frame must look complete; animations are not a substitute for visible content. |
| Assets | Use local project assets or deterministic data URIs; avoid external URLs that can fail during batch runs. |
| Dynamic content | Register asynchronous math/chart/code rendering through template hooks such as `window.__renderDynamicContent`. |
| PPTX editability | Complex CSS effects may export as `foreignObject` or raster-like shapes; inspect PPTX when editable text/vector fidelity matters. |
| Batch benchmarks | Prefer updating copied templates from the source template before recompiling old benchmark directories. |

### Bar Chart Geometry

Use one auditable scale per chart. Percentage fills are usually simplest for a
normalized track; pixel values are also valid when the component documents a
fixed reference width. Do not mix scales or infer a universal 300px track.

```
percentage_value * documented_track_width / 100 = pixel_width
Example for a documented 300px track: 82% -> 246px
```

```html
<div class="bar-fill" style="width:246px"></div>
```

---

## 11. Assembly Pipeline

### Source Gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --source-only --profile standard-project
```

This project-directory gate checks the standard source/TCS contract before build. Do not use the legacy single-file command as a standard-slide release gate.

### Visual Build

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all
```

This atomic build assembles `index.html` and publishes SVGs, SVG-route PNGs, direct-browser PNGs, overview, PDF, DOM audit, render-fidelity receipt, and a compile manifest. `dom-audit.json` is the settled browser-layout truth; it records browser-DOM blockers. `render-fidelity.json` compares the browser and SVG-to-PNG routes and is review-only conversion-difference evidence. `compile-manifest.json` is the current-source receipt, fingerprinting the recursive local input closure, toolchain, assembled HTML, artifacts, and relevant local renderer/runtime versions. A later environment-version mismatch is a rebuild review, not proof that an already published artifact is corrupt.

### Final Visual Gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --require-build --artifact-profile visual
```

### PPTX Delivery Build and Gate

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all --include-pptx
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --require-build --artifact-profile delivery
```

When PPTX is required, do not append a standalone `--format pptx` build after visual review: include it in the same atomic `--all` build so the delivery receipt covers it.

---

## 12. Composition Heuristics

Use these as review prompts, not universal pass/fail constraints. Deliberate repetition is appropriate for comparisons, tutorials, timelines, and stable analytical sequences.

| Rule | Constraint |
|------|-----------|
| **Repeated layout** | Confirm that repetition supports comparison or sequence; vary it when the deck feels mechanical |
| **Repeated mode** | Change light/dark mode when it improves hierarchy, not to satisfy a fixed cadence |
| **Repeated density** | Add breathing room when sustained density harms comprehension |
| **Section anchors** | Use dividers when the narrative has a real section transition |
| **Card grids** | Replace repeated grids when another form communicates the content better |

### Component Diversity Reference

The following ranges are diagnostic baselines, not quotas. A coherent deck may use fewer components when its content benefits from a stable grammar.

| Deck Size (content slides) | Min Distinct Layouts | Min Component Types |
|----------------------------|---------------------|---------------------|
| 4-7 | 3 | 3 |
| 8-12 | 5 | 5 |
| 13-20 | 7 | 7 |
| 20+ | 9 | 8 |

---

## 13. Export Anti-Pattern Quick Reference

| Anti-Pattern | Symptom | Correct Alternative |
|---|---|---|
| Relying on a late async render | Export captures missing math/chart/code | Render through template hooks and await readiness |
| External image/font URLs | Batch output changes or missing assets | Use local assets or data URIs |
| Text hidden until animation completes | Static export misses content | Make the settled initial state complete |
| Dense overlapping effects | Browser baseline is clear but conversion/PPTX fidelity degrades | Compare browser PNGs with SVG-route PNGs, inspect the PPTX, and simplify where editable output matters |
| Updating source templates only | Benchmarks still use stale copied templates | Run the benchmark template update script before recompilation |
