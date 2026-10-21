# Template Designer — HTML Slides Theme Design Role

## Table of Contents

- [Core Mission](#core-mission)
- [Visual Impact Requirements](#visual-impact-requirements)
- [Core Template Inventory](#core-template-inventory)
- [Template Design Specifications](#template-design-specifications)
- [CSS Custom Properties Architecture](#css-custom-properties-architecture)
- [Typography System](#typography-system)
- [Color Theme Variants](#color-theme-variants)
- [Component CSS Classes](#component-css-classes)
- [Layout Patterns (Flexbox)](#layout-patterns-flexbox)
- [Browser Export Rules](#browser-export-rules)
- [WebGL Background Integration](#webgl-background-integration)
- [Animation Recipes](#animation-recipes)
- [Theme Conventions](#theme-conventions)
- [Common Pitfalls](#common-pitfalls)
- [Theme Quality Checklist](#theme-quality-checklist)

## Core Mission

Generate custom HTML slide themes based on Design Specification. Each theme is a self-contained CSS + HTML system using Template-Content Separation (TCS).

> **One-shot reference**: Read `${SKILL_DIR}/templates/index.json`, select the closest registered themes by use case and visual character, then study only those themes' `theme.md`, `demo.html`, `template.css`, and rendered output. The catalog is the authority for what themes exist; do not maintain another theme list here.
>
> **Quality reference**: Shipped themes show working CSS token tiers, component classes, modes, and typography systems. Use the closest examples as a quality baseline without copying their visual signatures into an unrelated design.

## Role Independence

This is a standalone role, triggered only through the `${SKILL_DIR}/workflows/create-template.md` workflow.

---

## Visual Impact Heuristics

> These heuristics distinguish a coherent theme from a merely valid stylesheet. Apply them in context; do not add decoration or components solely to satisfy a count.

### A. The "World-Building" Principle

A theme does NOT decorate a template — it creates a **WORLD** the viewer inhabits for the duration of the presentation.

- **Design decisions should serve the visual world.** If you are building a "brutalist web" theme, ask whether an element belongs in that design language before including it.
- **Content slides should remain recognizably part of the theme.** Atmosphere may come from typography, spacing, structure, color, or imagery; it does not require decoration on every page.
- **The "Visual Signature Test"**: Remove all text from a content slide. Can you still identify which theme this is? If not, the content slide needs more visual identity via CSS classes and background treatments.

### B. Persistent Background Atmosphere

Give content slides a consistent visual identity through the smallest effective combination of typography, spacing, structure, color, imagery, and reusable components. A plain body area is acceptable when restraint is the intended identity.

**Reference implementations:**
- aurora-gradient: Tri-color gradient backgrounds, rounded containers (16px), gradient text, pill badges
- cyber-neon: Dark backgrounds always, neon glow on focal elements, scan-line CRT texture, terminal chrome headers
- data-dashboard: Dashboard chrome with status dots, metric cards with monospace values, bordered compact cards
- editorial-magazine: WebGL fluid/contour/dispersion backgrounds on hero slides, warm paper-toned card backgrounds, serif/sans/mono font triad throughout
- ink-landscape: Rice paper backgrounds, vermillion seal stamps, verse blocks in kaishu, Chinese numerals
- mckinsey-minimal: Executive summary bars, maximum whitespace, insight cards with accent top borders
- swiss-international: WebGL fine grid + dot-matrix backgrounds, IKB blue accent, extreme weight-200/600 type contrast, hairline 1px dividers
- ivory-theorem: Warm ivory paper backgrounds, navy theorem blocks with left borders, crimson accents on definitions, citation callout cards
- chalk-classroom: Chalkboard green backgrounds, chalk-style dashed borders, handwritten Caveat headings, yellow annotation highlights
- bloomberg-dark: Near-black backgrounds always, scarlet accent on focal data, tabular-number KPI cards, financial data tables

**Implementation pattern in template.css:**
```css
/* Persistent atmosphere via slide-level classes */
.slide.light {
  background-color: var(--bg-light);
  /* Subtle texture or gradient for atmosphere */
  background-image: linear-gradient(
    135deg,
    var(--bg-light) 0%,
    var(--bg-warm) 100%
  );
}

/* Dark slides carry the world with inverted palette */
.slide.dark {
  background-color: var(--bg-dark);
  color: var(--text-on-dark);
}

/* Hero slides get maximum atmosphere */
.slide.hero.dark {
  background-color: var(--bg-dark);
  /* WebGL canvas fills the background via index-template.html */
}
```

**Anti-pattern**: "Only hero slides are decorated; content slides are plain white with just a colored heading." This produces themes that feel like skins, not worlds.

### C. Component Structural Diversity

Consider the following structural vocabulary when the target use cases need it:

| Structural Pattern | Use when | Example |
|---|---|---|
| Card with accent border | A bounded callout or comparison needs emphasis | `.insight-box`, `.callout-banner` |
| Pure typographic component | A quote or statement should remain unboxed | `.big-quote` |
| Data visualization component | The theme targets quantitative material | `.bar-chart`, `.vbar-chart`, `.funnel` |
| Grid/multi-item arrangement | Several peer items need comparison | `.icon-grid`, `.compare-grid` |
| Badge/tag | Compact categorical metadata is common | `.tag` |

**Anti-pattern**: "All 8 components are `div { background: X; border: Y; padding: Z; }` with different colors." When every component is a card-with-colored-border, the theme feels like a CSS stylesheet, not a designed experience.

### D. Slide Type Personality

Supported slide modes should have clear semantic roles, not merely arbitrary color changes:

| Slide Mode | Visual Approach | Key Differentiator |
|---|---|---|
| **Hero Dark** | Maximally decorated, WebGL background, centered content | Defines the theme's world. Full atmosphere. |
| **Hero Light** | Clean dramatic statement, generous whitespace | NOT just "big title." Needs typographic presence. |
| **Light** | Persistent world-atmosphere + content area | Carries atmosphere everywhere. Never reverts to "plain white." |
| **Dark** | Inverted palette, dramatic contrast | Changes the FEELING. Different bg color, strong accent contrast. |

**Bookending heuristic**: Give the first and last slides related visual weight when that strengthens the narrative arc. They need not use identical compositions or a forced hero treatment.

### E. The "Wow Moment" Test

After completing the theme, apply this self-evaluation:

1. **"Would someone choose this over a professionally designed PowerPoint template?"** If the answer is not clearly YES, iterate.
2. **"Does the theme have a memorable, content-appropriate signature?"** This may be subtle typography or grid behavior; it need not be a complex effect.
3. **"Can I describe this theme's world in one sentence?"** If not, the metaphor is too weak.

---

## Output Location

`${SKILL_DIR}/templates/<theme_name>/`

---

## Core Template Inventory

| # | File | Purpose | Description |
|---|------|---------|-------------|
| 01 | `template.css` | Complete Theme CSS | CSS custom properties, component classes, layout rules, typography, color variants |
| 02 | `index-template.html` | HTML Shell | CDN links (fonts, MathJax, Prism.js), `<link>` to template.css, `<div id="deck">{{CONTENT}}</div>`, navigation JS, WebGL shaders |
| 03 | `demo.html` | Usage Example | Complete content.html showcasing all slide modes and components |
| 04 | `theme.md` | API Summary | Concise theme reference for downstream roles |

---

## Template Design Specifications

### 1. Must Generate theme.md

Every theme must include:

**`theme.md`** — API summary document:
- Available CSS classes, component catalog, color variants, layout recommendations, font stacks

### 2. Inherit Design Specification

The theme must inherit and implement all parameters specified in the Strategist's Design Specification:
- Page format (16:9 at 1280x720 viewport)
- Color scheme (industry-specific or custom)
- Typography plan (font families + scale)
- Style objective (editorial / data-driven / minimal / creative)
- WebGL background presets (fluid, grid, contour, dispersion, etc.)

### 3. Template-Content Separation Principles

> Full TCS specification: see `shared-standards.md` section 1.

| Principle | Description |
|-----------|-------------|
| No Content in template.css | template.css contains zero content text |
| Clean Markup in content.html | Semantic HTML with CSS classes only |
| Component Encapsulation | Complex layouts via reusable CSS class patterns |
| No Decorative Inline Styles | Exception: numeric data geometry on the canonical allowlist in `shared-standards.md` |

### 4. Three-File Architecture (MANDATORY)

The template system uses three files:

| File | Responsibility | Never Contains |
|------|---------------|----------------|
| `index-template.html` | CDN links, font loading, `{{CONTENT}}` placeholder, WebGL shaders, navigation JS | Slide content, CSS rules |
| `template.css` | All CSS custom properties, component classes, layout definitions, typography | HTML, JavaScript, content text |
| `content.html` | Semantic slide sections with CSS classes, `data-notes`, and allowlisted data geometry | `<style>`, `<script>`, `<link>`, ad hoc inline styling |

**Build output**: `html_compiler.py <theme> --all --entry demo.html` atomically merges `index-template.html` + `demo.html`, inlines CSS, writes root-level `index.html`, and publishes synchronized `output/svgs/`, `output/pngs/`, `output/browser_pngs/`, overview, and receipts. Ordinary presentation projects use the default `content.html` entry.

When switching themes, replace `index-template.html` + `template.css`. `content.html` stays the same.

---

## CSS Custom Properties Architecture

### Three-Tier Token System

Templates use a 3-tier CSS custom property architecture. Each tier references the tier above, creating a cascade from raw values to semantic meaning to component-specific tokens.

#### Tier 1: Primitive Tokens

Raw color, font, and spacing values. Defined on `:root`.

```css
:root {
  /* -- Primitive color tokens -- */
  --color-ink: #1a1a2e;
  --color-paper: #faf9f6;
  --color-blue-600: #2563eb;
  --color-amber-500: #f59e0b;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-500: #6b7280;
  --color-gray-800: #1f2937;

  /* -- Primitive font tokens -- */
  --font-serif: 'Playfair Display', 'Noto Serif SC', Georgia, serif;
  --font-sans: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* -- Primitive spacing tokens -- */
  --space-xs: 0.5vmin;
  --space-sm: 1vmin;
  --space-md: 2vmin;
  --space-lg: 4vmin;
  --space-xl: 6vmin;
}
```

#### Tier 2: Semantic Tokens

Map primitives to meaning. These change per color variant (via `:root[data-theme="..."]`).

```css
:root {
  /* -- Semantic color tokens -- */
  --bg-light: var(--color-paper);
  --bg-dark: var(--color-ink);
  --bg-warm: #f5f0e8;
  --text-primary: var(--color-gray-800);
  --text-secondary: var(--color-gray-500);
  --text-on-dark: var(--color-paper);
  --accent-primary: var(--color-blue-600);
  --accent-secondary: var(--color-amber-500);
  --border-light: var(--color-gray-200);
  --border-dark: rgba(255, 255, 255, 0.15);

  /* -- Semantic typography tokens -- */
  --font-heading: var(--font-serif);
  --font-body: var(--font-sans);
  --font-meta: var(--font-mono);
}
```

#### Tier 3: Component Tokens

Per-component overrides that reference semantic tokens. Allows components to be restyled without touching component CSS.

```css
:root {
  /* -- KPI Card tokens -- */
  --kpi-accent: var(--accent-primary);
  --kpi-bg: var(--color-gray-100);
  --kpi-value-color: var(--accent-primary);
  --kpi-label-color: var(--text-secondary);
  --kpi-note-color: var(--text-secondary);

  /* -- Insight Box tokens -- */
  --insight-bg: var(--color-gray-100);
  --insight-border: var(--accent-primary);
  --insight-title-color: var(--accent-primary);
  --insight-text-color: var(--text-primary);

  /* -- Bar Chart tokens -- */
  --bar-label-color: var(--text-primary);
  --bar-track-bg: var(--color-gray-200);
  --bar-fill-color: var(--accent-primary);
  --bar-value-color: var(--text-secondary);
}
```

### Why Three Tiers

| Tier | Changes When | Changed By |
|------|-------------|-----------|
| Primitive | New theme created | Theme designer |
| Semantic | Color variant switched (`data-theme`) | Theme designer or user |
| Component | Individual component needs special color | Theme designer |

**Rule**: Component CSS classes ONLY reference Tier 3 tokens. Tier 3 tokens reference Tier 2. Tier 2 references Tier 1. Never skip tiers.

---

## Typography System

### Font Stack Patterns

Each theme defines a font triad (or pair). Examples from the shipped themes:

**editorial-magazine** (serif heading + sans body + mono meta):
```css
:root {
  --font-heading: 'Playfair Display', 'Noto Serif SC', Georgia, serif;
  --font-body: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
  --font-meta: 'JetBrains Mono', 'Fira Code', monospace;
}
```

**swiss-international** (all sans-serif):
```css
:root {
  --font-heading: 'Inter', 'Helvetica Neue', 'Noto Sans SC', sans-serif;
  --font-body: 'Inter', 'Helvetica Neue', 'Noto Sans SC', sans-serif;
  --font-meta: 'Inter', 'Helvetica Neue', sans-serif;
}
```

Other themes follow similar patterns: aurora-gradient uses Outfit, cyber-neon uses Space Grotesk + JetBrains Mono, data-dashboard uses Inter + JetBrains Mono, ink-landscape uses Noto Serif SC + LXGW WenKai, mckinsey-minimal uses DM Sans, ivory-theorem uses Playfair Display + Source Sans 3 + JetBrains Mono, chalk-classroom uses Caveat + Inter + JetBrains Mono, and bloomberg-dark uses DM Serif Display + Inter + JetBrains Mono. See each theme's `theme.md` for the full font stack.

### Size Scale (Viewport-Relative)

| CSS Class | Size | Weight | Usage |
|-----------|------|--------|-------|
| `.h-hero` | 7-8vw | 700 | Title/cover slides only |
| `.h-xl` | 4-5vw | 700 | Section divider headings |
| `.h-md` | 2.4-3.5vw | 600 | Content slide titles (most common) |
| `.h-sm` | 1.6-2vw | 600 | Sub-section headings within a slide |
| `.meta-row` | 1.2vw | 400 | Subtitles, dates, author info |
| `.tag` | 0.85vw | 500 | Inline badges / category labels |
| body text | 2vw | 400 | Paragraphs, lists |

### Weight Hierarchy

Avoid using `font-weight: 700` everywhere. Create typographic contrast:

**editorial-magazine approach** (warm, inviting):
- Display (`.h-hero`): 700 italic
- Headings (`.h-md`): 600
- Body: 400
- Meta: 400 monospace (the font change IS the contrast)

**swiss-international approach** (inverse weight, extreme contrast):
- Display (`.h-hero`): 200 (ultralight)
- Body heading (`.h-md`): 600
- Body: 400
- Labels: 500 uppercase (written in HTML, not text-transform)
- Numeric values: 700

### CJK Typography Rules

- Avoid forcing long Chinese titles onto one line; allow wrapping or choose a layout with sufficient measure
- Include `Noto Serif SC` / `Noto Sans SC` in font stacks for CJK fallback
- CJK body text at slightly larger size than Latin (compensate for visual density)
- Font loading via Google Fonts CDN in `index-template.html`

---

## Color Theme Variants

### Implementing Variants via `data-theme`

Each theme ships with multiple color variants. The default palette lives on `:root`. Variants override semantic tokens via `:root[data-theme="variant-name"]`.

```css
/* Default palette (editorial-magazine: ink-classic) */
:root {
  --bg-light: #faf9f6;
  --bg-dark: #1a1a2e;
  --accent-primary: #2563eb;
  --accent-secondary: #f59e0b;
}

/* Variant: indigo-porcelain */
:root[data-theme="indigo-porcelain"] {
  --bg-light: #f0f0f8;
  --bg-dark: #1e1e3f;
  --accent-primary: #4f46e5;
  --accent-secondary: #818cf8;
}

/* Variant: forest-ink */
:root[data-theme="forest-ink"] {
  --bg-light: #f5f7f2;
  --bg-dark: #1a2e1a;
  --accent-primary: #166534;
  --accent-secondary: #65a30d;
}
```

**Activation**: Set `data-theme` on the `<html>` element in `index-template.html`:
```html
<html data-theme="indigo-porcelain">
```

### editorial-magazine Color Variants

| Variant | Accent | Background | Character |
|---------|--------|------------|-----------|
| ink-classic (default) | Blue | Warm paper | Classic editorial |
| indigo-porcelain | Indigo/violet | Cool porcelain | Elegant, refined |
| forest-ink | Deep green | Sage paper | Natural, earthy |
| kraft-paper | Amber | Kraft brown | Warm, artisanal |
| dune | Terracotta | Sandy cream | Desert warmth |

### swiss-international Accent Colors

| Accent | Hex | Character |
|--------|-----|-----------|
| Klein Blue IKB (default) | #002fa7 | Classic Swiss authority |
| Lemon Yellow | #f7e018 | High energy, tech |
| Lime Green | #84cc16 | Growth, sustainability |
| Safety Orange | #ff6600 | Bold, industrial |

### Two-Tone Derivation Pattern

The most elegant palette pattern derives all colors from just `ink` and `paper`:

```css
:root {
  --ink: #1a1a2e;
  --paper: #faf9f6;
  --ink-light: rgba(26, 26, 46, 0.6);      /* Secondary text */
  --ink-faint: rgba(26, 26, 46, 0.2);      /* Borders, rules */
  --ink-ghost: rgba(26, 26, 46, 0.06);     /* Ghost decorations */
  --ink-muted: rgba(26, 26, 46, 0.4);      /* Metadata text */
  --rule-color: rgba(26, 26, 46, 0.3);     /* Hairline rules */
  --meta-color: rgba(26, 26, 46, 0.5);     /* Chrome/footer text */
}
```

This guarantees palette coherence — every color is harmonious because they share the same hue, differing only in opacity.

---

## Component CSS Classes

### Design Principles

Components are CSS class patterns defined in `template.css` and used in `content.html`. They encapsulate visual treatment so that content markup stays semantic and clean.

### Component Structure Pattern

Every component follows this CSS pattern:

```css
/* Container with Tier 3 tokens */
.insight-box {
  display: flex;
  flex-direction: column;
  background: var(--insight-bg);
  border-left: 4px solid var(--insight-border);
  padding: var(--space-md);
  gap: var(--space-sm);
}

/* Child elements */
.insight-box .insight-title {
  font-family: var(--font-heading);
  font-weight: 600;
  color: var(--insight-title-color);
  font-size: 1.8vw;
}
```

### Dark Mode Inversion

Components must work in both `.light` and `.dark` slide modes. Use mode-scoped overrides:

```css
/* Default (light mode) */
.kpi-card {
  background: var(--kpi-bg);
  border: 1px solid var(--border-light);
}

/* Dark mode override */
.slide.dark .kpi-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-dark);
}
.slide.dark .kpi-value {
  color: var(--text-on-dark);
}
```

### Opaque Backgrounds Required

Every component that displays text over a background MUST have an opaque `background` or `background-color`. This prevents WebGL backgrounds or slide gradients from bleeding through and making text unreadable.

```css
/* BAD: no background -- text may be unreadable over WebGL */
.insight-box {
  border-left: 4px solid var(--insight-border);
  padding: var(--space-md);
}

/* GOOD: opaque fill ensures readability */
.insight-box {
  background: var(--insight-bg);
  border-left: 4px solid var(--insight-border);
  padding: var(--space-md);
}
```

### Per-Theme Component Treatment

Components render differently per theme even though `content.html` uses the same class names:

| Theme | Card Components | Typography | Borders |
|-------|----------------|------------|---------|
| aurora-gradient | Rounded 16px, gradient borders, warm fills | Outfit for all text | Gradient or 2px borders |
| cyber-neon | Sharp rectangles (0 radius), neon glow on focus | Space Grotesk + JetBrains Mono | 1px neon accent or solid border |
| data-dashboard | 8px radius, bordered, compact | Inter + JetBrains Mono for metrics | 1px solid, status-colored accents |
| editorial-magazine | Rounded corners (4-8px), warm fills, serif headings | Playfair Display for titles | Soft borders, accent left-border |
| ink-landscape | Minimal radius (0-4px), vermillion top border | Noto Serif SC for headings | Vermillion accent top border |
| mckinsey-minimal | Clean minimal (0-4px), accent top border | DM Sans for all text | Subtle 1px, accent top border |
| swiss-international | Sharp rectangles (0 radius), extreme type contrast | Inter at weight 200-700 scale | Hairline 1px only, no rounded corners |
| ivory-theorem | Warm ivory fills, theorem/definition blocks, subtle borders | Playfair Display for titles, Source Sans 3 for body | Navy left-border on theorem blocks, crimson accents |
| chalk-classroom | Chalk-style dashed borders, chalkboard green fills | Caveat for headings, Inter for body | Dashed chalk borders, yellow accent highlights |
| bloomberg-dark | Dark premium cards, tabular-number KPIs, data tables | DM Serif Display for titles, Inter for body | Scarlet accent borders, 1px subtle dividers |

---

## Layout Patterns (Flexbox)

### Stable Browser Layout

Layout definitions may use flexbox, CSS Grid, and absolute positioning when those are the clearest browser layout tools. Prefer stable dimensions and predictable constraints so the exported browser frame matches the design.

### Standard Layout Classes

```css
/* Two-column layout */
.layout-two-col {
  display: flex;
  flex-direction: row;
  gap: var(--space-lg);
  width: 100%;
  height: 100%;
}
.layout-two-col .col-left {
  width: 480px;   /* Stable width for predictable export */
  flex-shrink: 0;
}
.layout-two-col .col-right {
  width: 680px;
  flex-shrink: 0;
}

/* Three-column layout */
.layout-three-col {
  display: flex;
  flex-direction: row;
  gap: var(--space-md);
  width: 100%;
}
.layout-three-col .grid-item {
  width: 370px;   /* Explicit width, not flex: 1 */
  flex-shrink: 0;
}

/* Four-grid (2x2) */
.layout-four-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
  width: 100%;
}
.layout-four-grid .grid-item {
  width: 560px;   /* Roughly 48% of 1180px content area */
  flex-shrink: 0;
}
```

### Stable Sizing Requirements

Use explicit widths, grid tracks, or constrained flex children for dense layouts. Percentages and `flex: 1` are allowed, but add `min-width: 0` / `min-height: 0` where long content could force overflow.

| Content Area Width | Two-Col Split | Three-Col Split | Four-Grid Cell |
|---|---|---|---|
| ~1180px (after padding) | 480px + 680px | 370px each | 560px each |

### Vertical Composition Is a Theme Contract

Do not equate good composition with maximum occupancy. Define how each page
family uses its main frame:

- centered cluster: balanced negative space around one focal group;
- top-to-bottom: tables, charts, processes, or evidence rows use a deliberate
  vertical path through the body;
- split anchors: a real opening group and a real lower conclusion/source/action
  define the field between them;
- image hero: media supplies lower-page visual weight;
- intentional breathing: cover, quote, divider, or closing page is sparse by
  design.

For top-to-bottom families, the main frame should own remaining height with
`flex: 1; min-height: 0` or an equivalent grid track. Distribute existing
semantic groups through container `gap`, track sizing, centering, or
`space-between`. Do not make blank cards taller, add empty spacer elements, or
push a group by an arbitrary offset merely to consume space. Optical offsets
are valid only after the owning frame and alignment mechanism are correct.

Themes may opt a top-to-bottom page into DOM composition review using
`data-audit-composition="top-to-bottom"`, an explicit `data-audit-content`
root, and theme-owned thresholds documented in `design-guide.md`. Mark
persistent footer/navigation chrome with `data-audit-chrome` when needed. The
measurement is review telemetry, not a target fill ratio.

### Nesting Rules

- Maximum 2 levels of nesting (`.layout-* > .col-* > .component`)
- Nested flex containers must also have explicit widths
- Gap values use CSS custom properties for consistency

---

## Browser Export Rules

The export pipeline renders in Chromium and captures the final settled DOM. All CSS in `template.css` must render correctly in that browser frame and remain stable for batch export.

### Supported Features (Use Freely)

| Feature | Notes |
|---------|-------|
| Flexbox and CSS Grid | Use whichever makes the layout clearer |
| `calc()`, custom properties, viewport units | Supported by Chromium |
| Pseudo-elements, shadows, gradients, filters | Supported in browser-rendered export |
| Absolute positioning | Allowed when container dimensions are stable |
| MathJax, Prism, pseudocode.js, D3 | Supported when template scripts finish before export |

### Must Handle Explicitly

| Feature | Workaround |
|---------|------------|
| Animations/transitions | Export captures a static settled frame; initial settled state must be complete |
| External images/fonts | Prefer local assets or deterministic data URIs for benchmarks |
| Dynamic charts/math/code | Register render work in `window.__renderDynamicContent` or equivalent template hooks |
| Complex CSS effects | Inspect SVG/PPTX if editable output matters |
| Data bars | Use numeric pixel or percentage values permitted by the canonical allowlist |

### Browser Export Checklist

Before shipping a theme, verify:
- [ ] Source gate passes: `validate_project.py <theme> --entry demo.html --source-only --profile theme-demo`
- [ ] `html_compiler.py <theme> --all --entry demo.html` creates `output/svgs/`, `output/pngs/`, `output/browser_pngs/`, `output/overview.png`, and current receipts
- [ ] `output/overview.png` and every browser PNG have been visually inspected; SVG-route PNGs diagnose conversion differences
- [ ] Math, code highlighting, pseudocode, charts, images, and fonts are present in browser PNGs
- [ ] Dense layouts have stable dimensions and no text overflow
- [ ] Bar chart fills use auditable values
- [ ] Visual gate passes: `validate_project.py <theme> --entry demo.html --require-build --profile theme-demo --artifact-profile visual`
- [ ] Required PPTX uses `html_compiler.py <theme> --all --include-pptx --entry demo.html`, followed by the `delivery` artifact profile with the same entry; standalone `--format pptx` is diagnostic only

---

## WebGL Background Integration

### Architecture

WebGL shader backgrounds are defined in `index-template.html` (not `template.css`). They run as a `<canvas>` element behind the slide content. The CSS only controls positioning and z-indexing.

### CSS Integration Pattern

```css
/* WebGL canvas sits behind content */
.webgl-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  pointer-events: none;
}

/* Slide content sits above */
.slide {
  position: relative;
  z-index: 1;
}
```

### Available Shader Presets

| Preset | Theme | Effect |
|--------|-------|--------|
| fluid | editorial-magazine | Smooth fluid simulation with warm tones |
| contour | editorial-magazine | Topographic contour lines |
| dispersion | editorial-magazine | Light dispersion / prism effect |
| fine-grid | swiss-international | Precise dot-grid pattern |
| dot-matrix | swiss-international | Dense dot matrix background |

Other themes (aurora-gradient, cyber-neon, data-dashboard, ink-landscape, mckinsey-minimal, ivory-theorem, chalk-classroom, bloomberg-dark) use CSS-only backgrounds or theme-specific atmosphere treatments rather than WebGL shaders. See each theme's `index-template.html` for details.

### WebGL and SVG Export

WebGL backgrounds are browser-first. They may not survive SVG-to-PPTX conversion as editable vector content. For export, slides should still have a solid or CSS fallback background so the design remains complete if the WebGL layer is flattened or omitted.

### Hero Slide Background Pattern

```css
/* Hero slides get enhanced background in browser mode */
.slide.hero.dark {
  background-color: var(--bg-dark);
  /* WebGL canvas renders behind this in browser */
  /* SVG export sees only background-color */
}
```

---

## Animation Recipes

### Data Attributes for Animation

Slides support `data-anim="..."` attributes for browser-mode transitions. These are navigation animations only — they do not affect SVG/PPTX export.

```html
<section class="slide light" data-notes="..." data-anim="fade-in">
  <!-- content -->
</section>
```

### Available Animation Types

| `data-anim` Value | Effect | Best For |
|---|---|---|
| `fade-in` | Opacity 0 to 1 | Default, most slides |
| `slide-up` | Content slides up from below | Data reveals |
| `slide-left` | Content slides in from right | Sequential progression |
| `zoom-in` | Content scales from 0.9 to 1 | Hero/statement slides |
| `stagger` | Children animate in sequence | Lists, card grids |

### CSS Implementation Pattern

```css
/* Animations defined in template.css */
.slide[data-anim="fade-in"] {
  animation: fadeIn 0.6s ease-out;
}
.slide[data-anim="stagger"] > * {
  animation: fadeIn 0.4s ease-out both;
}
.slide[data-anim="stagger"] > *:nth-child(1) { animation-delay: 0s; }
.slide[data-anim="stagger"] > *:nth-child(2) { animation-delay: 0.1s; }
.slide[data-anim="stagger"] > *:nth-child(3) { animation-delay: 0.2s; }
/* etc. */

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

**Important**: export captures a static settled browser frame. Design slides to look complete without relying on animation timing.

---

## Theme Conventions

### Convention 1: Three-Tier Token System

All colors, fonts, and spacing MUST go through the 3-tier token system (Primitive -> Semantic -> Component). Never hardcode hex values in component CSS rules.

```css
/* BAD: hardcoded color in component */
.insight-box { border-left: 4px solid #2563eb; }

/* GOOD: references component token */
.insight-box { border-left: 4px solid var(--insight-border); }
```

### Convention 2: No Content in template.css

Template CSS should not carry substantive text. All meaningful text lives in `content.html`; CSS pseudo-element `content:` may be used only for decorative marks that can disappear without changing the message.

### Convention 3: Deduplicate Box Components

One base class + modifier variants, not separate components with identical CSS:

```css
/* GOOD: base class + modifier via token override */
.callout { /* base styling */ }
.callout.warning { --callout-border: var(--color-amber-500); }
.callout.info { --callout-border: var(--accent-primary); }
```

### Convention 4: Dark Mode via Slide Class

Use `.slide.dark .component` selectors for dark mode, not separate component classes:

```css
/* GOOD: mode-scoped */
.slide.dark .kpi-card { background: rgba(255,255,255,0.08); }

/* BAD: separate dark class */
.kpi-card-dark { background: rgba(255,255,255,0.08); }
```

### Convention 5: Stable Layout Dimensions

Every flex/grid child that needs predictable sizing must have stable constraints. Use explicit widths, grid tracks, `minmax(0, 1fr)`, and `min-width: 0` where long content could force overflow.

### Convention 6: Inline Styles Only for Canonical Data Geometry

The only permitted inline styles are numeric data geometry on the canonical class/property allowlist in `shared-standards.md`. All decorative and reusable visual treatment must come from CSS classes.

### Convention 7: Speaker Notes on Every Slide

Every `<section class="slide">` MUST have a non-empty `data-notes="..."`
attribute. Notes are part of the delivery artifact, not optional placeholder
markup. The atomic PPTX build maps these values to slide notes in source order;
the delivery gate verifies a non-empty notes part and relationship for every
slide, so sidecar files are not required for standard HTML projects.

### Convention 8: Resolve a Slide Mode

Prefer an explicit `light` or `dark` class (optionally with `hero`). A slide may
omit it only when the selected theme's `theme.md` documents an intentional
default mode. Do not infer a contract from incidental CSS inheritance.

---

## Common Pitfalls (MUST READ)

| # | Pitfall | Rule |
|---|---------|------|
| 0 | Unbounded grid/flex children | Long text overflows or pushes layout | Add stable tracks, `min-width: 0`, and overflow handling. |
| 1 | Animation-only content | Export misses content | Make the settled static frame complete. |
| 2 | Late async chart/math render | Export captures placeholders | Register render hooks and wait for readiness. |
| 3 | External URLs | Batch output changes or assets disappear | Use local assets or data URIs. |
| 4 | Pseudo-elements for meaningful text | PPTX/editability may suffer | Put real message text in HTML. |
| 5 | Bar geometry contradicts labels or scale | Use consistent numeric pixel or percentage geometry and verify the render. |
| 6 | Complex visual effects without PPTX check | PNG looks fine but PPTX may flatten | Inspect `slides.pptx` for required outputs. |
| 7 | Unresolved slide mode | Use `light`/`dark`, or document the theme's intentional default mode in `theme.md`. |
| 8 | Missing speaker notes | Every slide needs a non-empty `data-notes="..."`. |
| 9 | Components without opaque bg | Cards over WebGL backgrounds become unreadable. Always set `background` or `background-color`. |
| 10 | Remote `background-image: url()` | May fail in batch. Prefer local assets or data URIs. |
| 11 | Template CSS with semantic text | Hard to edit and validate. Keep meaning in `content.html`. |
| 12 | Inline styles in content.html | Permit only numeric data geometry on the canonical class/property allowlist in `shared-standards.md`; put everything else in classes. |
| 13 | Content frame collapses at the top | Define the page family's vertical mode and height owner; do not disguise the defect with a footer, oversized blank card, or arbitrary spacer. |

---

## Demo File Best Practices

**Structure**: Cover slide (hero dark) -> Section divider (hero light) -> Content sections (demo each component + layout) -> Data slide (dark) -> Closing slide (hero dark).

**Rules**: Use realistic content (not lorem ipsum). Demonstrate the theme's important layouts and components without quota-filling. Include an image example when the theme supports images. Validate with `validate_project.py` before shipping. Keep the demo concise enough to review.

---

## Theme Quality Checklist

> **Common checks**: See `shared-standards.md` for shared technical constraints (TCS, browser export readiness, anti-monotony).

**Template-designer-specific checks**:
- [ ] Three-tier token system implemented (Primitive -> Semantic -> Component)
- [ ] All component CSS classes reference Tier 3 tokens only
- [ ] Color variants work via `:root[data-theme="..."]` override
- [ ] Typography uses `--font-heading`, `--font-body`, `--font-meta` tokens
- [ ] Size classes defined: `.h-hero`, `.h-xl`, `.h-md`, `.h-sm`, `.meta-row`, `.tag`
- [ ] Layout classes use stable flex/grid/positioning constraints
- [ ] Flex/grid children have overflow-safe sizing
- [ ] Page families document an intentional vertical mode and lower-page mechanism
- [ ] Math, code highlighting, pseudocode, charts, and images render in exported PNGs
- [ ] Remote background/image URLs are avoided for benchmark templates
- [ ] Dark mode overrides for all components (`.slide.dark .component`)
- [ ] All card components have opaque `background` / `background-color`
- [ ] WebGL background CSS (`z-index`, `pointer-events`) is correct
- [ ] Data-fill geometry uses permitted numeric values and matches labels/scales
- [ ] Demo file (`demo.html`) showcases all slide modes and components
- [ ] `theme.md` API reference is complete
- [ ] Source gate passes with `python3 ${SKILL_DIR}/scripts/validate_project.py <theme> --entry demo.html --source-only --profile theme-demo`
- [ ] Synchronized build via `python3 ${SKILL_DIR}/scripts/html_compiler.py <theme> --all --entry demo.html` renders correctly
- [ ] Every browser PNG and the overview are visually reviewed; no content page is accidentally top-packed; visual gate passes with `--entry demo.html --require-build --profile theme-demo --artifact-profile visual`
- [ ] When PPTX is required, same-build `--all --include-pptx --entry demo.html` passes `--entry demo.html --require-build --profile theme-demo --artifact-profile delivery`; direct SVG-to-PPTX is not delivery
- [ ] Complex selectors and pseudo-elements are tested in exported PNG/SVG output
- [ ] Demo inline styles, if any, conform to the canonical data-geometry allowlist
- [ ] Every slide has an explicit mode or a documented theme default, plus non-empty `data-notes`
- [ ] Font CDN links in `index-template.html` include CJK fallbacks

---

## Aesthetic Identity and Visual Distinction

> This section captures lessons from creating themes. The difference between a memorable theme and a forgettable one is **strong aesthetic identity**.

### What Makes a Theme Memorable

A great theme has:
1. **A clear visual metaphor** — editorial-magazine = *Monocle* magazine; swiss-international = Vignelli/Muller-Brockmann grid systems; aurora-gradient = Apple Keynote; cyber-neon = cyberpunk terminal; data-dashboard = live monitoring console; ink-landscape = shanshui ink wash painting; mckinsey-minimal = McKinsey boardroom; ivory-theorem = academic journal; chalk-classroom = university lecture hall; bloomberg-dark = Bloomberg terminal editorial. The metaphor informs every design decision.
2. **Distinctive CSS treatment** — component styling that could not belong to any other theme. Editorial's serif/sans/mono triad is unmistakable. Swiss's weight-200 ultralight display is unmistakable.
3. **Unique component vocabulary** — components styled from the theme's world, not generic default CSS.
4. **Color palette derived from the metaphor** — editorial uses warm paper tones; Swiss uses IKB blue on clinical white.
5. **A recognizable visual signature** — the thing people remember may be a grid, type system, restrained motion, illustration language, or another content-appropriate treatment.

### Anti-Patterns That Kill Identity

| Problem | Example | Fix |
|---------|---------|-----|
| Generic card styling | Same rounded rectangle everywhere | Per-theme card personality (sharp vs. warm) |
| Blue-on-white default | Every business deck | Pick colors from the metaphor's world |
| Same layout without a structural reason | `layout-title-body` on everything | Vary layout classes where content roles differ; retain repetition for true comparisons or sequences |
| Mode changes without semantic purpose | Arbitrary light/dark alternation | Use contrast for meaningful transitions or emphasis |
| Font monoculture | One font weight everywhere | Create type-scale contrast (200 vs 700) |

### Per-Theme Identity Strategy

| Theme | Identity Through | Key Differentiators |
|-------|-----------------|---------------------|
| aurora-gradient | Tri-color gradients, rounded shapes, gradient text, pill badges | Outfit font, 16px radius, gradient backgrounds, Apple Keynote energy |
| cyber-neon | Neon glow hierarchy, terminal chrome, dark-first design, scan-line texture | Space Grotesk, zero radius, CRT overlay, system-inspired labels |
| data-dashboard | Status semantics, compact metrics, dashboard chrome, data tables | JetBrains Mono numbers, green/amber/red coding, 8px radius bordered cards |
| editorial-magazine | Font triad (serif/sans/mono), warm paper tones, WebGL fluid backgrounds, magazine asymmetry | Playfair Display, editorial tension in column splits, warm `#faf9f6` paper |
| ink-landscape | Seal stamps, verse blocks, Chinese numerals, rice paper backgrounds | Noto Serif SC, vermillion accents, LXGW WenKai kaishu, ink/paper duality |
| mckinsey-minimal | Maximum whitespace, executive summary bars, evidence-based structure | DM Sans, single accent, top-down communication, action-oriented closing |
| swiss-international | Type-scale extremes (200/700 weight contrast), IKB blue, 1px hairlines, zero border-radius | Weight 200 display, no rounded corners, grid precision, Carbon dot backgrounds |
| ivory-theorem | Theorem/definition/proof blocks, citation callouts, scholarly structure | Playfair Display serif headings, warm ivory `#FFFEF8` paper, navy + crimson accents |
| chalk-classroom | Chalk-style dashed borders, handwritten Caveat headings, annotation callouts | Chalkboard green `#1B2B1F`, chalk white text, yellow highlights, whiteboard mode |
| bloomberg-dark | KPI cards with tabular numbers, data tables, source citations, scarlet accent | DM Serif Display headings, near-black `#0F0F12`, financial editorial authority |
