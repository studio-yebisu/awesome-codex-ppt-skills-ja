# Neon Cyber — Layout Patterns Reference

This is the layout reference for **style #1 — Neon Cyber**. Extracted from the shipped
`preview/01-neon-cyber.html`. Use these CSS classes and HTML skeletons when generating
Neon Cyber presentations.

**Read this file during Step 5 (generation) when the chosen style is #1 Neon Cyber.**

The full design-system CSS lives in the `<head>` of the preview file — copy it into every deck. When using
parallel generation (8+ slides), the framework agent emits the head + controller and batch agents write ONLY
`<section class="slide …">…</section>` blocks between them — never add a second `<style>` or `<script>`.

## Hard rules

- **Icons:** raw inline Lucide `<svg viewBox="0 0 24 24"><path …></svg>` markup, paths only — no `fill`/`stroke`
  attributes on the element itself. The *parent* class (`.bento-icon svg`, `.spot-icon svg`, `.circuit-disc svg`,
  `.vs-item svg`, `.cta-badge svg`, …) sets `stroke: var(--accent-cyan)` (or a contextual color), `fill:none`,
  `stroke-width`, `stroke-linecap:round`, `stroke-linejoin:round`. NEVER emoji.
- **Reveal stagger:** add `reveal d1`…`reveal d7` to elements you want animated into view in sequence.
- **One `<section>` = one slide = `100vh`** (with `height:100dvh` fallback for mobile chrome). Never exceed it.
- **All sizing via `clamp()`.** Every font-size, gap, padding and radius in the theme uses `clamp()` so the deck
  scales from small laptop windows up to large displays without a second breakpoint system.
- **One `<script>`.** The controller (IntersectionObserver + nav), the FX engine (counters/typing/scramble/tilt),
  the constellation canvas, and the WebGL nebula all live in the single `<script>` block at the end of `<body>`.
- **Fonts:** Clash Display (`--font-display`, headings) + Satoshi (`--font-body`, copy) + JetBrains Mono
  (`--font-mono`, terminal/HUD/mono text), loaded from Fontshare in `<head>`.
- **`.beam-border` requires the `@property --beam-angle` registration** (see Common Elements) declared once in
  `<style>` before any element uses the class — without it the conic-gradient angle cannot be animated and the
  beam freezes at a static angle instead of spinning.
- **Gradient-clip text must stay on one unsplit element.** If you add `background-clip:text` anywhere, never
  combine it with `.kin` character-splitting — each `<span class="kin">` char is a separate box, so a gradient
  clipped across split spans re-clips per character and looks broken/banded. `.kin` headlines in this theme use
  `.neon-text` (glow via `text-shadow`), not gradient-clip.
- **Leave chrome auto-fields EMPTY.** The controller fills `.hud-index` (`IDX NN/NN`). Write it as an empty
  `<span class="hud-index"></span>`.
- Every CONTENT slide (2–10) carries the standard HUD chrome (frame + bar + scanline). The title and CTA
  covers intentionally drop it — see each layout below.

---

## Common Elements

### Theme tokens (defined in `:root`)

```css
--bg-primary:#0a0f1c; --bg-card:rgba(17,24,39,.7);
--text-primary:#e2e8f0; --text-secondary:#94a3b8;
--accent-cyan:#00ffcc; --accent-magenta:#ff00aa; --accent-blue:#00aaff;
--accent-glow-cyan:rgba(0,255,204,.3); --accent-glow-magenta:rgba(255,0,170,.25);
--font-display:'Clash Display',sans-serif; --font-body:'Satoshi',sans-serif;
--font-mono:'JetBrains Mono','SF Mono',Menlo,monospace;
--title-size:clamp(2rem,6vw,5rem); --h2-size:clamp(1.5rem,4vw,3rem); --h3-size:clamp(1rem,2vw,1.5rem);
--subtitle-size:clamp(.875rem,2vw,1.25rem); --body-size:clamp(.75rem,1.4vw,1.125rem);
--small-size:clamp(.65rem,1vw,.875rem); --mono-size:clamp(.6rem,.95vw,.82rem);
--slide-padding:clamp(1.5rem,4vw,4rem); --content-gap:clamp(1rem,2vw,2rem);
--ease-out-expo:cubic-bezier(.16,1,.3,1); --duration-normal:.6s;
```

Breakpoints shrink the scale at small viewports and hide chrome entirely at very short ones:

```css
@media (max-height:700px) { :root { --slide-padding:clamp(.75rem,3vw,2rem); --title-size:clamp(1.25rem,4.5vw,2.5rem);
    --h2-size:clamp(1rem,3vw,1.75rem); --content-gap:clamp(.6rem,1.5vw,1.2rem); } }
@media (max-height:600px) { :root { --slide-padding:clamp(.5rem,2.5vw,1.5rem); --title-size:clamp(1.1rem,4vw,2rem);
    --body-size:clamp(.7rem,1.2vw,.95rem); }
  .nav-dots, .decorative, .hud-frame, .hud-bar { display:none; } }
@media (max-width:600px) { :root { --title-size:clamp(1.25rem,7vw,2.5rem); } }
@media (prefers-reduced-motion:reduce) {
  *, *::before, *::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.2s!important; }
  html { scroll-behavior:auto; }
}
```

### HUD chrome (slides 2–10 only; title & CTA omit it)

```css
.hud-frame { position:absolute; inset:clamp(.7rem,2vw,1.4rem); z-index:3; pointer-events:none; }
.hud-corner { position:absolute; width:14px; height:14px; border-color:var(--accent-cyan);
    border-style:solid; border-width:0; opacity:.7; filter:drop-shadow(0 0 4px var(--accent-glow-cyan)); }
.hud-corner.tl { top:0; left:0; border-top-width:1.5px; border-left-width:1.5px; }
.hud-corner.tr { top:0; right:0; border-top-width:1.5px; border-right-width:1.5px; }
.hud-corner.bl { bottom:0; left:0; border-bottom-width:1.5px; border-left-width:1.5px; }
.hud-corner.br { bottom:0; right:0; border-bottom-width:1.5px; border-right-width:1.5px; }
.hud-bar { position:absolute; top:clamp(.9rem,2.4vw,1.7rem); left:clamp(1.4rem,3.4vw,2.6rem); right:clamp(1.4rem,3.4vw,2.6rem);
    z-index:3; pointer-events:none; display:flex; justify-content:space-between; align-items:center;
    font-family:var(--font-mono); font-size:var(--mono-size); letter-spacing:.14em; text-transform:uppercase;
    color:rgba(0,255,204,.55); }
.hud-index { color:var(--accent-magenta); opacity:.75; }
```

`.hud-label` has no rule of its own — it inherits `.hud-bar`'s mono font/tracking/color; only `.hud-index` gets a
color override. Every content slide repeats the same four corner marks + one bar:

