<h1 align="center">SeaSlides</h1>

<p align="center"><strong>AI-native presentation generation with Typst and Touying</strong></p>

<p align="center">
  Turn a topic, document, or URL into a compiled slide deck with a coherent narrative, a fitting<br>
  theme, speaker notes, and repeatable quality checks.
</p>

<p align="center">English · <a href="./README.zh-CN.md">简体中文</a></p>

<p align="center">
  <a href="https://github.com/touying-typ/seaslides/stargazers"><img src="https://img.shields.io/github/stars/touying-typ/seaslides?style=flat-square" alt="GitHub stars"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square" alt="License: MIT"></a>
  <a href="https://typst.app/"><img src="https://img.shields.io/badge/Typst-0.13%2B-239DAD?style=flat-square" alt="Typst 0.13+"></a>
  <a href="https://github.com/touying-typ/touying"><img src="https://img.shields.io/badge/Touying-0.7.4-5B5BD6?style=flat-square" alt="Touying 0.7.4"></a>
  <a href="#outputs"><img src="https://img.shields.io/badge/output-PDF%20%7C%20PNG%20%7C%20PPTX-111111?style=flat-square" alt="Output: PDF, PNG, PPTX"></a>
</p>

<p align="center">
  <a href="https://tylina.github.io/download/"><img src="https://img.shields.io/badge/Recommended_workspace-Download_Tylina-4F7FB3?style=for-the-badge" alt="Download Tylina, the recommended SeaSlides workspace"></a>
</p>

