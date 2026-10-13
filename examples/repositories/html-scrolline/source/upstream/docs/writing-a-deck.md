# Writing a deck

A deck is one folder, `decks/<id>/`, and its content lives in `deck.yaml`. This page covers every field, the beat types, how beats are laid out in time and the checks that run before a deck boots.

Related: [getting-started](getting-started.md) · [concepts](concepts.md) · [moves](moves.md) · [media](media.md) · [export](export.md) · [architecture](architecture.md)

## Deck folder

```
decks/<id>/
  deck.yaml        content: beats, sources, timing
  index.html       page shell with <div id="app"></div>
  main.js          boot() call: engine + moves + concept + deck
  assets/          images, videos, frame sequences (deck.yaml paths are relative to the deck folder: assets/…)
  sequences/       optional deck-only beats (type: sequence)
```

Create the folder with the CLI, then edit `deck.yaml`:

```bash
npm run deck -- new quarterly-review --concept data
```

## Top-level fields

| field | required | meaning |
|---|---|---|
| `id` | yes | `^_?[a-z0-9][a-z0-9-]*$`, same as the folder name. Ids starting with `_` are internal decks (gallery, diversity gate and batch export skip them) |
| `title` | yes | Deck title |
| `lang` | yes | `ko` or `en`. Drives word splitting and `Intl.NumberFormat` |
| `concept` | yes | A folder under `concepts/` |
| `sample` | no | `true` = fictional sample deck. The screen must say so; `source` is no longer required |
| `sources` | no | Source ledger: `{ id, title, url, accessed, short? }`. `short` is the on-screen label (`arXiv`, `Reuters`); otherwise `title` is shown |
| `timing` | no | Overrides `concept.timing`: `unit`, `hold`, `overlap`, `tail` |
| `export` | no | Overrides export path options, e.g. `secondsPerUnit` (see [export](export.md)) |
| `beats` | yes | One or more beats, in order |

Timing units are `u`. One `u` of scroll equals `viewport height × unit` pixels (default `unit: 0.55`). Engine defaults are `unit 0.55, hold 0.6, overlap 0.2, tail 0.8`, then the concept's values, then the deck's.

## Beat fields

Every beat has these common fields, plus the fields of its type.

| field | meaning |
|---|---|
| `id` | Unique in the deck, `^[a-z0-9][a-z0-9-]*$` |
| `type` | One of the beat types below; must be in the concept's `beats.allow` |
| `place` | `{ slot: center \| left \| right \| top \| bottom \| full \| lower-third }` (screen layer, camera does not affect it) or `{ world: { x, y, z?, s? } }` (world layer; `x`/`y` in screens, `z` in px, `s` scale) |
| `enter` | MoveRef: how the beat appears |
| `steps` | List of MoveRefs with `name`, run after the beat holds. Each step ends on a stop |
| `exit` | MoveRef: how the beat leaves. Ignored when `link` is set |
| `link` | MoveRef: one motion that turns this beat into the next. Cannot be on the last beat |
| `camera` | MoveRef: camera move that starts with the beat |
| `ambient` | List of MoveRefs that run for the whole life of the beat |
| `stop` | Default `true`. `false` = no main stop for this beat |
| `hold` | `u` to stay after the stop (default `timing.hold`) |
| `at` | Start offset relative to the previous beat (see timeline model) |
| `exportHold` | Seconds this stop holds in the MP4 export (default 1.6) |
| `repeat` | `intended` = allow the same move twice in the same role in this deck |
| `persist` | `true` = the beat stays visible after it ends. `place.world` beats only |
| `tone` | Integer 0..5, written as `data-tone` on the beat root; the concept's `tokens.css` can recolour per tone |
| `source` | A `sources[].id` or an array of ids |

A MoveRef is `{ move, params?, at?, override? }`:

- `move` – a move id from the registry (`npm run deck -- moves`) or a built-in `engine:fade-in`, `engine:fade-out`, `engine:crossfade`, `engine:none`
- `params` – move parameters; unknown keys and out-of-range values fail validation
- `at` – offset inside the beat (for `enter`, relative to the end of the incoming link)
- `override` – reason text, required when the move is not in the concept's allow list

`engine:none` is valid in any role and does nothing for 0 u. Use it as the `enter` of a beat that the previous beat's `link` already draws.

When a role is omitted, the move is resolved in this order:

1. the beat's own field
2. `concept.defaults.byType[type].enter|exit|link`
3. `concept.defaults.enter|exit`
4. `engine:fade-in` / `engine:fade-out`

