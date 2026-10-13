# Shared Technical Standards — Extended Reference

> **When to read**: Only consult this file when you need detailed examples for advanced CSS patterns, complex flexbox compositions, nested components, WebGL shader integration, advanced animation sequences, or cross-theme consistency rules. The core `shared-standards.md` contains everything needed for standard slide generation.

---

## Advanced CSS Patterns

### Nested Component Compositions

Components can be nested inside layout containers. When nesting, follow these rules:

1. **Outer container**: Uses a layout class (`layout-two-col`, `layout-three-col`, etc.)
2. **Inner children**: Use component classes (`.kpi-card`, `.insight-box`, etc.)
3. **Explicit widths at every level**: Both the layout column and the component inside it need explicit pixel widths

```html
<!-- Nested: KPI cards inside two-col layout -->
<div class="layout-two-col">
  <div class="col-left">
    <div class="h-md">Performance Metrics</div>
    <div class="layout-three-col">
      <div class="grid-item">
        <div class="kpi-card">
          <div class="kpi-value">92%</div>
          <div class="kpi-label">Accuracy</div>
        </div>
      </div>
      <div class="grid-item">
        <div class="kpi-card">
          <div class="kpi-value">1.2s</div>
          <div class="kpi-label">Latency</div>
        </div>
      </div>
      <div class="grid-item">
        <div class="kpi-card">
          <div class="kpi-value">99.9%</div>
          <div class="kpi-label">Uptime</div>
        </div>
      </div>
    </div>
  </div>
  <div class="col-right">
    <div class="insight-box">
      <div class="insight-title">Key Finding</div>
      <p>System performance exceeds all SLA targets.</p>
    </div>
  </div>
</div>
```

### CSS for Nested Layouts

When layout classes are nested, the inner layout's children need adjusted widths to fit inside the parent column:

```css
/* Top-level three-col: 370px per item in 1180px content area */
.layout-three-col .grid-item {
  width: 370px;
}

/* Three-col nested inside a col-left (480px): smaller items */
.col-left .layout-three-col .grid-item {
  width: 140px;
}

/* Three-col nested inside a col-right (680px) */
.col-right .layout-three-col .grid-item {
  width: 200px;
}
```

**Rule**: Always recalculate explicit pixel widths when nesting. The formula is:
```
child_width = (parent_width - (gaps * (num_children - 1))) / num_children
```

### Multi-Component Slides

Slides with multiple stacked components use vertical flex layout:

```html
<section class="slide light" data-notes="Dashboard overview">
  <div class="layout-title-body">
    <div class="title-area"><div class="h-md">Q4 Dashboard</div></div>
    <div class="body-area">
      <!-- First row: KPI cards -->
      <div class="layout-three-col">
        <div class="grid-item"><div class="kpi-card">...</div></div>
        <div class="grid-item"><div class="kpi-card">...</div></div>
        <div class="grid-item"><div class="kpi-card">...</div></div>
      </div>
      <!-- Second row: bar chart + insight -->
      <div class="layout-two-col">
        <div class="col-left"><div class="bar-chart">...</div></div>
        <div class="col-right"><div class="insight-box">...</div></div>
      </div>
    </div>
  </div>
</section>
```

**Vertical stacking rule**: The `.body-area` in `layout-title-body` owns the
remaining height and uses `flex-direction: column; min-height: 0`. Put semantic
rows directly inside it and let the owning layout class define `gap`, grid
tracks, vertical centering, or `justify-content: space-between`. Do not add
empty `.spacer` nodes or one-off margins merely to consume unused height.

When persistent chrome would distort composition measurements, mark the main
region with `data-audit-content` and the chrome with `data-audit-chrome`. Only a
content page whose theme explicitly declares `data-audit-composition="top-to-bottom"`
and theme-owned thresholds may produce a vertical-balance review item. Covers,
quotes, dividers, and closing pages remain observation-only unless their page
family defines a different contract.

---

## Complex Browser Layouts

### The Golden Rule: Stable Constraints

Browser export captures the final Chromium layout. Use explicit constraints where they prevent shifting, overflow, or ambiguous sizing, especially in dense benchmark decks.

### Pattern 1: Asymmetric Two-Column with Explicit Widths

```css
/* 30/70 split for editorial-magazine */
.layout-two-col-wide .col-left {
  width: 340px;
  flex-shrink: 0;
}
.layout-two-col-wide .col-right {
  width: 780px;
  flex-shrink: 0;
}
```

Percentage-based splits (`width: 30%` / `width: 70%`) are allowed, but pre-computed pixel or grid-track values are easier to audit when exact alignment matters.

