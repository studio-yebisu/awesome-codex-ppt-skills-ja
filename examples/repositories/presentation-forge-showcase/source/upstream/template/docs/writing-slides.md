# Writing slides

A deck is a folder. You write **one file per slide** in `slides/`, each holding a
single `<section class="slide">` with plain content using classes from the theme.
Everything else - scaling, navigation, the slide counter, and presenter
mode - is handled by the engine.

You never write the `<deck-stage>` wrapper or link the engine/theme by hand:
`build.py` assembles the slides, the engine, the theme and your images into one
self-contained `index.html`.

## One slide = one file

```html
<!-- slides/02-agenda.html -->
<section class="slide">
  <h2 class="title">What this deck shows.</h2>
  <ul class="bullets">
    <li>One idea per line.</li>
  </ul>
  <aside class="notes">Notes - visible only in presenter mode.</aside>
</section>
```

Slides display in **filename order**, so prefix them (`01-`, `02-`, …). To add a
slide, just drop a new file in `slides/`; to reorder, rename.

Slides are authored on a fixed **1920×1080** canvas. The engine scales that
canvas to fit any screen, so you always design against the same fixed size.

## Building & previewing

```sh
python3 build.py            # -> index.html (self-contained)
python3 build.py --watch    # rebuild on every save
python3 build.py --open     # build, then open in the browser
python3 build.py --pull     # only copy text edited in the browser back into slides/
```

Open `index.html` (double-click works - it's a single file with the engine,
theme and images all inlined).

## Slide variants

| Class                    | Use                          |
| ------------------------ | ---------------------------- |
| `slide`                  | standard content slide       |
| `slide slide--title`     | opening / hero slide         |
| `slide slide--section`   | section divider (dark)       |
| `slide slide--conclude`  | closing slide                |

## Content blocks

These classes are provided by the theme:

- `.eyebrow` - small uppercase kicker above a title
- `.display` - the largest heading (title slide)
- `h1` / `.title`, `h2` / `.subtitle`, `.lead` - headings and lead text
- `ul.bullets` - a bulleted list
- `.two-col` - a two-column grid
- `.card` - a boxed callout
- `blockquote` - a pull quote
- `pre` / `code` - code
- `.muted`, `.accent` - text colour helpers

## Charts, figures, icons and motion

The engine also ships ready-made components that follow whatever theme is
active - key figures (`.stats`), bar charts (`.bars`), gauges (`.ring`),
processes (`ol.steps`), timelines (`ol.timeline`), comparison tables
(`table.compare`), columns of cards (`.grid`), line icons
(`<i data-icon="rocket"></i>`) and decorative shapes (`.fx`) - and an animation
toolkit: `data-anim="rise"` to bring an element in, `data-stagger="rise"` on a
list to bring its items in one by one, `data-count` to count a figure up,
`data-loop` for ambient movement, `data-transition` on a slide. `build.py`
bundles only the components a deck uses.

How much it all moves is one setting, `"motion"` in `deck.config.json`: `none`,
`subtle`, `balanced` (default), `lively` or `extra`. The slides don't change;
the engine turns the dial. The full catalogue lives with the skill, in
`reference/components.md` and `reference/motion.md`.

## Progressive reveal (fragments)

