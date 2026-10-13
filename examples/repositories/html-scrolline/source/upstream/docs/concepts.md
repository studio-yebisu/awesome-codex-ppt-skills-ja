# Concepts

A concept pack decides how a deck moves: camera axis, timing, eases, which beat types and moves are allowed, and the colours and type. Two decks with different concepts should not read as the same deck with new pictures.

Related: [getting-started](getting-started.md) · [writing-a-deck](writing-a-deck.md) · [moves](moves.md) · [media](media.md) · [export](export.md) · [architecture](architecture.md)

## Shipped concepts

| id | name | axis | signature moves | motion grammar | typical use |
|---|---|---|---|---|---|
| `rail` | Horizontal timeline rail | x | `rail-advance` `era-shift` `counter-handoff` | Scrolling down runs time sideways. Scroll distance is proportional to real date gaps; a year counter rolls and arriving events rise off the rail. Light almanac-paper theme | Company history, roadmaps, a decade of an industry |
| `data` | Data journalism | free (camera fixed) | `dot-multiply` `mark-morph` `annotation-pin` | The chart is the stage and the camera never moves. One dot multiplies, dots become bars, bars become a line, the line end unfolds into a 100-cell grid. One screen = one claim | Quarterly results, market analysis |
| `launch` | Product launch | z (camera fixed) | `lit-from-dark` `sticky-scrub-link` `number-slam` | A fixed tripod on a dark stage. Light and rendered frames move, not the camera; scroll turns and opens the product | Product and feature launches |
| `zoom` | Infinite zoom drill-down | z | `zoom-dive` `zoom-surface` `depth-ladder` | A small thing on screen (one bar, one number, one cell) is the entrance to the next scene. Exponential zoom into it; depth of zoom = depth of the argument, then back out | Root-cause reports, TAM-SAM-SOM, org structure |
| `canvas` | Canvas fly-through | xyz | `arc-flight` `establish-crane` `atlas-pullback` | A camera flies over one large map, lands on each region to speak, then pulls back to show the whole route. Pan, altitude arc and tilt in one flight | Pitch decks, strategy maps, processes |
| `kinetic` | Kinetic type lecture | free (camera fixed) | `word-door` `slot-pick` `phrase-fold` | Letters are the stage and do the camera's work. Sentences are typed, rewound, folded; one slot becomes another word; a word opens as a door onto video | Lectures, keynotes, statements |

Each concept has one example deck in `decks/` (`rail-ai-decade`, `data-ev-shift`, `launch-orbit-note`, `zoom-root-cause`, `canvas-pitch`, `kinetic-next-word`).

## Pack layout

```
concepts/<id>/
  concept.json   axis, camera, timing, eases, allowed beats and moves, defaults, slots, tokens
  tokens.css     colours, fonts, sizes as --sl-* CSS variables, scoped to .sl-concept-<id>
  index.js       import concept from './concept.json' with { type: 'json' }; export default concept;
  layout.css     optional: per-type beat layout for this concept
```

Decks import `index.js` and `tokens.css` (and `layout.css` when present) from `main.js`. Concepts may import only from `moves/index.js` and `engine/index.js`; one concept never imports another (rule R4 in `tools/check-deps.mjs`).

## concept.json

```json
{
  "id": "data",
  "name": "데이터 저널리즘",
  "axis": "free",
  "camera": { "mode": "fixed", "perspective": 2400 },
  "timing": { "unit": 0.6, "hold": 0.9, "overlap": 0.15, "tail": 1.0 },
  "eases": { "in": "power2.in", "out": "power3.out", "inout": "sine.inOut", "scrub": "none", "settle": "power4.out" },
  "beats": { "allow": ["text", "chart", "number", "compare", "video", "quote", "photo"] },
  "moves": {
    "allow": ["dot-seed", "dot-multiply", "mark-morph", "annotation-pin", "baseline-grow", "line-mask-rise", "count-roll", "recede", "engine:fade-in", "engine:fade-out", "engine:none"],
    "signature": ["dot-multiply", "mark-morph", "annotation-pin"],
    "params": { "count-roll": { "unitSlide": 8 } }
  },
  "defaults": {
    "enter": "line-mask-rise",
    "exit": "engine:fade-out",
    "byType": {
      "chart": { "enter": "baseline-grow", "exit": "recede" },
      "number": { "enter": "count-roll", "exit": "recede" }
    }
  },
  "slots": { "left": { "x": 0.3, "y": 0.52 }, "lower-third": { "x": 0.0625, "y": 0.8 } },
  "tokens": { "stagger": 0.04, "dotRadius": 9, "dotGap": 6, "mutedAlpha": 0.35 }
}
```

Abridged from `concepts/data/concept.json`. The shipped packs do not set `moves.params` yet; the `count-roll` preset above shows the shape.

