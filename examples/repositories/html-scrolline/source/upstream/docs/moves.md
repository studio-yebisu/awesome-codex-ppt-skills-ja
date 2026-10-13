# Moves

A move is one piece of motion: how a beat appears, leaves, changes after a stop, hands itself to the next beat, moves the camera, or breathes while it holds. Beats only render DOM; every movement on screen is a move.

Related: [getting-started](getting-started.md) · [writing-a-deck](writing-a-deck.md) · [concepts](concepts.md) · [media](media.md) · [export](export.md) · [architecture](architecture.md)

## Browse the registry

```bash
npm run deck -- moves                       # id, family, role for every registered move
npm run deck -- moves --family rail
npm run deck -- moves --role link
```

The built-in moves `engine:fade-in`, `engine:fade-out`, `engine:crossfade` and `engine:none` are always registered. Under reduced motion the engine also uses them as same-length replacements for moves declared `reduce: 'fade'`.

## Roles

| role | when it runs | notes |
|---|---|---|
| `enter` | Beat appears; ends on the beat's stop | Can declare internal stops |
| `exit` | Beat leaves after its hold | Ignored when the beat has a `link` |
| `link` | Turns beat A into beat B | Uses handoff; `accepts` is checked against B's type |
| `step` | After a stop, the beat changes (chart morph, annotation) | Each step ends on its own stop |
| `camera` | Moves `.sl-camera` from the beat start | Only `family: camera` |
| `ambient` | Whole beat life | `duration: 'fill'` allowed |

## Families

Family is about what the move moves. The folder is `moves/<family>/`.

| family | moves… | examples |
|---|---|---|
| `reveal` | Focus and light: blur, brightness | `focus-pull` `blur-drop` `lit-from-dark` |
| `type` | Text parts: words, lines, characters | `line-mask-rise` `type-on` `slot-pick` `phrase-fold` |
| `morph` | One shape becoming the next beat's shape (links) | `glyph-to-bar` `iris-to-dot` `headline-to-caption` |
| `camera` | Camera and world scale; the only family allowed 3D properties | `arc-flight` `zoom-dive` `rail-settle` |
| `rail` | The horizontal time rail | `rail-advance` `era-shift` `counter-handoff` |
| `data` | Charts and numbers | `count-roll` `mark-morph` `dot-multiply` |
| `media` | Video, masks, frame sequences | `video-scrub` `mask-word-in` `word-door` |
| `assemble` | Lines and items that split or gather | `divider-split` `pin-drop` |
| `emphasis` | Aiming, annotation, receding | `recede` `port-aim` `depth-ladder` |

## Contract

```js
// moves/<family>/<id>.js
export default {
  id: 'match-cut',            // ^[a-z0-9][a-z0-9-]*$, globally unique, file name = id
  family: 'morph',            // = folder name
  role: 'link',               // enter | exit | link | step | camera | ambient
  accepts: ['photo', 'video'],// beat types, or ['*']; for links, the receiving beat's type
  sources: ['morph-match-cut'],// awesome-ai-motion technique slugs (1+)
  reduce: 'self',             // 'self' = handles ctx.reduce itself | 'fade' = engine swaps in a fade
  params: { duration: { type: 'number', default: 1.2, min: 0.2, max: 4, doc: 'Length (u)' } },
  timing(params, data) { return { duration: params.duration, stops: [] }; },
  build(tl, ctx, params) { /* add tweens to tl from 0 */ },
  handoff(params, { from, to }) { return { from: { part: 'frame' }, to: { part: 'media' } }; }, // optional, link only
};
```

- `params`: every key has a `default` and a `doc` (no `required`). Types: `number`, `integer`, `string`, `boolean`, `enum` (`values`), `ease`, `part`, `asset`, `array`, `object`, `any`.
- `timing` is pure: it sees only resolved params and beat data (`{ from, to }` for links). No viewport, no DOM, no reduce flag. It returns `{ duration, stops? }` where `stops[].at` is relative to the move start. Because timing is pure, stops are identical at every screen size and in the MP4 export.
- `build` receives a local timeline starting at 0. The engine adds it to the master timeline at the span start and checks `tl.duration() <= timing.duration + 0.001`.
- `handoff` (links only, pure) picks which part and index of A travels to which part and index of B. Without it, both sides use their primary part, index 0. Negative indices count from the end.