### Pattern 2: Wrap-Based Grid (2x2, 2x3)

```css
/* 2x2 grid using flex-wrap */
.layout-four-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;  /* Explicit pixel gap, not vmin */
  width: 100%;
}
.layout-four-grid .grid-item {
  width: 560px;  /* (1180 - 16) / 2 = 582, rounded down for safety */
  flex-shrink: 0;
}
```

Use pixel gaps when precise cell sizing matters. Viewport units are fine for slide-level rhythm and responsive spacing.

### Pattern 3: Vertical Stack with Controlled Heights

```css
/* Three horizontal bands */
.layout-stacked-thirds {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  height: 100%;
}
.layout-stacked-thirds .stack-row {
  width: 100%;
  height: 200px;  /* Explicit height for each row */
  display: flex;
  flex-direction: row;
  align-items: center;
}
```

### Pattern 4: Sidebar Layout

```css
.layout-sidebar {
  display: flex;
  flex-direction: row;
  gap: 24px;
  width: 100%;
  height: 100%;
}
.layout-sidebar .sidebar {
  width: 240px;
  flex-shrink: 0;
}
.layout-sidebar .main-content {
  width: 900px;
  flex-shrink: 0;
}
```

### Layout Stability Cheat Sheet

| Want This | Robust Pattern | Riskier Pattern |
|---|---|---|
| Two equal columns | `width: 570px` on each child or `grid-template-columns: 1fr 1fr` | Unconstrained children with long content |
| Three equal columns | `width: 370px` or `repeat(3, 1fr)` with `minmax(0, 1fr)` | Columns without overflow handling |
| Fill remaining space | Explicit `min-width: 0` / `min-height: 0` on flex/grid children | Flex children with intrinsic long text |
| Gap between items | `gap: 16px` for exact grids | Viewport gaps inside dense chart layouts |
| Centered content | `justify-content: center; align-items: center` | Centering without container dimensions |
| Wrap to next row | `flex-wrap: wrap` + stable child basis | Wrap without known item widths |

---

## Responsive Token Scaling

### Viewport-Relative Token Strategy

CSS custom properties can use viewport units for responsive scaling. This pattern works well for spacing and typography:

```css
:root {
  /* Spacing tokens scale with viewport */
  --space-xs: 0.5vmin;   /* ~3.6px at 1280x720 */
  --space-sm: 1vmin;     /* ~7.2px */
  --space-md: 2vmin;     /* ~14.4px */
  --space-lg: 4vmin;     /* ~28.8px */
  --space-xl: 6vmin;     /* ~43.2px */

  /* Typography scales with viewport width */
  --text-body: 2vw;      /* ~25.6px at 1280 */
  --text-sm: 1.5vw;      /* ~19.2px */
  --text-xs: 1.2vw;      /* ~15.4px */
  --text-md: 2.4vw;      /* ~30.7px */
  --text-lg: 3.5vw;      /* ~44.8px */
  --text-xl: 5vw;        /* ~64px */
  --text-hero: 8vw;      /* ~102.4px */
}
```

### Token Conversion Reference

The browser computes viewport units at the current slide size:

| Viewport Unit | Pixel Equivalent | Common Usage |
|---|---|---|
| 1vw | 12.8px | Horizontal dimensions, font sizes |
| 1vh | 7.2px | Vertical dimensions |
| 1vmin | 7.2px (min of vw/vh) | Spacing, padding |

When precision matters (component internals, bar chart tracks), use pre-computed pixel values. When scaling matters (headings, slide-level spacing), use viewport units.

### When to Use px vs vw/vh

| Context | Recommendation | Reason |
|---------|---------------|--------|
| Layout widths (flex/grid children) | `px`, `%`, `fr`, or constrained flex | Match the composition and avoid overflow |
| Typography (heading sizes) | `vw` | Scales with viewport |
| Component internal spacing | `px` or `vmin` | Predictable, small values |
| Slide-level padding | `vmin` or `vh` | Scales proportionally |
| Borders | `px` | Always thin, fixed |
| Bar chart fills | `px` | Must be exact data representation |

---

## WebGL Shader Integration Patterns

### Architecture Overview

WebGL shaders live in `index-template.html` as inline `<script>` blocks. They render to a `<canvas>` element that sits behind the slide content. The CSS controls layering.

### Shader-to-Theme Color Binding

Shaders should reference the theme's CSS custom properties for color consistency. The JavaScript in `index-template.html` reads CSS variables and passes them as uniforms:

