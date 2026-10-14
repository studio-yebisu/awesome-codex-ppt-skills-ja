# Paper2PPT Repository Redesign

**Date:** 2026-07-15
**Status:** Approved

## Objective

Rename `wp-a/nature-paper2ppt` to `wp-a/paper2ppt` and rebuild the repository
as a Chinese-first, Codex- and Claude Code-compatible Agent Skill for turning
scientific papers into editable, evidence-grounded PowerPoint presentations.

Remove `nature` from the repository name, Skill ID, plugin IDs, documentation,
default workflow, and visual language. Do not retain a compatibility alias or a
Nature-branded theme.

## Product Boundary

Paper2PPT remains an agent-driven Skill rather than becoming a standalone LLM
application. It must not require a separate model API key or duplicate the
reasoning and artifact capabilities already provided by Codex or Claude Code.

The repository may bundle deterministic Python utilities for input preflight,
PPTX inspection, and repository validation. It will not publish a PyPI package
or maintain an independent LLM runtime.

## Positioning

Paper2PPT is differentiated by the following contract:

- accepts paper PDFs, identifiers, URLs, text, notes, and user templates;
- uses the paper's argument and evidence chain as the presentation structure;
- generates a real, editable `.pptx`, not only an outline or Beamer PDF;
- preserves figures, source anchors, speaker notes, and uncertainty;
- performs content, package, and visual QA;
- runs as the same Agent Skill in Codex and Claude Code;
- defaults to Simplified Chinese while preserving technical terminology.

## Repository Architecture

```text
paper2ppt/
|-- SKILL.md
|-- README.md
|-- README.en.md
|-- LICENSE
|-- CHANGELOG.md
|-- references/
|   |-- workflow.md
|   |-- paper-types.md
|   |-- slide-design.md
|   |-- tool-routing.md
|   `-- quality-gates.md
|-- scripts/
|   |-- preflight.py
|   |-- inspect_pptx.py
|   `-- validate_repo.py
|-- examples/
|   |-- source/
|   |-- output/
|   `-- showcase/
|-- tests/
|   |-- test_skill.py
|   |-- test_manifests.py
|   |-- test_pptx_inspector.py
|   `-- trigger_cases.json
|-- plugins/paper2ppt/
|   |-- .codex-plugin/plugin.json
|   |-- .claude-plugin/plugin.json
|   `-- skills/paper2ppt/
`-- .github/workflows/ci.yml
```

The root `SKILL.md` is the canonical source. The packaged plugin copy must be
generated or synchronized from it, and tests must fail if the copies diverge.
References, scripts, and assets needed by the packaged Skill must also remain
synchronized.

## Skill Structure

The main `SKILL.md` should remain approximately 200-300 lines and contain only
the instructions required on every run:

- activation boundary and output contract;
- preflight and source-sufficiency gate;
- core evidence-first workflow;
- mandatory no-fabrication and source rules;
- tool-routing entry points;
- completion and QA gates;
- conditional links to detailed references.

Low-frequency material belongs in one-level-deep references. The Skill must
follow the Agent Skills frontmatter and progressive-disclosure conventions.

## Input Contract

Supported inputs include:

- local paper PDF;
- paper URL, DOI, PMID, PMCID, or arXiv identifier;
- article text or manuscript-derived Markdown/Word content;
- abstract plus results and figure legends;
- structured reading notes;
- supplementary figures or tables;
- a user-provided PPTX template.

Before analysis, determine the requested or inferred language, audience,
presentation duration, detail level, and template requirements. Default to a
12-16 slide Simplified Chinese deck for a 15-20 minute academic report.

Classify source sufficiency as full paper, partial paper content, or notes-only.
The confidence and output language must reflect that class. Partial inputs must
never be presented as a verified full-paper analysis.

## Evidence-First Workflow

1. Preflight the source, output path, required tools, and rendering options.
2. Extract and verify metadata where the environment provides suitable tools.
3. Identify the research problem, gap, primary claim, method, evidence,
   validation, limitations, and implications.
4. Build a claim-to-source map using pages, sections, figures, panels, tables,
   or supplied notes as anchors.
5. Classify the paper type and choose a matching narrative arc.
6. Plan slides according to talk duration and evidence density.
7. Select only figures and tables needed to support distinct claims.
8. Build a real editable PPTX with speaker notes and source labels.
9. Run content, structural, and visual QA, then revise detected defects.

The workflow must not copy the paper's section order mechanically.

## Paper-Type Routing

The detailed reference will cover at least:

- discovery and mechanism papers;
- clinical, population, and intervention studies;
- methods, AI, algorithms, and software tools;
- datasets, resources, atlases, omics, and benchmarks;
- chemistry, materials, physics, and engineering studies;
- reviews, perspectives, and systematic reviews.

Each type receives a distinct evidence arc. For example, methods papers should
move from bottleneck to method, evaluation, baselines, ablations, failure cases,
and reuse boundaries; discovery papers should move from question to evidence,
validation, model, limitations, and next experiments.

## Figure and Attribution Policy

Each result slide should normally carry one dominant item of evidence. Prefer
original figures or source-preserving crops over recreated data graphics. Keep
panel labels and scientific content intact.

