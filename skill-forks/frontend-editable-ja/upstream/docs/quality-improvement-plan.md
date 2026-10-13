# Editable Deck Quality Improvement Plan

## 1. Current State Assessment

### What exists today
| Layer | Script | What it checks | What it misses |
|-------|--------|---------------|----------------|
| Static contract | `validate-editable-decks.py` | Slide IDs, object IDs, scoped queries, required JS tokens, mobile markers, title editability | No CSS/layout correctness, no runtime behavior |
| Static contract | `validate-template-ports.py` | Slot coverage (title/body/image), edit modes, external deps, sanitizer | No visual regression, no interaction correctness |
| Fixture regression | `test-editable-contract-fixtures.py` | 10 tiny broken decks that must fail the validators above | Only proves validators catch their own stated rules |
| Browser smoke | `smoke-editable-decks.py` | Edit mode toggle, Pages copy/new-page, slot edit + undo/redo, Unlock layout, overflow at 3 viewports | 4 sampled decks only; no drag/resize, no RTE, no visual regression, no editable-element bounds check |
| Doc lint | `validate-skill-workflow.py` | SKILL.md and other docs contain required strings | Pure string match, no semantic check |

### Key gaps
1. **Editable content visibility** — current smoke checks "no scrolling / no horizontal overflow," but not whether `[data-edit-slot]` or `[data-slide-object]` is clipped by `overflow:hidden`
2. **Component stability** — no drag, resize, snap, multi-select, or undo/redo stress testing
3. **Feature usability** — RTE toolbar, keyboard shortcuts, image/video workflow, export fidelity untested
4. **Design preservation** — no automated check that ported templates keep upstream CSS, layout, and visual identity after slot editing or Unlock layout

### Recent browser finding to address first

A Playwright-style bounding-box probe across all 46 generated presets in a Chrome headless `1280x720` window (observed slide height `slideH≈633px`) currently finds **15 presets with editable slots outside their owning slide rectangle**. These decks can still pass the current smoke suite because `overflow:hidden` masks the issue instead of producing scrollbars.

Current batch status: the C0 detection path now exists via `SMOKE_PRESET_MATRIX=bounds`, but the full C0 repair target is not complete. The remaining failures are content-density/layout-fitting work for the next G2 milestone, not a repaired state.

Failing presets observed:

| Preset | Failure shape |
|--------|---------------|
| `biennale-yellow.html` | Dense editorial content clipped in the observed headless slide height |
| `bold-signal.html` | Large type/card content clipped in the observed headless slide height |
| `creative-mode.html` | Multiple title/body slots clipped near the bottom |
| `editorial-forest.html` | Large titles and body slots clipped |
| `editorial-tri-tone.html` | Editorial body/date slots clipped |
| `emerald-editorial.html` | Dense agenda/list slots clipped |
| `grove.html` | Page-number slots slightly clipped |
| `neo-grid-yellow.html` | Dense body slots clipped |
| `peoples-platform.html` | Oversized title/label slots clipped |
| `pin-and-paper.html` | Dense body/title slots clipped |
| `pink-script.html` | Large editorial titles/body slots clipped |
| `playful.html` | Dense playful content clipped in the observed headless slide height |
| `retro-zine.html` | One quote/tagline slot slightly clipped |
| `soft-editorial.html` | Several body/stat/title slots clipped |
| `stencil-tablet.html` | Dense body/stat slots clipped |

This is the first optimization target because it is already reproduced in real browser layout, directly affects delivered deck quality, and is not caught by the existing validators.

---

## 2. Three-Axis Improvement Strategy

### Axis A: Editable Component Stability (组件稳定性)

**Problem:** Static validators check DOM structure but not whether the runtime actually works — drag jumps, resize breaks text reflow, undo corrupts state, snap misaligns, or copy/new-page produces duplicate IDs at runtime.

**New tests needed:**