> [!TIP]
> **Recommended WYSIWYG workspace: [Tylina](https://tylina.github.io/).** Tylina is a local-first,
> document-first, AI-native WYSIWYG Typst desktop editor. Edit the typeset page directly, connect
> your own ACP agent, and keep standard `.typ` source as the canonical document. The development
> preview is available for macOS, Windows, and Linux and requires no account.

## SeaSlides × Tylina

SeaSlides is the generation layer: it reads source material, plans the story, selects or creates a
theme, authors Typst/Touying, compiles the deck, and checks the deliverables. Tylina turns that
output into a WYSIWYG desktop workspace. The typeset page is the editor—not merely a preview: click,
select, and type on the rendered deck, then open Source Lens or Split when source-level control is
needed.

- **WYSIWYG, backed by Typst** — edit the final typeset page while the real `.typ` source stays in sync.
- **Bring your own AI agent** — connect an ACP agent and give it document context through Skills and MCP.
- **A complete Slides workspace** — browse thumbnails, edit pages and speaker notes, reorder slides,
  and present from the same project.
- **Local and portable** — documents and history stay on your computer, with no proprietary document
  format or required account.

<p align="center">
  <strong><a href="https://tylina.github.io/download/">Download Tylina</a> · <a href="https://tylina.github.io/demo/">Watch the editing demo</a></strong>
</p>

<p align="center">
  <a href="https://tylina.github.io/"><img src="./assets/readme/tylina/slides.png" width="100%" alt="Tylina Slides workspace showing a SeaSlides-generated Botanical deck, slide thumbnails, rendered canvas, and ACP agent panel"></a><br>
  <sub>Generate with SeaSlides, then inspect, edit, reorder, and present in Tylina.</sub>
</p>

Tylina also includes a template browser for Tylina Slides and Typst Universe templates, so a new
deck can start from an existing visual system instead of rebuilding the design from scratch.

<p align="center">
  <a href="https://tylina.github.io/"><img src="./assets/readme/tylina/templates.png" width="100%" alt="Tylina template browser showing Tylina Slides and Typst Universe collections with a Botanical theme preview"></a><br>
  <sub>Browse presentation themes and the wider Typst Universe, then open a template as a draft or project.</sub>
</p>

## Theme Gallery

These overview contact sheets are compiled from the bundled `demo.typ` files. Click a preview to
open the corresponding theme.

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="./skills/seaslides-typst-slides-skill/templates/themes/custom-plain/cherry/"><img src="./assets/readme/themes/cherry-overview.png" width="100%" alt="Cherry Plain theme overview"></a><br>
      <strong>Cherry · Plain</strong><br>
      <sub>Soft sakura colors, restrained typography, and lightweight components.</sub>
    </td>
    <td width="50%" valign="top">
  <a href="./skills/seaslides-typst-slides-skill/templates/themes/custom-plain/midnight/"><img src="./assets/readme/themes/midnight-overview.png" width="100%" alt="Midnight Plain theme overview"></a><br>
  <strong>Midnight · Plain</strong><br>
  <sub>Dark navy foundations, cool accents, and readable technical content.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="./skills/seaslides-typst-slides-skill/templates/themes/custom-rich/bauhaus/"><img src="./assets/readme/themes/bauhaus-overview.png" width="100%" alt="Bauhaus Rich theme overview"></a><br>
      <strong>Bauhaus · Rich</strong><br>
      <sub>Geometric components, strong hierarchy, and structured visual rhythm.</sub>
    </td>
    <td width="50%" valign="top">
      <a href="./skills/seaslides-typst-slides-skill/templates/themes/custom-rich/data-ink/"><img src="./assets/readme/themes/data-ink-overview.png" width="100%" alt="Data Ink Rich theme overview"></a><br>
      <strong>Data Ink · Rich</strong><br>
      <sub>Charts, tables, metrics, and restrained analytical styling.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="./skills/seaslides-typst-slides-skill/templates/themes/custom-canvas/polar-expedition/"><img src="./assets/readme/themes/polar-expedition-overview.png" width="100%" alt="Polar Expedition Canvas theme overview"></a><br>
      <strong>Polar Expedition · Canvas</strong><br>
      <sub>Expedition-report structure, restrained cartography, and crisp scientific storytelling.</sub>
    </td>
    <td width="50%" valign="top">
      <a href="./skills/seaslides-typst-slides-skill/templates/themes/custom-canvas/botanical/"><img src="./assets/readme/themes/botanical-overview.png" width="100%" alt="Botanical Canvas theme overview"></a><br>
      <strong>Botanical · Canvas</strong><br>
      <sub>Archival botanical detail with an immersive light-and-dark rhythm.</sub>
    </td>
  </tr>
</table>

See the [complete theme catalog](./skills/seaslides-typst-slides-skill/templates/themes/README.md)
for all Plain, Rich, Canvas, Builtin, and Universe options.

## What You Get

- **Source to slides** — PDF, DOCX, PPTX, spreadsheets, EPUB, HTML, URLs, Markdown, or plain text
- **180+ catalogued themes** — 14 Plain, 86 Rich, 37 Canvas, 6 Touying built-ins, and 40 community themes
- **Two workflows** — Quick Mode for a fast usable draft; Full Mode for strategy, research, new assets, or bespoke design
- **Typst-native output** — readable `.typ` source with Touying components and speaker notes
- **Repeatable quality gates** — compilation, per-page PNGs, overview sheet, mechanical checks, validation, and review at the depth you request
- **Presentation resources** — 50+ chart templates, 15 optional Typst packages, and 6 icon systems
- **Optional asset and export tools** — AI image generation, licensed web image search, and PPTX export
- **More than slide decks** — academic posters, CVs, social covers, and other presentation-oriented formats

## 30-Second Start

### 1. Install the Agent Skill

For Claude Code, Codex, Cursor, and other local agents that support Skills:

```bash
npx skills add https://github.com/touying-typ/seaslides --skill seaslides-typst-slides-skill
```

Then give the agent a topic or a source file:

```text
Create a quick 8-slide Typst deck from this Markdown file. Use reasonable defaults.

Turn projects/q3-report/report.pdf into a concise executive presentation and export PDF and PPTX.

Use Full Mode to create a research talk from these notes, with citations and a delivery-grade visual review.
```

The skill automatically routes between Quick and Full Mode, converts supported source files,
selects a theme, compiles the deck, and validates the result.

The command above installs the Skill files. Install the Python dependencies from the installed
Skill directory, or clone the full repository below, to use the conversion, compilation, image,
and export tools.

### 2. Clone the Full Toolchain

Clone the repository when you want the complete scripts, theme library, and local development
workflow:

```bash
git clone https://github.com/touying-typ/seaslides.git
cd seaslides
python3 -m pip install -r requirements.txt
```

Optional image and search providers are configured through `.env`:

```bash
cp .env.example .env
```

The Python Typst binding is included in the requirements. A standalone `typst` CLI is only needed
for direct commands such as `typst watch`.

## Quick Mode or Full Mode?

| | Quick Mode | Full Mode |
|---|---|---|
| Best for | First usable draft, speed, reasonable defaults | High-stakes delivery, research, new assets, bespoke design |
| Theme | One existing Plain, Rich, or Canvas theme | Existing, extended, or newly designed theme |
| Planning | Concise narrative written directly | Separate content design specification |
| Roles | Direct authoring | Strategist → Image Generator when needed → Executor |
| Visual review | None, targeted, or full—matched to the request | Full workflow, with review depth still honoring the request |

Quick/Full are workflow modes. Plain/Rich/Canvas are theme-complexity tiers; a demonstrated Canvas
theme can still be fast in Quick Mode.

```text
Quick: Source → Project → Existing Theme → Author → Compile → [Review] → Export
Full:  Source → Project → Theme → Strategist → [Images] → Executor → Compile → Review → Export
```

## Outputs

The normal publication pipeline produces:

| Artifact | Purpose |
|---|---|
| `main.typ` + `template.typ` | Editable Typst/Touying source and project-owned theme |
| `output/slides.pdf` | Presentation-ready PDF |
| `output/pngs/slide_XX.png` | One PNG per rendered slide |
| `output/overview.png` | Contact sheet for fast deck-level review |
| `output/compile-manifest.json` | Receipt for a coherent compilation run |
| `output/slides.pptx` | Optional PPTX export through `typ2pptx` |

Every slide is authored with speaker notes.

## Theme System

SeaSlides chooses by content, audience, and delivery setting rather than mapping every topic to the
same style.

| Tier | Use it for |
|---|---|
| **Plain** | Restrained typography and minimal decoration |
| **Rich** | Dependable component-based decks, cards, metrics, and structured layouts |
| **Canvas** | Editorial, Swiss, festival, visual-storytelling, or bespoke page composition |
| **Builtin / Universe** | Named Touying themes and maintained community packages |

Browse the [theme dispatcher](./skills/seaslides-typst-slides-skill/templates/themes/README.md), or
open the [Plain](./skills/seaslides-typst-slides-skill/templates/themes/custom-plain/README.md),
[Rich](./skills/seaslides-typst-slides-skill/templates/themes/custom-rich/README.md), and
[Canvas](./skills/seaslides-typst-slides-skill/templates/themes/custom-canvas/README.md) catalogs.

## Command Reference

```bash
SKILL_DIR=skills/seaslides-typst-slides-skill

# Create and populate a project
python3 "$SKILL_DIR/scripts/project_manager.py" init my-deck --exact-name
python3 "$SKILL_DIR/scripts/project_manager.py" import-sources projects/my-deck source.pdf --copy

# Compile, audit, and validate
python3 "$SKILL_DIR/scripts/typst_compiler.py" projects/my-deck --all
python3 "$SKILL_DIR/scripts/typst_quality_checker.py" projects/my-deck
python3 "$SKILL_DIR/scripts/validate_project.py" projects/my-deck

# Quick Mode validation omits the separate design specification
python3 "$SKILL_DIR/scripts/validate_project.py" projects/my-deck --mode quick

# Optional PPTX export
python3 "$SKILL_DIR/scripts/typst_compiler.py" projects/my-deck --format pptx
```

For normal use, ask the agent to run the workflow instead of invoking every command manually.

## Repository Map

```text
skills/
  seaslides-typst-slides-skill/
    SKILL.md                     # Authoritative workflow and quality contract
    workflows/                   # Quick, Full, review, research, and theme workflows
    references/                  # Strategy, execution, design, and Typst standards
    scripts/                     # Conversion, compilation, validation, and image tools
    templates/                   # Themes, charts, packages, icons, and schemas
  seaslides-html-slides-skill/   # Companion HTML/SVG presentation backend
projects/                        # Local generated projects (gitignored)
```

Start with the [main Skill](./skills/seaslides-typst-slides-skill/SKILL.md). For implementation
details, see the [script index](./skills/seaslides-typst-slides-skill/scripts/README.md),
[Quick Mode](./skills/seaslides-typst-slides-skill/workflows/quick-mode.md), and the
[visual-review workflow](./skills/seaslides-typst-slides-skill/workflows/visual-review.md).

## Acknowledgments

### PPT Master — Project foundation

SeaSlides is developed on top of [PPT Master](https://github.com/hugohe3/ppt-master) by Hugo He.
PPT Master established the project foundation: an agent-driven workflow that turns source material
into a structured narrative, generates an editable presentation through multiple stages, and
checks the result before delivery.

SeaSlides extends that foundation with three major capabilities and architectural changes:

- **First-class Typst support.** The generation, compilation, review, and export pipeline is built
  around Typst and Touying, with native PDF, PNG, and PPTX output.
- **Separation of templates and content.** Reusable visual systems, layout components, and public
  APIs live in theme files, while presentation-specific narrative and copy remain in the content
  source. A deck can therefore change themes without rebuilding its content structure, and a theme
  can be reused across many decks.
- **Native Tylina editing.** SeaSlides decks can use [Tylina](https://tylina.github.io/)'s native
  Typst Slides workspace to open, edit, preview, reorder, and present from the desktop application.

We are grateful to PPT Master for the workflow architecture and implementation foundation that
made this project possible.

### Guizang PPT Skill — HTML presentation reference

The HTML presentation portion of SeaSlides was developed with reference to
[Guizang PPT Skill](https://github.com/op7418/guizang-ppt-skill) by Guizang. Its agent-native
HTML/CSS generation approach, electronic-magazine compositions, and Swiss editorial visual
language informed SeaSlides' HTML-side implementation and design vocabulary.

### Typst and Touying

[Typst](https://typst.app/) and [Touying](https://github.com/touying-typ/touying) provide the
typesetting and presentation foundations for SeaSlides' Typst workflow. Please visit and support
all of these original projects.

## Feedback

Bug reports, theme requests, and workflow ideas are welcome in
[GitHub Issues](https://github.com/touying-typ/seaslides/issues).

## License

Released under the [MIT License](./LICENSE). Third-party themes, packages, fonts, icons, and media
retain their respective licenses.

## Citation

If you find SeaSlides useful, please cite our paper:
[SeaSlides: Semantic Abstraction Layer for Agentic Slide Generation](https://arxiv.org/abs/2608.03298).

```bibtex
@misc{fang2026seaslides,
  title         = {{SeaSlides}: Semantic Abstraction Layer for Agentic Slide Generation},
  author        = {Shengjun Fang and Chenyang Wu and Zongzhang Zhang},
  year          = {2026},
  eprint        = {2608.03298},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  url           = {https://arxiv.org/abs/2608.03298}
}
```
