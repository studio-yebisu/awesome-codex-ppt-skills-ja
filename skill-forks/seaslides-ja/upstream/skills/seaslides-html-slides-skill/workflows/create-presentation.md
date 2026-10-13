---
description: Generate HTML presentation content (content.html) from a design spec and theme
---

# Create Presentation Content Workflow

> **Role invoked**: Executor (see `${SKILL_DIR}/references/executors/base.md` + `general.md` or `academic.md`)

Generate the content file (`content.html`) for an HTML slide deck using Template-Content Separation (TCS).

## Trigger Condition

Called when:
- A `template.css` exists in the project (copied from a selected theme)
- A `content_design_spec.md` exists with the slide outline and content plan

## Process Overview

```
Read Specs --> Generate content.html --> Add Speaker Notes --> Source Gate --> Build --> Review --> Final Gate
```

---

## Step 1: Read Design Specifications

Read the following files in order:

1. **`content_design_spec.md`** -- Full design specification (slide outline, content per page, image assignments, page rhythm, component mapping)
2. **`theme.md`** -- Theme API reference from `${SKILL_DIR}/templates/<theme>/theme.md` (CSS classes, component catalog, color palette, typography)
3. **`demo.html`** -- Working example from `${SKILL_DIR}/templates/<theme>/demo.html` (structural density reference)
4. **`template.css`** -- Skim for available CSS classes and variables
5. **`${SKILL_DIR}/references/components.md`** -- Full component catalog with usage examples

---

## Step 2: Determine Style

Check `content_design_spec.md` for the declared style objective:

| Style | Executor Reference |
|-------|-------------------|
| **General** | `${SKILL_DIR}/references/executors/base.md` + `${SKILL_DIR}/references/executors/general.md` |
| **Academic** | `${SKILL_DIR}/references/executors/base.md` + `${SKILL_DIR}/references/executors/academic.md` |

---

## Step 3: Generate content.html

### 3.1 Content Generation Rules

- **Semantic HTML sections** -- each slide is a `<section class="slide [mode] [modifier]">` block
- **CSS classes from theme only** -- use classes defined in `template.css` and documented in `components.md`. Never invent undeclared classes
- **Canonical inline data geometry only** -- follow the class/property allowlist in `shared-standards.md`
- **No `<style>`, `<script>`, or `<link>` tags** -- content.html contains only `<section>` blocks
- **Browser-rendered layout** -- use theme-defined classes; flexbox, grid, and absolute positioning are allowed when the final Chromium render is stable
- **Mode classes required** -- every slide gets one of: `light`, `dark`, `hero light`, `hero dark`
- **Action titles** -- state the conclusion, not a topic label

### 3.2 Slide Structure

```html
<section class="slide hero dark" data-notes="Speaker notes here" data-anim="fade">
  <div class="slide-header">
    <h1>Main Title</h1>
    <p class="subtitle">Supporting context</p>
  </div>
  <div class="slide-body">
    <!-- Content using theme components -->
  </div>
</section>
```

### 3.3 Image Integration

- Use images listed in `content_design_spec.md`
- Reference images via relative path: `assets/filename.jpg`
- For pending images: use `<!-- [Pending: description] -->` placeholder
- Image containers should use stable dimensions (`height`, `aspect-ratio`, grid tracks, or explicit constraints) so batch export does not shift.

---

## Step 4: Add Speaker Notes

Add `data-notes="..."` on EVERY `<section>` element:

- 2-5 natural sentences per slide
- TTS-ready (no bracketed markers, no meta-commentary)
- Tone matches the style objective (conversational / analytical / pedagogical)
- HTML-escape quotes within the attribute value

---

## Step 5: Add Animation Attributes

Add `data-anim="..."` on slide sections where appropriate:

- Available values depend on theme (e.g., `fade`, `slide-left`, `zoom`)
- Not every slide needs animation; use for emphasis and transitions
- Consistent within a deck -- pick 2-3 animation types maximum

---

## Step 6: Source Gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --source-only --profile standard-project
```

Fix source and TCS errors before building. This project-directory gate replaces legacy single-file validation for standard-slide delivery.

---

## Step 7: Build, Review, and Final Gate

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --require-build --artifact-profile visual
```

Inspect `output/overview.png` and `output/browser_pngs/` first: settled browser PNGs and `dom-audit.json` are the layout truth. Use SVG-route `output/pngs/` and `render-fidelity.json` only to diagnose conversion differences. Re-run the source gate and full build after every change. For PPTX delivery, use `html_compiler.py <project_path> --all --include-pptx`, then validate with `--require-build --artifact-profile delivery`.

### Validation Checklist

- [ ] The standard-project source gate passes before build
- [ ] CRITICAL: Every slide has a `data-notes="..."` attribute with real content
- [ ] Every slide has a mode class (`light` / `dark` / `hero light` / `hero dark`)
- [ ] No `<style>`, `<script>`, or `<link>` tags in content.html
- [ ] Inline styles conform to the canonical data-geometry allowlist
- [ ] Only CSS classes defined in `template.css` are used
- [ ] `data-anim` attributes present where appropriate
- [ ] Relevant and user-required source images are referenced; exclusions are documented
- [ ] Repeated layouts and modes are intentional and content-driven
- [ ] Component vocabulary supports the content without quota-filling
- [ ] Browser PNGs and DOM audit confirm stable layouts; SVG-route output is conversion diagnostics

---

## Notes

- This workflow generates `content.html` only -- `template.css` and `index-template.html` should already exist
- For theme selection, run `select-theme.md` first
- Speaker notes are required for TTS audio generation
- After validation passes, proceed to `visual-review.md`