```html
<div class="hud-frame"><span class="hud-corner tl"></span><span class="hud-corner tr"></span><span class="hud-corner bl"></span><span class="hud-corner br"></span></div>
<div class="hud-bar"><span class="hud-label">SYS.MODULE // 01 OVERVIEW</span><span class="hud-index"></span></div>
<!-- controller fills .hud-index with "IDX 02/11" etc; write it empty -->
```

Vary the `.hud-label` text per slide: `SYS.MODULE // 0N NAME` where NAME is the slide's English tag (OVERVIEW,
CAPABILITIES, WORKFLOW, METRICS, COMPARISON, PIPELINE, ECOSYSTEM, INSIGHT, INTEGRATIONS…).

### Grid background, scanline, neon glow, glow border

```css
.slide::before { content:''; position:absolute; inset:0;
    background-image: linear-gradient(rgba(0,255,204,.03) 1px, transparent 1px),
                       linear-gradient(90deg, rgba(0,255,204,.03) 1px, transparent 1px);
    background-size:60px 60px; pointer-events:none; z-index:0; }
.slide > * { position:relative; z-index:1; }

@keyframes scanline { 0% { top:-5%; } 100% { top:105%; } }
.scanline { position:absolute; left:0; width:100%; height:2px;
    background:linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    opacity:.15; animation:scanline 4s linear infinite; pointer-events:none; z-index:2; }

.neon-text { color:var(--accent-cyan);
    text-shadow:0 0 10px var(--accent-glow-cyan), 0 0 40px var(--accent-glow-cyan), 0 0 80px rgba(0,255,204,.1); }
.glow-border { border:1px solid rgba(0,255,204,.2);
    box-shadow:0 0 15px rgba(0,255,204,.05), inset 0 0 15px rgba(0,255,204,.02); }
```

Every slide gets the faint cyan grid via `.slide::before` automatically (no markup needed) and one `<div
class="scanline"></div>` sweeping top-to-bottom. `.neon-text` is the glow treatment for a highlighted word/phrase
inline in a heading. `.glow-border` is a reusable outline treatment for pills/badges (used on `.cta-badge`).

### Beam border utility (rotating conic edge)

Reusable on any bordered card that should look like it has a chasing light tracing its edge (shipped on
`.bento-hero`, see Layout 3). Requires the `@property` registration once in `<style>` — see Hard rules.

```css
@property --beam-angle { syntax:'<angle>'; initial-value:0deg; inherits:false; }
.beam-border { position:relative; }
.beam-border::before { content:''; position:absolute; inset:-1px; border-radius:inherit; padding:1.5px;
    background:conic-gradient(from var(--beam-angle), transparent 0 62%, #00ffcc 78%, #ff00aa 92%, transparent 100%);
    -webkit-mask:linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor; mask-composite:exclude;
    animation:beamSpin 5s linear infinite; pointer-events:none; z-index:2; }
@keyframes beamSpin { to { --beam-angle:360deg; } }
@media (prefers-reduced-motion:reduce) { .beam-border::before { animation:none; } }
```

### Reveal delays (use d1–d7 classes, not inline style)

```css
.reveal { opacity:0; transform:translateY(28px);
    transition:opacity var(--duration-normal) var(--ease-out-expo), transform var(--duration-normal) var(--ease-out-expo); }
.slide.visible .reveal { opacity:1; transform:translateY(0); }
.slide.visible .reveal.d1 { transition-delay:.1s; }   /* … d2 .2s … through … */
.slide.visible .reveal.d7 { transition-delay:.7s; }
```

### Section header pattern (reused across most content layouts)

```css
.section-number { font-family:var(--font-mono); font-size:var(--small-size); font-weight:600;
    color:var(--accent-cyan); letter-spacing:.2em; }
.section-title { font-family:var(--font-display); font-size:var(--h2-size); font-weight:600; line-height:1.2; }
.section-sub { font-size:var(--body-size); color:var(--text-secondary); line-height:1.6; max-width:620px; }
```

```html
<div class="section-number reveal d1">02 / CAPABILITIES</div>
<h2 class="section-title reveal d2">核心能力</h2>
<!-- optional: <p class="section-sub reveal d3">…</p> — most layouts put the body grid/row directly after the title -->
```

Most content slides put this header directly at the top of `.slide-content`, followed by the layout body (see
Layouts 3–5, 7, 8, 10). The Overview layout (2) nests it inside the left copy column instead. The Quote layout (9)
omits it entirely, matching the fully-centered convention.

### JS FX contract

One controller IIFE drives navigation; a second IIFE drives per-slide effects; two more run the always-on
canvases. All four live in the single `<script>` tag.

**Reveal + one-shot FX dispatch:**
```js
var obs = new IntersectionObserver(function (entries) {
  entries.forEach(function (e) {
    if (e.isIntersecting) { e.target.classList.add('visible'); if (window.runFX) window.runFX(e.target); }
  });
}, { threshold: 0.5 });
slides.forEach(function (s) { obs.observe(s); });
```
`window.runFX(slide)` is guarded by `slide.dataset.fx` so it fires exactly once per slide, the first time it
crosses 50% visible:
```js
window.runFX = function (slide) {
  if (slide.dataset.fx) return;
  slide.dataset.fx = '1';
  runCounters(slide); runTyping(slide); runScramble(slide);
};
```

- **Counters** — every `.count` element with `data-count="N"` + optional `data-suffix="…"` animates 0 → N over
  1.2s with an ease-out-cubic curve via `requestAnimationFrame`; `prefers-reduced-motion` sets the final value
  immediately. Used by `.bento-stat .count` and `.gauge-center .count`.
- **Typing** — every `[data-type="…"]` element in the slide is typed sequentially (one finishes before the next
  starts), 28ms/char. `.term-line` elements type into `textContent` and toggle an `.active` class (CSS `::after`
  blinking block caret) while typing; non-terminal elements (e.g. the title subtitle) type into `innerHTML` with
  an appended `<span class="cursor"></span>` that stays after typing finishes. Reduced motion sets full text
  immediately (still keeps the trailing cursor on non-term elements).
- **Scramble** — every `.scramble` element decodes its `data-text` left-to-right over 900ms, filling unrevealed
  characters with random glyphs from `"!<>-_\/[]{}—=+*^?#0123456789"`. Reduced motion sets final text immediately.
  Used by `.hud-strip .scramble` tag pills.
- **Spotlight + 3D tilt** — bound once at init (not gated by the IntersectionObserver, since it's a hover
  interaction, not a reveal): every `.spot-card` tracks `pointermove` to set `--mx`/`--my` custom properties
  consumed by its `::before` radial-gradient spotlight; cards additionally carrying `.tilt` get a
  `perspective(700px) rotateX() rotateY()` transform proportional to cursor position, cleared on `pointerleave`.
  Skipped under `prefers-reduced-motion`.
