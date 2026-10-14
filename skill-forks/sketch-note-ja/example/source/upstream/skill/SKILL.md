---
name: agentic-ppt
description: Generate styled HTML presentations from a topic or viewpoint. Supports multiple visual styles (sketch-notes, minimal, dark-pro, data-viz). Produces a self-contained single-file HTML deck with arrow-key navigation and zero dependencies. Use when (1) user wants to make a PPT, (2) user mentions "sketch notes", "簡報", "做 PPT", "agentic PPT", or "生成投影片".
---

# Agentic PPT — Skill Instructions

## Overview

You will generate a **single self-contained HTML file** that renders as a styled presentation. The output must be a fully working HTML deck — no frameworks, no npm, no build step. The file should work by simply opening it in a browser.

---

## Phase 0: Understand the Content

Before generating, ask the user (or infer from context):

1. **Topic / Viewpoint** — What is this presentation about? What is the author's unique take?
2. **Slide count** — How many slides? (Recommend 5–10 for clarity)
3. **Language** — Traditional Chinese (繁體中文) / Simplified Chinese (简体中文) / English?
4. **Audience** — Who will see this? (affects density and tone)
5. **Style** — Which visual style?
   - `sketch-notes` *(default)* — warm cream paper + manga-inspired hand-drawn feel
   - `minimal` — black & white, large typography, maximum whitespace
   - `dark-pro` — dark background, pro tech aesthetic, cyan/teal accents
   - `data-viz` — vibrant palette, bold charts, data-forward layout

---

## Phase 1: Plan the Slide Structure

Plan the deck before generating HTML. A good structure:

| # | Slide Type | Purpose |
|---|-----------|---------| 
| 1 | Cover | Title + subtitle + one-line hook in a speech bubble |
| 2 | Overview | 3–5 key points (tool cards or insight grid) |
| 3–N | Content | One idea per slide. Tables, comparisons, decision trees |
| N | Takeaway | 2–3 bold conclusions in speech bubbles |

**Rule: One idea per slide. If content overflows, split into two slides.**

---

## Phase 2: Generate the HTML

### Required Structure

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Presentation Title]</title>
  <style>
    /* === 1. Style token override (if non-default style) === */
    /* === 2. All CSS from Phase 3 === */
    /* === 3. Slide-specific styles === */
  </style>
</head>
<body>
  <div class="halftone"></div>
  <div class="deck">
    <!-- Slides here -->
  </div>
  <nav class="nav">
    <button onclick="prev()" aria-label="Previous">←</button>
    <span class="counter" id="counter">1 / N</span>
    <button onclick="next()" aria-label="Next">→</button>
  </nav>
  <script>
    const S=document.querySelectorAll('.slide');let c=0;
    function show(n){S[c].classList.remove('active');c=(n+S.length)%S.length;S[c].classList.add('active');document.getElementById('counter').textContent=`${c+1} / ${S.length}`;}
    function next(){show(c+1)} function prev(){show(c-1)}
    document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' ')next();if(e.key==='ArrowLeft')prev();});
    let tx=0;document.addEventListener('touchstart',e=>{tx=e.touches[0].clientX});
    document.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-tx;if(d<-50)next();if(d>50)prev();});
  </script>
