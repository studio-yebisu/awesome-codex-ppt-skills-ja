# re:Invent Keynote (v2) — Layout Patterns Reference

This is the layout reference for **style #2 — re:Invent Keynote**. Extracted from the shipped
`preview/02-reinvent-keynote.html`. Use these CSS classes and HTML skeletons when generating
re:Invent Keynote presentations.

**Read this file during Step 5 (generation) when the chosen style is #2 re:Invent Keynote.**

The full design-system CSS lives in the `<head>` of the preview file — copy it into every deck. When using
parallel generation (8+ slides), the framework agent emits the head + controller and batch agents write ONLY
`<section class="slide …">…</section>` blocks between them — never add a second `<style>` or `<script>`.

## Hard rules

- **Icons:** `<i data-lucide="name"></i>` only. NEVER emoji. The controller calls `lucide.createIcons()`.
- **Reveal stagger:** add `reveal d1`…`reveal d7` to elements you want animated into view in sequence.
- **One `<section>` = one slide = `100vh`.** Never exceed it. Copy is tuned for 1280×620+.
- **Colors via classes/vars only.** Up = green `.up`, down = rose `.down`, caution = amber `.warn`.
- **Leave chrome auto-fields EMPTY.** The controller fills `.slide-index` (`NN / NN`) and the
  `.slide-progress` pip row. Write them as empty elements.
- Every CONTENT slide MUST carry the standard chrome (frame + header + footer + progress). The
  cover and gradient-backdrop slides (title / divider / outlook) intentionally drop some chrome — see
  each layout below.

---

## Common Elements

### Theme tokens (defined in `:root`)

```css
--bg-primary:#0A0A0A; --bg-title:#0B0015;
--accent-purple:#8B5CF6; --accent-pink:#D946EF; --accent-blue:#3B82F6; --accent-orange:#FF9900;
--up:#34D399; --warn:#FBBF24; --down:#F472B6;            /* delta semantics */
--text-primary:#FFF; --text-secondary:rgba(255,255,255,.55); --text-faint:rgba(255,255,255,.38);
--card-bg:rgba(139,92,246,.07); --card-border:rgba(139,92,246,.2); --card-border-hover:rgba(139,92,246,.45);
--frame-border:rgba(139,92,246,.16); --hairline:rgba(255,255,255,.1);
--grad-accent:linear-gradient(135deg,#a78bfa,#e879f9,#f472b6);
--grad-bar:linear-gradient(90deg,var(--accent-purple),var(--accent-pink),var(--accent-orange));
--font-display:'Urbanist',sans-serif; --font-body:'Albert Sans',sans-serif;
--content-max:min(92vw,1180px); --content-gap:clamp(.8rem,2vw,1.8rem);
```

Fonts: **Urbanist** (display) + **Albert Sans** (body), loaded in the head. All type/spacing uses
`clamp()`; four viewport breakpoints (`max-height` 700/600/500 + `max-width` 600) shrink the scale and
collapse multi-column grids to one column. At `max-height:600px` orbs and pips auto-hide.

### Standard content-slide wrapper (use for every content layout)

Every content slide is the same shell; only the body block (between `.section-head` and the closing
`.slide-content`) changes per layout.

```html
<section class="slide content-slide" aria-label="SLIDE LABEL">
    <!-- background: 1–2 floating orbs (vary size/position/anim per slide) -->
    <div class="floating-orb orb-purple" style="width:28vw;height:28vw;top:8%;right:6%;animation:orbFloat2 15s ease-in-out infinite;"></div>
    <div class="floating-orb orb-pink"   style="width:20vw;height:20vw;bottom:12%;left:4%;animation:orbFloat3 17s ease-in-out infinite;"></div>

    <!-- chrome overlays (absolute; never push content) -->
    <div class="slide-frame"></div>
    <div class="slide-header">
        <span class="slide-eyebrow">— re:Invent · <b>TRACK NAME</b></span>
        <span class="slide-index"></span>            <!-- controller fills "NN / NN" -->
    </div>

    <div class="slide-content">
        <!-- optional header pattern -->
        <div class="section-head reveal d1">
            <div class="section-titlebar">
                <span class="section-num">01</span>
                <h2 class="section-title">Section Title</h2>
            </div>
            <p class="section-desc">Optional one-line description.</p>
        </div>

        <!-- one layout body block goes here (see layouts below) -->
    </div>

    <div class="slide-progress"></div>          <!-- controller fills pips -->
    <div class="slide-footer">&copy; 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.</div>
</section>
```

### Frame / header / index / progress chrome

```css
.slide-frame {                  /* rounded inset border + faint inner glow; empty div */
    position:absolute; inset:clamp(10px,1.6vw,22px);
    border:1px solid var(--frame-border); border-radius:clamp(14px,1.6vw,22px);
    box-shadow:inset 0 0 60px rgba(139,92,246,.06), inset 0 0 1px rgba(255,255,255,.05);
    pointer-events:none; z-index:5;
}
.slide-header {                 /* top bar: eyebrow (L) + index (R) */
    position:absolute; top:clamp(18px,2.6vw,34px);
    left:clamp(24px,3.4vw,48px); right:clamp(24px,3.4vw,48px);
    display:flex; align-items:center; justify-content:space-between; gap:1rem;
    z-index:6; pointer-events:none;
}
.slide-eyebrow { font-family:var(--font-body); font-size:var(--micro-size); font-weight:500;
    letter-spacing:.18em; text-transform:uppercase; color:var(--text-faint);
    display:inline-flex; align-items:center; gap:.5em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.slide-eyebrow b { color:rgba(255,255,255,.7); font-weight:600; }
.slide-index { font-family:var(--font-display); font-size:var(--micro-size); font-weight:700;
    letter-spacing:.12em; color:var(--text-faint); font-variant-numeric:tabular-nums; }
.slide-index b { background:var(--grad-accent); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.slide-progress {               /* centered segmented pip row, filled by controller */
    position:absolute; bottom:clamp(20px,2.6vw,34px); left:50%; transform:translateX(-50%);
    display:flex; align-items:center; gap:clamp(4px,.6vw,7px); z-index:6; pointer-events:none; }
.slide-progress .pip { width:clamp(8px,1vw,14px); height:clamp(3px,.4vw,4px); border-radius:3px;
    background:rgba(255,255,255,.16); transition:background .3s, width .3s; }
.slide-progress .pip.on { width:clamp(18px,2.2vw,28px); background:var(--grad-bar); box-shadow:0 0 8px rgba(217,70,239,.4); }
.slide-footer {                 /* centered AWS disclaimer */
    position:absolute; bottom:0; left:0; right:0; padding:clamp(.5rem,1vw,.85rem) var(--slide-padding);
    font-size:clamp(.5rem,.7vw,.65rem); color:var(--text-faint); text-align:center; z-index:4; letter-spacing:.05em; }
```

Fixed overlays shared across all slides (already in the body, do not re-add): `.progress-bar`
(top), `.nav-dots` (right rail), `.page-number` (bottom-right).

### Section header pattern (reused across most content layouts)

```css
.section-head { display:flex; flex-direction:column; align-items:flex-start;
    gap:clamp(.2rem,.6vw,.5rem); margin-bottom:clamp(.8rem,2vh,1.6rem); }
.section-head.center { align-items:center; text-align:center; }
.section-titlebar { display:flex; align-items:baseline; gap:clamp(.6rem,1.4vw,1.1rem); }
.section-num {                  /* big gradient "01"; OMIT the span when unnumbered */
    font-family:var(--font-display); font-size:clamp(2rem,5.5vw,4.2rem); font-weight:900;
    line-height:.9; letter-spacing:-.03em; background:var(--grad-accent);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    filter:drop-shadow(0 0 24px rgba(217,70,239,.35)); flex-shrink:0; }
.section-title { font-family:var(--font-display); font-size:var(--h2-size); font-weight:700; line-height:1.12; }
.section-desc { font-size:var(--body-size); color:var(--text-secondary); line-height:1.6; max-width:min(90vw,760px); }
.section-label {                /* legacy small uppercase purple eyebrow, still available */
    font-family:var(--font-body); font-size:var(--small-size); font-weight:500;
    letter-spacing:.15em; text-transform:uppercase; color:var(--accent-purple); margin-bottom:clamp(.3rem,.7vw,.5rem); }
```

Use `.section-head.center` for centered headers (stats, pipeline, comparison, process, timeline).
Drop the `.section-num` span when a number isn't meaningful. For fully-centered layouts (quote, big
number) omit `.section-head` and place content directly.

### Floating orbs (all content slides)

