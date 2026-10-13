# Editorial Magazine Theme

**Type**: HTML slide template (horizontal deck)
**Skill**: seaslides-html-slides-skill
**Aesthetic**: Editorial Magazine x Electronic Ink
**Origin**: Inspired by guizang-ppt-skill Style A
**Best For**: Keynotes, thought leadership, product launches, tech talks, independent creator decks
**Complexity Level**: Rich

## Description

The Editorial Magazine theme draws from independent print culture -- publications like Monocle, Apricot, A Book Apart, and design journals. It combines serif-forward typography, restrained color palettes, and magazine-style chrome (page headers and footers) with modern WebGL animated backgrounds and smooth Motion One entrance animations.

The core design philosophy:

- **Serif for impact, sans-serif for reading.** Headlines use Playfair Display (English) and Noto Serif SC (Chinese); body text uses Noto Sans SC for comfortable density.
- **Electronic ink aesthetic.** High contrast between ink (dark) and paper (light) tones, with warm undertones instead of pure black/white.
- **Magazine chrome.** Every slide has optional header (`.chrome`) and footer (`.foot`) bars with monospaced metadata, mimicking printed page margins.
- **WebGL depth.** Two full-screen shader backgrounds (holographic dark, pearl-flow light) create living texture behind content. Hero slides let these backgrounds shine through; regular slides mask them for readability.
- **Restrained animation.** Motion One drives cascading entrance animations. No bouncing, spinning, or gratuitous effects.

---

## Quick Start

### 1. Create your deck HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Presentation</title>
  <!-- Copy all <link> and <script> tags from index-template.html -->
  <link rel="stylesheet" href="template.css">
</head>
<body>
  <!-- Copy early scripts from index-template.html -->
  <canvas id="c-dark" class="bg"></canvas>
  <canvas id="c-light" class="bg"></canvas>
  <div id="deck">

    <!-- Your slides go here -->
    <section class="slide hero dark" data-theme="dark">
      <div class="chrome">
        <div class="left"><span>My Talk</span></div>
        <div class="right"><span>Vol.01</span></div>
      </div>
      <div class="frame" style="display:grid;gap:4vh;align-content:center;min-height:80vh">
        <div class="kicker" data-anim>Opening</div>
        <h1 class="h-hero h-hero-en" data-anim>Hello World</h1>
        <p class="lead" data-anim>A presentation about something important.</p>
      </div>
      <div class="foot">
        <div class="title">My Presentation</div>
        <div>-- 2026 --</div>
      </div>
    </section>

  </div>
  <div id="nav"></div>
  <!-- Copy remaining scripts from index-template.html -->
</body>
</html>
```

### 2. Choose a color theme

Add a theme class to `<body>` (or leave blank for ink-classic):

```html
<body class="indigo-porcelain">
```

### 3. Plan your slide rhythm

Before writing slides, map out the theme alternation:

| Slide | Theme | Type |
|-------|-------|------|
| 1 | `hero dark` | Cover |
| 2 | `light` | Content |
| 3 | `dark` | Content |
| 4 | `hero light` | Section divider |
| 5 | `light` | Content |
| ... | alternate | ... |

**Review heuristic**: Change light/dark treatment when it strengthens a narrative transition. Keep longer same-mode runs when continuity or comparison benefits from them.

---

## Color Themes

Five pre-designed palettes. **Do not mix values between themes.** Apply one theme per deck.

| Theme | Class | `--ink` | `--paper` | Best For |
|-------|-------|---------|-----------|----------|
| Ink Classic | *(default)* | `#0a0a0b` | `#f1efea` | General purpose, tech, business |
| Indigo Porcelain | `.indigo-porcelain` | `#0a1f3d` | `#f1f3f5` | Research, engineering, data science |
| Forest Ink | `.forest-ink` | `#1a2e1f` | `#f5f1e8` | Sustainability, culture, non-fiction |
| Kraft Paper | `.kraft-paper` | `#2a1e13` | `#eedfc7` | Humanities, literature, lifestyle |
| Dune | `.dune` | `#1f1a14` | `#f0e6d2` | Art, design, fashion, creative |

