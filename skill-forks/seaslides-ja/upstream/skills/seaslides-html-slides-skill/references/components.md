# Component Catalog

> All CSS classes available across SeaSlides HTML Slides templates. Content authors should use ONLY these classes -- no inline styles except where explicitly noted. HTML output is rendered by Chromium before SVG/PNG/PPTX export.

---

## Slide Structure

Every slide is a `<section>` element with class `slide` plus mode modifiers:

```html
<section class="slide light" data-notes="Speaker notes">...</section>
<section class="slide dark" data-notes="Speaker notes">...</section>
<section class="slide hero dark" data-notes="Speaker notes">...</section>
<section class="slide hero light" data-notes="Speaker notes">...</section>
```

| Modifier | Effect |
|----------|--------|
| `light` | Light background, dark text |
| `dark` | Dark background, light text |
| `hero` | Centers all content, larger padding |

---

## Typography

| Class | Size | Weight | Use Case |
|-------|------|--------|----------|
| `.h-hero` | 7vw (~90px) | 700 | Title slides, major section openers |
| `.h-xl` | 4vw (~51px) | 700 | Section divider headings |
| `.h-md` | 2.4vw (~31px) | 600 | Content slide titles (most common) |
| `.h-sm` | 1.6vw (~20px) | 600 | Sub-section headings within a slide |
| `.meta-row` | 1.2vw (~15px) | 400 | Subtitles, dates, author info |
| `.tag` | 0.85vw (~11px) | 500 | Inline badges/category labels |
| `.spacer` | 3vh height | -- | Vertical spacing element |

Standard HTML elements also work: `<p>`, `<ul>`, `<ol>`, `<li>`, `<strong>`, `<em>`.

---

## Export-Safe Rules

When authoring content for SVG/PPTX export:

1. **Keep content HTML semantic** -- no `<style>`, `<script>`, or layout hacks in `content.html`
2. **Use template classes** -- add missing styling to `template.css`, not inline attributes
3. **Localize assets** -- prefer project `assets/` files or data URIs for deterministic batch export
4. **Check the final browser frame** -- SVG/PNG/PPTX export captures the settled Chromium render
5. **Use hooks for dynamic output** -- math, pseudocode, code highlighting, and charts must finish before export
6. **Inspect PPTX when editability matters** -- complex CSS can render visually while remaining less editable in PowerPoint

---

## Shared Components

These components are available in all themes. Each theme's `template.css` defines the visual styling.

---

### 1. KPI Card (`.kpi-card`)

Single metric display with large value, label, and optional note.

**Classes**: `.kpi-card`, `.kpi-value`, `.kpi-label`, `.kpi-note`

**Usage**: Present 1-4 key metrics. Place inside a flex-row container. Keep values short (2-5 characters).

**CSS Tokens**: `--kpi-accent`, `--kpi-bg`, `--kpi-value-color`, `--kpi-label-color`, `--kpi-note-color`

---

### 2. Insight Box (`.insight-box`)

Highlighted callout box for key observations or conclusions.

**Classes**: `.insight-box`, `.insight-title`

**Usage**: Usually one focused insight is clearest. Multiple boxes are acceptable
when the narrative genuinely compares distinct conclusions and the rendered
hierarchy remains obvious. Omit `.insight-title` for a plain highlighted box.

**CSS Tokens**: `--insight-bg`, `--insight-border`, `--insight-title-color`, `--insight-text-color`

---

### 3. Pipeline (`.pipeline`)

Horizontal step-by-step process visualization.

**Classes**: `.pipeline`, `.step`, `.step-number`, `.step-title`, `.step-desc`, `.step-connector`

**Usage**: Keep the sequence short enough to read at delivery size; split long
processes rather than shrinking labels. Use `&#8594;` (right arrow) between
steps. Not for non-sequential content.

**CSS Tokens**: `--pipeline-accent`, `--pipeline-title-color`, `--pipeline-desc-color`, `--pipeline-connector-color`

---

### 4. Timeline (`.timeline`)

Vertical chronological sequence.

**Classes**: `.timeline`, `.timeline-item`, `.timeline-date`, `.timeline-content`

**Usage**: Keep the visible chronology short enough to scan at delivery size;
split or summarize longer histories. Works well in a column layout. Not for
non-chronological content.