- **`#particles` starfield canvas** — `position:fixed; inset:0; z-index:0` behind ALL slides, running
  continuously for the whole deck (not gated per-slide). Hand-written 2D-canvas star field kept deliberately
  quiet so it doesn't fight the grid + scanline + nebula layers: ~38 sparse, small, crisp stars (mostly cyan,
  ~1-in-6 magenta), very slow drift with edge-wrap, gentle sine twinkle, and a tight `source-over` halo (r×3 —
  **no additive `lighter` blending, no link lines, no click-to-add**; those were the old constellation's
  "too busy / washed-out" tells). Cursor proximity (≤160px) gives a subtle brighten only. DPR-capped at 1.5,
  ~45fps throttle, pauses on `document.hidden`. Reduced motion: zero velocity + no twinkle + one static draw,
  no RAF loop.
- **`#nebula` WebGL canvas — title slide ONLY.** Hand-written WebGL1 fragment shader (MIT `snoise`-based domain-
  warped fBm) rendering a cyan/magenta soft cloud mass behind the title copy. Needs explicit `width:100%;
  height:100%` in CSS (a canvas is a replaced element — `inset:0` alone won't size its backing store). An
  `IntersectionObserver` (threshold .15) on the title slide starts/stops the render loop so the GPU work only
  runs while slide 1 is on screen. If `getContext('webgl')` fails, `document.body.classList.add('no-webgl')`
  reveals the CSS radial-gradient fallback already baked into `.title-slide`'s background. Reduced motion draws
  exactly one static frame, no loop.

---

## Layout 1: Title / Kinetic Headline

**Use for:** The opening cover only. Centered, WebGL nebula backdrop behind a character-by-character kinetic
headline. Drops the HUD chrome entirely (no `.hud-frame`/`.hud-bar`) — only the scanline overlay remains.

**CSS:**
```css
.title-slide { background:
    radial-gradient(ellipse at 30% 70%, rgba(0,255,204,.08) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 30%, rgba(255,0,170,.06) 0%, transparent 50%),
    var(--bg-primary); }
#nebula { position:absolute; inset:0; width:100%; height:100%; z-index:0; display:block; }
body.no-webgl #nebula { display:none; }
.title-slide .slide-content { align-items:center; text-align:center; gap:var(--content-gap); }
.title-label { font-family:var(--font-body); font-size:var(--small-size); font-weight:500;
    letter-spacing:.3em; text-transform:uppercase; color:var(--accent-cyan); opacity:.8; }
.title-main { font-family:var(--font-display); font-size:var(--title-size); font-weight:700;
    line-height:1.1; letter-spacing:-.02em; }
/* Kinetic headline — each char rises + de-blurs, staggered by --i */
.kin span { display:inline-block; opacity:0; transform:translateY(.6em); filter:blur(8px); }
.kin span.space { width:.32em; }
.slide.visible .kin span { animation:charRise .7s var(--ease-out-expo) both; animation-delay:calc(var(--i) * 45ms); }
@keyframes charRise { from { opacity:0; transform:translateY(.6em); filter:blur(8px); } to { opacity:1; transform:translateY(0); filter:blur(0); } }
/* Neon flicker on the highlighted word after it rises — mark those spans .flick */
.slide.visible .kin span.flick { animation:charRise .7s var(--ease-out-expo) both, neonFlicker 2.4s .9s ease-in-out 1; }
@keyframes neonFlicker { 0%,68%,100% { opacity:1; } 70% { opacity:.35; } 72% { opacity:1; } 74% { opacity:.5; } 76% { opacity:1; } 78% { opacity:.72; } 80% { opacity:1; } }
@media (prefers-reduced-motion:reduce) { .kin span { opacity:1!important; transform:none!important; filter:none!important; } }
.title-sub { font-size:var(--subtitle-size); color:var(--text-secondary); max-width:620px; line-height:1.6; min-height:3.2em; }
.title-badge { display:inline-flex; align-items:center; gap:clamp(.3rem,.8vw,.6rem);
    padding:clamp(.3rem,.8vw,.5rem) clamp(.8rem,1.5vw,1.2rem); border-radius:100px; font-size:var(--small-size); font-weight:500;
    background:rgba(0,255,204,.08); border:1px solid rgba(0,255,204,.2); color:var(--accent-cyan); }
```

**HTML:**
```html
<section class="slide title-slide" aria-label="Title">
    <canvas id="nebula"></canvas>
    <div class="scanline"></div>
    <div class="slide-content">
        <div class="title-label reveal d1">ANTHROPIC PRESENTS</div>
        <h1 class="title-main kin reveal d2" aria-label="Claude Code">
            <span class="flick neon-text" style="--i:0">C</span><span class="flick neon-text" style="--i:1">l</span><span class="flick neon-text" style="--i:2">a</span><span class="flick neon-text" style="--i:3">u</span><span class="flick neon-text" style="--i:4">d</span><span class="flick neon-text" style="--i:5">e</span><span class="space" style="--i:6"> </span><span style="--i:7">C</span><span style="--i:8">o</span><span style="--i:9">d</span><span style="--i:10">e</span>
            <!-- one <span> per character (incrementing --i), a bare space gets class="space"; wrap the word to glow in .flick.neon-text spans -->
        </h1>
        <p class="title-sub reveal d3" data-type="终端中的 AI 编程助手，理解你的整个代码库&#10;用自然语言完成复杂的工程任务"><span class="cursor"></span></p>
        <div class="title-badge reveal d4"><span>Powered by Claude Opus 4</span></div>
    </div>
</section>
```

The `<span class="cursor"></span>` inside `.title-sub` is a placeholder; the typing FX clears/rebuilds
`innerHTML` and re-appends the caret as it types — leave it there in the source HTML.

---

## Layout 2: Terminal Overview (2-col copy + typed terminal)

**Use for:** The opening/overview content slide — a section intro paired with a simulated terminal session that
types out a command + response. 2-column grid; collapses to 1 column under 820px.

**CSS:**
```css
.overview-slide .slide-content { display:grid; grid-template-columns:1fr 1.15fr; gap:clamp(1.2rem,3vw,3rem); align-items:center; }
@media (max-width:820px) { .overview-slide .slide-content { grid-template-columns:1fr; } }
.overview-copy { display:flex; flex-direction:column; gap:clamp(.7rem,1.6vw,1.2rem); }
.term-window { background:rgba(0,0,0,.55); border:1px solid rgba(0,255,204,.15); border-radius:clamp(8px,1.2vw,14px);
    overflow:hidden; box-shadow:0 0 30px rgba(0,255,204,.06), inset 0 0 20px rgba(0,0,0,.4); }
.term-head { display:flex; align-items:center; gap:clamp(.5rem,1.2vw,.9rem);
    padding:clamp(.5rem,1.1vw,.8rem) clamp(.7rem,1.4vw,1.1rem); border-bottom:1px solid rgba(0,255,204,.1); background:rgba(255,255,255,.02); }
.term-dots { display:flex; gap:6px; } .term-dots i { width:11px; height:11px; border-radius:50%; display:block; }
.term-title { font-family:var(--font-mono); font-size:var(--mono-size); color:var(--text-secondary); margin-left:.4rem; }
.term-body { padding:clamp(.8rem,1.8vw,1.4rem); font-family:var(--font-mono); font-size:var(--mono-size); line-height:1.85;
    min-height:clamp(11rem,26vh,15rem); }
.term-line { white-space:pre-wrap; min-height:1.85em; color:var(--text-primary); }
.term-line.cmd::first-letter { color:var(--accent-cyan); }
.term-line.cmt { color:#6b7280; } .term-line.usr { color:var(--accent-cyan); } .term-line.rsp { color:var(--accent-magenta); }
.term-line.active::after { content:''; display:inline-block; width:8px; height:1.05em; background:var(--accent-cyan);
    vertical-align:text-bottom; margin-left:2px; animation:blink 1s step-end infinite; box-shadow:0 0 8px var(--accent-glow-cyan); }
```

**HTML** (inside `.slide-content` of the standard HUD wrapper):
```html
<div class="overview-copy">
    <div class="section-number reveal d1">01 / OVERVIEW</div>
    <h2 class="section-title reveal d2">不只是代码补全，<br>而是<span class="neon-text">编程搭档</span></h2>
    <p class="section-sub reveal d3">Claude Code 直接运行在你的终端中，深度理解项目上下文……</p>
</div>
<div class="term-window reveal d4">
    <div class="term-head">
        <span class="term-dots"><i style="background:#ff5f56"></i><i style="background:#ffbd2e"></i><i style="background:#27c93f"></i></span>
        <span class="term-title">claude — zsh</span>
    </div>
    <div class="term-body">
        <div class="term-line cmd" data-type="$ npm install -g @anthropic-ai/claude-code"></div>
        <div class="term-line cmt" data-type="# 在任意项目目录中启动"></div>
        <div class="term-line cmd" data-type="$ cd your-project &amp;&amp; claude"></div>
        <div class="term-line" data-type=" "></div>
        <div class="term-line usr" data-type="&gt; 帮我把这个模块重构为 TypeScript"></div>
        <div class="term-line rsp" data-type="✦ 已分析 47 个文件，开始重构…"></div>
        <!-- 4–6 lines: mix .cmd (traffic-light prompt), .cmt (dim comment), .usr (user turn), .rsp (agent reply) -->
    </div>
</div>
```

`.term-line` rows type in document order (part of the shared sequential `[data-type]` queue), each showing the
blinking `.active` caret only while it's the one currently typing.

---

## Layout 3: Bento Grid (hero cell + 4 cells, capabilities)

**Use for:** 5 capabilities/features where one deserves outsized emphasis. A 4×2 grid where the hero spans 2×2
with a chasing `.beam-border` edge and an optional live counter stat; the other 4 cells are single-height.

**CSS:**
```css
.capabilities-slide .slide-content { gap:clamp(.8rem,2vw,1.5rem); }
.bento-grid { display:grid; grid-template-columns:repeat(4,1fr); grid-template-rows:repeat(2,1fr);
    gap:clamp(.5rem,1vw,.9rem); max-width:1180px; width:100%; margin:0 auto; height:clamp(20rem,62vh,34rem); }
@media (max-width:820px) { .bento-grid { grid-template-columns:repeat(2,1fr); grid-template-rows:repeat(3,1fr); height:auto; } }
.bento-cell { background:var(--bg-card); border:1px solid rgba(0,255,204,.12); border-radius:clamp(10px,1.2vw,16px);
    padding:clamp(.8rem,1.6vw,1.4rem); display:flex; flex-direction:column; justify-content:center; gap:clamp(.3rem,.7vw,.5rem);
    transition:border-color .3s, box-shadow .3s, transform .3s; overflow:hidden; }
.bento-cell:hover { border-color:rgba(0,255,204,.4); box-shadow:0 0 24px rgba(0,255,204,.08); transform:translateY(-3px); }
.bento-hero { grid-column:span 2; grid-row:span 2; justify-content:flex-end; gap:clamp(.4rem,1vw,.8rem); }
@media (max-width:820px) { .bento-hero { grid-column:span 2; grid-row:span 1; } }
.bento-icon { color:var(--accent-cyan); line-height:0; }
.bento-icon svg { width:clamp(1.3rem,2.6vw,1.9rem); height:clamp(1.3rem,2.6vw,1.9rem); stroke:var(--accent-cyan); fill:none;
    stroke-width:1.75; stroke-linecap:round; stroke-linejoin:round; filter:drop-shadow(0 0 8px var(--accent-glow-cyan)); }
.bento-hero .bento-icon svg { width:clamp(2rem,4vw,3rem); height:clamp(2rem,4vw,3rem); }
.bento-cell h3 { font-family:var(--font-display); font-size:var(--h3-size); font-weight:600; }
.bento-hero h3 { font-size:clamp(1.3rem,3vw,2.2rem); }
.bento-cell p { font-size:var(--small-size); color:var(--text-secondary); line-height:1.5; }
.bento-stat { font-family:var(--font-mono); font-size:var(--small-size); color:var(--text-secondary); margin-top:clamp(.2rem,.6vw,.5rem); }
.bento-stat .count { color:var(--accent-cyan); font-weight:700; font-size:clamp(1rem,2.2vw,1.6rem); text-shadow:0 0 12px var(--accent-glow-cyan); }
```

**HTML** (inside `.slide-content`, after `.section-number`/`.section-title`):
```html
<div class="bento-grid">
    <div class="bento-cell bento-hero beam-border reveal d3">
        <div class="bento-icon"><svg viewBox="0 0 24 24"><path d="M20 10a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2.5a1 1 0 0 1-.8-.4l-.9-1.2A1 1 0 0 0 14 3h-2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z"></path></svg></div>
        <h3>全项目理解</h3>
        <p>自动索引整个代码库，理解文件关系、架构模式与依赖，让每次改动都在全局语境中进行。</p>
        <div class="bento-stat"><span class="count" data-count="200" data-suffix="K">0</span>+ 行代码上下文</div>
    </div>
    <div class="bento-cell reveal d4">
        <div class="bento-icon"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6…"></path></svg></div>
        <h3>自主编辑</h3>
        <p>直接读写文件、跑命令、执行测试。</p>
    </div>
    <!-- 4 plain cells total, stagger d4–d7; only the hero gets .beam-border + .bento-stat -->
</div>
```

---

## Layout 4: Spotlight Cards (3-step workflow)

**Use for:** 3-step (or 3-item) processes shown as equal cards with a cursor-tracking radial spotlight and,
optionally, `.tilt` 3D pointer-following rotation. Big outlined step number behind the icon/copy.

**CSS:**
```css
.workflow-slide .slide-content { gap:clamp(1rem,2.4vw,2rem); }
.spot-row { display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(.7rem,1.6vw,1.3rem); }
@media (max-width:820px) { .spot-row { grid-template-columns:1fr; } }
.spot-card { position:relative; background:var(--bg-card); border:1px solid rgba(0,255,204,.12);
    border-radius:clamp(12px,1.4vw,18px); padding:clamp(1.1rem,2.4vw,2rem); display:flex; flex-direction:column;
    gap:clamp(.4rem,1vw,.8rem); overflow:hidden; transform-style:preserve-3d;
    transition:border-color .3s, box-shadow .3s, transform .15s ease-out; }
.spot-card::before { content:''; position:absolute; inset:0; z-index:0; opacity:0; transition:opacity .4s;
    background:radial-gradient(240px circle at var(--mx,50%) var(--my,50%), rgba(0,255,204,.14), transparent 60%); }
.spot-card:hover { border-color:rgba(0,255,204,.35); box-shadow:0 12px 40px rgba(0,0,0,.3); }
.spot-card:hover::before { opacity:1; }
.spot-card > * { position:relative; z-index:1; }
.spot-step { font-family:var(--font-display); font-size:clamp(2rem,5vw,3.6rem); font-weight:700; line-height:1;
    color:transparent; -webkit-text-stroke:1px rgba(0,255,204,.35); }
.spot-icon { color:var(--accent-cyan); line-height:0; }
.spot-icon svg { width:clamp(1.5rem,3vw,2.2rem); height:clamp(1.5rem,3vw,2.2rem); stroke:var(--accent-cyan); fill:none;
    stroke-width:1.75; stroke-linecap:round; stroke-linejoin:round; filter:drop-shadow(0 0 8px var(--accent-glow-cyan)); }
.spot-card h3 { font-family:var(--font-display); font-size:var(--h3-size); font-weight:600; }
.spot-card p { font-size:var(--small-size); color:var(--text-secondary); line-height:1.55; }
```

**HTML** (inside `.slide-content`, after `.section-number`/`.section-title`):
```html
<div class="spot-row">
    <div class="spot-card tilt reveal d3">
        <div class="spot-step">01</div>
        <div class="spot-icon"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg></div>
        <h3>探索 Explore</h3>
        <p>扫描代码库、检索相关文件，构建对任务全貌与约束的完整理解。</p>
    </div>
    <!-- 3 cards, stagger d3–d5; always add .tilt alongside .spot-card for the 3D pointer effect -->
</div>
```

---

## Layout 5: Data HUD Gauges + Scramble Strip (metrics)

**Use for:** 2–4 headline percentage metrics as animated SVG ring gauges, plus a pill strip of scramble-decoded
tag keywords underneath. Fully centered.

**CSS:**
```css
.metrics-slide .slide-content { gap:clamp(1rem,2.6vw,2.2rem); align-items:center; }
.gauge-row { display:flex; justify-content:center; gap:clamp(1.2rem,4vw,4rem); flex-wrap:wrap; }
.gauge { position:relative; display:flex; flex-direction:column; align-items:center; gap:clamp(.4rem,1vw,.8rem); }
.gauge-ring { position:relative; width:clamp(8rem,15vw,11rem); height:clamp(8rem,15vw,11rem); }
.gauge-ring svg { width:100%; height:100%; transform:rotate(-90deg); }
.gauge-ring .track { fill:none; stroke:rgba(0,255,204,.12); stroke-width:8; }
.gauge-ring .val { fill:none; stroke-width:8; stroke-linecap:round; stroke-dasharray:0 100;
    transition:stroke-dasharray 1.4s var(--ease-out-expo); }
.slide.visible .gauge-ring .val { stroke-dasharray:var(--val) 100; }
.gauge-ring .val.cyan { stroke:var(--accent-cyan); filter:drop-shadow(0 0 6px var(--accent-glow-cyan)); }
.gauge-ring .val.magenta { stroke:var(--accent-magenta); filter:drop-shadow(0 0 6px var(--accent-glow-magenta)); }
.gauge-ring .val.blue { stroke:var(--accent-blue); filter:drop-shadow(0 0 6px rgba(0,170,255,.35)); }
.gauge-center { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.gauge-center .count { font-family:var(--font-display); font-size:clamp(1.4rem,3.4vw,2.4rem); font-weight:700; color:var(--text-primary); }
.gauge-label { font-size:var(--small-size); color:var(--text-secondary); text-align:center; max-width:9rem; line-height:1.4; }
.hud-strip { display:flex; flex-wrap:wrap; justify-content:center; gap:clamp(.5rem,1.6vw,1.4rem);
    padding:clamp(.6rem,1.4vw,1rem) clamp(.9rem,2vw,1.6rem); border:1px solid rgba(0,255,204,.15);
    border-radius:100px; background:rgba(0,0,0,.3); }
.hud-strip span { font-family:var(--font-mono); font-size:var(--mono-size); letter-spacing:.16em; color:var(--accent-cyan); }
.hud-strip .sep { color:rgba(0,255,204,.3); }
```

**HTML** (inside `.slide-content`, after `.section-number`/`.section-title`):
```html
<div class="gauge-row reveal d3">
    <div class="gauge">
        <div class="gauge-ring" style="--val:92">
            <svg viewBox="0 0 120 120"><circle class="track" cx="60" cy="60" r="52"></circle><circle class="val cyan" cx="60" cy="60" r="52" pathLength="100"></circle></svg>
            <div class="gauge-center"><span class="count" data-count="92" data-suffix="%">0</span></div>
        </div>
        <div class="gauge-label">任务一次通过</div>
    </div>
    <!-- 3 gauges, cycle val color cyan → magenta → blue; pathLength="100" lets --val be a plain 0–100 number -->
</div>
<div class="hud-strip reveal d4">
    <span class="scramble" data-text="AGENTIC">AGENTIC</span><span class="sep">·</span>
    <span class="scramble" data-text="CONTEXT-AWARE">CONTEXT-AWARE</span><span class="sep">·</span>
    <span class="scramble" data-text="TOOL-USE">TOOL-USE</span>
    <!-- 3–5 tags separated by .sep "·"; the .scramble decode reads from data-text -->
</div>
```

---

## Layout 6: VS Compare Panels (comparison)

**Use for:** Before/after or old-way/new-way comparisons. Two angled panels (opposing `clip-path` slants) flank a
circular `VS` badge; the "new" panel gets a cyan border glow, the "old" panel is muted.

**CSS:**
```css
.comparison-slide .slide-content { gap:clamp(1rem,2.4vw,1.8rem); }
.vs-layout { display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:clamp(.6rem,2vw,1.5rem);
    max-width:1100px; width:100%; margin:0 auto; }
@media (max-width:820px) { .vs-layout { grid-template-columns:1fr; } .vs-badge { margin:-.4rem auto; } }
.vs-panel { border-radius:clamp(12px,1.4vw,18px); padding:clamp(1rem,2.4vw,2rem); display:flex; flex-direction:column;
    gap:clamp(.5rem,1.2vw,.9rem); background:var(--bg-card); }
.vs-panel.old { border:1px solid rgba(255,255,255,.12); clip-path:polygon(0 2%, 100% 0, 100% 100%, 0 100%); }
.vs-panel.new { border:1px solid rgba(0,255,204,.35); box-shadow:0 0 26px rgba(0,255,204,.08);
    clip-path:polygon(0 0, 100% 2%, 100% 100%, 0 100%); }
.vs-panel h3 { font-family:var(--font-display); font-size:var(--h3-size); font-weight:600; margin-bottom:clamp(.2rem,.6vw,.4rem); }
.vs-panel.old h3 { color:var(--text-secondary); } .vs-panel.new h3 { color:var(--accent-cyan); }
.vs-item { display:flex; align-items:flex-start; gap:.5rem; font-size:var(--small-size); line-height:1.5; }
.vs-item svg { width:1.05em; height:1.05em; flex-shrink:0; margin-top:.15em; fill:none; stroke-width:2.4;
    stroke-linecap:round; stroke-linejoin:round; }
.vs-panel.old .vs-item { color:var(--text-secondary); } .vs-panel.old .vs-item svg { stroke:rgba(255,255,255,.35); }
.vs-panel.new .vs-item svg { stroke:var(--accent-cyan); filter:drop-shadow(0 0 4px var(--accent-glow-cyan)); }
.vs-badge { width:clamp(3rem,7vw,4.6rem); height:clamp(3rem,7vw,4.6rem); border-radius:50%; display:grid;
    place-items:center; font-family:var(--font-display); font-weight:700; font-size:clamp(.9rem,2vw,1.3rem);
    color:var(--text-primary); background:var(--bg-primary); position:relative; z-index:2; box-shadow:0 0 24px rgba(255,0,170,.3); }
.vs-badge::before { content:''; position:absolute; inset:-2px; border-radius:50%; z-index:-1;
    background:linear-gradient(135deg, var(--accent-magenta), var(--accent-cyan)); }
.vs-badge::after { content:''; position:absolute; inset:2px; border-radius:50%; z-index:-1; background:var(--bg-primary); }
```

**HTML** (inside `.slide-content`, after `.section-number`/`.section-title`):
```html
<div class="vs-layout">
    <div class="vs-panel old reveal d3">
        <h3>传统工作流</h3>
        <div class="vs-item"><svg viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>在多个文档与页面间反复切换查资料</div>
        <!-- 3–4 items, all with the same X-mark svg -->
    </div>
    <div class="vs-badge reveal d4"><span>VS</span></div>
    <div class="vs-panel new reveal d5">
        <h3>Claude Code</h3>
        <div class="vs-item"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>一句自然语言，直达任务目标</div>
        <!-- 3–4 items, all with the same checkmark svg -->
    </div>
</div>
```

---

## Layout 7: Circuit Pipeline (5-node flow)

**Use for:** A 5-stage end-to-end pipeline/flow — circular icon nodes joined by marching-ant wires with a pulse
dot traveling each segment, plus a ring-pulse halo on every node (staggered by `--pd`).

**CSS:**
```css
.pipeline-slide .slide-content { gap:clamp(1.4rem,3.4vw,2.6rem); align-items:center; }
.circuit { display:flex; align-items:flex-start; justify-content:center; width:100%; max-width:1100px; }
.circuit-node { display:flex; flex-direction:column; align-items:center; gap:clamp(.4rem,1vw,.7rem); flex-shrink:0; width:clamp(4rem,9vw,6rem); }
.circuit-disc { position:relative; width:clamp(3rem,6vw,4.4rem); height:clamp(3rem,6vw,4.4rem); border-radius:50%;
    display:grid; place-items:center; background:rgba(0,255,204,.06); border:1px solid rgba(0,255,204,.4); color:var(--accent-cyan); }
.circuit-disc svg { width:45%; height:45%; stroke:var(--accent-cyan); fill:none; stroke-width:1.9; stroke-linecap:round; stroke-linejoin:round; }
.circuit-disc::after { content:''; position:absolute; inset:-4px; border-radius:50%; border:1px solid var(--accent-cyan);
    opacity:0; animation:ringPulse 2.6s ease-out infinite; animation-delay:var(--pd,0s); }
@keyframes ringPulse { 0% { transform:scale(.85); opacity:.7; } 70%,100% { transform:scale(1.5); opacity:0; } }
.circuit-label { font-size:var(--small-size); color:var(--text-secondary); text-align:center; }
.circuit-wire { position:relative; flex:1; height:2px; margin-top:clamp(1.5rem,3vw,2.2rem); min-width:clamp(1.5rem,4vw,4rem);
    background-image:linear-gradient(90deg, rgba(0,255,204,.5) 0 6px, transparent 6px 12px); background-size:12px 2px;
    animation:marching .7s linear infinite; }
@keyframes marching { to { background-position:12px 0; } }
.pulse-dot { position:absolute; top:50%; left:0; width:6px; height:6px; margin-top:-3px; border-radius:50%;
    background:var(--accent-cyan); box-shadow:0 0 8px var(--accent-glow-cyan); animation:pulseTravel 2.4s linear infinite; animation-delay:var(--dd,0s); }
@keyframes pulseTravel { 0% { left:0; opacity:0; } 12% { opacity:1; } 88% { opacity:1; } 100% { left:100%; opacity:0; } }
@media (prefers-reduced-motion:reduce) {
    .circuit-wire { animation:none; background-image:linear-gradient(90deg, rgba(0,255,204,.35), rgba(0,255,204,.35)); }
    .pulse-dot, .circuit-disc::after { display:none; }
}
```

**HTML** (inside `.slide-content`, after `.section-number`/`.section-title`):
```html
<div class="circuit reveal d3">
    <div class="circuit-node">
        <div class="circuit-disc" style="--pd:0s"><svg viewBox="0 0 24 24"><path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0-6 0"></path></svg></div>
        <div class="circuit-label">需求</div>
    </div>
    <div class="circuit-wire"><span class="pulse-dot" style="--dd:0s"></span></div>
    <div class="circuit-node">
        <div class="circuit-disc" style="--pd:.5s"><svg viewBox="0 0 24 24"><path d="M9 11H3v10h6z"></path></svg></div>
        <div class="circuit-label">计划</div>
    </div>
    <!-- 5 nodes total, each --pd/--dd stepping +.5s (0s, .5s, 1s, 1.5s, 2s); one .circuit-wire between every pair of nodes, none after the last -->
</div>
```

---

## Layout 8: Dual Marquee (ecosystem)

**Use for:** A scrolling "ecosystem/integrations wall" of names — two rows of an infinitely looping horizontal
ticker, scrolling opposite directions at different speeds, with a subset of items highlighted (`.hl`).

**CSS:**
```css
.ecosystem-slide .slide-content { gap:clamp(1.2rem,3vw,2.4rem); }
.marquee { overflow:hidden; width:100%;
    -webkit-mask:linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent);
            mask:linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent); }
.marquee-track { display:flex; width:max-content; gap:clamp(1rem,2.6vw,2.2rem); align-items:center;
    font-family:var(--font-display); font-weight:500; font-size:clamp(1.4rem,3.5vw,2.6rem); color:rgba(226,232,240,.25); }
.marquee.row1 .marquee-track { animation:marqueeL 30s linear infinite; }
.marquee.row2 .marquee-track { animation:marqueeR 38s linear infinite; }
@keyframes marqueeL { to { transform:translateX(-50%); } }
@keyframes marqueeR { from { transform:translateX(-50%); } to { transform:translateX(0); } }
.marquee-track .diamond { color:var(--accent-cyan); font-size:.55em; opacity:.7; }
.marquee-track .hl { color:var(--accent-cyan); text-shadow:0 0 14px var(--accent-glow-cyan); }
@media (prefers-reduced-motion:reduce) { .marquee-track { animation:none!important; } }
```

**HTML** (inside `.slide-content`, after `.section-number`/`.section-title`):
```html
<div class="marquee row1 reveal d3">
    <div class="marquee-track">
        <span>MCP</span><span class="diamond">◆</span><span>Hooks</span><span class="diamond">◆</span><span class="hl">Skills</span><span class="diamond">◆</span>
        <!-- one full item list, THEN the exact same list repeated once more (for the seamless -50% loop) -->
    </div>
</div>
<div class="marquee row2 reveal d4">
    <div class="marquee-track">
        <!-- a differently-ordered item list, doubled the same way; row2 scrolls the opposite direction (marqueeR) and slower (38s vs 30s) -->
    </div>
</div>
```

The doubled track is mandatory — `translateX(-50%)` only loops seamlessly because the visible half and the
duplicate half are pixel-identical.

---

## Layout 9: Glitch Quote

**Use for:** A single punchy quote/insight slide. Fully centered; omits the `.section-number`/`.section-title`
header entirely. The quote text glitches via two color-split `::before`/`::after` layers reading `data-text`.

**CSS:**
```css
.quote-slide .slide-content { align-items:center; text-align:center; gap:clamp(1rem,2.6vw,2rem); }
.glitch { position:relative; font-family:var(--font-display); font-weight:600; font-size:clamp(1.3rem,4vw,2.8rem);
    line-height:1.35; max-width:16em; color:var(--text-primary); }
.glitch::before, .glitch::after { content:attr(data-text); position:absolute; inset:0; overflow:hidden; clip-path:inset(0 0 0 0); }
.glitch::before { color:var(--accent-cyan); animation:glitchTop 5s infinite steps(1); }
.glitch::after { color:var(--accent-magenta); animation:glitchBot 5s infinite steps(1); }
@keyframes glitchTop {
    0%,90%,100% { transform:translate(0,0); clip-path:inset(0 0 100% 0); opacity:0; }
    91% { transform:translate(-2px,-2px); clip-path:inset(0 0 55% 0); opacity:.8; }
    93% { transform:translate(3px,1px); clip-path:inset(0 0 62% 0); opacity:.8; }
    95% { transform:translate(-1px,0); clip-path:inset(0 0 58% 0); opacity:.8; }
}
@keyframes glitchBot {
    0%,90%,100% { transform:translate(0,0); clip-path:inset(100% 0 0 0); opacity:0; }
    92% { transform:translate(2px,2px); clip-path:inset(52% 0 0 0); opacity:.8; }
    94% { transform:translate(-3px,-1px); clip-path:inset(46% 0 0 0); opacity:.8; }
    96% { transform:translate(1px,0); clip-path:inset(50% 0 0 0); opacity:.8; }
}
@media (prefers-reduced-motion:reduce) { .glitch::before, .glitch::after { display:none; } }
.quote-attr { font-family:var(--font-mono); font-size:var(--small-size); letter-spacing:.14em; color:var(--accent-cyan); text-transform:uppercase; }
```

**HTML** (inside `.slide-content`; note this slide keeps the HUD frame/bar but the content itself skips the
section header):
```html
<blockquote class="glitch reveal d2" data-text="最好的工程师不是写代码最快的人，而是最会调度智能的人。">最好的工程师不是写代码最快的人，而是最会调度智能的人。</blockquote>
<div class="quote-attr reveal d4">// THE FUTURE OF ENGINEERING</div>
```

`data-text` MUST exactly duplicate the element's text content — the glitch layers render it via `content:
attr(data-text)`, so any mismatch shows stale text flashing over the real quote.

---

## Layout 10: Orbit Scene (integrations)

**Use for:** A tool/product ecosystem radiating around a central core — two counter-rotating dashed rings each
carrying icon chips that stay visually upright (counter-rotation cancels the ring spin).

**CSS:**
```css
.integrations-slide .slide-content { align-items:center; gap:clamp(.8rem,2vw,1.4rem); }
.orbit-scene { position:relative; width:min(58vh,520px); height:min(58vh,520px); }
.orbit-core { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); z-index:3;
    width:clamp(5rem,14vw,7.5rem); height:clamp(5rem,14vw,7.5rem); border-radius:50%; display:flex; flex-direction:column;
    align-items:center; justify-content:center; gap:.2rem; background:rgba(0,255,204,.08); border:1px solid rgba(0,255,204,.5);
    box-shadow:0 0 40px rgba(0,255,204,.25), inset 0 0 20px rgba(0,255,204,.1); color:var(--accent-cyan); }
