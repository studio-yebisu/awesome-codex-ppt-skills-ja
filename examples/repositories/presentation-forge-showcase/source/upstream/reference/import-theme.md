# Importing a theme

Reproduce a brand's graphic charter as a reusable Presentation Forge theme under
`themes/<name>/`. Capture four things and apply them faithfully:

1. the **palette** (real colours),
2. the **real fonts** (downloaded and embedded, not a system fallback),
3. the **logo**,
4. the **visual signature** (the layout: title placement, bands, rules, footer).

The reference can be a PowerPoint, image(s), a text description, or a combination,
plus an optional company logo. Handle whatever the user provides; if a logo or a
font file is needed but missing, ask for it.

It can also be a **saved style file** (`.pfstyle.json`) the user got from a
previous session. That is the fast, exact path: skip straight to *Reuse a saved
style file* below and you are done in one step.

`<skill-dir>` below is this skill's folder (where `SKILL.md` lives); `template/`
and `scripts/` are inside it.

## Reuse a saved style file (fastest, exact)

If the user provides a `.pfstyle.json`, do not reproduce anything: it already
contains the complete theme (CSS, fonts, logo, backgrounds), byte for byte.
Rebuild it into the deck and use it as-is:

```sh
python3 "<skill-dir>/scripts/theme_bundle.py" unpack <file.pfstyle.json> \
    "<deck>/themes"
```

It recreates `<deck>/themes/<name>/` exactly and prints the theme name and a
summary. Set `"theme": "<name>"` in `deck.config.json`, build, and you are done -
no images or PowerPoint needed. To reproduce a style from scratch instead,
continue with the steps below; either way, finish with *Export the style for
reuse*.

## Step 1 - Derive the design language

### From a PowerPoint (`.pptx`)

```sh
python3 "<skill-dir>/scripts/pptx_theme.py" <file.pptx> --dump-media /tmp/pptx-media
```

JSON fields:
- `palette` - theme colours (`dk1`, `lt1`, `dk2`, `lt2`, `accent1..6`, `hlink`),
- `fonts` - `major` (headings) and `minor` (body),
- `suggested_tokens` - a first colour mapping,
- `master` - **layout signal**: `background`, `title_box` and `body_box`
  (`{x,y,w,h}` in px at the deck's slide size), `title_pt` / `body_pt` default
  font sizes. Use this to reproduce placement and proportions (Step 6).
- `slide_size_px`, `media` (dumped for inspection).

### From image(s)

Sample the real colours instead of guessing:

```sh
python3 "<skill-dir>/scripts/image_colors.py" <image> --colors 6
```

It prints the dominant colours (`hex`, `share`, `hsv`) and a `suggested_tokens`
(`bg` / `ink` / `accent`). Then also **view** the image for what colours can't
tell you: the typography (serif vs sans, weight, character) and the layout
signature (title placement, a colour band, hairline rules, a footer, the bullet
style).

### From a text description

Translate brand words into tokens: mood -> light/dark `--bg`/`--ink`; brand colour
-> `--accent`; "modern geometric sans" / "classic serif" -> font families;
"airy/minimal" -> larger spacing. State what you inferred.

## Step 2 - Create the theme folder

Create a deck with `scripts/new_deck.py` if there isn't one yet, then copy the
base theme:

```sh
cp -R "<deck>/themes/ink-blue" "<deck>/themes/<name>"
```

This keeps the class/token contract; you override the look. Name `<name>` after
the brand (kebab-case). The engine's components (stats, bars, steps, timeline,
compare, grid, icons) already follow the tokens; restyle them in `slides.css`
only if the brand calls for it (`themes/obsidian/slides.css` ends with an
example).

## Step 3 - Map the palette into `themes/<name>/tokens.css`

| Token           | Set from                                        |
| --------------- | ----------------------------------------------- |
| `--bg`          | main background (pptx `lt1`, image `bg`)        |
| `--bg-soft`     | a near-background tint (pptx `lt2`)             |
| `--ink`         | body text (pptx `dk1`, image `ink`)            |
| `--accent`      | the brand colour (pptx `accent1`, image `accent`) |
| `--accent-deep` | a darkened accent or near-black (pptx `dk2`)   |
| `--accent-soft` | a lighter accent                                |
| `--accent-tint` | a very light accent, ~8-12% alpha (`#RRGGBB14`) |
| `--muted`       | a mid grey                                       |
| `--rule`        | `--ink` at low alpha (hairlines)                |

Set the **type scale** too if the master tells you (`title_pt` / `body_pt`): the
tokens `--type-display`, `--type-title`, `--type-body` etc. are the dials. Scale
the master's point sizes to the 1920x1080 canvas if the source slide size differs.

## Step 4 - Use the brand's real fonts

A fallback system font is the biggest fidelity loss, so fetch the real face when
it is free:

```sh
python3 "<skill-dir>/scripts/fetch_font.py" "<Family>" --weights 400,700 \
    --out "<deck>/themes/<name>/fonts"
```

It downloads the `.woff2` (latin + latin-ext, so French accents render) and prints
`@font-face` rules. Paste those into `themes/<name>/fonts.css`, then point the
token at the family in `tokens.css` (e.g. `--font-sans: "<Family>", system-ui,
sans-serif;`). Fetch both the heading and body families.

