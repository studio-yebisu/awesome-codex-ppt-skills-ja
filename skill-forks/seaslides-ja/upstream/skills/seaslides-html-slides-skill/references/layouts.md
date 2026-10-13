# Layout Catalog

> All layout patterns available in SeaSlides HTML Slides templates. Layouts define the structural arrangement of content within a slide. Templates may use normal browser CSS; prefer flexbox for simple rows/columns and CSS Grid for true grid compositions.

---

## Usage Rules

1. **One layout per slide** -- apply to the first `<div>` inside `<section class="slide">`
2. **Review repeated layouts** -- retain them when they support comparison or sequence; vary accidental monotony
3. **Nesting is allowed** -- a column within a two-col layout can contain another layout
4. **Children need predictable sizing** -- use stable widths, grid tracks, or flex constraints so the rendered slide does not shift
5. **Theme-appropriate layouts** -- see Per-Theme Recommendations below
6. **Choose a vertical mode** -- centered cluster, top-to-bottom, split anchors, image hero, or intentional breathing; do not let a content layout collapse to natural height at the top

---

## Shared Layouts

These layouts are available in all themes.

---

### 1. `layout-title-body`

Standard slide with heading area + body content area stacked vertically.

```html
<section class="slide light" data-notes="...">
  <div class="layout-title-body">
    <div class="title-area"><div class="h-md">Title Here</div></div>
    <div class="body-area">
      <!-- Components go here -->
    </div>
  </div>
</section>
```

**Best for**: Default content slides. Text + single component. Lists and
descriptions. The outer layout and `.body-area` should own the remaining height
with `min-height: 0`; use semantic `gap`, grid tracks, centering, or
`space-between` according to the planned vertical mode. Do not add empty spacer
nodes to force a lower position.

---

### 2. `layout-two-col`

Two-column split. Children use `.col-left` and `.col-right`.

```html
<div class="layout-two-col">
  <div class="col-left"><!-- text, charts, lists --></div>
  <div class="col-right"><!-- image, KPI, insight-box --></div>
</div>
```

**Best for**: Text + visual pairings. Comparison layouts. Image + explanation.

**editorial-magazine**: Prefer asymmetric splits (30/70 or 40/60). Never 50/50.

**swiss-international**: Equal splits acceptable. Content should align to grid.

---

### 3. `layout-two-col-wide`

Like two-col but with wider gutters and the left column occupying ~60%.

**Best for**: Long-form text on left, supporting visual on right. Narrative slides.

---

### 4. `layout-three-col`

Three equal-width columns.

```html
<div class="layout-three-col">
  <div class="grid-item"><!-- card 1 --></div>
  <div class="grid-item"><!-- card 2 --></div>
  <div class="grid-item"><!-- card 3 --></div>
</div>
```

**Best for**: KPI card triplets. Feature comparisons. Category breakdowns.

---

### 5. `layout-four-grid`

2x2 grid using flex-wrap.

```html
<div class="layout-four-grid">
  <div class="grid-item"><!-- cell 1 --></div>
  <div class="grid-item"><!-- cell 2 --></div>
  <div class="grid-item"><!-- cell 3 --></div>
  <div class="grid-item"><!-- cell 4 --></div>
</div>
```

**Best for**: Matrix/quadrant frameworks. Four-category comparisons. Dashboard grids.

---

### 6. `layout-center-narrow`

Centered content column at 50-60% width. Maximum whitespace on sides.

```html
<div class="layout-center-narrow">
  <div class="h-md">Centered Title</div>
  <p>Focused content with breathing room.</p>
</div>
```

**Best for**: Single-statement slides. Quotes. Introductions. Breathing slides.

---

### 7. `layout-full-width`

Content spans the full slide width (minus padding).

```html
<div class="layout-full-width">
  <!-- wide component: bar chart, timeline, pipeline -->
</div>
```

**Best for**: Bar charts. Timelines. Pipelines. Any component that benefits from horizontal space.

---

### 8. `layout-split-hero`

Slide split into two halves: one image/visual, one text. Typically 50/50 or 40/60.

```html
<div class="layout-split-hero">
  <div class="split-visual">
    <img src="assets/image.jpg" alt="Description">
  </div>
  <div class="split-content">
    <div class="h-md">Title</div>
    <p>Description text</p>
  </div>
</div>
```

**Best for**: Image + text pairings. Product showcase. Case study highlights.

---

### 9. `layout-hero-center`

All content centered both vertically and horizontally. Large text, minimal elements.

```html
<div class="layout-hero-center">
  <div class="h-hero">Big Statement</div>
  <div class="meta-row">Author | Date</div>
</div>
```

**Best for**: Cover slides. Section dividers. Ending slides. Single big number or quote.

---

### 10. `layout-mosaic`