```javascript
// In index-template.html <script>
const style = getComputedStyle(document.documentElement);
const inkColor = style.getPropertyValue('--bg-dark').trim();
const accentColor = style.getPropertyValue('--accent-primary').trim();

// Parse to RGB floats for WebGL
function hexToGL(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  return [r, g, b];
}

// Pass to shader as uniform
gl.uniform3fv(colorUniform, hexToGL(accentColor));
```

### Per-Slide Shader Selection

Different slides can trigger different shader presets via `data-*` attributes:

```html
<!-- Hero slide with fluid shader -->
<section class="slide hero dark" data-notes="..." data-shader="fluid">
  ...
</section>

<!-- Section divider with contour shader -->
<section class="slide hero light" data-notes="..." data-shader="contour">
  ...
</section>
```

The navigation JavaScript reads `data-shader` and activates the corresponding WebGL program when the slide is visible.

### Shader Performance Rules

1. **Maximum 2 shader programs per theme** -- more causes performance degradation on mobile
2. **Shaders activate only on visible slide** -- paused on non-visible slides
3. **Resolution capping**: Render at half resolution (640x360) and scale up -- still looks good for ambient backgrounds
4. **Fallback**: If WebGL unavailable, CSS `background-color` takes over seamlessly

### SVG Export Compatibility

Canvas/WebGL backgrounds may not survive SVG-to-PPTX conversion as editable vector content. Design slides so they still look complete with a CSS fallback background:

```css
/* Fallback background */
.slide.hero.dark {
  background-color: var(--bg-dark);
}
/* WebGL adds visual richness in browser mode only */
```

---

## Advanced Animation Sequences

### Stagger Animation Pattern

Children of a slide animate in sequence using `data-anim="stagger"`:

```html
<section class="slide light" data-notes="..." data-anim="stagger">
  <div class="h-md">Key Metrics</div>
  <div class="layout-three-col">
    <div class="grid-item"><div class="kpi-card">...</div></div>
    <div class="grid-item"><div class="kpi-card">...</div></div>
    <div class="grid-item"><div class="kpi-card">...</div></div>
  </div>
  <div class="insight-box">...</div>
</section>
```

```css
/* CSS for stagger -- each direct child gets increasing delay */
.slide[data-anim="stagger"] > * {
  opacity: 0;
  animation: staggerIn 0.5s ease-out forwards;
}
.slide[data-anim="stagger"] > *:nth-child(1) { animation-delay: 0.0s; }
.slide[data-anim="stagger"] > *:nth-child(2) { animation-delay: 0.15s; }
.slide[data-anim="stagger"] > *:nth-child(3) { animation-delay: 0.3s; }
.slide[data-anim="stagger"] > *:nth-child(4) { animation-delay: 0.45s; }
.slide[data-anim="stagger"] > *:nth-child(5) { animation-delay: 0.6s; }

@keyframes staggerIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

**Important**: export captures a static settled frame. Animation selectors can be used for browser presentation, but exported slides must look complete without depending on motion.

### Build-Up Animation (Progressive Reveal)

For data-heavy slides where you want to reveal elements one group at a time:

```html
<section class="slide light" data-notes="..." data-anim="build-up">
  <div class="h-md" data-step="1">Revenue Analysis</div>
  <div class="bar-chart" data-step="2">...</div>
  <div class="insight-box" data-step="3">...</div>