For every extracted asset, record the source file or page, figure and panel,
crop status, destination slide, and quality notes. AI-generated imagery must
never replace experimental, clinical, or analytical evidence.

## Visual System

Replace the Nature-branded visual language with a neutral, adaptive academic
system:

- restrained light canvas and readable dark type by default;
- accessible accent colors selected for the paper's evidence, not branding;
- conclusion-style titles and one dominant visual hierarchy per slide;
- layouts selected from figure aspect ratio, density, and argumentative role;
- compact source labels and captions tied to the relevant visual;
- no decorative stock imagery, gradients, fake dashboards, or forced 50/50
  layouts;
- dense figures must be cropped, split, or promoted to their own slide.

The system is adaptive rather than a menu of branded themes.

## Tool Routing

Use the best available presentation tooling already provided by the current
agent environment. Keep the workflow and output contract client-neutral.

When no higher-level artifact tool is available, use a cross-platform Python
path based on PyMuPDF, Pillow, and `python-pptx`. These packages may be installed
locally only when environment policy permits. The bundled scripts remain
deterministic utilities rather than an LLM pipeline.

## Output Contract

The default output is deliberately small:

```text
output/<paper-slug>/
|-- presentation_zh.pptx
|-- qa_report.md
|-- asset_manifest.md       # only when assets were extracted
`-- assets/                 # only when assets were extracted
```

Optional outlines, scripts, or figure plans should be produced only when the
user asks for them or when they are required to resolve uncertainty.

## Failure Handling

- Do not bypass publisher access controls. Ask for a local PDF when a source is
  unavailable behind a paywall.
- Use OCR only after normal extraction fails or the source is demonstrably
  scanned.
- Degrade figure acquisition from original extraction to page crop to explicit
  omission; never reconstruct unverifiable data.
- Validate user templates before writing. Fall back to the neutral system only
  when the template is not a hard requirement, and record the decision.
- If no PPTX authoring path is available, stop during preflight and report the
  exact missing requirement instead of doing expensive work and claiming an
  outline is the requested deliverable.
- If no renderer is available, permit structurally verified delivery only when
  `qa_report.md` explicitly records the missing visual inspection.

## Quality Gates

Content QA must check:

- every major claim has source support;
- quoted numbers, methods, and cohorts match the source;
- figure interpretation matches the selected panel;
- uncertainty and incomplete source coverage are visible;
- limitations are specific rather than generic.

PPTX QA must check:

- the package can be reopened;
- slide, media, relationship, and notes counts are plausible;
- expected speaker notes and source labels are present;
- shapes do not obviously exceed slide bounds;
- selected figures are embedded and not missing.

When a reliable renderer exists, visual QA must also check legibility,
overflows, overlaps, clipping, image quality, alignment, and projection-scale
density. Revise detected defects before delivery.

## Test Strategy

Repository tests must cover:

- Agent Skills name, description, length, and reference validity;
- Codex and Claude plugin manifest parsing and version consistency;
- byte-for-byte synchronization of canonical and packaged Skill files;
- absence of legacy `nature` IDs and default-style language in controlled
  repository text;
- PPTX inspector behavior for valid, missing-media, missing-notes,
  out-of-bounds, and damaged-package fixtures;
- positive and near-miss trigger cases;
- representative behavior for methods/AI papers, experimental studies,
  reviews, and partial inputs;
- a license-safe open-access example deck and its QA artifacts.

CI should run deterministic validation only. Model-based forward tests will be
run manually in Codex and Claude Code before release and recorded in release
notes or maintenance documentation.

## Documentation and Showcase

`README.md` is Chinese-first and `README.en.md` provides an English equivalent.
The README first viewport should show the Paper2PPT name, its concise value
proposition, and real output previews. It must include:

- feature and differentiation summary;
- example output and traceability artifacts;
- Codex, Claude Code, and generic Agent Skills installation paths;
- supported inputs and default outputs;
- workflow, privacy, limitations, and troubleshooting;
- a comparison with outline-only Skills, Beamer generators, and standalone
  API-key-based applications.

The showcase uses a license-safe open-access paper and includes an editable
PPTX plus rendered preview images.

## Rename and Release

Rename the GitHub repository in place from `wp-a/nature-paper2ppt` to
`wp-a/paper2ppt`. This preserves repository history and stars and allows GitHub
to redirect the former URL.

Rename the local repository directory and remote URL after the GitHub change.
Replace the installed local `nature-paper2ppt` Skill with `paper2ppt`; do not
keep the legacy Skill alias.

There are currently no tags or releases. Publish the rebuilt repository as
GitHub Release `v0.1.0` after all validation succeeds. Do not publish to PyPI.

## Acceptance Criteria

The redesign is complete when:

- the repository, Skill, plugins, docs, examples, and release use `paper2ppt`;
- controlled repository text contains no legacy Nature identity or default
  style requirement;
- the canonical Skill satisfies Agent Skills validation and progressive
  disclosure targets;
- Codex and Claude Code plugin manifests validate and load the same Skill;
- deterministic tests and CI pass;
- the PPTX inspector passes its fixtures and the example deck;
- the example deck is editable, sourced, rendered, and visually reviewed;
- representative Codex and Claude Code forward tests satisfy the output and
  QA contract;
- the repository is renamed and GitHub Release `v0.1.0` is published.
