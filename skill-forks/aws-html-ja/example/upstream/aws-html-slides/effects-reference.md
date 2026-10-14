# Effects Reference — 3D & Motion for Self-Contained Slides

> **Status: catalog + experimental demos.** This file is a researched, license-checked
> menu of ways to add 3D and motion to slides. The techniques here are NOT yet wired
> into the default generation flow — adopt them deliberately, per-deck. Working,
> Chrome-verified demos for the starred techniques live in `../demos/` (paths below).

This skill's prime directive is **self-contained, offline, single-file** decks
(see [SKILL.md](SKILL.md) "Core Principles"). Every technique below is judged first
on whether it survives that bar: **does it still work when you double-click the
`.html` with no network?** A beautiful effect that needs a live CDN or a paid export
is useless here.

> **Animated diagrams have their own reference.** The native SVG/CSS diagram
> framework (flowchart/sequence/ER/mindmap + isometric-3D architecture, with
> packet-flow animation) lives in [diagram-reference.md](diagram-reference.md),
> with five Chrome-verified demos under `../demos/diagrams/`. The techniques
> below are page-level effects; the diagram demos reuse the same offline rules.

> **Combined integration demo: `../demos/all-effects/`.** A single 5-slide deck that
> runs *every* effect below **together** in one document — WebGL nebula + GSAP kinetic
> title (cover), CSS 3D cube + stage light-pool, 2.5D parallax, GSAP staggered cards
> with gradient-hairline panels, and a closing `@property` conic-gradient halo + CSS
> aurora — behind a real slide engine (arrow keys / Space / wheel / nav dots, page
> number, per-slide intro replays). Proves the WebGL context, GSAP, and CSS 3D coexist
> offline with no conflict. The four single-effect demos (`webgl-nebula/`,
> `gsap-title/`, `css-3d-hero/`) remain as focused, copy-paste references.

**These effects serve both specialty styles.** The *techniques* are palette-agnostic
— each ships in two tints, with a working demo per tint:

- **re:Invent Keynote (style #2):** near-black `#0A0A0A`, purple `#8B5CF6` / pink
  `#D946EF` / blue, Urbanist + Albert Sans. Demos in `../demos/`.
- **Neon Cyber (style #1):** deep navy `#0a0f1c`, cyan `#00ffcc` / magenta `#ff00aa` /
  blue `#00aaff`, Clash Display + Satoshi. Demos in `../demos/neon/`.

Pick the token set for your chosen style (full table in **"Palette token sets"** below),
then copy the matching demo. See [STYLE_PRESETS.md](STYLE_PRESETS.md) and
[layout-reinvent.md](layout-reinvent.md).

> **Coverage note:** four techniques have a Neon-Cyber variant under `../demos/neon/`
> — WebGL nebula, constellation network, pointer tilt, and GSAP kinetic title. The
> remaining demos (CSS 3D hero, GSAP micro-effects, the combined `all-effects` deck)
> and **Three.js** exist in the re:Invent palette only; re-tint them per the token table
> if you need them for a Neon deck. Three.js is intentionally not part of the Neon set.

---

## Palette token sets

Every demo bypasses `:root` with hardcoded `rgba()`, JS color arrays, and GLSL `vec3`
constants — so re-tinting a purple demo to Neon (or vice-versa) means changing all of
them, not just the tokens. Use this map:

| Role | re:Invent purple (`demos/`) | Neon Cyber cyan (`demos/neon/`) |
|------|-----------------------------|----------------------------------|
| Background | `#0A0A0A` / `#06030d` / `#07030f` | `#0a0f1c` |
| Primary accent | purple `#8B5CF6` = `rgb(139,92,246)` | cyan `#00ffcc` = `rgb(0,255,204)` |
| Secondary accent | pink `#D946EF` = `rgb(217,70,239)` | magenta `#ff00aa` = `rgb(255,0,170)` |
| Tertiary accent | blue `#38BDF8` / `#3B82F6` = `rgb(56,189,248)` | blue `#00aaff` = `rgb(0,170,255)` |
| Display font | Urbanist | Clash Display |
| Body font | Albert Sans | Satoshi |

GLSL note (`vec3`, normalized 0–1): cyan `vec3(0.0,1.0,0.8)`, magenta
`vec3(1.0,0.0,0.667)`, blue `vec3(0.0,0.667,1.0)`, navy `vec3(0.039,0.059,0.110)`.
When porting, keep each `rgba()` **alpha** unchanged — only swap the RGB triple.

---

## The offline test (apply to every effect)

| Verdict | Meaning | Examples |
|---------|---------|----------|
| ✅ **Inline** | Pure CSS/JS/SVG written into the file. Can never break. | CSS 3D, animated gradients, hand-written WebGL shader, WAAPI |
| ✅ **Vendorable** | A single UMD/global build downloaded into `vendor/` + a relative `<script src>`. Works offline; adds file weight. | Three.js r160, GSAP 3.13, tsParticles, lottie-web |
| ❌ **CDN/online-only** | Needs a live network fetch or a hosted scene at runtime. **Banned.** | Spline online scenes, ESM-only libs via CDN import maps, Lottie `path:` URLs |
| ❌ **Paid/locked** | Requires a paid plan to export the asset at all. **Banned.** | Spline `.splinecode`/GLB export (Pro-only), SVGator watermark-free export |

**Rule of thumb:** prefer Inline → Vendorable → (never) CDN. The lighter and more
inline, the better. A 5 KB hand-written shader beats a 1.8 MB engine for a background.

---

## 🚦 Licensing red-lines (read before borrowing anything)

These are the traps that look free but aren't. **"No license" never means "free."**

| Source | Trap | Safe alternative |
|--------|------|------------------|
| **Spline** (app.spline.design) | Native export (`.splinecode`, GLB) is **Pro/Team-only**. Free accounts cannot export. Community scenes have **no public runtime URL** — must Remix+Export first. So neither offline nor online embedding works for free users. | Hand-built WebGL/Three.js, or CSS 3D. |
| **Shadertoy** shaders | **Default license is CC BY-NC-SA 3.0** = NonCommercial **and** ShareAlike. Copy-pasting into a sales/pitch/product deck infringes; ShareAlike also forces your whole deck open. Most shaders have no header → fall under this default. | Learn the *technique* (not copyrightable), write original GLSL. Use MIT `snoise` (below). |
| **The Book of Shaders** code | "All rights reserved… cannot use in any commercial or non-commercial product." | Learn from it; write your own. |
| **LYGIA** shader lib | Prosperity license: 30-day commercial trial then **paid**. | `stegu/webgl-noise` (MIT). |
| **whatamesh** / Stripe gradient | **No license** (reverse-engineered Stripe code) = legally all-rights-reserved. OK internal/personal; risky to publish/commercialize. | Hand-written shader gradient, or CSS mesh gradient. |
| **Lordicon** free tier | Requires a visible **backlink** + is **No-Derivatives / non-commercial**. | Lucide (animate with your own CSS). |
| **Rive** community assets | **CC BY 4.0 → mandatory attribution**; runtime also fetches `rive.wasm` from a CDN. | Lottie *free* assets, or GSAP/CSS. |
| **SVGator** free export | **Watermark** on every free export. | Pay for watermark-free, or hand-author. |
| **LottieFiles** "Premium/Marketplace" | Paid, separate license — looks identical to free assets in the UI. | Use only assets explicitly marked **free** (Lottie Simple License: commercial OK, no attribution). |
| **OGL**, **@shadergradient** | ESM-only, **no UMD/global build** → can't be vendored as one `<script src>` without a bundler/import-map. | Three.js r160, regl (both have real globals). |

**Always-safe to inline/use commercially** (license verified): `stegu`/`ashima`
`webgl-noise` (MIT `snoise`), `glsl-atmosphere` (Unlicense), **Three.js** (MIT),
**GSAP 3.13+** (free incl. commercial since the 2025 Webflow acquisition, no
attribution), **tsParticles** (MIT), **lottie-web** player (MIT), **Lucide** icons
(ISC), **Anime.js** (MIT), **Motion One** (MIT), CC0 assets from **Poly Haven /
ambientCG / Kenney / Quaternius / NASA**.

> Algorithms and visual *techniques* are not copyrightable — only specific code is.
> Reading a Shadertoy to learn "how do they do aurora," then writing your own GLSL,
> is clean-room and 100% safe. That is the recommended default for shader work.

---

## Technique catalog

Ranked by leverage for an offline dark-keynote deck. ⭐ = a working demo exists in `demos/`.

| Technique | Offline | Wow | Effort | Notes |
|-----------|---------|-----|--------|-------|
| **CSS animated gradients / aurora blobs** | ✅ Inline | 5 | Low | The re:Invent look itself (style #2); the grid + glow background is the style #1 default. |
| ⭐ **CSS 3D (cube / 2.5D parallax)** | ✅ Inline | 5 | Med | `demos/css-3d-hero/` (purple only). Zero deps, Baseline since 2015. |
| ⭐ **Pointer-driven 3D tilt** | ✅ Inline | 5 | Med | `demos/pointer-tilt/` + `demos/neon/pointer-tilt/`. Hand-written; cards/hero tilt toward cursor + specular sheen. Zero deps. |
| ⭐ **Hand-written WebGL shader bg** (snoise) | ✅ Inline | 5 | Med | `demos/webgl-nebula/` + `demos/neon/webgl-nebula/`. ~5 KB, MIT noise, total control. |
| ⭐ **Three.js real 3D** (emissive + bloom) | ✅ Vendorable | 5 | High | `demos/threejs-hero/` (purple only). Genuine 3D centerpiece: emissive core, fresnel shell, **inline hand-rolled bloom** (no ESM addons), ACES. r160 UMD global, ~654 KB raw. |
| ⭐ **GSAP timelines / kinetic type** | ✅ Vendorable | 5 | Med | `demos/gsap-title/` + `demos/neon/gsap-title/`. Free+commercial, ~71 KB+. Orchestration, SplitText, DrawSVG, MorphSVG. |
| ⭐ **GSAP content micro-effects** | ✅ Vendorable | 4 | Med | `demos/gsap-micro/` (purple only). Number count-up, text scramble/decode, SVG path-draw + staggered timeline. |
| ⭐ **Hand-written constellation / network** | ✅ Inline | 4 | Low | `demos/particles-network/` + `demos/neon/particles-network/`. 2D-canvas linked dots + cursor-grab. ~5 KB, zero deps (see note on tsParticles below). |
| **View Transitions API** (slide morph) | ✅ Inline | 5 | Low | Baseline Oct 2025; 1-line fallback to plain cut. Same-document only (no CORS, works file://). |
| **`@property` spinning conic gradient** | ✅ Inline | 5 | Low | Rotating neon ring/halo. Baseline 2024; degrades to static. Must set `initial-value`. |
| **Self-drawing neon SVG line** | ✅ Inline | 4 | Med | `stroke-dashoffset` animation. Use CSS (not SMIL). Few paths only. See `demos/gsap-micro/`. |
| **lottie-web + free Lottie asset** | ✅ Vendorable | 4 | Low | MIT player. Inline the JSON via `animationData` (never `path:` URL). ~164 KB `lottie_light`. |
| **`backdrop-filter` glass** | ✅ Inline | 5 | Med | **Needs `-webkit-` prefix** (Safari). Recent baseline; ancestor `filter/opacity` breaks it. |
| **Scroll-driven animations** | ⚠️ Inline | 2 | — | **Skip as core**: Firefox off-by-default, doesn't fit click-advanced slides. |

---

## ⭐ Demo 1 — WebGL nebula background (`demos/webgl-nebula/` · Neon: `demos/neon/webgl-nebula/`)

Hand-written **WebGL1** fragment shader: single-layer domain-warped fBm over MIT
`snoise`, confined to a soft off-center elliptical **mass** and graded to the
palette, with vignette + additive glow. Replaces the earlier
procedural-earth attempt with a cleaner, more "premium backdrop" look. The Neon
variant grades the same shader to cyan/magenta (the GLSL `vec3` constants are swapped
per the token table — a `:root` swap alone won't change the rendered colors).

**Why it's the recommended primary 3D-ish route:** zero dependencies, zero license
risk (snoise is MIT, keep its header comment), ~5 KB inline, total aesthetic control.

Baked-in robustness (copy these patterns):
- WebGL1 via `getContext("webgl")` + a real 3-vertex buffer (no `gl_VertexID`).
- `precision highp float;` at the top (mediump bands the noise).
- DPR capped at `Math.min(dpr, 1.5)`; render throttled to ~30 fps.
- Pause on `visibilitychange`; rebuild on `webglcontextlost`/`restored`.
- `prefers-reduced-motion` → render one static frame, no loop.
- CSS radial-gradient fallback if WebGL is unavailable (never a blank screen).

```js
// minimal skeleton — full version in demos/webgl-nebula/index.html
const gl = canvas.getContext("webgl", {antialias:false, alpha:false,
  depth:false, stencil:false, powerPreference:"low-power"});
// fragment shader: precision highp float; + Ashima snoise (MIT header kept) + fbm()
// loop: cap to 30fps, drift a time uniform, drawArrays(TRIANGLES,0,3)
```

**Avoiding the "liquid marble" trap** (this demo was retuned to fix exactly this):
- **One warp layer, low gain.** Two stacked domain warps at high gain (`p + 3.5*q`)
  produce tight closed-loop vortices that read as veined marble. A single low-gain
  warp (`p + 0.9*q`) keeps broad, drifting, gaseous streaks.
- **Low base frequency + fewer octaves.** `uv * ~0.7` and 4 octaves (drop the finest)
  removes hair-thin ridges. Soft fbm gain (`f*0.45+0.5`) keeps mid-tones diffuse.
- **Confine it spatially.** Don't light every pixel — multiply by a soft elliptical
  `mass` (biased away from the headline) then soft-threshold, so corners stay pure
  black. The negative space is what makes it read as a nebula, not a texture.
- **Bias hue on-brand.** Floor the primary↔blue mix toward the primary accent so it
  stays on-brand instead of drifting cold blue; let the secondary accent bloom across
  upper-mid densities. (re:Invent: floor toward purple. Neon: floor toward cyan.)

## ⭐ Demo 2 — GSAP kinetic title (`demos/gsap-title/` · Neon: `demos/neon/gsap-title/`)

GSAP **3.13** vendored locally (`vendor/gsap.min.js` + `SplitText` + `DrawSVGPlugin`).
A load timeline: per-character headline reveal → SVG underline draw → staggered cards
→ infinite glow pulse. `prefers-reduced-motion` jumps to the end state. The Neon variant
carries its own copy of `vendor/` and re-tints the headline gradient, the SVG underline
`<linearGradient>` stops, and the JS glow-pulse color to cyan/magenta.

**Licensing:** GSAP became **fully free including all former Club plugins** after the
2025 Webflow acquisition — commercial use allowed, no attribution. The only restriction
is not repackaging GSAP itself to build a competing tool. Embedding in a deck is fine.

**Offline:** download the UMD/global builds into `vendor/` and reference relatively.
If a plugin ever 404s, the demo feature-detects and falls back to hand-rolled
char-splitting + manual `stroke-dashoffset` (works with `gsap.min.js` alone).

```html
<script src="./vendor/gsap.min.js"></script>
<script src="./vendor/SplitText.min.js"></script>
<script>
  gsap.registerPlugin(SplitText);
  const split = new SplitText(".headline", { type: "chars" });
  gsap.timeline({defaults:{ease:"power3.out"}})
    .from(split.chars, {yPercent:120, opacity:0, stagger:0.04, filter:"blur(8px)"})
    .from(".underline path", {drawSVG:"0%", duration:0.8}, "-=0.3");
</script>
```

> **Icons must be Lucide, not emoji** — even inside effects demos. Both demos here
> inline Lucide SVG paths (ISC) rather than the usual CDN, so they stay offline.
> Emoji-as-icons is banned by [SKILL.md](SKILL.md).

## ⭐ Demo 3 — CSS 3D hero (`demos/css-3d-hero/`, purple only)

Pure CSS, **zero JS dependency**: a rotating `preserve-3d` cube (6 faces, Lucide-icon
glyphs, neon edges) + a 2.5D parallax title using layered `translateZ`. No Neon variant
ships yet — re-tint per the token table if you need it for a style #1 deck (colors live
in `:root` plus ~21 inline `rgba` glow/light-pool spots).

**The flattening gotcha (bake into every CSS-3D template):** an element with
`transform-style: preserve-3d` must NOT also have `opacity<1`, `filter`,
`overflow != visible`, `clip-path`, `mask`, or `mix-blend-mode` — any of those
silently collapse the 3D to flat. **Put glow/opacity/filter on children**, never on
the `preserve-3d` parent.

```css
.scene { perspective: 1100px; }
.cube  { transform-style: preserve-3d; animation: spin 18s linear infinite; }
/* glow lives on .face children, NOT on .cube */
.face  { position:absolute; backface-visibility:hidden;
         box-shadow: inset 0 0 40px var(--pink); }
.front { transform: translateZ(100px); }
.back  { transform: rotateY(180deg) translateZ(100px); }
@media (prefers-reduced-motion: reduce){ .cube{ animation:none; transform:rotateX(-20deg) rotateY(-30deg);} }
```

---

## Which effect for what

Paths show the re:Invent (purple) demo; append `neon/` for the Neon-Cyber (cyan) variant
where one exists (✅ Neon column).

| You want… | Use | Where (purple) | Neon |
|-----------|-----|----------------|------|
| A living dark background behind any slide | CSS aurora blobs (light) or WebGL nebula (rich) | `demos/webgl-nebula/` | ✅ `demos/neon/webgl-nebula/` |
| A "wow" hero object on a title/section slide | CSS 3D cube or 2.5D parallax | `demos/css-3d-hero/` | — (re-tint) |
| An interactive, cursor-responsive hero/cards | Pointer-driven 3D tilt | `demos/pointer-tilt/` | ✅ `demos/neon/pointer-tilt/` |
| A genuine 3D model/object centerpiece | Three.js r160 (emissive + inline bloom) | `demos/threejs-hero/` | — (purple only) |
| Choreographed title / kinetic typography | GSAP timeline + SplitText | `demos/gsap-title/` | ✅ `demos/neon/gsap-title/` |
| Animated metrics / decoding text / drawn timeline | GSAP content micro-effects | `demos/gsap-micro/` | — (re-tint) |
| Network/constellation backdrop | Hand-written 2D-canvas constellation | `demos/particles-network/` | ✅ `demos/neon/particles-network/` |
| Every effect at once (integration test) | Combined 5-slide deck | `demos/all-effects/` | — (purple only) |
| Slide-to-slide "magic move" morph | View Transitions API | research only | — |
| A pre-made animated illustration | lottie-web + a **free** Lottie JSON (inlined) | research only | — |

For weight discipline: a deck should lean on **inline CSS/shader** effects first.
Reserve a vendored engine (GSAP, Three.js) for the one or two slides that truly need
it — don't ship 1.8 MB of Babylon for a background a 5 KB shader could draw.

### Three.js notes (demo: `demos/threejs-hero/`)

A real WebGL engine for genuine 3D. The bundled demo is an abstract "compute core"
(emissive faceted icosahedron + counter-rotating fresnel shell + orbiting glow sprites
+ starfield), NOT a procedural planet — see the lesson at the end. Key facts:

- **Vendor r160** — the **last release with a UMD `build/three.min.js`** that sets a
  global `window.THREE` (`<script src="./vendor/three.min.js">`, works offline).
  r161+ are ESM-only and would force an import map or bundler, breaking the
  double-click-offline model. Pin r160. MIT license. A harmless r160 console
  deprecation warning about the UMD build is expected.
- **Weight:** `three.min.js` ≈ 654 KB raw / ~163 KB gzip — the single biggest asset
  in a deck. Worth it only when a real 3D object is the centerpiece; otherwise
  the WebGL-shader background (`demos/webgl-nebula/`) gets a similar vibe at ~5 KB.
- **Looking keynote-grade** needs effort: the demo does **inline hand-rolled bloom**
  (bright-pass → separable gaussian blur → additive composite, as `ShaderMaterial`s +
  `WebGLRenderTarget`s) because the `EffectComposer`/`UnrealBloomPass` addons live in
  `examples/jsm/` and are ESM-only. Plus ACES filmic tone mapping, emissive PBR, and a
  fresnel rim shell. (Alternatively, adapt the addon files: `import {X} from 'three'` →
  `const {X}=THREE;`.)
- **Compose off-centre with `camera.setViewOffset`** — the demo keeps the object at
  world origin but slides the projection so it renders in the right third, leaving the
  left clear for the headline. Cleaner than moving the object + re-aiming the camera.
- **Free CC0 assets** (if you swap in a real model): Poly Haven, ambientCG, Kenney,
  Quaternius, NASA (US public domain). Inline budget ≤ ~15–25 MB; textures dominate —
  use 1k/2k HDRIs, meshopt (MIT) over Draco.

> An earlier Three.js rotating-**earth** demo was prototyped and removed — the
> procedural planet read as amateur. The lesson held: the replacement is an **abstract
> emissive object**, which looks keynote-grade without needing photoreal textures. If
> you do want a real model, start from a CC0 asset, not procedural noise.

### tsParticles note — verify before trusting it

The catalog lists tsParticles as vendorable (MIT, `window.tsParticles`), and the model
loads fine offline. **But in this skill's offline verification the bundled v3
`tsparticles.bundle.min.js` populated its particle model yet never painted a single
pixel to its canvas** (a manual `fillRect` on the same 2D context worked, so the
context was fine — the engine's own render loop didn't reach the screen). Rather than
ship an effect that couldn't be verified, `demos/particles-network/` (purple) and
`demos/neon/particles-network/` (cyan) are a **hand-written
2D-canvas constellation** (~5 KB, zero deps): drifting dots, squared-distance link test,
cursor-grab lines, click-to-add. It's lighter and fully controllable. The Neon variant
re-tints the JS `COLORS` RGB-triple array and the link/grab stroke strings, not just
`:root`. **Lesson:** for an
effect this simple, a hand-written canvas loop beats a ~180 KB engine — and always
confirm pixels actually render (sample the canvas / screenshot), not just that the
library "loaded".

---

## Offline-verification checklist (run before shipping any effect)

1. **Double-click the `.html` from a fresh location** (or `file://`) with **Wi-Fi
   off**. It must fully render and animate — no blank canvas, no missing fonts/icons.
2. **No runtime network refs:** `grep -nE "https?://(cdn|unpkg|jsdelivr|fonts\.)" file.html`
   should return nothing (a local `vendor/` `<script src="./...">` is fine).
3. **Vendored files present & non-trivial:** every `vendor/*.js` exists and is the
   real build (e.g. GSAP > 3 KB, Three.js > 100 KB).
4. **No emoji as icons:** icons are Lucide SVG (inlined when offline). Grep for emoji.
5. **Viewport fit:** each slide still fits 100vh — heavy effects must not push layout
   or add scrollbars (see [SKILL.md](SKILL.md) viewport rules).
6. **`prefers-reduced-motion`:** animations stop/jump-to-end when the OS pref is set.
7. **Console clean:** no errors in DevTools (a single Three.js r160 UMD deprecation
   warning is expected and harmless).
8. **WebGL fallback:** if the effect uses WebGL, confirm a CSS fallback shows when the
   context is unavailable.

---

## Verified facts (as of 2026-06, with sources to re-confirm for legal-grade use)

- **GSAP** is free incl. commercial + all plugins since the 2025 Webflow acquisition
  (gsap.com/pricing, GitHub README). Not MIT — GreenSock's "no-charge" license.
- **Three.js r160** is the **last release with a UMD `build/three.min.js`** (global
  `window.THREE`); r161+ are ESM-only. Stay on r160 for the vendored-global path.
- **Spline** native export requires a paid plan — the blocker that ruled it out.
- **Shadertoy** default = CC BY-NC-SA 3.0 (NonCommercial + ShareAlike).
- CC0 asset hubs: Poly Haven, ambientCG, Kenney, Quaternius, NASA (US public domain).

GSAP's verbatim license page and LottieFiles' license page intermittently 403'd
during research — quote the live pages for any legally binding decision.
