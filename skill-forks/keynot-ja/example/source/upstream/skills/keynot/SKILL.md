---
name: keynot
description: Create polished, self-contained HTML slide presentations — no PowerPoint or Keynote needed. Use this skill whenever the user asks for a presentation, slide deck, slides, or one-pager that will be shown in a browser. Also trigger when the user says things like "make it a deck", "turn this into slides", "build a presentation from this content", or "I need something to present". Prefer this over PPTX when the user has not explicitly asked for a .pptx file — HTML decks are more flexible, more visually rich, and easier to iterate on. Always use this skill when the user provides a brand style guide (PDF, URL, or description) alongside a presentation request. Trigger even if the user only says "make me a deck" with no further detail — start with content questions.
---
 
# Keynot
 
A skill for building browser-based slide presentations as single, self-contained HTML files. Keyboard navigation, swipe, fullscreen, animated reveals, embedded images, brand-accurate design. No external dependencies required at runtime.
 
---
 
## When to Use This Skill
 
- User asks for a "presentation", "deck", "slides", "one-pager to present"
- User has a brand style guide and wants slides that match it
- User wants to iterate on slides quickly in the browser
- User wants a file they can open anywhere without software
 
**Prefer HTML over PPTX unless:**
- User explicitly asks for `.pptx`
- User needs to edit slides in PowerPoint
- User needs to share with someone who must edit in Office
 
---
 
## Step 1: Extract the Brand Guide
 
If the user provides a brand PDF, URL, or describes their brand, extract these before writing any code. Be explicit and precise.
 
### What to Extract
 
**Colors**
- Primary (dominant background/text color)
- Accent (calls to action, rules, highlights)
- Neutrals (background, cream, gray)
- Document exact hex codes — never approximate
 
**Typography**
- Serif font (display headings, pull quotes)
- Sans-serif font (body, labels, UI)
- If proprietary fonts are specified (e.g., ITC Stone Serif, Acumin), find the closest Google Fonts equivalent
- Document the pairing explicitly
 
**Layout Language**
- Dominant color usage ratio (e.g., "blue should always dominate, red as accent only")
- Typical layout patterns visible in the guide (split panels, rules, dividers, margins)
- Tone: formal/editorial, warm/approachable, minimal/dense
 
**Logo and Mark Rules**
- Whether the logo/wordmark may be reproduced
- Clear space requirements
- Approved color variants (full color, white, black)
- Note: for institutional brands (universities, corporations), do NOT reproduce trademarked logos — use a text-based wordmark instead
 
### Example Brand Record
 
Once extracted, record the brand parameters in a compact block at the top of the deck's `<style>` so they're easy to audit and swap:
 
```
Primary Colors:
  Primary:  #HEX  (dominant — backgrounds, headings)
  Accent:   #HEX  (rules, CTAs, status — used sparingly)
  Cream:    #HEX  (light slide backgrounds)
 
Usage Rule: One color dominates. Accent appears sparingly —
  rules, call-to-action bars, status indicators.
  Never use the accent color as a full background.
 
Typography:
  Serif:      <Brand serif>      → <closest Google Font>
  Sans-serif: <Brand sans-serif> → <closest Google Font>
 
Layout Language:
  - Which colors own which regions (dark panels vs. light panels)
  - Any spine bars, rules, or dividers the brand uses
  - Layout motifs (split panels, stat columns, card grids)
  - Tone: editorial / warm / minimal / dense
 
Logo Rule: For institutional or trademarked brands, do NOT
  reproduce the logo. Use a text-based wordmark instead:
  <div class="wordmark">
    <div class="w-line-1">Organization</div>
    <div class="w-line-2">Subtitle or parent entity</div>
  </div>
```
 
---
 
## Step 2: Deck Architecture
 
Every deck is a single HTML file. All assets (fonts via CDN, images via base64) are embedded.
 
### Shell Structure
 
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google Fonts import -->
  <!-- All CSS in <style> tag -->
