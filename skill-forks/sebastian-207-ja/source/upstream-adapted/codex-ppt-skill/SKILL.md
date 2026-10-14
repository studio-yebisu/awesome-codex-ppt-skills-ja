---
name: codex-ppt-skill
description: General-purpose PowerPoint and slide creation skill for helping users create, reference, edit, optimize, QA, and export presentations with AI. Use when users ask to make PPT/PPTX/slides from any input, convert articles/documents/ideas/scripts into decks, reference an existing PPT for style or structure, modify an existing deck, edit a single slide, infer presentation style, plan visual assets or image generation, produce speaker notes, or export PPTX/PDF/PNG/HTML deliverables.
---

# Codex PPT Skill Phase 3 Aesthetic Design Engine

This skill helps other people use AI to make deliverable presentations. Do not treat it as a personal one-off PPT helper. Optimize for ordinary users, workers, students, teachers, creators, enterprise teams, and clients who need clear, good-looking, checkable, modifiable slides.

## Non-Negotiables

- Highest priority: read `references/completion-contract.md`. Planning artifacts are not final delivery.
- Choose execution backend before authoring. Read `references/execution-backends.md`.
- Before building new decks, select a reference board. Read `references/reference-board.md` and write `reference_board.json`, `reference_board.md`, and `reference_board_montage.png`.
- Use the executable design system under `design-system/` for typography, grid, layout, components, charts, imagery, and style tokens.
- Start every task with requirement check. Read `references/requirement-check.md`.
- Before asking or reporting to a user, read `references/user-dialogue.md` and communicate in plain Chinese when the user is Chinese.
- Choose a route before generation or editing. Read `references/router.md`.
- Keep V1 routes stable: `template_pptx`, `native_pptx`, `html_slides`, `image_first`.
- For new decks, create `asset_plan.json`; image planning has a minimum, not a maximum. Read `references/asset-plan.md`.
- Before any image generation or visual-heavy slide build, create page-level semantic visual briefs. Read `references/semantic-visual-brief.md` and run `scripts/create_visual_briefs.py` so each required asset is bound to a slide, layout slot, aspect ratio, and prompt.
- Qualified PPT delivery must include at least one AI-generated raster visual captured into the workspace. No-image PPT is not qualified final delivery.
- Generated images must be page-specific. The prompt and `asset_plan.json` must bind each generated image to that slide's title, core message, visual role, and intended composition. Generic seed images, deck-level gate images, or unrelated reused images do not qualify.
- In Codex runs, required PPT raster visuals must use Codex image2 through built-in `$imagegen`. This applies to cover visuals, concept illustrations, scenario illustrations, and in-slide illustrations. Local semantic renderers, icons, native diagrams, color blocks, or placeholders may only be temporary drafts or explicit fallbacks, and must not be marked as final qualified generated illustrations unless the user explicitly accepts an unqualified draft after `IMAGEGEN_OUTPUT_NOT_DISCOVERABLE`.
- Infer 1-3 style candidates from the user's topic, audience, scenario, industry, tone, and references before asking for confirmation. Read `references/style-library.md`.
- For reference PPT work, state exactly what is referenced and what is not. Read `references/reference-ppt.md`.
- For deck edits, preserve facts, data, core meaning, and logic unless the user explicitly asks to rewrite them. Read `references/edit-deck.md`.
- For single-slide edits, lock every non-target slide. Read `references/single-slide-edit.md`.
- Run functional QA and Aesthetic QA before delivery. Write `qa_report.md`, `aesthetic_qa_report.md`, `aesthetic_qa_report.json`, montage previews, and `delivery_manifest.json`. QA must reject unintentional right-side blank space and generated images that are not tied to the slide message. Read `references/qa-gate.md`, `references/aesthetic-qa.md`, and `references/export-matrix.md`.
- Do not read, print, infer, or copy API keys. Do not run third-party install scripts. Installation requires explicit authorization unless the user has granted it for the current phase. Read `references/safety.md`.
- Never report a presentation task as complete unless the requested presentation files have actually been generated, rendered, validated, and saved.

## Route Summary

