# Executor Canvas -- High-Craft Visual Composition

## Role Definition

High-craft visual HTML slide executor for editorial magazine and Swiss international presentations. Every slide is a unique layout canvas with per-slide CSS class composition, advanced flexbox arrangements, WebGL backgrounds, and editorial-grade visual craft. Restraint over spectacle. Structure over decoration. The benchmark is "indistinguishable from a professional design studio's output."

**Core philosophy**: Canvas = giving the LLM freedom to write visually rich, hand-crafted layouts directly in `content.html` using CSS component classes, custom flexbox arrangements, and the theme's design vocabulary. Canvas is NOT about relying on repeated component patterns. It is about composing unique pages from first principles -- each slide a distinct visual composition.

## References

- `base.md` -- Common execution guidelines, phased generation workflow, slide type mapping
- `shared-standards.md` -- HTML/CSS technical constraints, layout system, browser export rules
- `template-designer.md` -- Theme design patterns, component CSS implementations
- `components.md` -- Component catalog with classes and usage
- `layouts.md` -- Layout patterns with per-theme recommendations
- `design-guide.md` -- Aesthetic philosophy, anti-patterns, visual excellence principles
- `image-layout-patterns.md` -- Image-text layout patterns (Primary + Modifier vocabulary)

> **Rule**: All technical standards (APIs, browser export constraints, class names) are defined in those documents. This file covers **Canvas style-specific** guidance only.

---

## Complexity Level

Canvas is the **highest complexity tier** -- each slide in `content.html` is a unique layout composition.

| When Canvas is the Right Choice | When Canvas is Overkill |
|-------------------------------|----------------------|
| Magazine editorial decks | Internal status updates |
| Brand launches / keynotes | Quick training materials |
| Festival / gallery presentations | Data-driven consulting |
| Portfolio / case study showcases | Any deck under 8 slides |

---

## 1. The Canvas Architecture

### What Canvas Is

Every slide is a unique composition built from CSS building blocks:

- **Layout classes** -- `layout-two-col`, `layout-mosaic`, `layout-split-hero`, `layout-three-col`, etc.
- **Component classes** -- `.kpi-card`, `.insight-box`, `.bar-chart`, `.pull-quote`, `.feature-card`, etc.
- **Mode classes** -- `light`, `dark`, `hero light`, `hero dark` for slide-level atmosphere
- **Typography classes** -- `.h-hero`, `.h-xl`, `.h-md`, `.h-sm`, `.meta-row`, `.tag`
- **Image compositions** -- `.img-frame`, `.layout-split-hero` for editorial image integration
- **Data visualization** -- `.bar-chart`, `.vbar-chart`, `.stat-card`, `.kpi-card` for metrics

### What Canvas Is NOT

- Inline `style="..."` outside the canonical numeric data-geometry allowlist
- `<style>`, `<script>`, or `<link>` tags in content.html
- Raw layout hacks in `content.html`; use theme classes and browser-tested template CSS
- Mechanical layout repetition that does not support comparison, sequence, or continuity

### Two-Level Architecture

**template.css provides**: CSS custom properties, layout classes, component classes, mode classes, WebGL integration.

**content.html composes**: Content-driven per-slide arrangements, deliberate mode and layout choices, relevant components and images, and speaker notes on every `<section>`.

### Abstraction Threshold

> If a visual pattern repeats across 3+ slides, it should be a CSS class in `template.css`. Unique compositions belong in `content.html` using existing classes.

---

## 2. Seven Iron Rules of Canvas Aesthetics

### Rule 1: Restraint Over Spectacle
- Hero slides (cover, divider, closing) use `hero dark` with WebGL; body slides stay clean
- Breathing slides carry a single focal element framed by deliberate negative space; no fixed occupancy percentage defines the result
- Keep the component set small enough to preserve a clear hierarchy; split crowded content when needed

### Rule 2: Typography Is the Foundation

**editorial-magazine (Triple-Font System):**
| Role | Font | Usage |
|------|------|-------|
| Display | Serif (Playfair Display) | `.h-hero`, `.h-xl`, `.h-md` |
| Body | Sans-serif | `<p>`, `<li>`, descriptions |
| Metadata | Monospace | `.meta-row`, `.tag` |

