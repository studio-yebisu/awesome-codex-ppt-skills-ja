# Agent Instructions

You are working with the **ai-slide-templates** library by Cogine AI.

This repository is a template library for AI-assisted slide generation. Each template is a self-contained HTML deck with metadata:

```txt
templates/
  <slug>/
    template.html
    template.json
```

Your job, when the user asks for a deck, is to use this library to produce a finished, browser-openable HTML slide deck from the user's real content.

These instructions are a protocol, not a rigid script. Choose the lightest workflow that fits the user's request.

When the user's input is a long script, article, transcript, or scattered raw material, first synthesize a slide outline before choosing or building the final deck. Use `INPUT_GUIDE.md` as the user-facing reference for what input to request and how to structure briefs.

---

## Operating Modes

### 1. Direct Mode

Use this when the user has already chosen a template, named a style, or given a brief that clearly maps to one template.

Do this:

1. Read the chosen template's `template.json` and `template.html`.
2. Consult `layout_slots`, when present, to identify the fillable structure for each layout before editing HTML.
3. Clone the full template folder into the user's output workspace.
4. Replace placeholder content with the user's real content.
5. Preserve the template's design system.
6. Open the finished HTML deck in the browser and give the user the absolute file path.

Do **not** force a multi-option selection step when the user already knows what they want.

### 2. Selection Mode

Use this when the user gives a deck topic or content but has not chosen a visual direction.

Read every `templates/*/template.json`. Filter and score candidates in this order:

1. Start with explicit user constraints: `scheme`, audience and `formality`, and `occasion`. If the user clearly asks for a dark deck, board-level formality, investor pitch, classroom handout, or similar constraint, reject or strongly demote templates that clash with it.
2. Check content volume, `density`, `content_limits`, and `layouts`. Low-density templates work best for concise narratives with one idea per slide. Medium- and high-density templates can carry more bullets, tables, charts, or operational detail. When the user's content is heavier than the selected template can comfortably hold, split it across more slides by duplicating the closest matching layout instead of cramming text into one slide. If the brief depends on timelines, comparison tables, chart-heavy reviews, or portfolio grids, prefer candidates with layout vocabulary that naturally supports that structure.
3. Compare `best_for` and `avoid_for`. Prefer templates whose `best_for` matches the deck's core job. Treat `avoid_for` as a warning signal and demote templates when the warning matches the user's brief.
4. Use `mood` and `tone` to break ties and align the recommendation with the desired emotional feel and presentation voice.
5. Use Preview Mode when confidence is low.

Then recommend the best fit. If several genuinely plausible directions remain, show a short list of alternatives. Usually show two to four preview candidates when visual taste is uncertain, the top candidates differ mainly by mood or density, the choice is high-stakes, or the user has not given enough constraints to choose confidently. Do not pad the list to a fixed size.

Ask clarifying questions only when they would change the template choice, slide structure, or density decision. Prefer concise questions about occasion, audience, mood, density, and light/dark preference.

### 3. Preview Mode

Use this when visual taste is uncertain, the user asks to compare options, or the choice is high-stakes.

Use the preview tooling instead of hand-building one-off preview files:

```sh
node scripts/preview.mjs --title "<deck title>" --subtitle "<short context>" <slug...>
```

This writes standalone first-slide previews to `previews/<slug>-preview.html`. Use multiple slugs in one command when comparing candidates, either as separate arguments or comma-separated values.

When the user needs visual comparison artifacts, render screenshots from the generated preview files:

```sh
node scripts/screenshot.mjs previews/<slug>-preview.html
```

If screenshot dependencies are not installed yet, run:

```sh
npm install
npx playwright install chromium
```

Open the generated preview HTML files or screenshots in the browser and send the absolute file paths.

Preview files are for choosing a direction. Once the user chooses, build the full deck in that template.

### 4. Maintenance Mode

Use this when the user asks to add templates, edit metadata, change validation, reorganize the repository, or publish the library.

Do not run the deck-building workflow. Work on the library directly, keep changes scoped, and run the relevant validation.

---

## Template Metadata

