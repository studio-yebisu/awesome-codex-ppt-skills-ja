# Style Presets Reference

Curated visual styles for Frontend Slides. Each preset is inspired by real design references — no generic "AI slop" aesthetics. **Abstract shapes only — no illustrations.**

This skill ships **2 specialty presets**: **Neon Cyber** (#1) and **re:Invent Keynote** (#2). The re:Invent Keynote preset has a rich, keynote-grade content-layout system documented in [layout-reinvent.md](layout-reinvent.md). **Both** presets support optional self-contained 3D/motion effects documented in [effects-reference.md](effects-reference.md) — the palette-agnostic catalog ships each technique in two tints: re:Invent purple (`demos/`) and Neon Cyber cyan (`demos/neon/`).

**Viewport CSS:** For mandatory base styles, see [viewport-base.css](viewport-base.css). Include in every presentation.

---

## Specialty Themes

### 1. Neon Cyber

**Vibe:** Futuristic, techy, confident

**Typography:** `Clash Display` + `Satoshi` (Fontshare)

**Colors:** Deep navy (#0a0f1c), cyan accent (#00ffcc), magenta (#ff00aa)

**Signature:** Particle backgrounds, neon glow, grid patterns, cyberpunk HUD chrome (corner
brackets + monospace `SYS.MODULE` labels), kinetic per-char titles, terminal typing, SVG gauge
rings with count-up, glitch quotes, orbit diagrams, dual marquee rows

**Layout System:** See [layout-neon.md](layout-neon.md) for the full set of ~11 HUD-grade layouts
(kinetic title, terminal overview, bento grid with border-beam hero, spotlight cards, gauge
metrics + scramble strip, VS comparison, circuit pipeline, marquee ecosystem, glitch quote, orbit
integrations, CTA closing) — each with CSS classes + HTML skeletons. The bundled preview at
`preview/01-neon-cyber.html` is the canonical implementation.

**Optional 3D & motion effects:** Experimental, self-contained, offline effects can enrich this style — a cyan WebGL shader nebula, an upgraded constellation network, pointer-driven 3D tilt, and a GSAP-orchestrated kinetic title. Neon-palette demos live in `demos/neon/`; see [effects-reference.md](effects-reference.md) (palette-agnostic catalog, use the Neon token set). The particle/grid background remains the lightweight default.

---

### 2. re:Invent Keynote

**Vibe:** Futuristic, keynote-stage, high-tech, professional

**Layout:** Near-black background with purple-pink gradient accents. Title/divider slides use full gradient backgrounds; content slides sit inside a refined rounded frame with a top breadcrumb/page-index bar and floating gradient orbs for stage-light atmosphere.

**Typography:**
- Display: `Urbanist` (700/800)
- Body: `Albert Sans` (400/500)

**Colors:**
```css
:root {
    --bg-primary: #0A0A0A;
    --bg-gradient: linear-gradient(135deg, #1A0033 0%, #2D0066 40%, #7C3AED 100%);
    --accent-purple: #8B5CF6;
    --accent-pink: #D946EF;
    --accent-orange: #FF9900;
    --accent-up: #34D399;      /* positive delta / growth */
    --accent-down: #FBBF24;    /* negative / caution delta */
    --text-primary: #FFFFFF;
    --text-secondary: rgba(255, 255, 255, 0.6);
    --glow-purple: rgba(139, 92, 246, 0.4);
    --card-bg: rgba(139, 92, 246, 0.08);
    --card-border: rgba(139, 92, 246, 0.25);
}
```

**Signature Elements:**
- Purple-pink gradient backgrounds for title/divider slides, near-black (#0A0A0A) for content slides
- Animated color-shifting blobs on title slides (see `animation-patterns.md` "Animated Blob Backgrounds")
- Refined content-page chrome: a thin rounded frame, a top-left eyebrow breadcrumb, a top-right `NN / NN` page index, and a centered segmented progress pip row
- Big gradient **section number** (`01`) beside each content title
- Floating gradient orbs on content slides (`filter: blur(100px)`, slow drift)
- Pill-shaped feature cards with purple glow border (`box-shadow: 0 0 20px rgba(139,92,246,0.4)`)
- Refined metric cards: category tag + large gradient number + unit + delta line (green up / amber down)
- AWS orange (#FF9900) used sparingly — only for small accents, never dominant

**Layout System:** See [layout-reinvent.md](layout-reinvent.md) for the full set of ~19 keynote-grade layouts (refined title, section divider, pill cards, metric-cards row, callout bar, tagged card grid, metric + side list, stats + feature grid, split divider, pipeline columns, quote, big number hero, comparison split, process flow, timeline zigzag, two-column reflection, numbered outlook, **bento grid with border-beam hero, spotlight cards, marquee**, and more) — each with CSS classes + HTML skeletons. Motion defaults: title word-reveal + gradient shimmer, count-up on every metric number.

**Optional 3D & motion effects:** Experimental, self-contained, offline effects can enrich this style — CSS 3D heroes, hand-written WebGL shader backgrounds, and GSAP-orchestrated titles. See [effects-reference.md](effects-reference.md) and the `demos/` directory. The CSS animated-blob cover remains the lightweight default.

---

## Chart Color Palettes

Each theme provides 6 harmonious colors for Chart.js datasets, plus grid/text colors. Use these when generating chart configurations.

### 1. Neon Cyber
```css
--chart-colors: #00ffcc, #ff00aa, #00aaff, #ffaa00, #aa00ff, #ff5555;
--chart-grid: rgba(0,255,204,0.06);
--chart-text: rgba(224,224,255,0.4);
--chart-card-bg: rgba(0,255,204,0.03);
--chart-card-border: rgba(0,255,204,0.15);
```

### 2. re:Invent Keynote
```css
--chart-colors: #8B5CF6, #D946EF, #FF9900, #06B6D4, #34D399, #F472B6;
--chart-grid: rgba(139,92,246,0.08);
--chart-text: rgba(255,255,255,0.4);
--chart-card-bg: rgba(139,92,246,0.06);
--chart-card-border: rgba(139,92,246,0.2);
```

---

## Font Pairing Quick Reference

| Preset | Display Font | Body Font | Source |
|--------|--------------|-----------|--------|
| Neon Cyber | Clash Display | Satoshi | Fontshare |
| re:Invent Keynote | Urbanist | Albert Sans | Google |

---

## DO NOT USE (Generic AI Patterns)

**Fonts:** Inter, Roboto, Arial, system fonts as display

**Colors:** `#6366f1` (generic indigo), purple gradients on white

**Layouts:** Everything centered, generic hero sections, identical card grids

**Card accents:** The **solid colored `border-left: 3px` rail** on a filled rounded card (esp. paired
with a rounded-square icon tile + round bullet dots) is the #1 AI/dashboard tell — avoid it. Carry
color with an inline heading icon, a short underline tick, an outlined index, or a hairline divider
instead of a full painted edge. (See Layout 12 in [layout-reinvent.md](layout-reinvent.md) for the
editorial-split alternative.)

**Decorations:** Realistic illustrations, gratuitous glassmorphism, drop shadows without purpose, emoji as icons (use Lucide)

---

## CSS Gotchas

### Negating CSS Functions

**WRONG — silently ignored by browsers (no console error):**
```css
right: -clamp(28px, 3.5vw, 44px);   /* Browser ignores this */
margin-left: -min(10vw, 100px);      /* Browser ignores this */
```

**CORRECT — wrap in `calc()`:**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));  /* Works */
margin-left: calc(-1 * min(10vw, 100px));     /* Works */
```

CSS does not allow a leading `-` before function names. The browser silently discards the entire declaration — no error, the element just appears in the wrong position. **Always use `calc(-1 * ...)` to negate CSS function values.**
