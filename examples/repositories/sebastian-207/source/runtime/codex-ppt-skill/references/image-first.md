# Image-First Route

Use only when the user explicitly accepts full-slide image pages.

## Explain First

Tell the user:

- Visual consistency is strong.
- It works well for poster-like, launch-like, social, and visual decks.
- Text, charts, and shapes are usually not separately editable.

## Required Workflow

1. Confirm `image_first` route.
2. Generate `slides_plan.json`.
3. Generate `asset_plan.json`.
4. Generate one sample slide first.
5. Continue only after confirmation, unless Auto Mode explicitly allows proceeding.
6. Save page images as `images/slide_XX.png`.
7. Record `slide_jobs.json` and `run_state.json`.
8. Assemble to `pptx/final.pptx`.

## QA Focus

- Correct slide count
- 16:9 image dimensions
- Required assets generated or failure recorded
- Visual consistency
- No core text accidentally missing
- Editability limitation recorded in `delivery_manifest.json`