Each theme also defines `--ink-rgb`, `--paper-rgb`, `--paper-tint`, and `--ink-tint` for transparent overlays and tinted backgrounds.

---

## Typography System

### Font Families

| Token | Stack | Role |
|-------|-------|------|
| `--serif-display` | Playfair Display, Source Serif 4 | English display headings |
| `--serif-body` | Source Serif 4, Georgia | English body serif |
| `--serif-zh` | Noto Serif SC | Chinese headings, quotes |
| `--sans-zh` | Noto Sans SC | Chinese body text, descriptions |
| `--mono` | IBM Plex Mono | Kicker, meta, code, footer |

### Typography Classes

| Class | Font | Size | Weight | Use Case |
|-------|------|------|--------|----------|
| `.display` | Playfair Display | 11vw | 700 | Hero English headlines |
| `.display-zh` | Noto Serif SC | 7.8vw | 700 | Hero Chinese headlines |
| `.h1` | Noto Serif SC | 4.6vw | 700 | Page main title |
| `.h2` | Noto Serif SC | 3.2vw | 600 | Subtitle |
| `.h3` | Noto Serif SC | 1.9vw | 500 | Section / step titles |
| `.lead` | Noto Serif SC | 1.75vw | 400 | Lead paragraph (serif, opacity .86) |
| `.body` | Noto Sans SC | 1.22vw | 400 | Body text (sans, opacity .82) |
| `.body-serif` | Noto Serif SC | 1.3vw | 400 | Body text (serif alt, opacity .88) |
| `.big-num` | Playfair Display | 10vw | 800 | Giant metric number |
| `.mid-num` | Playfair Display | 5.5vw | 700 | Medium metric number |
| `.kicker` | IBM Plex Mono | 12px | 400 | Pre-title label (uppercase) |
| `.meta` | IBM Plex Mono | 0.88vw | 400 | Meta info tags (uppercase) |

### Layout-API Heading Aliases

| Class | Size | Description |
|-------|------|-------------|
| `.h-hero` | 10vw | Largest heading, for hero slides |
| `.h-xl` | 6.2vw | Section heading |
| `.h-sub` | 3.1vw | Subtitle (opacity .7) |
| `.h-md` | 2.3vw | Medium heading |
| `.h-hero-en` | -- | English override (Playfair Display) |
| `.h-xl-en` | -- | English override (Playfair Display) |

### Typography Rules

1. **Serif** (Noto Serif SC / Playfair Display / Source Serif 4): Headlines, key quotes, large numbers -- the "visual accent"
2. **Sans-serif** (Noto Sans SC): Body text, descriptions, dense information -- the "reading voice"
3. **Monospace** (IBM Plex Mono): Kicker labels, meta tags, footer text, code -- the "decorative rhythm"
4. English emphasis: `<em class="en">term</em>` renders in Playfair Display italic
5. Never use emoji as icons. Use Lucide icons via CDN instead.

---

## Slide Types

| Class | Description | WebGL Visibility |
|-------|-------------|------------------|
| `.slide.light` | Light background, dark text | ~22% (heavily masked) |
| `.slide.dark` | Dark background, light text | ~22% (heavily masked) |
| `.slide.hero.light` | Light hero, WebGL visible | ~84% (thin mask) |
| `.slide.hero.dark` | Dark hero, WebGL visible | ~88% (thin mask) |

**Every** `<section class="slide ...">` must also have `data-theme="light"` or `data-theme="dark"` so the navigation script can switch the WebGL canvas layers.

**Hero slides** are for visual-impact pages only: covers, section dividers, big quotes, closing CTAs. Do not use hero for content-dense slides.

---

## Component Catalog

### Chrome (page header)

```html
<div class="chrome">
  <div class="left">
    <span>Section Label</span>
    <span class="sep"></span>
    <span>Sub-label</span>
  </div>
  <div class="right"><span>03 / 12</span></div>
</div>
```

### Foot (page footer)

```html
<div class="foot">
  <div class="title">Project Name</div>
  <div>Act II &middot; Topic</div>
</div>
```