.orbit-core svg { width:clamp(1.4rem,3vw,2rem); height:clamp(1.4rem,3vw,2rem); stroke:var(--accent-cyan); fill:none;
    stroke-width:1.75; stroke-linecap:round; stroke-linejoin:round; }
.orbit-core span { font-family:var(--font-display); font-size:clamp(.6rem,1.3vw,.85rem); font-weight:600; }
.orbit-ring { position:absolute; top:50%; left:50%; border-radius:50%; border:1px dashed rgba(0,255,204,.2); }
.orbit-ring.r1 { width:55%; height:55%; transform:translate(-50%,-50%); animation:spin 26s linear infinite; }
.orbit-ring.r2 { width:100%; height:100%; transform:translate(-50%,-50%); animation:spin 40s linear infinite reverse; }
@keyframes spin { to { transform:translate(-50%,-50%) rotate(360deg); } }
/* item positions a chip at radius --r / angle --a; the inner wrappers
   cancel the position angle (static) and the ring spin (animated) so icons stay upright. */
.orbit-item { position:absolute; top:50%; left:50%; width:0; height:0; transform:rotate(var(--a)) translateX(var(--r)); }
.orbit-upright { position:absolute; transform:rotate(calc(-1 * var(--a))); }
.orbit-chip { width:clamp(2.4rem,5vw,3.2rem); height:clamp(2.4rem,5vw,3.2rem);
    margin:calc(clamp(2.4rem,5vw,3.2rem) / -2) 0 0 calc(clamp(2.4rem,5vw,3.2rem) / -2); border-radius:14px; display:grid;
    place-items:center; background:var(--bg-card); border:1px solid rgba(0,255,204,.25); color:var(--accent-cyan);
    box-shadow:0 0 18px rgba(0,0,0,.4); }