If the script reports the family is **not on Google Fonts** (a commercial or
custom face): ask the user for the `.woff2` files (drop them in `fonts/` and write
the `@font-face` by hand), or choose the closest free alternative and say so.
Network is available in Claude Code; in a restricted sandbox the fetch may fail -
fall back to the same options.

## Step 5 - Integrate the logo

Place the logo in `themes/<name>/logos/` (prefer transparent PNG or SVG), then
wire it into `slides.css` with `url(logos/<file>)` (the build inlines it):

- small corner logo on every slide via a `.slide` background-image, kept clear of
  the content (`background-position: right 48px top 40px; background-size: 160px`);
- or larger on `.slide--title` only; or in a `.footer`.

Mind legibility: modest size, clear of text; on dark variants (`slide--section`)
use a light/monochrome logo or suppress it (`.slide--section{background-image:none}`).
Pick the real brand mark from the pptx media; discard sample screenshots/icons.

## Step 6 - Reproduce the visual signature (slides.css)

Colours, fonts and a logo get you "on brand". Matching the **layout** is what makes
it look like the real charter. Adapt `themes/<name>/slides.css` to echo the
reference's signature, for example:

- **title placement and size** - from the master `title_box` (position) and
  `title_pt` (size), or from the image. Move/scale `.title` / `.display`
  accordingly;
- **a brand colour band or sidebar** - a coloured strip behind the title or down
  one edge;
- **hairline rules / underlines** - an accent rule under the title or in the
  footer;
- **a footer** - logo, a short brand line, a slide number, using `.footer`;
- **section dividers** - how `slide--section` looks (full-bleed brand colour,
  large number, etc.);
- **bullet markers** - the shape/colour of `ul.bullets` markers;
- **backgrounds** - if the master/reference has a background fill or texture, set
  it on `.slide` (or just `slide--title` / `slide--section`); put image textures in
  `themes/<name>/images/` and keep contrast high enough to read.

**Preserve the contract.** Keep every class (`.slide`, `.title`, `.bullets`,
`.two-col`, `.card`, `slide--title/section/conclude`, ...) and every token name.
You are restyling them, not renaming them, so any deck still builds. Translate the
master's px boxes proportionally to the 1920x1080 canvas (multiply by
`1920 / pptx_slide_width`).

**Never set engine-owned layout properties on `.slide` itself.** The engine
absolutely-positions every slide to stack and scale them, so a theme must not set
`position`, `top` / `right` / `bottom` / `left`, `transform`, `width` / `height`,
`visibility` or `opacity` on `.slide` (or `.slide--*`). Doing so breaks the layout
of the entire deck. To anchor a logo, footer, page number, or colour band inside a
slide, you do **not** need `position: relative` on `.slide` - it is already a
positioned box, so just give the child `position: absolute` and it anchors to the
slide. Style padding, colours, fonts, backgrounds and the slide's inner blocks,
not the slide's own placement in the canvas.

**Motion belongs to the deck's level.** If the brand's look includes movement (a
drifting background, a rule that draws in), scope it so the level controls it:
ambient loops get `animation-play-state: var(--pf-loops, paused)` (they run from
`lively` up), and entrance effects key on `.pf-canvas:not([data-dir="prev"]) >
.slide[data-active]` (forward arrivals only). `themes/obsidian/slides.css` does
both; the `none` level stops everything by itself.

Trade-off to state to the user: a strong visual signature makes this theme
specific to the brand (less of a neutral drop-in). That is the right call for a
faithful charter; note it so they know why it looks less generic than `ink-blue`.

## Step 7 - Activate, verify against the reference, report

1. Set `"theme": "<name>"` in `deck.config.json` and `python3 build.py`.
2. Render and **compare side by side with the reference**: a title slide, a
   content slide, and a `slide--section`. Get images of them with:
   ```sh
   python3 "<skill-dir>/scripts/check_deck.py" "<deck>" --slides 1,2,3 --scale 1
   ```
   Look at the title position/size, colours, fonts (are the real faces loading?),
   logo placement, and overall feel. Tune `tokens.css` and `slides.css` and rebuild
   until it matches and text stays legible.
3. **Report** the colours and fonts used (and whether each font was fetched or
   substituted), where the logo sits, what layout signatures you reproduced, and
   any assumptions, so the user can correct them.

## Step 8 - Export the style for reuse (always)

Whenever you reproduce or build a theme, package it into a single portable style
file and give it to the user, so they never have to refurnish the image, the
PowerPoint, or the description again:

```sh
python3 "<skill-dir>/scripts/theme_bundle.py" pack "<deck>/themes/<name>" \
    -o "<name>.pfstyle.json"
```

This writes one `<name>.pfstyle.json` that contains the **entire** theme byte for
byte: `tokens.css`, `slides.css`, `fonts.css`, the `.woff2` font files, the logo,
and any backgrounds, plus a readable summary. Nothing is lost.

Hand that file to the user and tell them: in any future conversation, attaching
this one file is enough to recreate the exact same style (see *Reuse a saved style
file*) - no images or PowerPoint needed.

## Notes

- Keep the class/token contract intact so the new theme works with any deck.
- For a `.pptx`, this reads the theme + master design, not the content of sample
  slides.
- Clean up any `/tmp/pptx-media` you created.