**CSS Tokens**: `--timeline-line-color`, `--timeline-date-color`, `--timeline-title-color`, `--timeline-text-color`

---

### 5. Bar Chart (`.bar-chart`)

Horizontal bar chart for comparing values.

**Classes**: `.bar-chart`, `.bar-row`, `.bar-label`, `.bar-track`, `.bar-fill`, `.bar-value`

**Data geometry**: Set numeric width in pixels or percentages as allowed by `shared-standards.md`. Keep a common scale and ensure the rendered length matches the label.

**Usage**: 3-7 bars maximum. Always include track background.

**CSS Tokens**: `--bar-label-color`, `--bar-track-bg`, `--bar-fill-color`, `--bar-value-color`

---

### 6. Vertical Bar Chart (`.vbar-chart`)

Bars growing upward from a baseline.

**Classes**: `.vbar-chart`, `.vbar-col`, `.vbar-value`, `.vbar-fill`, `.vbar-label`

**Data geometry**: Set numeric height in pixels or percentages as allowed by `shared-standards.md`. Keep a common baseline and scale.

**Usage**: 3-7 columns maximum. Container uses `align-items:flex-end`.

**CSS Tokens**: `--vbar-fill-color`, `--vbar-value-color`, `--vbar-label-color`

---

### 7. Progress Group (`.progress-group`)

Completion percentages or skill levels.

**Classes**: `.progress-group`, `.progress-item`, `.progress-label`, `.progress-percent`, `.progress-bar`, `.progress-fill`

**Data geometry**: Set numeric width in pixels or percentages as allowed by `shared-standards.md`.

**Usage**: 3-6 items maximum. More compact than `.bar-chart`.

**CSS Tokens**: `--progress-label-color`, `--progress-percent-color`, `--progress-track-bg`, `--progress-fill-color`

---

### 8. Stat Card (`.stat-card`)

Metric card with directional trend indicator.

**Classes**: `.stat-card`, `.stat-value`, `.stat-label`, `.stat-change`, `.stat-change.up`, `.stat-change.down`

**Usage**: Typically 3 cards in a flex-row. Use `.up` for positive (green), `.down` for negative (red).

**CSS Tokens**: `--stat-card-bg`, `--stat-card-border`, `--stat-value-color`, `--stat-label-color`, `--stat-up-color`, `--stat-down-color`

---

### 9. Funnel (`.funnel`)

Progressively narrowing bars for conversion funnels.

**Classes**: `.funnel`, `.funnel-step`, `.funnel-step-label`

**Data geometry**: Give each step a numeric pixel or percentage width proportional to a common maximum and verify it against the label.

**Usage**: 3-6 steps. Steps centered, progressively narrower. The narrowing IS the point.

**CSS Tokens**: `--funnel-color-1` through `--funnel-color-4`, `--funnel-text-dark`

---

### 10. Compare Grid (`.compare-grid`)

Side-by-side feature comparison with icons.

**Classes**: `.compare-grid`, `.compare-row`, `.compare-icon`, `.compare-text`, `.compare-cols`, `.compare-col-val`

**Usage**: 4-8 rows maximum. Use `&#10003;` for yes, `&#10007;` for no.

**CSS Tokens**: `--compare-row-bg`, `--compare-yes-color`, `--compare-no-color`, `--compare-text-color`

---

### 11. Code Block (`.code-block`)

Syntax-highlighted code display.

**Classes**: `.code-block`, `pre`, `code`, `.language-*`

**Usage**: Keep code snippets short (5-12 lines). Always specify language class.

**CSS Tokens**: `--code-bg`, `--code-text-color`, `--font-mono`

---

### 12. Big Quote (`.big-quote`)

Large centered quote for hero slides.

**Classes**: `.big-quote`, `blockquote`, `.cite`

**Usage**: Best on hero slides with minimal other content. Large italic text, centered.

**CSS Tokens**: `--quote-text-color`, `--quote-cite-color`, `--quote-weight`

---

### 13. Compare Table (`.compare-table`)

Structured tabular comparison using flexbox rows (not HTML tables).

**Classes**: `.compare-table`, `.table-header`, `.table-row`

**Usage**: Use only as many columns and rows as remain readable on the selected
canvas. Split dense comparisons instead of shrinking type. Use flexbox rows,
not `<table>` elements.