The last beat never gets a default exit; only an `exit` you write yourself is used.

## Beat types

Renderers build the finished, at-the-stop DOM with `data-part` elements. All motion comes from moves. Text stays real DOM text.

| type | required | optional | parts | primary |
|---|---|---|---|---|
| `text` | `text` | `emphasis` (substrings), `size: xl\|l\|m`, `lines` | `block` `line` `word` `em` | `block` |
| `photo` | `src`, `alt` | `focus {x,y}`, `caption`, `credit`, `source` | `frame` `media` `caption` | `frame` |
| `video` | `src` (mp4), `poster`, `alt`, `mode: scrub\|play\|loop` | `frames` (required for scrub), `caption`, `mask {type: text\|shape, text?, shape?}`, `credit`, `source` | `frame` `media` `caption` `credit` | `frame` |
| `number` | `value`, `label` | `format {prefix, suffix, decimals, unit}`, `from`, `source` | `value` `digits` `unit` `label` `source` | `value` |
| `chart` | `kind: bar\|line\|area\|dot`, `categories`, `series [{name, values}]` | `unit`, `highlight {series?, index?}`, `title`, `dek`, `notes [{index, series?, text}]`, `orient: v\|h`, `states`, `source` | `plot` `axis` `mark` `label` `legend` `source` `title` `dek` `note` `baseline` | `plot` |
| `chronology` | `events [{date, title}]` (2+) | `events[].note/media/weight/source`, `scale: even\|time`, `axis: x\|y`, `label`, `caption`, `counter: none\|year\|month`, `ground`, `now` (0..1), `ticks: none\|year` | `track` `event` `date` `title` `note` `media` `dot` `stem` `source` `label` `caption` `counter` `reel` `ground` `ghost` `now` `tick` | `track` |
| `compare` | `items [{label}]` (2–4) | `items[].value/text/media`, `verdict`, `source` | `item` `label` `value` `text` `divider` `verdict` `source` | `item` |
| `quote` | `text`, `by` | `role`, `source` | `block` `mark` `word` `by` | `block` |
| `prompt` | `text` | `label`, `result {type: photo\|text, src?, text?, alt?}` | `field` `char` `caret` `label` `result` `word` | `field` |
| `code` | `code`, `lang` | `highlight [[from, to]]`, `caption` | `block` `line` `token` `caret` | `block` |
| `sequence` | `use` | `data` | defined by the sequence | defined by the sequence |

Notes by type:

- **chart** – `title` is the one-line claim above the plot, `dek` the supporting line, `notes` the labels next to marks. `orient: h` gives horizontal bars. Negative values grow from a zero `baseline`. `states` describes what each step changes: `{ name, kind?, series?, title?, dek?, notes?, unit? }`. Each `states[].name` must match a `steps[].name` and cannot be `base`. Text in states is pre-rendered as hidden `[data-state]` layers; the step move switches layers and morphs marks.
- **chronology** – `axis: x` is a horizontal rail. `scale: time` spaces events by real date gaps. `counter` adds rolling digit reels for the year or month. `ground` draws large ghost years behind the track. `weight: minor` makes an event secondary.
- **video** – `scrub` draws a frame sequence on canvas and is driven by scroll; `play` and `loop` use a muted `<video>` that plays while the beat is active. `mask.type: text` only marks the media; a mask move applies it. See [media](media.md).
- **sequence** – a deck-only beat for scenes no generic type covers. Write `decks/<id>/sequences/<use>.js` (default export: `{ type: 'sequence', fields, primary, render, timing(data), build(tl, ctx) }`) and pass it to `boot`. A sequence beat takes no `enter`; its own `build` plays in that span.

```js
// decks/canvas-pitch/main.js
import ground from './sequences/ground.js';
import atlas from './sequences/atlas.js';

boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  sequences: { ground, atlas },
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,
});
```

## Timeline model

There is one stage and one master timeline. Beats are not scenes with their own scroll sections; they overlap on a single time axis.

- The next beat starts `overlap` u after the previous beat's exit begins, so the screen is never empty by default. A positive `at` leaves a gap; a negative `at` overlaps more.
- If the previous beat has a `link`, the link replaces its exit: the link span plays first and the next beat's enter starts where the link ends. The link carries one part of beat A into the place of a part of beat B.
- Inside a beat: incoming link → `enter` → stop → `hold` → each step (each ending on its own stop and hold) → `exit` or outgoing `link`. `camera` runs in parallel from the beat start; `ambient` runs for the beat's whole life.
- Stops are timeline labels: `stop:<beatId>` at the end of the enter, and `stop:<beatId>/<stepName>` at the end of each step (or `stop:<beatId>/<n>` for unnamed steps). Some enter moves add internal stops.
- The plan is computed without a DOM, so the same `t` shows the same content at any viewport size, in portrait, and with reduced motion.

