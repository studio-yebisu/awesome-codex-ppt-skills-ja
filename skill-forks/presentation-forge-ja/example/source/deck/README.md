# Presentation Forge

Build presentations as clean, readable HTML.

You write one HTML file per slide; a small build step bundles them with the
engine, the theme and your images into a single self-contained `index.html` you
can double-click, email, or host anywhere. No framework, no dependencies.

*[Version française](README.fr.md)*

## Structure

```
presentation-forge/
├── engine/              # the presentation logic - don't edit
│   ├── deck-stage.js    #   the engine: a <deck-stage> custom element
│   ├── base.css         #   its mechanics: scaling, controls, presenter UI
│   ├── motion.css       #   the animation toolkit (entrances, loops, transitions)
│   ├── components/      #   charts, figures, timelines… (bundled only if used)
│   └── icons.json       #   line icons for <i data-icon="…"> (Lucide, ISC)
├── themes/              # the looks - one folder per theme, swap freely
│   ├── obsidian/        #   dark, editorial (the default)
│   │   ├── tokens.css   #     the dials: colours, type scale, spacing, fonts
│   │   ├── fonts.css    #     @font-face declarations
│   │   ├── slides.css   #     how blocks are styled (.title, .bullets, variants…)
│   │   ├── fonts/       #     font files            ┐ the look - travels
│   │   ├── images/      #     backgrounds, textures │ with the theme
│   │   └── logos/       #     logos                 ┘
│   └── ink-blue/        #   clean, light alternative
├── slides/              # your content - one file per slide, ordered by name
│   ├── 01-title.html    #   (a new deck starts empty: these are yours to write)
│   └── …
├── assets/              # content images for THIS deck (kept apart from themes)
├── deck.config.json     # title, language, theme, transition, motion level
├── deck.css             # optional: styles for this deck only
├── build.py             # bundles everything into one self-contained index.html
├── index.html           # the build output - open & share THIS file
└── README.md
```

Three clear layers: **logic** (`engine/`), **look** (`themes/`), **content**
(`slides/`). A theme is a self-contained folder (styles + its fonts, backgrounds
and logos); switching the `theme` in `deck.config.json` restyles the whole deck
without touching a single slide, because every theme honours the same set of
tokens and slide classes.

## Workflow

```sh
# 1. Edit slides in slides/ (one <section class="slide"> per file).
# 2. Build the deck (on Windows, use "python" instead of "python3" if that's
#    what's on your PATH):
python3 build.py            # -> index.html (self-contained)
# 3. Open or share index.html - it's a single file with everything inside,
#    images included, so it works by double-click and offline.
```

While editing, rebuild on every save and refresh the browser:

```sh
python3 build.py --watch
python3 build.py --open     # build, then open it in the browser
```

Text fixed straight in the browser (the Edit button, in Chrome or Edge on the
local file) is saved into `index.html`; the next build copies it back into
`slides/` first, so a rebuild never loses it. `python3 build.py --pull` does
only that copy.

Move through the slides with the arrow keys or Space.

## Writing a slide

Each file in `slides/` is one `<section class="slide">`:

```html
<section class="slide">
  <h2 class="title">Your point here.</h2>
  <ul class="bullets">
    <li>One idea per line.</li>
  </ul>
  <aside class="notes">Notes - visible only in presenter mode.</aside>
</section>
```

Slide variants: `slide--title`, `slide--section`, `slide--conclude`.
Content blocks from the theme: `eyebrow`, `display`, `title`, `lead`, `muted`,
`accent`, `bullets`, `two-col`, `card`, `blockquote`, `pre > code`.
Components from the engine: `stats`, `bars`, `ring`, `steps`, `timeline`,
`compare`, `grid`, icons (`<i data-icon="rocket"></i>`) and `fx` decoration.
Motion: `data-anim`, `data-stagger`, `data-count`, `data-loop`,
`data-transition`, scaled by `"motion"` in `deck.config.json` (`none` to
`extra`).

Slides display in **filename order** (`01-`, `02-`…); to add one, drop a new
file in `slides/`. See [docs/writing-slides.md](docs/writing-slides.md) for the
full guide.

## Presenting

- **Progressive reveal** - add `class="fragment"` to an element to reveal it
  step by step on click (the presenter view shows `step 2/3`).
- **Full screen** - the ⤢ button or `f`.
- **Presenter mode** - the screen button or `p`: opens an audience window
  (full-screen slide) and a presenter view here with the next-slide preview,
  speaker notes, a wall clock and timers, drawing and a laser pointer.
- **Overview** - `o` shows every slide as a grid; `b` / `w` blanks the screen.
- **Keyboard shortcuts** - press `?` for the full list.

## License

The engine and build tooling are [MIT](LICENSE) © Thomas Gourmelen. The slides you write are yours.
