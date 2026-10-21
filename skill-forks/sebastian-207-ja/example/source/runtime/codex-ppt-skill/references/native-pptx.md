# Native PPTX Route

Use `native_pptx` when the user needs an editable PPTX and no template is provided.

## Rules

- Use native PPTX text for titles, body, labels, and key data.
- Use native shapes, lines, and tables where practical.
- Use charts/diagrams as editable objects when practical.
- Do not turn the whole deck into slide images.
- Every slide needs a slide type, layout family, and content budget.
- Generate `design_spec.md`, `spec_lock.json`, `slides_plan.json`, and `asset_plan.json`.

## QA Focus

- Text overflow
- Shape overlap
- Font fallback
- Placeholder remnants
- Missing images
- Export preview

## Image Use

Images are allowed for cover visuals, scene illustrations, conceptual backdrops, and supporting graphics. They must not carry core text, facts, charts, or conclusions that should remain editable.
