<p align="center">
  <img src="assets/logo.png" alt="Keynot — Kill PowerPoint with HTML" width="520" />
</p>

<h1 align="center">keynot</h1>

<p align="center">
  <strong>kill powerpoint with html.</strong>
</p>

<p align="center">
  <a href="https://github.com/shawnzam/keynot/stargazers"><img src="https://img.shields.io/github/stars/shawnzam/keynot?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://github.com/shawnzam/keynot/commits/main"><img src="https://img.shields.io/github/last-commit/shawnzam/keynot?style=flat" alt="Last Commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/shawnzam/keynot?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="#what-it-does">What</a> •
  <a href="#install">Install</a> •
  <a href="#how-to-use">How</a> •
  <a href="#whats-in-the-skill">Inside</a> •
  <a href="#when-not-to-use">Caveats</a>
</p>

---

Someone asks you to "put together a few slides" and your hand drifts to the PowerPoint icon out of pure muscle memory. Then come the next twenty minutes of fighting a template you didn't pick, nudging a text box three pixels to the left, and discovering that your brand colors aren't in the theme. None of that is the presentation. None of that is the idea. That's tax you pay for using a tool built in 1987.

**keynot** is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that stops paying it. Ask Claude for "slides" or "a deck" and it ships you a single `.html` file — keyboard nav, swipe, fullscreen, staggered reveals, editorial typography, all wired up. It opens in any browser, runs offline, and weighs less than the email you were going to attach a 40MB `.pptx` to. Hand Claude a brand guide — a PDF, a URL, even a paragraph describing the vibe — and it extracts the palette and type system into CSS variables so the whole deck inherits it. *"Match this brand"* stops being a half-day in Figma and starts being a sentence.