.orbit-ring.r1 .orbit-chip { animation:counterCW 26s linear infinite; }
.orbit-ring.r2 .orbit-chip { animation:counterCCW 40s linear infinite; }
@keyframes counterCW { to { transform:rotate(-360deg); } }
@keyframes counterCCW { to { transform:rotate(360deg); } }
.orbit-chip svg { width:48%; height:48%; stroke:var(--accent-cyan); fill:none; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }
@media (prefers-reduced-motion:reduce) { .orbit-ring, .orbit-chip { animation:none!important; } }
```

**HTML** (inside `.slide-content`, after `.section-number`/`.section-title`):
```html
<div class="orbit-scene reveal d3">
    <div class="orbit-core">
        <svg viewBox="0 0 24 24"><path d="M12 3l1.6 4.6L18 9l-4.4 1.4L12 15l-1.6-4.6L6 9l4.4-1.4z"></path></svg>
        <span>Claude Code</span>
    </div>
    <div class="orbit-ring r1">
        <div class="orbit-item" style="--a:0deg;--r:calc(min(58vh,520px)*0.275)"><div class="orbit-upright"><div class="orbit-chip"><svg viewBox="0 0 24 24">…</svg></div></div></div>
        <!-- inner ring: 3 chips at --a 0/120/240deg, --r = min(58vh,520px)*0.275 -->
    </div>
    <div class="orbit-ring r2">
        <div class="orbit-item" style="--a:45deg;--r:calc(min(58vh,520px)*0.5)"><div class="orbit-upright"><div class="orbit-chip"><svg viewBox="0 0 24 24">…</svg></div></div></div>
        <!-- outer ring: 4 chips at --a 45/135/225/315deg, --r = min(58vh,520px)*0.5 -->
    </div>
