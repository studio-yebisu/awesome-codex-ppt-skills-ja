# Diagram Reference — Native SVG/CSS Framework (+ drawio for AWS only)

Integration patterns for rendering rich diagrams inside slides. Read this file when generating slides that contain `### diagram` blocks in content.md.

**The routing rule (decides everything else):**

| `type:` | Renderer | Why |
|---------|----------|-----|
| `flowchart` (default), `sequence`, `class`, `er`, `network`, `mindmap`, `arch` | **Native inline SVG/CSS** — hand-drawn by the skill, directly in the slide | Vector, zero-dependency, theme-native colors, **animatable** (packets flowing along edges, staggered entrances, hover-highlight). PNG exports can't do any of this. |
| `aws` / `architecture` with AWS services | **drawio skill → PNG** (legacy path, see end of file) | The official AWS service icon set is the one thing worth a raster export. |

The old drawio-for-everything path produced broken arrowheads (crow's-foot ticks rendered wrong), washed-out layouts, and dead raster images that clash with an otherwise animated deck. Native SVG fixes all three and needs **no CLI install** for the common diagram types.

> `arch` (non-AWS architecture) is drawn natively — either flat (routed edges between service cards) or as the isometric 3D showpiece below. Only diagrams that need *official AWS icons* go to drawio.

---

## Parsing content.md `### diagram` Blocks

```
### diagram
type: sequence
caption: POST /orders 从客户端到数据库再回来
animate: flow
Client -> API Gateway: POST /orders
API Gateway -> Lambda: Invoke
Lambda -> DynamoDB: PutItem
DynamoDB --> Client: 201 Created
```

**Parsing rules:**

1. `type:` (optional, default `flowchart`) → one of:
   `flowchart` | `sequence` | `class` (UML) | `er` | `network` | `mindmap` | `arch` | `aws`/`architecture`
2. `caption:` (optional) → one muted line under the diagram.
3. `title:` (optional) → falls back to the slide heading.
4. `animate:` (optional) → `flow` (default: packets/entrance choreography) | `static` (entrance only, no ambient loop) | `none`.
5. Every remaining non-empty line → the **description**: prose, arrow flows (`A -> B: label`, `-->` for dashed/return), or bullets. The skill designs the geometry from this.

**Validation (Step 4 content review):**
- Unknown `type` → warn, fall back to `flowchart`.
- Empty description → flag as an empty diagram.
- Only if the deck contains a `type: aws` block: note that AWS diagrams need the draw.io desktop CLI (`drawio`) and flag once if missing. **Native types need nothing.**

---

## Native Diagram Framework

**Working, Chrome-verified reference demos — copy their code, don't reinvent:**

| Demo | Type | Palette | Signature techniques |
|------|------|---------|---------------------|
| `../demos/diagrams/01-flowchart-flow/` | flowchart | re:Invent purple | node pop + edge draw-in choreography, SMIL packets chained through the graph, dashed marching-ants return edge, golden-node glow pulse |
| `../demos/diagrams/02-sequence-api/` | sequence | Neon cyan | lifelines + growing activation bars, 7 messages fired strictly in order, **two-clock sync** (SMIL packets + CSS delays from one delay table), JS cycle loop |
| `../demos/diagrams/03-er-schema/` | er | re:Invent purple | **geometrically correct crow's-foot markers** (the drawio failure case), entity cards with PK/FK tags, hover/click subtree highlight |
| `../demos/diagrams/04-arch-isometric-3d/` | arch (3D) | re:Invent purple | CSS isometric plane (`rotateX(55°) rotateZ(-45°)`), extruded tiles, billboarded labels, request/response packet waves, pointer tilt |
| `../demos/diagrams/05-mindmap-radial/` | mindmap | Neon cyan | radial bezier limbs, staggered bloom entrance, per-branch ambient drift, subtree hover highlight |

All five are single-file, offline, zero-dependency, emoji-free (Lucide inline), `prefers-reduced-motion`-safe, console-clean. When generating a diagram slide, open the matching demo and adapt its patterns to the deck's palette and content.

### Core rules (every native diagram)

1. **Inline `<svg>` with a fixed design grid** — design at `viewBox="0 0 1400 H"` (H ≈ 640–760), hand-place coordinates generously, let CSS scale it (`width:100%; max-height:60vh`). Never compute layout at runtime.
2. **Text via `<text>` + `<tspan>`** (never `foreignObject`). Hand-wrap CJK; keep effective font ≥14px.
3. **Arrowheads/markers are hand-built geometry** — either `<marker>` defs (one per color: `markerUnits="userSpaceOnUse"`, explicit `fill`, since markers can't inherit CSS vars) or, when the tip must animate on arrival, a plain `<polygon>` popped in with the arrival FX. Crow's-foot: "exactly one" = two perpendicular ticks; "many" = three-prong foot opening toward the entity (see demo 03's commented defs).
4. **Edge labels on dark pills**: small `rx=10+` rect filled with the slide bg color + edge-color border at ~40% alpha, sitting on the path midpoint. This is what kills the drawio white-box label problem.
5. **Theme-native colors**: use the preset's `--chart-colors` + accents as **literal hex inside the SVG attrs**, matching chart slides. Node fill `rgba(accent,0.06-0.1)` + 1.5px accent stroke + soft `drop-shadow` glow on dark themes.
6. **No emoji** — Lucide paths inlined (24×24 stroke icons). Same ban as everywhere in this skill.

### Animation choreography (the whole point)

Standard two-phase pattern (see demos 01/02 for full implementations):

- **Phase A — entrance (~2–2.5s, replayable)**: nodes pop staggered (`scale(.85)→1` + fade, `transform-box:fill-box; transform-origin:center`), edges draw in via `pathLength="1"` + `stroke-dasharray:1; stroke-dashoffset:1→0` (length-independent), arrowheads/badges pop on arrival.
- **Phase B — ambient loop**: glowing packets ride the edges via SMIL `<animateMotion><mpath href="#edge-path"/></animateMotion>`; dashed return edges run a marching-ants `stroke-dashoffset` loop; key nodes breathe (slow glow pulse).
- **Two-clock sync** (when packets must line up with CSS FX): one hidden SMIL `<animate id="clock">` kicked by JS `beginElement()`; every packet begins at `clock.begin+OFFSETs`; CSS `animation-delay`s use the same offsets; document both in ONE delay-table comment. Restart cycle = remove/re-add `.play` class + `clock.beginElement()` (demo 02).
- **In-slide activation**: inside a deck, start the choreography when the slide becomes active (hook the deck's existing slide-change handler or an IntersectionObserver) and reset it on leave, so the entrance replays each visit and packets don't run behind other slides.
- **`prefers-reduced-motion`**: land on the fully-drawn final state, hide packets, no loops. Default no-JS state should also be the final drawn state (never blank).

### Isometric 3D architecture (showpiece option)

For `type: arch` when the user wants the 3D look (demo 04). Key facts:
- Stack: `.scene{perspective}` → `.tilt` (pointer nudge wrapper) → `.iso-stage{rotateX(55deg) rotateZ(-45deg); preserve-3d}`. **Flattening gotcha applies** — no opacity/filter/overflow/mask on preserve-3d nodes; fades live on leaf children (see effects-reference.md).
- Tiles = pad + `translateZ(--h)` top face + two extruded side faces + blurred ground shadow; labels **billboarded** with the inverse pose (`rotateZ(45deg) rotateX(-55deg)`) and anchored well *above* the top face (`translateZ(calc(var(--h) + 34px))`) so the tilted label plane doesn't sink into the block.
- Routes live in one in-plane SVG child; packets are SMIL dots; request wave out, response wave back.
- Budget the viewport: the projected plane leans toward the viewer, so scale the stage down (~0.8×) and pull it up (negative margin) until every tile + billboarded label fits 100vh. **Verify with a screenshot** — this is the #1 regression.
- One diagram per slide; this one especially.

### Slide embedding

Native diagrams are part of the slide markup — no `<img>`, no lightbox needed (they're already full-resolution vector):

```html
<section class="slide">
    <div class="slide-content">
        <h2 class="reveal">一次 API 请求的完整流转</h2>
        <figure class="diagram-figure reveal">
            <svg class="native-diagram" viewBox="0 0 1400 640" role="img" aria-label="...">
                <!-- nodes / edges / packets, per the demo patterns -->
            </svg>
            <figcaption class="diagram-caption">POST /orders — 从客户端到数据库再回来</figcaption>
        </figure>
    </div>
    <div class="slide-footer">© 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.</div>
</section>
```

```css
/* === NATIVE DIAGRAM === */
.diagram-figure {
    display: flex; flex-direction: column; align-items: center;
    gap: clamp(0.4rem, 1vh, 0.8rem);
    width: 100%; max-width: min(1200px, 94vw); margin: 0 auto;
}
.native-diagram {
    width: 100%; height: auto;
    max-height: min(60vh, 560px);   /* viewport fit — non-negotiable */
}
.diagram-caption {
    font-family: var(--font-body);
    font-size: clamp(0.7rem, 1.1vw, 0.9rem);
    color: var(--chart-text, var(--text-secondary));
    text-align: center;
}
@media (max-height: 600px) { .native-diagram { max-height: 52vh; } }
@media (max-height: 500px) { .native-diagram { max-height: 46vh; } }
```

### Viewport fitting (NON-NEGOTIABLE)

- One diagram per slide. Heading + diagram + 1-line caption + footer is the maximum.
- Dense diagram (>~12 nodes)? **Split across two slides** (overview → detail) instead of shrinking below readability.
- Keep the 60vh cap and height breakpoints above.

### Parallel generation note

With 8+ slides (batch agents): the **lead** designs each native diagram's SVG (or delegates one diagram = one agent), because batch agents writing `<section>` markup shouldn't each invent geometry conventions. Hand a batch agent the finished `<figure>` block to inline verbatim.

---

## AWS Architecture via drawio (the one remaining drawio path)

Only for `type: aws` — when official AWS service icons materially improve the diagram. Produces a PNG in `assets/`, embedded like an image (lightbox applies).

1. **Brief** — combine `title` + description into one prompt for drawio-skill; tell it to use the official AWS shape library (its `shapesearch.py` resolves exact shapes — don't guess shape names).
2. **Export** — `.drawio` source + PNG into `assets/`:
   ```bash
   drawio -x -f png -s 2 -t -o my-presentation/assets/diagram-1.png my-presentation/assets/diagram-1.drawio
   ```
   `-s 2` = 2x for crisp text; `-t` = transparent background. **Never `-e`** (truncated-IEND corrupt PNG, drawio-skill issue #8). Cap very large diagrams with `--width 2400` instead of `-s 2`.
3. **Theme-match before export** — resolve every color to literal hex (no `var()` in .drawio XML):
   - Fills from the preset `--chart-colors`, assigned per tier/group.
   - Dark themes → light strokes/labels (`rgba(255,255,255,0.7)` / `#ffffff`); prefer outlined nodes (near-transparent fill + colored stroke) over pale solid fills. Edge/arrow color = the preset accent.
   - **Edge labels need `labelBackgroundColor` set to the slide bg hex** (e.g. `#0A0A0A`) or they render as white boxes on the transparent PNG.
   - Pass the preset body font as `defaultFontFamily` (rasterized at export).
4. **Embed** with the classic image mechanics (this is the only diagram path that still uses `<img>` + lightbox):
   ```html
   <img class="slide-image diagram-image" src="assets/diagram-1.png" alt="...">
   ```
   `.diagram-image { max-height: min(60vh, 560px); object-fit: contain; cursor: zoom-in; }` — same caps/breakpoints as native.

### Fallback chain (AWS type only)

| Scenario | Behavior |
|----------|----------|
| drawio CLI available | `.drawio` + PNG export, embed. (Preferred for `type: aws`.) |
| CLI missing, XML generated | Keep `.drawio` in `assets/`, embed a placeholder card, tell the user to `brew install --cask drawio` and re-run. |
| drawio-skill not installed | **Draw it natively instead**: service cards with Lucide icons + routed edges (the `arch` treatment) — no AWS official icons, but animated and self-contained. Tell the user. |
| Empty description | Skip, warn (caught in Step 4). |

Whatever the path, `index.html` stays self-contained: inline SVG or relative `assets/*.png` only — never an external URL.

### Prerequisite (AWS type only)

```bash
brew install --cask drawio && drawio --version
```

Mention once during Step 4 review if a `type: aws` block exists and the CLI is missing. Native diagram types have **no prerequisites**.