Read the writeup: [**Stop Reaching for PowerPoint**](https://zamechek.com/blog/stop-reaching-for-powerpoint/).

## Live demo

<p align="center">
  <a href="https://shawnzam.github.io/keynot/examples/keynot-for-zombies.html">
    <img src="assets/zombies-preview.png" alt="Live demo: Keynot for Zombies" width="820" />
  </a>
</p>

<p align="center">
  <a href="https://shawnzam.github.io/keynot/examples/keynot-for-zombies.html"><strong>→ Open the live deck</strong></a><br />
  <em>Arrow keys or swipe to navigate · press <code>f</code> for fullscreen</em>
</p>

Generated from a single prompt: *"keynot, but if the audience was zombies, and lean into it."* Everything — nav, fullscreen, animations, typography, all five slides — is one HTML file. [Source](examples/keynot-for-zombies.html).

## What it does

Ask Claude for "slides", "a deck", or "something to present" and keynot activates. You get one HTML file with:

- **Navigation** — arrow keys, space, swipe on touch, clickable dot indicators, auto-hiding nav bar
- **Fullscreen** — `f` key or click the fullscreen button
- **Staggered reveals** — content fades up in sequence on each slide
- **Brand theming** — CSS variables for primary/accent/typography swap in seconds
- **Layout library** — split panels, stat columns, value cards, approach rows, photo panels
- **Embedded assets** — fonts via CDN, images via base64 — one file, no broken links
- **PDF export** — `Cmd+P` → Save as PDF gives one slide per page, backgrounds intact, no extra tooling
- **PPTX export** — ask for PowerPoint and keynot generates a `python-pptx` script you run with `uv run --with python-pptx`

## Install

### Claude Code

keynot is published in the official Claude Code plugin marketplace. Install it with one command:

```
/plugin install keynot@claude-plugins-official
```

The official marketplace is pre-registered — no `marketplace add` step needed. You can also browse it at [claude.com/plugins](https://claude.com/plugins) or run `/plugin` and pick keynot from the **Discover** tab.

<details>
<summary><strong>Self-hosted (pre-marketplace) install</strong></summary>

If you're pinned to an older Claude Code build without the official marketplace, the self-hosted route still works:

```
/plugin marketplace add shawnzam/keynot
/plugin install keynot@keynot-marketplace
```
</details>

### Codex (project-scoped)

Codex reads `AGENTS.md` from the current working directory — there's no global plugin registry. Drop the skill into whatever project you're presenting from:

```bash
mkdir -p your-project/skills/keynot
curl -fsSL https://raw.githubusercontent.com/shawnzam/keynot/main/skills/keynot/SKILL.md \
  -o your-project/skills/keynot/SKILL.md
curl -fsSL https://raw.githubusercontent.com/shawnzam/keynot/main/AGENTS.md \
  -o your-project/AGENTS.md
```

Restart Codex in that directory. The `AGENTS.md` tells it to read the skill when you ask for slides. Repeat for each project where you want keynot available.

### Gemini CLI

```bash
gemini extensions install https://github.com/shawnzam/keynot
```

### Cursor, Windsurf, Cline, or any other agent

```bash
npx skills add shawnzam/keynot -a cursor
npx skills add shawnzam/keynot -a windsurf
npx skills add shawnzam/keynot -a cline
npx skills add shawnzam/keynot -a github-copilot
```

Or install generically (supports 40+ agents):

```bash
npx skills add shawnzam/keynot
```

> **Windows note:** if symlinks fail, add the `--copy` flag.

### Manual drop-in

If none of the above apply, the `SKILL.md` is self-contained markdown. Copy it wherever your agent reads instructions:

```bash
curl -fsSL https://raw.githubusercontent.com/shawnzam/keynot/main/skills/keynot/SKILL.md \
  -o SKILL.md
```

Read it, point your agent at it, and go.

## How to use

Once installed, just ask. One sentence is usually enough — keynot asks follow-ups if it needs them.

```
Make me a 5-slide deck introducing our new product.
Brand guide is attached.
```

```
Turn this doc into slides.
```

```
I need something to present tomorrow on the roadmap. Dark theme, serif headings.
```

```
keynot, but if the audience was zombies, and lean into it.
```

keynot extracts brand parameters (colors, type, layout language), picks a slide sequence that matches your goal, and ships a single `.html` file you can open in any browser. Iterate in plain English: *"slide 3: swap the headline"*, *"make the accent color less aggressive"*, *"add a stat column with these three numbers."* No hunting through a sidebar of 40 objects.

## Exporting to PDF

Every generated deck ships with a `@media print` block that un-stacks absolutely-positioned slides, kills animations, hides the nav bar, and sets `@page` to landscape. Result: open the deck, hit `Cmd+P` (`Ctrl+P` on Windows/Linux), pick "Save as PDF" — you get one slide per page with backgrounds and typography intact. No external tools.

See a generated example: [**keynot-for-zombies.pdf**](examples/keynot-for-zombies.pdf) — the zombies demo deck exported straight from Chrome's print dialog.

**Tip:** enable "Background graphics" in the print dialog if it's off by default, and pick a landscape paper size (or let the browser fit to the `1600 × 1000` `@page` rule). Firefox handles pixel-based `@page size` less reliably than Chrome/Safari — if output looks wrong there, the skill docs include a physical-units fallback.

## Exporting to PPTX

If your audience needs editable PowerPoint files, ask keynot for `.pptx` output. It generates a Python script that builds the deck using `python-pptx`. Run it with:

```bash
uv run --with python-pptx <script>.py
```

No system-wide installs — `uv` handles the dependency inline. See the proof-of-concept: [**keynot-for-zombies-pptx.py**](examples/keynot-for-zombies-pptx.py) → [**keynot-for-zombies.pptx**](examples/keynot-for-zombies.pptx).

**Note:** PPTX output is a solid starting point but not a pixel-perfect replica of the HTML deck. Web fonts fall back to system equivalents (Georgia, Arial), gradients become solid fills, and animations are omitted. Double-check alignment and font rendering in PowerPoint before presenting. If you just need a static handout, [printing to PDF](#exporting-to-pdf) is faster and pixel-perfect.

## Example use cases

- **Investor or pitch decks** — Paste your narrative, drop in a brand guide, get a polished deck in minutes. Iterate in plain English instead of wrestling with slide masters.
- **Conference talks & tech demos** — Single HTML file that opens anywhere, runs offline, and won't embarrass you when the venue wifi dies. Keyboard nav and fullscreen are already wired up.
- **Internal readouts & weekly updates** — Turn a status doc into a skimmable deck so your team actually reads it. Swap content in seconds when numbers change.
- **Client one-pagers** — Match any client's brand from a PDF style guide and deliver something that looks bespoke without opening Figma.
- **Workshop & teaching slides** — Build a course deck with embedded images, staggered reveals, and deep-linkable slide URLs. Students open it in their browser, no installs.
- **Sales leave-behinds** — Ship a self-contained `.html` that prospects can forward internally. No broken fonts, no missing assets, no "please install our viewer."
- **Portfolio & case studies** — Present past work with editorial-quality typography and layouts that match each project's brand.

## What's in the skill

The [`SKILL.md`](skills/keynot/SKILL.md) file walks Claude through:

1. **Brand extraction** — how to parse a style guide (PDF, URL, description) into CSS variables
2. **Deck architecture** — the single-file HTML shell with all navigation and fullscreen wired up
3. **Layout patterns** — split panels, stat columns, value cards, approach rows, tool cards, photo panels
4. **Content sequencing** — a proven 5-slide structure for introductions and pitches
5. **Typography rules** — display, heading, eyebrow, and body tokens with `clamp()` scaling
6. **Iteration workflow** — how to make surgical edits without corrupting JavaScript
7. **Pitfalls** — JS operator corruption from blanket regex, base64 sizing, emoji hygiene
8. **PPTX export** — generating editable PowerPoint decks via `python-pptx` when explicitly requested

## When not to use

- **PowerPoint is required** — your audience needs to edit in Office. keynot can [export to PPTX](#exporting-to-pptx), but the output may need manual touch-up.
- **You need real-time collaboration** — Google Slides wins here.
- **Heavy animations or transitions** — keynot does opacity fades and staggered reveals, not 3D cube transitions.
- **Video embeds** — possible, but bloats the single-file deck quickly.
- **Portrait mobile viewing** — decks are landscape-first. Phones held vertically see a "rotate your device" overlay; landscape phone viewing works fine.

For everything else — pitches, one-pagers, internal readouts, conference talks, lunch-and-learns — keynot ships faster and looks sharper than the alternatives.

---

The next time someone says *"can you throw together some slides,"* throw together some HTML instead.

## Acknowledgments

Thanks to [Brandon Lafving](https://www.linkedin.com/in/brandon-lafving) for introducing me to the idea of generating presentations as self-contained HTML instead of reaching for PowerPoint. keynot wouldn't exist without that nudge.

## License

MIT — see [LICENSE](LICENSE).