Asymmetric multi-zone layout. One large zone + 2-3 smaller zones.

```html
<div class="layout-mosaic">
  <div class="mosaic-main"><!-- large content --></div>
  <div class="mosaic-side">
    <div class="mosaic-item"><!-- small 1 --></div>
    <div class="mosaic-item"><!-- small 2 --></div>
  </div>
</div>
```

**Best for**: Dashboard-style slides. Mixed content types. Photo + caption arrangements.

---

### 11. `layout-sidebar`

Narrow sidebar (20-25% width) with main content area (75-80%).

```html
<div class="layout-sidebar">
  <div class="sidebar"><!-- navigation, agenda, TOC --></div>
  <div class="main-content"><!-- primary content --></div>
</div>
```

**Best for**: Slides with persistent context (agenda, timeline, navigation markers).

---

### 12. `layout-banner-body`

Full-width banner strip at top, body content below.

```html
<div class="layout-banner-body">
  <div class="banner"><!-- callout, key stat --></div>
  <div class="body-area"><!-- supporting content --></div>
</div>
```

**Best for**: Key finding + supporting evidence. Alert banner + detail. Section headers with content.

---

### 13. `layout-stacked-thirds`

Three horizontal bands stacked vertically.

```html
<div class="layout-stacked-thirds">
  <div class="stack-row"><!-- row 1 --></div>
  <div class="stack-row"><!-- row 2 --></div>
  <div class="stack-row"><!-- row 3 --></div>
</div>
```

**Best for**: Progressive content (past/present/future). Layered arguments. Three-point summaries.

---

### 14. `layout-timeline`

Optimized for vertical timeline component with generous vertical spacing.

**Best for**: Chronological narratives. Project milestones. Historical progressions.

---

### 15. `layout-comparison`

Two columns with a visual divider, optimized for head-to-head comparisons.

```html
<div class="layout-comparison">
  <div class="compare-left">
    <div class="h-sm">Option A</div>
    <!-- content -->
  </div>
  <div class="compare-divider"></div>
  <div class="compare-right">
    <div class="h-sm">Option B</div>
    <!-- content -->
  </div>
</div>
```

**Best for**: Before/after. Old way/new way. Pros/cons. Technology comparisons.

---

## Per-Theme Layout Recommendations

### aurora-gradient

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-hero-center`, `layout-two-col`, `layout-three-col` | Bold hero moments, gradient-driven |
| **Secondary** | `layout-center-narrow`, `layout-full-width`, `layout-split-hero` | Breathing slides, single focal elements |
| **Use sparingly** | `layout-four-grid`, `layout-sidebar` | Dense grids dilute the gradient energy |

**Rules**:
- Hero slides with gradient backgrounds need `layout-hero-center`
- One hero element per slide -- avoid clutter
- Generous whitespace to let gradients breathe
- Rounded containers (16px radius) throughout

### cyber-neon

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-title-body`, `layout-two-col`, `layout-three-col`, `layout-full-width` | Terminal-style structure, dark precision |
| **Secondary** | `layout-hero-center`, `layout-four-grid`, `layout-comparison` | Hero statements, data grids |
| **Use sparingly** | `layout-mosaic`, `layout-split-hero` | Asymmetric layouts fight the terminal aesthetic |

**Rules**:
- Chrome headers (`.chrome-top`) on content slides
- Sharp rectangles -- zero border-radius on all containers
- Neon glow reserved for focal elements only
- Dark background always -- no light slide backgrounds

### data-dashboard

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-three-col`, `layout-four-grid`, `layout-full-width`, `layout-title-body` | Dense data layouts, metric grids |
| **Secondary** | `layout-two-col`, `layout-banner-body`, `layout-stacked-thirds` | Supporting content, summary banners |
| **Use sparingly** | `layout-center-narrow`, `layout-split-hero` | Low density fights the dashboard character |

**Rules**:
- Metric cards in `layout-three-col` or `layout-four-grid`
- Data tables always use `layout-full-width`
- Dashboard headers (`.dash-header`) on content slides
- Compact padding -- data density is a feature, not a problem

### editorial-magazine

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-two-col`, `layout-split-hero`, `layout-mosaic` | Magazine-style asymmetry, editorial tension |
| **Secondary** | `layout-center-narrow`, `layout-hero-center`, `layout-full-width` | Breathing slides, hero statements |
| **Use sparingly** | `layout-four-grid`, `layout-three-col` | Dense grids fight the editorial character |

**Rules**:
- Asymmetric column splits preferred (30/70 or 40/60)
- Pull-quotes and big-quotes need `layout-center-narrow` or `layout-hero-center`
- Image-text pairings use `layout-split-hero` or `layout-two-col`
- Never stack identical grid layouts back-to-back