| field | meaning |
|---|---|
| `id`, `name` | Folder name and display name |
| `axis` | Main motion axis: `x`, `z`, `xyz`, `free` (descriptive) |
| `camera` | `mode` and `perspective` (px) for `.sl-viewport` |
| `timing` | `unit`, `hold`, `overlap`, `tail`; a deck's `timing` overrides these |
| `eases` | Aliases for `ctx.ease('in' \| 'out' \| 'inout' \| 'scrub' \| …)`. Unknown names pass through as GSAP ease strings |
| `beats.allow` | Beat types a deck of this concept may use |
| `moves.allow` | Moves a deck may use without `override` |
| `moves.signature` | Moves that identify the concept; each deck should use them at least once |
| `moves.params` | Per-concept param presets: `{ "<moveId>": { "<param>": value } }` |
| `defaults` | Default `enter` / `exit`, and per type `byType[type].enter \| exit \| link` |
| `slots` | Slot positions (below) |
| `tokens` | Numbers only, read by moves as `ctx.tokens` (e.g. `blurMax`, `stagger`, `depthNear`, `depthFar`, `dimOthers`) |

### Param presets

A move's params resolve in this order, and the merged result is checked against the move's schema (unknown preset keys fail too):

1. the beat's `MoveRef.params`
2. `concept.moves.params[moveId]`
3. the move's schema defaults

Presets give one shared move a concept-specific texture (for example `blur-drop` drops by word in `kinetic` and leaves as a block in `zoom`) without branching on concept id inside the move.

### Slots

`place: { slot: <name> }` positions a beat from `SLOT_DEFAULTS` (in `engine/constants.js`) with the concept's `slots[name]` merged key by key:

| key | meaning |
|---|---|
| `x`, `y` | Anchor position as a fraction of the screen |
| `ax`, `ay` | Anchor point inside the block: 0 = left/top edge, 0.5 = centre, 1 = right/bottom edge |
| `w` | Maximum width as a fraction of the screen |

The engine applies them as inline `left`, `top`, `translate` and `max-width`. The `transform` property is reserved for moves. `left` and `lower-third` anchor the block's left edge (`ax: 0`) so lines of different length start at the same place; `right` uses `ax: 1`; `full` fills the stage.

## tokens.css

`tokens.css` defines only these variables, inside `.sl-concept-<id>`:

| variables | meaning |
|---|---|
| `--sl-bg` `--sl-fg` `--sl-fg-muted` `--sl-accent` `--sl-accent-2` `--sl-rule` `--sl-scrim` | Colours |
| `--sl-font-display` `--sl-font-text` `--sl-font-mono` | Font families |
| `--sl-weight-display` `--sl-weight-text` | Weights |
| `--sl-size-xl` `--sl-size-l` `--sl-size-m` `--sl-size-s` `--sl-size-caption` | Sizes, written `calc(var(--px) * N * 1px)` |
| `--sl-leading-display` `--sl-leading-text` `--sl-tracking-display` | Line height and tracking |
| `--sl-perspective` | Perspective of `.sl-viewport` |
| `--sl-gutter` `--sl-radius` | Margins and corners |
| `--sl-caption-left` `--sl-caption-bottom` `--sl-caption-width` | Photo and video caption column |

The engine sets `--px` (1 at 1920 px wide landscape, `w / 760` in portrait), `--vw-px`, `--vh-px` and `--sl-portrait` on the stage; concepts do not override them. Sizes in design pixels therefore scale with the screen.

Tones: a beat with `tone: N` gets `data-tone="N"` on its root. `tokens.css` may redefine the same variables per tone, with no new names:

```css
.sl-concept-rail [data-tone="0"] { --sl-bg: #efe9dd; --sl-accent: #8a5a1f; --sl-rule: #c9bfae; }
.sl-concept-rail [data-tone="1"] { --sl-bg: #e6eaee; --sl-accent: #1f4fbf; --sl-rule: #b7c1cc; }
```

Moves never read CSS variables in tweens. Before building, the engine reads `--sl-bg`, `--sl-fg`, `--sl-fg-muted`, `--sl-accent`, `--sl-accent-2`, `--sl-rule` and `--sl-scrim` from each beat root (so tone is included) and passes the computed strings as `ctx.colors`.

Fonts are loaded by the deck's `index.html` (`<link>` to the font CSS). `tokens.css` only names them.

## layout.css

Base beat layout comes from `engine/engine.css`, which styles parts by class (`sl-<type>__<part>`). A concept that needs a different arrangement for a type (the rail concept turns `chronology` into a horizontal almanac rail) puts it in `concepts/<id>/layout.css`:

- every selector scoped to `.sl-concept-<id>`
- colours only through `var(--sl-*)`
- no `!important`, no `@import`

Import it after `tokens.css` in the deck's `main.js`. `npm run deck -- new` adds that import when the concept has a `layout.css`.

## Adding a concept

1. Create `concepts/<id>/` with a lowercase kebab-case id.
2. Write `concept.json`. Start `moves.allow` from existing moves (`npm run deck -- moves`), pick one to three as `signature`, set `defaults` so a deck with no explicit moves still has an enter and exit per type.
3. Write `tokens.css` with every variable in the table above.
4. Add `index.js`:

   ```js
   import concept from './concept.json' with { type: 'json' };
   export default concept;
   ```

5. Scaffold a deck and preview it:

   ```bash
   npm run deck -- new my-deck --concept <id>
   npm run dev
   # http://localhost:5173/decks/my-deck/
   ```

6. Run `npm run ci`. `check-deps` fails if the concept imports another concept, a deck, or `gsap` directly.

If the concept needs a motion that no move provides, write the move first ([moves](moves.md)), then add its id to `moves.allow`. Behaviour that only one deck needs belongs in a `sequence` beat inside that deck, not in the concept.