**swiss-international (Single-Family System):**
Large display text uses weight 200 (ExtraLight). Inverse weight hierarchy: bigger = lighter weight. All sans-serif, always.

### Rule 3: Color Restraint
- Use the selected theme's semantic palette; restrained two-tone systems suit some themes, while multi-accent systems such as neo-bauhaus are intentional
- Remove colors without a communication or theme-identity role; do not enforce a universal hue count
- CSS custom properties only -- never inline color values

### Rule 4: Grid Supremacy
- Left-aligned by default. Center only for hero/focus slides
- **editorial-magazine**: asymmetric splits (30/70, 40/60). Never 50/50.
- **swiss-international**: equal splits acceptable. Grid-snapped.

### Rule 5: Sharp Geometry
- **swiss-international**: No gradients, no shadows, no `border-radius`. Hairline dividers (1px).
- **editorial-magazine**: Rounded corners allowed on `.feature-card`. Serif quotation marks on `.pull-quote`.

### Rule 6: Image Discipline
- Use `.layout-split-hero` for image+text. `.img-frame` for captioned images.
- Keep images inside the theme's safe canvas geometry and verify the rendered result; use relative paths such as `src="assets/filename.ext"`
- Generated images must NOT contain slide chrome

### Rule 7: Visual Rhythm Planning

Plan before writing:

```
Slide 1:  hero dark   (cover)
Slide 2:  light       (content -- layout-two-col)
Slide 3:  light       (data -- layout-three-col, kpi-cards)
Slide 4:  dark        (data -- layout-full-width, bar-chart)
Slide 5:  hero dark   (section divider)
Slide 6:  light       (content -- layout-split-hero)
Slide 7:  hero light  (breathing -- big-quote)
Slide 8:  light       (content -- layout-mosaic)
Slide 9:  hero dark   (closing)
```

**Composition heuristics:**
- Review repeated modes and layouts; keep them when comparison or sequence benefits from consistency
- Use hero or breathing slides only at meaningful emphasis or transition points

There is no fixed Hero quota. Use Hero or breathing slides only when the narrative needs emphasis, transition, or a deliberate change of pace.

---

## 3. Canvas Layout Patterns (12 Registered)

> Every Canvas slide should map to one of these. If none fits, compose from two -- do not invent from scratch. See `layouts.md` and `components.md` for full class references.

### 3.1 Full-Bleed Hero (WebGL Background)
Mode `hero dark` with `.layout-hero-center`. Use `.h-hero` + `.meta-row`. WebGL renders automatically. For covers, chapter openers, closing.

### 3.2 Asymmetric Split (layout-two-col-wide)
60/40 split. Large statement left (`.h-xl`), supporting detail right (`.insight-box`, `.definition-list`). Most common Canvas layout.

### 3.3 Pillar Cards (layout-three-col)
Three equal `.feature-card` elements with `.feature-icon` (01/02/03), `.feature-title`, `.feature-desc`. Classic "three pillars."

### 3.4 Data Dashboard (KPI Row + Detail)
`.layout-three-col` with 3 `.kpi-card` elements at top. `.insight-box` below for interpretation. For performance/metrics slides.

### 3.5 Dark Statement (Section Divider)
Mode `hero dark` with `.layout-hero-center`. `.tag` for section label, `.h-xl` for statement. WebGL background automatic.

### 3.6 Dark Stat Slide (Giant Numbers)
Mode `dark` with `.split-stat` components in `.layout-three-col`. Giant `.split-stat-number` with `.split-stat-body` context.

### 3.7 Two-Column Comparison
`.layout-comparison` with `.compare-left`, `.compare-divider`, `.compare-right`. Lists in each column. Optional `.pull-quote` below.

### 3.8 Chapter Divider (Image Split)
`.layout-split-hero` with `.split-visual` (image) + `.split-content` (`.tag` chapter label + `.h-xl` title). For section transitions.

### 3.9 Focus Quote (Breathing Slide)
Mode `hero dark` or `hero light`. `.layout-center-narrow` with `.big-quote` > `<blockquote>` + `.cite`. Minimal chrome.

