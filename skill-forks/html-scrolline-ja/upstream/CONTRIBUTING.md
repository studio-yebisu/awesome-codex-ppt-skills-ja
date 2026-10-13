# Contributing

Thanks for helping. This repository follows a few fixed rules so that `main` stays green and the six decks keep moving differently. Read [docs/architecture.md](docs/architecture.md) first. The interface contract is `plan/CONTRACTS.md` (Korean), and where it and the code disagree, the contract wins.

## Setup

```bash
git clone https://github.com/gongnyang/awesome-html-scrolline-deck.git
cd awesome-html-scrolline-deck
git checkout v2
npm install
npm run ci
```

Node.js 22 or newer. ffmpeg and the HyperFrames CLI (via `npx`) are needed only for media and export work.

## What to change where

| Change | Where | Guide |
|---|---|---|
| A new deck | `decks/<id>/` | [writing-a-deck.md](docs/writing-a-deck.md) |
| A new move | `moves/<family>/<id>.js` + `<id>.test.js` | [moves.md](docs/moves.md) |
| A new concept | `concepts/<id>/` | [concepts.md](docs/concepts.md) |
| Engine behaviour | `engine/` | needs a contract change first (below) |
| Tools and checks | `tools/` | keep `--help` output and docs in sync |

A deck should never need an engine or move edit. If a scene is unique to one deck, write it as a sequence beat in `decks/<id>/sequences/`.

## Rules

1. **Small steps.** One pull request adds one deck, one move, one concept or one engine module. Every commit leaves a deck that runs.
2. **Self-testing code.** Every `engine/**/*.js` and `moves/**/*.js` file has a sibling `<name>.test.js`. `npm run check` fails when one is missing. Move tests use `checkMove` from `moves/_shared/contract-check.js`, plus tests for the move's own behaviour.
3. **Continuous integration.** `npm run ci` (`npm test && npm run check`) must pass locally and in GitHub Actions before merge.
4. **Two hats.** A commit either adds behaviour or restructures it, never both. End the message with a trailer:
   - `Hat: feature`: adds or changes at least one test file.
   - `Hat: refactor`: changes no existing test file. Add new regression tests next to the module as `<name>.<topic>.test.js` instead.

   Check a range with `node tools/check.mjs --hat <base>..<head>`.
5. **Module boundaries.** Imports go `decks → concepts → moves → engine`, only through public entry points (`engine/index.js`, `moves/index.js`, `concepts/<id>/index.js`). No cycles, no imports between sibling decks, concepts or move families (except `moves/_shared/`). Only `engine/` imports `gsap`, and moves receive it as `ctx.gsap`.

## Move rules

`tools/check-moves.mjs` blocks `.from(`, `var(`, clock and random calls, 3D properties outside `camera`, and direct `gsap` imports. The `checkMove` contract test covers seek determinism, rewind and timeline length.

- Declare the start state with `ctx.initial`. No `tl.from()`, and every `fromTo` has `immediateRender: false`.
- No `var(` inside tween values. Read numbers from `ctx.tokens` and colours from `ctx.colors`.
- No `Math.random`, `Date.now` or `performance.now`. Use `ctx.rng()`.
- Rotation, `z` and perspective belong to `family: camera` only.
- `timing(params, data)` is pure, and the built timeline is no longer than `timing().duration`.

## Content rules for decks

- Real figures need a `source` that points to `sources[]`, with a URL and an access date. Fictional decks set `sample: true`.
- No placeholder text. `validateDeck` rejects `TODO`, `TBD`, `lorem`, `???`, `{{ }}`, empty strings and similar.
- Stock media needs a licence that allows redistribution, and a line in `decks/<id>/assets/CREDITS.md`.
- For reference sites, borrow ideas only. Do not copy code, images, fonts or brand assets.

## Contract changes

Changes to `engine/index.js`, `engine/types.js`, `engine/constants.js` or the shape of `deck.yaml`, beats, moves or concepts start as an issue that describes the change against `plan/CONTRACTS.md`. Once agreed, the contract, types and constants change together in one `Hat: refactor` commit.

## Pull requests

- Describe what changed and how you verified it (test names, `npm run deck -- plan` output, smoke report).
- For visual changes, attach stop captures (`npm run capture -- <deckId> --stops`) or a smoke contact sheet.
- Keep generated output (`out/`, `node_modules/`, `media-src/`) out of commits.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
