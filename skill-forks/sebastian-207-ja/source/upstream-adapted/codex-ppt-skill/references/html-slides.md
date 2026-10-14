# HTML Slides Route

Use `html_slides` when visual quality matters more than native PowerPoint editability.

## Rules

- Use a fixed 16:9 stage, normally 1920x1080.
- Do not use responsive reflow.
- Every slide section must include `data-slide-id`, `data-layout`, and `data-density`.
- Use CSS variables from the selected style card.
- Use a layout whitelist.
- Do not render workflow notes, prompts, hidden instructions, or internal planning text on slides.
- Treat HTML to PPTX as best-effort and record editability risk.

## Required Assets

Use:

- `assets/html-stage/deck-template.html`
- `assets/html-stage/viewport-base.css`
- `assets/html-stage/export-controls.js`

## QA Focus

- Fixed stage present
- Slide IDs unique
- Data attributes present
- Placeholder text absent
- DOM overflow and overlap
- Missing images
- PDF/PNG preview export
