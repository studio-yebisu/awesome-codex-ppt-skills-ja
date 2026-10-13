# Image-Text Layout Patterns

A vocabulary registry of ways images can be placed on HTML slides. The point of this file is to **expand the mental list of options** so that when you reach for an image layout, you do not default to the same three patterns (left/right, top/bottom, full-width hero).

Every entry has a name plus a short technical hint in HTML/CSS syntax. This is a registry, not a teaching document; no use-case prescriptions or coverage requirements.

> **Numbers are local browse anchors, not a cross-backend contract.** They help locate existing entries in this file, but a content plan does not need to cite them and an exporter never maps them to fixed geometry. Plan image-led pages by composition responsibility: **P** primary structure, useful **M** modifier layers, prepared **A** asset-dependent treatments, and intentional **C** cross-page continuity. A free-form theme-owned composition remains valid.

---

## Image Fundamentals (HTML `<img>` Reference)

### Basic Usage

```html
<!-- Simple image inside a component -->
<div class="img-frame">
  <img src="assets/photo.jpg" alt="Description of the image">
</div>

<!-- Image inside a layout column -->
<div class="col-right">
  <img src="assets/diagram.png" alt="System architecture diagram">
</div>

<!-- Image with caption -->
<figure class="img-frame">
  <img src="assets/chart.png" alt="Revenue growth chart">
  <figcaption class="img-caption">Quarterly revenue growth 2024-2025</figcaption>
</figure>
```

### Key HTML Attributes

| Attribute | Required | Purpose |
|-----------|----------|---------|
| `src` | Yes | Path to image file (always relative: `assets/filename.ext`) |
| `alt` | Yes | Accessibility description of the image |

### CSS Sizing via Component Classes

Image sizing is controlled by CSS classes in `template.css`, NOT by `width`/`height` attributes on the `<img>` element. The theme's component and layout classes handle dimensions.

```css
/* In template.css -- image sizing handled by container */
.img-frame img {
  width: 100%;
  height: auto;
  display: block;
}

/* Image in a flex column -- fills available width */
.col-left img,
.col-right img {
  width: 100%;
  height: auto;
  object-fit: cover;
}
```

### `object-fit` and `object-position` Rules

These CSS properties control how images fill their containers:

| Property | Value | Behavior | Use Case |
|----------|-------|----------|----------|
| `object-fit: cover` | Fills container, crops overflow | Hero images, backgrounds, editorial photos |
| `object-fit: contain` | Fits entire image, may leave whitespace | Diagrams, screenshots, charts |
| `object-fit: fill` | Stretches to fill exactly | Rarely appropriate (distorts) |
| `object-position: center` | Centers crop point | Default -- works for most photos |
| `object-position: top` | Crops from bottom | Portraits, headshots |
| `object-position: left center` | Crops from right | Subjects on the left side |

```css
/* Hero image: fill and crop */
.layout-split-hero .split-visual img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* Diagram: contain without distortion */
.img-frame.contain img {
  width: 100%;
  height: auto;
  object-fit: contain;
}
```

### Browser Export Image Constraints

The browser exporter resolves images through Chromium and serializes the rendered slide. Follow these rules for deterministic batch output:

1. **Container should have stable dimensions**: The parent flex/grid container or component class should define predictable width/height constraints.
2. **Use `object-fit` in CSS classes, not on the img element**: Keep sizing behavior centralized in the template.
3. **Avoid `width` and `height` HTML attributes on `<img>`**: Let CSS classes control sizing.
4. **Prefer `<img>` for semantic images**: Use CSS backgrounds for decoration only, and keep URLs local/data-backed.
5. **File format**: PNG and JPEG work reliably. SVG-as-`<img>` works. Avoid WebP and GIF.

### Pixel Width Requirements

When images need specific dimensions inside dense layouts, the **parent container** should provide stable sizing:

