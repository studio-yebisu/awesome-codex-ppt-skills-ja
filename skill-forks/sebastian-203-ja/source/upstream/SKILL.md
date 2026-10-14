---
name: academic-review-decksmith
description: Convert literature reviews, paper folders, thesis drafts, journal-style reports, or research outlines into rigorous academic slide decks and review artifacts. Use when Codex must create, rebuild, or polish PPTX presentations from scholarly sources while preserving academic logic, citation-aware image/formula handling, editable layouts, figure explanations, template fidelity, and export-based visual QA.
---

# Academic Review Decksmith

Use this skill to turn a scholarly review draft and its source papers into a defensible academic presentation or review-support artifact. The goal is not to decorate content, but to make the research argument readable: background, mechanism, structure/method, modeling/theory, control/analysis, applications, limitations, and outlook.

## Operating Principles

- Read the supplied draft, outline, template, and source papers before writing conclusions. If sources are local PDFs or DOCX/PPTX files, inspect them directly.
- Preserve the target template unless the user asks for a redesign. Reuse master style, logos, margins, page numbers, and academic color language.
- Build around technical objects, not vague slogans. Prefer variables, constraints, mechanisms, structures, algorithms, evaluation metrics, and experimental settings.
- Keep citations traceable. Use author-year labels, figure captions, or source notes; never invent references or silently claim unsupported results.
- Keep text audience-facing. Do not include process notes such as "user requested", "from the paper library", "AI-generated", "screenshot later", or production instructions inside final slides.
- Treat figures and formulas as teaching devices. Every essential image or equation needs a short explanation of how to read it and why it matters.

## Workflow

1. **Inventory inputs**
   - Identify the review draft, paper folder, PPT template, logos, previous slide versions, and required output path.
   - Extract existing slide text or DOCX headings when modifying an artifact.
   - Build a source map: platform images, mechanism diagrams, formulas, experimental results, and tables.

2. **Rebuild the academic narrative**
   - Convert chapter headings into a natural argument rather than a mechanical chapter-by-chapter copy.
   - Use this default progression when suitable: research background -> biomimetic mechanism -> structure/drive -> modeling/theory -> control -> applications/limitations.
   - Merge repetitive sections. Keep only subdivisions that help compare methods, explain mechanisms, or support evaluation.

3. **Draft slide-level content**
   - Each slide should contain one core claim plus two to four compact evidence points, tables, or figure annotations.
   - Avoid decorative jargon and "trend" packaging unless the claim is tied to a concrete method, metric, or system.
   - For 30-45 minute academic talks, prefer 24-32 slides with deeper treatment of the theory/control or methods section.

4. **Handle figures, formulas, and tables**
   - Classify each visual as a literature figure, controlled redrawn figure, generated text-free schematic, or editable PPT component.
   - Use literature figures for real platforms, experimental sequences, apparatus, and published results.
   - Redraw process diagrams, control architectures, matrices, and modeling logic when labels must remain editable or bilingual.
   - Add a visible "read this figure/table/formula" note for key visuals, especially theory and method slides.
   - See `references/figure_formula_guidelines.md` when formulas, captions, or visual source notes matter.

5. **Design the deck**
   - Use sober academic styling: restrained palette, high-weight titles, generous margins, consistent tables, and clear image frames.
   - Keep figures serious and source-grounded. Avoid fake 3D icons, mascot-like drawings, decorative gradients, and meaningless pipeline graphics.
   - Make PPT components editable when they express logic, classification, or comparison. Use raster images only for literature figures or final render-safe illustrations.

6. **Export and verify**
   - Export all slides to PNG and inspect for overflow, cropping, image compression, missing source notes, low contrast, and collisions.
   - Search final text for process phrases, unsupported claims, and banned filler terms defined by the task.
   - Fix, re-export, and re-check affected slides. Do not declare success from an unrendered PPTX.
   - Use `scripts/scan_ppt_text.py` for text screening and `scripts/make_overview_assets.py` when preparing GitHub gallery assets.

## Quality Bar

- The final artifact should answer: what problem is studied, what mechanisms govern it, how structures implement those mechanisms, how models describe the system, how controllers act on model/state variables, and where the approach succeeds or fails in real scenes.
- A reviewer should be able to trace every technical statement to a source, a figure, a formula, or a clearly stated inference.
- A listener should understand each key image or formula without needing to read the original paper during the presentation.

## Resource Guide

- `references/academic_review_deck_workflow.md`: detailed end-to-end workflow for turning a scholarly review into a presentation.
- `references/figure_formula_guidelines.md`: rules for captions, figure categories, formula explanation boxes, and source traceability.
- `references/review_language_rules.md`: wording rules for removing AI-like filler and strengthening academic prose.
- `assets/templates/`: optional PPT templates or sample deck shells to copy into new projects.
- `assets/gallery/`: preview images for README or user-facing examples.
