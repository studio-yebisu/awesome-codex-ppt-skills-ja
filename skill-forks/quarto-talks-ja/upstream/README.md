# quarto-talks

`quarto-talks` is a small RevealJS format for argument-led presentations, plus a portable agent skill for turning source material into a deck. 

## What is included

- a self-contained `quarto-talks-revealjs` format extension;
- one restrained SCSS theme with no remote fonts;
- defaults for prose, statements, questions, quotations, figures, tables, code, mathematics, and citations;
- a starter [`template.qmd`](template.qmd);
- a portable [`SKILL.md`](SKILL.md) for compatible coding agents;
- three synthetic example decks and a render test.

The format uses standard Quarto and RevealJS syntax. 

## Requirements

- Quarto 1.4 or newer.
- Quarto 1.6.39 is the version currently exercised by the local render suite.

## Install

Start a new deck from the repository template:

```bash
quarto use template alfredo-hs/quarto-talks
```

Add only the format extension to an existing Quarto project:

```bash
quarto add alfredo-hs/quarto-talks
```

For local development, clone the repository and install from its path:

```bash
git clone https://github.com/alfredo-hs/quarto-talks.git
mkdir my-talk && cd my-talk
quarto add ../quarto-talks
cp ../quarto-talks/template.qmd talk.qmd
quarto render talk.qmd
```

## Use the format directly

Select the format in a `.qmd` file:

```yaml
---
title: "A specific title"
author: "Your Name"
format:
  quarto-talks-revealjs: default
---
```

Then write ordinary Quarto slides:

```markdown
## The main result {.statement}

One sentence of support can sit here.

## What changes the decision? {.question}

## Evidence {.visual}

![Outcome by month](figure.svg){fig-alt="Describe the axes, groups, and main pattern."}
```

Available slide classes are `.statement`, `.question`, `.quote`, `.visual`, `.math`, and `.code`. Ordinary slides need no class. Standard features such as columns, speaker notes, fragments, citations, and slide attributes continue to work normally.

The default output embeds its resources in a single HTML file. Override any RevealJS option in the document YAML when a project needs different behaviour.

### Optional: embed a Bluesky post

Enable it once in the document header:

```yaml
bluesky:
  enabled: true
  max-width: 560
```

Then place the full post URL in a `.bluesky-post` div on any slide:

```markdown
## A response worth reading

::: {.bluesky-post}
https://bsky.app/profile/bsky.app/post/3lndjyecwcs2a
:::
```

`max-width` is optional, defaults to `600`, and is constrained to the `220`–`600` pixel range supported by the official Bluesky oEmbed service.

Rendering never contacts Bluesky. When the presentation is viewed online, the link card asks Bluesky's official oEmbed service for the public post and upgrades it to the official iframe. If the request, JavaScript, post, or iframe is unavailable, the link card—or Bluesky's static blockquote—remains readable instead. No login, API key, package, or copied embed HTML is required.

## Use the agent skill

Copy [`SKILL.md`](SKILL.md) into the skill directory used by a compatible coding agent, or provide the file with the source material and ask the agent to follow it. The skill directs the agent to inspect the sources, identify the audience and central argument, draft the intellectual spine, select material, render, and repair obvious problems.

It can work from `.qmd`, `.md`, `.tex`, `.docx`, `.pdf`, figures, bibliography files, code, and existing Quarto or Beamer decks, subject to the extraction and rendering tools available in the agent's environment. It explicitly prohibits invented citations, quotations, equations, results, figures, and execution claims.

## Examples

- [`examples/research/research.qmd`](examples/research/research.qmd): a synthetic research-style talk with a figure and citation.
- [`examples/conceptual/conceptual.qmd`](examples/conceptual/conceptual.qmd): a conceptual argument with no figures.
- [`examples/math-code/math-code.qmd`](examples/math-code/math-code.qmd): display mathematics, readable code, and a comparison table.

Render one deck:

```bash
quarto render examples/research/research.qmd
```

Render the starter and every example:

```bash
quarto render
```

Run the install-and-render checks:

```bash
bash tests/render-examples.sh
```

## Design decisions

The visual system follows stable design principles. A quiet blue accent, white background, system-serif headings, system-sans body text, thin rules, and generous spacing carry the design. Equations are centred and enlarged; code retains a comfortable size and wraps rather than being globally reduced. Figures receive room instead of decoration, while semantic sparse slides and RevealJS's native `.center` class create intentional changes of pace.

The core theme contains no behavioural JavaScript and only six semantic slide classes. Optional integrations may add small local progressive-enhancement scripts, without frameworks or packages. This keeps the source readable and makes normal Quarto knowledge sufficient to modify a deck.

## Current limitations

- Visual quality still depends on editorial judgement; the extension does not detect overflow or redesign figures automatically.
- Dense tables, long derivations, and large code listings should be split or moved to an appendix.
- The theme targets a 16:9 projected layout and has not been tuned for every screen, browser, or print-to-PDF workflow.
- The agent skill depends on the host agent's ability to read source formats and run Quarto; it does not bundle document parsers or execution environments.
- Only Quarto 1.6.39 has been tested so far, although the manifest permits Quarto 1.4 and newer because it uses stable format-extension features.

## License

MIT. See [`LICENSE`](LICENSE).