### Stat Card

```html
<div class="stat-card" data-anim>
  <div class="stat-label">Revenue</div>
  <div class="stat-nb">$42<span class="stat-unit">M</span></div>
  <div class="stat-note">Up 28% year-over-year</div>
</div>
```

Use inside `.grid-6` (3x2), `.grid-4` (2x2), or `.grid-3` (3x1).

### Callout (quote box)

```html
<div class="callout" data-anim>
  <div class="q-big">"Key insight or memorable quote."</div>
  <span class="cite">-- Attribution</span>
</div>
```

Automatically styled with left border and tinted background. Adapts to light/dark slides.

### Rowline (table row)

```html
<div class="rowline" data-anim>
  <div class="k">Feature Name</div>
  <div class="v">Description of what this feature does and why it matters.</div>
  <div class="m">Category &middot; Tag</div>
</div>
```

Three-column grid: key (serif) | value (sans) | meta (mono, right-aligned). First and last rows get automatic borders.

### Pillar (concept card)

```html
<div class="pillar" data-anim>
  <div class="ic">01</div>
  <div class="t">Card Title</div>
  <div class="d">Description text explaining this concept in detail.</div>
</div>
```

Use inside `.grid-3` for three-column layout. `.ic` can be a number, letter, or Lucide icon.

### Pipeline (process flow)

```html
<div class="pipeline-section">
  <div class="pipeline-label">Phase Name</div>
  <div class="pipeline" data-cols="4">
    <div class="step" data-anim="step">
      <div class="step-nb">01</div>
      <div class="step-title">Step Name</div>
      <div class="step-desc">Step description.</div>
    </div>
    <!-- more steps... -->
  </div>
</div>
```

Add `data-animate="pipeline"` to the parent `<section>` for manual step-through animation.

### Ghost (decorative background text)

```html
<div class="ghost" style="right:-6vw;top:-8vh">01</div>
```

34vw, 6% opacity. Use English words or numbers. Position with absolute offsets.

### Highlight

```html
<span class="hi">emphasized phrase</span>
```

Adds a subtle highlight bar under the text. Adapts to light/dark automatically.

### Tag

```html
<div class="tag">Label Text</div>
```

Bordered capsule with monospace text. Use in flex containers for tag groups.

### Image Placeholder

```html
<div class="img-slot r-4x3">
  <span class="plus">+</span>
  <span class="label">Image Description</span>
</div>
```

Dashed border placeholder for design-phase wireframing.

---

## Layout API

### Frame

`.frame` is the main content container inside each slide. It fills available space between `.chrome` and `.foot`.

### Grid Classes

| Class | Columns | Use Case |
|-------|---------|----------|
| `.grid-2-7-5` | 7fr 5fr | Text-heavy left + supporting right |
| `.grid-2-6-6` | 1fr 1fr | Equal split (comparison, before/after) |
| `.grid-2-8-4` | 8fr 4fr | Large text + small image/data |
| `.grid-3` | 3x 1fr | Three equal columns (pillars) |
| `.grid-3-3` | 3x 1fr, 2 rows | Six-item matrix (image grid) |
| `.grid-6` | 3x 1fr, 2 rows | Six stat cards |
| `.grid-4` | 2x 1fr, 2 rows | Four stat cards |
| `.split` | 1fr 1fr | Simple two-column split |

All grids default to `align-items: start` and `gap: 3vw 4vh`.

### Combining Frame with Grid

```html
<div class="frame grid-2-7-5" style="padding-top:6vh">
  <div><!-- left column --></div>
  <div><!-- right column --></div>
</div>
```

---

## Image System

### Frame-Img Container

```html
<figure class="frame-img r-16x10" data-anim>
  <img src="images/photo.jpg" alt="Description">
  <figcaption class="img-cap">Caption Text</figcaption>
</figure>
```

### Ratio Classes (single images only)