Add `class="fragment"` to any element to reveal it step by step on click,
instead of showing the whole slide at once (like Beamer's `\pause`):

```html
<section class="slide">
  <h2 class="title">My points</h2>
  <ul class="bullets">
    <li class="fragment">First point</li>
    <li class="fragment">Second point</li>
    <li class="fragment">Third point</li>
  </ul>
</section>
```

Each press of → reveals the next fragment; once all are shown, → moves to the
next slide. ← hides the last fragment (and going back to a slide shows all of
its fragments). The audience window and the presenter step counter
(`step 2/3`) stay in sync. A slide with no `.fragment` behaves exactly as
before.

Add `data-anim` to pick how a fragment comes in (`data-anim="from-left"`), or
`data-anim="highlight"` to keep it visible and mark it with a highlighter on the
click instead.

## Images

Put images in `assets/` and reference them from a slide with a path relative to
the project root:

```html
<img src="assets/diagram.png" alt="Architecture" />
```

`build.py` inlines them as base64, so the built `index.html` stays a single
portable file.

## Navigating

- **Next / previous:** → · PageDown · Space  /  ← · PageUp (these also step
  through fragments)
- **First / last:** Home · End
- **Jump:** number keys `1`-`9`, or click a slide in the left-hand rail
- **Overview (all slides):** `o`
- **Full screen:** the button or the `f` key (Esc to leave)
- **Presenter mode:** the button or `p`
- **Black / white screen:** `b` / `w` (any key resumes)
- **Shortcuts overlay:** `?`
- **Touch:** swipe left / right, or tap the left / right half of the stage
- The current slide is kept in the URL. Give a slide an `id` (e.g.
  `<section class="slide" id="intro">`) for a stable named link (`#intro`);
  otherwise it's the slide number (`#3`).

## Editing text in the browser

In Chrome, Edge, or another Chromium browser, opening `index.html` straight from
disk (double-click, not a hosted link) shows an **Edit** button top-right. Click
it, pick the deck's `index.html` in the dialog that appears, and grant write
access; existing titles, bullets and paragraphs become editable in place. Saves
happen automatically when you leave a slide or close edit mode, plus a save
button while editing. Speaker notes become editable too, through the same
mechanism, once you've granted access once: one line per paragraph, start a
line with `- ` for a bullet or `1. ` for a numbered item. Notes you don't touch
keep their original HTML exactly.

This only edits existing text - it can't add or remove bullets, slides or
images. The Edit button only appears when saving could actually work: it's
hidden in browsers without the underlying API (Safari, Firefox) and on hosted
copies of a deck (there's no real local file to save over there), so no one
sees a control that wouldn't work for them. Speaker notes stay viewable in
those cases, just not editable.

Edits are saved into `index.html`, and the next `python3 build.py` copies them
back into `slides/*.html` before rebuilding, so nothing typed in the browser is
lost (`python3 build.py --pull` does only that copy). If a slide file also
changed since the last build, its browser edit is not forced in: the edited
deck is kept as `index.unmerged-edits.html` so you can bring the text over by
hand.

## Deck configuration

Set these in `deck.config.json`:

| Key          | Default        | Purpose                                     |
| ------------ | -------------- | ------------------------------------------- |
| `title`      | `Presentation` | the page title                              |
| `lang`       | `en`           | document language                           |
| `theme`      | `obsidian`     | which `themes/<name>/` folder to use        |
| `motion`     | `balanced`     | how much moves: `none` · `subtle` · `balanced` · `lively` · `extra` |
| `transition` | `fade`         | slide transition: `none` · `fade` · `slide` · `zoom` · `rise` · `blur` · `flip` (a slide's own `data-transition` wins) |
| `width` `height` | `1920` `1080` | the design canvas size                  |
| `exit_hint`  | English        | toast text shown when entering full screen  |

For a one-off tweak that belongs to this deck only, add a `deck.css` next to
`deck.config.json`: it loads after the theme.

## Theming

A theme is a self-contained folder under `themes/`, split by concern:

```
themes/obsidian/   # the default theme; a light "ink-blue" theme also ships
├── tokens.css   # the dials: colours, type scale, spacing, font-family names
├── fonts.css    # @font-face declarations
├── slides.css   # how the blocks above are styled
├── fonts/       # font files            ┐ part of the look -
├── images/      # backgrounds, textures │ travels with the theme
└── logos/       # logos                 ┘
```

Keep theme assets (fonts, backgrounds, logos) inside the theme folder, and your
deck's content images in `assets/` - the two never mix.

To make a new look, copy `themes/ink-blue/` to `themes/<name>/`, edit
`tokens.css` (and `slides.css` if needed), and set `"theme": "<name>"` in
`deck.config.json`. Because every theme defines the same tokens and styles the
same slide classes, switching themes never breaks a deck. `build.py` inlines the
theme's stylesheets and assets (base64) into the single-file build.