</section>
```

The navigation JavaScript handles `data-step` attributes, showing elements progressively on click/keypress. This is a browser-mode feature -- SVG/PPTX export shows all elements visible.

### Slide Transition Types

| Transition | CSS | Effect |
|---|---|---|
| Fade | `opacity: 0 -> 1` | Smooth cross-dissolve |
| Slide Up | `transform: translateY(30px) -> translateY(0)` | Content rises into view |
| Slide Left | `transform: translateX(30px) -> translateX(0)` | Content slides from right |
| Scale | `transform: scale(0.95) -> scale(1)` | Subtle zoom-in |
| None | No animation | Instant switch |

### Animation Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Bounce / elastic easing | Unprofessional, distracting | Use `ease-out` or `ease-in-out` |
| Duration > 1s | Feels sluggish | Keep under 0.6s |
| Rotating elements | Dizzying, unprofessional | Avoid rotate transforms |
| Complex path animations | Performance issues, static export may differ | Simple translate/opacity only |
| Animation on every element | Visual noise | Stagger at group level, not element level |

---

## Cross-Theme Consistency Rules

### What Must Be Identical Across Themes

| Element | Must Match | Reason |
|---------|-----------|--------|
| Slide wrapper | `<section class="slide [mode]">` | Content.html portability |
| Component class names | `.kpi-card`, `.insight-box`, etc. | Same content.html works with any theme |
| Layout class names | `.layout-two-col`, `.layout-three-col`, etc. | Same content.html works with any theme |
| Mode classes | `light`, `dark`, `hero` | Mode switching is theme-independent |
| Data attributes | `data-notes`, `data-anim`, `data-shader` | Pipeline infrastructure |
| Typography classes | `.h-hero`, `.h-xl`, `.h-md`, `.h-sm`, `.meta-row`, `.tag` | Content uses these for sizing |
| Child class names | `.kpi-value`, `.kpi-label`, `.col-left`, `.col-right`, etc. | Component structure is shared |

### What Differs Between Themes

| Element | aurora-gradient | cyber-neon | data-dashboard | editorial-magazine | ink-landscape | mckinsey-minimal | swiss-international |
|---------|----------------|------------|----------------|-------------------|---------------|-----------------|---------------------|
| `--font-heading` | Outfit (sans) | Space Grotesk (sans) | Inter (sans) | Playfair Display (serif) | Noto Serif SC (serif) | DM Sans (sans) | Inter (sans) |
| `--font-body` | Outfit (sans) | Space Grotesk (sans) | Inter (sans) | Inter (sans) | Noto Sans SC (sans) | DM Sans (sans) | Inter (sans) |
| `--font-meta` | Outfit (sans) | JetBrains Mono (mono) | JetBrains Mono (mono) | JetBrains Mono (mono) | JetBrains Mono (mono) | IBM Plex Mono (mono) | Inter (sans) |
| `border-radius` | 16px (rounded) | 0px (sharp) | 8px (subtle) | 4-8px (warm) | 0-4px (minimal) | 0-4px (clean) | 0px (sharp) |
| Heading weight | 700 (bold) | 600-700 (bold) | 600-700 (bold) | 600-700 (bold) | 600-700 (bold) | 600-700 (bold) | 200-700 (inverse) |
| Accent application | Tri-color gradient | Single neon glow | Status color semantics | Warm borders, fills | Vermillion accents | Single corporate accent | Single high-contrast accent |
| Card borders | Gradient border option | Neon-glow border | 1px solid + 8px radius | Left-accent or soft outline | Vermillion top border | Accent top border | Hairline 1px only |
| Color variants | 4 gradients (Aurora, Sunset, Ocean, Forest) | 4 neons (Cyan, Magenta, Blue, Amber) | 5 status colors (green, amber, red, blue, purple) | 5 warm palettes (ink, indigo, forest, kraft, dune) | 4 traditional (Vermillion, Jade, Indigo, Gold) | 4 corporate (Blue, Emerald, Coral, Violet) | 4 accent colors (IKB, yellow, green, orange) |
| Special features | Gradient text, pill badges | Scan-line CRT, terminal chrome | Data tables, metric cards | WebGL fluid/contour/dispersion | Seal stamps, verse blocks | Executive summary bars | WebGL fine-grid, dot-matrix |

### Theme Switching Test

To verify theme portability:
1. Write a `content.html` using theme A
2. Switch to theme B (replace `template.css` and `index-template.html`)
3. Assemble and verify: all classes resolve, all components render, layout is intact
4. Visual style changes (fonts, colors, borders) but structure is preserved

---

## Image Optimization for SVG Export

### How Images Flow Through the Pipeline

```
content.html (<img src="assets/photo.jpg">)
  -> assemble.py (preserved as-is in root-level index.html)
    -> browser_dom_to_svg.mjs (Chromium renders the DOM and serializes each slide)
      -> svg_to_pptx (converts to PPTX image embed)
```

### Image Format Recommendations

| Format | Best For | SVG Export | PPTX Support |
|--------|----------|------------|--------------|
| PNG | Screenshots, diagrams, icons | Good | Good |
| JPEG | Photos, hero images | Good | Good |
| SVG | Vector graphics, icons, diagrams | Excellent (native) | Converted |
| WebP | Not recommended | Inconsistent | Limited |
| GIF | Not recommended | Static frame only | Limited |

### Image Sizing for Browser Export

Browser export supports normal image sizing. Follow these rules for predictable batch output:

```html
<!-- GOOD: explicit width in CSS class or component -->
<div class="img-frame">
  <img src="assets/diagram.png" alt="System architecture">
</div>

<!-- GOOD: width constrained by parent flex container -->
<div class="col-right">
  <img src="assets/photo.jpg" alt="Team photo">
