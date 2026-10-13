# Export, capture and smoke

How a scroll deck becomes an MP4, how stop frames are captured for review, and how to smoke-test a deck in a real browser.

Canonical contract: `plan/CONTRACTS.md` C14. Tools: `tools/export.mjs`, `tools/capture.mjs`, `tools/smoke.mjs`.

## Requirements

| Tool | Needed for | Check |
|---|---|---|
| Node.js 22 or newer | everything | `node --version` |
| HyperFrames CLI (run through `npx`, not a package dependency) | `export`, `capture`, smoke `--driver chrome` | `npx hyperframes --version` |
| ffmpeg on `PATH` | frame extraction, capture contact sheet, audio or concat post-processing | `ffmpeg -version` |

## Why the MP4 matches the live deck

The live deck is already a single paused GSAP master timeline whose only input is time, which is the contract HyperFrames renders against. Export replaces the scroll input with a fixed **presentation path**: a wrapper timeline that travels between stops and holds on each one, the way a presenter would.

### The presentation path

`exportPath(map, opts, holds)` in `engine/export.js` is pure and runs in node:

```text
lead (t = 0, still)
→ for each stop: travel to the stop → hold
→ travel from the last stop to the end of the map
→ tail (still)
```

- **travel** seconds = `clamp(Δu × secondsPerUnit, travelMin, travelMax)`, eased with `power1.inOut`.
- **hold** seconds = the beat's `exportHold`, or `stopHold` when it has none.
- `stopAt[name]` = the video second at the middle of each hold. `capture` uses it.

Defaults (`EXPORT_DEFAULTS` in `engine/constants.js`):

| Key | Default | Meaning |
|---|---|---|
| `width` × `height` | 1920 × 1080 | Fixed export viewport |
| `fps` | 30 | Render frame rate (`--fps` overrides) |
| `secondsPerUnit` | 0.5 | Seconds of travel per timeline unit |
| `stopHold` | 1.6 | Seconds held on each stop |
| `travelMin` / `travelMax` | 0.6 / 5 | Clamp on one travel |
| `lead` / `tail` | 0.4 / 1.2 | Still time at start and end |
| `ease` | `power1.inOut` | Travel easing |

Override per deck and per beat in `deck.yaml`:

```yaml
export:
  secondsPerUnit: 0.6        # slower travel for this deck

beats:
  - id: b-sales
    # …
    exportHold: 2.2          # hold this stop longer in the MP4
```

### What the export build contains

- The wrapper is `gsap.timeline({ paused: true })` with `master.tweenFromTo(from, to, { duration, ease })` added at each travel segment's start second. Holds are gaps in the wrapper, not empty tweens.
- In export mode, `boot` fixes the viewport to 1920 × 1080, disables reduced motion, skips the scroll driver and presenter, waits for fonts, images and every frame sequence's `preloadAll()`, then registers `window.__timelines['scrolline'] = wrapper` and fires `scrolline:export-ready`.
- In-scene clips (`mode: play | loop`) get `data-start` and `data-duration` on the export path; HyperFrames plays and decodes them. See [media.md](media.md).
- HyperFrames reads the composition length before any script runs, so `tools/export.mjs` computes it in node (`plan` + `exportPath`) and writes it statically:

```html
<div id="scrolline-root" data-composition-id="scrolline" data-width="1920" data-height="1080" data-duration="…">
```

## Required line in `main.js`

Export only works when the deck's entry passes the build mode to `boot`. Without it, the export build boots in live mode and never registers a timeline.

```js
boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,   // 'live' in dev, 'export' in the export build
});
```

`decks/canvas-pitch/main.js` is a complete example. `vite.config.js` defines `import.meta.env.SCROLLINE_MODE` from the `SCROLLINE_MODE` environment variable (default `live`). Check this line in decks scaffolded with `npm run deck -- new`.

## Render an MP4

```bash
npm run export -- <deckId> [--fps 30] [--out out/export/<deckId>.mp4] [--build-only] [--report file] [--dry-run]
```

Steps:

1. Parse `decks/<deckId>/deck.yaml`, run `plan` and `exportPath` in node.
2. `vite build` with `SCROLLINE_MODE=export SCROLLINE_DECK=<deckId>` into `out/export/<deckId>/`.
3. Copy `decks/<deckId>/assets/` into the build.
4. Stamp the `#scrolline-root` wrapper with `data-duration`.
5. `npx hyperframes lint out/export/<deckId>`.
6. `npx hyperframes render out/export/<deckId> --fps <fps> --output <out>`.