### ink-landscape

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-center-narrow`, `layout-two-col`, `layout-hero-center` | Generous negative space, ink wash elegance |
| **Secondary** | `layout-stacked-thirds`, `layout-title-body`, `layout-full-width` | Structured verse, timeline content |
| **Use sparingly** | `layout-four-grid`, `layout-three-col` | Dense grids fight the ink wash tranquility |

**Rules**:
- Generous negative space -- rice paper backgrounds need breathing room
- Seal stamps placed as section markers, not decoration
- Verse blocks need `layout-center-narrow` for proper focus
- Ink cards in `layout-two-col` or `layout-three-col`

### mckinsey-minimal

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-title-body`, `layout-two-col`, `layout-three-col`, `layout-full-width` | Clean structure, executive clarity |
| **Secondary** | `layout-hero-center`, `layout-banner-body`, `layout-comparison` | Hero statements, summary bars |
| **Use sparingly** | `layout-mosaic`, `layout-split-hero` | Asymmetric layouts fight the consulting precision |

**Rules**:
- Executive summary bars at the top of content slides
- Maximum whitespace with generous padding (6vh/6vw)
- Top-down communication flow within each slide
- Insight cards in `layout-two-col` or `layout-three-col`

### swiss-international

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-title-body`, `layout-three-col`, `layout-four-grid`, `layout-full-width` | Grid precision, structured columns |
| **Secondary** | `layout-two-col`, `layout-hero-center`, `layout-comparison` | Data pairings, hero statements |
| **Use sparingly** | `layout-mosaic`, `layout-split-hero` | Asymmetric layouts fight the grid character |

**Rules**:
- Equal column widths preferred (50/50, 33/33/33)
- Elements snap to the 12-column grid system
- Left-aligned content with generous right-side whitespace
- KPI cards belong in `layout-three-col` or `layout-four-grid`
- Data visualizations use `layout-full-width`

### ivory-theorem

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-title-body`, `layout-center-narrow`, `layout-two-col` | Scholarly journal layout, generous margins |
| **Secondary** | `layout-full-width`, `layout-hero-center`, `layout-stacked-thirds` | Theorem sequences, hero statements |
| **Use sparingly** | `layout-four-grid`, `layout-mosaic` | Dense grids fight the scholarly elegance |

**Rules**:
- Theorem/definition/proof blocks are primary content -- use `layout-title-body` or `layout-center-narrow`
- Citation callouts belong at slide bottom in `layout-title-body`
- Two-column layouts pair theorem statement (left) with proof or illustration (right)
- Generous margins evoke journal page layout -- never crowd the content

### chalk-classroom

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-title-body`, `layout-two-col`, `layout-center-narrow` | Lecture flow, step-by-step progressions |
| **Secondary** | `layout-stacked-thirds`, `layout-hero-center`, `layout-full-width` | Tutorial steps, hero concepts |
| **Use sparingly** | `layout-four-grid`, `layout-mosaic` | Dense grids fight the chalkboard warmth |

**Rules**:
- Step-by-step walkthroughs use `layout-stacked-thirds` or `layout-title-body`
- Annotation callouts pair with content in `layout-two-col`
- Chalk-bordered cards in `layout-two-col` or `layout-three-col`
- Whiteboard mode slides use same layouts with light variant

### bloomberg-dark

| Priority | Layouts | Character |
|----------|---------|-----------|
| **Primary** | `layout-three-col`, `layout-four-grid`, `layout-full-width`, `layout-title-body` | Dense financial data, metric grids |
| **Secondary** | `layout-two-col`, `layout-banner-body`, `layout-comparison` | Data pairings, summary banners |
| **Use sparingly** | `layout-center-narrow`, `layout-split-hero` | Low density fights the financial data character |

**Rules**:
- KPI cards in `layout-three-col` or `layout-four-grid`
- Data tables always use `layout-full-width`
- Source citation blocks at slide bottom
- Dark background always -- no light slide backgrounds in standard mode

---

## Layout Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| Repeated layout without a comparison or sequence rationale | Visual monotony | Introduce a different composition where it clarifies hierarchy or pacing |
| `layout-four-grid` in editorial-magazine | Too rigid for editorial character | Use `layout-mosaic` or `layout-two-col` |
| `layout-mosaic` in swiss-international | Too asymmetric for grid character | Use `layout-three-col` or `layout-four-grid` |
| Empty layout columns | Unfinished appearance | Either fill or use a narrower layout |
| Nesting 3+ levels deep | Overcomplicated, hard to maintain | Flatten to max 2 levels |
| `layout-hero-center` for data slides | Hero is for breathing, not density | Use `layout-title-body` or `layout-three-col` |
| All slides using `layout-title-body` | Boring, template-feeling | Mix in `layout-two-col`, `layout-full-width`, etc. |
