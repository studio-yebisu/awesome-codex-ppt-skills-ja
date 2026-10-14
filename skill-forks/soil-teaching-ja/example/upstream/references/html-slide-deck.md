# Mode C Offline HTML Slide Deck

## Contents

1. Output contract
2. Template workflow
3. Slide markup
4. Layout and typography
5. Dense teaching content
6. Progressive reveal
7. Interaction and motion
8. Images and diagrams
9. Preview and verification
10. Delivery

## Output Contract

Create a build-free, offline-ready folder:

```text
deck-name/
├── index.html
├── styles.css
├── slides.js
└── assets/          # only when needed
```

The user must be able to open `index.html` locally or serve the folder with a basic static server. Keep all presentation text and structural diagrams editable in HTML, CSS, or inline SVG.

Do not add remote fonts, CDN scripts, analytics, network requests, package managers, bundlers, React, or slide frameworks by default. Use a framework only when the user explicitly requests it.

## Template Workflow

1. Copy `assets/html-deck-template/` into a new output folder.
2. Replace the sample title, theme class, slide sections, labels, and metadata.
3. Preserve the required accessibility, navigation, scaling, print, and reduced-motion hooks.
4. Put optional local images in `assets/` with descriptive filenames and alt text.
5. Run `scripts/validate_html_deck.mjs` against the output folder.

Never modify the installed template in place.

## Slide Markup

Use one semantic section per page:

```html
<section class="slide layout-statement" data-slide-id="opening" aria-labelledby="slide-01-title">
  <p class="eyebrow">單元標籤</p>
  <h2 id="slide-01-title">本頁標題</h2>
  <div class="slide-content">…</div>
</section>
```

Rules:

- Give every slide one unique, stable `data-slide-id`.
- Give every slide one heading and connect it with `aria-labelledby`.
- Keep page order equal to the approved SOIL plan.
- Use real HTML text instead of text baked into images.
- Use lists, figures, tables, and blockquotes only when their semantics match the content.
- Keep one primary teaching task per slide.

## Layout and Typography

Use a 16:9 design stage based on `1600 × 900` CSS pixels and scale it to the available viewport. Keep all important content inside a safe area of at least 64 pixels.

Choose page layout from the SOIL information relationship:

- Statement or belief: one dominant sentence with generous whitespace.
- Comparison: two aligned columns or a balance structure.
- Process: ordered nodes connected with directional lines.
- Cause/effect: clear origin, connector, and consequence zones.
- Hierarchy: nested frames, tiers, or a tree.
- Matrix: a real table or CSS grid with clear row and column labels.
- Practice: one task, required materials, and response instruction.
- Summary: convergence, checklist, or final judgment.

Use CSS custom properties for theme tokens. Prefer system font stacks that include Microsoft JhengHei for Taiwan Traditional Chinese:

```css
font-family: "Microsoft JhengHei", "PingFang TC", "Noto Sans TC", system-ui, sans-serif;
```

Do not fetch a remote font. Keep audience-facing text large enough for projection. Shorten or split content before shrinking it excessively.

## Dense Teaching Content

When a slide needs a matrix, comparison table, responsibility board, or multi-stage process, preserve projection readability before preserving every source sentence.

- At the 1600 × 900 design stage, target 24–28 px for primary cell text and 18–21 px for secondary cues.
- Keep each cell to one main statement plus at most one necessary cue.
- Replace repeated prose with parallel keywords, short labels, or slash-separated contrasts.
- Use stable headers, row labels, restrained cell shading, and one accent column to make scanning order obvious.
- If the text still does not fit, remove speaker-level explanation or split the relationship across slides. Do not solve density by shrinking audience-facing text.
- Recheck the actual rendered slide at 1280 × 720; CSS pixel values alone do not prove projection readability.

## Progressive Reveal

Use progressive reveal only when the user requests sequential appearance or the teaching task requires controlled attention. Keep layout space reserved so revealing content does not shift the table or diagram.

Use `.fragment` on each row, card, decision, or conclusion that should appear in sequence. The template supports `.fragment`, `.is-revealed`, and `[data-step]`.

Plan the order explicitly:

1. Keep the slide title, learner task, and table header visible.
2. Reveal table rows or concept groups in teaching order.
3. Reveal decisions or checks after the evidence they depend on.
4. Reveal the core judgment last.

Forward navigation must reveal the next fragment before changing slides. Backward navigation must hide the previous fragment before leaving the slide. When moving back to a completed slide, show its full state. Display the reveal count as `current / total` beside the page number.

In print CSS, force every fragment to `opacity: 1`, `visibility: visible`, and `transform: none`. Do not print partial teaching states.

## Interaction and Motion

Keep these controls functional:

- ArrowRight, PageDown, or Space: next fragment, then next slide
- ArrowLeft or PageUp: previous fragment, then previous slide
- Home: first slide
- End: last slide
- URL hash: deep link to a slide by `data-slide-id`
- Fullscreen button: enter or exit fullscreen
- Visible current/total status and progress bar

Do not capture keyboard events while focus is inside a link, button, input, textarea, select, or editable element.

Use one restrained transition family across the deck. Honor `prefers-reduced-motion: reduce`. Do not add autoplay, sound, decorative fragments, or timers unless requested.

## Images and Diagrams

Prefer editable DOM structures:

- CSS Grid or Flexbox for grouping and comparison
- Borders, backgrounds, and pseudo-elements for frames and signals
- Inline SVG for arrows, paths, cycles, timelines, or simple diagrams
- Native tables for real tabular relationships

Add a raster image only when it materially improves understanding or the user requests one. Store it locally, add meaningful alt text, and verify that the file exists. Do not put essential Traditional Chinese teaching text inside a generated image when it can remain native HTML.

## Preview and Verification

1. Run the validator:

   ```powershell
   node scripts/validate_html_deck.mjs <deck-folder>
   ```

2. Serve the folder with an available local static server when browser preview is needed. Do not require the user to keep a server running for ordinary playback.
3. Inspect at 1280×720 and 1920×1080.
4. Verify slide count, order, titles, labels, and final judgments against the approved plan.
5. Test all navigation keys, hash deep links, fullscreen control, status, and progress.
6. When fragments exist, test initial `0 / total`, first reveal without page change, page advance after the final reveal, backward reveal state, and full print visibility.
7. Inspect for clipping, overlap, tiny type, broken diagrams, missing assets, and unintended scrollbars.
8. Open print preview and confirm one slide per page with navigation hidden.
9. Confirm the deck works with the network disconnected.

Treat validator warnings as review prompts. Fix all errors before delivery.

## Delivery

Deliver the complete folder and link directly to `index.html`. State the selected style family and whether any images were used. Report browser-specific behavior or an untested print/PDF path honestly.
