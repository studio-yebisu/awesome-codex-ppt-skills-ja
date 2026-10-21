# Quality Checklist

This checklist captures real issues from iterative deck building. Every rule exists because it was violated and caused visible damage.

Run through this BEFORE delivery. P0 issues are blockers -- fix them or the deck is broken.

---

## P0 -- Must Fix (Breaks the Presentation)

### 0-1. Undefined CSS classes

**Symptom**: Components render as unstyled plain text or collapse into the wrong layout.

**Fix**: Cross-check every class against `template.css`. Add a reusable missing class to `template.css`; do not inline-style the workaround.

### 0-2. Content overflow or collision

**Symptom**: Text, images, or components are clipped, overlap unintentionally, or leave the canvas.

**Fix**: Edit the content or layout and inspect the rendered output. Split a slide when necessary; do not solve overflow by making text unreadably small.

### 0-3. Unresolved slide mode

**Fix**: Prefer `light`, `dark`, `hero light`, or `hero dark` on the slide. A
class may be omitted only when the selected theme's `theme.md` documents an
intentional default mode.

### 0-4. Missing speaker notes

**Fix**: Every `<section>` needs a non-empty `data-notes="..."` value. Notes should expand on slide content, not repeat it, and should include useful transitions where appropriate.

### 0-5. Broken required images

**Fix**: Verify every referenced relative path and required asset. Unused assets are not failures when the design spec records why they are irrelevant.

### 0-6. Forbidden inline style

**Fix**: Keep only numeric data geometry allowed by `shared-standards.md`. Put all other reusable visual rules in `template.css` and confirm with `validate_project.py`.

### 0-7. Forbidden tags or handlers

**Fix**: Remove `<style>`, `<script>`, `<link>`, and event-handler attributes from standard-slide `content.html`.

## Design Heuristics (Non-Blocking Individually)

- Review long runs of the same layout, mode, or density. Keep deliberate repetition when it supports comparison, sequence, or tutorial continuity.
- Use enough component vocabulary to express the material clearly, but do not add component types to reach a quota.
- Use theme signature elements purposefully; recognizability matters more than a fixed count or coverage percentage.
- Add breathing slides and section dividers at real narrative pauses, not at fixed page intervals.
- Replace repeated card grids when another representation communicates the content better.

---

## P1 -- Should Fix (Harms Quality)

### 1-1. Bullet list is hard to scan

**Review**: Recompose a list when its length, nesting, or line wrapping makes
the slide hard to scan. There is no universal item-count cutoff; a concise
six-item comparison can be clearer than four verbose bullets.

**Possible fixes**: Tighten wording, improve grouping, use an appropriate
grid/timeline/pipeline, or split the slide when the narrative supports it.

### 1-2. Topic title instead of action title

**Bad**: "Q3 Results" / "Architecture" / "Key Metrics"
**Good**: "Q3 revenue exceeded target by 18%" / "Microservices cut deploy from 4h to 12min"

**Exception**: Cover, section dividers, and ending slides may use thematic labels.

### 1-3. Theme-inappropriate component usage

**Symptom**: Components fight the theme personality.

**Fix by theme**:

| aurora-gradient violations | cyber-neon violations | data-dashboard violations |
|---------------------------|----------------------|--------------------------|
| Sharp corners (0 radius) | Rounded corners | Serif typography |
| Monochrome palettes | Light backgrounds | Large hero text |
| Hairline-only borders | Gradient fills | Decorative illustrations |
| Dense data grids | Warm tones | Gradient fills |

| editorial-magazine violations | ink-landscape violations | mckinsey-minimal violations | swiss-international violations |
|-------------------------------|-------------------------|----------------------------|-------------------------------|
| Dense 4-column grids | Neon colors | Neon glow effects | Serif fonts anywhere |
| Terminal-style monospace headings | Terminal chrome | Gradient fills | Rounded corners on any element |
| Brutalist thick borders | Dense data grids | Decorative illustrations | Gradient fills or drop shadows |
| Uniform symmetric layouts | Corporate blue palettes | Cultural motifs | Multiple accent colors |

