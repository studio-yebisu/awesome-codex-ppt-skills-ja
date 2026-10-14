# Sketch Notes Style Guide

> Design principles behind the Agentic PPT visual system.

---

## Core Philosophy

**"One idea per slide. One personality per deck."**

A Sketch Notes presentation should feel like a thoughtful hand-drawn summary — not a polished corporate deck. The visual style borrows from manga and sketchbooks: bold ink lines, rough textures, intentional whitespace, and a warm paper tone.

---

## Colour System

| Token | Hex | Usage |
|-------|-----|-------|
| `--ink` | `#1a1a1a` | All strokes, text, borders, dark backgrounds |
| `--paper` | `#f5f0e8` | Slide background — warm cream, not pure white |
| `--grey` | `#888` | Secondary text, labels, subtle elements |
| `--light-grey` | `#d0ccc4` | Decorative lines, crosshatch, borders |

**Rule:** Add one accent colour per deck maximum (e.g. orange `#FF6B35`, teal `#4ECDC4`). Use it sparingly — only for one component type.

---

## Typography

### Font Stack

| Role | Font | Why |
|------|------|-----|
| EN display / hero titles | `Permanent Marker` | Authentic hand-lettered feel |
| CJK body / headings | `Noto Sans SC` | Best CJK coverage + weights |
| Handwritten accents / captions | `Caveat` | Sketch, casual, human |

### Always Use `clamp()`

Every font-size, padding, and gap in this system uses `clamp(min, preferred, max)`.  
This ensures slides look right from 1024px desktop to 1920px 4K monitors — without breakpoints.

```css
/* ✅ Correct */
font-size: clamp(24px, 3.2vw, 48px);

/* ❌ Never */
font-size: 36px;
```

---

## Layout System

### The Golden Rule: 100vh, No Scroll

Every slide must fit within `100vh`. No exceptions.

- If content overflows → **split into two slides**
- Never reduce font sizes below `clamp()` minimums
- Never enable `overflow: scroll` on `.slide`

### Content Density Limits

| Slide Type | Maximum Content |
|-----------|----------------|
| Cover | Title + subtitle + 1 speech bubble |
| Content | 1 heading + 4–6 points OR 2 paragraphs |
| Card grid | 6 cards maximum (2×3 or 3×2) |
| Quote | 1 quote, max 3 lines + attribution |
| Comparison table | Max 6 rows, 5 columns |
| Takeaway | 2–3 speech bubbles |

---

## Visual Components

### Manga Decorations (Use Sparingly)
- `.crosshatch` — diagonal crosshatch texture patch in corners
- `.halftone` — full-slide dot overlay (opacity 4%, always on)
- `.sketch-underline` — hand-drawn wavy underline on headings
- `.manga-star` — twinkling star emoji with animation

### Structural Components
- `.bubble` — speech bubble (white, thick ink border, tail at bottom-left)
- `.tool-card` — product/feature card with speed-lines corner decoration
- `.insight-card` — numbered principle card with large ghost number
- `.dt-node.question` — hexagonal decision node (dark bg)
- `.dt-node.answer` — dashed answer leaf
- `.emphasis-box` — tilted black box for power statements
- `.compare-table` — manga-style comparison table (dark header)

---

## Anti-Patterns

### Fonts to Avoid
- Inter, Roboto, Arial, Helvetica — too generic
- System UI fonts — no character

### Colours to Avoid
- Purple + white (peak AI slop)
- Gradients on text (unreadable at small sizes)
- Pure black `#000` + pure white `#fff` backgrounds (use `--ink` + `--paper`)

### Layout Anti-Patterns
- Centring everything (use left-aligned text blocks for content slides)
- Equal-size everything (use intentional hierarchy)
- Filling every corner (whitespace is intentional)

---

## Slide Flow Patterns

### Pattern 1: Topic Introduction
```
Cover → Overview (cards) → Deep Dive → Comparison → Takeaway
```

### Pattern 2: How-To / Tutorial
```
Cover → Why This Matters → Step 1 → Step 2 → Step 3 → Common Mistakes → Summary
```

### Pattern 3: Opinion / Essay
```
Cover → My Thesis → Evidence 1 → Evidence 2 → Counterargument → Conclusion
```

---

## Animation Philosophy

Slides cross-fade at 0.5s (`transition: opacity .5s ease`). This is sufficient.

Do **not** add complex entrance animations to individual elements — this distracts from content. The visual style itself carries the energy.

The one exception: `.manga-star { animation: twinkle }` — a subtle looping element that adds life without distraction.