`template.json` is the metadata source of truth. Do not depend on a hand-maintained central index. If a generated catalog exists later, treat it as a cache and fall back to per-template metadata when in doubt.

The metadata shape is documented in `schema/template.schema.json`. Use that schema when adding or editing templates, but still treat the real `template.html` as the authority for visual details such as exact fonts, colors, layouts, and navigation behavior.

Key fields:

| field | how to use it |
|---|---|
| `mood` | Emotional feel: confident, calm, playful, editorial, etc. |
| `tone` | Presentation voice: bold, polished, warm, technical, literary, etc. |
| `occasion` | Example use cases. Use as a soft signal, not a hard industry filter. |
| `formality` | Audience fit: low through high. |
| `density` | How much content each slide can comfortably carry. |
| `scheme` | Light, dark, or mixed. Treat as important when the user specifies it. |
| `best_for` | Strongest match signal for what the template is good at. |
| `avoid_for` | Soft warning about tone clashes. |
| `content_limits` | Machine-readable capacity guidance: title/subtitle/body character limits, bullet/card counts, and recommended slide-count range. |
| `layouts` | Available layout vocabulary in the template. |
| `layout_slots` | Optional map from each layout name to fillable slots. Use this before editing HTML so replacements are deliberate and layout-safe. |
| `slide_count` | Number of demo slides and layout examples. |

Templates have tones, not industries. A template designed for one business context can work for another if the user's desired mood fits.

---

## Design System Contract

When adapting a template, preserve the visual system. These are part of the template identity:

- Fonts and imported font families.
- Font choices are template-specific. Do not normalize the library to one common font stack; distinctive display, serif, mono, condensed, rounded, or decorative fonts are part of the source-inspired style.
- Color palette, including `:root` variables and hard-coded accent colors.
- Layout grid, spacing rhythm, and major positioning rules.
- Slide-level CSS classes and component structures.
- Decorative vocabulary: shapes, borders, ornaments, paper texture, illustrations, icon style.
- Navigation/runtime behavior: inline keyboard handler, buttons, scroll-snap, progress bar, etc.

Replace the content, not the design system.

Always replace:

- Headlines and section labels.
- Body copy, bullets, captions, and quotes.
- Numbers, charts, tables, and stats.
- Names, dates, company names, attribution lines.
- Image placeholders, while keeping the same frame and visual treatment.

Do not recolor, substitute fonts, modernize the style, strip decoration, or combine slides from different templates.

When adding a new source-inspired template, follow the source typography as closely as practical. If the exact source font is proprietary or unavailable for portable HTML, use a visually close web-available font or system fallback and make `template.json.typography` describe the actual implemented font, not an unavailable one.

---

## Building The Deck

After selecting a template:

1. Clone the chosen template folder into the user's output location.
2. Read `layout_slots` for the chosen layout, when available, and map the user's content into those named slots before touching markup.
3. Check `template.json.content_limits` when present. If the user's content exceeds the title, subtitle, body, bullet, card, or slide-count limits, split the material across additional slides instead of shrinking the design system or overfilling a layout.
4. Adapt `template.html` slide by slide.
5. If the user needs fewer slides, remove unnecessary slides and update counters.
6. If the user needs more slides, duplicate the closest matching layout and replace the content.
7. If the template lacks a needed layout, design a new slide using the same design system.

For new layouts, match the template's fonts, palette, spacing, component grammar, decorations, chrome, and navigation. The new slide should look native when placed between existing slides.

Do not switch templates mid-deck just because one layout is missing.

---

## Output And Verification

For final decks:

1. Open the finished `template.html` in the browser.
2. Visually check that the deck renders, navigation works, and content does not obviously overflow.
3. Send the user the absolute file path.
4. Briefly state which template you used and why it matched the requested tone.
5. Mention any caveats, such as custom layouts you added.

For previews or intermediate artifacts, also open the files and send their absolute paths.

Keep the final response focused on the artifact, the path, and any important caveat. Do not narrate every step.

---

## Library Maintenance Checks

When maintaining this repository, run:

```sh
node scripts/validate.mjs
```

When changing validation logic, also run:

```sh
node scripts/validate.test.mjs
```
