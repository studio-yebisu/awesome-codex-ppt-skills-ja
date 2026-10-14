# Paper2PPT

<a href="README.md">简体中文</a> | English

<p>
  <img alt="version 0.1.0" src="https://img.shields.io/badge/version-0.1.0-2563eb">
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-0f766e">
  <img alt="Agent Skills compatible" src="https://img.shields.io/badge/Agent%20Skills-compatible-7c3aed">
  <img alt="Codex and Claude Code" src="https://img.shields.io/badge/Codex%20%2B%20Claude%20Code-compatible-334155">
</p>

**Turn a scientific paper into an editable, traceable Chinese PPTX with speaker notes and explicit quality checks.**

Paper2PPT is an Agent Skill for Codex and Claude Code. It structures a presentation around the paper's argument and evidence instead of copying section order. The default is a 12-16 slide Simplified Chinese deck for a 15-20 minute research talk.

## Quick start

```bash
git clone https://github.com/wp-a/paper2ppt.git
mkdir -p ~/.agents/skills
cp -R paper2ppt/plugins/paper2ppt/skills/paper2ppt ~/.agents/skills/
```

Start a new Codex task and prompt: `Use $paper2ppt to turn this paper into a 15-minute Chinese journal-club deck.`

<img alt="Paper2PPT real output overview" src="examples/showcase/overview.png" width="100%">

<a href="examples/output/paper2ppt-example-zh.pptx">Download the editable example PPTX</a> · <a href="examples/output/qa_report.md">Read its QA report</a> · <a href="examples/output/asset_manifest.md">Inspect its asset manifest</a>

## Why Paper2PPT

- **Evidence before layout:** build a claim-to-source map before choosing the narrative, slides, or figures.
- **A real PPTX:** deliver an editable `.pptx`, not only an outline, image set, or PDF.
- **Traceable results:** result slides include source labels and speaker notes; extracted assets record page, figure, panel, crop, and destination.
- **Paper-type routing:** discovery, clinical, methods/AI, resource, engineering, and review papers use different evidence arcs.
- **Three separate gates:** run content QA, structural QA, and visual QA; an openable file is not proof of scientific accuracy or projection readability.
- **One canonical Skill:** the root `SKILL.md` is synchronized into both the Codex and Claude Code plugin packages and checked by tests.

## Installation

### Direct Skill: the simplest path

Direct installation suits personal use and local evaluation. Copy the complete Skill directory, not `SKILL.md` alone.

**Codex**

Install target: `~/.agents/skills/paper2ppt`

```bash
mkdir -p ~/.agents/skills
cp -R paper2ppt/plugins/paper2ppt/skills/paper2ppt ~/.agents/skills/
```

**Claude Code**

Install target: `~/.claude/skills/paper2ppt`

```bash
mkdir -p ~/.claude/skills
cp -R paper2ppt/plugins/paper2ppt/skills/paper2ppt ~/.claude/skills/
```

**Other Agent Skills clients**

```bash
cp -R paper2ppt/plugins/paper2ppt/skills/paper2ppt <AGENT_SKILLS_DIR>/paper2ppt
```

The Agent Skills specification defines the package format, not one universal discovery directory. Replace `<AGENT_SKILLS_DIR>` with the path documented by your client.

### Plugin: install UI, version, and distribution metadata

The plugin at `plugins/paper2ppt/` contains both `.codex-plugin` and `.claude-plugin` manifests. Add the repository as a marketplace, then install it from Codex `/plugins` or the desktop Plugins page. Claude Code supports a complete command-line flow:

```bash
codex plugin marketplace add wp-a/paper2ppt
codex plugin add paper2ppt@personal
claude plugin marketplace add wp-a/paper2ppt
claude plugin install paper2ppt@paper2ppt
```

Codex also supports selecting Paper2PPT from `/plugins` or the desktop Plugins page. Start a new task after installation.

Choose either the direct Skill or plugin installation to avoid duplicate Skill entries. See the <a href="docs/installation.md">installation guide</a> for project scope, local plugin testing, upgrades, migration, and uninstall steps.

## Supported inputs

- local paper PDF;
- article URL, DOI, PMID, PMCID, or arXiv identifier;
- article text, Markdown, or Word-derived content;
- abstract plus results and figure legends;
- structured reading notes;
- supplementary figures or tables, and an optional user PPTX template.

Preflight records language, audience, duration, detail, and template requirements. Source sufficiency is classified as `full-paper`, `partial-paper`, or `notes-only`; a partial source is never represented as a verified full-paper reading.

## Exact default outputs