- `template_pptx`: Use when a PPTX template/reference deck should preserve layouts, masters, placeholders, fonts, and editability. Use `$slides` when exact template-following is available; fallback to `scripts/profile_template.py` and `scripts/build_template_pptx.py`.
- `native_pptx`: Use when the user needs editable PPTX without a template. Prefer `$slides`; fallback to project-local `pptxgenjs` via `scripts/build_native_pptx.mjs`.
- `html_slides`: Use when visual expression is the priority and HTML/PDF/PNG are acceptable. Use `scripts/build_html_deck.mjs` and `scripts/render_html_deck.mjs` with a fixed 16:9 stage.
- `image_first`: Use only when the user explicitly accepts full-slide image pages. Use built-in `$imagegen`, explain editability limits, generate one sample first in Production Mode, then batch or auto-confirm in Test Mode.

Put external API generation, MCP API, OCR-to-editable reconstruction, TTS/video, complex animation, Docker sandbox, and full multi-agent platform work into V2 backlog unless the user explicitly asks otherwise.

## Required Run Artifacts

Create a task directory under `ppt_runs/<date>_<project>/`. Not every task needs every file, but every task needs:

- `requirement_check.md`
- `route_decision.md`
- `qa_report.md`
- `delivery_manifest.json`

New deck creation also requires `asset_plan.json`.

Phase 3 new deck creation also requires:

- `reference_board.json`
- `reference_board.md`
- `reference_board_montage.png`
- `design_spec.md` with selected style and design DNA
- `aesthetic_qa_report.md`
- `aesthetic_qa_report.json`
- `montage.png`

Use `references/artifact-contracts.md` for artifact schemas and `references/workflow-gates.md` for confirmation gates.

## Useful Scripts

- Inspect or profile PPTX: `scripts/inspect_pptx.py`, `scripts/profile_template.py`.
- Scan Chinese reference cases: `scripts/scan_chinese_reference_cases.py`.
- Build reference board: `scripts/build_reference_board.py`.
- Create page-level image briefs and prompt files: `scripts/create_visual_briefs.py`.
- Scan fonts: `scripts/font_inventory.py`.
- Validate plans and outputs: `scripts/validate_slides_plan.py`, `scripts/validate_html_deck.mjs`, `scripts/validate_pptx.py`.
- Render previews and montages: `scripts/render_pptx.py`, `scripts/render_html_deck.mjs`, `scripts/render_montage.py`.
- Aesthetic QA: `scripts/aesthetic_qa.py`.
- Capture built-in image generation output: `scripts/capture_imagegen_asset.py`.
- Assemble or package deliverables: `scripts/assemble_image_deck.py`, `scripts/embed_speaker_notes.py`, `scripts/make_delivery_manifest.py`.

Scripts are executable Phase 3 backends. Use project-local dependencies, render outputs, run functional QA and Aesthetic QA, repair failures when possible, and write `delivery_manifest.json`.

## Built-In Delegation

- Use `$slides` / `presentations` for editable PPTX creation, template-following, render inspection, and PowerPoint exports when available. Local fallback builders must still call `design-system/native/` or `design-system/html/`.
- Use Codex image2 through built-in `$imagegen` for project-bound raster assets. Never ask for an API key for built-in image generation. Before calling it, read `references/imagegen-asset-handoff.md`; after calling it, run `scripts/capture_imagegen_asset.py` to capture any persisted file/attachment into the run directory before using it. The fixed manual handoff inbox is `incoming_assets/imagegen_handoff/`; if the UI download is not automatically discoverable, downloaded images must be saved there so the capture script can pick them up without guessing paths.
- If a built-in backend is unavailable, use the project-local fallback recorded in `references/execution-backends.md`.

## Production Mode And Test Mode

Production Mode:

- Follow the user's real request.
- Ask only missing high-impact questions.
- Use Auto Mode when the user says "随便 / 你看着办 / 直接做 / 自由发挥 / 不用问我".
- For `image_first`, wait for sample confirmation unless Auto Mode clearly authorizes proceeding.
- If the user has not said "直接做", generate style previews or a target sample before batch production.
- Do not deliver a deck with Aesthetic QA score below 85 or severe anti-slop failure modes unless the user explicitly accepts a draft.

Test Mode:

- Use the complete test prompt and isolated run directory.
- If an image sample passes style and QA, auto-confirm and continue.
- Do not block waiting for simulated user confirmation.
- Only mark E2E tests pass when real artifacts exist, render, and pass QA.
