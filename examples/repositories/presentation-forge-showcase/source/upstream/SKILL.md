---
name: presentation-forge
description: >-
  Build beautiful, self-contained HTML presentations (slide decks) with the
  bundled Presentation Forge engine: one HTML file per slide, bundled into a
  single portable index.html with presenter mode, progressive reveal, and
  swappable themes, plus built-in animations (five motion levels), charts,
  figures and icons. Use this whenever the user wants to create, design, write, or
  build a presentation, slide deck, talk, or "slides" as HTML or for the browser;
  wants a web-based or single-file shareable deck; wants to turn a topic, brief,
  outline, notes, or a document into slides (technical talks AND any other
  subject); or wants to recreate a brand/PowerPoint look as a reusable theme, from
  a .pptx, from image(s), or from a text description, optionally integrating a
  company logo. Produces HTML decks, not native PowerPoint files.
---

# Presentation Forge

Presentation Forge turns plain HTML into polished presentations. You write **one
HTML file per slide**; a tiny Python build step (`build.py`, standard library
only) bundles the slides, the engine, the chosen theme and all images into a
single **self-contained `index.html`** that opens by double-click, emails
cleanly, and works offline.

Everything needed ships **inside this skill**, so it works the same in Claude
Code, in the Claude apps, and via the API - anywhere Claude has a filesystem and
can run Python.

Three layers, always kept separate:

- **engine** (`template/engine/`) - rendering logic: scaling, navigation,
  presenter mode, progressive reveal. **Don't edit it** to change content or look.
- **theme** (`template/themes/<name>/`) - the look: colours, type, spacing, fonts,
  logos, backgrounds. Swap themes without touching slides.
- **content** (`slides/`) - the slides, one file each, ordered by name.

This skill supports two workflows, chosen from what the user asks:

1. **Create a presentation** - author a deck from a topic or brief.
2. **Import a theme** - build a reusable theme from a `.pptx`, image(s), or a
   description, with optional logo integration. See
   [`reference/import-theme.md`](reference/import-theme.md) for the full procedure.

## Where the engine lives

This skill bundles the deck scaffold in **`template/`**, a sibling of this
`SKILL.md`: `engine/` (with the animation toolkit, the components and the icons),
`themes/` (the dark `obsidian` and the light `ink-blue`), an empty `slides/`,
`assets/`, `build.py` and `deck.config.json`. The scripts are in `scripts/`.

Resolve the skill's own directory first (it's wherever this `SKILL.md` was read
from), then treat `template/` and `scripts/` as relative to it:

```sh
SKILL_DIR="$(dirname "$(find . -name SKILL.md -path '*presentation-forge*' 2>/dev/null | head -1)")"
# or just use the directory you read this SKILL.md from
```

In Claude Code the skill folder is known directly; in the Claude apps / API the
skill is unzipped into the working filesystem - in both cases `template/` sits
next to `SKILL.md`. Use `python` instead of `python3` wherever that is what
resolves on this machine (common on Windows).

## Workflow 1 - Create a presentation

**The user decides what the deck says.** They describe their talk - topic, points,
notes, a document - when they start the conversation. Build from that; don't
quiz them about content. If the brief is thin, write a plausible first draft and
flag what you invented so they can correct it.

### Step 1 - Ask two questions, then nothing else

Before writing anything, ask these two together, in the user's language, in one
message (with the `AskUserQuestion` tool when it is available, otherwise a short
message listing the options). Skip a question the user already answered, and
skip both if they said to go straight ahead - then use the defaults.

1. **How should we build it?**
   - **Plan first** (default, recommended) - you propose the outline, they adjust
     it, then you write the whole deck.
   - **All at once** - you write the whole deck in one go.
   - **Slide by slide** - you write one slide, they review it, then the next.
2. **How much animation?**
   - **None** - perfectly still.
   - **Subtle** - soft fades, nothing distracting.
   - **Balanced** (default) - polished entrances, counting figures, reveals.
   - **Lively** - more movement, ambient loops, decorative shapes.
   - **Extra** - the full show: 3D, springy pops, drawn icons, strong loops.

### Step 2 - Create the deck

Pick a target folder (a new kebab-case folder named after the topic in the
current working directory, unless the user named one) and create it empty:

```sh
python3 "$SKILL_DIR/scripts/new_deck.py" "<target>" --title "<title>" \
    --lang <en|fr|…> --theme <obsidian|ink-blue|…> --motion <level>
```

The deck starts with **no slides**: everything in it comes from this user's brief.
Never build inside the skill's `template/`.

### Step 3 - Plan the deck from the brief

Fix the **one core message**, the **audience** and an **arc** that follows what
the user wants to say (see [`reference/writing-decks.md`](reference/writing-decks.md)).
For each slide choose its shape from [`reference/layouts.md`](reference/layouts.md):
a figure, a chart, a process, a comparison, bullets… The only fixed slides are
the title and the close; an agenda, section dividers, a quote or a footer appear
only when this content calls for them - not because a deck "usually" has them.

### Step 4 - Write, following the chosen mode

