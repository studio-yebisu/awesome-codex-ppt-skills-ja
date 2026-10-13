# Media

How a deck shows video: scroll-scrubbed frame sequences, in-scene playing clips, and text or shape masks over either.

Canonical contract: `plan/CONTRACTS.md` C4 (`video` beat), C5 (move context) and C13 (media). Design reasons: `plan/ARCHITECTURE.md` §6.

> **Before you add video: get your own stock API key.** To search and download stock footage automatically, issue a free key from [Pexels](https://www.pexels.com/api/) (`PEXELS_API_KEY`) or [Pixabay](https://pixabay.com/api/docs/) (`PIXABAY_API_KEY`) and keep it in a root `.env` file or your shell environment. `.env` is git-ignored, and `npm run check` fails if a key lands in a tracked file. `npm run frames` and `npm run deck -- new` print this reminder while no key is set. Without a key you can still add footage you shot or downloaded yourself; record its source and license in `decks/<id>/assets/CREDITS.md`.

## Three ways to show video

| Need | Use | Beat field | Driven by |
|---|---|---|---|
| Video that moves only when the audience scrolls, and rewinds when they scroll back | Frame sequence on `<canvas>` | `mode: scrub` + `frames` | A move's tween (`video-scrub`, `frame-scrub`, `sticky-scrub-link`, …) |
| A short clip that keeps playing while its beat is on screen (loop backdrop, product demo) | `<video muted playsinline>` | `mode: play` or `mode: loop` | `boot`, on `scrolline:active` |
| Video seen through letters or a shape | Mask on the media element | `mask: { type: text \| shape }` | Text: a move. Shape: static `clip-path` |

## Why scroll video is an image sequence

Scrubbing a `<video>` by setting `currentTime` looks fine going forward and breaks in reverse. The engine therefore turns scrub video into numbered still frames and draws the right one onto a canvas.

| Option | Decision | Reason |
|---|---|---|
| Image sequence + canvas | Chosen | A frame is a file, so seeking is immediate and exact. Rewind is symmetric. Every browser draws the same frame. The HyperFrames render sees the same pixels, so MP4 export stays deterministic |
| `video.currentTime` | Rejected | Seeking is bound to the keyframe interval: latency on seek, stutter in reverse, differences between browsers. All-intra encoding (`-g 1`) helps but inflates file size |
| WebCodecs | Deferred | Needs a demuxer dependency and decoder queue management, and frame-exact seek still has to be written by hand. The only gain is bandwidth; revisit if performance measurements call for it |

## Cutting frames

```bash
npm run frames -- <input.mp4> <outDir> [--fps 24] [--tiers 1920,960] [--quality 78] [--from 0] [--to <sec>]
```

- Requires `ffmpeg` on `PATH`. If `ffmpeg -version` fails the tool exits with code 2; usage or extraction errors exit with 1.
- `--from` / `--to` trim the source in seconds. `--tiers` lists output widths; each tier gets its own folder.
- Output:

```text
<outDir>/frames.json
<outDir>/poster.webp
<outDir>/1920/f_0001.webp …
<outDir>/960/f_0001.webp …
```

A real manifest, `decks/data-ev-shift/assets/frames/open-highway/frames.json`:

```json
{
  "version": 1,
  "fps": 24,
  "count": 156,
  "width": 1920,
  "height": 1080,
  "pattern": "f_%04d.webp",
  "tiers": {
    "960": "960/",
    "1920": "1920/"
  },
  "poster": "poster.webp"
}
```

Frame path = manifest folder + `tiers[tier]` + `pattern` (1-based).

## How a sequence plays

`frameSequence(host, manifest, opts)` returns a `FrameSeq` with a `canvas`, `setProgress(p)`, `setFrame(i)`, `ready()`, `preloadAll()` and `destroy()`.

- **Tier**: `viewport.w × dpr ≥ 1400` picks the largest tier, otherwise 960 (or the smallest tier if 960 is missing).
- **Loading order**: poster first, then every 8th frame (coarse pass), then ±12 frames around the current position, then the rest.
- **Missing frames**: when the target frame has not loaded yet, the canvas shows the nearest earlier loaded frame. Rewinding never jumps forward.
- **Progress comes from the timeline only**: a scrub move calls `setProgress` inside a tween's `onUpdate`. Scroll, presenter keys and MP4 export all go through that same tween, so the same timeline time always shows the same frame.

```js
// inside a move's build(tl, ctx, params)
const seq = ctx.beat.media.seq;             // set by the video renderer for mode: scrub
const proxy = { p: 0 };
tl.to(proxy, { p: 1, duration: params.duration, ease: 'none', onUpdate: () => seq.setProgress(proxy.p) }, 0);
```

Library moves use the shared helper `scrubTo(tl, seq, { from, to, at, duration })` in `moves/_shared/media.js`. In a `link` move, the outgoing beat's sequence is `ctx.from.media.seq`. See [moves.md](moves.md).

## The `video` beat

Required fields: `src` (mp4), `poster`, `alt`, `mode`. Optional: `frames` (required for `scrub`), `caption`, `mask`, `source`, `credit`. Parts: `frame`, `media`, `caption`, `credit`. Field reference: [writing-a-deck.md](writing-a-deck.md).

### `mode: scrub`

```yaml
- id: b-open
  type: video
  src: assets/video/open-highway.mp4
  poster: assets/frames/open-highway/poster.webp
  frames: assets/frames/open-highway/frames.json
  alt: "Night highway interchange seen from above; the car lights fade to a single point"
  mode: scrub
  place: { slot: full }
  enter: { move: video-scrub, params: { duration: 2.4 } }
```

The renderer creates the canvas (part `media`) and hands the `FrameSeq` to the beat as `ctx.beat.media.seq`. Nothing moves until a move drives it.

### `mode: play` and `mode: loop`

```yaml
- id: b-street
  type: video
  src: assets/video/vietnam-street.mp4
  poster: assets/video/vietnam-street-poster.webp
  alt: "A wide street in Saigon, packed with motorbikes and cars"
  mode: loop
  place: { slot: full }
```

- Live: the element is `<video muted playsinline preload="metadata">`. `boot` calls `clip.activate()` (play) when the beat's span is entered and `clip.deactivate()` (pause, position kept) when it is left, from the same `scrolline:active` enter/leave events used for accessibility. Moves never start or stop clips.
- Export: `boot` calls `clip.bindExport({ start, duration })`, which writes `data-start` and `data-duration` (seconds on the export path). HyperFrames owns decoding and playback; no JavaScript seeks the clip. Do not add a `crossorigin` attribute.
- `play` plays once; `loop` repeats. Cut loops so the last frame runs into the first (the stock loops in this repo crossfade the last 0.5–0.6 s into the head with ffmpeg `xfade`).

## Masks

### Text mask

The video plays inside the strokes of a word, then usually opens to full frame.

```yaml
- id: b-title
  type: video
  tone: 0
  src: assets/video/v1-attention.mp4
  poster: assets/video/v1-attention.jpg
  alt: "Thin lines of light flowing slowly between words"
  mode: loop
  mask: { type: text, text: "10년" }
  caption: "생성형 AI, Transformer에서 GPT-6까지 · 업계 브리핑 2026.10"
  place: { slot: full }
  enter: { move: mask-word-in, params: { duration: 1.4, captionIn: true } }
```

(From `decks/rail-ai-decade/deck.yaml`.)

- The renderer does **not** apply the mask. It adds class `sl-mask` and `data-mask-text` to the media element, so the rendered state is the unmasked video.
- A move applies it: `ctx.textMask(text, { rect?, align? })` returns an SVG data URL drawn in the concept's display font, sized so the text spans 0.92 of the rect width. The move sets it with `ctx.initial(media, { maskImage, webkitMaskImage, maskRepeat: 'no-repeat', … })` and tweens `maskSize` / `maskPosition`.
- Moves that use it: `mask-word-in`, `text-mask-dive`, `word-door`, `into-word`, `glyph-to-bar`. Shared helper: `applyTextMask` / `clearMask` in `moves/_shared/mask.js`.
- The mask SVG is a transparent background with white glyphs; masks are read by alpha.

### Shape mask

```yaml
mask: { type: shape, shape: "inset(12% 20% 12% 20%)" }
```

`shape` is a CSS `clip-path` value. Because it is static, the renderer applies it directly. Moves that open a window (`window-open`, `window-takeover`) tween `clipPath` with GSAP; tween values never contain `var(`.

## Assets, credits, budget

- Asset paths in `deck.yaml` are relative to the deck folder (`assets/…`). Renderers resolve them through `rc.asset(path)`; the deck's `main.js` passes `assetBase: new URL('./', document.baseURI).href`.
- `credit` on a `video` beat renders a small credit line (part `credit`) for stock footage that needs one on screen.
- Every deck that ships third-party media keeps `decks/<id>/assets/CREDITS.md`: source URL, author, license, download date and the processing applied. Stock footage in this repo is under the Pexels License. Self-made clips are HyperFrames renders whose sources live in `media-hf/<deck>/<asset>/`.
- Unprocessed originals are kept out of git (`media-src/` is ignored). Only the processed loop or frames enter the repo.
- Keep sequences small: frames cost bandwidth on every view. Use the 960 tier, lower `--fps`, shorter ranges or a lower `--quality` before adding frames. The largest sequence in the sample decks is about 13 MB for both tiers.

## See also

- [writing-a-deck.md](writing-a-deck.md) — all beat fields
- [moves.md](moves.md) — writing a scrub or mask move
- [export.md](export.md) — how clips and sequences behave in MP4 export
- [architecture.md](architecture.md) — where media sits in the engine