| Class | Aspect Ratio | Max Height |
|-------|-------------|------------|
| `.r-16x9` | 16:9 | 64vh |
| `.r-16x10` | 16:10 | 56vh |
| `.r-4x3` | 4:3 | 56vh |
| `.r-3x2` | 3:2 | 46vh |
| `.r-3x4` | 3:4 (portrait) | 60vh |
| `.r-1x1` | 1:1 | 50vh |

### Height Classes (for image grids -- never use ratio classes in grids)

| Class | Height |
|-------|--------|
| `.h-16` | 16vh |
| `.h-18` | 18vh |
| `.h-20` | 20vh |
| `.h-22` | 22vh |
| `.h-24` | 24vh |
| `.h-26` | 26vh |
| `.h-28` | 28vh |

**Critical rule**: In grids, all images in the same group must use the same height class. Never mix heights or use aspect-ratio classes inside grids.

### Image Cropping

Images default to `object-fit: cover` with `object-position: top center`. This means only the bottom of the image gets cropped -- top and sides are always preserved.

For screenshots or information graphics, add `.fit-contain` to prevent any cropping.

---

## WebGL Backgrounds

Two shader programs run on separate `<canvas>` elements:

- **Dark canvas** (`#c-dark`): Holographic Dispersion -- titanium iridescence with rainbow micro-perturbation and mouse-reactive radial ripples
- **Light canvas** (`#c-light`): Spiral Vortex -- FBM domain-warp flow with silver-pearl coloring, no center structure

The navigation script toggles which canvas is visible based on the current slide's theme. Hero slides show the WebGL prominently through thin overlays (12-16% opacity mask). Regular slides mask the WebGL heavily (78% opacity mask) to ensure text readability.

Press **B** to toggle low-power mode, which disables WebGL rendering entirely.

---

## Animation Recipes

Every element that should animate on entrance gets `data-anim`. The parent `<section>` can optionally specify `data-animate="recipe"` to select an animation style.

| Recipe | Trigger | Behavior | Best For |
|--------|---------|----------|----------|
| `cascade` | (default) | Stagger 120ms fade + translate-Y | Most content slides |
| `hero` | Auto on `.hero` slides | Slower stagger 180ms, ceremonial | Covers, dividers |
| `quote` | `data-animate="quote"` | Line-by-line 550ms reveal | Big quote slides |
| `directional` | `data-animate="directional"` | Left-in, divider, right-in | Before/after comparison |
| `pipeline` | `data-animate="pipeline"` | Manual advance per step | Process/workflow slides |

### Animation Attributes

| Attribute | Location | Value | Purpose |
|-----------|----------|-------|---------|
| `data-anim` | Any element | *(empty)* | Mark for cascade/hero entrance |
| `data-anim` | Element | `"left"` | Slide in from left |
| `data-anim` | Element | `"right"` | Slide in from right |
| `data-anim` | Element | `"line"` | Line-by-line quote reveal |
| `data-anim` | Element | `"step"` | Pipeline manual advance |
| `data-anim` | Element | `"divider"` | Fade to 25% opacity |
| `data-animate` | `<section>` | Recipe name | Select animation recipe |

---

## Design Rules

### Do

- Use light/dark changes to mark hierarchy or narrative transitions, not a fixed page interval
- Use hero slides sparingly (covers, dividers, quotes, closing)
- Keep kicker text different from chrome text (kicker is the page hook, chrome is the section label)
- Use `data-anim` on leaf elements (headings, cards, figures), not containers
- Control image height with fixed vh classes in grids
- Use `.fit-contain` for screenshots and information graphics
- Add meaningful, non-empty `data-notes="..."` to every `<section>`

### Do Not

- Use emoji as icons (use Lucide via CDN)
- Mix color theme values between different themes
- Let long same-mode runs become visually monotonous without a narrative reason
- Apply `align-self: end` to images (they will stack at bottom)
- Use `aspect-ratio` in image grids (use height classes instead)
- Add `box-shadow` or thick borders to images
- Write chrome and kicker with the same content
- Place content so low it overlaps with nav dots (leave 3vh+ clearance)
- Invent custom CSS class names (use inline styles if needed)
- Use hero class on content-dense slides

---

## Example Patterns

### Hero Cover

