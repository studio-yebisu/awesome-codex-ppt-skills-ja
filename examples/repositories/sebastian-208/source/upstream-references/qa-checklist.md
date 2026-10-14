# QA Checklist

Use this checklist before delivering any academic image PPTX.

## Source And Plan

- [ ] Goal-alignment dialogue was completed before extraction, blueprinting, thumbnail design, or image generation.
- [ ] `qa/alignment-summary.md` exists.
- [ ] `qa/alignment-summary.md` records use case, audience, target slide count/duration, output mode, metadata, style reference, must-preserve figures, and closing wording.
- [ ] Any target slide count from alignment was treated as a design reference, not a strict cap or exact requirement; final count follows the approved blueprint.
- [ ] If duration was provided without an exact page count, Codex suggested a slide budget using the timing rule and the user accepted or revised it before blueprinting.
- [ ] User confirmed the `Alignment Summary`, or all material corrections were incorporated and confirmed again.
- [ ] Paper text extraction is readable, especially Chinese.
- [ ] `Academic Input Pack` was created from the paper before slide planning.
- [ ] Academic narrative spine exists and matches the paper's logic.
- [ ] `qa/deck-blueprint.md` exists with final slide count.
- [ ] `qa/deck-blueprint.md` records explicit `blueprint approval`.
- [ ] The approved `Deck Blueprint` was completed before any three-option thumbnail generation.
- [ ] Each blueprint entry includes slide number, page type, section, title, governing message, evidence role, visual opportunity, candidate visual directions, source evidence, must-preserve evidence, imagegen redraw permission, layout intent, and QA risks; chart/table/result pages also include a key-finding annotation plan.
- [ ] Blueprint entries do not include or require a fixed evidence-shape field; they define the evidence task and leave final visual carriers to sample briefs or image prompts.
- [ ] Unsupported numbers, citations, cases, chart values, and factual claims are marked `needs user confirmation`, omitted, or rewritten as non-numeric qualitative statements before prompting.
- [ ] User-facing parameters were confirmed or recorded as assumptions: school, logo, student name, student ID, major, advisor, date, target slide count as reference, chapter structure, style reference, and closing wording.
- [ ] The paper was organized into a reasonable 4-6 part structure, unless the user explicitly requested otherwise.
- [ ] The approved blueprint includes section divider pages for the main academic parts by default, unless the user explicitly requested a compact or no-divider structure.
- [ ] Any user-requested blueprint revisions were applied and re-approved before thumbnail design.
- [ ] Three thumbnail variants were generated before final slide images.
- [ ] Thumbnail variants, sample pages, preview boards, reference-thumbnail boards, and final slide pages were generated or regenerated with imagegen unless the user explicitly requested a local method.
- [ ] No Python + PIL, SVG/HTML/canvas, screenshots, local drawing, or local refinement was used to create or visually edit thumbnail boards, sample pages, reference boards, or final slide pages without explicit user permission.
- [ ] Thumbnail or sample-page previews follow the preview-board format: style introduction header, 6 miniature slides, and bottom specification band.
- [ ] Each preview board includes exactly these 6 slide types: cover, contents, section divider, 2 representative content pages, and standalone closing/Q&A page.
- [ ] Each of the 6 miniature slide previews inside every preview board is a true 16:9 slide frame; none are vertical cards, square cards, long strips, cropped panels, rotated panels, or irregular panels. The overall preview board itself may use any aspect ratio chosen for the design.
- [ ] Thumbnail boards preview a real page system, not a sparse moodboard or mostly cover-like pages.
- [ ] The 2 representative content miniatures show realistic evidence carriers guided by the approved blueprint, such as data cards, comparison tables, process arrows, evidence strips, mechanism diagrams, chart strips, framework nodes, or conclusion panels.
- [ ] Empty, decorative-only, overly sparse, or blueprint-disconnected thumbnail boards were rejected or regenerated before user selection.
- [ ] The preview-board introduction includes title, version, overall tone, style keywords, color rules, font rules with key font names, icon style, layout traits, and use scenarios.
- [ ] The user selected one thumbnail direction before per-slide generation began.
- [ ] Any requested thumbnail revisions were applied to the selected direction.
- [ ] `qa/thumbnail-selection.md` records selected option and revision notes.
- [ ] `qa/thumbnail-style-contract.md` exists and records palette, typography, icon style, layout density, title system, header/footer treatment, chart/figure language, content-block rhythm, and decorative motifs from the selected thumbnail.
- [ ] 1-2 full-size sample pages were generated from the approved blueprint and selected visual direction before full-slide generation.
- [ ] Full-size sample pages use `thumbnails/selected.png` and `qa/thumbnail-style-contract.md`; they add detail without switching palette, title system, page rhythm, icon language, chart language, or density.
- [ ] If the user selected a sample page as the basis for final pages, `qa/sample-revision-contract.md` exists and records layout skeleton, information density, header/footer system, recurring evidence carriers, chart/table language, conclusion-panel style, required corrections, and high-risk text constraints.
- [ ] `qa/sample-approval.md` records user approval for full-size sample quality.
- [ ] Contents page ranges match the approved blueprint.
- [ ] Required metadata is exact: title, author, school, major, advisor, date.
- [ ] Required source figures are listed with preserve/redraw decisions.
- [ ] Chart or analytical-figure pages prefer imagegen-redrawn, source-faithful figures over directly pasted PDF/DOCX originals unless the user explicitly requested original preservation.