</div>
```

The `img-frame` component and layout column classes handle sizing via CSS. Avoid setting explicit `width` and `height` attributes on the `<img>` element itself unless the component requires it.

### Image File Size Guidelines

| Context | Max File Size | Reason |
|---------|--------------|--------|
| Hero/background image | 500KB | Embedded in SVG output |
| Content image | 300KB | Balance quality vs export size |
| Icon/diagram | 50KB | Should be small and crisp |
| Total per deck | 5MB | PPTX file size concern |

Optimize images before placing in `assets/`. Use appropriate compression for the format (JPEG quality 80, PNG with pngquant).

### Transparency Handling

- PNG with alpha: Works in browser, SVG export, and PPTX
- SVG with transparency: Native support throughout pipeline
- JPEG: No transparency (white background assumed)

For images that need transparent backgrounds (icons, cutouts), always use PNG with alpha channel or SVG.

---

## Advanced Data Visualization Patterns

### Combining Multiple Chart Types

A single slide can combine chart components with text components:

```html
<section class="slide light" data-notes="Revenue breakdown">
  <div class="layout-title-body">
    <div class="title-area"><div class="h-md">Revenue by Channel</div></div>
    <div class="body-area">
      <div class="layout-two-col">
        <div class="col-left">
          <div class="bar-chart">
            <div class="bar-row">
              <div class="bar-label">Direct</div>
              <div class="bar-track"><div class="bar-fill" style="width:246px"></div></div>
              <div class="bar-value">82%</div>
            </div>
            <div class="bar-row">
              <div class="bar-label">Partner</div>
              <div class="bar-track"><div class="bar-fill" style="width:156px"></div></div>
              <div class="bar-value">52%</div>
            </div>
            <div class="bar-row">
              <div class="bar-label">Online</div>
              <div class="bar-track"><div class="bar-fill" style="width:195px"></div></div>
              <div class="bar-value">65%</div>
            </div>
          </div>
        </div>
        <div class="col-right">
          <div class="kpi-card">
            <div class="kpi-value">$4.2M</div>
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-note">+18% YoY</div>
          </div>
          <div class="spacer"></div>
          <div class="insight-box">
            <div class="insight-title">Trend</div>
            <p>Direct channel growth outpaces all others by 2x.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

### Waterfall Chart Positioning

Waterfall charts require precise vertical positioning using `margin-top` to offset bars from a baseline:

```html
<div class="waterfall-chart">
  <!-- Positive bar: starts at baseline -->
  <div class="waterfall-col">
    <div class="waterfall-value">+$120K</div>
    <div class="waterfall-bar positive" style="height:120px"></div>
    <div class="waterfall-label">Revenue</div>
  </div>
  <!-- Negative bar: offset from top -->
  <div class="waterfall-col">
    <div class="waterfall-value">-$45K</div>
    <div class="waterfall-bar negative" style="height:45px; margin-top:75px"></div>
    <div class="waterfall-label">COGS</div>
  </div>
  <!-- Running total bar -->
  <div class="waterfall-col">
    <div class="waterfall-value">$75K</div>
    <div class="waterfall-bar total" style="height:75px; margin-top:45px"></div>
    <div class="waterfall-label">Gross Profit</div>
  </div>
</div>
```

The `margin-top` on negative and total bars offsets them so they visually connect to the running total. This is one of the few cases where inline `style` with `margin-top` is acceptable in content.html (alongside bar widths/heights).

---

## Code Block and Math Rendering

### Code Blocks via Prism.js

Code highlighting is handled by Prism.js, loaded via CDN in `index-template.html`. Content.html uses standard `<pre><code>` markup:

```html
<div class="code-block">
  <pre><code class="language-python">
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
  </code></pre>
</div>
```

### Math via MathJax

Mathematical expressions use MathJax SVG rendering, loaded by `index-template.html`. Content.html uses LaTeX delimiters:

```html
<!-- Inline math -->
<p>The loss function is \(L = -\sum_{i} y_i \log(\hat{y}_i)\)</p>

<!-- Display math (block) -->
<div class="math-block">
  \[E = mc^2\]
</div>
```

The browser exporter waits for MathJax before capturing slides. If a template creates math dynamically, call the template math hook before export readiness resolves.

### Code highlighting in SVG Export

Syntax highlighting is handled in the browser by the template's code highlighter. The exporter captures the highlighted DOM after template scripts finish.

---

## Placeholder Patterns

When images are pending (not yet generated or provided):

```html
<div class="img-frame placeholder">
  <div class="placeholder-inner">
    <p class="meta-row">Pending: team photo</p>
  </div>
</div>
```

```css
/* In template.css */
.placeholder .placeholder-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 200px;
  background: var(--color-gray-100);
  border: 2px dashed var(--color-gray-300);
}
```