</div>
```

Every `.orbit-item` needs BOTH wrapper divs — skipping `.orbit-upright` leaves the chip's icon rotating with the
ring instead of staying upright.

---

## Layout 11: CTA Closing

**Use for:** The final call-to-action / closing cover. Mirrors Layout 1's centered kinetic-headline treatment
(no WebGL nebula here, just the ambient radial-gradient background) plus an install command pill and a badge row.

**CSS:**
```css
.cta-slide { background:
    radial-gradient(ellipse at 50% 60%, rgba(0,255,204,.08) 0%, transparent 55%),
    radial-gradient(ellipse at 70% 30%, rgba(255,0,170,.06) 0%, transparent 50%),
    var(--bg-primary); }
.cta-slide .slide-content { align-items:center; text-align:center; gap:var(--content-gap); }
.cta-title { font-family:var(--font-display); font-size:clamp(2.4rem,8vw,6rem); font-weight:700; line-height:1.05; letter-spacing:-.02em; }
.cmd-pill { display:inline-flex; align-items:center; gap:.5rem; font-family:var(--font-mono); font-size:var(--body-size);
    padding:clamp(.6rem,1.4vw,.9rem) clamp(1rem,2.4vw,1.6rem); border-radius:100px; background:rgba(0,0,0,.45);
    border:1px solid rgba(0,255,204,.25); color:var(--text-primary); box-shadow:0 0 24px rgba(0,255,204,.08); }