```css
.floating-orb { position:absolute; border-radius:50%; pointer-events:none; z-index:0; }
.orb-purple { background:radial-gradient(circle, rgba(139,92,246,.30) 0%, rgba(139,92,246,0) 70%); }
.orb-pink   { background:radial-gradient(circle, rgba(217,70,239,.26) 0%, rgba(217,70,239,0) 70%); }
.orb-blue   { background:radial-gradient(circle, rgba(59,130,246,.22) 0%, rgba(59,130,246,0) 70%); }
@keyframes orbFloat1 { 0%,100%{transform:translate(0,0) scale(1);} 50%{transform:translate(20px,-30px) scale(1.05);} }
@keyframes orbFloat2 { 0%,100%{transform:translate(0,0) scale(1);} 50%{transform:translate(-25px,20px) scale(.95);} }
@keyframes orbFloat3 { 0%,100%{transform:translate(0,0) scale(1);} 50%{transform:translate(15px,25px) scale(1.03);} }
```

Give each content slide 1–2 orbs with inline size/position/animation, varied per slide so backgrounds
never repeat:

```html
<div class="floating-orb orb-purple" style="width:28vw;height:28vw;top:8%;right:6%;animation:orbFloat2 15s ease-in-out infinite;"></div>
<div class="floating-orb orb-blue"   style="width:24vw;height:24vw;top:15%;left:60%;animation:orbFloat1 16s ease-in-out infinite;"></div>
```

### Reveal delays (use d1–d7 classes, not inline style)

```css
.reveal { opacity:0; transform:translateY(25px);
    transition:opacity var(--duration-normal) var(--ease-out-expo), transform var(--duration-normal) var(--ease-out-expo); }
.slide.visible .reveal { opacity:1; transform:translateY(0); }
.slide.visible .reveal.d1 { transition-delay:.1s; }   /* … d2 .2s … through … */
.slide.visible .reveal.d7 { transition-delay:.7s; }
```

### Animated blobs (cover / divider / outlook backdrops only)

```css
.blob-canvas { position:absolute; inset:0; overflow:hidden; pointer-events:none; z-index:0; }
.blob { position:absolute; border-radius:50%; filter:blur(80px); will-change:transform, opacity; }
/* blob1–blob4: each keyframe set color-shifts purple→pink→blue→orange across translate/scale steps */
```

### Lucide icon picks (common)

`bot` `brain` `cpu` `server` `cloud` `database` `lock` `shield-check` `layers` `boxes` `zap`
`git-branch` `workflow` `bar-chart-3` `trending-up` `arrow-up-right` `arrow-down-right` `users`
`globe` `map-pin` `sparkles` `lightbulb` `alert-triangle` `rocket` `wrench` `chevron-right` `coins`

---

## Layout 1: Title / Cover

**Use for:** Opening cover and closing/CTA cover. (`02-reinvent-keynote.html` ships two: "Title" and
"Build with AWS".) Centered, animated blob backdrop, gradient `<em>` headline.
Cover does NOT use the frame / header / progress chrome — only the footer.

**CSS:**
```css
.title-slide { background:var(--bg-title); }
.title-slide::after { content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse 90% 90% at 50% 50%, transparent 40%, rgba(11,0,21,.6) 100%);
    pointer-events:none; z-index:1; }
.title-slide .slide-content { align-items:center; text-align:center;
    gap:clamp(.6rem,1.5vw,1.2rem); padding-top:var(--slide-padding); padding-bottom:var(--slide-padding); }
.title-label { font-family:var(--font-body); font-size:var(--small-size); font-weight:500;
    letter-spacing:.35em; text-transform:uppercase; color:rgba(255,255,255,.6); }
.title-main { font-family:var(--font-display); font-size:var(--title-size); font-weight:800;
    line-height:1.05; letter-spacing:-.025em; text-shadow:0 0 30px rgba(139,92,246,.3), 0 0 80px rgba(139,92,246,.15); }
.title-main em { font-style:normal; background:var(--grad-accent);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    filter:drop-shadow(0 0 25px rgba(217,70,239,.5)) drop-shadow(0 0 60px rgba(139,92,246,.3)); }
.title-accent { width:clamp(40px,5vw,56px); height:3px; border-radius:2px;
    background:linear-gradient(90deg, var(--accent-orange), var(--accent-pink));
    box-shadow:0 0 12px rgba(255,153,0,.4), 0 0 30px rgba(217,70,239,.2); }
.title-sub { font-size:var(--subtitle-size); color:rgba(255,255,255,.65);
    max-width:min(90vw,550px); line-height:1.6; text-shadow:0 0 20px rgba(0,0,0,.5); }
```

**HTML:**
```html
<section class="slide title-slide" aria-label="Title">
    <div class="blob-canvas">
        <div class="blob" style="width:55vw;height:55vw;top:-10%;left:40%;background:rgba(139,92,246,0.5);animation:blob1 12s ease-in-out infinite;"></div>
        <div class="blob" style="width:50vw;height:50vw;bottom:-5%;left:-10%;background:rgba(217,70,239,0.45);animation:blob2 15s ease-in-out infinite;"></div>
        <div class="blob" style="width:40vw;height:40vw;top:20%;left:10%;background:rgba(59,80,200,0.4);animation:blob3 18s ease-in-out infinite;"></div>
        <div class="blob" style="width:35vw;height:35vw;bottom:10%;right:5%;background:rgba(236,72,153,0.3);animation:blob4 20s ease-in-out infinite;"></div>
    </div>
    <div class="slide-content">
        <div class="title-label reveal d1">AMAZON WEB SERVICES</div>
        <h1 class="title-main reveal d2">Building the Future with<br><em>Generative AI</em></h1>
        <div class="title-accent reveal d3"></div>
        <p class="title-sub reveal d4">Subtitle line one,<br>subtitle line two.</p>
    </div>
    <div class="slide-footer">&copy; 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.</div>
</section>
```

**IMPORTANT:** the gradient `<em>` MUST sit on its own visual line (after `<br>`). Do NOT mix gradient
and non-gradient text on the same line — the clip can fail to render.

---

## Layout 2: Section Divider / Agenda

**Use for:** Section dividers and the agenda opener — a giant outlined-gradient number on a rich
gradient backdrop. Two shipped variants: "Section Divider" (with footer) and "Today's Agenda"
(the agenda opener, no footer). Uses the header + progress chrome but **omits `.slide-frame`** (the
blob canvas replaces it).

**CSS:**
```css
.divider-slide { background:var(--bg-title); }
.divider-slide::after { content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse 80% 80% at 50% 45%, rgba(124,58,237,.18) 0%, transparent 60%),
               radial-gradient(ellipse 70% 70% at 50% 55%, transparent 45%, rgba(11,0,21,.55) 100%);
    pointer-events:none; z-index:1; }
.divider-slide .slide-content { align-items:center; text-align:center; gap:clamp(.4rem,1vw,.9rem); }
.divider-num { font-family:var(--font-display); font-size:clamp(4.5rem,16vw,13rem); font-weight:900;
    line-height:.85; letter-spacing:-.04em; background:var(--grad-accent);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; filter:drop-shadow(0 0 50px rgba(217,70,239,.4)); }
.divider-title { font-family:var(--font-display); font-size:var(--h2-size); font-weight:800; line-height:1.1; }
.divider-sub { font-size:var(--subtitle-size); color:var(--text-secondary); max-width:min(85vw,620px); line-height:1.55; }
```

**HTML:**
```html
<section class="slide divider-slide" aria-label="Section Divider">
    <div class="blob-canvas">
        <div class="blob" style="width:50vw;height:50vw;top:-8%;left:35%;background:rgba(139,92,246,0.45);animation:blob1 14s ease-in-out infinite;"></div>
        <div class="blob" style="width:42vw;height:42vw;bottom:-6%;left:-8%;background:rgba(217,70,239,0.4);animation:blob2 17s ease-in-out infinite;"></div>
    </div>
    <div class="slide-header">
        <span class="slide-eyebrow">— re:Invent · <b>Platform Innovation</b></span>
        <span class="slide-index"></span>
    </div>
    <div class="slide-content">
        <div class="divider-num reveal d1">02</div>
        <h2 class="divider-title reveal d2">Platform Innovation</h2>
        <p class="divider-sub reveal d3">What's new across the AWS AI stack this year.</p>
    </div>
    <div class="slide-progress"></div>
    <div class="slide-footer">&copy; 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.</div>
</section>
```

---

## Layout 3: Pill Cards (left header + right pill list)

**Use for:** 3–5 key capabilities / product lineups that benefit from row-card treatment. Put the
`.section-head` INSIDE the left grid cell here (not at the top of `.slide-content`).

