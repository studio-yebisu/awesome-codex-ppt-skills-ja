---
name: ai-slide-templates
description: Use the Cogine AI ai-slide-templates repository to help users create polished slide decks from real content. Trigger when the user asks to make slides, a PPT, a presentation deck, an HTML deck, choose a presentation template, use Cogine AI slide templates, or install/use the ai-slide-templates workflow in Codex, OpenClaw, or another agent.
---

# AI Slide Templates

Use this skill to turn a user's real material into a finished, browser-openable HTML slide deck using Cogine AI's `ai-slide-templates` repository.

The repository is the source of truth:

```txt
https://github.com/cogine-ai/ai-slide-templates
```

Always prefer the repository's current `AGENTS.md` over memory or this skill if they disagree.

## Core Workflow

1. Locate or clone the template repository.
2. Read `AGENTS.md` in that repository.
3. Use `INPUT_GUIDE.md` when the user's source material is incomplete, long-form, or scattered.
4. Read template metadata from `templates/*/template.json`.
5. Select the best template for the user's content and audience.
6. Clone the chosen template folder into the user's output workspace.
7. Replace demo content in `template.html` with the user's real content.
8. Open the finished HTML deck in a browser and verify basic rendering.
9. Return the absolute path to the finished `template.html`.

If the agent cannot run shell or browser tools, give the user exact commands and file steps instead of claiming the deck was built.

## Repository Setup

If the current workspace already contains `AGENTS.md`, `README.md`, and `templates/*/template.json` from `ai-slide-templates`, use that checkout.

Otherwise guide the user to clone it:

```sh
git clone https://github.com/cogine-ai/ai-slide-templates.git
cd ai-slide-templates
```

Then read:

```sh
cat AGENTS.md
```

When the user needs help preparing the brief or the input is a long article, script, transcript, memo, report, or scattered notes, also read:

```sh
cat INPUT_GUIDE.md
```

Do not rely on a central template index. Scan per-template metadata:

```sh
find templates -maxdepth 2 -name template.json
```

## Template Selection

Use `template.json` as the matching surface. Compare the user's brief against:

- `mood`
- `tone`
- `occasion`
- `formality`
- `density`
- `scheme`
- `best_for`
- `avoid_for`
- `content_limits`
- `layouts`
- `layout_slots`
- `slide_count`

Templates have tones, not fixed industries. Reuse a template across domains when its mood, content density, and audience fit the user's need.

If the user already picked a template or named a clear style, do not force options. Use that template unless it clearly conflicts with the content.

If the user has not picked a visual direction, recommend the strongest fit. When multiple directions are plausible, show a short list of two to four choices with one-line reasons.

When the source material is longer than the requested slide count, repetitive, or not already organized per slide, synthesize a slide outline before choosing or building the final deck. The outline should include slide titles, key messages, rough visual direction, and any blocking questions.

Use `content_limits` to judge whether a template can carry the user's amount of text, bullets, cards, or slide count. If content exceeds the limits, split it across more slides instead of shrinking fonts, removing whitespace, or overfilling a layout.

Use `layout_slots`, when present, to map the user's content into named fillable regions before editing HTML.

Ask clarifying questions only when the answer changes the template or deck structure. Good questions are about audience, occasion, desired tone, content density, and light/dark preference.

## Deck Assembly

After choosing a template:

1. Copy the full `templates/<slug>/` folder to the output location.
2. Keep the folder's `template.html` and `template.json` together.
3. Read `layout_slots` for the chosen layouts, when available.
4. Check `content_limits`, when available, and split overlong content across additional slides.
5. Edit `template.html` slide by slide.
6. Replace all placeholder titles, body copy, bullets, captions, quotes, names, dates, numbers, charts, stats, tables, and image placeholders.
7. If the user needs fewer slides, remove unneeded slides and update any visible counters.
8. If the user needs more slides, duplicate the closest matching layout and replace the content.
9. If a needed layout is missing, add a new slide that follows the same design system.

Preserve the template's visual identity:

- Fonts and imported font families
- Color palette and CSS variables
- Layout grid, spacing, and major positioning rules
- Slide classes and component structures
- Decorative vocabulary, borders, ornaments, textures, illustrations, and icon style
- Navigation behavior, keyboard handlers, progress bars, and counters

Do not recolor, substitute fonts, strip decoration, merge multiple templates, or redesign the deck unless the user explicitly asks for template maintenance work.

## Preview Mode

Use previews when the user is unsure about visual taste, asks to compare options, or the presentation is high-stakes.

Use the repository preview tooling:

```sh
node scripts/preview.mjs --title "<deck title>" --subtitle "<short context>" <slug...>
```

This writes standalone first-slide previews to `previews/<slug>-preview.html`.

When the user needs screenshot comparison artifacts, render screenshots:

```sh
node scripts/screenshot.mjs previews/<slug>-preview.html
```

If screenshot dependencies are missing, run:

```sh
npm install
npx playwright install chromium
```

Open the generated preview HTML files or screenshots in the browser and send the absolute paths.

After the user chooses a direction, build the full deck from that template only.

## Verification

For final decks, open the generated `template.html` in a browser and check:

- The deck renders without a blank page.
- Navigation works if the template declares navigation.
- Content does not obviously overflow or collide.
- Counters, progress bars, and copied slides still make sense.
- The deck uses the chosen template's visual system.

If the repository's optional visual validator is available and the environment has a compatible browser, use it for higher confidence:

```sh
node scripts/validate-visual.mjs
```

For repository maintenance, run:

```sh
node scripts/validate.mjs
```

If validation logic changed, also run:

```sh
node scripts/validate.test.mjs
```

## Final Response

Keep the response focused:

- State the chosen template and why it matched the user's requested tone.
- Provide the absolute path to the finished `template.html`.
- Mention important caveats, such as custom layouts or missing browser verification.

Do not narrate every implementation step unless the user asked for a walkthrough.
