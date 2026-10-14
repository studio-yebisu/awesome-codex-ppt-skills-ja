# Usage & technical guide

[← Back to home](../README.en.md) · [中文指南](guide.md)

## Current workflow contract

- One main path: new source material must become an image deck before editable reconstruction. Do not replace the workflow with editable-first authoring.
- Content quality review: expand the outline into a slide-by-slide draft with claims, support, evidence, interpretation, and actual visible content. Fix content issues before style selection.
- Two approval gates: after content review, present the draft separately and wait only if approval or explicit authority to decide the content is missing. Record the agent's quality judgment separately from user authorization.
- Deterministic style exemptions: only an explicit locked reference, preview skip, or delegated choice can change the four-option flow.
- Page Spec bridge: preserve approved text, data, sources, stable IDs, and semantic intent while generating images so reconstruction does not repeat OCR or guess known content.
- Explicit fast-forwarding: only clear instructions such as “skip previews,” “choose for me,” or “decide missing details” waive the corresponding gate.
- Image reconstruction: preserve visible content and layout while separating semantic elements.
- A versioned JSON scene with stable IDs, geometry, stacking, groups and provenance.
- Native text, shapes, arrows, nested groups, tables and charts with embedded workbooks.
- Deterministic asset extraction from supplied bounding boxes and optional masks.
- An editability audit that checks exported objects, image geometry/crops, and nested group transforms against the scene.
- GPT Image 2.5 guidance for Flare exploration and Sunburst reference editing.
- Existing image-only export and raster text overlay commands remain available.