**CSS:**
```css
.content-layout { display:grid; grid-template-columns:2fr 3fr;
    gap:clamp(1.5rem,4vw,3.5rem); align-items:center; width:100%; max-width:var(--content-max); }
.pill-cards { display:flex; flex-direction:column; gap:clamp(.45rem,1vw,.7rem); }
.pill-card { display:flex; align-items:center; gap:clamp(.6rem,1.2vw,1rem);
    padding:clamp(.65rem,1.3vw,.95rem) clamp(.8rem,1.5vw,1.2rem);
    background:var(--card-bg); border:1px solid var(--card-border); border-radius:clamp(10px,1.2vw,14px);
    transition:border-color .3s, box-shadow .3s, transform .3s; }
.pill-card:hover { border-color:var(--card-border-hover); box-shadow:0 0 25px rgba(139,92,246,.15); transform:translateX(4px); }
.pill-icon { width:clamp(28px,3vw,36px); height:clamp(28px,3vw,36px); border-radius:clamp(6px,.8vw,10px);
    flex-shrink:0; background:linear-gradient(135deg, rgba(139,92,246,.2), rgba(217,70,239,.12));
    display:flex; align-items:center; justify-content:center; }
.pill-icon i { width:55%; height:55%; color:var(--accent-purple); }
.pill-text { font-size:var(--body-size); font-weight:500; line-height:1.3; }
.pill-text span { color:var(--text-secondary); font-weight:400; }
.pill-arrow { margin-left:auto; flex-shrink:0; width:clamp(16px,1.8vw,22px); height:clamp(16px,1.8vw,22px);
    border-radius:50%; background:rgba(139,92,246,.12); display:flex; align-items:center; justify-content:center; }
.pill-arrow i { width:55%; height:55%; color:rgba(255,255,255,.4); }
```

**HTML** (inside `.slide-content` of the standard wrapper):
```html
<div class="content-layout">
    <div>
        <div class="section-head reveal d1">
            <div class="section-titlebar"><span class="section-num">01</span><h2 class="section-title">End-to-End<br>AI Platform</h2></div>
            <p class="section-desc">A complete stack to build, train, and deploy generative AI.</p>
        </div>
    </div>
    <div class="pill-cards">
        <div class="pill-card reveal d2">
            <div class="pill-icon"><i data-lucide="layers"></i></div>
            <div class="pill-text">Amazon Bedrock<br><span>Access leading foundation models via one API</span></div>
            <div class="pill-arrow"><i data-lucide="chevron-right"></i></div>
        </div>
        <!-- 3–5 pills, stagger d2–d6 -->
    </div>
</div>
```

---

## Layout 4: Metric Cards Row (+ optional callout bar)

**Use for:** A row of 4 headline metrics, each with a category tag, big gradient number + unit, and a
colored delta line. Add an optional full-width `.callout-bar` summary strip below.

**CSS:**
```css
.metric-row { display:flex; gap:clamp(.6rem,1.4vw,1.1rem); width:100%; max-width:var(--content-max); }
.metric-card { flex:1; min-width:0; background:var(--card-bg); border:1px solid var(--card-border);
    border-radius:clamp(12px,1.4vw,18px); padding:clamp(.8rem,1.8vw,1.4rem);
    transition:border-color .3s, box-shadow .3s, transform .3s; }
.metric-card:hover { border-color:var(--card-border-hover); box-shadow:0 0 28px rgba(139,92,246,.16); transform:translateY(-3px); }
.metric-tag { display:inline-flex; align-items:center; gap:.4em; font-size:var(--micro-size); font-weight:600;
    letter-spacing:.08em; text-transform:uppercase; color:var(--text-secondary); margin-bottom:clamp(.4rem,1vw,.7rem); }
.metric-tag i { color:var(--accent-purple); }
.metric-value { font-family:var(--font-display); font-size:clamp(1.7rem,4.5vw,3.2rem); font-weight:800;
    line-height:1; letter-spacing:-.02em; background:linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; display:inline-flex; align-items:baseline; }
.metric-unit { font-family:var(--font-display); font-size:clamp(.8rem,1.6vw,1.2rem); font-weight:700;
    color:var(--text-secondary); -webkit-text-fill-color:var(--text-secondary); margin-left:.18em; }
.metric-delta { display:inline-flex; align-items:center; gap:.3em; margin-top:clamp(.4rem,.9vw,.65rem);
    font-size:var(--small-size); font-weight:600; }
.metric-delta.up { color:var(--up); } .metric-delta.down { color:var(--down); } .metric-delta.warn { color:var(--warn); }
.metric-delta span { color:var(--text-faint); font-weight:400; }

/* Callout: uniform border + soft horizontal gradient wash — NO solid colored
   left rail (that reads as generic AI/dashboard slop). Direction comes from the
   wash + a leading icon + a small monospace tag. */
.callout-bar { display:flex; align-items:center; gap:clamp(.7rem,1.5vw,1.1rem); width:100%; max-width:var(--content-max);
    margin-top:clamp(.7rem,1.6vh,1.2rem); padding:clamp(.7rem,1.4vw,1.05rem) clamp(1rem,2vw,1.6rem);
    background:linear-gradient(90deg, rgba(217,70,239,.10), rgba(139,92,246,.04) 45%, transparent);
    border:1px solid var(--card-border); border-radius:clamp(10px,1.2vw,14px); }
.callout-bar i { color:var(--accent-pink); flex-shrink:0; }
.callout-bar .callout-tag { font-family:var(--font-body); font-size:var(--micro-size); font-weight:600;
    letter-spacing:.18em; text-transform:uppercase; color:var(--accent-pink); flex-shrink:0;
    padding-right:clamp(.7rem,1.5vw,1.1rem); border-right:1px solid var(--hairline); }
.callout-bar p { font-size:var(--body-size); line-height:1.45; color:rgba(255,255,255,.85); }
.callout-bar strong { font-weight:700; background:var(--grad-accent); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
@media (max-width:600px) { .callout-bar .callout-tag { display:none; } }
```

**HTML** (inside `.slide-content`, after `.section-head`):
```html
<div class="metric-row">
    <div class="metric-card reveal d2">
        <div class="metric-tag"><i data-lucide="users"></i>Customers</div>
        <div class="metric-value">100<span class="metric-unit">K+</span></div>
        <div class="metric-delta up"><i data-lucide="arrow-up-right"></i>42% <span>vs 2024</span></div>
    </div>
    <!-- 4 cards, stagger d2–d5 -->
</div>
<div class="callout-bar reveal d6">
    <i data-lucide="sparkles"></i>
    <span class="callout-tag">Insight</span>
    <p><strong>Record year:</strong> generative AI adoption on AWS doubled across every region.</p>
</div>
```

Delta variants: `.up` (green ↑), `.down` (rose ↓), `.warn` (amber). Put the muted comparison text in a
`<span>`; use `.metric-unit` for the small unit beside the big number.

---

## Layout 5: Tagged Card Grid (3×2)

**Use for:** A grid of 6 detailed items (launches, features). Each card = one colored chip, bold
title, ~2-line description, and one colored metric footer line.

**CSS:**
```css
.tag-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(.6rem,1.3vw,1rem);
    width:100%; max-width:var(--content-max); }
.tag-card { background:var(--card-bg); border:1px solid var(--card-border); border-radius:clamp(10px,1.2vw,15px);
    padding:clamp(.7rem,1.5vw,1.15rem); display:flex; flex-direction:column; gap:clamp(.25rem,.6vw,.45rem);
    transition:border-color .3s, box-shadow .3s, transform .3s; }
.tag-card:hover { border-color:var(--card-border-hover); box-shadow:0 0 26px rgba(139,92,246,.14); transform:translateY(-3px); }
.tag-chip { align-self:flex-start; display:inline-flex; align-items:center; gap:.35em; font-size:var(--micro-size);
    font-weight:600; letter-spacing:.06em; text-transform:uppercase; padding:clamp(2px,.4vw,4px) clamp(7px,1vw,11px);
    border-radius:999px; color:#fff; background:rgba(139,92,246,.18); border:1px solid rgba(139,92,246,.35); }
.tag-chip.purple { background:rgba(139,92,246,.18); border-color:rgba(139,92,246,.4); color:#c4b5fd; }
.tag-chip.pink   { background:rgba(217,70,239,.16); border-color:rgba(217,70,239,.4); color:#f0abfc; }
.tag-chip.blue   { background:rgba(59,130,246,.16); border-color:rgba(59,130,246,.4); color:#93c5fd; }
.tag-chip.green  { background:rgba(52,211,153,.15); border-color:rgba(52,211,153,.4); color:#6ee7b7; }
.tag-chip.orange { background:rgba(255,153,0,.15);  border-color:rgba(255,153,0,.4);  color:#fcd34d; }
.tag-card h3 { font-family:var(--font-display); font-size:var(--h3-size); font-weight:700; line-height:1.2; }
.tag-card p { font-size:var(--small-size); color:var(--text-secondary); line-height:1.45; flex:1; }
.tag-foot { font-family:var(--font-display); font-size:var(--small-size); font-weight:700; color:var(--accent-pink);
    padding-top:clamp(.25rem,.6vw,.45rem); border-top:1px solid var(--hairline);
    display:inline-flex; align-items:center; gap:.35em; }
@media (max-width:900px) { .tag-grid { grid-template-columns:repeat(2,1fr); } }
```

