# Asset Plan

Every new deck must create `asset_plan.json`. This is a no-laziness contract.

Before deciding per-slide assets, read `visual-asset-decision.md`. That file defines when a slide needs image generation, illustration, icon set, chart, screenshot, or background visual.

Before calling image generation or building visual slots, also read `semantic-visual-brief.md`. Required visual assets must have a slide-specific semantic binding, an image slot, an aspect ratio, an integration treatment, and a prompt file. Use `scripts/create_visual_briefs.py` to normalize these fields.

## Minimum Is Not Maximum

Every qualified new deck must plan and complete at least:

- 1 AI-generated raster visual captured into the workspace
- Cover hero visual or another clearly justified generated concept/scenario/product/vision visual
- 1-2 additional key illustrations, concept visuals, or scene visuals when the content needs them

This is only the minimum. If five slides truly need generated visuals, plan five. Do not stop at two.

No-image PPT is not qualified. If a user explicitly asks for a no-image draft, mark the run as `UNQUALIFIED_NO_IMAGE_DRAFT` in `qa_report.md` and `delivery_manifest.json`; do not call it final delivery.

## Per-Slide Decision

Every slide must decide:

- Does this page need a visual asset?
- What type?
- Is image generation required?
- Can native shapes, charts, icons, screenshots, or diagrams do the job?
- Why or why not?

## Required Fields

```json
{
  "slide_id": "slide_04",
  "visual_need": "required | optional | not_needed",
  "asset_type": "cover_hero | concept_illustration | scene_illustration | process_diagram | data_chart | icon_set | screenshot | background",
  "generation_required": true,
  "reason": "",
  "image_slot": "cover_hero | right_40 | left_40 | top_strip | chart_sidecar | image_grid | background_atmosphere",
  "aspect_ratio": "16:9 | 16:10 | 21:9 | 4:3 | 3:2",
  "integration_treatment": "full-bleed hero | 60/40 split | masked editorial crop | atmospheric background with overlay | image grid | tinted monochrome treatment",
  "must_not_skip": true,
  "fallback_allowed": false,
  "status": "planned | generated | failed | not_needed",
  "output_path": "",
  "generation_backend": "codex_builtin_imagegen",
  "prompt_path": "",
  "semantic_binding": {
    "bound_to_slide": true,
    "slide_title": "",
    "core_message": "",
    "visual_role": "",
    "layout_archetype": "",
    "intended_composition": "",
    "visual_brief": ""
  }
}
```

## Forbidden Shortcuts

- Do not skip a required image because earlier slides already met the minimum.
- Do not use blank placeholders, low-quality icons, or flat color blocks to fake required illustrations.
- Do not hide image generation failures.
- Do not bake core titles, body text, key data, or chart conclusions into generated images.

If `generation_required=true`, generate the asset or record the failure reason in `qa_report.md` and `delivery_manifest.json`.

At least one asset must satisfy all of these fields for a qualified deck:

```json
{
  "generation_required": true,
  "generation_backend": "codex_builtin_imagegen",
  "status": "generated",
  "output_path": "existing workspace image path"
}
```

`replaced_by_chart`, `replaced_by_screenshot`, `replaced_by_user_asset`, native shapes, and template artwork are useful but do not satisfy the mandatory image generation gate.

QA must confirm that required visual assets are not skipped merely because the deck already has a cover visual plus 1-2 key illustrations.

## Built-In Imagegen Capture Fields

When using built-in `$imagegen`, also record:

```json
{
  "generation_backend": "codex_builtin_imagegen",
  "capture_status": "captured | not_discoverable",
  "capture_source": "original file or attachment path if discovered",
  "captured_at": "ISO timestamp"
}
```

Use `scripts/capture_imagegen_asset.py` after each `$imagegen` call. If capture fails because the image exists only as a Codex UI inline asset, set:

```json
{
  "status": "failed",
  "failed_reason": "IMAGEGEN_OUTPUT_NOT_DISCOVERABLE"
}
```