| ivory-theorem violations | chalk-classroom violations | bloomberg-dark violations |
|--------------------------|---------------------------|--------------------------|
| Neon glow effects | Serif headings | Handwritten fonts |
| Gradient fills | Corporate precision | Chalkboard aesthetics |
| Terminal chrome | Ultra-clean minimalism | Gradient fills |
| Handwritten fonts | Financial data tables | Rounded corners |

### 1-4. Content is stranded at the top

**Symptom**: The title and meaningful body stop in the upper half while the
middle/lower field has no framing, continuation, or semantic anchor. A page
number, footer, or decorative line is the only element near the bottom.

**Fix**: Classify the page as centered cluster, top-to-bottom, split anchors,
image hero, or intentional breathing. Give the main region real height and
redistribute existing groups with semantic `gap`, grid tracks, vertical
centering, or `space-between`. Enlarge a real chart/table/process/media slot or
move an existing source/takeaway/status anchor only when the content supports
it. Do not add filler copy, empty cards, or spacer nodes.

---

## P2 -- Nice to Fix (Polish)

### 2-1. Inconsistent typography hierarchy

**Fix**: Establish consistent mapping: Cover title `.h-hero`, section divider `.h-xl`, content slide title `.h-md`, sub-headings `.h-sm`.

### 2-2. Too many colors on one slide

**Fix**: Remove colors without a communication or theme-identity role, then verify semantic palette use and contrast. Do not enforce a universal hue count.

### 2-3. Unclear separation between content groups

**Fix**: Correct the owning semantic container's `gap`, padding, or documented theme class. Avoid inserting arbitrary spacer elements as a default repair.

### 2-4. Code blocks without language class

**Fix**: Always specify language: `<pre><code class="language-python">...</code></pre>`

### 2-5. Density mismatch with rhythm tag

**Fix**: Match actual content density to the page's narrative role. An anchor
has a dominant focal claim, a breathing page uses deliberate negative space,
and a dense page still needs a navigable hierarchy. Do not infer these roles
from element counts or a universal occupancy percentage.

---

## P3 -- Suggestions (Optional Enhancements)

### 3-1. Transitional speaker notes

Speaker notes should include natural transition phrases: "Now let's look at...", "This leads us to...", "With that context..."

### 3-2. Use insight-box for key takeaways

When a slide has one critical insight buried in surrounding content, extract it into an `.insight-box`.

### 3-3. Match code block to slide mode

Light slides: default code blocks. Dark slides: use language classes that produce distinct highlighting.

### 3-4. Strengthen theme personality on weak slides

If individual slides pass structural checks but feel generic: add one more theme signature element, adjust component choice to better match theme preferences.

---

## Theme-Specific Checklists

### aurora-gradient

```
[ ] Gradient backgrounds appear on hero slides
[ ] All containers use 16px border-radius (rounded)
[ ] At least 1 gradient text element (.grad-text) per deck
[ ] Pill badges used for categories/CTAs
[ ] One gradient set used consistently (no mixing palettes)
[ ] Max 2 .grad-text elements per slide
[ ] Generous whitespace -- one hero element per slide
```

### cyber-neon

```
[ ] ALL slides use dark backgrounds (no light slide backgrounds)
[ ] Single neon accent color used throughout deck
[ ] Chrome headers (.chrome-top) on content slides
[ ] Zero border-radius on all containers
[ ] Neon glow reserved for one element per slide max
[ ] JetBrains Mono used for all metrics and numbers
[ ] Scan-line texture present on slides
```

### data-dashboard

```
[ ] Dashboard header (.dash-header) on content slides
[ ] Status badges use semantic colors (green/amber/red)
[ ] Metric cards use monospace values (JetBrains Mono)
[ ] Data tables use .data-table component
[ ] Bordered containers with 8px radius, no shadows
[ ] Compact layout -- data density is appropriate
[ ] Status dot indicators present in chrome
```

### editorial-magazine

```
[ ] Headings render in serif font (Playfair Display)
[ ] At least 1 pull-quote or big-quote per deck
[ ] Asymmetric column splits used (no 50/50 on all slides)
[ ] Caption text offset below-left of images
[ ] Mixed font families visible (serif + sans + mono)
[ ] WebGL background appears on hero slides only
[ ] Chinese titles max 5 characters with nowrap
[ ] Image grids use height:Nvh, never aspect-ratio
```

### ink-landscape

