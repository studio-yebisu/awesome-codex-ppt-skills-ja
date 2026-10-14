# Visual Asset Decision

Use this before writing `asset_plan.json`. It decides whether each slide needs image generation, illustration, icon set, chart, screenshot, or background visual.

## Image Generation Is Required For Qualified Delivery

For production-quality PPT delivery, at least one AI-generated raster visual is mandatory, and it must be generated with Codex image2 through built-in `$imagegen`.

- A deck with no image2-generated asset is not qualified.
- Native charts, native shapes, screenshots, icons, local semantic renderers, user-provided images, and template decorations do not satisfy this minimum.
- The generated image must be captured into the project workspace and referenced by a real `output_path`.
- The generated image may enhance a cover, concept page, scenario page, product/system capability page, or closing vision page.
- Generated images must not carry core titles, body text, key numbers, or chart conclusions; those remain editable whenever the route supports editability.

## Coverage

`asset_plan.json` must cover every slide. No slide may be omitted.

Every slide must include:

- `visual_need`: `required`, `optional`, or `not_needed`
- `asset_type`
- `generation_required`
- `reason`
- `must_not_skip`
- `status`

## Visual Need Values

- `required`: the slide needs a strong visual asset to explain, sell, clarify, or carry emotion.
- `optional`: a visual asset may improve the slide, but native text/shape/chart layout can still work.
- `not_needed`: a visual asset would add noise; the slide is clearer without generated imagery.

## Pages That Usually Need Strong Visual Assets

Strongly consider `required` for:

- Cover page
- Abstract concept explanation
- Scenario simulation
- Product or system capability showcase
- Complex process page
- Case story page
- Strong emotional hook page
- Closing vision page

## Pages That May Not Need Image Generation

These may be `optional` or `not_needed`:

- Simple table of contents
- Pure data table
- Page where a native chart is clearer
- Concise conclusion page
- Regulation, clause, checklist, or policy information page

Even if an individual page is clearer without generated imagery, the whole deck still needs at least one generated visual asset unless the run is explicitly marked as an unqualified no-image draft.

## If visual_need = required

- Set `generation_required=true`, unless the slide explicitly needs a screenshot, native chart, or user-provided material instead.
- Set `generation_backend=codex_builtin_imagegen` after successful capture. The intended image model is Codex image2 through built-in `$imagegen`.
- Provide a concrete `reason`.
- Set `must_not_skip=true`.
- If image2 generation or capture fails, write the failure into `qa_report.md` and `delivery_manifest.json`; do not replace it with a local renderer and call it qualified final generation.

Acceptable alternatives to generation:

- `asset_type=screenshot` with user-provided or captured screenshot
- `asset_type=data_chart` with native editable chart
- `asset_type=process_diagram` using editable native shapes
- user-provided image or brand asset

When using an alternative, record why generation is not required.

## No-Laziness Rules

- Do not skip later required visuals because the deck already has a cover plus two key images.
- Do not use low-quality icons, pure color blocks, or blank placeholders to fake required illustrations.
- Do not use local semantic renderers or locally drawn placeholder art to fake image2-generated illustrations.
- Do not hide image generation failures.
- Do not bake core text, key data, or chart conclusions into images.
- Keep titles, body text, key data, and chart labels editable whenever the route supports editability.

## QA Implication

QA must check:

- Every slide appears in `asset_plan.json`.
- Every slide has `visual_need`.
- Required visual assets are generated, planned for generation, or explicitly replaced by screenshot/chart/user material.
- No required visual is skipped due to the minimum image count already being met.