Inspect the computed stops and spans:

```bash
npm run deck -- plan quarterly-review
```

The output is the `TimelineMap` JSON (`duration`, `stops[]`, `beats[].spans[]`). The CLI accepts only ids without a leading `_`.

## Content audit

`validateDeck` runs in `boot` before anything renders. On failure the page lists the errors and the deck does not start.

| rule | error message |
|---|---|
| Any string (including move params, `states`, `notes`) matching a placeholder: `TODO`, `TBD`, `lorem`, `ipsum`, `xxx`, `「x」`, `???`, `{{`, `}}`, `<placeholder>`, `자리표`, `예시 문구`, empty or whitespace-only | `placeholder text is not allowed` |
| Move outside `concept.moves.allow` without `override` | `required for move outside concept allow list` |
| `number`, `chart`, `quote`, `photo`, and `compare` with any `items[].value` need `source` (unless `sample: true`) | `source is required` |
| Same move in the same role twice without `repeat: intended` (`engine:none` exempt) | `<move> repeats as <role> without repeat: intended` |
| `persist: true` on a slot beat, `tone` outside 0..5, `link` on the last beat, chart state names not matching steps | error with the field path |

Each error carries a path such as `deck.beats[1].source`.

## Example: sample deck

A fictional deck needs no sources. Defaults come from the `data` concept: `line-mask-rise` for text, `count-roll` for number, `baseline-grow` for chart.

```yaml
id: quarterly-review
title: "Q3 review"
lang: en
concept: data
sample: true
beats:
  - id: b-open
    type: text
    text: "Q3 revenue grew for the third quarter in a row"
    emphasis: ["third quarter"]
    place: { slot: center }

  - id: b-total
    type: number
    value: 4.2
    format: { prefix: "$", suffix: "M", decimals: 1 }
    from: 0
    label: "Q3 revenue"
    place: { slot: center }

  - id: b-trend
    type: chart
    kind: bar
    categories: ["Q1", "Q2", "Q3"]
    series:
      - { name: "Revenue ($M)", values: [3.1, 3.6, 4.2] }
    unit: "$M"
    title: "Each quarter added about $0.5M"
    states:
      - name: steps
        notes:
          - { index: 1, text: "+0.5" }
          - { index: 2, text: "+0.6" }
    place: { slot: full }
    steps:
      - { name: steps, move: annotation-pin }
    exportHold: 2.4
```

This plans to four stops: `b-open`, `b-total`, `b-trend`, `b-trend/steps`.

## Example: sourced deck

Real figures need a source id on the beat.

```yaml
id: ev-brief
title: "EV sales brief"
lang: en
concept: data
sample: false
sources:
  - { id: s1, short: "OWID", title: "Our World in Data, Number of new electric cars sold", url: "https://ourworldindata.org/grapher/electric-car-sales", accessed: "2026-10-08" }
timing:
  hold: 1.0
beats:
  - id: b-open
    type: text
    text: "Electric car sales, 2015 to 2025"
    place: { slot: center }
    enter: { move: line-mask-rise, params: { stagger: 0.14 } }
    exit: { move: "engine:fade-out" }
  - id: b-sales
    type: chart
    kind: bar
    categories: ["2015", "2020", "2025"]
    series:
      - { name: "Sales (M)", values: [0.52, 2.98, 21.2] }
    unit: "M"
    title: "Sales grew forty-fold in ten years"
    source: s1
    place: { slot: full }
    exportHold: 2.0
```

For larger references, read the shipped decks: `decks/data-ev-shift` (chart steps and links), `decks/rail-ai-decade` (chronology, camera, world placement), `decks/canvas-pitch` (sequences, persist).

## Previewing

```bash
npm run dev
# http://localhost:5173/decks/quarterly-review/
```

Scroll or use the presenter keys (→ ↓ Space PageDown next, ← ↑ Shift+Space PageUp previous, Home, End, `b` or `.` blackout, `f` fullscreen).

- `?motion=reduce` forces reduced motion: smooth scrolling off, keys jump instantly, `reduce: 'fade'` moves become same-length fades, so every stop stays at the same `t`.
- `window.__deck` exposes `map`, `tl`, `time()`, `seek(t)`, `goto(name)` and `stops()` in the browser console, e.g. `__deck.goto('b-trend/steps')`.