**HTML** (inside `.slide-content`, after `.section-head`):
```html
<div class="tag-grid">
    <div class="tag-card reveal d2">
        <span class="tag-chip purple"><i data-lucide="cpu"></i>Compute</span>
        <h3>AWS Trainium4</h3>
        <p>Next-gen training silicon delivering higher throughput per watt for frontier models.</p>
        <span class="tag-foot"><i data-lucide="trending-up"></i>3x performance</span>
    </div>
    <!-- 6 cards (stagger d2–d7); vary chip color: purple | pink | blue | green | orange -->
</div>
```

---

## Layout 6: Big Number Hero

**Use for:** A single impressive metric / adoption number. Fully centered; omit `.section-head` and
use a `.section-label` eyebrow instead. Add `bignumber-slide` to the section class.

**CSS:**
```css
.bignumber-slide .slide-content { align-items:center; text-align:center; gap:clamp(.4rem,1vw,.8rem); }
.bignumber { font-family:var(--font-display); font-size:clamp(4rem,14vw,12rem); font-weight:800; line-height:1;
    background:linear-gradient(135deg, var(--accent-purple), var(--accent-pink), var(--accent-orange));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; filter:drop-shadow(0 0 40px rgba(139,92,246,.3)); }
.bignumber-label { font-family:var(--font-display); font-size:var(--h2-size); font-weight:700; }
.bignumber-desc { font-size:var(--subtitle-size); color:var(--text-secondary); max-width:min(80vw,600px); line-height:1.6; }
```

**HTML** (inside `.slide-content`; section class = `slide bignumber-slide content-slide`):
```html
<div class="section-label reveal d1">ADOPTION</div>
<div class="bignumber reveal d2">100K+</div>
<div class="bignumber-label reveal d3">Customers Building AI on AWS</div>
<p class="bignumber-desc reveal d4">From startups to enterprises, worldwide.</p>
```

---

## Layout 7: Stats Row + Feature Grid

**Use for:** A metrics bar (one bordered row, equal columns) over a supporting feature grid (3 or 6
cards). Use a centered header (`.section-head.center`).

**CSS:**
```css
.stats-row { display:flex; width:100%; max-width:min(90vw,940px); border:1px solid var(--card-border);
    border-radius:clamp(12px,1.3vw,16px); background:var(--card-bg); overflow:hidden; margin-bottom:var(--content-gap); }
.stat-item { flex:1; text-align:center; padding:clamp(.6rem,1.5vw,1.2rem) clamp(.5rem,1vw,1rem);
    border-right:1px solid rgba(139,92,246,.15); }
.stat-item:last-child { border-right:none; }
.stat-value { font-family:var(--font-display); font-size:clamp(1.4rem,3.5vw,2.6rem); font-weight:800; line-height:1.1;
    background:linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.stat-label { font-size:var(--small-size); color:var(--text-secondary); text-transform:uppercase;
    letter-spacing:.08em; margin-top:clamp(.15rem,.4vw,.3rem); }
.features-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(.5rem,1.1vw,.8rem);
    width:100%; max-width:min(90vw,940px); }
.feature-card { background:var(--card-bg); border:1px solid var(--card-border); border-radius:clamp(8px,1vw,12px);
    padding:clamp(.7rem,1.5vw,1.1rem); transition:border-color .3s, box-shadow .3s, transform .3s; }
.feature-card:hover { border-color:var(--card-border-hover); box-shadow:0 0 25px rgba(139,92,246,.12); transform:translateY(-3px); }
.feat-icon { width:clamp(26px,2.8vw,34px); height:clamp(26px,2.8vw,34px); border-radius:clamp(5px,.7vw,8px);
    background:linear-gradient(135deg, rgba(139,92,246,.18), rgba(217,70,239,.1));
    display:flex; align-items:center; justify-content:center; margin-bottom:clamp(.3rem,.7vw,.5rem); }
.feat-icon i { width:55%; height:55%; color:var(--accent-purple); }
.feature-card h3 { font-family:var(--font-display); font-size:var(--h3-size); font-weight:700; margin-bottom:clamp(.1rem,.3vw,.2rem); }
.feature-card p { font-size:var(--small-size); color:var(--text-secondary); line-height:1.45; }
```

**HTML** (inside `.slide-content`):
```html
<div class="section-head center reveal d1">
    <div class="section-titlebar"><span class="section-num">03</span><h2 class="section-title">Proven at Scale</h2></div>
</div>
<div class="stats-row reveal d2">
    <div class="stat-item"><div class="stat-value">100K+</div><div class="stat-label">Customers</div></div>
    <!-- 3–4 stat items -->
</div>
<div class="features-grid">
    <div class="feature-card reveal d3"><div class="feat-icon"><i data-lucide="shield-check"></i></div><h3>Enterprise Security</h3><p>VPC isolation, encryption, IAM.</p></div>
    <!-- 3 or 6 cards -->
</div>
```

---

## Layout 8: Split Divider (left product name + right bullets)

**Use for:** Product introductions / feature deep-dives — left product name & tagline, gradient
divider line, right bullet list.

**CSS:**
```css
.split-layout { display:grid; grid-template-columns:1fr auto 1fr; align-items:center;
    width:100%; max-width:var(--content-max); gap:0; }
.split-left { padding-right:clamp(1.5rem,4vw,3rem); }
.split-product-name { font-family:var(--font-display); font-size:var(--h2-size); font-weight:400;
    line-height:1.2; margin-bottom:clamp(.2rem,.5vw,.4rem); }
.split-product-name strong { font-weight:800; }
.split-product-sub { font-size:var(--body-size); color:var(--accent-purple); font-weight:500; }
.split-divider-line { width:1px; height:clamp(120px,25vh,250px);
    background:linear-gradient(180deg, transparent, rgba(139,92,246,.4), rgba(217,70,239,.3), transparent); }
.split-right { padding-left:clamp(1.5rem,4vw,3rem); }
.split-bullets { display:flex; flex-direction:column; gap:clamp(.8rem,2vh,1.5rem); list-style:none; }
.split-bullets li { font-size:clamp(.85rem,1.6vw,1.15rem); line-height:1.4; color:var(--text-secondary); }
@media (max-width:768px) { .split-layout { grid-template-columns:1fr; text-align:center; }
    .split-divider-line { width:60%; height:1px; margin:0 auto;
        background:linear-gradient(90deg, transparent, rgba(139,92,246,.4), transparent); } }
```

**HTML** (inside `.slide-content`; no top `.section-head` — the eyebrow lives in `.split-left`):
```html
<div class="split-layout">
    <div class="split-left">
        <div class="section-label reveal d1">NEW ENHANCEMENTS</div>
        <div class="split-product-name reveal d2">Amazon<br><strong>Q Developer</strong></div>
        <div class="split-product-sub reveal d3">Your AI-powered code companion</div>
    </div>
    <div class="split-divider-line reveal d2"></div>
    <div class="split-right">
        <ul class="split-bullets">
            <li class="reveal d3">Infrastructure as Code — CloudFormation, CDK, Terraform</li>
            <li class="reveal d4">Customize with your private codebase</li>
            <!-- 3–5 items, stagger d3–d6 -->
        </ul>
    </div>
</div>
```

---

## Layout 9: Pipeline Columns

**Use for:** Multi-stage processes / platform capability categories shown as 5 equal columns with
color-shifting gradient bars and an uppercase footer line. Centered header.