```html
<!-- GOOD: parent container has explicit width via layout class -->
<div class="col-left">  <!-- width: 480px in CSS -->
  <img src="assets/photo.jpg" alt="Photo">
</div>

<!-- RISKY: no stable width context for long adjacent content -->
<div class="col">
  <img src="assets/photo.jpg" alt="Photo">
</div>
```

---

## Core Principle -- Two Layers

Almost every pattern below is an instance of one underlying split:

> **The image carries atmosphere, world-building, emotional weight. HTML elements carry information, data, editable text.**

The default reflex is to place image and text in adjacent columns. The far more powerful move -- especially for content-rich slides -- is to let the image occupy the background of a hero slide while semantic HTML elements (cards, stats, labels) float above it.

Anything that must be editable, numerically accurate, contain CJK text, or be styled to the deck's exact theme tokens belongs in the HTML layer regardless of what the image shows.

### Choosing the Right Mechanism

| Goal | Idiomatic Approach | NOT This |
|------|-------------------|----------|
| **Image + text side-by-side** | `layout-split-hero` or `layout-two-col` with `<img>` in one column | Baking text into the image |
| **Image as slide background** | Hero slide with `<img>` filling the `.split-visual` area | Remote CSS backgrounds that can fail in batch |
| **Image in a card** | `<img>` inside `.img-frame` component | `background-image` on a div |
| **Multiple images in grid** | Grid or flex layouts with `<img>` in each item | Unconstrained image children |
| **Image with text overlay** | `<img>` in a positioned container + text elements above | Baking text into the image |

---

# Part 1 -- Primary Structures

Pick one or more of these as the slide's bones. Cross-primary combinations are encouraged (see Composition Guidance).

## Container Layouts (where the image sits)

1. **Full-width hero image with centered title** -- `layout-split-hero` or `layout-hero-center` with large image in visual area, title/subtitle overlaid. The image fills the visual half; text sits on the content half or overlays the image with a scrim effect.

2. **Left-third image + right text body** -- `layout-two-col` with `<img>` in `.col-left`, text in `.col-right`. Image occupies approximately 40% width.

```html
<div class="layout-two-col">
  <div class="col-left">
    <img src="assets/product.jpg" alt="Product photo">
  </div>
  <div class="col-right">
    <div class="h-sm">Product Overview</div>
    <p>Key features and benefits described here...</p>
  </div>
</div>
```

3. **Right-third image + left text body** -- Mirror of #2: text in `.col-left`, image in `.col-right`.

4. **Split hero (50/50)** -- `layout-split-hero` with `.split-visual` and `.split-content` at equal widths.

```html
<div class="layout-split-hero">
  <div class="split-visual">
    <img src="assets/hero.jpg" alt="Hero image">
  </div>
  <div class="split-content">
    <div class="h-md">Title Here</div>
    <p>Description text goes here.</p>
  </div>
</div>
```

5. **Top-band image + bottom multi-column text** -- Image strip in a banner area (via `layout-banner-body`), text content in body below.

6. **Bottom-band image + top title + middle text** -- Mirror of #5 with image at the bottom of the slide.

7. **Top-and-bottom symmetric split** -- Image occupies 50% (top), content occupies 50% (bottom). Uses `layout-stacked-thirds` with two rows.

8. **Z-pattern serpentine** -- Three rows alternating image left/right. Use `layout-stacked-thirds` with each `.stack-row` containing a two-column flex arrangement that alternates direction.

9. **Centered image with surrounding text** -- `layout-mosaic` with `.mosaic-main` holding the image and `.mosaic-side` items holding text blocks.

10. **Centered image with callout annotations** -- Image in center of slide, text labels positioned around it. Use `layout-center-narrow` with the image and annotation elements.

11. **Diagonal composition (image + gradient)** -- `layout-split-hero` with `.split-visual` holding the image and CSS gradient overlay on the theme level creating a diagonal visual boundary.

12. **Faded image as backdrop with oversized text** -- Hero slide with image in visual area + large `.h-hero` text overlay. Theme CSS applies opacity treatment.

