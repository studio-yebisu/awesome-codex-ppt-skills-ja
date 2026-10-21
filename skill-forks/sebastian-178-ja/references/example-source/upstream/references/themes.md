# Theme Guide

Themes are token files. They should not contain layout rules or component CSS.

## Available Themes

- `assets/themes/blue.css`: blue accent system.
- `assets/themes/red.css`: red accent system.
- `assets/themes/green.css`: green accent system.
- `assets/themes/mono.css`: black-and-white system.
- `assets/themes/pitch.css`: investor, board, fundraising, and VC-style pitch decks.
- `assets/themes/classic.css`: compatibility alias for the default blue token set.

## Light And Dark Modes

Each theme defines both light and dark tokens:

- Light mode: default `.slide`.
- Dark mode: `.slide.dark` or `.slide[data-mode="dark"]`.
- Dark cover: `.slide.dark-cover` or `.slide[data-variant="dark-cover"]`; these selectors automatically apply dark text, muted, line, panel, and accent tokens.

Never put a dark background on a slide, region, split panel, or custom block without also activating the matching dark token context. Use `.dark`, `[data-mode="dark"]`, `.dark-cover`, or `[data-variant="dark-cover"]` instead of only changing `background`. This prevents dark text from appearing on dark backgrounds across blue, red, green, mono, and custom themes.

Use one theme file per deck. Do not mix theme files in one production deck unless the user explicitly wants a theme comparison.

Honor explicit tone requests across the whole deck: dark means consistently dark token contexts, light means consistently light pages, and mixed pacing is used only when the user asks for it or provides a clearly mixed reference. If the user does not specify a style, keep one dominant tone across the deck. Default ordinary analytical body pages to light or neutral mode because they carry tables, charts, comparisons, and executive reading. Use dark mode only for the cover, closing, deliberate section dividers, or a few high-emphasis story moments. Do not alternate dark and light body slides only for visual variety.

For pitch-style decks, use `assets/themes/pitch.css` rather than recreating pitch colors inline. Treat pitch as a cohesive token set, not a mandate to mix dark and light pages throughout the deck. Prefer a dark cover plus light analytical body pages unless the user explicitly asks for a dark pitch deck or the page is a deliberate divider/emphasis moment. Any dark page must pass `scripts/check-deck-contrast.sh path/to/deck.html`. The runtime can auto-apply dark text tokens to a slide-level dark background, but it cannot reliably infer the intent of every custom nested panel, gradient, or image overlay.

## Token Rules

- Put colors only in `assets/themes/*.css`.
- Put layout structure in `assets/css/layouts.css`.
- Put reusable content components in `assets/css/components.css`.
- Put neutral illustration styling and asset slots in `assets/css/illustrations.css`.
- Put optional static images, SVGs, screenshots, and headshots in `assets/media/`.

## Required Theme Tokens

Every theme must define the same token contract so components can stay color-neutral:

- Accent tokens: `--theme-accent`, `--theme-accent-soft`, `--theme-accent-strong`.
- State tokens: `--theme-success`, `--theme-danger`.
- Dark-mode tokens: `--theme-dark-bg`, `--theme-dark-accent`, `--theme-dark-bg-gradient`.
- Data tokens: `--chart-series-1` through `--chart-series-5`, plus `--chart-highlight`.
- Part-to-whole tokens: `--part-1-color` through `--part-4-color`.
- Diverging heat tokens: `--heat-neg-3`, `--heat-neg-2`, `--heat-neg-1`, `--heat-zero`, `--heat-pos-1`, `--heat-pos-2`, `--heat-pos-3`.

If a new component needs color, add a semantic token to all themes rather than hardcoding the color in component CSS.

## Font Stack

`assets/css/fonts.css` is bilingual by default:

- Latin sans: Inter.
- Latin serif: Libre Baskerville.
- Simplified Chinese sans fallback: Noto Sans SC plus system CJK sans fonts.
- Simplified Chinese serif fallback: Noto Serif SC plus system CJK serif fonts.

Use `--font-sans` and `--font-serif` in layouts/components. Use `--font-cjk-sans` or `--font-cjk-serif` only when a page intentionally needs a CJK-specific override.

Source decks load predownloaded Google Latin fonts through this shared file for browser preview. `scripts/render.sh --package` inlines those local font files so delivered packages do not depend on remote font services. Full CJK webfont binaries are intentionally not vendored by default because they add tens of megabytes; CJK text uses the system fallback stack.
