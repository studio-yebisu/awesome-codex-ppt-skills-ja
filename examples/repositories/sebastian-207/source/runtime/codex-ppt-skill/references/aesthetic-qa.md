# Aesthetic QA

Every generated deck must render to PNG, build a montage, and pass deterministic checks plus a visual critic pass.

Score dimensions, 10 points each: typography, visual hierarchy, grid and alignment, whitespace and density, color and contrast, layout suitability, image integration, chart and data design, cross-slide consistency and rhythm, originality / anti-AI-slop.

Release threshold: total score at least 85, typography at least 8, hierarchy at least 8, grid at least 8, cross-slide consistency at least 8, and no severe failure mode.

## Mandatory Image Generation Gate

A qualified PPT must include at least one AI-generated raster visual captured into the workspace. Aesthetic QA must fail decks that have no `codex_builtin_imagegen` asset with `generation_required=true`, `status=generated`, and an existing `output_path`.

Native charts, shapes, screenshots, user-provided images, and template artwork do not satisfy this mandatory image generation gate.

The generated image must also be semantically bound to the slide. `asset_plan.json` must record:

- `semantic_binding.bound_to_slide=true`
- `semantic_binding.slide_title`
- `semantic_binding.core_message`
- `semantic_binding.visual_brief`
- `semantic_binding.intended_composition`
- `prompt_path` containing a page-specific prompt derived from the slide title or core message

Generic seed images, deck-level gate images, and repeated generated images reused across unrelated slides fail QA. A generated image is not acceptable merely because it exists on disk.

## Unintentional Blank Space

Aesthetic QA must inspect rendered PNGs for page balance. Large blank regions are acceptable only when they create deliberate focus or rhythm. A content page fails or is penalized when the right side of the slide is mostly unused and no chart, insight block, image, diagram, or deliberate silence is planned there.
