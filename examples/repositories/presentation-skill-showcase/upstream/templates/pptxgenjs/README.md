# templates/pptxgenjs

Template modules for the default pptxgenjs renderer
(`scripts/build_deck_pptxgenjs.js`). These modules are plain CommonJS, so
`require()` from the builder pulls them in without a bundler.

The renderer is the default path. `scripts/build_deck.py` remains the fallback
only for legacy or python-pptx-specific behavior that the fast editable path
does not cover.

Lab/report decks use `deck_style.header_variant` to vary the clean content
header without changing the evidence-first layout. Supported values are
`auto`, `left-accent`, `split-rule`, `title-rule`, `side-rail`,
`top-bottom-rule`, and `plain`; the `lab-report` preset defaults to `auto`.
Set `deck_style.style_seed` to a short stable deck-specific string when auto
header variation should be reproducible but not identical across similar lab
reports.
Workspace builds record the resulting per-slide `resolved_treatments` and
`resolved_treatment_summary` in `build/outline_resolved.json`, and readiness
Markdown summarizes the selected header-variant counts before render.
When a slide uses `treatment_key`, build-time style-reference resolution also
records `resolved_treatments.style_reference_layout` with the selected
reference ID, treatment key, source/resolved variant, content-recipe library
version, and content-recipe signature.
The same `header_mode: "lab-clean"` report chrome can be layered over other
presets when a deck needs a boardroom, editorial, research, or journal palette
but still wants restrained heading/accent-rule rhythm.
Deck-level structure is selected through one of eight composition grammars:
Answer Pyramid, Evidence Plate, Care Pathway, Editorial Spread, Thesis Stage,
Operating Grid, Public Docket, and Telemetry Canvas. Each grammar provides
v2 role contracts for title, section, evidence, comparison, chart, table,
decision, and references. Contracts contain normalized semantic slots and
render through reusable primitives, so native text, charts, and tables stay
editable. `role_layout_variant` may be `primary`, `alternate`, or `dense`.
Keep the grammar coherent; do not splice unrelated page systems together.
New workspaces use v2 automatically. A v1-only workspace remains on the legacy
role system until the explicit idempotent upgrader is run.
The lower-level `page_system` values remain available for bounded rendering:
`clinical-rail`, `board-ledger`, `editorial-field`, `command-canvas`,
`lab-plate`, and `investor-thesis`.
Each preset also owns a `structural_motif`. These thirteen motif contracts
change persistent page geometry inside a page system, so related families do
not differ only by palette. Keep the preset motif unless intentionally
recomposing the whole structural contract.
`image-sidebar` supports `analysis-rail`, `evidence-mosaic`, and
`editorial-atlas` through `image_sidebar_mode`. `comparison-2col` supports
`open-columns` and metric-led `scorecard` through `comparison_mode`.
Chart slides can use `deck_style.chart_treatment` or slide-level
`chart_treatment` to choose `standard`, `facts-below`, `facts-right`,
`minimal`, `hero-stat`, `threshold-band`, or `sparse-wide` chart compositions
while keeping chart JSON and captions editable.
Editable table slides can use `deck_style.table_treatment` or slide-level
`table_treatment` to choose `standard`, `compact-ledger`,
`readout-sidecar`, `decision-matrix`, or `journal-grid` table compositions.
`footer_mode: source-line` reserves a compact provenance line for `sources`,
`refs`/`references`, and the page number.
The builder validates enum-like `deck_style` and slide-level treatment values
before writing a `.pptx`, so quick-deck calls fail on misspellings instead of
silently falling back to the default renderer treatment.

## Modules

| File         | Responsibility                                                                 |
| ------------ | ------------------------------------------------------------------------------ |
| `presets.js` | Style presets (palette + font pair) keyed by the skill's canonical preset names. Exports `getPreset(name)` / `listPresets()`. |
| `slides.js`  | Slide-family renderers, v2 role-contract recipes, and shared chrome. |
| `role_layout_contracts.js` | Loads and validates the eight-grammar role-layout catalog and resolves bounded per-slide variants. |