## MoveContext

| field | meaning |
|---|---|
| `gsap`, `plugins` | GSAP instance and registered plugins (do not import `gsap`) |
| `role` | This move's role |
| `beat` | Target `BeatInstance` (B for links): `id`, `type`, `data`, `root`, `parts`, `part(name)`, `anchor(part?, index?)`, `span`, `media` |
| `from` | Leaving beat (A for links) |
| `prev`, `next` | Neighbouring beats |
| `handoff` | Links: `{ from, to }`, each `{ beat, part, index, rect, point, node, style }` measured before any transform |
| `camera` | Camera role: target `{ x, y, s, rx, ry }` computed from `place.world` |
| `step` | Step role: `{ name, index }` |
| `stage`, `viewport` | Stage elements; `{ w, h, portrait, px, dpr }` |
| `reduce` | Reduced motion is on |
| `start`, `duration` | Absolute start (u) and length of this move |
| `skipParts`, `skipNodes` | Parts and elements an incoming link already delivered |
| `overlay` | Container for DOM this move adds; visible from span start to the end of the beat |
| `tokens`, `colors` | Concept numbers; computed colours (`bg`, `fg`, `fg-muted`, `accent`, `accent-2`, `rule`, `scrim`) |
| `ease(alias)` | Concept ease alias to GSAP ease string |
| `initial(targets, vars)` | Declare the start state |
| `rng()` | Seeded random in [0, 1), seed = deck, beat, role and move id |
| `textMask(text, opts)` | SVG data URL for a text mask in the concept's display font |

## Rules

`tools/check-moves.mjs` and the move tests enforce these.

- Declare the start state only with `ctx.initial(...)`. No `tl.from()`. `fromTo` needs `immediateRender: false`.
- No `var(` strings in tween values. Use `ctx.tokens` for numbers and `ctx.colors` (or `_shared/color.js`) for colours.
- No `Math.random`, `Date.now`, `performance.now`. Use `ctx.rng()`.
- Do not import `gsap` or GSAP plugins; use `ctx.gsap` and `ctx.plugins`.
- Add DOM only inside `ctx.overlay`.
- Do not touch `autoAlpha`, `visibility` or `display` of `ctx.beat.root`; the engine owns beat visibility. Move parts only.
- Leave `ctx.skipParts` and `ctx.skipNodes` alone (no `initial`, no tween bringing them in).
- 3D properties (`rotationX`, `rotationY`, `z`, `translateZ`, `perspective`, `transformPerspective`) only in `family: camera`, only on `ctx.stage.camera` or `[data-depth]` layers, tilt within 12°. No decorative 3D objects.
- `reduce: 'fade'` means the engine replaces the move with a fade of the same length. `reduce: 'self'` means the move checks `ctx.reduce` and drops blur and 3D itself. Camera moves and step moves that change values or shapes must be `reduce: 'self'`, so the final value still shows.
- Measure only through `anchor()` and `ctx.handoff` rects, never `getBoundingClientRect`.
- No branching on concept id. Concept texture comes from params, presets and tokens.

## Links and handoff

Before building, the engine measures every part once, without transforms. A link moves A's `handoff.from.node` (or an overlay copy) into `handoff.to.rect`. At the end of the link:

- B's target part is visible and A's carrier is hidden;
- both are visible together for at most 0.15 u;
- B's enter skips what the link delivered (`skipParts`, or `skipNodes` when the link picked an index).

`moves/_shared/link.js` implements this: `finishLink(tl, ctx, { at, cross })` does the crossfade and final `set`s, `ghost(ctx, node, rect)` clones a node into the overlay at a rect, and `carriedRect(node, gsap)` reports where a carrier ended up (used by tests).

## Shared helpers

`moves/_shared/` is the only folder every family may import. Helpers are pure or only add tweens to a given `tl`.