## Image Pages

- [ ] `thumbnails/option_a.png`, `option_b.png`, `option_c.png`, and `selected.png` exist.
- [ ] `image_pages/slide_01.png` through final slide exist.
- [ ] Slide images were generated with imagegen unless the user explicitly requested local refinement / Python + PIL.
- [ ] No unauthorized local refinement, Python + PIL, SVG/HTML/canvas rendering, or local full-slide generation replaced imagegen output.
- [ ] Final slide prompts used `qa/deck-blueprint.md` as the content source of truth.
- [ ] Final slide prompts used `thumbnails/selected.png`, `qa/thumbnail-style-contract.md`, approved sample pages, and `qa/sample-revision-contract.md` when present as visual references.
- [ ] Anchor-page-first generation was used when a user-preferred sample page, key result page, or representative dense evidence page defined the final visual standard.
- [ ] Anchor pages were inspected and accepted before expanding the same visual system to the full deck.
- [ ] Filenames are zero-padded and sequential.
- [ ] Every image is `1280x720` unless a different size was chosen.
- [ ] No missing section divider, summary page, or standalone final closing page.
- [ ] The final closing page is separate and not mixed with summary/outlook/content material.
- [ ] Page numbers are sequential and match the approved blueprint.

## Text And Data QA

- [ ] Chinese titles and body text are readable and not malformed.
- [ ] English subtitles are spelled correctly.
- [ ] Names, school names, major, advisor, and dates are exact.
- [ ] Student ID is included or omitted according to user preference.
- [ ] Final closing wording avoids "感谢聆听" and uses the approved correction-request wording.
- [ ] High-risk metadata was checked on every relevant slide: institution, logo, student/author name, student ID, major/program, advisor display or omission, date, closing wording, section titles, and page numbers.
- [ ] Metric names, metric values, chart labels, and indicator meanings were checked together; no slide has a correct number attached to the wrong indicator meaning.
- [ ] Formulas are not corrupted.
- [ ] Table values and metric values are exact.
- [ ] AUC, accuracy, recall, false alarm rate, inference time, and other metrics match the paper.
- [ ] Figure captions and chart legends are legible.
- [ ] No invented citations, fake logos, or unrelated terms.
- [ ] No invented data, indicators, chart values, author/school metadata, experiment results, cases, citations, or factual claims.
- [ ] Every number, metric, citation, chart value, case, and factual claim in final prompts and slide images traces to source material or explicit user confirmation.

## Figure QA

- [ ] Training curves preserve intended trend and labels.
- [ ] Confusion matrix preserves source data pattern or approved redraw.
- [ ] ROC curve preserves source meaning, AUC, axes, and legends.
- [ ] Every chart/table/result figure marks the key finding with a callout, arrow, highlight, label, shaded region, focal color, or equivalent annotation; charts are not dropped onto slides without interpretation.
- [ ] Redrawn charts preserve hard values, trends, axes, labels, legends, AUC/accuracy numbers, class names, table values, and relative comparisons from the source figure.
- [ ] Model architecture diagrams show correct order and model names.
- [ ] Arrows and flows do not imply unapproved methodology.

## Contact Sheet

- [ ] `qa/contact-sheet.png` includes every slide.
- [ ] The contact sheet rhythm reads as an authored academic defense deck.
- [ ] Section pages are visually distinct.
- [ ] No three content slides accidentally repeat the same composition unless intended.
- [ ] The preferred style reference is visibly respected.
- [ ] The selected thumbnail direction is consistently applied across all final slide images.
- [ ] The approved full-size sample direction is consistently applied across all final slide images.
- [ ] The approved full-size sample direction visibly inherits the selected thumbnail style contract; if it diverges, regenerate the sample before batch generation.

## Speaker Notes

- [ ] `qa/speaker-notes.md` exists unless the user explicitly requested no notes.
- [ ] `qa/speaker-notes.md` contains one note block per approved slide.
- [ ] Notes are ordered sequentially and match `image_pages/slide_01.png` through the final slide.
- [ ] Notes are source-faithful defense/report narration, not unsupported expansion or verbatim slide reading.
- [ ] Notes preserve exact names, metric meanings, chart conclusions, section transitions, and closing-page wording.
- [ ] Notes do not invent citations, data, cases, experiment results, school/author metadata, or claims.

## PPTX Package

- [ ] Final PPTX exists and is non-empty.
- [ ] PPTX slide count equals image count and approved blueprint count.
- [ ] Each PPTX slide contains exactly one full-bleed image.
- [ ] PPTX package validation confirms one image relationship per slide and no extra editable text/shapes on slide pages.
- [ ] PPTX notes count equals slide count unless the user explicitly requested no notes.
- [ ] Each PPTX slide's speaker notes area contains the matching note block from `qa/speaker-notes.md`.
- [ ] No slide has a blank or duplicate image.
- [ ] The final filename follows `<paper-title>_图片版.pptx`.

## Delivery Note

Report slide count, final path, whether speaker notes were inserted, and any residual risk. If OCR/manual text QA was limited, say so explicitly.