### 3.10 Numbered Process + Visual
`.layout-two-col`: left `.numbered-list` (01/02/03 items), right `.img-frame` or diagram image.

### 3.11 Context Cards (Three-Column)
`.layout-three-col` with 3 `.feature-card` elements: "Context. Opportunity. Impact." pattern.

### 3.12 Mosaic Dashboard
`.layout-mosaic`: `.mosaic-main` (primary chart/visual) + `.mosaic-side` with `.mosaic-item` (`.kpi-card`, `.insight-box`).

### Example: Composing Canvas Slides

A Canvas deck should demonstrate variety across every dimension -- mode, layout, and component selection. Below are four consecutive slides showing the kind of rhythmic variety expected.

```html
<!-- Slide 1: Asymmetric split with statement + supporting data -->
<section class="slide light" data-notes="Core thesis with supporting metrics.">
  <div class="layout-two-col-wide">
    <div class="col-left">
      <div class="tag">CORE THESIS</div>
      <div class="h-xl">The strategic insight that reframes everything</div>
    </div>
    <div class="col-right">
      <div class="insight-box"><p>Key context with supporting data.</p></div>
      <div class="spacer"></div>
      <div class="kpi-card">
        <div class="kpi-value">42%</div>
        <div class="kpi-label">Growth Rate</div>
      </div>
    </div>
  </div>
</section>

<!-- Slide 2: Dark stat slide with giant numbers (different layout + mode) -->
<section class="slide dark" data-notes="Key metrics overview.">
  <div class="layout-title-body">
    <div class="title-area">
      <div class="tag">OBSERVATORY</div>
      <div class="h-md">Key Metrics</div>
    </div>
    <div class="body-area">
      <div class="layout-three-col">
        <div class="grid-item">
          <div class="split-stat">
            <div class="split-stat-number">512K</div>
            <div class="split-stat-body"><strong>Files</strong></div>
          </div>
        </div>
        <div class="grid-item">
          <div class="split-stat">
            <div class="split-stat-number">3</div>
            <div class="split-stat-body"><strong>Players</strong></div>
          </div>
        </div>
        <div class="grid-item">
          <div class="split-stat">
            <div class="split-stat-number">0%</div>
            <div class="split-stat-body"><strong>Innovation</strong></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Slide 3: Breathing quote (hero mode, center-narrow layout) -->
<section class="slide hero dark" data-notes="Pause to let the key message land.">
  <div class="layout-center-narrow">
    <div class="big-quote">
      <blockquote>"The best interface is no interface at all."</blockquote>
      <div class="cite">-- Golden Krishna</div>
    </div>
  </div>
</section>

<!-- Slide 4: Mosaic dashboard (back to light, different layout again) -->
<section class="slide light" data-notes="Dashboard combining chart with supporting insight.">
  <div class="layout-mosaic">
    <div class="mosaic-main">
      <div class="h-md">Adoption by Segment</div>
      <div class="bar-chart">
        <div class="bar-row">
          <div class="bar-label">Enterprise</div>
          <div class="bar-track"><div class="bar-fill" style="width:246px"></div></div>
          <div class="bar-value">82%</div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Mid-Market</div>
          <div class="bar-track"><div class="bar-fill" style="width:171px"></div></div>
          <div class="bar-value">57%</div>
        </div>
        <div class="bar-row">
          <div class="bar-label">SMB</div>
          <div class="bar-track"><div class="bar-fill" style="width:93px"></div></div>
          <div class="bar-value">31%</div>
        </div>
      </div>
    </div>
    <div class="mosaic-side">
      <div class="mosaic-item">
        <div class="kpi-card">
          <div class="kpi-value">92%</div>
          <div class="kpi-label">Satisfaction</div>
        </div>
      </div>
      <div class="mosaic-item">
        <div class="insight-box"><p>Enterprise adoption drives 70% of revenue growth.</p></div>
      </div>
    </div>
  </div>
</section>
```

Note the rhythm: light (two-col-wide) -> dark (title-body/three-col) -> hero dark (center-narrow) -> light (mosaic). Four consecutive slides, four different layouts, three mode changes, six different component types.

---

## 4. Image Composition in Canvas