</body>
</html>
```

### Style Token Override

If the user picks a **non-default** style, prepend one `:root` block in the `<style>` tag **before** all other rules. Each variant only overrides CSS custom properties — component classes and layout stay the same. See **Phase 3.5** for the exact `:root` blocks.

```css
/* Example: dark-pro override */
:root {
  --ink: #e0e0e0;
  --paper: #1a1a2e;
  --accent: #4ECDC4;
  /* ... see Phase 3.5 for complete tokens */
}
```

> For `dark-pro` and other dark themes, also invert the `.halftone` overlay opacity and adjust `.nav` button colors to match `--ink`.

---

## Phase 3: Visual Design Rules (Sketch Notes — Default)

### Typography (MANDATORY)

```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=Caveat:wght@400;700&family=Permanent+Marker&display=swap');
```

| Element | Font | Weight |
|---------|------|--------|
| Main headings (EN) | `Permanent Marker` | — |
| Body text, CJK | `Noto Sans SC` | 400 / 700 / 900 |
| Handwritten accents | `Caveat` | 400 / 700 |

### All sizes MUST use clamp()

```css
/* Good */  font-size: clamp(36px, 5vw, 72px);
/* Bad */   font-size: 48px;  /* ← NEVER do this */
```

### Colour Palette (Sketch Notes)

```css
:root {
  --ink: #1a1a1a;
  --paper: #f5f0e8;       /* warm cream */
  --grey: #888;
  --light-grey: #d0ccc4;
}
```

### Entrance Animations

Add `.reveal` to elements that should animate in when their slide becomes active.

```css
.reveal {
  opacity: 0; transform: translateY(30px);
  transition: opacity 0.6s cubic-bezier(0.16,1,0.3,1),
              transform 0.6s cubic-bezier(0.16,1,0.3,1);
}
.slide.active .reveal { opacity: 1; transform: translateY(0); }
/* Stagger children */
.reveal:nth-child(1) { transition-delay: 0.1s; }
.reveal:nth-child(2) { transition-delay: 0.2s; }
.reveal:nth-child(3) { transition-delay: 0.3s; }
.reveal:nth-child(4) { transition-delay: 0.4s; }
```

> Use `.reveal` on headings, cards, and bubbles. **Do not** animate body text paragraphs.

---

## Phase 3.5: Style Variants

When the user selects a non-default style, use the corresponding `:root` block below **and** swap the `@import` font URL. All component classes (`.bubble`, `.tool-card`, etc.) remain the same — only tokens and fonts change.

### `minimal` — Black & White

```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&family=Noto+Sans+SC:wght@400;700;900&display=swap');

:root {
  --ink: #111;
  --paper: #ffffff;
  --grey: #999;
  --light-grey: #e5e5e5;
  --accent: #111;
}
```

| Element | Font | Notes |
|---------|------|-------|
| Headings | `Outfit` 900 | All-caps recommended |
| Body / CJK | `Noto Sans SC` 400 | |

> Hide `.halftone` and `.crosshatch` overlays. Rely on typography hierarchy and whitespace only.

### `dark-pro` — Tech Dark

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Noto+Sans+SC:wght@400;700;900&display=swap');

:root {
  --ink: #e0e0e0;
  --paper: #1a1a2e;
  --grey: #7f8c9b;
  --light-grey: #2a2a4a;
  --accent: #4ECDC4;
}
```

| Element | Font | Notes |
|---------|------|-------|
| Headings | `Space Grotesk` 700 | Use `--accent` for key terms |
| Body / CJK | `Noto Sans SC` 400 | |

> Replace `.halftone` with a subtle CSS grid pattern (`--light-grey` lines on `--paper`). Add `box-shadow: 0 0 20px var(--accent)` glow on `.tool-card:hover`.

### `data-viz` — Vibrant Data

```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Noto+Sans+SC:wght@400;700;900&display=swap');

:root {
  --ink: #2d3436;
  --paper: #fafafa;
  --grey: #636e72;
  --light-grey: #dfe6e9;
  --accent: #6C5CE7;
  --chart-1: #00b894;
  --chart-2: #fdcb6e;
  --chart-3: #e17055;
  --chart-4: #0984e3;
}
```

| Element | Font | Notes |
|---------|------|-------|
| Headings | `Plus Jakarta Sans` 800 | |
| Body / CJK | `Noto Sans SC` 400 | |

> Use `--chart-1` through `--chart-4` for bar/pie/line chart segments. Add `border-left: 4px solid var(--accent)` on `.insight-card`.

---

## Phase 4: Available Visual Components

### 1. Speech Bubble `.bubble`
Best for: quotes, key takeaways, the author's voice.
```html
<div class="bubble">
  <p>Your insight here.</p>
</div>
```