**CSS:**
```css
.pipeline-row { display:grid; grid-template-columns:repeat(5,1fr); gap:clamp(.4rem,1vw,.8rem);
    width:100%; max-width:var(--content-max); }
.pipeline-col { text-align:center; }
.pipeline-col-title { font-family:var(--font-display); font-size:var(--small-size); font-weight:700;
    margin-bottom:clamp(.3rem,.6vw,.5rem); line-height:1.3; }
.pipeline-bar { height:clamp(3px,.5vw,5px); border-radius:3px; margin-bottom:clamp(.4rem,.8vw,.6rem); }
.pipeline-items { display:flex; flex-direction:column; gap:clamp(.2rem,.4vw,.35rem); }
.pipeline-items span { font-size:var(--small-size); color:var(--text-secondary); line-height:1.3; }
.pipeline-footer { width:100%; max-width:var(--content-max); text-align:center; font-size:var(--small-size);
    color:var(--text-secondary); letter-spacing:.15em; text-transform:uppercase;
    margin-top:clamp(.6rem,1.4vh,1rem); padding-top:clamp(.5rem,1vw,.8rem); border-top:1px solid var(--hairline); }
@media (max-width:768px) { .pipeline-row { grid-template-columns:repeat(2,1fr); } }
```

**HTML** (inside `.slide-content`):
```html
<div class="section-head center reveal d1">
    <div class="section-titlebar"><h2 class="section-title">Amazon Bedrock</h2></div>
    <p class="section-desc">The easiest way to build generative AI applications.</p>
</div>
<div class="pipeline-row">
    <div class="pipeline-col reveal d3">
        <div class="pipeline-col-title">Broadest Model Choice</div>
        <div class="pipeline-bar" style="background:linear-gradient(90deg,#3b82f6,#6366f1);"></div>
        <div class="pipeline-items"><span>Custom Model Import</span><span>Model Evaluation</span></div>
    </div>
    <!-- 5 columns; bar gradient shifts blue→indigo→purple→violet→pink -->
</div>
<div class="pipeline-footer reveal d7">AWS Security, Privacy &amp; Reliability Built-in</div>
```

---

## Layout 10: Metric + Side List (org split)

**Use for:** Left 2×2 metric cards (reuses `.metric-card`) + right labeled list (label | value rows).

**CSS:**
```css
.org-layout { display:grid; grid-template-columns:3fr 2fr; gap:clamp(1rem,3vw,2.4rem);
    align-items:stretch; width:100%; max-width:var(--content-max); }
.org-metrics { display:grid; grid-template-columns:1fr 1fr; gap:clamp(.6rem,1.3vw,1rem); }
.org-side { display:flex; flex-direction:column; padding:clamp(.8rem,1.8vw,1.3rem) clamp(.9rem,2vw,1.5rem);
    background:var(--card-bg); border:1px solid var(--card-border); border-radius:clamp(12px,1.4vw,18px); }
.org-side-title { font-family:var(--font-display); font-size:var(--small-size); font-weight:700;
    letter-spacing:.1em; text-transform:uppercase; color:var(--text-secondary); margin-bottom:clamp(.3rem,.8vw,.6rem); }
.org-list { display:flex; flex-direction:column; }
.org-row { display:flex; align-items:center; justify-content:space-between; gap:.8rem;
    padding:clamp(.4rem,1vw,.7rem) 0; border-bottom:1px solid var(--hairline); }
.org-row:last-child { border-bottom:none; }
.org-row .label { font-size:var(--small-size); color:var(--text-secondary); display:inline-flex; align-items:center; gap:.45em; }
.org-row .label i { color:var(--accent-purple); }
.org-row .value { font-family:var(--font-display); font-size:var(--body-size); font-weight:700; color:var(--text-primary); white-space:nowrap; }
```

**HTML** (inside `.slide-content`, after `.section-head`):
```html
<div class="org-layout">
    <div class="org-metrics">
        <div class="metric-card reveal d2"> … (same structure as Layout 4 metric-card) … </div>
        <!-- 4 metric cards, stagger d2–d5 -->
    </div>
    <div class="org-side reveal d3">
        <div class="org-side-title">By the org</div>
        <div class="org-list">
            <div class="org-row"><span class="label"><i data-lucide="map-pin"></i>Regions</span><span class="value">33</span></div>
            <div class="org-row"><span class="label"><i data-lucide="server"></i>Availability Zones</span><span class="value">105</span></div>
            <!-- 3–5 rows -->
        </div>
    </div>
</div>
```

---

## Layout 11: Comparison Split

**Use for:** Side-by-side comparison of two options/products. Centered header + two bordered cards
each with a colored dot title and bulleted list.

**CSS:**
```css
.compare-grid { display:grid; grid-template-columns:1fr 1fr; gap:clamp(.8rem,2vw,1.5rem);
    width:100%; max-width:min(92vw,1000px); }
.compare-card { background:var(--card-bg); border:1px solid var(--card-border);
    border-radius:clamp(10px,1.2vw,16px); padding:clamp(1rem,2.5vw,2rem); }
.compare-card-title { font-family:var(--font-display); font-size:var(--h3-size); font-weight:700;
    margin-bottom:clamp(.5rem,1vw,.8rem); display:flex; align-items:center; gap:clamp(.3rem,.6vw,.5rem); }
.compare-dot { width:clamp(8px,1vw,12px); height:clamp(8px,1vw,12px); border-radius:50%; flex-shrink:0; }
.compare-list { list-style:none; display:flex; flex-direction:column; gap:clamp(.3rem,.7vw,.5rem); }
.compare-list li { font-size:var(--body-size); color:var(--text-secondary); padding-left:clamp(.8rem,1.5vw,1.2rem); position:relative; }
.compare-list li::before { content:''; position:absolute; left:0; top:clamp(.35rem,.7vw,.5rem);
    width:clamp(4px,.5vw,6px); height:clamp(4px,.5vw,6px); border-radius:50%; background:var(--accent-purple); }
@media (max-width:768px) { .compare-grid { grid-template-columns:1fr; } }
```

**HTML** (inside `.slide-content`):
```html
<div class="section-head center reveal d1">
    <div class="section-titlebar"><h2 class="section-title">SageMaker vs Bedrock</h2></div>
</div>
<div class="compare-grid">
    <div class="compare-card reveal d2">
        <div class="compare-card-title"><div class="compare-dot" style="background:var(--accent-purple);"></div>Amazon SageMaker</div>
        <ul class="compare-list"><li>Full control over training</li><li>Bring your own architecture</li></ul>
    </div>
    <div class="compare-card reveal d3">
        <div class="compare-card-title"><div class="compare-dot" style="background:var(--accent-pink);"></div>Amazon Bedrock</div>
        <ul class="compare-list"><li>Fully managed FMs</li><li>Built-in RAG, Agents, Guardrails</li></ul>
    </div>
</div>
```

---

## Layout 12: Two-Column Reflection (editorial split)

**Use for:** Paired lists — typically Challenges (`.warm`, amber) vs Learnings (`.cool`, green). Each
column: inline-icon heading + numbered items. Default (no modifier) = purple.

> **AVOID the AI-slop version.** The obvious take — two filled rounded cards, each with a solid
> `border-left: 3px` colored rail and a rounded-square icon tile — is a generic dashboard cliché.
> This layout deliberately drops all three: **no card fill, no left rail, no icon tile.** Instead it's
> two open columns sharing ONE neutral center hairline; color is carried only by (a) a small inline
> heading icon, (b) a short underline tick on the header hairline, and (c) hanging `01/02/03` indices.
> When you need a color accent on a panel, prefer an inline icon + a short tick over a full border edge.

**CSS:**
```css
.reflect-grid { display:grid; grid-template-columns:1fr 1fr; gap:0; width:100%; max-width:min(90vw,1020px); }
.reflect-col { padding:clamp(.3rem,1.2vw,.9rem) clamp(1.1rem,3.2vw,2.6rem); }
.reflect-col + .reflect-col { border-left:1px solid var(--hairline); }   /* the ONLY divider */
.reflect-head { position:relative; padding-bottom:clamp(.55rem,1.3vw,.95rem);
    margin-bottom:clamp(.7rem,1.7vw,1.25rem); border-bottom:1px solid var(--hairline); }
.reflect-head h3 { display:flex; align-items:center; gap:clamp(.4rem,.9vw,.65rem);
    font-family:var(--font-display); font-size:var(--h3-size); font-weight:800; line-height:1.15; letter-spacing:-.01em; }
.reflect-head h3 i { width:clamp(18px,2.2vw,26px); height:clamp(18px,2.2vw,26px); flex-shrink:0; color:var(--accent-purple); }
.reflect-col.warm .reflect-head h3 i { color:var(--warn); }
.reflect-col.cool .reflect-head h3 i { color:var(--up); }
.reflect-head::after { content:''; position:absolute; left:0; bottom:-1.5px;
    width:clamp(32px,5vw,54px); height:2.5px; border-radius:2px; background:var(--accent-purple); }   /* the tick */
.reflect-col.warm .reflect-head::after { background:var(--warn); box-shadow:0 0 10px rgba(251,191,36,.4); }
.reflect-col.cool .reflect-head::after { background:var(--up);  box-shadow:0 0 10px rgba(52,211,153,.4); }
.reflect-list { list-style:none; display:flex; flex-direction:column; gap:clamp(.6rem,1.5vw,1.05rem); counter-reset:rf; }
.reflect-list li { position:relative; padding-left:clamp(1.7rem,3.2vw,2.5rem);
    font-size:var(--body-size); color:var(--text-secondary); line-height:1.5; counter-increment:rf; }
.reflect-list li::before { content:counter(rf, decimal-leading-zero); position:absolute; left:0; top:.08em;
    font-family:var(--font-display); font-weight:800; font-size:.82em; color:var(--accent-purple); font-variant-numeric:tabular-nums; }
.reflect-col.warm .reflect-list li::before { color:var(--warn); }
.reflect-col.cool .reflect-list li::before { color:var(--up); }
@media (max-width:768px) { .reflect-grid { grid-template-columns:1fr; }
    .reflect-col { padding-left:0; padding-right:0; }
    .reflect-col + .reflect-col { border-left:none; border-top:1px solid var(--hairline); padding-top:clamp(.8rem,2vw,1.2rem); } }
```