| Goal | Use This | NOT This |
|------|----------|----------|
| Image + text side-by-side | `layout-split-hero` | Inline `<img>` mixed with text |
| Captioned image | `.img-frame` with `.img-caption` | Raw `<img>` without framing |
| Multiple images | `layout-four-grid` with `.img-frame` per `.grid-item` | Stacking raw images |

Rules: relative paths (`assets/`), max 70vh height, meaningful `alt` text, standard aspect ratios (16:9, 4:3, 3:2, 1:1), no slide chrome in generated images.

---

## 5. Theme-Specific Canvas Patterns

### editorial-magazine

Preferred classes: `.pull-quote` (oversized serif marks), `.big-quote` (serif italic), `.feature-card` (rounded corners), `.img-frame` (magazine caption), `.meta-row` (monospace). WebGL fluid/contour/dispersion on hero slides.

```
Cover (hero dark) -> Dark stat slide -> Light pillar cards (layout-three-col)
-> Light comparison (layout-comparison) -> Hero dark divider -> Light detail
(layout-two-col) -> Breathing (big-quote) -> Ending (hero dark)
```

### swiss-international

Preferred classes: `.kpi-card` (sharp rectangles, hairline borders), `.bar-chart` (single accent), `.compare-table` (grid-precise), `.pipeline` (1px connectors), `.stat-card` (type-scale only). WebGL fine grid on hero slides.

```
Cover (hero dark) -> Section divider -> Text+stat (layout-two-col-wide)
-> Three-column cards -> KPI dashboard -> Numbered items+image
-> Focus (hero light, big-quote) -> Ending (hero dark)
```

---

## 6. Speaker Notes Style

**Confident, measured** -- editorial clarity, not jargon. Present tense, active voice. One core message per slide in 2-4 sentences. Let the visual do the heavy lifting. Notes provide context the audience cannot see.

---

## 7. Quality Checklist

### P0 -- Must never violate
- [ ] Every `<section>` has `data-notes="..."` and mode class
- [ ] No `<style>`, `<script>`, `<link>`, or inline style outside the canonical data-geometry allowlist
- [ ] All CSS classes exist in `template.css` / `components.md`
- [ ] All images use relative `assets/` paths with `alt` text
- [ ] Browser-exported PNG/SVG output matches the intended composition
- [ ] Bar fills use permitted numeric geometry and match their labels/scales

### P1 -- Rhythm rules
- [ ] Repeated modes/layouts are intentional; hero and breathing slides serve the narrative.

### P2 -- Visual polish
- [ ] Inverse weight for swiss-international. Triple-font for editorial-magazine.
- [ ] WebGL backgrounds stay purposeful; component and layout choices serve the content without quota-filling.

### P3 -- Aesthetic excellence
- [ ] Apply the selected theme's visual-signature test. Vary a repeated layout only when repetition weakens comprehension or rhythm; comparisons and sequences may intentionally remain stable.

---

## 8. Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| All `layout-title-body` | Looks like a Word document | Mix layouts: two-col, mosaic, split-hero, three-col, hero |
| Inline `style="color:..."` | TCS violation | Use CSS classes from `template.css` |
| Mechanical same-layout repetition | Visual monotony | Keep repetition when it aids comparison or sequence; otherwise choose a structure that better fits the content |
| `border-radius` in swiss-international | Breaks Swiss geometry | Sharp rectangles only |
| Unmotivated flat mode rhythm | Weak emphasis | Change mode at meaningful transitions or focal moments; keep it stable when continuity benefits |
| Centered everything | No visual tension | Left-aligned; center ONLY for hero/focus |
| Sustained density causes fatigue | Weak pacing | Add a breathing page at a meaningful narrative pause |
| Unstable grid/flex sizing | Exported layout overflows | Add stable tracks, constraints, and overflow handling |
| `position: absolute` | Elements vanish in export | Flexbox alignment via layout classes |
| `flex: 1` on children | Width collapses to 0 | Explicit `width: Npx` or percentage |
| Serif in Swiss themes | Violates all-sans rule | Sans-serif exclusively |
| Drop shadows | Incompatible with editorial/Swiss | Depth via backgrounds + opacity only |
