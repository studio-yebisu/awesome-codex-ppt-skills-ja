---
name: soil-teaching-slides
description: Turn teaching materials into SOIL-style instructional slide plans, PPTX decks, or offline HTML presentations. Use when the user asks for teaching slides, instructional decks, SOIL slide planning, editable PPTX, ChatGPT Image 2/image-first PPTX, browser-based or HTML slides, page-by-page slide plans, YAML-driven slide style, hand-drawn teaching diagrams, or converting lesson materials into slides. Always produce a text-only page-by-page plan for confirmation before generating final slide assets.
---
# SOIL Teaching Slides

Use this skill when the user wants to turn teaching content into a structured instructional slide deck.

Work in Traditional Chinese by default for Taiwan education contexts.

## Core Rule

Always begin with a text-only, page-by-page teaching slide plan. Stop and wait for user confirmation before generating images, PPTX files, HTML decks, or final slide assets.

If the user provides a YAML/style definition, treat it as the visual source of truth for style, but keep SOIL page role and structure as the source of truth for layout decisions.

Default visual architecture:

- Mode A uses the user's old `黑白手繪教學圖解風` v2.1 template and YAML. Read `references/soil-handdrawn-style-v2.yaml` as the canonical style source and `references/handdrawn-soil-style.md` as its compact operational guide.
- Mode B is an independent editable large-text system. Never import Mode B typography, page chrome, title treatment, or no-footer rule into Mode A.
- Mode C is an independent offline HTML system. Reuse the approved SOIL teaching structure, but do not inherit the fixed visual system of A or B unless the user explicitly requests it. Before building, ask the user to choose a visual style unless they already supplied one. If they have no preference or do not answer the style part of the confirmation, use the approved default Structured Teaching style defined in `references/html-style-selection.md`.
- Override a mode's default only when the user explicitly supplies another template, brand system, or visual style for that mode.

## Output Modes

Offer these modes after the user confirms the plan, unless the user already chose one:

- A. Image-first PPTX: generate one full-slide 16:9 image per page, then package the images into a PPTX. Slide text is not expected to be editable.
- B. Editable PPTX: default to the approved v8 pure-text style and build the deck with editable native text boxes, shapes, lines, tables, and diagrams. Do not add images unless the user explicitly requests them.
- C. Offline HTML presentation: create a browser-playable 16:9 slide deck with editable HTML text and structure. Default to local HTML, CSS, JavaScript, and assets with no build step, CDN, or network dependency. Add images only when pedagogically necessary or explicitly requested.

Default to mode B when the user emphasizes classroom reuse, future editing, or teacher customization. Default to mode A when the user asks for highly visual SOIL-style slides, ChatGPT Image 2, image2, image-first, direct image-generated slide text, or the default black-and-white hand-drawn teaching diagram style.
Default to mode C when the user asks for HTML slides, browser slides, a web presentation, offline web slides, or an editable presentation that runs without PowerPoint.

## Phase 1: Slide Plan

Prepare a reviewable slide plan, usually 8-14 slides unless the material clearly needs a different length.

For each slide, include:

- Page number and total pages
- Course or section label. For Mode A, approve exactly one short header label per slide; keep it separate from the slide's required short labels
- Exact slide title
- One teaching point
- Learner task: what the learner should notice, compare, sequence, decide, or practice
- Page role: question opener, misconception clarifier, comparison, process, cause/effect, category, practice, summary, or another clear role
- Visual structure: comparison, flow, hierarchy, matrix, cycle, timeline, risk map, checklist, or another clear structure
- Required short labels
- Core takeaway or closing judgment. For Mode A, plan it as the old-style bottom reminder bar by default; for Mode B, place it inside the page structure unless the user explicitly requests a special footer
- For Mode C, add a short deck-level style brief: selected style family, selection reason, palette direction, typography direction, motion level, and image policy. If the user did not specify a style, offer 2-4 concise choices from `references/html-style-selection.md`, put the content-based recommendation first, and include the approved default Structured Teaching option. State that no preference means the approved default.

