<p align="right"><b>English</b> | <a href="./README.fr.md">Français</a></p>

<h1 align="center">Presentation Forge</h1>

<p align="center">
  <b>Describe your talk to Claude. It writes the slides and bundles them into one portable <code>index.html</code> you can double-click, email, or host anywhere.</b>
</p>

<p align="center">
  <a href="https://github.com/thmsgo18/presentation-forge/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/thmsgo18/presentation-forge/ci.yml?style=for-the-badge&label=CI" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge" alt="License MIT"></a>
  <img src="https://img.shields.io/badge/claude-skill-d97757?style=for-the-badge" alt="Claude Skill">
  <img src="https://img.shields.io/badge/output-single%20file-2563eb?style=for-the-badge" alt="Single file output">
  <img src="https://img.shields.io/badge/python-stdlib%20only-f59e0b?style=for-the-badge" alt="Python stdlib only">
</p>

<p align="center">
  <a href="https://thmsgo18.github.io/presentation-forge/"><b>Live demo</b></a> •
  <a href="#install">Install</a> •
  <a href="#why-html-not-powerpoint">Why HTML</a> •
  <a href="#what-it-can-do">What it can do</a> •
  <a href="#example">Example</a> •
  <a href="#how-it-works">How it works</a> •
  <a href="#themes">Themes</a>
</p>

---