</head>
<body>
  <div class="deck" id="deck">
    <div class="slide" id="s1">...</div>
    <div class="slide" id="s2">...</div>
    <!-- more slides -->
  </div>
  <!-- Navigation -->
  <div class="nav">
    <button id="prev">&#8592;</button>
    <div class="dots" id="dots"></div>
    <button id="next">&#8594;</button>
    <span class="counter" id="counter">1 / N</span>
    <button id="fsBtn" onclick="toggleFS()">&#x26F6;</button>
  </div>
  <!-- Portrait/mobile rotate hint (see Portrait / Mobile Handling below) -->
  <div class="rotate-overlay" aria-hidden="true">
    <svg class="rotate-icon" width="56" height="56" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" stroke-width="1.4"
         stroke-linecap="round" stroke-linejoin="round">
      <rect x="5" y="2" width="14" height="20" rx="2.5" />
      <line x1="12" y1="18.5" x2="12.01" y2="18.5" />
    </svg>
    <h2>Rotate your device</h2>
    <p>This deck is designed for landscape viewing. Turn your phone sideways to continue.</p>
  </div>
  <script><!-- All JS inline --></script>
</body>
</html>
```
 
### Core CSS Patterns
 
```css
:root {
  /* Always use CSS variables for brand colors — swap these per brand */
  --primary: #1a1a2e;   /* dominant: dark panels, headings */
  --accent:  #e94560;   /* sparingly: rules, CTAs, status */
  --white:   #ffffff;
  --cream:   #f7f4ee;   /* light slide backgrounds */
  --serif:   'Cormorant Garamond', Georgia, serif;
  --sans:    'DM Sans', system-ui, sans-serif;
}
 
/* Deck shell */
html, body { width: 100%; height: 100%; overflow: hidden; background: #000; }
.deck { width: 100vw; height: 100vh; position: relative; }
 
/* Slides: opacity transition, stacked absolutely */
.slide {
  position: absolute; inset: 0;
  opacity: 0; pointer-events: none;
  transition: opacity .55s cubic-bezier(.4,0,.2,1);
}
.slide.active { opacity: 1; pointer-events: all; }
 
/* Staggered reveal animation on active slide children */
.slide.active .reveal { animation: fadeUp .6s both; }
.slide.active .reveal:nth-child(2) { animation-delay: .1s; }
.slide.active .reveal:nth-child(3) { animation-delay: .2s; }
/* ...continue for as many children as needed */
 
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(22px); }
  to   { opacity: 1; transform: translateY(0); }
}
```
 
### Navigation CSS
 
```css
.nav {
  position: fixed; bottom: 28px; left: 50%;
  transform: translateX(-50%);
  z-index: 999;
  display: flex; align-items: center; gap: 14px;
  background: rgba(26,26,46,.75);  /* tint from --primary */
  backdrop-filter: blur(10px);
  padding: 9px 20px; border-radius: 40px;
  border: 1px solid rgba(255,255,255,.14);
  opacity: 1;
  transition: opacity .4s ease;   /* required for auto-hide */
}
.nav-hidden { opacity: 0; pointer-events: none; }  /* auto-hide state */
.nav button {
  background: none; border: none; cursor: pointer;
  color: rgba(255,255,255,.65); font-size: 16px;
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%;
  transition: color .2s, background .2s;
}
.nav button:hover { color: #fff; background: rgba(255,255,255,.12); }
.dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: rgba(255,255,255,.3); cursor: pointer;
  transition: background .2s, transform .2s;
}
.dot.active { background: var(--accent); transform: scale(1.35); }
```
 
### JavaScript (complete — do not modify arithmetic)
 
```javascript
// Fullscreen
function toggleFS() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(() => {});
    document.getElementById('fsBtn').innerHTML = '&#x2715;';
  } else {
    document.exitFullscreen();
    document.getElementById('fsBtn').innerHTML = '&#x26F6;';
  }
}
document.addEventListener('fullscreenchange', () => {
  if (!document.fullscreenElement)
    document.getElementById('fsBtn').innerHTML = '&#x26F6;';
});
 