.cmd-pill .prompt { color:var(--accent-cyan); }
.cta-badges { display:flex; gap:clamp(.6rem,1.6vw,1rem); flex-wrap:wrap; justify-content:center; }
.cta-badge { display:inline-flex; align-items:center; gap:.45rem; font-size:var(--small-size); font-weight:500;
    padding:clamp(.4rem,1vw,.6rem) clamp(.9rem,1.8vw,1.3rem); border-radius:100px; color:var(--accent-cyan); }
.cta-badge svg { width:1.05em; height:1.05em; stroke:var(--accent-cyan); fill:none; stroke-width:1.9; stroke-linecap:round; stroke-linejoin:round; }
.cta-foot { font-size:var(--small-size); color:var(--text-secondary); letter-spacing:.08em; }
```

**HTML** (no HUD chrome, same as Title):
```html
<section class="slide cta-slide" aria-label="Get started">
    <div class="scanline"></div>
    <div class="slide-content">
        <div class="title-label reveal d1">START BUILDING</div>
        <h2 class="cta-title kin reveal d2" aria-label="开始构建">
            <span class="flick neon-text" style="--i:0">开</span><span class="flick neon-text" style="--i:1">始</span><span style="--i:2">构</span><span style="--i:3">建</span>
        </h2>
        <div class="cmd-pill reveal d3"><span class="prompt">$</span> npm install -g @anthropic-ai/claude-code</div>
        <div class="cta-badges reveal d4">
            <a class="cta-badge glow-border" href="#"><svg viewBox="0 0 24 24">…</svg>Docs</a>
            <a class="cta-badge glow-border" href="#"><svg viewBox="0 0 24 24">…</svg>GitHub</a>
        </div>
        <div class="cta-foot reveal d5">// 终端中的 AI 编程助手 · Powered by Claude Opus 4</div>
    </div>