**HTML** (inside `.slide-content`, after `.section-head`):
```html
<div class="reflect-grid">
    <div class="reflect-col warm reveal d2">
        <div class="reflect-head"><h3><i data-lucide="alert-triangle"></i>Challenges</h3></div>
        <ul class="reflect-list"><li>Scaling inference cost while latency expectations tightened.</li><!-- 3 items --></ul>
    </div>
    <div class="reflect-col cool reveal d3">
        <div class="reflect-head"><h3><i data-lucide="lightbulb"></i>Learnings</h3></div>
        <ul class="reflect-list"><li>Managed services collapsed time-to-first-token dramatically.</li><!-- 3 items --></ul>
    </div>
</div>
```

---

## Layout 13: Process Flow

**Use for:** Step-by-step workflows / how-it-works sequences (3–6 numbered steps connected by a
gradient line). Centered header.

**CSS:**
```css
.process-row { display:flex; align-items:flex-start; width:100%; max-width:var(--content-max); gap:0; position:relative; }
.process-step { flex:1; text-align:center; position:relative; padding:0 clamp(.3rem,.8vw,.6rem); }
.step-num { width:clamp(32px,4vw,48px); height:clamp(32px,4vw,48px); border-radius:50%;
    margin:0 auto clamp(.4rem,.8vw,.6rem); display:flex; align-items:center; justify-content:center;
    font-family:var(--font-display); font-size:var(--body-size); font-weight:800;
    background:linear-gradient(135deg, rgba(139,92,246,.2), rgba(217,70,239,.15));
    border:1px solid var(--card-border); position:relative; z-index:1; }
.process-step:not(:last-child)::after { content:''; position:absolute; top:clamp(16px,2vw,24px);
    left:calc(50% + clamp(20px,2.5vw,30px)); width:calc(100% - clamp(40px,5vw,60px)); height:1px;
    background:linear-gradient(90deg, rgba(139,92,246,.3), rgba(217,70,239,.2)); z-index:0; }
.step-title { font-family:var(--font-display); font-size:var(--h3-size); font-weight:700; margin-bottom:clamp(.15rem,.3vw,.25rem); }
.step-desc { font-size:var(--small-size); color:var(--text-secondary); line-height:1.4; }
@media (max-width:768px) { .process-row { flex-direction:column; gap:clamp(.5rem,1.5vw,1rem); align-items:center; }
    .process-step:not(:last-child)::after { display:none; } }
```

**HTML** (inside `.slide-content`):
```html
<div class="section-head center reveal d1">
    <div class="section-titlebar"><h2 class="section-title">From Idea to Production</h2></div>
</div>
<div class="process-row">
    <div class="process-step reveal d3"><div class="step-num">1</div><div class="step-title">Choose Model</div><div class="step-desc">Select a leading FM or import your own.</div></div>
    <!-- 3–6 steps, stagger d3–d7 -->
</div>
```

---

## Layout 14: Timeline Zigzag

**Use for:** Chronological milestones / evolution history (5 columns). Odd columns show cards ABOVE
the line, even columns BELOW. Empty cells use `.empty`. Centered header.

**CSS:**
```css
.timeline { width:100%; max-width:var(--content-max); display:grid;
    grid-template-rows:auto auto auto; grid-template-columns:repeat(5,1fr); }
.tl-top { grid-row:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; }
.tl-top .tl-card { margin-bottom:clamp(.5rem,1.2vw,1rem); }
.tl-top.empty, .tl-bot.empty { visibility:hidden; }
.tl-mid { grid-row:2; display:flex; align-items:center; justify-content:center; position:relative; height:clamp(20px,2.5vw,30px); }
.tl-mid::before { content:''; position:absolute; left:0; right:0; top:50%; height:3px;
    transform:translateY(-50%); background:rgba(139,92,246,.3); }
.tl-col1.tl-mid::before { left:50%; background:linear-gradient(90deg, rgba(59,130,246,.5), rgba(139,92,246,.4)); }
.tl-col5.tl-mid::before { right:50%; background:linear-gradient(90deg, rgba(217,70,239,.4), rgba(236,72,153,.3)); }
.tl-dot { width:clamp(14px,1.6vw,20px); height:clamp(14px,1.6vw,20px); border-radius:50%;
    border:2.5px solid currentColor; background:var(--bg-primary); position:relative; z-index:1; box-shadow:0 0 14px currentColor; }
.tl-bot { grid-row:3; display:flex; flex-direction:column; align-items:center; justify-content:flex-start; }
.tl-bot .tl-card { margin-top:clamp(.5rem,1.2vw,1rem); }
.tl-stem-up   { width:2px; height:clamp(16px,3vh,30px); background:linear-gradient(180deg, transparent, currentColor); }
.tl-stem-down { width:2px; height:clamp(16px,3vh,30px); background:linear-gradient(180deg, currentColor, transparent); }
.tl-card { text-align:center; padding:0 clamp(.2rem,.5vw,.4rem); }
.tl-year { font-family:var(--font-display); font-size:var(--h3-size); font-weight:800; color:currentColor; }
.tl-desc { font-size:var(--small-size); color:var(--text-secondary); line-height:1.35; }
/* per-column colors (blue→purple→violet→pink→rose) */
.tl-col1 { color:#3b82f6; } .tl-col2 { color:#8b5cf6; } .tl-col3 { color:#a855f7; }
.tl-col4 { color:#d946ef; } .tl-col5 { color:#ec4899; }
```

**HTML** (inside `.slide-content`, after `.section-head.center`): three grid rows — top cards,
center dots (all 5 cols), bottom cards. Odd cols filled on top + `.empty` on bottom; even cols the
reverse. `.empty` cells still need the same inner markup with `&nbsp;` placeholders to hold the grid.
```html
<div class="timeline reveal d3">
    <!-- Row 1: top cards -->
    <div class="tl-top tl-col1"><div class="tl-card"><div class="tl-year">2017</div><div class="tl-desc">SageMaker</div></div><div class="tl-stem-up"></div></div>
    <div class="tl-top tl-col2 empty"><div class="tl-card"><div class="tl-year">&nbsp;</div><div class="tl-desc">&nbsp;</div></div><div class="tl-stem-up"></div></div>
    <div class="tl-top tl-col3"> … 2023 … </div>
    <div class="tl-top tl-col4 empty"> … &nbsp; … </div>
    <div class="tl-top tl-col5"> … 2025 … </div>
    <!-- Row 2: dots (all 5 cols) -->
    <div class="tl-mid tl-col1"><div class="tl-dot"></div></div> … <div class="tl-mid tl-col5"><div class="tl-dot"></div></div>
    <!-- Row 3: bottom cards (even cols content, odd cols .empty) -->
    <div class="tl-bot tl-col1 empty"><div class="tl-stem-down"></div><div class="tl-card"><div class="tl-year">&nbsp;</div><div class="tl-desc">&nbsp;</div></div></div>
    <div class="tl-bot tl-col2"><div class="tl-stem-down"></div><div class="tl-card"><div class="tl-year">2022</div><div class="tl-desc">Trainium</div></div></div>
    … cols 3 (.empty), 4 (content), 5 (.empty) …
</div>
```

---

## Layout 15: Quote

**Use for:** Executive quotes, key insights, bold statements. Fully centered; omit `.section-head`.
Add `quote-slide` to the section class.

