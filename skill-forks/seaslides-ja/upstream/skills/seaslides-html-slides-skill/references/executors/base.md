# Executor Common Guidelines

> Base execution rules for ALL executors (general and academic). Covers workflow, slide type mapping, and content construction rules. Theme-specific CSS rules and component documentation live in `shared-standards.md`, `components.md`, and `layouts.md`.

---

## 1. Template-Content Separation (TCS)

> Full specification: See `shared-standards.md` Section 1.

### The Golden Rules

1. **NEVER** put `<style>`, `<script>`, or `<link>` tags in content.html
2. Use inline `style="..."` only for numeric data geometry on the class/property allowlist in `shared-standards.md`
3. **ALWAYS** use CSS classes defined in the project's `template.css`
4. If a class you need does not exist in `template.css`, **add it to template.css** -- do not inline-style the workaround

---

## 2. Phased Content Generation

### Phase 1: Pre-Check

Before writing a single line of content.html:

1. **Read `content_design_spec.md`** -- understand every slide requirement
2. **Read `template.css`** -- know every available CSS class
3. **Read theme's `theme.md`** -- understand theme-specific component patterns
4. **Read theme's `demo.html`** -- see structural reference for component usage and density
5. **Verify image availability** -- if images are listed, confirm they exist in `assets/`
6. **Plan rhythm and composition** -- mark each slide as anchor/dense/breathing, assign dark/light mode, and choose centered cluster, top-to-bottom, split anchors, image hero, or intentional breathing

### Phase 2: Skeleton

Write content.html with all `<section>` elements, each containing:
- Correct `class="slide [mode]"` with mode class
- `data-notes="..."` placeholder (can be brief initially)
- Correct layout `<div>` wrapper
- `data-audit-composition="top-to-bottom"` plus a `data-audit-content` body only when the selected theme defines that composition contract
- Heading with appropriate `.h-*` class

### Phase 3: Fill

Add components and content to each slide:
- Follow the design spec's component assignments
- Apply one idea per slide
- Use action titles (conclusions, not topic labels)
- Keep bullets scannable at the rendered size; regroup or split when wording and nesting make them hard to follow
- Use consistent numeric chart geometry and verify that fills match labels and scales

### Phase 4: Polish

- Review every slide against the checklist (`checklist.md`)
- Add complete speaker notes to every slide
- Review mode and layout repetition in narrative context
- Review whether component choices fit the content; do not add components to satisfy a quota

---

## 3. Slide Type Mapping

| Type | Mode | Layout | Vertical Mode | Components | Notes |
|------|------|--------|---------------|------------|-------|
| **Cover** | `hero dark` | `layout-hero-center` | Intentional breathing / image hero | `.h-hero`, `.meta-row` | Title, subtitle, author, date |
| **Section divider** | `hero dark` or `hero light` | `layout-hero-center` | Centered cluster / intentional breathing | `.h-xl` | Section name only; use a mode change only when it serves hierarchy |
| **Content (text)** | `light` or `dark` | `layout-title-body`, `layout-two-col` | Top-to-bottom / split anchors | `.h-md`, lists, `.insight-box` | Action title required |
| **Content (data)** | `light` or `dark` | `layout-three-col`, `layout-full-width` | Top-to-bottom | `.kpi-card`, `.bar-chart`, `.stat-card` | Let real charts/tables/cards carry the main region |
| **Content (process)** | `light` or `dark` | `layout-full-width`, `layout-title-body` | Top-to-bottom | `.pipeline`, `.timeline`, `.roadmap` | Keep steps legible; split only when the rendered sequence becomes cramped |
| **Breathing** | `dark` or `hero light` | `layout-hero-center`, `layout-center-narrow` | Centered cluster / intentional breathing | `.big-quote`, `.split-stat` | Minimal content with a clear focal point |
| **Ending** | `hero dark` | `layout-hero-center` | Centered cluster / intentional breathing | `.h-hero` | Closing statement, CTA, or thank you |

---

## 4. Content Construction Rules

### Slide Structure Template

```html
<section class="slide [mode]" data-notes="Speaker notes here">
  <div class="[layout-class]">
    <div class="title-area">
      <div class="h-md">Action Title: States the Conclusion</div>
    </div>
    <div class="body-area">
      <!-- Components from components.md -->
    </div>
  </div>
</section>
```