// Deep-link & session persistence helpers
function parseHash() {
  const m = location.hash.match(/^#slide-(\d+)$/);
  if (!m) return -1;
  const idx = parseInt(m[1], 10) - 1;  // hash is 1-based, array is 0-based
  return (idx >= 0 && idx < document.querySelectorAll('.slide').length) ? idx : -1;
}
function initialSlide() {
  const fromHash = parseHash();
  if (fromHash >= 0) return fromHash;
  const stored = sessionStorage.getItem('keynot-slide');
  if (stored !== null) {
    const idx = parseInt(stored, 10);
    if (idx >= 0 && idx < document.querySelectorAll('.slide').length) return idx;
  }
  return 0;
}
function persistSlide(idx) {
  sessionStorage.setItem('keynot-slide', idx);
  history.replaceState(null, '', '#slide-' + (idx + 1));
}

// Navigation
const slides = document.querySelectorAll('.slide');  // REQUIRED — do not omit
const dotsEl = document.getElementById('dots');
const counter = document.getElementById('counter');
let cur = initialSlide();

// Remove default 'active' class from slide 1 if restoring a different slide
slides.forEach(s => s.classList.remove('active'));

slides.forEach((_, i) => {
  const d = document.createElement('div');
  d.className = 'dot';
  d.addEventListener('click', () => go(i));
  dotsEl.appendChild(d);
});

// Activate the initial slide
slides[cur].classList.add('active');
dotsEl.children[cur].classList.add('active');
counter.textContent = `${cur + 1} / ${slides.length}`;
persistSlide(cur);

function go(n) {
  slides[cur].classList.remove('active');
  dotsEl.children[cur].classList.remove('active');
  cur = (n + slides.length) % slides.length;
  slides[cur].classList.add('active');
  dotsEl.children[cur].classList.add('active');
  counter.textContent = `${cur + 1} / ${slides.length}`;
  persistSlide(cur);
}

// Deep-link: respond to manual hash changes or pasted URLs
window.addEventListener('hashchange', () => {
  const idx = parseHash();
  if (idx >= 0 && idx !== cur) go(idx);
});
 
document.getElementById('next').addEventListener('click', () => go(cur + 1));
document.getElementById('prev').addEventListener('click', () => go(cur - 1));
 
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') go(cur + 1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                     go(cur - 1);
  if (e.key === 'f' || e.key === 'F') toggleFS();
});
 
// Auto-hide nav after 1.8s of inactivity; reappear on any interaction
const nav = document.querySelector('.nav');
let hideTimer;
function showNav() {
  nav.classList.remove('nav-hidden');
  clearTimeout(hideTimer);
  hideTimer = setTimeout(() => nav.classList.add('nav-hidden'), 1800);
}
document.addEventListener('mousemove', showNav);
document.addEventListener('touchstart', showNav, { passive: true });
document.addEventListener('keydown', showNav);
showNav(); // start timer on load
 
