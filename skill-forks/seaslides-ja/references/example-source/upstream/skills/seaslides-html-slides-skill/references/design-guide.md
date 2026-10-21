# Design Philosophy & Aesthetic Guide

Design standards for SeaSlides HTML Slides Skill -- ensuring presentations feel intentionally designed and professionally crafted.

Treat rhythm, diversity, and signature-element use in this guide as context-dependent heuristics. Compilation, readability, content accuracy, TCS, overflow, and export readiness remain hard requirements; do not damage a clear narrative merely to satisfy a visual quota.

---

## Contents

1. [The Five Laws](#1-the-five-laws)
2. [Theme Authority and Fidelity](#2-theme-authority-and-fidelity)
3. [Visual Signature Test](#3-visual-signature-test)
4. [Slide Rhythm](#4-slide-rhythm)
5. [Action Titles](#5-action-titles)
6. [Typography](#6-typography)
7. [Color and Space](#7-color-and-space)
8. [Anti-Patterns](#8-anti-patterns)
9. [Speaker Notes Craft](#9-speaker-notes-craft)
10. [Image Standards](#10-image-standards)
11. [Visual Direction and Continuity](#11-visual-direction-and-continuity)

---

## 1. The Five Laws

> Violate any of these and the presentation stops looking intentional.

1. **Distinctive, not generic.** Every presentation should have a visual identity reflecting its subject matter. If two unrelated presentations could swap themes without anyone noticing, the design has failed.

2. **Anti-AI-slop.** The most common failure mode is sameness: default palettes, symmetrical grids, decorative filler. Every design choice must be intentional and defensible. If you cannot explain WHY a component, color, or layout was chosen, remove it.

3. **Restraint over decoration.** A beautiful slide nobody can read is worse than a plain one. Contrast ratios matter. Font sizes matter. White space is not wasted space -- it is breathing room that makes content readable.

4. **Every element earns its place.** If a decorative element, icon, or colored block does not serve hierarchy, emphasis, or navigation -- delete it. No placeholder content. No "looks nice" additions.

5. **Content density matches audience capacity.** Expert audiences tolerate dense slides. General audiences need breathing room. Match the density to who is watching, not to how much you want to say.

### What "Intentional" Means in Practice

| Decision | Unintentional (Bad) | Intentional (Good) |
|----------|--------------------|--------------------|
| Color choice | "Blue looks professional" | "Blue matches the brand; accent orange highlights CTAs" |
| Layout | "Two columns because default" | "Two columns: left evidence, right conclusion" |
| Font size | "Same size for everything" | "4vw title, 2vw body: 2x ratio creates clear hierarchy" |
| Dark slide | "Variety" | "Dark here because the big number needs dramatic emphasis" |
| Icon | "Decoration" | "Arrow-right icon signals 'next step' in pipeline" |

---

## 2. Theme Authority and Fidelity

Use `${SKILL_DIR}/templates/index.json` as the only theme catalog. Once a theme is selected, its `theme.md`, `demo.html`, and copied project `template.css` own its typography, palette, geometry, components, supported modes, signature elements, variants, and image treatment. Do not maintain parallel per-theme profiles here.

For each slide, ask:

1. Are the visual choices supported by the selected theme contract?
2. Does each theme-native cue serve hierarchy, meaning, or navigation?
3. Could the slide move unchanged to an unrelated theme? If so, strengthen it with a small number of supported theme-native cues.
4. Is a needed treatment missing from the theme? Add a reusable project-local class to `template.css`; do not borrow another theme's class contract or use ad hoc inline styling.

Theme fidelity is structural, not decorative. A consistent grid, type hierarchy, component vocabulary, and image treatment matter more than repeating ornamental motifs.

---

## 3. Visual Signature Test

Replace the text with neutral blocks and ignore color. The composition should still express a coherent visual language through typography, grid, geometry, framing, component vocabulary, density, or image treatment.

If the slide feels generic, inspect the selected theme's `theme.md` and `demo.html`, then add one or two purposeful, supported cues. Do not treat signature elements as a coverage quota, and do not add decoration that weakens clarity.

---

## 4. Slide Rhythm

### The Three Rhythms

| Tag | Density | Purpose |
|-----|---------|---------|
| `anchor` | Low | Structural page -- cover, section divider, ending. Bold, simple, ceremonial. |
| `dense` | High | Information-rich -- grids, tables, KPIs, comparisons. The "work" of the deck. |
| `breathing` | Low | Narrative pause -- hero quote, single big number, full-bleed image. Resets attention. |

### Rhythm Heuristics

- **Consider alternating** dense and breathing slides when sustained density causes fatigue
- **Review 3+ consecutive** slides at the same density, but retain them when comparison or sequence benefits from consistency
- **Add section dividers** only at real narrative transitions
- **Opening and closing** deserve 2x the design attention of content slides
- **Use breathing slides** after dense passages when they improve comprehension

### Dark/Light Alternation

- Cover and section dividers -> `.dark` or `.hero dark` (ceremonial, bold)
- Content slides -> choose `.light` or `.dark` for readability and emphasis
- Key statements or big numbers -> `.dark` (dramatic emphasis)
- Review long same-mode runs, but keep them when a stable mode supports the material

---

## 5. Action Titles

Every slide title should be a complete sentence stating the slide's conclusion:

| Label Title (Avoid) | Action Title (Prefer) |
|---|---|
| Q3 Results | Q3 revenue exceeded target by 18% |
| Architecture | Microservices reduce deploy time from 4h to 12min |
| Market Overview | Southeast Asia mobile payments grew 3x |

**Exception**: Cover slides, section dividers, and ending slides may use short thematic labels.

---

## 6. Typography

### Font Roles

Use the font families and role assignments declared by the selected theme's `theme.md` and `template.css`. Do not copy roles from another theme or introduce arbitrary fonts. If a declared font is unavailable, preserve its broad category and hierarchy with the closest supported fallback, and record the project-local change in `template.css`.

### Size Hierarchy Must Be Unmistakable

Use the selected theme's semantic type tokens. The following is an illustrative
fallback scale when a theme does not define one; it is not a validator threshold:

| Level | Size | When to Use |
|-------|-----|-------------|
| `.h-hero` | 7-8vw | Cover title, ONE per deck |
| `.h-xl` | 4-5vw | Section dividers |
| `.h-md` | 2.4-3.5vw | Content slide titles (most slides) |
| `.h-sm` | 1.6-2vw | Sub-headings within a slide |
| Body `<p>` | ~2vw | Running text |
| `.meta-row` | ~1.2vw | Dates, attribution, metadata |

If two levels look the same size on screen, the hierarchy has failed.

### CJK Rules

- CJK text often needs more line height than comparable Latin text; calibrate it in the rendered theme
- CJK titles may need slightly smaller font-size to avoid overflow
- Templates include CJK fallback fonts -- do not add your own

### Weight Is a Delivery Token, Not a Fixed Style Rule

Small text often needs a little more weight to survive projection, browser rasterization, and mixed-script rendering; display text can often be lighter when the selected theme supports it. Make that decision through the theme's or project-local semantic typography tokens, with the delivery medium and language under review. Do not introduce a universal numeric weight, a Swiss-specific threshold, or a one-size-fits-all override in content HTML.

Themes that need automated review may opt in with their own CSS lengths: `--seaslides-audit-font-min-body`, `--seaslides-audit-font-min-code`, and `--seaslides-audit-font-min-label`. Assign `--seaslides-audit-font-role: body|code|label` only to the corresponding reusable text selectors. The browser audit emits a review item—not a blocker—when an opted-in role falls below that theme's floor. With no declared role/threshold, the check is disabled; never invent a global fallback.

---

## 7. Color and Space

### Color Rules

- Follow the selected theme's palette roles and contrast contract.
- Keep colors purposeful and repeatable. Multiple accents are valid when they encode distinct states or are part of the theme's visual identity.
- The 60-30-10 proportion can be a useful review heuristic for some restrained themes, but it is not a quota and does not override themes such as neo-bauhaus.
- Color should clarify hierarchy: primary text, emphasis/data roles, and muted supporting information must remain distinguishable.

### Whitespace Rules

- Use the theme's safe-area, navigation, title-gap, and component-gutter tokens; inspect browser output rather than enforcing a universal occupancy percentage.
- Keep meaningful content inside the theme's safe canvas. Full-bleed and edge-touching decorative fields are valid when the theme owns them.
- Preserve a readable title/body relationship using the theme's layout gap.
- Express group spacing through semantic container `gap`/padding or documented theme classes, not ad hoc spacer quota-filling.
- **Never fill every pixel.** A slide with 50% empty space and one strong statement is more effective than a slide packed with information.

### Vertical Composition Contract

Whitespace is useful only when it has a compositional job. Before styling a
content slide, choose one vertical mode and make the main region own the
available height (`flex: 1; min-height: 0` or an equivalent grid track):

| Mode | Use | Expected lower-page behavior |
|------|-----|------------------------------|
| Centered cluster | One statement, quote, or compact comparison | The cluster is optically centered; empty space frames it on both sides |
| Top-to-bottom | Tables, charts, processes, or stacked evidence | Existing rows/tracks use the main region and finish near the safe bottom |
| Split anchors | Opening claim plus conclusion, source, status, or next action | Both anchors carry information; the space between them creates hierarchy |
| Image hero | One dominant image with a short text block | The image supplies visual weight through the lower region |
| Intentional breathing | Cover, divider, or closing page | Sparsity is the page's role and has a clear focal point |

A content page is top-heavy when its meaningful group stops in the upper half
and the remaining middle/lower field neither frames a focal statement nor leads
to a real anchor. A footer, page number, or decorative rule does not by itself
repair that composition.

Use this correction ladder, stopping as soon as the page balances:

1. Give the owning body container a real height instead of natural top-packed height.
2. Redistribute existing semantic groups with `gap`, grid tracks, vertical centering, or `justify-content: space-between`.
3. Increase the useful height of an existing chart, table, process, media slot, or card row while preserving readability.
4. Move an existing source, takeaway, status, or action into a lower anchor when that relationship is semantically true.
5. Change the page family or split the page when the content cannot support the current composition.

Do not add filler copy, empty cards, arbitrary spacer nodes, or exaggerated
font sizes merely to consume space. Theme-owned DOM geometry measurements are
review evidence, not universal quotas; the selected theme and page role still
own the judgment.

For a page family that is expected to use its vertical body region, the theme
may opt into a mechanical review contract:

```html
<section class="slide light" data-audit-composition="top-to-bottom">
  <main class="content-frame" data-audit-content>...</main>
  <footer data-audit-chrome>...</footer>
</section>
```

```css
.slide[data-audit-composition="top-to-bottom"] {
  --seaslides-nav-safe-bottom: 6vh;
  --seaslides-audit-bottom-gap-max: 18vh;
  --seaslides-audit-active-height-min: 0.58;
  --seaslides-audit-vertical-gap-max: 24vh;
}
```

The browser audit resolves CSS lengths to canvas pixels. It emits only a
review item, never a blocker: top-heavy review requires both excessive bottom
gap and insufficient active height, while the internal-gap check runs only
when its optional threshold is present. Without explicit `top-to-bottom` mode and a
`data-audit-content` root, the metrics are observation-only. Chrome remains in
overflow and clipping checks even when it is excluded from composition.

### Whitespace Anti-Patterns

| Bad | Fix |
|-----|-----|
| Meaningful content outside the safe canvas | Restore the selected theme's safe-area geometry |
| Title/body collision or unclear separation | Correct the owning layout gap and verify the browser render |
| Cards touching each other | Use flex gap |
| Content packed at the top with a dead middle/lower field | Recompose the existing groups inside a height-owning main region; use a real lower anchor only when the content provides one |
| Footer used to disguise an otherwise top-heavy page | Exclude persistent chrome from balance judgment and fix the body composition |

---

## 8. Anti-Patterns

### Visual Monotony (The Enemy)

Monotony is the unmistakable signature of auto-generated content:

- Same layout on every slide without a comparison or sequence rationale
- No contrast or mode change where hierarchy needs it
- Uniform heading sizes
- Every card identical dimensions
- Same component type repeated mechanically where another form would communicate better

**The monotony test**: Shuffle all content slides randomly. If the deck feels the same in any order, it lacks rhythm and variety.

### Anti-AI-Slop Checklist

Before declaring a deck done, verify these are NOT true:

- [ ] Every slide looks interchangeable
- [ ] Color palette is "default" with no relationship to content
- [ ] Decorative elements serve no hierarchy purpose
- [ ] All slides have the same density (no rhythm)
- [ ] Opening slide could belong to any presentation
- [ ] Bullet points are generic statements
- [ ] No specific data, names, dates, or concrete details
- [ ] Theme signature elements are absent
- [ ] Component choices feel mechanically narrow for the content
- [ ] Repeated layouts lack a comparison or sequence rationale
- [ ] Deck could pass as any other theme (lacks identity)

**Diversity review prompts** for a finished deck of 8+ slides:
- Does the deck use enough component and layout variation to avoid accidental monotony?
- Are mode changes tied to hierarchy or emphasis rather than an arbitrary cadence?
- Do breathing and dense slides reflect the narrative needs?
- Is the theme recognizable through a few purposeful signature elements?

---

## 9. Speaker Notes Craft

Speaker notes are NOT slide captions. They are presenter coaching tools.

### What Good Notes Include

- **Opening hook**: How to introduce this slide
- **Emphasis markers**: What to stress, where to pause
- **Data context**: Numbers not on the slide that support the point
- **Transition phrase**: Exact words to bridge to the next slide
- **Timing cues**: "Spend 90 seconds here" or "Quick -- 30 seconds"

### What Notes Should NOT Be

- A repetition of bullet points on the slide
- A full script (too long to glance at)
- Empty or one-word notes
- Generic phrases like "Explain this slide"

---

## 10. Image Standards

### When to Use Images

- Screenshots of actual products/interfaces (evidence)
- Diagrams that explain structure or flow (clarity)
- Data visualizations too complex for CSS components

### When NOT to Use Images

- Generic stock photos (adds nothing, screams "AI-generated deck")
- Decorative illustrations with no information content
- Low-resolution or watermarked images

### Image Sizing Rules

- Preserve the source evidence and match the target slot; common ratios are useful defaults, not an allowlist
- Images must fit within their container -- never overflow
- Use `<figure class="img-frame">` when the theme documents it and a captioned/framed figure is semantically appropriate
- Size images within the theme's safe title/body/footer geometry; verify the rendered canvas instead of applying a universal height cap
- Use local relative `assets/` paths for deterministic delivery; remote assets require an explicit acquisition step before build

### Theme-Specific Image Treatment

Follow the selected theme's `theme.md`, `demo.html`, and `template.css` for cropping, framing, grid alignment, corner treatment, shadows, and image prominence. Keep these rules with the theme instead of duplicating them in this shared guide.

## 11. Visual Direction and Continuity

The content design specification must state a **Visual Direction** before execution: the visual premise, the recurring image treatment, the type/contrast posture, and the planned transitions between sections. Treat it as a cross-page contract, not a request to make every slide identical.

For each slide, preserve continuity deliberately: carry forward a meaningful cue (for example, a photo treatment, alignment edge, accent behavior, or evidence-to-conclusion relationship) and change it only when the narrative transition warrants a reset. Covers, dividers, and emphasis slides may break the pattern on purpose; record why in the outline.

A quick workflow may reduce interactive decision rounds or exploratory variants, but it never removes the source, build/assembly, validation, or final visual gates. Review the settled browser output and inspect the SVG route when framing or export equivalence could change delivery.

### Image Composition Grammar: P / M / A / C

Use P/M/A/C as a compact description of composition responsibilities when an image-led page benefits from it. It is not a taxonomy that assigns one letter to every image, and it is not a page or deck quota.

| Layer | Responsibility | Typical HTML realization |
|---|---|---|
| **P — Primary Structure** | Define the page skeleton: one visual field, image-as-canvas, comparison, or multi-visual system | Theme-owned split, full-bleed, figure, comparison, or gallery classes |
| **M — Modifier Layer** | Add only the crop/reveal, tone/focus, framing, placement, or depth treatment that the skeleton needs | Theme-owned crop, scrim, frame, focus, or restrained depth modifier |
| **A — Asset-Dependent Treatment** | Use a prepared local composite, cutout, or registered derivative that cannot be reconstructed faithfully as ordinary HTML layout | Verified transparent cutout, precomposited treatment, or registered derivative |
| **C — Cross-Page Continuity** | Preserve a deliberate visual relationship across slides | Stable source/crop, progressive annotations, camera movement, or matched framing |

Start with the smallest useful P structure, add M only for a named communication job, use A only when the required prepared asset exists, and use C only for an intentional cross-page relationship. A free-form composition is valid when it communicates better; catalog identifiers and family coverage are never required.