See the [official image guide](https://developers.openai.com/api/docs/guides/image-generation).
The host may not expose an image model selector. These recommendations are not a measured model benchmark.

## Editability contract

| Content | Export | Editing |
|---|---|---|
| Headings, body copy, labels | Native text boxes | Text, font, position, color |
| Geometry and diagrams | Native shapes, lines, groups | Geometry and style; ungroup to edit children |
| Tables | Native tables | Cells and formatting |
| Bar, column, line, pie, doughnut | Native charts with workbooks | Data and chart formatting |
| Photos and complex illustrations | Separate image objects | Move, crop, resize, replace |

Raster artwork does not become editable vector paths. Missing or occluded details cannot be recovered with guaranteed accuracy.
**The local scripts do not perform OCR, automatic segmentation or image understanding.** Those steps belong to the host agent and its available vision/image tools.

## Quick start

See the [CLI guide](cli.en.md) for the unified local entry point, runtime diagnosis and isolated interpreter selection. Existing scripts and workflow gates remain available.

### Recommended: let your agent install it

Send this to Codex, Claude Code, or OpenCode:

```text
Install SlideMuse from https://github.com/helloo1568/slidemuse .
Run the repository's install.py to register the skill, install isolated dependencies, and verify the setup. If multiple clients are detected, pass --client for the one you are using.
```

### Manual install

Requires Python 3.10+. You do not need to create a virtual environment or install dependencies globally:

```sh
git clone https://github.com/helloo1568/slidemuse.git slidemuse
python slidemuse/install.py
```

The installer detects Codex / Claude Code / OpenCode. It auto-selects only when exactly one client is detected; if multiple clients are present, it stops and asks you to pass `--client` to avoid installing into the wrong user-level skill directory. It then creates an isolated `.venv`, installs dependencies, and runs the strict Page Spec self-check:

```sh
python slidemuse/install.py --client codex
python slidemuse/install.py --client claude
python slidemuse/install.py --client opencode
```

It stages and validates the new version before replacing an existing installation, and restores the old version if final validation fails. If a skill with the previous name is present, the installer reports its location so you can remove it after confirming `$slidemuse` works.

Invoke it as `$slidemuse` after installation. Keep task materials and outputs in a separate working directory.

## Runtime environments

| Environment | Image backend | Notes |
|---|---|---|
| Codex (recommended) | Codex image generation; prefer GPT Image 2.5 when selectable | Flare for exploration, Sunburst for final and precision editing |
| Other agents | That agent's own native or connected image generation/editing capability | Keep the same state machine, prompts, and acceptance checks |
| Python only | No end-to-end image generation | Local scripts only assemble, overlay text, compile scenes, crop assets, and audit |

The skill does not install an image plugin for another agent, search for API keys, or silently switch to an external service. Stop and report the missing capability when the current agent cannot generate images.

## Example requests

```text
Use $slidemuse to turn this report into a 10-slide editable deck for a project pitch.
I have no style reference. Show the content outline and wait for approval, then show four slide-sorter directions. After selection, build the image deck and page-spec.json, then reconstruct the editable version.
```

```text
Use $slidemuse starting at Step 3 to reconstruct these existing slide images into editable PPTX.
Preserve wording, layout and page order. Separate every element I need to edit.
Remove duplicated content from the background and include the scene and assets.
```

## The one three-stage workflow

```text
Confirm source, style reference, audience/use case, page count, and delivery scope
  ↓
Step 1A Draft each slide → review/fix content → present draft → wait if approval or authority is missing
  ↓
Step 1B Four slide-sorter overviews → wait for selection
  ↓ explicit locked-reference/skip/delegation rules only
Step 2  page-spec.json → generate and validate every slide image → image-only PPTX
  ↓ only when editable reconstruction was explicitly requested
Step 3  Page Spec + slide images → scene.json → native editable PPTX → structural and visual review
```

Ordinary requests do not waive gates. Explicit authorization is interpreted narrowly.

### How detailed should the outline be?

State the audience's central question, the answer supported by the material, and how the slides build that answer. Content slides include a claim, distinct supporting points, traceable sources, interpretation, and necessary qualifications. Specify the actual visible copy and chart content; optional speaker notes cannot hide essential evidence. A title list or isolated numbers are insufficient. Covers, transitions, and chart-led slides follow their purpose without a fixed word count, text ratio, or bullet count.

Review goal coverage, narrative progression, reasoning depth, factual scope, visible-content completeness, and fit within the requested length. Record the reviewed version, reasons, issue pages, and repairs. Stay in S1 while blocking issues remain; narrow unsupported claims rather than inventing mechanisms. Page Spec validation and delivery scoring do not establish narrative depth. See the [content-depth reference](../references/content-outline.md) and [draft template](../references/deck-spec-template.md) (Chinese).

Honor clear authorization already given in context without requiring exact phrases. A standalone “continue” does not grant authority over every stage. Style overviews and final images must preserve approved explanations and qualifications. If content does not fit, use the change workflow rather than silently dropping it.

### Style and image production

Use the task's slide aspect ratio in all four overviews. Show every slide for decks of up to eight pages; otherwise select the same six to eight representative pages. A one-slide deck has one page per option; never invent extra pages.
Each overview is a landscape thumbnail grid, not a vertical strip of full pages. For three pages, use a 2-by-2 grid with one empty position. `style-options.json` lists only the four current candidates; retries replace their original option number. Run `validate_style_options.py` before selection, then visually inspect the actual thumbnail grid and content. See [overview validation](../references/style-options.md).
If text is still incorrect after two attempts, generate a text-free page retaining all subjects and graphics, then overlay accurate text. Subject removal belongs to Step 3.
Existing slide images or scanned PDF pages can enter Step 3 directly when reconstruction is the stated goal. Ordinary edits to an already-editable PPTX are outside this workflow.
Follow-up edits to this skill's existing Scene continue in S6. Save the baseline version and authorized differences, invalidate affected images, and use the [change and recovery rules](../references/workflow-updates.md) to avoid repeatedly asking about known differences from historical images.

## Commands and contract

- validate_page_spec.py: validate content approval, ordered pages, stable IDs, geometry hints, unresolved items, unique image paths, and approved image delivery/aspect ratios.
- build_editable_ppt.py: validate a scene and compile native objects.
- audit_editability.py: inspect PPTX and optionally compare it with a scene; --strict fails on warnings.
- extract_assets.py: crop known regions, apply supplied masks, record coordinates and hashes.
- build_image_ppt.py: assemble only the approved images listed in Page Spec, preserving its page order and aspect ratio; legacy directory sorting remains supported.
- overlay_text.py: existing deterministic raster text overlay.
- render_deck.py: render every PPTX slide, write a review sheet, and optionally compare with approved Page Spec images.
- audit_page_content.py: compare a hash-bound visual transcription with confirmed text and required visible values.
- plan_deck_update.py: snapshot approved inputs and plan which slides to reuse, review or regenerate after edits.
- evaluate_delivery.py: combine current PPTX content observations, rendered-slide review, and optional Scene editability checks into a hash-bound scorecard.

```sh
python scripts/build_image_ppt.py work/page-spec.json output/image-deck.pptx
python scripts/render_deck.py output/image-deck.pptx output/image-review --page-spec work/page-spec.json
python scripts/render_deck.py output/editable.pptx output/editable-review --page-spec work/page-spec.json
python scripts/audit_page_content.py work/page-spec.json work/observations-s02.json --init --slide s02
python scripts/plan_deck_update.py snapshot work/page-spec.json work/snapshots/baseline.json
```

Page Spec export runs strict image validation automatically. Extra drafts in the directory are ignored; duplicate paths, missing or unapproved images, and mismatched aspect ratios stop export without replacing an existing output. `--width` or `--height` adjusts physical size; if both are supplied, they must preserve the canvas ratio. For standalone merging without a Page Spec, the legacy command remains `python scripts/build_image_ppt.py work/slides output/image-deck.pptx`.
Raster text overlay now fails when a text box overflows; adjust its size or font before rerunning. The renderer uses PowerPoint on Windows when available, or LibreOffice plus Poppler (`soffice` and `pdftoppm`). Its output directory must be empty unless `--overwrite` is given. The comparison sheet shows source, rendered slide and pixel difference; the numeric difference is diagnostic and still needs visual review. Historical reference images marked `revision` are accepted for authorized editable changes.
After generating an observation template, fill `observed_text` with the text actually visible in the image and set `status` to `complete` only after a full transcription. Run `audit_page_content.py ... --require-complete --output work/content-audit.json`; a changed page image invalidates its old observation. The update planner only reports affected slides and does not change Page Spec approval. See [revision rules](../references/workflow-updates.md).
For regression or release checks, record observations and a visual review for every rendered slide, then run `evaluate_delivery.py` as described in the [delivery evaluation guide](../references/evaluation.md). An editable deliverable must include `--scene` to count editability in its scorecard.
Starting in 2.6.0, render reports and visual reviews also bind reference image hashes. Recreate and actually review legacy evidence. Charts and tables require separate per-element `data_reviews`; an overall visual pass cannot approve unchecked data. Appending or removing slides only regenerates affected pages; mark slides displaying total-page counts or depending on deck size with `depends_on_slide_count: true`.

[Page Spec](../references/page-spec.md) · [Scene format](../references/scene-format.md) · [Layer reconstruction](../references/reconstruction.md) · [Models](../references/models.md)

Scene coordinates are canvas pixels; fonts and strokes are points. Asset paths are relative to and confined to the scene directory.
Group children use full-slide coordinates. Array order determines stacking.
This version does not implement a generic SVG importer, merged table cells, automatic connector attachment, or inline rich text.

## Validation

```sh
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests/ -q
```

CI covers Windows/Linux and Python 3.10/3.12/3.13.
Audit checks declared objects, not source-image completeness or visual similarity.
Render and inspect every slide before delivery. Portfolio images retain the source page dimensions; automated tests do not require PowerPoint.

## Credits

See the [three-slide acceptance record](acceptance-2026-09-18.md) for real rendering, data edits, object movement, and known limitations.

Research includes [PPT Master by Hugo He](https://github.com/hugohe3/ppt-master),
[banana-slides](https://github.com/Anionex/banana-slides) and [PPTAgent](https://github.com/icip-cas/PPTAgent).
The scene compiler is independently implemented; their code and dependencies are not bundled.
See [research notes](../references/research.md) for specific references and tradeoffs.

Early workflow inspiration: Xiaoheihe author 玩家22186848 and Bilibili creator 一往无前河井.

Local scripts perform no network requests and need no API key. Host AI services may receive supplied content.
Exclude private source documents and credentials from shared outputs.

[MIT](../LICENSE) © 2026 风清云影（helloo1568）

## Chart reliability (2.8.0)

Review numeric labels and geometry separately. Stop repeating image repairs after two consecutive checks fail for the same geometric issue. The precise horizontal-bar region fallback respects host image-edit permissions; the geometry audit checks independently recorded bar/column endpoints without performing image recognition. See [chart reliability](../references/chart-reliability.md).

Full scorecards use visual review v1.2 with source/value, label/unit, scale/geometry or table alignment checks plus a per-page data-visual inventory. Recheck the new items when migrating historical v1.1 reviews. Point colors, negative inversion, label placement, plot layout and doughnut settings are now declared and audited in [Scene](../references/scene-format.md).

## Speaker notes and material-specific review (2.9.0)

When the content draft has presenter notes, preserve them in Page Spec/Scene `speaker_notes`. Both PPTX exports retain them; editable `--page-spec` verifies upstream order and declared notes. Delivery evaluation reads actual PPTX notes. Notes-only edits rebuild exports while reusing images. `export_speaker_notes.py` optionally writes a source-referenced Markdown companion; see [speaker notes](../references/speaker-notes.md).

Paper review covers formula variables, input/operation/output, experimental scope and source conflicts. Long-form review distinguishes targets, actions, support conditions and observed effects; see [material reading](../references/material-reading.md). Note fidelity does not prove semantic depth.

## Multi-material evaluation (2.10.0)

Freeze the source registry and rubric before execution. Preserve each complete delivery attempt and report first and final results separately. Missing, changed or unreviewed cases remain in the denominator; repairs require new attempts. `evaluate_benchmark.py review-contract` exports a content contract without generation prompts and verifies its binding to the source. Separate objective invocation transactions from author quality judgments before independent review; see [benchmark records](../references/benchmark.md).

Native chart auditing checks both display caches and embedded workbook cells so Edit Data cannot silently restore older values. Tool checks and software tests do not replace actual source, visual or reviewer-independence judgments.
