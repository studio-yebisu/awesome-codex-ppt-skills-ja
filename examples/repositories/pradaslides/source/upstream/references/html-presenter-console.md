# HTML presenter console

## Purpose

Use the bundled console for either a live browser deck or the default PPTX render-parity preview. It makes the output behave like a presentation product while keeping the slide canvas separate from editing chrome.

The console is not a substitute for slide design. It wraps either authored HTML slides or final PPTX render images with navigation, thumbnails, presenter mode, notes, and honest export actions.

## Choose one preview mode

- `render-parity` is the default companion to a PPTX. The PPTX remains editable; the HTML displays final slide renders and must be rebuilt after any PPTX repair.
- `native-html` is for explicitly web-native, interactive, or HTML-editable slide content. It has a separate authoring source and requires cross-runtime comparison when PPTX is also delivered.

## Project files

Copy the runtime with:

```bash
python scripts/scaffold_presenter.py --output <project-dir>/presenter --deck-plan <project-dir>/deck-plan.json --design-system <project-dir>/design-system.json
```

The result contains:

```text
presenter/
  index.html
  presenter.css
  presenter.js
  deck.css
  deck.js
```

Open `index.html` directly or serve the directory with any static server. No package installation or remote CDN is required.

For a PPTX render-parity preview, first render the final PPTX, then run:

```bash
python scripts/build_pptx_preview.py --output <project-dir>/presenter --slides-dir <project-dir>/renders/slides --deck-plan <project-dir>/deck-plan.json --title "<deck title>" --force
```

This copies ordered slide images into `presenter/slides/`, creates final `deck.js`, and uses the same dependency-free console. The preview hides tone, density, and furniture controls because those properties belong to the PPTX source.

## Architecture

Keep four layers separate:

1. **deck data and art direction** in `deck.js` and `deck.css`: slide ID, role, topology, tone, title, body HTML, notes, furniture, safe control values, and deck-specific styling;
2. **slide canvas**: a fixed `1600×900` stage scaled as one unit;
3. **console shell**: thumbnails, toolbar, inspector, counter, and navigation;
4. **presentation mode**: chrome-free fullscreen stage with keyboard navigation.

The scaffold writes a neutral `.prada-composition` with copy and visual regions for every planned slide. The root's `topology-*` class gives that shell a distinct stage, split, spine, axis, matrix, stack, network, mosaic, field, or frame silhouette through `deck.css`. Replace the empty regions with audience-facing content and deck-specific art direction; do not remove the topology distinction merely to reuse one two-column component everywhere.

Keep the fixed slide canvas centered independently of CSS Grid's overflow alignment. `.stage-scaler` must be absolutely positioned at `left: 50%` and `top: 50%`; `scaleStage()` must apply `translate(-50%, -50%) scale(...)`. Scaling without the translate can push the canvas under the inspector on short or narrow windows even when the scale calculation itself uses the correct minimum ratio.

Never bake console UI into a PPTX or PDF export. UI chrome belongs to the authoring/presenter experience, not the visible slide.

## Slide data contract

Each slide in `window.PRADA_DECK.slides` uses:

```js
{
  id: "P03",
  role: "content",
  topology: "axis",
  layout: "ranked-evidence-axis",
  tone: "light",
  referenceIds: ["V03"], // only when an exhaustive reference benchmark is active
  title: "Two queues account for most measured delay",
  kicker: "CURRENT STATE",
  html: `<div class="prada-axis">...</div>`,
  notes: "Explain the measurement boundary and scenario status.",
  furniture: {
    kicker: true,
    pageNumber: true,
    progress: true,
    frameCorners: false,
    sectionRail: false,
    ghostMarker: "46"
  }
}
```

Use audience-facing HTML only. Keep production notes in `notes`.

For exhaustive reference fixtures, set `referenceId` for a one-to-one page or `referenceIds` when several references legitimately share one response. The runtime writes them to `data-reference-ids`; browser QA compares the rendered values with `reference-benchmark.json`. Do not use this field in ordinary user decks that have no reference-coverage contract.

## Safe controls

The inspector may adjust only declared display properties:

- transition: none, fade, or slide;
- page tone: light, dark, accent, or media-aware when a background asset supplies the field;
- density: air, standard, or compact within the layout's budget;
- furniture visibility: kicker, page number, progress, frame corners, section rail, ghost marker, metric strip, and page hint;
- global UI theme and panel visibility.

Controls may not rewrite claims, evidence, chart data, source status, media crops, or layout semantics. A topology change requires editing the authoring source and re-running QA.

Local changes are stored in the browser. Reset returns to `deck.js`. Export before distributing if inspector changes matter.

## Presentation behavior

Support:

- click thumbnails and previous/next controls;
- Arrow, PageUp/PageDown, Space, Home, and End keys;
- `F` or the Present button for chrome-free fullscreen;
- Escape to leave presentation mode;
- notes visibility in the console, never on the audience slide;
- scale-to-fit without slide reflow;
- visible focus states and accessible button labels;
- reduced-motion preference.

## Export behavior

Keep export claims conservative:

- **Print/PDF** uses the browser print route and hides console chrome.
- **HTML package** is the folder itself; all assets must use relative paths.
- **PPTX** is a separate production route. Do not claim that browser HTML is natively editable PowerPoint.
- **PNG** requires a verified renderer or screenshot tool; do not expose a non-functional button.

When native HTML and PPTX are both required, use the same `brief.json`, `source-ledger.json`, `deck-plan.json`, `design-system.json`, and `layout-manifest.json` to build both outputs. Compare their renders, but let each runtime use native primitives. For the default render-parity preview, the final PPTX render is already the visible slide source; verify ordering, image loading, notes, and console behavior instead of re-authoring the design.

## Visual system and furniture

Use the console to expose meaningful deck controls, not a playground of decorative switches. Furniture should improve wayfinding:

- kicker identifies a section or evidence class;
- page number and progress locate the audience;
- frame corners reinforce the stage boundary;
- section rail marks a chapter or decision context;
- ghost marker repeats a meaningful code, number, or initial;
- metric strip supports no more than four decision-critical values;
- page hint helps live navigation but is unnecessary in static PDF.

Limit decorative motifs to two per slide and keep their contrast below the claim and proof.

## QA

Run the dependency-free Chromium check when Node.js and Chrome/Edge are available:

```bash
node scripts/qa_html_presenter.mjs --entry <project-dir>/presenter/index.html --count <slide-count> --output <project-dir>/qa/html-presenter.json --render-dir <project-dir>/renders/slides --montage <project-dir>/renders/slide-montage.png --console-shot <project-dir>/renders/console/presenter-console.png
```

The script detects broken images, missing image alt text, geometric image distortion, video without controls/poster/label, forbidden autoplay, placeholders, fixed-stage mismatch, authored elements leaving the slide, clipped content, audience text crossing the default outer safe area, collisions between independent text blocks, excessive title lines, undersized body text, incorrect thumbnail count, missing console regions, a visible draft badge, and collapsed toggles. It also exercises ArrowRight, Home, End, deep-link route synchronization, thumbnail synchronization, notes visibility, panel visibility, theme switching, query-driven presentation mode, and print-media page count/geometry. Treat it as structural browser evidence, not a substitute for human inspection of hierarchy, crop intent, focal placement, contrast, semantics, and originality.

`HTML_TEXT_SAFE_AREA` is blocking. The default threshold is the larger of `48px` or `3%` of slide width horizontally, and the larger of `36px` or `4%` of slide height vertically. Only intentional furniture may opt out with `data-edge-safe="ignore"`.

`HTML_TEXT_COLLISION` is blocking. It compares visible audience text after fonts load and rejects intersections between independent blocks. Parent/child text structures are ignored. A deliberate typographic interaction may use `data-text-overlap="allow"`, but do not use the marker to hide accidental title/subtitle or card-label collisions.

`HTML_TEXT_OBSTRUCTION` is blocking. Figures are protected regions by default, and other independently positioned diagrams, charts, process rows, or card groups should declare `data-no-text-overlap`. The gate rejects sibling text entering those rendered bounds. A full-bleed, contrast-checked text-on-media composition must explicitly declare `data-text-overlap="allow"` on the shared composition container.

Every generated slide section carries `role="group"`, `aria-roledescription="slide"`, and an accessible label derived from its page number and title. Browser QA requires exactly one slide-title `h1`, the slide semantics, an `aria-live="polite"` presenter announcement region, and accessible names for every visible button, select, input, and summary control.

When `deck-plan.json` is available, `run_html_benchmark.py` also passes it to browser QA. Mark rendered media with `data-asset-id="A01"`; mark a video's separately planned poster/fallback with `data-poster-asset-id="A02"`. For background media, set `background.assetId` beside `background.src` in `deck.js`; the runtime writes the DOM marker. Add `background.alt` for a meaningful background or `background.decorative: true` when it is purely presentational. Browser QA loads CSS background URLs independently and rejects missing files or unlabeled non-native media containers. Every rendered slide must expose exactly the `asset_ids` declared for the same slide in the deck plan.

Before delivery:

1. validate the deck plan, design system, and layout manifest;
2. open the console at desktop and reduced viewport sizes;
3. inspect all thumbnails for sequence and tone rhythm;
4. inspect every slide at full stage size;
5. test keyboard, focus, Present, Escape, Reset, and Print/PDF;
6. verify local assets load under `file://` and static-server routes;
7. verify no slide content shifts when console panels open or close;
8. test reduced motion;
9. compare HTML and PPTX renders if both exist;
10. record limitations in `qa-report.json`.