```
[ ] Rice paper cream backgrounds (not pure white)
[ ] Vermillion (zhu sha red) is the sole accent color
[ ] At least 1 seal stamp (.seal) per deck
[ ] Chinese numerals used for section numbering
[ ] Noto Serif SC used for headings
[ ] Verse blocks use LXGW WenKai kaishu calligraphy
[ ] Generous negative space throughout
[ ] Ink/paper duality maintained for dark slides
```

### mckinsey-minimal

```
[ ] DM Sans used for ALL text (no serif anywhere)
[ ] Executive summary bar (.exec-bar) on key slides
[ ] Single accent color -- max 2-3 accent touches per slide
[ ] Maximum whitespace with generous padding (6vh/6vw)
[ ] Top-down communication flow within slides
[ ] Insight cards with numbered labels
[ ] Action-oriented closing with numbered next steps
```

### swiss-international

```
[ ] ALL fonts are sans-serif (no serif anywhere)
[ ] Single accent color used throughout deck
[ ] No gradients, shadows, or border-radius > 0
[ ] Title-to-body font-size ratio >= 8:1
[ ] Large text uses ExtraLight weight (200)
[ ] Hairline dividers (1px) only -- no thick borders
[ ] Elements left-aligned with 30-40% whitespace
[ ] Sharp rectangles on all block elements
```

### ivory-theorem

```
[ ] Headings render in serif font (Playfair Display)
[ ] Body text uses Source Sans 3
[ ] Warm ivory (#FFFEF8) backgrounds (not pure white)
[ ] Navy (#1B2A4A) headings throughout
[ ] Crimson (#C62828) accents used sparingly for key terms
[ ] At least 1 theorem or definition block per deck
[ ] Citation callouts present for references
[ ] Generous margins evoking journal page layout
```

### chalk-classroom

```
[ ] Headings render in handwritten font (Caveat)
[ ] Chalkboard green (#1B2B1F) backgrounds on standard slides
[ ] Chalk white (#F5F0E8) text color
[ ] Yellow (#F4D35E) accents for highlights and annotations
[ ] Chalk-style dashed borders on card components
[ ] At least 1 annotation callout per deck
[ ] Whiteboard mode used for contrast slides
[ ] Inter used for body text readability
```

### bloomberg-dark

```
[ ] ALL slides use dark backgrounds (near-black #0F0F12)
[ ] Headings render in serif font (DM Serif Display)
[ ] Warm gray (#E8E4DF) text -- never pure white
[ ] Scarlet (#E63946) accent for critical data points
[ ] KPI cards use JetBrains Mono tabular numbers
[ ] Data tables use alternating row tints
[ ] Source citation blocks present for data provenance
[ ] Horizontal bar charts use scarlet fills
```

---

## Pre-Flight Checklist (Copy-Paste Before Delivery)

```
BEFORE writing content
  [ ] Read template.css -- confirmed all needed classes exist
  [ ] Rhythm plan done (every slide tagged: anchor / dense / breathing)
  [ ] Mode plan done (explicit mode or selected theme's documented default)
  [ ] Repeated modes/densities are intentional and content-driven
  [ ] Section dividers correspond to real narrative transitions
  [ ] Narrative arc planned (Hook -> Context -> Core -> Shift -> Takeaway)
  [ ] Theme signature elements selected purposefully

AFTER writing content
  [ ] Every slide has an explicit mode or the selected theme documents its default
  [ ] No <style>, <script>, <link> in content.html
  [ ] Inline styles conform to the canonical data-geometry allowlist
  [ ] Action titles on all content slides
  [ ] Non-empty speaker notes on every slide (data-notes)
  [ ] Repeated layouts are intentional; component vocabulary serves the content
  [ ] Lists remain scannable at the rendered size
  [ ] Images all load (relative paths, files exist)
  [ ] All class names verified against template.css
  [ ] Mode changes and breathing slides serve hierarchy and comprehension
  [ ] Repeated card grids are justified by the material
  [ ] Theme signature is recognizable without quota-filling
  [ ] Visual Signature Test passes (theme recognizable without color)
  [ ] Theme-specific checklist above passes
  [ ] Every browser PNG was inspected, not only overview suspects
  [ ] Every content page has an intentional vertical mode and no dead middle/lower field
  [ ] Footers and page numbers were not mistaken for body anchors
```
