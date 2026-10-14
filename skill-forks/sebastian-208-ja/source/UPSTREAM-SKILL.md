---
name: academic-image-ppt
description: Generate academic, thesis-defense, seminar, or research-report PowerPoint decks as image-based PPTX files from academic papers. Use when the user provides a paper, thesis, dissertation, report, PDF, DOCX, or manuscript and asks for "生成学术PPT", academic PPT, defense PPT, presentation, report deck, "图片版PPT", image-only PPT, imagegen-generated PPT, slide images embedded into PowerPoint, or defense speaker notes. This skill prioritizes full-page raster slide generation with imagegen, strict source-faithful academic content, Chinese text/data QA, speaker notes for each slide, and final PPTX packaging where each slide is one full-bleed image.
---

# Academic Image PPT

Create academic "图片版 PPT" decks from papers. The intended output is not an editable reconstructed PPT. Each slide must first be produced as a complete raster image with imagegen, then embedded full-bleed into a PPTX.

## Core Contract

- Use the built-in imagegen path by default for full-page slide images.
- Treat each slide image as the canonical page. The PPTX is only a delivery wrapper containing one full-slide image per slide.
- Generate source-faithful defense speaker notes for each slide by default unless the user explicitly asks to omit notes. Insert each slide's note into that slide's PPT speaker notes area during final PPTX packaging.
- Use 16:9 `1280x720` as the default slide image size unless the user gives another size.
- Do not rebuild the deck as editable shapes unless the user explicitly asks for editable PPT.
- Do not switch to local refinement, local drawing, Python + PIL, SVG/HTML/canvas rendering, or any "本地精修方式生成" path unless the user explicitly requests it. If the user asks for image gen / imagegen generation, use imagegen for slide images and do not decide on a local generation method yourself.
- Treat thumbnails, sample pages, preview boards, reference-thumbnail boards, and final slide pages as visual generation outputs. Generate or regenerate them with imagegen by default. Do not use Python + PIL, SVG/HTML/canvas, screenshots, local drawing, or other local refinement to create or visually edit these assets unless the user explicitly asks for that method.
- Local tools may be used only for mechanical tasks such as file copying, dimension checks, OCR, contact sheets, PPTX packaging, compression, and package validation; they must not replace imagegen for visual page, thumbnail, sample, or reference-board creation.
- Do not hardcode slide counts. The user's target slide count from goal alignment is a planning reference, not a strict cap or exact requirement. Design the `Deck Blueprint` around actual academic communication needs, then derive the final count from the approved blueprint and verify it against images, contact sheet, and final PPTX.
- Start with an interactive goal-alignment dialogue. Proactively help the user complete key parameters when they are not already supplied: paper file, defense/report setting, audience, target slide count or duration, school, logo, student name, student ID, major, advisor, date, paper type, chapter preference, style reference, must-preserve figures, closing wording, and output format. Treat any user-provided target slide count as a blueprint design reference only; do not force the deck to match it if the paper's structure, section divider pages, source figures, or explanation needs require a different count. If the user provides a duration but not a page count, suggest a slide budget and ask whether to use it: maximum one slide per minute; typical academic budgets are 8-10 content slides for 10 minutes, 12-14 for 15 minutes, 15-18 for 20 minutes, and 30-40 for a 45-minute seminar, with cover/contents/closing handled according to the approved structure.
- Produce an `Alignment Summary` and obtain user confirmation before locking the production direction. If the user corrects any critical parameter, revise the summary and confirm again.
- Organize academic content into a reasonable 4-6 part structure by default. Do not force every paper into the same outline; adapt the section titles to the paper type and user preference.
- When designing the `Deck Blueprint`, include section divider pages by default for the main academic parts unless the user explicitly asks to omit or compress section dividers. Treat them as structure pages when calculating the full deck count.
- Build an `Academic Input Pack` and a page-by-page `Deck Blueprint` before any thumbnail design. The blueprint is a formal production artifact, not a temporary draft.
- Each `Deck Blueprint` entry must include slide number, slide type, section, title, governing message, evidence role, visual opportunity, candidate visual directions, source evidence, must-preserve evidence, whether imagegen may redraw visuals, and QA risks. Do not generate or require any separate fixed evidence-shape field. The blueprint should define the evidence task, not lock a fixed visual carrier such as cards, boxes, matrix, funnel, route map, or flowchart. Choose the final visual carrier later by combining the blueprint's evidence role with the approved thumbnail/sample visual contract.
- Show the full `Deck Blueprint` to the user and ask for approval or page-level revisions. The user may change any page title, governing message, section order, page count, figure use, or slide inclusion. Iterate until the user explicitly approves the blueprint.
- Do not generate three thumbnail variants until `blueprint approval` is recorded.
- Before generating any final per-slide images, create exactly three style thumbnail variants and present them to the user for selection. Thumbnail variants and sample-page previews must follow the preview-board format in `references/prompt-templates.md`: a style introduction header, 6 miniature slides, and a bottom specification band for colors, fonts, icons, layout traits, and use cases. The thumbnail board is a real page-system preview, not a sparse cover-style moodboard: the 6 previews must include cover, contents, section divider, 2 representative content pages, and standalone closing/Q&A page. Content miniatures must show realistic evidence carriers such as data cards, tables, process arrows, comparison panels, mechanism diagrams, chart strips, or conclusion panels. The overall preview board does not have to be 16:9; choose its aspect ratio freely to fit the header, 6-slide body, and specification band. However, each of the 6 miniature slide previews inside the board must be drawn as a true 16:9 slide frame. Do not stretch, crop, rotate, or turn any miniature slide into a vertical card, long strip, square card, or irregular panel. Reject or regenerate thumbnail boards that feel empty, decorative-only, or disconnected from the approved deck structure. Do not proceed to full-slide generation until the user chooses one variant and any requested thumbnail-level revisions are applied.
- After the user selects a thumbnail direction, create `qa/thumbnail-style-contract.md` from the selected board. It must record palette, typography, icon style, layout density, title system, header/footer treatment, chart/figure language, content-block rhythm, and decorative motifs. Full-size sample pages must inherit this contract and `thumbnails/selected.png`; samples may become more detailed, but must not switch to another visual system.
- After full-size sample pages are shown, if the user prefers a specific sample structure or asks to use one sample as the basis for the deck, create `qa/sample-revision-contract.md` before final generation. This contract must record the selected sample's layout skeleton, information density, header/footer system, recurring content blocks, chart/table language, conclusion-panel style, required corrections, and high-risk text constraints. Final slide prompts must inherit both `qa/thumbnail-style-contract.md` and `qa/sample-revision-contract.md` when both exist.
- Maintain a high-risk text and data checklist throughout prompting and QA. At minimum, check school/institution name, logo use, student/author name, student ID, major/program, advisor display or omission, date, closing wording, section titles, page numbers, metric names, metric values, chart labels, and indicator meanings on every relevant slide. A correct number with a wrong indicator meaning is a failure and must be regenerated or corrected.
- Use anchor-page-first generation after sample approval when the deck has a user-preferred sample, a critical evidence page, or a page that defines the visual system. Generate that anchor page first, inspect it, save it as `image_pages/slide_XX.png` only if it satisfies the visual contract and high-risk text constraints, then expand to the rest of the deck. If a page repeatedly fails imagegen, record it, continue with independent pages when safe, and return to regenerate the failed page before contact-sheet QA.
- Generate the final page as a standalone closing / Q&A / correction-request page. Do not merge the closing page with summary or content slides. Avoid "感谢聆听"; prefer wording such as "恳请各位老师同学批评指正" or "恳请各位老师批评指正", adjusted to the user's audience.
- Create `qa/speaker-notes.md` after the final blueprint is approved and before PPTX packaging. Notes must be split one section per slide, follow the approved slide order, and act as brief defense narration rather than a verbatim reading of the slide. Use only source-supported content, preserve the user's audience tone, include transition cues where helpful, and keep closing-page wording consistent with the approved final slide.
- For charts and analytical figures such as training curves, confusion matrices, ROC curves, bar charts, tables, and result plots, prefer imagegen redrawing instead of directly pasting the original PDF/DOCX figure. Use the source figure as the strict data reference: preserve hard metrics, values, trends, axes, legends, labels, AUC/accuracy numbers, and class names. Integrate the redrawn chart into the page style, and add callout arrows, highlights, labels, or shaded regions that mark the key finding so the slide is self-explanatory. Directly paste an original figure only when the user asks for original preservation or exact redraw quality cannot be safely achieved.
- Run visual and text QA after imagegen. Chinese text, formulas, names, school metadata, captions, metrics, and table values are high-risk. Never invent data, indicators, citations, chart values, school or author metadata, experiment results, or source claims. If a number, citation, case, chart value, or factual claim is not in the source material or explicitly confirmed by the user, mark it as `needs user confirmation`, omit it, or rewrite it as a non-numeric qualitative statement; do not send it into an image prompt.