**CSS Tokens**: `--table-header-bg`, `--table-border-color`, `--table-row-even-bg`, `--table-row-odd-bg`, `--table-text-color`

---

### 14. Image Frame (`.img-frame`)

Image with optional caption.

**Classes**: `.img-frame`, `img`, `.img-caption`

**Usage**: Relative paths `assets/filename.ext`. Caption is optional. Content-bearing visuals only.

**CSS Tokens**: `--img-frame-border`, `--img-caption-bg`, `--img-caption-color`

#### Screenshot Semantics

Use `.img-frame` as a semantic `<figure>` for screenshots. Preserve the source
pixels and UI by default; record the target slot ratio, fit, crop permission,
crop-safe area, focal point, and concise caption/source when needed. Choose
background, padding, inset, shadow, corners, and alignment from the selected
theme. `object-fit: contain` is the safe default for evidence; use `cover` only
for a verified crop that keeps the required evidence.

---

### 15. Icon Grid (`.icon-grid`)

2x3 or 3x3 grid of icon+label pairs.

**Classes**: `.icon-grid`, `.icon-grid-item`, `.icon-grid-icon`, `.icon-grid-label`, `.icon-grid-desc`

**Usage**: Keep the grid scannable at the rendered size; split or regroup when labels wrap or cells become too small. Use HTML entities or inline SVG for icons. Description is optional.

**CSS Tokens**: `--icon-grid-accent`, `--icon-grid-label-color`, `--icon-grid-desc-color`

---

### 16. Numbered List (`.numbered-list`)

Large-number + text pairs for ordered content.

**Classes**: `.numbered-list`, `.numbered-item`, `.numbered-num`, `.numbered-content`

**Usage**: 3-5 items per slide. Zero-padded numbers (01, 02, 03). Not for non-sequential content.

**CSS Tokens**: `--numbered-accent`, `--numbered-title-color`, `--numbered-desc-color`

---

### 17. Callout Banner (`.callout-banner`)

Full-width colored strip with text.

**Usage**: Single-line impactful text. One per slide maximum.

**CSS Tokens**: `--banner-bg`, `--banner-text-color`

---

### 18. Split Stat (`.split-stat`)

Big number on left, explanation on right.

**Classes**: `.split-stat`, `.split-stat-number`, `.split-stat-body`

**Usage**: Single standout metric with context. Keep number short (2-4 characters + unit).

**CSS Tokens**: `--split-stat-bg`, `--split-stat-accent`, `--split-stat-number-color`, `--split-stat-title-color`, `--split-stat-desc-color`

---

### 19. Matrix 2x2 (`.matrix-2x2`)

Labeled 2x2 quadrant layout for frameworks and positioning maps.

**Classes**: `.matrix-2x2`, `.matrix-row`, `.matrix-cell`, `.matrix-labels-top`, `.matrix-labels-bottom`

**Usage**: Always label axes. Distinct background colors per quadrant.

**CSS Tokens**: `--matrix-label-color`, `--matrix-cell-bg-1` through `--matrix-cell-bg-4`

---

### 20. Pros and Cons (`.pros-cons`)

Two-column layout with positive/negative headers.

**Classes**: `.pros-cons`, `.pros-col`, `.cons-col`

**Usage**: Keep items balanced (3-5 per side). Use `&#10003;` for pros, `&#10007;` for cons.

**CSS Tokens**: `--pros-bg`, `--pros-accent`, `--cons-bg`, `--cons-accent`

---

### 21. Definition List (`.definition-list`)

Term + definition pairs.

**Classes**: `.definition-list`, `.definition-item`, `.definition-term`, `.definition-desc`

**Usage**: 3-6 definitions per slide. Short terms (1-3 words), concise definitions.

**CSS Tokens**: `--def-term-color`, `--def-desc-color`, `--def-border-color`

---

### 22. Roadmap (`.roadmap`)

Horizontal timeline with milestones.

**Classes**: `.roadmap`, `.roadmap-phase`, `.roadmap-marker`, `.roadmap-connector`

**Usage**: 3-5 phases. Left-to-right chronological progression.

**CSS Tokens**: `--roadmap-marker-bg`, `--roadmap-line-color`, `--roadmap-title-color`, `--roadmap-date-color`

---

### 23. Feature Card (`.feature-card`)

Icon + title + description card.

**Classes**: `.feature-card`, `.feature-icon`, `.feature-title`, `.feature-desc`