| Flag | Effect |
|---|---|
| `--fps <n>` | Render frame rate, positive integer. Default 30 |
| `--out <file>` | Output MP4. Default `out/export/<deckId>.mp4` |
| `--build-only` | Stop after lint. Useful to inspect the composition |
| `--report <file>` | Also write `{ deck, fps, out, buildDir, map, path }` JSON |
| `--dry-run` | Print the map and export path as JSON. Builds nothing |

Any failure prints `export: <message>` and exits with code 2.

Check the length before a long render:

```bash
npm run -s export -- rail-ai-decade --dry-run | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).path.duration))'
```

### Audio and joining

The tool renders picture only. Add narration or music, or join several decks, as an ffmpeg post-process on the MP4. Use `--dry-run` output (`path.stopAt`) to align narration to stops.

## Capture stop frames

```bash
npm run capture -- <deckId> [--stops] [--between] [--at s1,s2]
```

- Runs `export.mjs --build-only`, then `npx hyperframes snapshot` on the export build. Output goes to `out/capture/<deckId>/`.
- With no stop selection (or with `--stops`), every stop is captured at its `stopAt` second: `stop-01-<stop>.png`, …
- `--at s1,s2` captures only the named stops (names as in the map, e.g. `b-sales` or `b-sales/share`). Unknown names fail.
- `--between` adds one frame halfway between each pair of consecutive stops: `between-NN-<a>-to-<b>.png`. Use it to judge transitions.
- Writes `manifest.json` (`{ deck, shots: [{ file, t, stop, kind }] }`) and a contact sheet `sheet.png` (ffmpeg).
- Failure prints `capture: <message>` and exits with code 2.

## Browser smoke

Smoke boots a deck in a real browser, visits every stop through `window.__deck.seek(t)` and measures what is on screen. It needs a running dev server:

```bash
npm run dev -- --port 5190                                  # terminal 1
node tools/smoke.mjs <deckId> --driver chrome [--shots]     # terminal 2
```

```text
node tools/smoke.mjs <deckId> [--port 5190] [--host localhost] [--shots] [--driver aside|chrome]
```

| Driver | What it uses | Notes |
|---|---|---|
| `chrome` | HyperFrames' chrome-headless-shell over the Chrome DevTools Protocol, 1920 × 1080 | Run `npx hyperframes browser ensure` if the browser is missing. Required for `--shots` (and chosen automatically by it) |
| `aside` | The Aside desktop browser CLI, current window size | Default when `--shots` is absent. Only for machines with Aside installed |

Per stop it records boot errors and page errors, visible beats, empty screens, overlapping text boxes, clipped text and the smallest font size. Output:

- `out/smoke/<deckId>/report.json` with a `summary` (`stops`, `errors`, `empty`, `overlaps`, `clipped`, `tinyText` for text under 14 px, measured as if the window were 1920 px wide)
- with `--shots`: `stop-01.png` … and `sheet.png`
- terminal: one line per stop, then the totals

Exit codes: 0 clean, 1 if there are errors or empty stops, 2 if the run itself failed.

## Reviewing a deck

Automated numbers do not judge whether a deck reads well. The review loop used for the sample decks:

1. `npm run ci` green.
2. `node tools/smoke.mjs <deckId> --driver chrome --shots` with no errors, no empty stops.
3. `npm run capture -- <deckId> --between` and read `sheet.png`: one focal point per frame, a three-level hierarchy, no meta captions.
4. Scroll and press the presenter keys in a real browser to judge pacing.
5. `npm run export -- <deckId>` and watch the MP4 end to end.

## See also

- [getting-started.md](getting-started.md) — first deck to first MP4
- [writing-a-deck.md](writing-a-deck.md) — `exportHold`, `export:` and stops
- [media.md](media.md) — clips and sequences in export
- [architecture.md](architecture.md) — why the timeline is deterministic

## Transition check

`tools/smoke.mjs` looks at stops. A deck can pass it and still break between stops, for example when a link leaves the full-frame source on screen and the next beat pops in at the end. `tools/transitions.mjs` seeks through every `link` and `step` span and writes one strip per transition:

```bash
npm run transitions -- rail-ai-decade            # dev server on :5190
npm run transitions -- rail-ai-decade --url http://localhost:5195/decks/rail-ai-decade/index.html --samples 6
```

Output goes to `out/transitions/<deck>/`: `NN-<beat>-<move>.jpg` strips and `transitions.json`. Read the strips for every deck you change. The rules they enforce are in CONTRACTS C7 v2.3: links call `takeoff()`, mask zooms drive size and position together, and full-screen grounds sit behind content in depth.