## Required Companion Skills

Use these when applicable:

- `imagegen` for every full-slide raster generation or regeneration.
- `documents` or PDF-reading tools to extract academic paper content from DOCX/PDF.
- `Presentations` or artifact-tool presentation JSX to package final images into PPTX.
- `scripts/package_image_pptx_with_notes.mjs` when packaging image pages into PPTX with speaker notes.

## Workflow

For the full workflow, read `references/workflow.md`.

1. Run the interactive goal-alignment dialogue and record `qa/alignment-summary.md`.
2. Confirm the `Alignment Summary` with the user before proceeding.
3. Extract the paper into readable text and media. Confirm Chinese text is not mojibake before summarizing.
4. Build the `Academic Input Pack`, academic narrative spine, and page-by-page `Deck Blueprint`.
5. Show the `Deck Blueprint` to the user. Revise titles, governing messages, page count, section order, evidence roles, and candidate visual directions until the user approves it.
6. Record `blueprint approval` in `qa/deck-blueprint.md`; do not proceed without it.
7. Generate three thumbnail style variants using `references/prompt-templates.md`, then show them to the user.
8. Wait for the user to choose one variant. If the user requests changes, revise that chosen variant and confirm it before continuing.
9. Generate `qa/thumbnail-style-contract.md` from the selected thumbnail direction.
10. Generate 1-2 full-size sample pages from the approved blueprint, `thumbnails/selected.png`, and `qa/thumbnail-style-contract.md`; revise until the user approves both sample quality and style inheritance.
11. Lock the selected thumbnail, thumbnail style contract, approved sample direction, and any `qa/sample-revision-contract.md` as the visual contract for all final slide images.
12. Generate one full-slide image per slide with imagegen using the selected visual contract. Prefer anchor-page-first generation when a page defines the deck's style or carries the user's strongest preference.
13. Assemble `qa/contact-sheet.png` and inspect the full deck at thumbnail level.
14. Run the QA gates in `references/qa-checklist.md`.
15. Generate `qa/speaker-notes.md`, one note block per approved slide, with source-faithful defense narration.
16. Package the final PPTX by embedding each `image_pages/slide_XX.png` full-bleed and inserting the matching speaker note into that slide's notes area.
17. Verify final PPTX slide count, image count, approved blueprint count, notes count, and that each slide contains exactly one full-bleed image plus the intended speaker note.