// Swipe
let tx = 0;
document.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
document.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 50) go(dx < 0 ? cur + 1 : cur - 1);
}, { passive: true });
```
 
### Portrait / Mobile Handling
 
Slide decks are a landscape medium. Rather than reflowing split-panel layouts into unreadable mobile stacks, **show a "rotate your device" overlay when the viewport is portrait + narrow**. This covers iPhones held vertically without doubling the CSS for every layout pattern. Landscape phone viewing keeps working because `clamp()` font sizing already scales down.
 
Add this CSS to every deck, near the bottom of the `<style>` block so it overrides nothing:
 
```css
/* Rotate-to-landscape overlay — only visible on portrait phones */
.rotate-overlay {
  display: none;
  position: fixed; inset: 0;
  z-index: 9999;
  background: var(--primary);
  color: var(--white);
  flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center; padding: 40px;
  font-family: var(--sans);
}
.rotate-overlay .rotate-icon {
  margin-bottom: 24px;
  color: var(--accent);
  animation: rotate-hint 2.4s ease-in-out infinite;
}
.rotate-overlay h2 {
  font-family: var(--serif);
  font-size: 30px; font-weight: 400;
  margin-bottom: 12px; letter-spacing: -.01em;
}
.rotate-overlay p {
  font-size: 14px; line-height: 1.6;
  opacity: .72; max-width: 280px;
}
@keyframes rotate-hint {
  0%, 40%, 100% { transform: rotate(0deg); }
  60%, 80%      { transform: rotate(90deg); }
}
@media (orientation: portrait) and (max-width: 900px) {
  .rotate-overlay { display: flex; }
}
```
 
The overlay HTML is included in the [Shell Structure](#shell-structure) above. Drop both in and the deck handles portrait phones gracefully without any per-slide changes.
 
**Why not full mobile responsiveness?** Split panels, stat columns, and photo backgrounds all rely on horizontal real estate to communicate. A reflowed mobile version is effectively a different deck — and a worse one. PowerPoint and Google Slides also fail on portrait mobile; the audience already accepts this for the format.
 
### Print / PDF Export
 
Users should be able to hit `Cmd+P` → "Save as PDF" and get a clean one-slide-per-page PDF. The screen deck stacks slides absolutely and hides inactive ones via `opacity: 0`, so a naive print captures only the active slide. The fix: **a `@media print` block that un-stacks every slide, kills animations, hides nav/overlays, and forces landscape page size**.
 
Add this near the bottom of the `<style>` block:
 
```css
/* Print / PDF export — Cmd+P → Save as PDF gives one slide per page */
@media print {
  @page {
    size: 1600px 1000px;  /* native deck aspect ratio; user can fit-to-page */
    margin: 0;
  }
  html, body {
    width: 1600px; height: auto;
    overflow: visible !important;
    background: #fff;
  }
  .deck {
    width: 1600px; height: auto;
    position: static !important;
  }
  .slide {
    position: relative !important;
    inset: auto !important;
    width: 1600px; height: 1000px;
    opacity: 1 !important;
    pointer-events: auto !important;
    page-break-after: always;
    break-after: page;
    transform: none !important;
  }
  /* Kill all animations and transitions so content is in final state */
  *, *::before, *::after {
    animation: none !important;
    animation-duration: 0s !important;
    animation-delay: 0s !important;
    transition: none !important;
  }
  .slide .reveal {
    opacity: 1 !important;
    transform: none !important;
  }
  /* Hide interactive chrome */
  .nav, .rotate-overlay { display: none !important; }
  /* Preserve backgrounds and colors in print output */
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}
```
 
**Usage:** user opens the deck in a browser, hits `Cmd+P` (or `Ctrl+P`), picks "Save as PDF" as the destination, and optionally toggles "Background graphics" on if the print dialog offers it. The default paper size in the dialog doesn't matter much — the `@page` rule sets the content frame, and browsers scale to fit. For pixel-perfect output, users can pick "Custom" paper size matching `1600 × 1000` in the dialog.
 
**Gotchas:**
- Gradients and some photo-panel rasterization can look slightly different from screen (Chrome and Safari differ). If the deck must look identical in print, keep backgrounds solid.
- Slides taller than 1000px will clip. Don't let content overflow the slide bounds on screen and it won't clip in print.
- Firefox honors `@page size: <pixels>` less reliably than Chrome/Safari. For critical Firefox users, swap to `size: 10in 6.25in` (same ratio, physical units).
 
---
 
## Step 3: Layout Patterns
 
Use these as building blocks. Mix and match per slide.
 
### Split Panel (most versatile)
Dark panel left (brand primary color), light panel right (white or cream). Diagonal slice or hard edge between them.
 
```html
<div class="slide" id="sN" style="display:flex;">
  <div class="left-panel"><!-- headline, statement, quote --></div>
  <div class="right-panel"><!-- list, stats, details --></div>
</div>
```
 
```css
.left-panel {
  width: 50%; background: var(--primary);
  display: flex; flex-direction: column; justify-content: center;
  padding: 72px 64px; position: relative; overflow: hidden;
}
.right-panel {
  flex: 1;
  display: flex; flex-direction: column; justify-content: center;
  padding: 72px 56px 72px 64px; background: var(--cream);
}
```
 
### Stat Column (credentials, metrics)
Right-side column of large serif numbers/words with small uppercase labels. Works over photo backgrounds.
 
```html
<div class="stats-col">
  <div class="stat">
    <div class="stat-n">13+</div>
    <div class="stat-l">Years at institution</div>
  </div>
  <!-- divider between stats: border-top: 1px solid rgba(255,255,255,.09) -->
</div>
```
 
### Value Cards (principles, pillars)
Left colored bar accent, title + description. One bar color per value for visual differentiation.
 
```html
<div class="value-card">
  <div class="value-bar" style="background:#2e7d32"></div>
  <div>
    <div class="value-title">Principle Name</div>
    <div class="value-text">Description of the principle.</div>
  </div>
</div>
```
 
### Approach Rows (process, steps)
Large ghost number, vertical rule, then body content. Good for 3-step processes.
 
```html
<div class="approach">
  <div class="approach-num">01</div>
  <div class="approach-body">
    <div class="approach-title">Step Title</div>
    <div class="approach-text">Detail text.</div>
    <div class="approach-tags"><span>Tag 1</span><span>Tag 2</span></div>
  </div>