**CSS:**
```css
.quote-slide .slide-content { align-items:center; text-align:center; gap:var(--content-gap); }
.quote-mark { font-family:var(--font-display); font-size:clamp(3rem,8vw,6rem); line-height:1; font-weight:800;
    background:linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; opacity:.5; }
.quote-text { font-family:var(--font-display); font-size:clamp(1.1rem,2.5vw,2rem); font-weight:500;
    line-height:1.5; max-width:min(85vw,800px); color:rgba(255,255,255,.9); }
.quote-attr { font-size:var(--body-size); color:var(--text-secondary); }
.quote-attr strong { color:var(--text-primary); font-weight:600; }
```

**HTML** (inside `.slide-content`; section class = `slide quote-slide content-slide`):
```html
<div class="quote-mark reveal d1">&ldquo;</div>
<p class="quote-text reveal d2">Every application will be reinvented with generative AI.</p>
<div class="quote-attr reveal d3"><strong>Andy Jassy</strong> &mdash; CEO, Amazon</div>
```

---

## Layout 16: Numbered Outlook Columns

**Use for:** A forward-looking agenda — centered tagline + 3 outlined-number columns on a rich
gradient backdrop. Add `outlook-slide` to the section class; uses the blob canvas + header + progress
chrome but **omits `.slide-frame`**.

**CSS:**
```css
.outlook-slide { background:var(--bg-title); }
.outlook-slide::after { content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse 90% 80% at 50% 40%, rgba(124,58,237,.16) 0%, transparent 60%),
               radial-gradient(ellipse 70% 70% at 50% 60%, transparent 45%, rgba(11,0,21,.5) 100%);
    pointer-events:none; z-index:1; }
.outlook-tagline { font-family:var(--font-display); font-size:var(--subtitle-size); font-weight:600;
    color:rgba(255,255,255,.85); text-align:center; max-width:min(85vw,700px); line-height:1.4; margin-bottom:clamp(.8rem,2vh,1.6rem); }
.outlook-tagline em { font-style:normal; background:var(--grad-accent); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.outlook-row { display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(.9rem,2.4vw,2rem);
    width:100%; max-width:var(--content-max); }
.outlook-col { display:flex; flex-direction:column; gap:clamp(.3rem,.8vw,.55rem);
    padding-top:clamp(.4rem,1vw,.7rem); border-top:2px solid rgba(139,92,246,.3); }
.outlook-num { font-family:var(--font-display); font-size:clamp(2.2rem,6vw,4.2rem); font-weight:800;
    line-height:.9; letter-spacing:-.03em; -webkit-text-stroke:1.5px rgba(196,181,253,.7);
    -webkit-text-fill-color:transparent; color:transparent; }
.outlook-col h3 { font-family:var(--font-display); font-size:var(--h3-size); font-weight:700; line-height:1.2; }
.outlook-col p { font-size:var(--small-size); color:var(--text-secondary); line-height:1.5; }
```

**HTML:**
```html
<section class="slide outlook-slide" aria-label="2026 Outlook">
    <div class="blob-canvas">
        <div class="blob" style="width:48vw;height:48vw;top:-6%;left:30%;background:rgba(139,92,246,0.4);animation:blob1 15s ease-in-out infinite;"></div>
        <div class="blob" style="width:40vw;height:40vw;bottom:-6%;right:-6%;background:rgba(217,70,239,0.35);animation:blob3 18s ease-in-out infinite;"></div>
    </div>
    <div class="slide-header">
        <span class="slide-eyebrow">— re:Invent · <b>OUTLOOK</b></span>
        <span class="slide-index"></span>
    </div>
    <div class="slide-content">
        <p class="outlook-tagline reveal d1">Where we invest <em>next</em> — the 2026 agenda.</p>
        <div class="outlook-row">
            <div class="outlook-col reveal d2"><span class="outlook-num">01</span><h3>Agentic by Default</h3><p>Every workflow gains a reasoning agent with built-in guardrails.</p></div>
            <div class="outlook-col reveal d3"> … 02 … </div>
            <div class="outlook-col reveal d4"> … 03 … </div>
        </div>
    </div>
    <div class="slide-progress"></div>
    <div class="slide-footer">&copy; 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.</div>
</section>
```

---

## Layout 17: Bento Grid (asymmetric feature mosaic)

**Use for:** A platform map / capability mosaic where ONE item deserves hero treatment — a 4-column
grid with a 2×2 hero cell (rotating border-beam + big count-up stat), four 1×1 cells, and a
full-width bottom strip. The most eye-catching content layout; use at most once per deck.

**CSS:**
```css
.bento-grid { display:grid; grid-template-columns:repeat(4,1fr); grid-auto-rows:minmax(0,1fr);
    gap:clamp(.5rem,1.1vw,.9rem); width:100%; max-width:var(--content-max); max-height:min(68vh,620px); }
.bento-cell { background:var(--card-bg); border:1px solid var(--card-border);
    border-radius:clamp(12px,1.4vw,18px); padding:clamp(.8rem,1.6vw,1.3rem);
    display:flex; flex-direction:column; gap:clamp(.3rem,.7vw,.55rem); min-width:0; overflow:hidden;
    transition:border-color .3s, box-shadow .3s, transform .3s; }
.bento-cell:hover { border-color:var(--card-border-hover); box-shadow:0 0 28px rgba(139,92,246,.16); transform:translateY(-3px); }
.bento-icon { width:clamp(28px,3vw,38px); height:clamp(28px,3vw,38px); border-radius:clamp(6px,.8vw,10px);
    flex-shrink:0; background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(217,70,239,.1));
    display:flex; align-items:center; justify-content:center; }
.bento-icon i { width:55%; height:55%; color:var(--accent-purple); }
.bento-cell h3 { font-family:var(--font-display); font-size:var(--h3-size); font-weight:700; line-height:1.2; }
.bento-cell p { font-size:var(--small-size); color:var(--text-secondary); line-height:1.45; }
.bento-hero { grid-column:span 2; grid-row:span 2; justify-content:flex-end;
    gap:clamp(.4rem,1vw,.75rem); overflow:visible; /* let the border beam render outside */ }
.bento-hero h3 { font-size:var(--h2-size); font-weight:800; letter-spacing:-.01em; line-height:1.1; }
.bento-hero p { font-size:var(--body-size); }
.bento-stat { font-family:var(--font-display); font-size:clamp(2rem,5.5vw,3.6rem); font-weight:800;
    line-height:1; letter-spacing:-.02em; background:linear-gradient(135deg,var(--accent-purple),var(--accent-pink));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    display:inline-flex; align-items:baseline; margin-top:clamp(.1rem,.4vw,.3rem); }
.bento-wide { grid-column:1 / -1; flex-direction:row; align-items:center; }
.bento-wide p { margin-left:auto; text-align:right; }
@media (max-width:900px) { .bento-grid { grid-template-columns:repeat(2,1fr); max-height:none; }
    .bento-hero { grid-column:span 2; grid-row:span 1; } .bento-wide { grid-column:span 2; } }
@media (max-width:600px) { .bento-grid { grid-template-columns:1fr; } .bento-hero, .bento-wide { grid-column:span 1; } }
```

Border beam (hero cell only; needs `@property`):
```css
@property --beam-angle { syntax:'<angle>'; initial-value:0deg; inherits:false; }
.beam-border { position:relative; }
.beam-border::before { content:''; position:absolute; inset:-1px; border-radius:inherit; padding:1.5px;
    background:conic-gradient(from var(--beam-angle), transparent 0 62%, #8B5CF6 78%, #D946EF 90%, #FF9900 96%, transparent 100%);
    -webkit-mask:linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor; mask-composite:exclude;
    animation:beamSpin 6s linear infinite; pointer-events:none; }
@keyframes beamSpin { to { --beam-angle:360deg; } }
@media (prefers-reduced-motion:reduce){ .beam-border::before { animation:none; } }
```

**HTML** (inside `.slide-content`, after `.section-head`):
```html
<div class="bento-grid">
    <div class="bento-cell bento-hero beam-border reveal d2">
        <div class="bento-icon"><i data-lucide="layers"></i></div>
        <h3>One Platform, Every Model</h3>
        <p>From foundation models to custom silicon — build, tune, and ship without leaving AWS.</p>
        <div class="bento-stat"><span class="count" data-count="200" data-decimals="0">0</span>+</div>
    </div>
    <div class="bento-cell reveal d3">
        <div class="bento-icon"><i data-lucide="bot"></i></div>
        <h3>Bedrock AgentCore</h3>
        <p>Managed reasoning agents with memory and tool use.</p>
    </div>
    <!-- 4 small cells, stagger d3–d6; then one full-width strip: -->
    <div class="bento-cell bento-wide reveal d7">
        <div class="bento-icon"><i data-lucide="zap"></i></div>
        <h3>Sub-second inference at global scale</h3>
        <p>Optimized serving across 33 Regions and 600+ edge locations.</p>
    </div>
</div>
```