### 2. Tool Cards `.tool-card` in `.tools-grid`
Best for: comparing 4–6 items side by side.
```html
<div class="tools-grid">
  <div class="tool-card">
    <div class="icon">⚡</div>
    <div class="tag">CATEGORY</div>
    <h3>Title</h3>
    <div class="cn-name">中文名稱</div>
    <p>Description.</p>
  </div>
</div>
```

### 3. Decision Tree `.decision-tree`
Best for: "How to choose?" slides.
```html
<div class="decision-tree">
  <div class="dt-node question">Core question?</div>
  <div class="dt-arrow"></div>
  <div class="dt-branch">
    <div class="dt-branch-item">
      <div class="dt-label">Option A</div>
      <div class="dt-arrow"></div>
      <div class="dt-node answer">Answer A</div>
    </div>
    <div class="dt-branch-item">
      <div class="dt-label">Option B</div>
      <div class="dt-arrow"></div>
      <div class="dt-node answer">Answer B</div>
    </div>
  </div>
</div>
```

### 4. Insight Grid `.insight-grid` / `.insight-card`
Best for: 4–6 insight/principle cards with large background number.
```html
<div class="insight-grid">
  <div class="insight-card">
    <div class="num">01</div>
    <h3>Principle title</h3>
    <p>Explanation.</p>
  </div>
</div>
```

### 5. Comparison Table `.compare-table`
Best for: head-to-head feature comparison.

### 6. Emphasis Box `.emphasis-box`
Best for: a single powerful statement.
```html
<div class="emphasis-box">One powerful sentence here</div>
```

### 7. Decorative Elements
```html
<!-- Manga crosshatch corner patch (sketch-notes only) -->
<div class="crosshatch" style="width:200px;height:200px;top:40px;left:30px;"></div>

<!-- Sketch underline on heading -->
<h2><span class="sketch-underline">Section Title</span></h2>
```

---

## Phase 5: Content Density Limits

| Slide Type | Max Content |
|-----------|------------|
| Cover | 1 title + 1 subtitle + 1 speech bubble |
| Content | 1 heading + 4–6 points OR 1 heading + 2 paragraphs |
| Card grid | 1 heading + max 6 cards (2×3 or 3×2) |
| Quote | 1 quote (max 3 lines) + attribution |
| Takeaway | 2–3 speech bubbles with bold conclusions |

**If content overflows → split into two slides. Never compress or scroll.**

---

## Anti-Patterns to Avoid

- ❌ Do NOT use: Inter, Roboto, Arial, system fonts (too generic)
- ❌ Do NOT use: purple gradient + white background ("AI slop")
- ❌ Do NOT use: fixed `px` sizes (use `clamp()`)
- ❌ Do NOT allow: vertical scroll on any slide (`overflow: hidden` on `.deck`)
- ❌ Do NOT embed: base64 images > 50KB (slows file loading)
- ❌ Do NOT center-align everything — use asymmetric layout for visual interest
- ❌ Do NOT use generic indigo `#6366f1` or purposeless glassmorphism

> **Self-awareness check:** You tend to converge toward "on distribution" outputs — the same layout, the same decorations, the same color choices every time. This is what users call "AI slop." Even within the same style, vary your decorative placement, card arrangements, and visual surprises across each generation.

---

## CSS Gotchas

Common AI-generated CSS mistakes — avoid these:

```css
/* ❌ Negative clamp — silently ignored by browsers */
right: -clamp(28px, 3.5vw, 44px);
/* ✅ Correct */
right: calc(-1 * clamp(28px, 3.5vw, 44px));

/* ❌ CJK text overflow — long Chinese strings may not wrap */
/* ✅ Always add on text containers */
word-break: break-word;
overflow-wrap: break-word;

/* ❌ vh on mobile Safari — address bar causes overflow */
/* ✅ Use dvh with fallback */
height: 100vh;
height: 100dvh;
```

---

## Delivery

Output a single `.html` file to `output/[topic]-ppt.html`. The `output/` directory is gitignored — all generated decks live there.

Include a brief summary of:
- Number of slides generated
- Style applied (and any style-specific notes)
- Key design choices made
- Keyboard shortcuts reminder: `→` / `Space` = next, `←` = prev