</div>
```
 
### Tool/Status Cards
Name + status badge + description. Status badge variants: live (green), in-progress (amber), planned (neutral).
 
```html
<div class="tool-card">
  <div class="tool-body">
    <div class="tool-name">Tool Name</div>
    <span class="status status-live">Live</span>
    <div class="tool-desc">What it does and who it's for.</div>
  </div>
</div>
```
 
### Photo Background Panel
Embed image as base64, apply gradient overlay so text stays readable.
 
```html
<div class="photo-panel" style="
  position:absolute; top:0; right:0; bottom:0; width:42%;
  background: url('data:image/png;base64,...') center/cover no-repeat;
  z-index:1;
">
  <div style="position:absolute;inset:0;
    background:linear-gradient(to right, var(--primary) 0%, rgba(0,0,0,.55) 40%, rgba(0,0,0,.1) 100%);
  "></div>
</div>
```
 
To embed an image as base64:
```python
import base64
data = 'data:image/png;base64,' + base64.b64encode(open('image.png','rb').read()).decode()
```
 
---
 
## Step 4: Content Slide Sequence
 
A strong 5-slide deck structure for an institutional introduction:
 
| Slide | Purpose | Layout |
|-------|---------|--------|
| 1 | Who you are + elevator pitch | Full bleed dark + photo + stat column |
| 2 | Values / principles | Split panel + value cards |
| 3 | Approach / framework | Light background + approach rows |
| 4 | Tools / enablement | Dark background + two columns |
| 5 | Close + discussion opener | Split panel + photo background |
 
Adapt freely. The key is each slide has ONE job and ONE dominant visual idea.
 
---
 
## Step 5: Typography Rules
 
```css
/* Display heading — large, light weight, letter-spaced */
.display {
  font-family: var(--serif);
  font-size: clamp(52px, 7vw, 88px);
  font-weight: 300; line-height: .95;
  letter-spacing: -.01em;
}
 
/* Section heading */
.heading {
  font-family: var(--serif);
  font-size: clamp(32px, 4vw, 50px);
  font-weight: 400; line-height: 1.1;
}
 
/* Eyebrow label */
.label {
  font-family: var(--sans);
  font-size: 10px; font-weight: 600;
  letter-spacing: .2em; text-transform: uppercase;
}
 
/* Body */
.body {
  font-family: var(--sans);
  font-size: 13px; font-weight: 300; line-height: 1.65;
}
 