```text
output/<paper-slug>/
├── presentation_zh.pptx
├── qa_report.md
├── asset_manifest.md       # only when assets were extracted
└── assets/                 # only when assets were extracted
```

PDFs, outlines, scripts, and figure plans are optional and generated only when requested. Another requested language uses `presentation_<language-code>.pptx`.

## Workflow and quality gates

1. **Preflight:** verify input, output, extraction, editable PPTX authoring, notes, and rendering capabilities.
2. **Evidence model:** extract the problem, gap, design, claims, evidence, validation, limitations, and implications, then bind them to pages, sections, figures, tables, and panels.
3. **Narrative plan:** route by paper type and talk duration, with one primary claim per slide.
4. **Authoring:** build the editable PPTX and add source labels, notes, and scientific qualifiers to result slides.
5. **content QA:** verify numbers, units, cohorts, methods, figure interpretations, causal language, and uncovered scope.
6. **structural QA:** reopen the OOXML package and inspect slides, media, relationships, speaker notes, bounds, and external dependencies.
7. **visual QA:** when a renderer exists, render every slide and inspect overlap, clipping, glyphs, contrast, density, and projection readability; revise and rerun after any defect.

Any unresolved content or structural failure produces `blocked`. `structurally-verified-with-disclosure` is allowed only when content and structure pass but visual QA is unavailable solely because no renderer exists.

## Reproducible example

The showcase uses a CC BY 4.0 open-access paper. It includes a nine-slide editable Chinese PPTX, notes on every slide, an asset manifest, and a full-slide render review using LibreOffice and Poppler.

| Method | Main result | Evidence boundary |
| --- | --- | --- |
| <img alt="Editable method slide" src="examples/showcase/slide-04-method.png" width="100%"> | <img alt="Main result slide" src="examples/showcase/slide-05-results.png" width="100%"> | <img alt="Study boundary slide" src="examples/showcase/slide-08-boundaries.png" width="100%"> |

See the <a href="examples/source/README.md">source and license metadata</a>.

## How it differs

| Approach | Primary deliverable | Evidence and notes | Runtime boundary |
| --- | --- | --- | --- |
| **Paper2PPT** | Editable PPTX | Source labels, speaker notes, asset manifest, three QA gates | Runs inside an existing Codex or Claude Code session; no separate model API key |
| Outline-only Skills | Markdown or text outline | Traceability and QA depend on the implementation | Useful for reviewing structure, but not a finished PPTX |
| Beamer generators | TeX source, usually compiled to PDF | Citation behavior depends on the template; continued editing uses LaTeX/Beamer | Useful for code-based typesetting, not native PowerPoint editing |
| Standalone API-key applications | Product-specific, often a web result or exported file | Depends on the product | Requires separate deployment/account and a model API key supplied to that application |

This compares deliverables and runtime boundaries. It does not claim that every tool in a category has identical features.

## Privacy and limitations

- **Privacy:** Paper2PPT has no backend and does not collect papers. Data handling follows the active Codex or Claude Code client, connectors, and third-party services. Check organizational policy before processing unpublished or sensitive material.
- **Paywall:** the workflow does not bypass access controls. Provide a local PDF when the full text is not legally accessible.
- **OCR:** use it only when ordinary extraction fails and the source is demonstrably scanned. OCR can corrupt formulas, symbols, tables, and captions; verify important values manually.
- **Renderer:** without LibreOffice, PowerPoint, or another reliable renderer, only structural QA is possible and `qa_report.md` must disclose that visual QA did not run.
- **Partial source:** `partial-paper` and `notes-only` support narrower claims and cannot establish unobserved methods, numbers, or limitations.
- **Templates and fonts:** an invalid optional template falls back to a neutral academic layout; unavailable fonts may be substituted on another device. A missing mandatory template blocks delivery.
- **Runtime dependencies:** the Skill prefers capabilities already exposed by the client. The Python fallback requires permission to install compatible PyMuPDF, Pillow, and `python-pptx`. This repository is not a PyPI package and contains no standalone model runtime.

## Development and verification

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/sync_plugin.py --check
python scripts/validate_repo.py
python -m pytest -q
python scripts/inspect_pptx.py examples/output/paper2ppt-example-zh.pptx --require-notes
```

See <a href="docs/maintenance.md">maintenance</a> and the <a href="CHANGELOG.md">changelog</a>.

## License

<a href="LICENSE">MIT</a>. Example paper figures retain their original CC BY 4.0 license and attribution; see the <a href="examples/output/asset_manifest.md">asset manifest</a>.