**Usage**: Place 2-3 cards in a flex-row. Keep description to 2-3 sentences. Always pair with at least one other card.

**CSS Tokens**: `--feature-card-bg`, `--feature-card-border`, `--feature-icon-color`, `--feature-title-color`, `--feature-desc-color`

---

### 24. Pull Quote (`.pull-quote`)

Offset large quote in magazine style. Designed for inline use within content.

**Classes**: `.pull-quote`

**Usage**: Use within content slides to break up text-heavy sections. Includes oversized opening quotation mark.

**CSS Tokens**: `--pull-quote-border`, `--pull-quote-accent`, `--pull-quote-text-color`, `--pull-quote-cite-color`

---

### 25. Agenda List (`.agenda-list`)

Numbered agenda items with optional timing.

**Classes**: `.agenda-list`, `.agenda-item`, `.agenda-number`, `.agenda-text`, `.agenda-time`

**Usage**: 4-7 items maximum. Time column is optional.

**CSS Tokens**: `--agenda-accent`, `--agenda-item-bg`, `--agenda-text-color`, `--agenda-time-color`

---

### 26. Highlight Strip (`.highlight-strip`)

Colored background text band for emphasis.

**Classes**: `.highlight-strip`

**Usage**: 1-2 sentence summaries or takeaways.

**CSS Tokens**: `--strip-bg`, `--strip-accent`, `--strip-text-color`

---

### 27. Waterfall Chart (`.waterfall-chart`)

Stacked positive/negative bars for financial analysis.

**Classes**: `.waterfall-chart`, `.waterfall-col`

**Data geometry**: Use numeric pixel or percentage heights. Use the allowed offset property for negative bars and verify a common baseline.

**Usage**: 4-7 columns maximum.

**CSS Tokens**: `--waterfall-positive-color`, `--waterfall-negative-color`, `--waterfall-total-color`, `--waterfall-baseline`, `--waterfall-label-color`

---

### 28. Annotation Box (`.annotation-box`)

Margin note / footnote callout.

**Classes**: `.annotation-box`, `.annotation-marker`, `.annotation-content`

**Usage**: Place at bottom or side of slide. Keep content brief (1-2 sentences). Auxiliary information only.

**CSS Tokens**: `--annotation-bg`, `--annotation-border`, `--annotation-accent`, `--annotation-text-color`

---

## editorial-magazine Specific Components

These components are unique to or specially treated in editorial-magazine:

| Component | Treatment |
|-----------|-----------|
| `.pull-quote` | Oversized serif quotation marks, editorial border treatment |
| `.big-quote` | Serif italic rendering, warm paper-toned background |
| `.feature-card` | Rounded corners allowed, editorial card styling |
| `.img-frame` | Caption offset below-left, magazine-style framing |
| `.meta-row` | Monospace rendering for date/metadata |

**Preferred components**: `.pull-quote`, `.big-quote`, `.split-stat`, `.feature-card`, `.timeline`, `.numbered-list`

---

## aurora-gradient Specific Components

These components are unique to or specially treated in aurora-gradient:

| Component | Treatment |
|-----------|-----------|
| `.aurora-card` | Rounded card (16px radius) with optional gradient border (`.grad-border`) |
| `.pill` | Rounded pill-shaped badge for categories and CTAs |
| `.grad-text` | Gradient text via background-clip for key labels and metrics |
| `.kpi-card` | Rounded corners, gradient accent borders |
| `.big-quote` | Large gradient-accented quote on hero slides |

**Preferred components**: `.aurora-card`, `.pill`, `.grad-text`, `.kpi-card`, `.big-quote`, `.feature-card`

---

## cyber-neon Specific Components

These components are unique to or specially treated in cyber-neon:

| Component | Treatment |
|-----------|-----------|
| `.chrome-top` | Terminal-inspired header with accent dot and monospace labels |
| `.kpi-card` | Sharp rectangles, neon glow border on focus, dark elevated background |
| `.bar-chart` | Neon accent fill colors, dark track background |
| `.code-block` | Dark terminal background with neon syntax highlighting |
| `.pipeline` | Neon-accented connectors, system-inspired step labels |

**Preferred components**: `.kpi-card`, `.bar-chart`, `.code-block`, `.pipeline`, `.compare-table`, `.stat-card`