```html
<section class="slide hero dark" data-theme="dark" data-notes="Cover slide.">
  <div class="ghost" style="right:-6vw;top:-8vh">01</div>
  <div class="chrome">
    <div class="left"><span>Talk Title</span><span class="sep"></span><span>2026</span></div>
    <div class="right"><span>Vol.01</span></div>
  </div>
  <div class="frame" style="display:grid;gap:4vh;align-content:center;min-height:80vh">
    <div class="kicker" data-anim>Opening Line</div>
    <h1 class="h-hero" data-anim>Big Title</h1>
    <p class="lead" style="max-width:60vw" data-anim>Supporting sentence.</p>
    <div class="meta-row" data-anim><span>Author</span><span>&middot;</span><span>Role</span></div>
  </div>
  <div class="foot"><div class="title">Deck Name</div><div>-- 2026 --</div></div>
</section>
```

### Data Grid (6 metrics)

```html
<section class="slide light" data-theme="light" data-notes="KPI dashboard.">
  <div class="chrome">...</div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker" data-anim>Metrics</div>
    <h2 class="h-xl" data-anim>By The Numbers</h2>
    <div class="grid-6" style="margin-top:6vh">
      <div class="stat-card" data-anim>
        <div class="stat-label">Users</div>
        <div class="stat-nb">2.4<span class="stat-unit">M</span></div>
        <div class="stat-note">Monthly active users</div>
      </div>
      <!-- 5 more stat-cards... -->
    </div>
  </div>
  <div class="foot">...</div>
</section>
```

### Left Text + Right Image

```html
<section class="slide dark" data-theme="dark" data-notes="Feature highlight.">
  <div class="chrome">...</div>
  <div class="frame grid-2-7-5" style="padding-top:6vh">
    <div style="display:flex;flex-direction:column;justify-content:space-between;gap:3vh">
      <div>
        <div class="kicker" data-anim>Feature</div>
        <h2 class="h-xl" data-anim>Feature Name</h2>
        <p class="lead" style="margin-top:3vh" data-anim>Description.</p>
      </div>
      <div class="callout" data-anim>
        <div class="q-big">"A relevant quote."</div>
        <span class="cite">-- Source</span>
      </div>
    </div>
    <figure class="frame-img r-16x10" data-anim>
      <img src="images/feature.png" alt="Feature screenshot">
      <figcaption class="img-cap">Caption</figcaption>
    </figure>
  </div>
  <div class="foot">...</div>
</section>
```

### Pipeline (manual advance)

```html
<section class="slide light" data-theme="light" data-animate="pipeline" data-notes="Process.">
  <div class="chrome">...</div>
  <div class="frame">
    <div class="kicker">Workflow</div>
    <h2 class="h-xl">Process Name</h2>
    <div class="pipeline-section">
      <div class="pipeline-label">Phase Label</div>
      <div class="pipeline" data-cols="4">
        <div class="step" data-anim="step">
          <div class="step-nb">01</div>
          <div class="step-title">Step</div>
          <div class="step-desc">Description.</div>
        </div>
        <!-- more steps... -->
      </div>
    </div>
  </div>
  <div class="foot">...</div>
</section>
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Arrow Right` / `Space` / `Arrow Down` | Next slide (or next pipeline step) |
| `Arrow Left` / `Arrow Up` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `Escape` | Toggle overview mode |
| `B` | Toggle low-power mode (disables WebGL + animations) |

---

## External Dependencies

| Library | Purpose | Loaded Via |
|---------|---------|-----------|
| Google Fonts | Typography (5 families) | CDN link |
| KaTeX 0.16.11 | Math formula rendering | CDN |
| Prism.js 1.29 | Syntax highlighting | CDN + autoloader |
| pseudocode.js 2.4.1 | Algorithm pseudocode | CDN |
| Lucide Icons | SVG icon library | CDN (unpkg) |
| Motion One 11.11 | Entrance animations | Local file with CDN fallback |

All dependencies gracefully degrade: if CDN fails, content remains readable. Motion One has a local fallback path (`./motion.min.js`). If all animation loading fails, elements default to `opacity: 1`.