13. **Narrow vertical image strip + wide title** -- `layout-two-col` with narrow left column (via `layout-sidebar`) for image, wide right for large display text.

14. **Horizontal banner strip cutting mid-section** -- `layout-banner-body` with image in the `.banner` area spanning full width.

15. **Multi-image montage with text band** -- Multiple images in `layout-three-col` or `layout-four-grid`, with a `callout-banner` or text row spanning below.

16. **Negative-space dominant -- small image, mostly whitespace** -- `layout-center-narrow` with a single small image and minimal text. Rest is breathing room.

17. **Picture-in-picture inset** -- Main content slide with a small `.img-frame` positioned in one corner. Use `layout-mosaic` with the main content in `.mosaic-main` and the small image in a `.mosaic-item`.

18. **Image as full-height sidebar** -- `layout-sidebar` with image filling the `.sidebar` column and text in `.main-content`.

19. **Image floating in whitespace with thin frame and caption** -- `layout-center-narrow` containing a single `<figure class="img-frame">` with `<figcaption>`.

## Image-as-Background + Content Overlay

The shared pattern: image fills the visual area of a hero slide; semantic HTML components are placed alongside or overlaid.

> **Common structure for #38-#46**: `layout-split-hero` with image in `.split-visual`, content elements in `.split-content` -- or a hero dark slide with the image providing atmosphere.

38. **Hero image + annotation cards** -- `layout-split-hero` with image on one side; 2-4 `.feature-card` or `.kpi-card` elements on the content side. Each card highlights a region or detail of the image.

39. **Hero image + flow/pipeline overlay** -- Hero slide with image background. Content side contains a `.pipeline` component showing process steps related to what the image depicts.

40. **Hero image + floating KPI cards** -- `layout-split-hero` with image in visual area. Content area contains 3-4 `.kpi-card` components displaying metrics.

41. **Hero image + measurement annotations** -- Hero slide with image. Content side uses a `.numbered-list` or `.definition-list` to annotate specific aspects of the image.

42. **Hero image + translucent panels** -- Dark hero slide with image. Content elements use theme dark-mode card styling (semi-transparent backgrounds via `.slide.dark .kpi-card` CSS).

43. **Hero image + data visualization** -- `layout-split-hero` with image on one side and `.bar-chart` or `.vbar-chart` on the content side.

44. **Hero image + architecture/flow diagram** -- `layout-split-hero` with image in visual area and `.pipeline` or `.timeline` in content area.

45. **Hero image + numbered hotspot legend** -- Image on one side, `.numbered-list` on the other side serving as a legend for numbered points of interest in the image.

46. **Hero image + highlight callout** -- `layout-split-hero` with image and a single `.insight-box` or `.callout-banner` on the content side.

## Multi-Image Compositions

47. **Small multiples -- 3-6 same-kind images** -- `layout-three-col` with each `.grid-item` containing an `<img>` and caption. Identical framing communicates comparison.

```html
<div class="layout-three-col">
  <div class="grid-item">
    <div class="img-frame">
      <img src="assets/sample-a.png" alt="Sample A">
      <div class="img-caption">Version A</div>
    </div>
  </div>
  <div class="grid-item">
    <div class="img-frame">
      <img src="assets/sample-b.png" alt="Sample B">
      <div class="img-caption">Version B</div>
    </div>
  </div>
  <div class="grid-item">
    <div class="img-frame">
      <img src="assets/sample-c.png" alt="Sample C">
      <div class="img-caption">Version C</div>
    </div>
  </div>
</div>
```

48. **Side-by-side comparison (before/after, A/B)** -- `layout-comparison` or `layout-two-col` with one image per column and labels.

