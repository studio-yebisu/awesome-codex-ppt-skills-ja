# Execution Backends

Use this file after routing and before authoring. Prefer reliable built-in capabilities, but keep project-local fallbacks available.

## 1. native_pptx

Primary backend:

- Codex system `$slides` / `presentations` skill.
- Use its `@oai/artifact-tool` PowerPoint APIs when available for editable objects, rendering, layout inspection, overflow checks, and font checks.

Project fallback:

- Project-local `pptxgenjs`.
- Project-local `python-pptx` for simple fallback authoring or template-oriented operations.

Execution rules:

- Keep titles, body text, labels, and key numbers as native editable text.
- Keep simple charts as native PowerPoint charts when practical.
- Prefer editable shapes and connectors for simple process diagrams.
- Insert illustrations as separate image assets.
- Do not rasterize the whole deck.
- Keep an authoring source file, for example `authoring/build_deck.mjs`.

## 2. template_pptx

Primary backend:

- `$slides` template-following workflow when exact clone/edit is possible.
- Template profiler plus Python/OOXML helpers for local fallback.

Execution rules:

- Read original deck size first.
- Prefer original layouts, masters, placeholders, theme, and fonts.
- Do not casually add text boxes that break the template.
- Generate `template_profile.md` and `template_profile.json`.
- Never overwrite the original template.
- Output a new PPTX.

## 3. html_slides

Primary backend:

- Local HTML/CSS/JS.
- Playwright + Chromium.

Execution rules:

- Use a fixed 1920x1080 canvas or match the source deck size.
- Every page is an independent `section`.
- Every page has `data-slide-id`, `data-layout`, and `data-density`.
- Export `index.html`, PDF, and per-slide PNG.
- Use DOM bounding boxes to check overflow and overlap.
- HTML-to-PPTX is auxiliary and must be labeled as best-effort, not fully editable.

## 4. image_first

Primary backend:

- Codex image2 through built-in `$imagegen`.
- `$slides`, `pptxgenjs`, or `python-pptx` assembles the PPTX container.
- `scripts/capture_imagegen_asset.py` captures any persisted `$imagegen` file or attachment into the run directory.

Execution rules:

- Use Codex image2 through built-in `$imagegen`; do not require API keys.
- Before each generation call, write a capture marker; after the call, run `scripts/capture_imagegen_asset.py`. Read `imagegen-asset-handoff.md`.
- Generate one sample first in normal production mode.
- In test mode, if the sample passes style and QA, auto-confirm and continue.
- Save the prompt and generation note for every image.
- Save the captured image path in `asset_plan.json`; UI-only inline images are previews, not usable delivery assets.
- Mark full image pages as not fine-grained editable.
- Do not silently replace `image_first` with `native_pptx`.

## 5. Image Assets In Any Route

Use Codex image2 through built-in `$imagegen` for required generated PPT illustrations:

- Cover hero visuals.
- Concept illustrations.
- Scenario illustrations.
- Abstract metaphors.
- Light visual explainers.
- Visually consistent illustration series.

Project-local raster renderers may create temporary drafts, debug visuals, or emergency placeholders, but they do not satisfy the final image-generation requirement. If image2 output is not discoverable as a local file, record `IMAGEGEN_OUTPUT_NOT_DISCOVERABLE`, ask for the fixed handoff folder workflow, and do not mark the generated visual as passed.

Do not use generated images to replace:

- Editable body text.
- Titles.
- Key numbers.
- Native charts.
- Simple process boxes.
- User-provided screenshots or assets that must be preserved.

## 6. Imagegen Asset Handoff

After calling built-in `$imagegen`, the generated image must be handed to the execution backend as a real file.

Use `scripts/capture_imagegen_asset.py` to:

- scan explicit paths, Codex attachments, Downloads, Temp, `incoming_assets/`, and run directories
- filter by capture marker time, dimensions, and optional aspect ratio
- copy the selected image to `<run_dir>/images/<slide_id>.png`
- update `asset_plan.json`

If no file path, attachment path, or bytes are exposed, record `IMAGEGEN_OUTPUT_NOT_DISCOVERABLE` and do not mark image generation as passed.