For a top-to-bottom page whose theme supplies composition thresholds, add
`data-audit-composition="top-to-bottom"` to the slide and `data-audit-content` to its
main layout wrapper. Omit `fill` for covers, quotes, dividers, closings,
centered clusters, and split-anchor pages unless the theme documents a specific
contract. Persistent footer/navigation chrome may use `data-audit-chrome`; it
remains subject to overflow and clipping checks.

### Resolved Mode (Required on Every Slide)

Prefer one of these explicit classes:
- `light` -- light background, dark text
- `dark` -- dark background, light text
- `hero light` -- centered light background
- `hero dark` -- centered dark background

A slide may omit an explicit mode only when the selected theme's `theme.md`
documents its default. Preserve documented theme-specific modifiers such as
`surface`, `accent`, or `whiteboard` rather than replacing them with a generic
mode solely to satisfy a checklist.

### Speaker Notes (Required on Every Slide)

Every `<section>` MUST have a non-empty `data-notes="..."` value. Notes should:
- Expand on slide content (not repeat it)
- Include transition phrase to next slide
- Include timing cues where appropriate
- Contain presentation-specific context

### Bar Chart Geometry

Use percentage fills for normalized tracks, or use pixels only when the
selected component documents a fixed track. For a documented 300px track:

```
pixel_width = percentage_value * 300 / 100

82% -> 82 * 300 / 100 = 246px
45% -> 45 * 300 / 100 = 135px
100% -> 100 * 300 / 100 = 300px
```

For a component with a documented 200px vertical track:
```
pixel_height = percentage_value * 200 / 100
```

---

## 5. Theme-Specific Content Rules

### editorial-magazine

- Headings MUST render in serif font. If they show as sans-serif, the class is missing.
- Image grids use `height:Nvh`, never `aspect-ratio` (which can overflow).
- Chinese titles: max 5 characters with `nowrap` to prevent 1-character-per-line breaks.
- Font division: serif = titles, sans-serif = body, monospace = metadata.
- Asymmetric column splits preferred (30/70, 40/60). Avoid 50/50.
- WebGL backgrounds appear on hero slides only.

### swiss-international

- ALL sans-serif, always. Any serif font appearance is an error.
- Single accent color per deck. Never mix multiple highlight colors.
- No gradients, no shadows, no `border-radius` > 0. All blocks are sharp rectangles.
- Extreme font-size contrast: title-to-body ratio >= 8:1.
- Large text uses weight 200 (ExtraLight); small text uses weight 400-600.
- All elements snap to 12-column grid. Left-aligned with generous whitespace.
- Hairline dividers (1px) only. No thick borders.

---

## 6. Image Usage Rules

- Every relevant or user-required image in `assets/` appears where it supports the narrative; record why material source images were omitted
- Group or distribute images according to the story rather than an even-spread quota
- All paths relative: `src="assets/filename.ext"`
- No external URLs, no absolute paths
- Match the source and target-slot aspect ratios; use crop-safe `cover` only when evidence is preserved
- Size images within the theme's safe canvas and title/footer geometry; no universal height cap replaces rendered inspection
- Use `.img-frame` when the selected theme documents it and semantic framing is appropriate
- Include meaningful `alt` text

---

## 7. Post-Generation Checklist

After writing content.html:

```
[ ] Every slide has an explicit mode or a documented theme default
[ ] Every slide has non-empty data-notes
[ ] No <style>, <script>, <link> tags
[ ] Inline styles conform to the canonical data-geometry allowlist
[ ] All CSS classes verified against template.css
[ ] Action titles on all content slides
[ ] Repeated layouts and modes are intentional
[ ] Component vocabulary serves the content without quota-filling
[ ] Lists remain scannable at the rendered size
[ ] Images use relative assets/ paths
[ ] Density changes support narrative rhythm; deliberate dense sequences are allowed
[ ] Every slide's vertical mode is intentional; content pages are not stranded at the top
[ ] A footer/page number is not being mistaken for a lower content anchor
[ ] Every direct-browser PNG was inspected before final sign-off
```
