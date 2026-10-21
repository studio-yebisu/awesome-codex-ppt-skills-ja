# Template Profiler

Use for `template_pptx` and reference decks that should preserve layout/editability.

## Required Extraction

- Slide size and aspect ratio
- Slide count
- Layouts
- Placeholder types and counts
- Theme colors
- Fonts
- Masters/layout availability
- Images and media count
- Speaker notes availability when detectable

## Required Outputs

- `template_profile.md`
- `template_profile.json`

## Rules

- Prefer existing layout and placeholder objects.
- Do not casually overlay text boxes on a template.
- Support `[HINT: layout_name]` or `layout_id` in `slides_plan.json`.
- If a template has no useful placeholders, record that limitation and consider `native_pptx`.

Use `scripts/profile_template.py` when a PPTX is available.