---

## data-dashboard Specific Components

These components are unique to or specially treated in data-dashboard:

| Component | Treatment |
|-----------|-----------|
| `.metric-card` | Compact KPI card with value, delta indicator, and status color |
| `.badge` | Status badge with semantic color (green/amber/red/blue) |
| `.data-table` | Full-width tabular data with monospace numbers |
| `.dash-header` | Dashboard chrome header with status dot indicator |
| `.bar-chart` | Compact styling with status-colored fills |

**Preferred components**: `.metric-card`, `.badge`, `.data-table`, `.dash-header`, `.bar-chart`, `.stat-card`

---

## editorial-magazine Specific Components

These components are unique to or specially treated in editorial-magazine:

| Component | Treatment |
|-----------|-----------|
| `.pull-quote` | Oversized serif quotation marks, editorial border treatment |
| `.big-quote` | Serif italic rendering, warm paper-toned background |
| `.feature-card` | Rounded corners allowed, editorial card styling |
| `.img-frame` | Caption offset below-left, magazine-style framing |
| `.meta-row` | Monospace rendering for date/metadata |

**Preferred components**: `.pull-quote`, `.big-quote`, `.split-stat`, `.feature-card`, `.timeline`, `.numbered-list`

---

## ink-landscape Specific Components

These components are unique to or specially treated in ink-landscape:

| Component | Treatment |
|-----------|-----------|
| `.seal` | Traditional Chinese seal stamp (yin zhang) for section labels |
| `.verse-block` | Classical Chinese text in LXGW WenKai kaishu calligraphy |
| `.ink-card` | Card with vermillion top border and Chinese numeral indicator |
| `.big-quote` | Serif rendering with rice paper background |
| `.timeline` | Vermillion accent dots, ink wash styling |

**Preferred components**: `.seal`, `.verse-block`, `.ink-card`, `.big-quote`, `.timeline`, `.numbered-list`

---

## mckinsey-minimal Specific Components

These components are unique to or specially treated in mckinsey-minimal:

| Component | Treatment |
|-----------|-----------|
| `.exec-bar` | Accent-colored executive summary bar for key insight |
| `.insight-card` | Grey card with accent top border, numbered labels |
| `.kpi-card` | Clean, minimal styling with bold metric values |
| `.bar-chart` | Simple, professional styling with single accent fills |
| `.pipeline` | Clean geometric markers, restrained color |

**Preferred components**: `.exec-bar`, `.insight-card`, `.kpi-card`, `.bar-chart`, `.pipeline`, `.compare-table`

---

## swiss-international Specific Components

These components are unique to or specially treated in swiss-international:

| Component | Treatment |
|-----------|-----------|
| `.kpi-card` | Sharp rectangles, hairline borders, extreme size contrast |
| `.bar-chart` | Minimal styling, single accent color fills |
| `.compare-table` | Grid-precise alignment, hairline separators |
| `.pipeline` | Clean geometric step markers, 1px connectors |
| `.stat-card` | No borders, type-scale hierarchy only |

**Preferred components**: `.kpi-card`, `.bar-chart`, `.compare-table`, `.pipeline`, `.stat-card`, `.icon-grid`

---

## Layout Helpers

| # | Component | Classes | Purpose |
|---|-----------|---------|---------|
| 29 | Column Left | `.col-left` | Left child in two-col layout |
| 30 | Column Right | `.col-right` | Right child in two-col layout |
| 31 | Grid Item | `.grid-item` | Child in grid/mosaic layout |
| 32 | Card Group | `.card-group` | Flex wrapper for multiple cards |

---

## Anti-Patterns (Quick Reference)

| Do NOT | Do Instead |
|--------|-----------|
| Add `<style>` in content.html | Use template classes only |
| Use `style="color: red"` | Use semantic classes and CSS tokens |
| Use chart geometry that contradicts labels or mixes scales | Use consistent numeric geometry and verify the rendered scale |
| Write 50+ words per bullet | Keep bullets concise (under 15 words) |
| Put 8+ items in a grid | Split across slides |
| Use `<br>` for spacing | Use `.spacer` class or flex gaps |
| Use CSS Grid | Use flexbox with explicit widths |
| Use `position: absolute` | Use flexbox alignment |
| Use `flex:1` | Use explicit width values |
| Use `calc()` | Pre-compute all values |