</section>
```

Reuses `.title-label`/`.kin`/`.neon-text`/`.flick` from Layout 1 — the CTA is the title layout's mirror image at
the end of the deck, so keep both slides' kinetic-headline markup structurally identical.

---

## Layout Selection Guide

| Content Type | Recommended Layout |
|---|---|
| Opening cover | **Title / Kinetic Headline** (Layout 1) |
| Section/opening intro + live demo feel | **Terminal Overview** (Layout 2) |
| 5 capabilities, one emphasized | **Bento Grid** (Layout 3) |
| 3-step process / workflow | **Spotlight Cards** (Layout 4) |
| 2–4 headline percentage metrics | **Data HUD Gauges** (Layout 5) |
| Before/after, old-way/new-way | **VS Compare Panels** (Layout 6) |
| 5-stage end-to-end pipeline | **Circuit Pipeline** (Layout 7) |
| Ecosystem / integration wall of names | **Dual Marquee** (Layout 8) |
| Executive quote / bold statement | **Glitch Quote** (Layout 9) |
| Tool/product ecosystem around a core | **Orbit Scene** (Layout 10) |
| Closing / call-to-action cover | **CTA Closing** (Layout 11) |

**Rule: never use plain left-aligned bullet lists.** Always wrap content in one of these layouts. If content
doesn't fit any layout, default to **Bento Grid** (Layout 3) or **Spotlight Cards** (Layout 4) when unsure.