/* Use clamp() for all font sizes to scale with viewport */
```
 
---
 
## Critical Pitfalls
 
### NEVER use blanket string/regex replacement on files containing JavaScript
 
This will corrupt arithmetic operators. Example of what goes wrong:
 
```python
# DANGEROUS — corrupts JS
content = content.replace(' - ', ', ')
# cur - 1  becomes  cur, 1     (prev button breaks)
# clientX - tx  becomes  clientX, tx  (swipe breaks)
```
 
**Safe approach:** Use targeted `str_replace` with unique, specific strings. Always view the JS section after any automated replacement to verify arithmetic operators are intact.
 
### Always declare `const slides` before using it
 
If inserting a new function before the navigation block, check that `const slides = document.querySelectorAll('.slide')` is still present and comes before `slides.forEach(...)`.
 
### `str_replace` requires unique strings
 
Before using str_replace, grep for the target string to confirm it appears exactly once. If it appears multiple times, add more context lines to make it unique.
 
### Base64 images make files large but self-contained
 
A single high-res PNG can add 150-200KB to the file. This is fine for a presentation deck. Use `cover` sizing and `center center` positioning. Always add a gradient overlay div for text legibility.
 
### Emoji in content
 
Avoid leading emoji in list items and card titles — they read as AI-generated and date quickly. If the user asks to remove emoji, use Python unicode replacement rather than sed:
 
```python
import re
content = re.sub(r'[\U00002600-\U0001FAFF]+', '', content)
content = content.replace('\ufe0f', '')  # variation selector
```
 
---
 
## Iterative Editing Workflow
 
When making changes after initial build:
 
1. **View the relevant section first** — `view` tool with line range
2. **Use `str_replace`** for surgical edits — never rewrite the whole file for small changes
3. **Verify JS after any automated text processing** — check lines with `cur`, `dx`, `+`, `-` operators
4. **Present fresh file after changes** — user may be viewing cached version
 
When the user says things like "slide 3: change X" — make ONLY that change. Resist the urge to improve adjacent content.
 
---
 
## Codex / API Usage Notes
 
This skill is compatible with Claude API (Codex) usage. Key considerations:
 
- The complete JS block (navigation + fullscreen) should be treated as a unit — include it verbatim and do not modify arithmetic
- When generating via API, stream the file to disk and open in browser for preview
- The base64 embedding approach works identically in API context
- CSS variables (`--primary`, `--accent`, etc.) make theming programmatic — pass brand colors as parameters and substitute into the template
 
---
 
## PPTX Export (PowerPoint)

When the user explicitly asks for a `.pptx` file, generate a Python script that uses `python-pptx` to build the deck programmatically. The user runs it with:

```bash
uv run --with python-pptx <script>.py
```

No system-wide installs required — `uv` handles the dependency inline.

### When to use PPTX instead of HTML

- User explicitly asks for `.pptx` or "PowerPoint"
- User needs recipients to edit slides in Office
- User says "I need to share this with someone who uses PowerPoint"

### How it works

Same content extraction and brand logic as HTML — extract colors, fonts, layout intent from the prompt. Then emit a self-contained `.py` script instead of an `.html` file.

### PPTX Generation Pattern

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Brand colors mapped from CSS variables
PRIMARY = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT = RGBColor(0xE9, 0x45, 0x60)

prs = Presentation()
prs.slide_width = Inches(16)
prs.slide_height = Inches(10)
blank_layout = prs.slide_layouts[6]  # blank — full control

def set_slide_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text_box(slide, left, top, width, height, text,
                 font_size=18, bold=False, italic=False,
                 color=RGBColor(0xFF,0xFF,0xFF), font_name="Arial"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.italic = italic
    p.font.color.rgb = color
    p.font.name = font_name

# Build slides...
slide1 = prs.slides.add_slide(blank_layout)
set_slide_bg(slide1, PRIMARY)
add_text_box(slide1, Inches(0.8), Inches(3), Inches(10), Inches(3),
             "Title Here", font_size=72, font_name="Georgia")

prs.save("output.pptx")
print("Saved: output.pptx")
```

### Mapping HTML layouts to PPTX

| HTML Pattern | PPTX Equivalent |
|---|---|
| Split panel (dark left / light right) | Rectangle shape as left bg + text boxes on each side |
| Stat columns | Large-font text boxes with small label text boxes below |
| Value cards with colored bars | Thin rectangle shapes as accent bars + adjacent text boxes |
| Approach rows (numbered steps) | Large number text box + title/body text boxes offset right |
| Full-bleed background | `set_slide_bg()` with brand color |

### Important caveats

**Warn the user:** PPTX output is an approximation of the HTML deck, not a pixel-perfect replica. python-pptx does not support CSS, gradients, `clamp()` scaling, or web fonts. The generated deck will:

- Use system fonts (Arial, Georgia) as fallbacks for Google Fonts
- Approximate gradients with solid colors
- Skip animations and reveals (static slides)
- Require manual touch-up for precise alignment

Always tell the user: *"The .pptx is a solid starting point but may need minor adjustments in PowerPoint — check alignment and font rendering before presenting."*

### Font mapping

| HTML (Google Font) | PPTX fallback |
|---|---|
| Cormorant Garamond | Georgia |
| DM Sans | Arial |
| Playfair Display | Georgia |
| Inter | Arial |
| Any serif | Georgia or Times New Roman |
| Any sans-serif | Arial or Calibri |

---

## Quick Reference: Palette Slots
 
Every deck fills these slots. Populate from the brand guide, then theme programmatically via CSS variables.
 
```
--primary     Dominant backgrounds and dark panels
--accent      Rules, spine bars, CTAs, status dots, hover states
--cream       Light slide backgrounds (warmer than pure white)
--stone       Dividers, subtle borders (one tint above cream)
--ink         Body text on light backgrounds (softer than black)
--muted       Labels, metadata, secondary text
--go          Positive / live / green status
--warn        Review / caution / amber status
--alt         Fifth accent for value/pillar differentiation
```
 
Fill with real hex codes at the top of `<style>` and reference everywhere via `var(--name)`.