| Test ID | Name | Type | What it proves |
|---------|------|------|---------------|
| A1 | Drag position roundtrip | Browser smoke | Drag an object, release, verify `left`/`top` changed and are valid `%` of slide |
| A2 | Resize text reflow | Browser smoke | Resize a text object narrower, verify no horizontal overflow and text wrapped |
| A3 | Multi-select group drag | Browser smoke | Ctrl+click 2 objects, drag, verify both moved by same delta |
| A4 | Snap alignment | Browser smoke | Drag object near slide center, verify it snaps within 8px threshold |
| A5 | Undo/redo chain depth | Browser smoke | Perform 5+ operations (move, resize, delete, copy slide, new page), undo all, redo all, verify final state matches |
| A6 | Copy slide ID uniqueness under load | Browser smoke | Copy same slide 3 times, verify all slide IDs and object IDs remain unique |
| A7 | New page style inheritance | Browser smoke | New page inherits slide background class, has editable title object, uses preset CSS variables |
| A8 | Save/load roundtrip fidelity | Browser smoke | Edit content, save, clear DOM, load from localStorage, verify content and structure match |
| A9 | Export standalone completeness | Browser smoke | Export, parse exported HTML, verify no `deck-edit-mode` class, no `is-selected`, no file inputs, no filmstrip clones, has DOCTYPE, all slides present |
| A10 | Unlock layout undo completeness | Browser smoke | Unlock layout, verify new objects created, undo, verify objects removed and `data-componentized` cleared |