```html
<div class="layout-comparison">
  <div class="compare-left">
    <div class="h-sm">Before</div>
    <div class="img-frame">
      <img src="assets/before.png" alt="Before state">
    </div>
  </div>
  <div class="compare-divider"></div>
  <div class="compare-right">
    <div class="h-sm">After</div>
    <div class="img-frame">
      <img src="assets/after.png" alt="After state">
    </div>
  </div>
</div>
```

49. **Asymmetric collage** -- `layout-mosaic` with one large image in `.mosaic-main` and 2-3 smaller images in `.mosaic-item` elements.

50. **Tiled grid (2x2)** -- `layout-four-grid` with each `.grid-item` containing an `<img>` element.

51. **Mosaic (mixed sizes)** -- `layout-mosaic` with varying image sizes between `.mosaic-main` and `.mosaic-side`.

52. **Image strip / filmstrip** -- `layout-three-col` or wider with thin gap between images, all same height. Each `.grid-item` contains an image cropped via `object-fit: cover`.

53. **Vertical image stack** -- `layout-stacked-thirds` with each `.stack-row` containing a single full-width image.

54. **Overlapping image composition** -- Supported by browser export when the positioning is stable. Test PNG and PPTX output if editability matters.

55. **Diptych split** -- `layout-two-col` with each column containing one image at equal size.

56. **Image triptych** -- `layout-three-col` with three images side-by-side.

---

# Part 2 -- Modifier Layers

Stack any of these freely on top of a Primary structure. Multiple Modifiers per slide is the expected case.

## Image Shape Treatments

20. **Circular crop** -- Apply via CSS class in `template.css`:

```css
.img-circle img {
  border-radius: 50%;
  overflow: hidden;
  object-fit: cover;
}
```

```html
<div class="img-frame img-circle">
  <img src="assets/portrait.jpg" alt="Headshot">
</div>
```

21. **Rounded rectangle crop** -- CSS `border-radius` on the image container:

```css
.img-rounded img {
  border-radius: 8px;
  overflow: hidden;
}
```

> **swiss-international**: Do NOT use rounded corners. Set `border-radius: 0` on all image containers.

22. **Pill/ellipse shape** -- Use generous `border-radius` (e.g., `50%` on a non-square container).

23. **Sharp corners (Swiss style)** -- Explicit `border-radius: 0` on image containers. Default for swiss-international.

24. **Transparent PNG cutout** -- PNG with alpha channel placed via `<img>`. Transparency renders natively in browser, SVG export, and PPTX.

25. **Image with colored matte frame** -- CSS border on the `.img-frame`:

```css
.img-frame.matte img {
  border: 3px solid var(--accent-primary);
}
```

26. **Image with thin hairline frame** -- 1px border for swiss-international:

```css
.img-frame.hairline img {
  border: 1px solid var(--border-light);
}
```

## Overlay and Masking Treatments

27. **Gradient scrim for text legibility** -- CSS gradient on a dark hero slide provides text contrast. Handled in `template.css`:

```css
.slide.hero.dark .split-visual::after {
  /* Pseudo-elements are fine for decorative export effects. */
  /* Use a real element if the overlay needs to be inspectable/editable in PPTX. */
}

/* Editable/PPTX-friendly alternative: use a scrim div */
.scrim-overlay {
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0) 100%
  );
}
```

> **Export note**: pseudo-elements render in Chromium export, but real overlay elements are easier to inspect and convert in PPTX.

28. **Color-tinted overlay** -- A semi-transparent colored div over the image that pushes toward the theme palette:

```html
<div class="split-visual">
  <img src="assets/photo.jpg" alt="Background">
  <div class="color-overlay"></div>
</div>
```

```css
.color-overlay {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(37, 99, 235, 0.15);  /* accent-primary at 15% */
}
```

> **Note**: absolute overlays are supported. Test exported PNG/SVG/PPTX output for complex stacks.

29. **Dark scrim band at bottom** -- Horizontal gradient band for text readability over image bottom.

30. **Flat semi-transparent overlay** -- Uniform opacity reduction on image.