Keep small-cell copy to ONE short line — cells clip overflow. The hero's `.count` is animated by the
controller's count-up (see Layout 19 notes).

---

## Layout 18: Spotlight Cards (pointer-follow glow)

**Use for:** 3 pillar reasons / principles — outlined big number + icon + title + 2-line desc, with a
radial glow that follows the cursor inside each card. Centered header.

**CSS:**
```css
.spot-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(.8rem,2vw,1.5rem);
    width:100%; max-width:var(--content-max); }
.spot-card { position:relative; overflow:hidden; background:var(--card-bg);
    border:1px solid var(--card-border); border-radius:clamp(12px,1.4vw,18px);
    padding:clamp(1rem,2.2vw,1.8rem); display:flex; flex-direction:column; gap:clamp(.4rem,1vw,.7rem);
    transition:border-color .3s, box-shadow .3s, transform .3s; }
.spot-card:hover { border-color:var(--card-border-hover); box-shadow:0 0 28px rgba(139,92,246,.16); transform:translateY(-3px); }
.spot-card::before { content:''; position:absolute; inset:0; z-index:0; pointer-events:none;
    background:radial-gradient(240px circle at var(--mx,50%) var(--my,50%), rgba(139,92,246,.16), transparent 60%);
    opacity:0; transition:opacity .35s; }
.spot-card:hover::before { opacity:1; }
.spot-card > * { position:relative; z-index:1; }
.spot-num { font-family:var(--font-display); font-size:clamp(2rem,5vw,3.6rem); font-weight:800;
    line-height:1; -webkit-text-stroke:1.5px rgba(196,181,253,.5); -webkit-text-fill-color:transparent; color:transparent; }
.spot-icon { /* same tile treatment as .feat-icon, slightly larger */ }
@media (max-width:768px) { .spot-grid { grid-template-columns:1fr; } }
```

JS (bind once, after the controller):
```js
document.querySelectorAll('.spot-card').forEach(card => {
    card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
});
```

**HTML** (inside `.slide-content`, after `.section-head.center`):
```html
<div class="spot-grid">
    <div class="spot-card reveal d2">
        <span class="spot-num">01</span>
        <div class="spot-icon"><i data-lucide="shield-check"></i></div>
        <h3>Security by Design</h3>
        <p>VPC isolation, end-to-end encryption, and fine-grained IAM protect every workload.</p>
    </div>
    <!-- 3 cards, stagger d2–d4 -->
</div>
```

---

## Layout 19: Marquee (dual scrolling keyword rows)

**Use for:** Ecosystem / service-catalog slides — two full-bleed rows of oversized service names
scrolling in opposite directions with soft masked edges; 1–2 highlighted gradient names per row.
Centered header. Duplicate the item sequence TWICE inside each track (the -50% translate loops
seamlessly only with an exact duplicate).

**CSS:**
```css
.marquee-block { width:100%; display:flex; flex-direction:column; gap:clamp(.8rem,2vh,1.6rem); }
.marquee { width:100vw; margin-left:calc(50% - 50vw); overflow:hidden;
    -webkit-mask:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);
            mask:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent); }
.marquee-track { display:flex; align-items:center; gap:clamp(1.2rem,3vw,2.6rem);
    width:max-content; animation:marqueeMove 32s linear infinite; }
.marquee-track.rev { animation-duration:40s; animation-direction:reverse; }
@keyframes marqueeMove { to { transform:translateX(-50%); } }
.mq-item { font-family:var(--font-display); font-weight:700; font-size:clamp(1.3rem,3.2vw,2.4rem);
    color:rgba(255,255,255,.22); white-space:nowrap; }
.mq-item.hl { background:var(--grad-accent); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.mq-dot { width:clamp(6px,.9vw,10px); height:clamp(6px,.9vw,10px); flex-shrink:0;
    background:var(--accent-pink); transform:rotate(45deg); border-radius:1px;
    box-shadow:0 0 8px rgba(217,70,239,.5); }
@media (prefers-reduced-motion:reduce) { .marquee-track { animation:none; } }
```

**HTML** (inside `.slide-content`, after `.section-head.center`):
```html
<div class="marquee-block reveal d2">
    <div class="marquee"><div class="marquee-track">
        <span class="mq-item">EC2</span><span class="mq-dot"></span>
        <span class="mq-item">S3</span><span class="mq-dot"></span>
        <span class="mq-item hl">Amazon Bedrock</span><span class="mq-dot"></span>
        <!-- …rest of sequence, then the ENTIRE sequence duplicated once more verbatim -->
    </div></div>
    <div class="marquee"><div class="marquee-track rev">
        <!-- second row, different services, same duplicate-twice rule -->
    </div></div>
</div>
```

Use `.mq-dot` separators — never a literal `◆` character.

---

## Motion upgrades (title + numbers) — apply to every deck

**Title word reveal + shimmer.** Wrap each headline word in
`<span class="tw" style="--i:0">Building</span>`; keep the gradient `<em>` as ONE unit inside its
own span (`<span class="tw" style="--i:4"><em>Generative AI</em></span>`) — splitting a
gradient-clipped `<em>` across spans breaks the clip.

```css
.title-main .tw { display:inline-block; opacity:0; transform:translateY(.5em); filter:blur(8px); }
.slide.visible .title-main .tw { animation:wordRise .8s var(--ease-out-expo) both; animation-delay:calc(var(--i)*90ms); }
@keyframes wordRise { to { opacity:1; transform:none; filter:blur(0); } }
.title-main em { background-size:200% 100%; animation:emShimmer 5s ease-in-out 1.2s infinite; }
@keyframes emShimmer { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
@media (prefers-reduced-motion:reduce){ .title-main .tw { opacity:1; transform:none; filter:none; } }
```

**Count-up numbers.** Wrap ONLY the numeric part:
`<div class="metric-value"><span class="count" data-count="100" data-decimals="0">0</span><span class="metric-unit">K+</span></div>`.
Applies to `.metric-value`, `.stat-value`, `.bignumber`, `.bento-stat`. Leave non-numeric values
("24/7") untouched; decimals via `data-decimals`. The controller triggers once per slide inside the
IntersectionObserver callback:

```js
if (!e.target.dataset.fx) { e.target.dataset.fx = '1'; runCounters(e.target); }
```

`runCounters` = rAF ease-out-cubic over ~1.3s; when `prefers-reduced-motion`, set the final value
instantly. Full implementation in [animation-patterns.md](animation-patterns.md) "Signature Motion
Patterns".

---

## Layout Selection Guide

| Content Type | Recommended Layout |
|---|---|
| Opening cover, closing / CTA cover | **Title / Cover** (Layout 1) |
| Section opener, agenda opener | **Section Divider / Agenda** (Layout 2) |
| 3–5 key capabilities / product lineup | **Pill Cards** (Layout 3) |
| Row of 4 headline metrics (+ summary) | **Metric Cards Row** (Layout 4) |
| 6 detailed launches / feature cards | **Tagged Card Grid** (Layout 5) |
| One single impressive number | **Big Number Hero** (Layout 6) |
| Metrics bar + supporting features | **Stats Row + Feature Grid** (Layout 7) |
| Product intro with bullet details | **Split Divider** (Layout 8) |
| Multi-stage platform / capability map | **Pipeline Columns** (Layout 9) |
| 2×2 metrics + labeled side list | **Metric + Side List** (Layout 10) |
| Two-option comparison | **Comparison Split** (Layout 11) |
| Challenges vs learnings / pros vs cons | **Two-Column Reflection** (Layout 12) |
| Step-by-step workflow (3–6 steps) | **Process Flow** (Layout 13) |
| Chronological milestones (5 points) | **Timeline Zigzag** (Layout 14) |
| Executive quote / bold statement | **Quote** (Layout 15) |
| Forward-looking 3-point agenda | **Numbered Outlook Columns** (Layout 16) |
| Platform map with ONE hero item | **Bento Grid** (Layout 17) |
| 3 pillar reasons / principles | **Spotlight Cards** (Layout 18) |
| Ecosystem / service catalog | **Marquee** (Layout 19) |

**Rule: never use plain left-aligned bullet lists.** Always wrap content in one of these layouts. If
content doesn't fit any layout, default to **Pill Cards** (Layout 3) or **Tagged Card Grid** (Layout 5).

**Motion defaults:** every deck gets the title word-reveal + em shimmer, and count-up on all metric
numbers (see "Motion upgrades" above). Use **Bento Grid** and **Marquee** at most once each per deck —
they are signature moments, not repeatable fillers.
