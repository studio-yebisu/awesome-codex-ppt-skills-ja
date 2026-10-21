# Edit Existing Deck

Use when the user uploads or points to an existing PPT and asks to modify, optimize, rewrite, beautify, compress, expand, or repair it.

## Rules

- Generate `change_plan.md` before editing.
- Preserve facts, data, core meaning, and logic by default.
- Improve expression only when it does not change meaning.
- If the user says "不改内容", only change visuals, layout, typography, color, alignment, and supporting assets.
- Preserve the original file by copying into the run directory; do not overwrite source files.
- Output before/after previews when possible.
- Output `change_log.md`.
- If the user specifies page numbers, route to `single_slide_edit`.

## change_plan.md Must Include

- Pages to modify
- Pages not to modify
- Whether content changes
- Whether visual changes
- Whether page count changes
- Whether template changes
- Whether new images are planned
- Whether original charts/data/images are preserved
- Risks