31. **Duotone treatment** -- Must be baked into the source image at generation time. Request in the image generation prompt.

## Image as Texture / Atmosphere

57. **Full-bleed image at low opacity as background texture** -- Hero slide with image providing subtle atmospheric texture. The image is visible but the theme's dark/light background color dominates.

58. **Small decorative image in corner** -- Small `.img-frame` positioned in one corner of the slide, not the focus, just visual seasoning. Use `layout-mosaic` with a small `.mosaic-item`.

59. **Image as horizontal divider** -- Narrow landscape image used between text sections as a visual break.

60. **Image as ambient atmosphere** -- Low contrast, mood-setting image. Same as #57 but on a light slide.

## Special Techniques

62. **Same image, two sizes -- overview + detail zoom** -- Reference the same image file twice: once in a `.grid-item` at small size, once in the main area at larger size. Creates a zoom-callout effect.

63. **Transparent PNG sticker / cutout** -- RGBA PNG with transparent background. Use for product shots, icons, or subjects that should float over the slide background.

64. **Image with text overlay** -- Image in visual area; text elements (`.h-md`, `.kpi-card`, etc.) positioned in the content area adjacent to the image. Never bake text into the image.

65. **Image with NO embedded text** -- All labels, numbers, and annotations are HTML elements. Generate images with "no text, no letters, no numbers" instruction.

66. **Image fading into slide background** -- Simulated via CSS gradient overlay that matches the slide's `background-color`.

67. **Image with border frame (editorial style)** -- Warm editorial framing:

```css
/* editorial-magazine: warm frame with caption below */
.img-frame.editorial {
  border: 2px solid var(--border-light);
  border-radius: 4px;
  padding: 4px;
  background: var(--bg-light);
}
```

68. **Image with caption offset below-left (magazine style)** -- Editorial-magazine specific:

```html
<figure class="img-frame editorial">
  <img src="assets/scene.jpg" alt="Scene description">
  <figcaption class="img-caption">Caption text aligned left</figcaption>
</figure>
```

---

## Per-Theme Image Treatment Rules

### aurora-gradient

| Aspect | Rule |
|--------|------|
| **Corners** | Rounded (`border-radius: 16px`) on all image containers |
| **Framing** | Optional gradient border (`.grad-border`) for emphasis |
| **Captions** | Below image, left-aligned, Outfit font |
| **Hero images** | Bold, vibrant imagery that complements gradient palette |
| **Image grids** | Generous spacing, rounded containers |
| **Shadows** | Available in browser export. Use restrained shadows or gradient borders according to theme tone. |
| **Color treatment** | Gradient overlays permitted |
| **Preferred components** | `.img-frame`, `.aurora-card` with image |

### cyber-neon

| Aspect | Rule |
|--------|------|
| **Corners** | Sharp only (`border-radius: 0`). No rounded corners. |
| **Framing** | 1px neon-colored border or no border |
| **Captions** | Below image, monospace font, muted color |
| **Hero images** | Dark, high-contrast, tech/sci-fi aesthetic |
| **Image grids** | Sharp rectangles, dark backgrounds |
| **Shadows** | Never. Use neon glow borders sparingly. |
| **Color treatment** | No tinted overlays. Keep dark atmosphere. |
| **Preferred components** | `.img-frame` with sharp corners, terminal-style captions |

### data-dashboard

| Aspect | Rule |
|--------|------|
| **Corners** | Subtle rounding (`border-radius: 8px`) |
| **Framing** | 1px solid border matching container style |
| **Captions** | Below image, compact, sans-serif |
| **Hero images** | Diagrams, charts, screenshots preferred over photos |
| **Image grids** | Compact, dense, grid-aligned |
| **Shadows** | Never. Bordered containers only. |
| **Color treatment** | No tinted overlays. Data-accurate fidelity. |
| **Preferred components** | `.img-frame` within metric layouts |

### editorial-magazine