End Phase 1 by asking the user to confirm, revise, reorder, add, or remove slides, and to choose output mode A, B, or C if needed. For Mode C, include the style choice in this same confirmation request rather than creating an unnecessary extra round. Do not ask again when the user already supplied an explicit visual direction.

## Phase 2A: Image-First PPTX

Use this path only after the user confirms mode A.

1. Apply SOIL cognitive editing to the approved slide plan.
2. Use the default `黑白手繪教學圖解風` unless the user explicitly provides a different style. If the user provides a YAML/style file, extract only durable style constraints: palette, typography tone, illustration style, layout language, emphasis rules, and final checks. Do not copy sample layouts unless the YAML explicitly says to.
3. Generate one 16:9 full-slide image prompt per page. Each prompt must state the page role and visual structure from Phase 1.
4. Generate one slide image per page with the image generation tool the user requested. If the user requests ChatGPT Image 2/image2, use image2-style prompts and keep the final text in the generated image when explicitly requested.
5. Save images as `slide-01.png`, `slide-02.png`, and so on in a project output folder.
6. Create a contact sheet for review and inspect it before packaging.
7. Regenerate any slide whose style, page role, page order, or text legibility clearly fails.
8. Package the images into a widescreen PPTX with one image covering each slide.
9. Verify the PPTX has the expected slide count and no overflow.

### Image2 Direct-Text Rule

For Mode A black-and-white hand-drawn decks, default to direct-generated Traditional Chinese inside the image unless the user explicitly requests editable/native PowerPoint text. Apply these rules:

- Put only short, large, approved text in the image prompt: page number, section label, title, key labels, and bottom takeaway.
- Use only the approved single section label in the top-left header. Never join the slide's key labels into the header.
- Use exact Traditional Chinese text in quoted form.
- Tell image2 to make the visible typography resemble Microsoft JhengHei: clean bold Traditional Chinese sans-serif, upright strokes, high legibility, and no calligraphic styling.
- Apply the Microsoft-JhengHei-like typography to every visible character, including page number, section label, title, diagram labels, small illustration text, and bottom takeaway.
- Avoid dense prose, tiny labels, long paragraphs, and large matrices with many small cells.
- Prefer simpler visual structures when text is direct-generated: comparison, three-step process, four-item checklist, simplified transfer map.
- Expect that image2 may slightly alter small characters or punctuation. Inspect the contact sheet and regenerate the worst failures with fewer words and larger labels.
- Do not replace direct image2 text with native PowerPoint text overlays merely to guarantee an installed font. Use native PowerPoint text only when the user explicitly requests editable or typographically exact text.

### Default and YAML-Driven Hand-Drawn Style

Before producing any Mode A image-first deck, read both `references/soil-handdrawn-style-v2.yaml` and `references/handdrawn-soil-style.md`. Treat the YAML as canonical and the Markdown as a concise execution guide. If the user explicitly supplies a different template, brand system, or visual style for Mode A, follow that newer instruction instead.

Apply these priorities:

1. SOIL page role and visual structure
2. This slide's teaching task
3. This slide's information relationship
4. YAML visual style consistency
5. Aesthetic polish

For black-and-white hand-drawn decks, use white background, black line art, gray sketch shading, Microsoft-JhengHei-like Traditional Chinese typography, medium-gray page-number blocks, light-gray takeaway borders, black structural frames, and sparse orange accents. Keep the top-left page number and section label geometry identical across the deck. Orange should mark the shared short header underline, arrows, step badges, check marks, or one key phrase, not decorate the page.

## Phase 2B: Editable PPTX

Use this path only after the user confirms mode B.

Read `references/editable-pptx-layout.md` before building. Treat `assets/mode-b-approved-reference.pptx` as the visual benchmark for spacing, hierarchy, framed-text structures, and large-text treatment only; never inherit its teaching content, wording, or fixed slide count.

Use the Presentations skill and `@oai/artifact-tool` to create PowerPoint-native objects. Import `scripts/editable_b_style_helpers.mjs` when practical so color, typography, page chrome, footer, and center-line calculations remain consistent.

Also read `references/b-mode-quality.md` and use `scripts/editable_b_formula_helpers.mjs` for mathematical and scientific expressions. Apply its learner-sequence, formula, filename, package-validation, and rendering checks only to Mode B; preserve Modes A and C.

