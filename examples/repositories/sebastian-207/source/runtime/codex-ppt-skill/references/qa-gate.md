# QA Gate

Run QA before every delivery. QA failure must not be silently shipped.

For visual assets, read `visual-asset-decision.md` and `semantic-visual-brief.md`, then verify `asset_plan.json` against both no-laziness and slide-specific semantic binding rules.

## Required Checks

- Files exist
- Page count correct
- Slide size correct
- Placeholder remnants absent
- `lorem`, `xxxx`, `TODO` absent
- Text does not overflow
- Images are present
- Image aspect ratios are not obviously wrong
- Fonts are available or fallback is recorded
- Shapes/DOM elements do not incoherently overlap
- Speaker notes did not leak into slide body
- Required images in `asset_plan.json` were generated or failure recorded
- At least one AI-generated raster asset is completed and captured into the workspace for qualified delivery
- No-image PPT is marked FAIL or `UNQUALIFIED_NO_IMAGE_DRAFT`, not PASS
- Built-in `$imagegen` assets have real `output_path` files after `scripts/capture_imagegen_asset.py`; UI-only inline images are not accepted as generated assets
- Every slide appears in `asset_plan.json`
- Every required visual asset is completed, planned for generation in planning-only mode, or explicitly replaced by screenshot/native chart/user material
- Every generated visual asset has `image_slot`, `aspect_ratio`, `integration_treatment`, and `semantic_binding` tied to that slide's title and core message
- Generated images are not generic deck backgrounds unless the slide explicitly needs an atmospheric background and preserves a clear text safe area
- Internal workflow labels such as `PAGE-SPECIFIC VISUAL REQUIRED`, `VISUAL MODEL`, or `HTML DECK` are absent from delivered slide bodies
- No slide was skipped because the minimum image count had already been met
- Native charts, shapes, screenshots, icons, user-provided images, and template decorations do not satisfy the mandatory generated-image gate
- PPTX/PDF/PNG export succeeded or failure recorded
- Single-slide edit did not change locked slides
- Reference PPT mode states reference scope

## Outputs

- `qa_report.md`
- QA status inside `delivery_manifest.json`

## Failure Handling

If QA fails:

- List failed checks.
- Identify affected slide IDs.
- Record whether auto-repair was attempted.
- If not repaired, mark delivery as blocked or partial.