| Aspect | Rule |
|--------|------|
| **Corners** | Rounded (`border-radius: 4-8px`) permitted and encouraged |
| **Framing** | Warm editorial borders, subtle padding inside frame |
| **Captions** | Below image, left-aligned, monospace font (via `.img-caption`) |
| **Hero images** | Warm tones preferred, editorial photography style |
| **Image grids** | Asymmetric layouts preferred (30/70 or 40/60 splits) |
| **Shadows** | Available in browser export. Use subtle editorial shadows or border contrast. |
| **Color treatment** | Warm color overlay permitted |
| **Preferred components** | `.img-frame`, `figure` with `figcaption`, editorial captions |

### ink-landscape

| Aspect | Rule |
|--------|------|
| **Corners** | Minimal rounding (0-4px) or sharp |
| **Framing** | Subtle vermillion accent border or no border |
| **Captions** | Below image, serif font, left-aligned |
| **Hero images** | Ink wash, landscape, traditional Chinese art aesthetic |
| **Image grids** | Generous negative space, asymmetric |
| **Shadows** | Never. Let rice paper backgrounds provide atmosphere. |
| **Color treatment** | No tinted overlays. Preserve ink wash tones. |
| **Preferred components** | `.img-frame` with minimal framing, cultural imagery |

### mckinsey-minimal

| Aspect | Rule |
|--------|------|
| **Corners** | Clean (0-4px), minimal rounding |
| **Framing** | Subtle 1px border or no border |
| **Captions** | Below image, DM Sans, small size |
| **Hero images** | Professional, clean, high-quality photography |
| **Image grids** | Equal-width columns, structured, generous whitespace |
| **Shadows** | Never. Maximum cleanliness. |
| **Color treatment** | No tinted overlays. Professional fidelity. |
| **Preferred components** | `.img-frame` within insight card layouts |

### swiss-international

| Aspect | Rule |
|--------|------|
| **Corners** | Sharp only (`border-radius: 0`). No rounded corners. |
| **Framing** | Hairline border (1px) only, or no border at all |
| **Captions** | Below image, left-aligned, sans-serif, small weight |
| **Hero images** | High contrast, precise, architectural/product photography |
| **Image grids** | Equal-width columns (50/50, 33/33/33), grid-precise |
| **Shadows** | Never. No elevation effects. |
| **Color treatment** | No tinted overlays. Images at full fidelity. |
| **Preferred components** | `.img-frame.hairline`, clean sans-serif captions |

---

## Composition Guidance

Use the smallest combination that communicates the page:

1. Choose the **P — Primary Structure**: one visual field, image-as-canvas, comparison, sequence, or multi-visual system. More than one compatible structure may coexist when the page needs it.
2. Name a concrete integration job, then add only the **M — Modifier Layer** that serves it: crop/reveal, tone/focus, framing, placement, or restrained depth.
3. Use an **A — Asset-Dependent Treatment** only when its prepared local composite, cutout, or registered derivative exists. Do not fake it with brittle content HTML.
4. Add **C — Cross-Page Continuity** only when consecutive slides intentionally preserve or transform a visual relationship.
5. Stop when another layer no longer earns its place.

The numbered entries below are optional recall aids. Repeated plain splits can be exactly right for a comparison or a coherent series; modifiers are not required for variety's sake.

### A — Asset-Dependent Treatments

Examples include a verified transparent cutout, a prepared duotone or soft blend, and a registered sharp-subject/background derivative. The asset pipeline owns their preparation. HTML consumes the local result and keeps exact labels, data, and annotations native.

### C — Cross-Page Continuity

Useful relationships include a persistent source and crop with progressive native annotations, an intentional pan or push between overview and detail, and matched framing across different sources. Record the relationship in Visual Direction. Each slide must still be understandable as a settled static frame; runtime motion may enhance, but must not be the only carrier of meaning.

## Hard Constraints

