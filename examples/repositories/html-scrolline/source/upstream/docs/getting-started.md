# Getting started

This guide takes you from a fresh clone to a running deck of your own and an MP4 export.

## 1. Install

| Tool | Needed for | Check |
|---|---|---|
| Node.js 22 or newer | everything | `node --version` |
| ffmpeg on `PATH` | cutting frame sequences from video | `ffmpeg -version` |
| HyperFrames CLI, fetched by `npx` | MP4 export, stop capture, `smoke --driver chrome` | `npx hyperframes --version` |

```bash
git clone https://github.com/gongnyang/awesome-html-scrolline-deck.git
cd awesome-html-scrolline-deck
git checkout v2
npm install
```

`.npmrc` sets `legacy-peer-deps=true`, which the vitest 5 and vite 8 peer ranges need.

## 2. Open an example deck

```bash
npm run dev
```

Vite serves every deck folder. Open one of these:

| URL | Concept |
|---|---|
| `http://localhost:5173/decks/rail-ai-decade/` | rail |
| `http://localhost:5173/decks/data-ev-shift/` | data |
| `http://localhost:5173/decks/launch-orbit-note/` | launch |
| `http://localhost:5173/decks/zoom-root-cause/` | zoom |
| `http://localhost:5173/decks/canvas-pitch/` | canvas |
| `http://localhost:5173/decks/kinetic-next-word/` | kinetic |

Scroll with the wheel, or use <kbd>→</kbd> and <kbd>←</kbd> to move between stops. Add `?motion=reduce` to the URL to see the reduced-motion version. In the browser console, `window.__deck` exposes `time()`, `seek(t)`, `goto(name)` and `stops()`.

## 3. Create a deck

```bash
npm run deck -- new my-review --concept data
```

The `--` is required so npm passes `--concept` through. The command creates:

```text
decks/my-review/
  deck.yaml     id, title, lang, concept, sample, sources: [], beats: []
  index.html    <div id="app"> + main.js
  main.js       imports engine, moves, the concept pack and deck.yaml, then calls boot()
  assets/
```

Deck ids are lowercase kebab-case and must match the folder name. Pick the concept by the motion your story needs (see [concepts.md](concepts.md)):

| Your story | Concept |
|---|---|
| events along time | `rail` |
| numbers and charts that change | `data` |
| one product, revealed | `launch` |
| from the big picture down to one cause | `zoom` |
| several areas on one map | `canvas` |
| a talk carried by sentences | `kinetic` |

Check that `main.js` passes the build mode to `boot`. Export needs it:

```js
boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,
});
```

## 4. Write beats

Replace `beats: []` in `decks/my-review/deck.yaml`. This deck is complete and valid for the `data` concept:

```yaml
id: my-review
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

No beat names an `enter` or `exit` move, so the concept defaults apply. For `data`, these are `line-mask-rise` for text, `count-roll` then `recede` for numbers, and `baseline-grow` for charts. `sample: true` marks the figures as fictional. A deck with real figures sets `sample: false` and gives every number, chart, quote, photo and valued compare a `source` from its `sources` list.

Field reference: [writing-a-deck.md](writing-a-deck.md).

## 5. Check the plan

```bash
npm run deck -- plan my-review
```

This prints the timeline map that the engine computes in node, with no browser. For the deck above, it gives these stops:

```text
b-open        t = 0.80
b-total       t = 3.25
b-trend       t = 5.50
b-trend/steps t = 7.30
duration 8.30 u
```

Each stop is where a presenter key lands. `b-trend/steps` is the stop after the `annotation-pin` step. Open `http://localhost:5173/decks/my-review/` to see it run. If validation fails, the page lists every error with its path, for example `deck.beats[1].source: source is required`.

## 6. Smoke test in a browser

```bash
npm run dev -- --port 5190            # terminal 1
node tools/smoke.mjs my-review --driver chrome --shots   # terminal 2
```

Smoke boots the deck, seeks to every stop and reports boot errors, empty stops, overlapping and clipped text, and text smaller than 14 px. The report is written to `out/smoke/my-review/report.json`, and `--shots` adds one PNG per stop plus a contact sheet. The exit code is 1 when a stop is empty or errors occur.

## 7. Export to MP4

```bash
npm run export -- my-review --dry-run   # path and duration only
npm run export -- my-review             # out/export/my-review.mp4
```

Export builds the deck in export mode and runs `hyperframes lint`, then renders 1920×1080 at 30 fps. See [export.md](export.md) for the presentation path, the `exportHold` timing and stop capture.

## 8. Run the checks

```bash
npm run ci
```

`npm test` runs every engine, move and deck test, and `npm run check` enforces dependency rules, tests next to modules, state schemas and move static rules. Both must pass before a merge.

## Next

- [writing-a-deck.md](writing-a-deck.md): every `deck.yaml` field and beat type
- [concepts.md](concepts.md): concept packs and how to add one
- [moves.md](moves.md): the move contract and how to write and test a move
- [media.md](media.md): frame sequences, in-beat video, masks
- [export.md](export.md): MP4 export, capture, smoke
- [architecture.md](architecture.md): layers, timeline model, development rules, state log