A [Claude](https://claude.com) skill that turns plain language into polished slide decks. You say *"make me a presentation about X"*; Claude scaffolds the deck, writes the slides, picks or builds a theme, and compiles everything into a single **self-contained `index.html`**. Engine, theme, fonts and images are all inlined, so the file opens by double-click, emails cleanly, and works fully offline. No framework, no build server, no dependencies.

It is an **Agent Skill**: one folder that works the same in **Claude Code**, the **Claude apps** (claude.ai and desktop), and through the **API**. No slash command to memorize, just ask.

> [!TIP]
> ⭐ Enjoying Presentation Forge? Starring the repo helps more people find it, thank you!

## Install

Install once on each surface where you want it.

**Claude Code** : drop the skill into your skills folder, Claude discovers it automatically:

```bash
git clone https://github.com/thmsgo18/presentation-forge.git ~/.claude/skills/presentation-forge
```

(For one project only, clone into `.claude/skills/presentation-forge/` inside that repo instead.)

> On Windows, run this in Git Bash or WSL, not plain PowerShell or cmd - they
> don't expand `~` to your home folder.

**Claude apps** (claude.ai and desktop) : upload **`dist/presentation-forge-skill.zip`** in **Settings → Features → Skills** (Pro, Max, Team or Enterprise, with code execution enabled).

**API** : upload the same `dist/presentation-forge-skill.zip` through the Skills API (`/v1/skills`) and reference it from the code-execution container.

> Custom skills do not sync across surfaces. Upload the zip once per surface.

## Why HTML, not PowerPoint

Claude can already spit out a `.pptx`. But a `.pptx` stays a prisoner of PowerPoint: it needs the app to open, its fonts and layout drift from one machine to the next, and it is a binary blob you cannot read or version. A Presentation Forge deck is just **one HTML file** that any browser renders identically, today and in ten years.

| | PowerPoint `.pptx` | Presentation Forge (HTML) |
| :--- | :---: | :---: |
| Presenter mode, speaker notes, timer | ✅ | ✅ |
| Progressive reveal, step by step | ✅ | ✅ |
| Slide transitions and animations | ✅ | ✅ |
| Images, code, quotes, multi-column layouts | ✅ | ✅ |
| Works with a presenter remote or clicker | ✅ | ✅ |
| Works fully offline | ✅ | ✅ |
| Anyone can fix a typo, no code needed | ✅ | ✅ |
| Opens with no software, in any browser | ❌ | ✅ |
| Renders identically on every machine | 🟠 | ✅ |
| Fonts travel inside the file | 🟠 | ✅ |
| Ships as one self-contained file | 🟠 | ✅ |
| Editable without proprietary software | ❌ | ✅ |
| Readable and versionable in git | ❌ | ✅ |
| Hostable as a public link | ❌ | ✅ |
| Reusable brand theme across decks | 🟠 | ✅ |
| No paid software to create or open | 🟠 | ✅ |

<sub>✅ yes · 🟠 partial or fragile · ❌ no. The top rows are everything PowerPoint already gives a presenter; Forge matches them, then adds the rest.</sub>

You lose nothing PowerPoint gives a presenter, and you gain portability, longevity and a file you actually own.

## What it can do

- 🧠 **Any brief into a deck** : a topic, an outline, rough notes, or a whole document. Technical talks, courses, pitches, lectures, any subject.
- ✍️ **Slides that land** : assertion-style titles, one idea per slide, tight bullets. Walls of text go into the notes, not on screen.
- 🧭 **Your deck, your pace** : Claude asks two things up front, then builds it plan first, all at once, or slide by slide with your review after each one. Every deck starts from your brief, never from a template to fill.
- 🎬 **Animation on a dial** : five levels, from perfectly still to the full show (3D, springy pops, icons that draw themselves). Change your mind later in one word, the slides don't move.
- 📊 **Charts, figures and icons built in** : key figures that count up, bar charts, gauges, timelines, processes, comparison tables and 84 line icons, all following your theme. Only what a deck uses gets bundled.
- 👀 **Claude checks its own slides** : every slide is rendered in a headless browser before you see it, so text running off a slide or a broken image gets fixed first.
- 🎤 **Present like a pro** : built-in presenter mode with speaker notes, a timer, and next-slide preview. Full keyboard navigation, press `?` for shortcuts.
- ✏️ **Edit without touching code** : fix a typo or reword a line right in the browser, saved straight back to the file, and kept when Claude rebuilds the deck.
- ✨ **Progressive reveal** : build a point step by step with `fragment`, the presenter view tracks each step.
- 🎨 **Swappable themes** : change the entire look without touching a single slide.
- 🏢 **Import a brand** : recreate an identity from a `.pptx`, an image, or a text description, and drop in a company logo.
- 💾 **Save a style once** : export any theme to a single `.pfstyle.json` and recreate the exact same look in any future conversation, no original files needed.
- 📦 **Single-file output** : one `index.html`, offline ready, zero dependencies, opens anywhere a browser exists.

<sub>Editing works in Chrome, Edge, or another Chromium browser - it's not available in Safari or Firefox, the button simply won't appear there. It also only works on a deck opened from your own machine: a downloaded or emailed copy is fine, a hosted link is not, since there is no real file there to save back to.</sub>

<p align="center">
  <img src="docs/screenshots/presenter-mode.png" width="49%" alt="Presenter mode: speaker notes, timer and next-slide preview">
  <img src="docs/screenshots/comparison-table.png" width="49%" alt="A content slide built with the obsidian theme, comparing PowerPoint and Presentation Forge">
</p>

## Example

```
You: /presentation-forge make me a deck about our Q3 results for the
     all-hands. Five minutes, upbeat tone. Revenue up 18%, churn down to
     4%, two new enterprise logos. Use our brand, here is last quarter's
     deck (attached .pptx).

Claude: Two quick choices first. Plan first, all at once, or slide by
        slide? And how much animation: none, subtle, balanced, lively
        or extra?

You: Plan first, lively.

Claude: [proposes a 6-slide outline: the headline figures, the two new
        logos, what's next. You swap two slides.]

        [imports the brand from the .pptx into a reusable theme, writes
        assertion-led slides with counting figures and speaker notes,
        builds a single index.html, then checks every slide in a
        headless browser]

        Done. Your deck is in q3-all-hands/index.html (6 slides).
        Open it and press p for presenter mode, arrow keys to navigate,
        ? for all shortcuts. I also saved the theme as acme.pfstyle.json
        so you can reuse this exact look next quarter.
```

## How it works

Three layers, always kept separate so a deck never breaks when you reskin it:

- **engine** (`template/engine/`) : rendering, scaling, navigation, presenter mode, reveal. Never edited.
- **theme** (`template/themes/<name>/`) : the look: colours, type, spacing, fonts, logos, backgrounds.
- **content** (`slides/`) : the slides, one HTML file each, ordered by name.

A new deck starts empty and is written from your brief; the [live demo](https://thmsgo18.github.io/presentation-forge/) is an example deck kept apart, in [`examples/showcase/`](examples/showcase/). The build is deliberately boring, which is what makes it portable: write slides in `slides/`, run `python3 build.py` (`python build.py` on Windows if `python3` isn't on `PATH`), and it inlines the engine, the theme, the fonts and every image into a single `index.html`. Slides are authored on a fixed **1920x1080** canvas that the engine scales to any screen, so a deck looks the same on a laptop, a projector or a phone. Full authoring contract in [`SKILL.md`](SKILL.md) and [`reference/`](reference/).

## Themes

A theme is a self-contained folder (`tokens.css`, `fonts.css`, `slides.css`, plus `fonts/`, `images/`, `logos/`). Every theme defines the same tokens and styles the same slide classes, so switching themes never breaks a deck. Two ship out of the box — **obsidian** (the dark, editorial look in the [live demo](https://thmsgo18.github.io/presentation-forge/)) and **ink-blue** (clean and light). Build your own from a brand four ways:

| Source | What Claude does |
| :----- | :--------------- |
| `.pptx` PowerPoint | Extracts the palette, fonts, embedded media and master layout geometry |
| Image (slide or mockup) | Samples the exact dominant colours, reads typography and layout by sight |
| Text description | Maps brand words to design tokens |
| `.pfstyle.json` | Rebuilds the entire theme (CSS, fonts, logos, backgrounds) in one step |

Whatever the source, the theme exports to one portable **`.pfstyle.json`**. Keep that file and recreate the exact same identity anytime. Full procedure in [`reference/import-theme.md`](reference/import-theme.md).

## Requirements

- A Claude client that supports skills ([Claude Code](https://docs.claude.com/en/docs/claude-code), the Claude apps, or the API).
- **Python 3.10+**, standard library only, to build decks and read `.pptx` files. Nothing else.
- A browser to view the result. With Chrome, Chromium, Edge or Brave installed, Claude also checks every slide visually before handing the deck over.

## Contributing

Bug reports and pull requests are welcome - see [`CONTRIBUTING.md`](CONTRIBUTING.md). Notable changes are tracked in [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE) © Thomas Gourmelen