- Long body copy, data points, numeric labels, and CJK text always go in the HTML layer -- never baked into the image.
- Semantic images use `<img src="assets/filename.ext">`; decorative CSS backgrounds should use local assets or data URIs.
- Browser export supports `box-shadow`, `filter`, `backdrop-filter`, and `mask`, but PPTX editability may vary. Inspect required output formats.
- Image transparency relies on PNG alpha or SVG with alpha; rendered natively throughout the pipeline.
- Always include `alt` text on every `<img>` element.
- Use `object-fit: cover` for hero/editorial images, `object-fit: contain` for diagrams/screenshots.

## Screenshot Framing

Preserve the original screenshot pixels, text, data, and UI details by default.
Choose the target slot ratio before choosing the treatment. Record `fit`, crop
permission, crop-safe area, focal point, and any theme-supported background,
padding, inset, shadow, corners, or alignment. Use `contain` for
legibility-sensitive UI, diagrams, and terminal evidence. Use `cover` only when
an approved crop keeps all required evidence. Redesign a screenshot only when
the source shape or density cannot remain legible in the required slot.

Use a semantic `<figure class="img-frame">` with a useful `alt` value. When
interpretation needs it, provide a concise visible caption and source in
`figcaption` (for example, `Checkout flow — Source: product team, 2026-08-02`).
Do not fabricate source attribution, application chrome, or device hardware.
Inspect browser and SVG/PPTX routes when their framing or crop differs
materially.

When embedding screenshots (UI mockups, terminal output, browser windows), follow this theme-treatment table:

| Parameter | aurora-gradient | cyber-neon | data-dashboard | editorial-magazine | ink-landscape | mckinsey-minimal | swiss-international |
|-----------|----------------|------------|----------------|-------------------|---------------|-----------------|---------------------|
| Background | Cream (`--surface-l`) | Dark elevated (`--bg-elevated`) | White surface (`--surface`) | Warm paper (`--bg-warm`) | Rice paper cream | Light grey (`--grey-1`) | Cool gray (`--color-gray-100`) |
| Padding | 5-8% inset | 3-5% inset | 3-5% inset | 5-8% inset | 5-8% inset | 5-8% inset | 3-5% inset |
| Corners | 16px radius | 0px (sharp) | 8px radius | 8px radius | 0-4px | 0-4px | 0px (sharp) |
| Border | Gradient or 2px | 1px neon accent | 1px solid | 2px warm border | 1px subtle | 1px subtle | 1px hairline |
| Fit | `object-fit: contain` | `object-fit: contain` | `object-fit: contain` | `object-fit: contain` | `object-fit: contain` | `object-fit: contain` | `object-fit: contain` |

### Optional Crop-Safe Bundled Background

An image may be used as a bundled, local background only when it is intentionally atmospheric or contextual and has a verified crop-safe region for the target canvas. Record the local asset, focal point, safe regions, contrast treatment, and whether the background is optional in the design spec. If the crop would hide required evidence, compete with text, or fail in another aspect ratio, use an `<img>`/`figure` instead. This is an optional composition tool, never a requirement to add a background image.

## Hard Constraint: No Slide Chrome in Generated Images

AI-generated images must NEVER contain:
- Headers, footers, or page numbers
- Slide titles or section labels
- Corner marks or decorative frames
- Text overlays that should be HTML elements

These elements are handled by the template's CSS classes and HTML structure. Including them in images creates duplication and prevents theme-switching.

> For the full "no slide chrome" rule and other hard constraints, see `image-generator.md` section 3 Hard Rules.

---

## Related Documents

- [`image-generator.md`](image-generator.md) -- Prompt assembly, Style Anchors, aspect ratio lookup table, and generation workflow. Determines what to generate for each pattern.
- [`shared-standards.md`](shared-standards.md) -- Slide dimensions, image embedding rules, and placeholder patterns.
- [`components.md`](components.md) -- `.img-frame` component definition and CSS tokens.
- [`layouts.md`](layouts.md) -- Layout classes for image positioning.