Mode B defaults to a pure-text deck:

- White 1280 × 720 canvas and Microsoft JhengHei typography
- Left-aligned title at 32 PowerPoint pt (`fontSize: 43` px), bold and normally kept on one line
- Large-text judgments, primary questions, and conclusions at 48–72 PowerPoint pt (`fontSize: 64–96` px); default to one line and use two lines only as a rare exception
- General labels and supporting explanations at 20–23 PowerPoint pt (`fontSize: 27–31` px); do not go below 20 pt for audience-facing teaching content
- Black text, gray structural lines, and muted orange `#D35230` reserved for one core concept or active step
- No fixed takeaway footer by default. Put the conclusion inside the page structure: the large statement itself, the final highlighted frame, or a summary band within the content area
- Small gray `section · page` metadata at bottom right when page identification is useful
- Comparison columns, process rows, and question frames positioned from the page center line with calculated symmetry
- Framed-text layouts may use many boxes when they clarify grouping, sequence, or hierarchy. Use heavier outer frames, lighter inner frames, and at most one orange focus
- Speaker notes on every slide

Build the deck with editable PowerPoint-native objects:

- Text boxes for titles, labels, body text, and takeaways
- Shapes for concept blocks, steps, groups, emphasis, and framed-text structures
- Lines, arrows, and connectors for relationships
- Tables or matrix layouts when comparison is the teaching goal
- Speaker notes when they help the teacher deliver the lesson

Do not flatten the full slide into a single image. Do not add decorative or supporting images by default. Use images only when the user explicitly asks for them.

Use `addPageMeta(...)` for optional bottom-right metadata. Keep `addTakeaway(...)` only for an explicitly requested special takeaway page; it is not default page chrome.

For large-text pages, shorten the statement or split the idea across slides before allowing a second line. Do not shrink a long statement merely to force it into one line.

Do not create unused transparent objects, empty text boxes, white cover masks, or negative-size shapes. Do not use the old top-left page marker, centered title, single gray-rule footer, or detached page marker. The editable orange `◎` inside the takeaway bar is the only default footer marker.

Before final delivery, verify:

- Expected slide count
- Text is readable and does not overlap
- The main teaching concept is visually dominant and at least one clear size tier larger than supporting text
- Each slide has one clear teaching job
- The PPTX remains editable
- Titles are left-aligned and comparison/process layouts are symmetric about the slide center
- Large-text statements are one line by default and never exceed two lines
- Framed-text pages distinguish outer groups, inner items, and one orange focus
- No fixed takeaway footer appears unless the page plan explicitly calls for a special takeaway page
- Every slide has speaker notes
- `ppt/media` is zero unless the user explicitly requested images
- Empty transparent objects, white cover masks, and negative `cx`/`cy` are zero

Render every slide at full size and as a contact sheet. Run the Presentations overflow check and `scripts/validate_editable_b_pptx.py` before delivery. Add `--forbid-fixed-takeaway` unless the approved slide plan explicitly requests a special bottom takeaway page.

For Mode B, also run `scripts/test_editable_b_quality.py` when changing the skill or formula/rendering code. On a deck, use the validator's package, editable-object, and formula checks, then render every slide through PowerPoint when available or LibreOffice otherwise. Record which application opened and rendered the file; structure validation or LibreOffice success alone does not establish Microsoft PowerPoint compatibility.

On Windows with Microsoft PowerPoint installed, use `tests/powerpoint_smoke_test.ps1` to open the final deck read-only and export each slide. Use `-TestEditability` for a temporary-copy text edit check; never save test edits to the delivered deck.

## Phase 2C: Offline HTML Presentation

Use this path only after the user confirms mode C or explicitly asks for an HTML/browser presentation.

Before building, read both:

- `references/html-slide-deck.md` for the file contract, template workflow, interaction rules, and QA requirements
- `references/html-style-selection.md` for content-driven style selection when the user does not provide a visual direction