| file | main exports |
|---|---|
| `timeline.js` | `seg(d, a, b)`, `slots(n, {...})`, `px(ctx, n)`, `clamp`, `lerp` |
| `link.js` | `finishLink`, `ghost`, `carriedRect` |
| `stroke.js` | `svgLayer`, `path`, `line`, `polyline`, `drawOn`, `pointOnPolyline` (dash-offset drawing, no DrawSVG) |
| `count.js` | `formatNumber`, `countTo` |
| `reel.js` | `buildReel`, `reelFrom`, `rollReel` (rolling digits) |
| `mask.js` | `applyTextMask`, `clearMask` |
| `media.js` | `frameSeqOf`, `scrubTo` (frame sequence progress from a tween) |
| `color.js` | `colorOf(ctx, name)` |
| `words.js` | `wordsIn`, `ghostWords` |
| `scramble.js` | `scrambleTable`, `scrambleAt` |
| `grid.js` | `gridLayout`, `canvasLayer`, `drawDots` |
| `event-part.js`, `rail-focus.js` | Chronology part indexing and rail focus |
| `contract-check.js` | `checkMove(move, scenario, createHarness)` |

## Example: a new enter move

`moves/type/word-lift.js`:

```js
/** Words rise into place one after another. */
import { px } from '../_shared/timeline.js';

export default {
  id: 'word-lift',
  family: 'type',
  role: 'enter',
  accepts: ['text', 'quote'],
  sources: ['word-rise-fade'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.9, min: 0.3, max: 2, doc: 'Total length (u)' },
    stagger: { type: 'number', default: 0.06, min: 0, max: 0.2, doc: 'Delay between words (u)' },
    rise: { type: 'number', default: 24, min: 0, max: 80, doc: 'Start offset (design px)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const words = ctx.skipParts.includes('word')
      ? []
      : ctx.beat.part('word').filter((node) => !ctx.skipNodes.includes(node));
    const each = Math.max(0.1, params.duration - params.stagger * (words.length - 1));
    words.forEach((word, i) => {
      ctx.initial(word, { autoAlpha: 0, y: px(ctx, params.rise) });
      tl.to(word, { autoAlpha: 1, y: 0, duration: each, ease: ctx.ease('out') }, Math.min(i * params.stagger, params.duration - each));
    });
  },
};
```

`moves/type/word-lift.test.js`:

```js
import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './word-lift.js';

const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'One small step' } }],
  run: { role: 'enter', beat: 'b', params: { duration: 0.9, stagger: 0.06, rise: 24 } },
};

it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
```

`checkMove` passes `scenario.run.params` to `timing` as given, without filling schema defaults, so list every param that `timing` reads. Add move-specific assertions next to it (see `moves/reveal/focus-pull.test.js`). The harness runs on happy-dom, which has no layout; give fake rects with `rects: { 'b.word#1': { x, y, w, h } }` when the move depends on positions.

### What checkMove runs

1. `createRegistry([move])` accepts the definition.
2. `timing` is pure (two calls deep-equal) and `duration > 0` (except ambient).
3. The local timeline is no longer than `timing.duration`.
4. Seeking A → B → A gives identical snapshots.
5. Seeking to the end and back to 0 restores the `initial` state.
6. With reduce on: no `blur(` filter and no 3D transforms (camera excepted).
7. Links: at the end, B's target is visible, A's source hidden, and the carrier sits on `handoff.to.rect` within 1 px (`scenario.carry: null` skips the rect check for links that open rather than carry).

The contract (C17) adds one more item that `checkMove` does not run, so write it as its own test when it applies: elements in `skipNodes` keep their inline style through build (enter and step moves), and `handoff()` returns deep-equal results for the same input.

## Registering

1. Add the import to `moves/<family>/index.js`, keeping ids in alphabetical order, and add it to the exported array in the same order:

   ```js
   import wordLift from './word-lift.js';
   import wordSlam from './word-slam.js';
   export default [/* … */ wordLift, wordSlam];
   ```

2. `moves/index.js` builds the registry from all family arrays; the new move is then listed by `npm run deck -- moves`.
3. Add the id to `moves.allow` of every concept that may use it ([concepts](concepts.md)). A deck can use a move outside its concept only with `override: "<reason>"` on the MoveRef.
4. Run the gates:

   ```bash
   npx vitest run moves/type/word-lift.test.js
   npm run ci        # npm test && npm run check
   ```

   `npm run check` fails if a move file has no sibling `.test.js` (`check-tests`) or breaks a static rule (`check-moves`: 3D outside camera, `.from(`, `var(`, clock or random calls, direct `gsap` import, `family` not matching the folder).