**Implementation approach:**
- Extend `smoke-editable-decks.py` with new JS test scripts (same `chrome_eval` harness)
- Run A1-A4 against at least: 1 legacy preset, 2 ported presets (dark + light), the reference
- Run A5-A10 against the reference deck (it's the canonical runtime)
- Add `SMOKE_PRESET_MATRIX=stability` mode for A1-A4 across all 46 presets (fast, parallelizable)

### Axis B: Editable Feature Usability (功能可用性)

**Problem:** The RTE toolbar, keyboard shortcuts, image/video insertion, and export are documented but never exercised by automated tests. A broken `font-size` drawer or a missing `Ctrl+Z` binding silently degrades the user experience.

**New tests needed:**

| Test ID | Name | Type | What it proves |
|---------|------|------|---------------|
| B1 | RTE bold/italic toggle | Browser smoke | Select text, apply bold, verify `<b>` or `font-weight: 700`; toggle off |
| B2 | RTE font family change | Browser smoke | Change font family via drawer, verify `font-family` inline style applied |
| B3 | RTE font size change | Browser smoke | Change size via Px drawer, verify `font-size` inline style; test custom px input |
| B4 | Keyboard E toggle isolation | Browser smoke | Press E in edit mode while contenteditable focused → should NOT exit edit mode |
| B5 | Ctrl+S persistence trigger | Browser smoke | Press Ctrl+S, verify `localStorage.setItem` was called with correct key |
| B6 | Delete object with Backspace | Browser smoke | Select object, press Backspace, verify removed; undo restores |
| B7 | Add element: text | Browser smoke | Click Add element → Text, verify new `data-slide-object` on current slide |
| B8 | Add element: image placeholder | Browser smoke | Click Add element → Image, verify image object created with placeholder |
| B9 | Export strips transient state | Browser smoke | Enter edit mode, select objects, export; verify exported HTML has no `deck-edit-mode`, no `is-selected`, no `.slide-object-media-file` inputs |
| B10 | Sidebar delete slide safety | Browser smoke | Try to delete the last slide, verify "Keep at least one slide" guard |

**Implementation approach:**
- New JS test scripts in `smoke-editable-decks.py`
- B1-B3 test against ported presets that have `data-edit-slot` (text content exists)
- B4-B10 test against the reference deck
- Add `SMOKE_PRESET_MATRIX=rte` mode for B1-B3 across all ported presets

### Axis C: Template Design Preservation (模版设计保留)

**Problem:** The slot editing model promises "edit content, keep layout," but there's no automated proof that:
1. Original CSS classes, grid structure, and decorative DOM survive the build pipeline
2. Slot editing doesn't break the template's visual identity
3. Unlock layout preserves backgrounds and locked decorative elements

**New tests needed:**

| Test ID | Name | Type | What it proves |
|---------|------|------|---------------|
| C0 | Editable bounds visibility | Browser smoke | Every visible `[data-edit-slot]` and `[data-slide-object]` stays inside its owning slide in a headless `1280x720` window with observed `slideH≈633px`; optional mobile checks when mobile adaptation is enabled |
| C1 | Upstream CSS class preservation | Static | Ported deck retains all original slide-level CSS classes from upstream template |
| C2 | Decorative DOM preservation | Static | Ported deck retains texture layers, gridlines, scanlines, SVG marks, glitch overlays |
| C3 | Font family match | Static | Ported deck's `font-family` declarations match `STYLE_PRESETS.md` spec for that preset |
| C4 | Color token match | Static | Ported deck's `:root` CSS variables include expected palette tokens from STYLE_PRESETS |
| C5 | Slot editing layout stability | Browser smoke | Edit a slot's text, verify slide's bounding box and key decorative elements didn't shift |
| C6 | Unlock layout locked elements | Browser smoke | Unlock layout, verify backgrounds, gridlines, SVG marks, scanlines remain in DOM and are NOT in `.slide-edit-layer` |
| C7 | Chrome token presence | Static | Every preset defines `--deck-chrome-*` variables (not hardcoded hex in chrome CSS) |
| C8 | No generic AI slop | Static | No preset uses banned fonts (Inter, Roboto, Arial as display), banned colors (#6366f1), or banned patterns |
| C9 | Visual regression baseline | Screenshot diff | Capture cover/mid/late screenshots, compare against stored baselines with tolerance |
| C10 | Slot content roundtrip | Browser smoke | Edit slot text, save, reload, verify text persisted AND layout unchanged |

**Implementation approach:**
- C0, C5-C6, C10: Extend `smoke-editable-decks.py`
- C1-C4, C7-C8: New static validator `validate-design-preservation.py`
- C9: New script `capture-visual-baselines.py` + `diff-visual-baselines.py` using Chrome screenshot + pixelmatch/ssim

---

## 3. Implementation Roadmap

### Phase 0: Editable Bounds Visibility + Repairs (C0) — 1-2 days
**Why first:** This is the only currently reproduced browser-layout failure. It is masked by `overflow:hidden`, so it must be tested with actual element bounding boxes, not scroll metrics.

**Deliverables:**
- Extend `scripts/smoke-editable-decks.py` with `EDITABLE_BOUNDS_SCRIPT`
- Check visible `[data-edit-slot]` and `[data-slide-object]` against the owning slide's `getBoundingClientRect()`
- Add a matrix mode such as `SMOKE_PRESET_MATRIX=bounds` or include the check in `SMOKE_PRESET_MATRIX=ported|all`
- Produce a failing list for the 15 currently clipped presets
- Repair the ported template CSS / builder patches so all 46 presets pass in a headless `1280x720` window with observed `slideH≈633px`
- Optional after repair: check mobile portrait/landscape only for decks with `data-mobile-adaptation="enabled"`

**Acceptance criteria:**
- Existing static validators still pass
- Existing sample smoke still passes
- Full bounds check reports `0` clipped editable elements across all 46 presets in a headless `1280x720` window with observed `slideH≈633px`

### Phase 1: Static Design Preservation (C1-C4, C7) — 2 days
**Why second:** Fast to implement and useful for CI, but less urgent than the reproduced clipping bug. Keep it factual and avoid over-broad aesthetic gates.

**Deliverables:**
- New script: `scripts/validate-design-preservation.py`
- Reads each ported preset's upstream template from `beautiful-html-templates/templates/{slug}/template.html`
- Compares CSS classes on `<section class="slide">` nodes
- Checks for decorative DOM markers (scanlines, gridlines, texture, glitch, SVG)
- Validates required `--deck-chrome-*` presence
- Optionally reports `:root` CSS variables against STYLE_PRESETS.md palette tokens as warnings when the preset uses explicit palette tokens
- Treats "generic AI slop" checks as warnings, not hard failures, because ported templates may legitimately contain upstream fallback fonts or RTE font options
- Integrates into the existing test runner

### Phase 2: Component Stability Smoke (A1-A10) — 3 days
**Why second:** Core runtime correctness. Without stable drag/resize/undo, nothing else matters.

**Deliverables:**
- Extended `smoke-editable-decks.py` with 10 new JS test scripts
- New `SMOKE_PRESET_MATRIX=stability` mode
- Tests A1-A4 run against sampled presets; A5-A10 against reference

### Phase 3: Feature Usability Smoke (B1-B10) — 2 days
**Why third:** Depends on stable components (Phase 2) to be meaningful.

**Deliverables:**
- Extended `smoke-editable-decks.py` with 10 new JS test scripts
- New `SMOKE_PRESET_MATRIX=rte` mode
- Tests B1-B3 against ported presets; B4-B10 against reference

### Phase 4: Visual Regression Baseline (C9) — 3 days
**Why last:** Highest setup cost, highest value for long-term maintenance.

**Deliverables:**
- New script: `scripts/capture-visual-baselines.py` — captures cover/mid/late screenshots at 1280x720 for all 46 presets
- New script: `scripts/diff-visual-baselines.py` — compares current screenshots against stored baselines
- Baseline storage: start by reusing or comparing against `docs/preset-previews/`; only move to a new git-tracked `docs/visual-baselines/` after the diff process is stable
- Tolerance: configurable pixel diff threshold (default 5%)
- Triggered manually or in CI after `build-*.py` runs

### Phase 5: Fixture Expansion — 1 day
- Add new regression fixtures to `test-editable-contract-fixtures.py` for each new static check
- Add fixture for: missing `--deck-chrome-*`, banned font as display, missing decorative DOM, broken slot roundtrip

---

## 4. Test Execution Matrix

| Script | What | Scope | Runtime | Frequency |
|--------|------|-------|---------|-----------|
| `validate-editable-decks.py` | Runtime contract | 46 presets + reference | ~0.2s | Every commit |
| `validate-template-ports.py` | Port contract | 34 ported + 12 legacy | ~0.3s | Every commit |
| `validate-design-preservation.py` (NEW) | Design fidelity | 34 ported | ~0.5s | Every commit |
| `test-editable-contract-fixtures.py` | Regression fixtures | 15+ tiny HTML files | ~2s | Every commit |
| `validate-skill-workflow.py` | Doc lint | 4 markdown files | ~0.1s | Every commit |
| `smoke-editable-decks.py` (sample) | Edit + pages + overflow | 4 decks | ~30s | Pre-merge |
| `smoke-editable-decks.py` (bounds) | Editable element visibility | 46 decks | ~60-90s | Pre-merge until fixed, then nightly or pre-merge |
| `smoke-editable-decks.py` (stability) | Drag/resize/snap/undo | 4+ decks | ~60s | Pre-merge |
| `smoke-editable-decks.py` (rte) | RTE + keyboard + add | 4+ decks | ~60s | Pre-merge |
| `smoke-editable-decks.py` (all) | Full matrix | 46 decks | ~5min | Nightly |
| `diff-visual-baselines.py` (NEW) | Visual regression | 46 presets × 3 shots | ~3min | Pre-merge |

---

## 5. Priority-Ordered Task List

### P0 — Must have (blocks confidence in any change)
1. C0: Editable bounds visibility across all 46 presets, plus repairs for the 15 currently clipped presets
2. A5: Undo/redo chain depth (the single most fragile runtime path)
3. Export integrity: merge A9 and B9 into one export cleanup/completeness test
4. `validate-design-preservation.py`: C1 (class preservation), C3 (font match where objectively specified), C4 (color token warning or hard check only for explicit tokens), C7 (chrome token presence)

### P1 — Should have (catches real user-facing bugs)
5. A1: Drag position roundtrip
6. A2: Resize text reflow
7. A6: Copy slide ID uniqueness under load
8. B1-B3: RTE toolbar basic operations
9. C2: Decorative DOM preservation
10. C5: Slot editing layout stability

### P2 — Nice to have (defense in depth)
11. A3, A4: Multi-select and snap
12. A7, A8: New page style + save/load roundtrip
13. B4-B8, B10: Keyboard, delete, add element, sidebar safety
14. C6, C8, C10: Unlock layout, slop warning, slot roundtrip
15. C9: Visual regression baseline

---

## 6. Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Chrome headless flakiness | Smoke tests randomly fail | Use `--virtual-time-budget`, generous timeouts, retry on timeout |
| Visual regression noise | False positives from font loading, anti-aliasing | Use SSIM with 5% tolerance; capture after `--virtual-time-budget=8000` |
| Upstream template drift | beautiful-html-templates changes break C1-C2 | Pin to local checkout; diff against last-known-good |
| Test maintenance burden | 46 presets × many tests = slow feedback | Tiered execution: static always, smoke pre-merge, full nightly |
| Fixture explosion | Too many tiny HTML files to maintain | Generate fixtures from a template function (already done in `test-editable-contract-fixtures.py`) |
| `overflow:hidden` masks clipped content | Tests pass while users see cropped editable text | Add C0 bounds checks that inspect actual element rectangles inside each slide |
| Over-strict aesthetic lint | Legitimate upstream template fonts/colors fail CI | Make "AI slop" and palette checks warnings unless STYLE_PRESETS gives explicit hard tokens |

---

## 7. Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Static contract checks per preset | ~15 | ~25 (add design preservation) |
| Browser interaction tests per run | 4 decks × 4 tests | 4 decks × 14 tests (sample), 46 × 4 (matrix) |
| Visual regression coverage | 0 presets | 46 presets × 3 screenshots |
| Editable bounds failures in headless 1280x720 (`slideH≈633px`) | 15 presets observed | 0 presets |
| Time for full CI gate | ~5s (static only) | ~90s (static + sampled smoke) |
| Time for nightly full suite | N/A | ~8min (all smoke + visual diff) |

---

## 8. Codex Goal Execution Notes

Use Codex goal mode only when the user explicitly asks to execute this plan as a goal. Do not create a goal merely because this document exists.

### Recommended goal objective

> Improve `frontend-slides-editable` quality gates by using the existing editable bounds validation to repair the 15 currently clipped preset decks, then expanding runtime/design smoke tests according to `docs/quality-improvement-plan.md`.

### Goal execution rules

- Create a goal only after explicit user instruction.
- Set a token budget only if the user explicitly provides one.
- Treat the next G2 content-density repair as the first goal milestone when resuming this plan. Do not start broad visual-regression work before the 15 known bounds failures are repaired.
- Mark the goal `complete` only after the requested milestone has concrete verification output, such as passing validator/smoke commands and a summary of changed files.
- Mark the goal `blocked` only if the same blocking condition recurs for at least three consecutive goal turns and meaningful progress cannot continue without user input or an external state change.
- Do not use `blocked` to mean "hard," "slow," or "needs more time."
- If the goal is budgeted, report the final token usage when marking it complete.

### Goal-sized execution slices

| Slice | Objective | Done when |
|-------|-----------|-----------|
| G1 | Add C0 bounds smoke and reproduce failures | Done in the current batch: `SMOKE_PRESET_MATRIX=bounds` can report clipped editable elements and the 15-preset failure list is reproducible |
| G2 | Repair clipped presets | All 46 presets pass C0 in a headless `1280x720` window with observed `slideH≈633px`; existing validators still pass |
| G3 | Add export/undo runtime hardening | A5 and merged Export Integrity tests pass in sample smoke |
| G4 | Add RTE/add/delete usability smoke | B1-B8/B10 pass on the selected sample set |
| G5 | Add static design preservation checks | New static validator passes and warnings are documented |
| G6 | Add visual regression workflow | Screenshot capture/diff flow works without excessive false positives |
