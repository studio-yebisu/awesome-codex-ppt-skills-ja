# Single-Slide Edit

Use when the user specifies one or more target slides.

## Lock Rules

- Only modify target slides.
- Lock every non-target slide.
- Do not change non-target slide content.
- Do not change non-target slide layout.
- Do not change slide order.
- Do not change non-target fonts, colors, pictures, charts, or notes.

## Target Slide Must Inherit

- Existing colors
- Fonts
- Title hierarchy
- Density
- Layout rhythm
- Header/footer
- Numbering system
- Icon style
- Image style

## Versions

Generate one best version by default. Generate 2-3 variants only when the user asks for multiple versions.

## Required Outputs

- `single_slide_edit_plan.md`
- `locked_slides.json`
- `preview_before/slide_NN.png`
- `preview_after/slide_NN.png`
- `change_log.md`

QA must compare non-target slides and report if anything changed.