## Run Folder Convention

Use a per-run workspace. Keep final deliverables in `output/` and QA artifacts in `qa/`.

```text
<run>/
  image_pages/
    slide_01.png
    slide_02.png
  thumbnails/
    option_a.png
    option_b.png
    option_c.png
    selected.png
  qa/
    alignment-summary.md
    deck-blueprint.md
    thumbnail-style-contract.md
    sample-revision-contract.md
    sample-approval.md
    speaker-notes.md
    contact-sheet.png
    ocr-report.md
    pptx-package-check.md
  output/
    <paper-title>_图片版.pptx
```

Package with speaker notes using:

```bash
npm install
node skills/academic-image-ppt/scripts/package_image_pptx_with_notes.mjs \
  --images <run>/image_pages \
  --notes <run>/qa/speaker-notes.md \
  --out <run>/output/<paper-title>_图片版.pptx \
  --title "<paper title>"
```

Write `qa/speaker-notes.md` with one heading per slide:

```markdown
## Slide 01
第一页答辩讲稿。

## Slide 02
第二页答辩讲稿。
```

## Case Study

This skill was created from the project in `D:\AI\Codex PPT1_6.3wsg`.

Read `references/project-postmortem.md` before working on a similar thesis-defense deck. The key lesson: the user's actual desired output was a 21-page full-image academic defense PPTX, not an editable PPT reconstruction. A previous build drifted to 20 slides and hardcoded that count, so page-count reconciliation is a mandatory gate.

Useful bundled assets:

- `assets/case-study-contact-sheet.png`: the 21-page case-study quality target.
- `assets/reference-thumbnails/case-study-style-grid.png`: preferred blue academic visual system.
- `assets/reference-thumbnails/version-a-academic-blue.png`
- `assets/reference-thumbnails/version-b-clean-college.png`
- `assets/reference-thumbnails/version-c-formal-defense.png`
- `assets/reference-thumbnails/option-c-preview-board-format.png`: required preview-board format example for future thumbnails and sample pages.

## Delivery Rules

Final response should include:

- final PPTX path;
- slide count;
- whether speaker notes were inserted;
- whether every slide is image-only;
- QA status and any remaining risks.

Do not claim the deck is complete if any image is missing, if speaker notes are missing or misaligned, if the PPTX slide count differs from the image count, or if Chinese/data QA has not been performed.