Slides go in `<target>/slides/`, one `<section class="slide">` per file, numbered
`01-`, `02-`, … (see *The slide authoring contract*). Use the components in
[`reference/components.md`](reference/components.md) and the motion in
[`reference/motion.md`](reference/motion.md) - matching the chosen level - rather
than inventing CSS.

- **Plan first** - show the outline: for each slide, its title (a full
  assertion), its shape, and one line on what it shows. Wait for the user's
  answer, apply their changes, then write every slide, build and check (Step 5).
- **All at once** - write every slide, build and check.
- **Slide by slide** - show a short outline once, then for each slide: write it,
  build, check it (`--slides N`), show the user that slide's image and wait for
  their feedback before the next one. Apply what they say to the current slide,
  and carry their preferences forward.

### Step 5 - Build, then look at the result

```sh
python3 build.py                                     # inside <target>
python3 "$SKILL_DIR/scripts/check_deck.py" "<target>"   # add --slides N or all
```

The build must print `Built index.html - N slides` with the count you expect,
with no `!` warnings. `check_deck.py` renders the deck in headless Chrome, lists
layout problems (text past the slide's edge, content cut off, broken images) and
saves a contact sheet of every slide plus an image of each problem slide. **Fix
every reported problem and look at the contact sheet before handing the deck
over.** In slide-by-slide mode, share the slide image with the user when your
environment can show files; otherwise tell them to open `index.html#N`. If no
Chrome / Chromium / Edge is installed, say the visual check was skipped - never
install a browser.

### Step 6 - Hand it over

Report the deck folder, the theme and motion level, anything you invented for a
thin brief, and how to present: arrow keys / Space, `p` presenter mode, `?`
shortcuts. Mention they can fix wording right in the browser (Chrome or Edge, on
the local file) - those edits are kept.

### Changing an existing deck

The user may have edited text in the browser since the last build; those edits
live in `index.html`. **Before touching `slides/`, run `python3 build.py --pull`**:
it copies them back into the slide files, so you work on the latest text (every
build does this too, so a rebuild never loses them). If it reports edits it
could not merge, the edited deck was kept as `index.unmerged-edits.html` - bring
those lines over by hand, then delete that file.

### Write it well, from the start

Treat the writing as the product, not an afterthought. Per slide:

- make the **title a full assertion** that states the point ("Caching cut p99 by
  40%", not "Performance"); the body is only the evidence for it;
- **one idea per slide**, few words, parallel and concrete bullets, no walls of
  text - prose belongs in the notes;
- give almost every content slide **speaker notes** in `<aside class="notes">`:
  the spoken narration and delivery cues the slide does NOT show (not a copy of
  the slide text, not a word-for-word script);
- match the language to the audience; flag specifics you invent for a thin brief.

For the full method (arc, assertion-evidence, tight on-slide text, and exactly
what to put in speaker notes), read
[`reference/writing-decks.md`](reference/writing-decks.md) before writing. It is
what makes the deck and its text excellent rather than merely correct.

## Workflow 2 - Import a theme

Reproduce a brand's charter as a **reusable** theme under
`template/themes/<name>/` (or a deck's `themes/<name>/`): its **palette**, its
**real fonts** (downloaded and embedded, not a system fallback), its **logo**, and
its **visual signature** (layout: title placement, bands, rules, footer). The
reference can be:

- **a saved style file (`.pfstyle.json`)** from a previous session - the exact,
  one-step path: `scripts/theme_bundle.py unpack` rebuilds the whole theme (CSS,
  fonts, logo, backgrounds) byte for byte, with no reproduction needed;
- **a PowerPoint (`.pptx`)** - `scripts/pptx_theme.py` extracts the palette, the
  fonts, the embedded media, and the master's layout geometry (title/body boxes,
  font sizes, background);
- **image(s)** - `scripts/image_colors.py` samples the exact dominant colours;
  view the image for typography and layout;
- **a text description** - brand words mapped to tokens;
- optionally **a company logo** to integrate onto slides.

Real fonts are fetched with `scripts/fetch_font.py` (Google Fonts) when free, with
a fallback to asking for the font files. Whenever you build a theme, **export it**
with `scripts/theme_bundle.py pack` into a single `<name>.pfstyle.json` and give it
to the user: handing back that one file in any future conversation recreates the
exact same style, with no image or PowerPoint needed. The full step-by-step
procedure (colour mapping, font fetching, logo integration, reproducing the layout
in `slides.css`, and packing/unpacking the style file) is in
[`reference/import-theme.md`](reference/import-theme.md). Read it when this
workflow triggers.

## The slide authoring contract

Each file in `slides/` is exactly one slide. Keep markup plain and lean on the
theme's classes - that keeps slides consistent and themes swappable.

```html
<section class="slide">
  <h2 class="title">One clear point per slide.</h2>
  <ul class="bullets">
    <li>One idea per line.</li>
  </ul>
  <aside class="notes">Speaker notes - shown only in presenter mode.</aside>
</section>
```

Slides are authored on a fixed **1920×1080** canvas; the engine scales it to any
screen, so always design against that fixed size.

### Slide variants

| Class                   | Use                               |
| ----------------------- | --------------------------------- |
| `slide`                 | standard content slide            |
| `slide slide--title`    | opening / hero slide              |
| `slide slide--section`  | section divider (dark background) |
| `slide slide--conclude` | closing slide                     |

### Content blocks (from the theme)

`.eyebrow` (kicker) · `.display` (largest heading) · `h1`/`.title`,
`h2`/`.subtitle`, `.lead` · `ul.bullets` · `.two-col` (two-column grid) · `.card`
(callout) · `blockquote` · `pre > code` (escape `< > &`) · `.footer` · `.muted` /
`.accent` (colour helpers) · `aside.notes` (presenter-only notes).

### Components (from the engine)

Figures (`.stats`), bar charts (`.bars`), gauges (`.ring`), processes
(`ol.steps`), timelines (`ol.timeline`), comparison tables (`table.compare`),
columns of cards (`.grid`), 84 line icons (`<i data-icon="rocket">`) and
decorative shapes (`.fx`). They follow the active theme and only the ones a deck
uses are bundled. Markup and limits:
[`reference/components.md`](reference/components.md).

### Motion

Entrances (`data-anim="rise"`), one-after-the-other lists (`data-stagger`),
counting figures (`data-count`), ambient loops (`data-loop`), per-slide
transitions (`data-transition`) - all scaled by the deck's level. What to use at
each level: [`reference/motion.md`](reference/motion.md).

### Progressive reveal

Add `class="fragment"` to any element to reveal it step by step on click (add
`data-anim` to choose the effect, or `data-anim="highlight"` to mark words
instead). Each `→` reveals the next fragment, then advances to the next slide;
the presenter view shows `step 2/3`.

### Images

Put a deck's content images in `assets/` and reference them relative to the deck
root (`<img src="assets/diagram.png">`); `build.py` inlines them as base64. Keep
theme assets (fonts, backgrounds, logos) inside the theme folder.

## Configuration (`deck.config.json`)

`scripts/new_deck.py` writes it; change it any time and rebuild.

| Key              | Default        | Purpose                                                     |
| ---------------- | -------------- | ----------------------------------------------------------- |
| `title`          | `Presentation` | page title                                                  |
| `lang`           | `en`           | document language (`fr`, `en`, …)                           |
| `theme`          | `obsidian`     | which `themes/<name>/` folder to use                        |
| `motion`         | `balanced`     | `none` · `subtle` · `balanced` · `lively` · `extra`         |
| `transition`     | `fade`         | `none` · `fade` · `slide` · `zoom` · `rise` · `blur` · `flip` |
| `width` `height` | `1920` `1080`  | design canvas size                                          |
| `exit_hint`      | English string | toast shown on entering full screen                         |

An optional `deck.css` at the deck's root holds styles for that deck only (a
one-off layout); it loads after the theme. Prefer theme classes and components.

## Theming basics

A theme is a self-contained folder: `tokens.css` (colours, type scale, spacing,
font-family names), `fonts.css` (`@font-face`), `slides.css` (block styling), plus
`fonts/`, `images/`, `logos/`. To make a look, copy `themes/ink-blue/` to
`themes/<name>/`, edit `tokens.css`, and set `"theme": "<name>"`. Every theme must
define the same token names and style the same slide classes, so switching a theme
never breaks a deck.

## Reference

- [`reference/writing-decks.md`](reference/writing-decks.md) - how to write the
  presentation and its text well, and what to put in speaker notes. Load it for
  Workflow 1.
- [`reference/layouts.md`](reference/layouts.md) - the shapes a slide can take and
  when each fits. Load it to plan a deck.
- [`reference/components.md`](reference/components.md) - figures, charts,
  processes, timelines, tables, icons, decoration: markup and limits.
- [`reference/motion.md`](reference/motion.md) - the animation toolkit and what to
  use at each motion level.
- [`reference/import-theme.md`](reference/import-theme.md) - full theme-import
  procedure (pptx / image / description / logo). Load it for Workflow 2.
- `template/docs/writing-slides.md` - the deep authoring guide (navigation,
  presenter mode, deeper theming). Load it when you need detail beyond the
  contract above.

## Guardrails

- One `<section class="slide">` per file in `slides/`; the build warns otherwise.
- Don't edit `engine/` to change content or styling - that's the theme's job.
- Don't build inside `template/`; always start a deck with `scripts/new_deck.py`.
- Prefer the theme's classes, the components and the motion toolkit over inline
  styles or custom CSS, so themes stay swappable and the level stays a dial.
- Never hand over a deck without building it and running `check_deck.py` (when a
  browser is available).
- Never `pip install` a package into the system/global Python - it can clobber
  a version another project on the machine relies on. Every script here is
  stdlib-only except `scripts/image_colors.py` (needs Pillow), which already
  handles this: on import failure it installs Pillow into a dedicated venv at
  `~/.cache/presentation-forge/venv` via `scripts/pf_venv.py` and re-execs
  itself there. If a future script needs another package, follow the same
  pattern (`pf_venv.reexec_in_venv("<pypi-name>")`) instead of a bare `pip
  install`.