1. Resolve the deck-level visual style before building. Follow an explicit user style first. Otherwise present 2-4 recommended choices as part of the Phase 1 confirmation. If the user says they have no preference, asks the agent to decide, or confirms the plan without addressing style, use the approved default Structured Teaching style. Record the decision in the style brief and do not mix competing families.
2. Preserve the confirmed SOIL page order, exact titles, teaching tasks, page roles, information relationships, and required labels.
3. Copy `assets/html-deck-template/` into a new project output folder. Replace the sample slides, theme tokens, and document title with the approved content; do not edit the installed template in place.
4. Build slides as semantic HTML with editable text. Use CSS Grid/Flexbox and inline SVG for comparison, process, hierarchy, cause/effect, timelines, checklists, and simple diagrams. Use raster images only when they materially improve understanding or the user asks for them.
5. Keep the default deck offline and build-free: local `index.html`, `styles.css`, `slides.js`, and optional `assets/`. Do not add a CDN, remote font, analytics, web request, package manager, bundler, React, or a slide framework unless the user explicitly requests it.
6. Provide 16:9 stage scaling, previous/next controls, Arrow/PageUp/PageDown/Space navigation, Home/End navigation, URL hash deep links, current/total page status, progress indication, fullscreen support, reduced-motion support, and one-slide-per-page print CSS.
7. For dense teaching content, simplify before shrinking. At the 1600 × 900 design stage, target 24–28 px for table or matrix primary text and 18–21 px for secondary text. Remove repeated explanation, reduce cells to one main statement plus one necessary cue, and split the slide if it still does not fit.
8. Keep transitions restrained and instructional. Add progressive reveal only when the user requests sequencing or when the approved page plan depends on staged attention. Keep headers visible, reveal rows or groups in teaching order, reveal the judgment last, allow backward steps, show the current reveal count, and force all fragments visible in print.
9. Do not add autoplay, sound, video, timers, or decorative animation unless requested.
10. Preview the deck through a local static server when possible. Check at 1280x720 and 1920x1080, test keyboard navigation and hash links, inspect every slide for overflow, and print-preview the one-slide-per-page layout.
11. Run `node scripts/validate_html_deck.mjs <output-folder>` from the skill directory or copy the validator to a writable location. Fix all errors before delivery; report warnings that reflect intentional choices.
12. Deliver the complete folder and link to `index.html`. Explain that text and structure remain editable and that the deck runs locally without PowerPoint or a build step.

## SOIL Design Priorities

For each slide, make the thinking structure visible:

- Use size to show what matters most.
- Use distance to show grouping or separation.
- Use lines and arrows to show relationships.
- Use color sparingly to distinguish roles, stages, or contrasts.
- Use shape differences to signal different kinds of concepts.

Avoid decorative slides that look polished but do not clarify the learning relationship.

## Verification

For image-first decks:

- Confirm the output folder contains exactly one `slide-XX.png` per slide.
- Create a clean contact sheet from only `slide-*.png`, excluding previous contact sheets or draft images.
- Inspect whether the visible style matches the user's YAML/reference style.
- Inspect direct-generated text for obvious page-breaking errors; regenerate the worst slides instead of accepting unreadable text.
- Package into PPTX and verify slide count, media count, and no overflow.
- If render tools fail because of Windows Chinese path or `HOME` runtime issues, copy the PPTX to an ASCII temp path and set `HOME=C:\Users\User` before rendering.

For HTML decks:

- Confirm `index.html`, `styles.css`, and `slides.js` exist and no required asset is missing.
- Confirm the number and order of `.slide` sections match the approved plan and every slide has a unique `data-slide-id`.
- Confirm the deck contains no unapproved HTTP(S) dependency, remote font, analytics, or network request.
- Run `scripts/validate_html_deck.mjs` and fix every error.
- Test keyboard navigation, Home/End, hash deep links, fullscreen control, current/total status, and progress indication.
- For progressive reveal, verify that the first forward action reveals content without changing pages, the action after the final fragment advances, backward navigation hides a fragment before leaving the slide, and print mode exposes every fragment.
- Inspect all slides at 1280x720 and 1920x1080 for clipping, unreadable type, overlap, or broken relationships.
- Check print preview or print CSS so each slide occupies one page without navigation chrome.
- Report any browser-specific behavior or untested print/PDF path honestly.