## Slide family map

| Outline shape                  | Renderer          | Notes                                                     |
| ------------------------------ | ----------------- | --------------------------------------------------------- |
| `type: title`                  | `renderTitle`     | Full-bleed dark hero; optional `background_image`.        |
| `type: section`                | `renderSection`   | Dark divider slide with oversized title.                  |
| `content / standard`           | `renderStandard`  | Bullets + optional right-side highlights card.            |
| `content / cards-2`            | `renderCards`     | Two square-edged cards with flush top accent rail.        |
| `content / cards-3`            | `renderCards`     | Three equal-width cards.                                  |
| `content / split`              | `renderSplit`     | Bullets left, dark highlights panel right.                |
| `content / timeline`           | `renderTimeline`  | Milestone sequence with rail, staggered, bands, or chapter-spread treatment. |
| `content / stats`              | `renderStats`     | Oversized fact tiles (value + label + caption + source).  |
| `content / kpi-hero`           | `renderKpiHero`   | Single dark KPI emphasis slide.                           |
| `content / table`              | `renderTable`     | Native editable table.                                    |
| `content / lab-run-results`    | `renderLabRunResults` | Compact editable lab/result dashboard with highlighted tables. |
| `content / comparison-2col`    | `renderComparison2col` | Two-column contrast with optional verdict.          |
| `content / matrix`             | `renderMatrix`    | 2x2 quadrant grid.                                        |
| `content / flow`               | `renderFlow`      | Mermaid/diagram image as the body.                        |
| `content / chart`              | `renderChart`     | Native editable bar/line/pie chart from inline or staged chart JSON. |
| `content / scientific-figure`  | `renderScientificFigure` | Editable figure slide with `panel-grid`, `primary-rail`, `ledger-rail`, or `strip-readout` layouts. |
| `content / generated-image`    | `renderGeneratedImage` | Standalone generated visual with metadata.           |

Use the Python renderer only for legacy or python-pptx-specific chart behavior
outside the fast path's common bar/line/pie payloads.

## Style presets

The renderer exports 13 canonical presets: `arctic-minimal`,
`bold-startup-narrative`, `charcoal-safety`, `data-heavy-boardroom`,
`editorial-minimal`, `executive-clinical`, `forest-research`, `lab-report`,
`lavender-ops`, `midnight-neon`, `paper-journal`, `sunset-investor`, and
`warm-terracotta`. At most two presets share a composition grammar; the preset
controls its bounded palette, typography, density, and treatment interpretation.

For scientific work that should read like print rather than a colored template,
use `lab_monochrome_v1` with `lab-report` or `journal_monochrome_v1` with
`paper-journal`. Both keep the page white and reserve their secondary accent for
semantic emphasis, so structure still comes from the selected grammar.

Each returns `{ bg, bg_dark, surface, text, text_muted, accent_primary,
accent_secondary, line, font_heading, font_body }`. `surface` and `line` are
provided as convenience tokens that several slide families use but are not
part of the required preset shape.

## House rules (worth repeating)

1. pptxgenjs hex colors never carry `#`. Write `"1493A4"`, never `"#1493A4"`.
2. Never reuse an options object across `addShape` / `addText` calls.
   pptxgenjs mutates what you pass in. Use the factory helpers
   (`textOpts()`, `shapeOpts()`, `cardShadow()`) so every call gets a fresh
   object.
3. Every text box sets `margin: 0` so the baseline math matches the layout
   coordinates exactly.
4. Canvas is `10.0" x 5.625"` (16:9). Side margins 0.5". The dark title
   bar is at least 0.90" tall, but folded titles/subtitles are measured and
   the renderer returns `contentTop`; content must start from that value, not
   from a fixed y-coordinate.
5. Sandwich: dark title slide -> light content body -> dark closing /
   section. Don't bounce between light and dark mid-deck.
