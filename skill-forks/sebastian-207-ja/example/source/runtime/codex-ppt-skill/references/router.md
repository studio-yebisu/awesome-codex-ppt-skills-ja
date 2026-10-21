# Router

Choose a route before generation or editing. Always write `route_decision.md`.

## Task Types

- `create_from_anything`: one word, sentence, article, markdown, document, script, rough ideas
- `reference_deck`: create a new deck from a reference PPT
- `edit_deck`: modify an existing PPT
- `single_slide_edit`: modify specified slide(s) only
- `template_pptx`: use an existing PPTX template, master, layout, or placeholder system
- `native_pptx`: create/edit an editable PPTX with native objects
- `html_slides`: create a fixed-stage HTML deck and export PDF/PNG
- `image_first`: create full-slide image pages and assemble to PPTX

## Route Rules

- Choose `template_pptx` when a template/reference deck must preserve layouts, placeholders, masters, theme, or editability.
- Choose `native_pptx` when the user needs editable PPTX and no template is provided.
- Choose `html_slides` when visual expression is the priority and HTML/PDF/PNG are acceptable.
- Choose `image_first` only when the user explicitly accepts full-slide image pages and editability limits.
- Route `edit_deck` to `single_slide_edit` if the user names specific slide numbers.

## route_decision.md Must Include

- Selected route
- Why this route was chosen
- Why other routes were not chosen
- Editability expectation: `editable`, `balanced_editable`, `partly_editable`, or `non_editable_image_pages`
- Whether image generation is needed
- Whether user confirmation is needed
- Required artifacts
- Export targets
- QA profile

## V2 Backlog

Keep these outside V1 core unless explicitly requested:

- `mcp_api`
- External generation APIs
- OCR-to-editable reconstruction
- TTS and video export
- Complex animation systems
- Full multi-agent platform runtime
