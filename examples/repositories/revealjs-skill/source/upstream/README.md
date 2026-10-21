# revealjs-skill

A coding agent skill for creating polished, professional [Reveal.js](https://revealjs.com/) HTML presentations using natural language.

**[View Example Presentation](https://ryanbbrown.com/revealjs-skill/examples/revealjs/presentation.html)**

Allows for:

- Professional themes and color palettes
- Multi-column layouts
- Callout boxes and styled components
- Chart.js integration for data visualization
- Font Awesome icons
- Speaker notes
- Animations and transitions
- Custom CSS styling

No build step required - just open the generated HTML in a browser. Can also be exported as a PDF.

## Installation

### Plugin (recommended)

Add the marketplace and install the plugin from within Claude Code:

```
/plugin marketplace add ryanbbrown/revealjs-skill
/plugin install revealjs@revealjs-skill
```

Then install dependencies (needed for overflow checking and PDF export):

```bash
npm install --prefix ~/.claude/plugins/cache/revealjs
```

### Manual

Alternatively, copy the `skills/revealjs` folder to your Claude Code skills directory:

```bash
# User-level installation (available in all projects)
cp -r skills/revealjs ~/.claude/skills/

# Or project-level installation
cp -r skills/revealjs .claude/skills/
```

Install dependencies (needed for overflow checking and PDF export):

```bash
npm install
```

### Dependencies

- **[Playwright](https://playwright.dev/)** - Browser automation for overflow detection
- **[DeckTape](https://github.com/astefanutti/decktape)** - PDF export and slide screenshots (using a [fork](https://github.com/ryanbbrown/decktape) that adds `--slides` flag for capturing specific slides, enabling faster iteration when fixing visual issues)
- **[Cheerio](https://cheerio.js.org/)** - HTML parsing to validate generated Chart.js

## Usage

Once installed, simply ask Claude Code to create a presentation:

> "Create a 10-slide presentation about renewable energy trends"

> "Make a pitch deck for a SaaS startup"

> "Build a quarterly business review presentation with charts"

Claude Code will:
1. Plan the slide structure based on your content
2. Choose an appropriate color palette and design
3. Generate the HTML and CSS files
4. Check for content overflow
5. Review screenshots of every slide for visual issues

## Browser Editing

After generating a presentation, you can edit text directly in the browser — no need to touch raw HTML:

```bash
node ~/.claude/skills/revealjs/scripts/edit-html.js my-presentation/presentation.html
```

This opens the presentation in a local server where you can click any text to edit it inline, then click Save to write changes back to the file. Press Escape to deselect a text element. Useful for wordsmithing, fixing typos, or tweaking copy after Claude generates the initial version.

## Features

Beyond base Reveal.js, this skill adds:

- **Custom CSS theme** - CSS variables for easy customization of colors, typography, callouts, and layout without modifying core styles
- **Scaffold generation** - Scaffolding script generates HTML structure so the LLM doesn't waste tokens recreating boilerplate
- **Overflow detection** - Automated checking catches content that extends beyond slide boundaries, faster than taking and reviewing screenshots
- **Chart export mode** - `?export` query parameter disables Chart.js animations so charts render fully in PDF/screenshots
- **Dynamic viewport color** - Viewport background color matches each slide's background for seamless full-screen presentation

## Star History

<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="https://api.star-history.com/svg?repos=ryanbbrown/revealjs-skill&type=Date&theme=dark"
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="https://api.star-history.com/svg?repos=ryanbbrown/revealjs-skill&type=Date"
  />
  <img
    alt="Star History Chart"
    src="https://api.star-history.com/svg?repos=ryanbbrown/revealjs-skill&type=Date"
  />
</picture>
