---
name: seaslides-html-slides-skill
description: >
  AI-driven HTML presentation generation system. Converts source documents
  (PDF/DOCX/URL/Markdown) into browser-ready HTML slide decks and exports them
  to SVG, PNG, and native PPTX through multi-role collaboration. Use this skill
  when the user requests HTML slides, a web presentation, a browser-editable or
  WYSIWYG-friendly deck, horizontal swipe slides, or document-to-slides work that
  explicitly requires HTML output. Trigger phrases include "html slides",
  "html presentation", "web slides", "make html deck", "html ppt",
  "horizontal swipe deck", "浏览器幻灯片", "HTML 演示文稿", or mentions
  "seaslides-html-slides-skill".
---

# SeaSlides HTML Slides Skill

Convert source material into a browser-ready HTML deck with synchronized SVG, PNG, and PPTX outputs.

**Pipeline**: `Source -> Project -> Theme -> Strategist -> [Images] -> Executor -> Assemble -> Review -> Export`

## Hard Contract for Standard Slides

1. Run creation phases serially and complete each gate before continuing.
2. Ask at blocking decisions. In unattended mode, decide them and continue.
3. Convert document sources to Markdown before planning.
4. Preserve Template-Content Separation (TCS): shell in `index-template.html`, reusable styling in `template.css`, semantic slides in `content.html`.
5. Keep `<style>`, `<script>`, `<link>`, event handlers, and ad hoc visual styles out of standard-slide `content.html`.
6. Permit inline styles only for data values on the component/property allowlist defined in `${SKILL_DIR}/references/shared-standards.md`; the validator enforces the same list.
7. Reassemble after every content, CSS, or template change. Treat root `index.html`, SVGs, both PNG routes, overview, and compiler receipts as one synchronized generation.
8. Pass the source gate before building, then pass the current-build visual gate before delivery. Build PPTX in that same build when it is requested.

The canonical standard-slide TCS rules live in `${SKILL_DIR}/references/shared-standards.md` and `${SKILL_DIR}/scripts/validate_project.py`.

## Scenario Routing

Route special outputs before applying the standard-slide contract:

| Intent | Read and follow |
|---|---|
| Academic or conference poster | `${SKILL_DIR}/references/scenarios/poster.md` |
| CV or resume | `${SKILL_DIR}/references/scenarios/cv.md` |
| Social cover, article header, or thumbnail | `${SKILL_DIR}/references/scenarios/social-cover.md` |
| Standard HTML presentation | Continue below |

Each special scenario defines its own authoring and review contract. Do not apply the standard-slide TCS validator or standard slide-count/rhythm rules unless that scenario explicitly requests them.

Match the user's language. Keep the structural headings in `content_design_spec.md` stable while writing values in the user's language when appropriate.

For 25+ slide decks, use `${SKILL_DIR}/workflows/resume-execute.md` to split planning and execution across sessions.

## Standard-Slide Architecture

| File | Responsibility |
|---|---|
| `index-template.html` | Browser shell, navigation, external libraries, `{{CONTENT}}` placeholder |
| `template.css` | Canvas metadata, theme tokens, layout and component classes |
| `content.html` | Semantic `<section class="slide ...">` blocks and speaker notes |

`html_compiler.py --all` atomically assembles root `index.html` and produces `output/svgs/`, `output/pngs/`, `output/browser_pngs/`, `output/overview.png`, `output/slides.pdf`, `output/dom-audit.json`, `output/render-fidelity.json`, and `output/compile-manifest.json`. Add `--include-pptx` when PowerPoint is required; it produces `output/slides.pptx` in the same build and receipt.

## Resource Map

Load references only when entering the relevant phase.

| Phase or need | Resource |
|---|---|
| Full creation workflow | `${SKILL_DIR}/workflows/create-presentation.md` |
| Theme selection | `${SKILL_DIR}/workflows/select-theme.md` |
| New theme creation | `${SKILL_DIR}/workflows/create-template.md` |
| Topic-only research | `${SKILL_DIR}/workflows/topic-research.md` |
| Chart calibration | `${SKILL_DIR}/workflows/verify-charts.md` |
| Visual review | `${SKILL_DIR}/workflows/visual-review.md` |
| Strategist role | `${SKILL_DIR}/references/strategist.md` |
| Standard HTML/TCS contract | `${SKILL_DIR}/references/shared-standards.md` |
| Executor fundamentals | `${SKILL_DIR}/references/executors/base.md` |
| General / consulting / MBB / academic style | `${SKILL_DIR}/references/executors/<style>.md` |
| Components and layouts | `${SKILL_DIR}/references/components.md`, `${SKILL_DIR}/references/layouts.md` |
| Design heuristics | `${SKILL_DIR}/references/design-guide.md` |
| Image dispatch and layout | `${SKILL_DIR}/references/image-base.md`, `${SKILL_DIR}/references/image-layout-patterns.md` |
| Review rubric and issue severity | `${SKILL_DIR}/references/visual-review.md`, `${SKILL_DIR}/references/checklist.md` |
| Artifact and visual issue ownership | `${SKILL_DIR}/references/artifact-ownership.md` |
| Theme creation internals | `${SKILL_DIR}/references/template-designer.md` |
| Browser DOM export | `${SKILL_DIR}/scripts/docs_html/browser_dom_export.md` |
| Content plan template | `${SKILL_DIR}/templates/content_design_spec_reference.md` |

Use `${SKILL_DIR}/templates/index.json` as the only theme catalog. Do not maintain a second theme list in this entry file.

## Workflow

### Step 1: Process Sources

**Gate**: Source material or a topic is available.

If only a topic is provided, follow `${SKILL_DIR}/workflows/topic-research.md` or create a source brief before continuing.

| Input | Command |
|---|---|
| PDF | `python3 ${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py <file> --images filtered` |
| DOCX / EPUB / HTML / LaTeX / RST | `python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py <file>` |
| PPTX / PPSX | `python3 ${SKILL_DIR}/scripts/source_to_md/ppt_to_md.py <file>` |
| Excel | `python3 ${SKILL_DIR}/scripts/source_to_md/excel_to_md.py <file>` |
| Web page | `python3 ${SKILL_DIR}/scripts/source_to_md/web_to_md.py <url>` |
| Markdown / text | Read directly |

Do not proceed with only an unread raw document when a converter is available.

### Step 2: Initialize the Project

**Gate**: Readable source content exists.

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py init <project_name>
python3 ${SKILL_DIR}/scripts/project_manager.py import-sources <project_path> <source_files...> --copy
```

Use `--exact-name` only when a deterministic, date-free directory name is needed (for example, a reproducible benchmark); normal projects retain the dated suffix.

Use `--move` only when explicitly requested. Copy extracted images into `assets/` and import the converted Markdown.

### Step 3: Select a Theme

**Gate**: Project directory exists.

Follow `${SKILL_DIR}/workflows/select-theme.md`.

1. Read `${SKILL_DIR}/templates/index.json`.
2. Use a user-named theme directly; otherwise rank themes by metadata such as tags, `bestFor`, style, audience, and content needs.
3. Present a concise recommendation and wait unless unattended mode is active.
4. Do not use a fixed default theme merely because the request is ambiguous; choose the best-supported candidate from the catalog.

Copy the selected theme files:

```bash
cp ${SKILL_DIR}/templates/<theme>/index-template.html <project_path>/
cp ${SKILL_DIR}/templates/<theme>/template.css <project_path>/
```

Read the selected theme's `theme.md` and `demo.html`. Use their actual CSS vocabulary and composition patterns; do not copy irrelevant sample content or decorative details mechanically. A demo may contain theme-authoring geometry: never copy a non-data inline style into standard-slide `content.html`; translate reusable treatment into `template.css` classes.

### Step 4: Produce the Content Design Spec

**Gate**: Theme is selected and understood.

Read the Strategist and shared standards. Present the nine decisions as one bundle and wait unless unattended mode is active:

1. Page format
2. Page-count range
3. Target audience
4. Style objective
5. Color scheme
6. Typography plan
7. Image approach
8. Slide rhythm plan
9. Per-slide component/layout assignment

For standard slides, use canvas metadata in the first `:root` block of `template.css`:

```css
:root {
  --slide-width: 1280px;
  --slide-height: 720px;
}
```

Use `960x720` for 4:3. Scenario documents own non-slide canvas formats.

If user images exist, run:

```bash
python3 ${SKILL_DIR}/scripts/analyze_images.py <project_path>/assets
```

Write `content_design_spec.md` from `${SKILL_DIR}/templates/content_design_spec_reference.md`, including project settings, a catalog theme ID, narrative, per-slide content/layout decisions, image decisions, colors, and typography. Record intentionally excluded assets.

### Step 5: Acquire Images When Needed

**Gate**: The design spec requests generated or searched images.

Read `${SKILL_DIR}/references/image-base.md`, then the relevant image workflow. Generate/search assets, verify files, and match image shape to the intended slot. Skip this phase when no new images are needed.

### Step 6: Author `content.html`

**Gate**: Design spec, selected theme, and required assets are ready.

Read executor base, exactly one style executor, shared standards, `template.css`, the selected `theme.md`, and `demo.html`.

Author standard slides with these constraints:

- Use `<section class="slide [mode] [modifier]" data-notes="...">` for every slide.
- Every slide must resolve to one valid mode: give it an explicit `light`, `dark`, `hero light`, or `hero dark` class; a selected theme's documented default mode in `theme.md` is also valid. Do not rely on an undocumented CSS fallback.
- Use only classes defined by the selected theme or required external libraries.
- Put reusable styling in `template.css`; use only canonical data-value inline styles from shared standards.
- Keep every slide visible in the settled export state without hover, timer, scroll, or active-carousel dependencies.
- Use action titles when they clarify the conclusion; allow short thematic titles for covers and dividers.
- Use relevant or user-required images and meaningful `alt` text. Do not insert unrelated assets merely to exhaust the folder.
- Keep TODOs, diagnostics, raw markup, component labels, and accidental source text out of rendered slides.
- Count all title, divider, hero, focus, and appendix slides within the requested range.
- Use `\(LaTeX\)` for inline MathJax formulas and `\[LaTeX\]` for display formulas.

Treat layout variety, component variety, dark/light alternation, and hero cadence as design heuristics. Use them when they improve hierarchy and pacing; allow deliberate repetition for comparisons, timelines, tutorials, and other content that benefits from a stable visual grammar.

### Step 7: Assemble, Review, Validate, and Export

**Gate**: `content.html`, `template.css`, and `index-template.html` exist.

#### 7.1 Source Gate

Before building, validate the project source and TCS contract only:

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --source-only --profile standard-project
```

Fix source/TCS errors before compiling. This is a project-directory gate; do not use the legacy single-file invocation for standard-slide delivery.

#### 7.2 Assemble and Render

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all
```

Require root `index.html`, matching slide counts in `output/svgs/`, `output/pngs/`, and `output/browser_pngs/`, plus `output/overview.png`, `output/dom-audit.json`, `output/render-fidelity.json`, and `output/compile-manifest.json`. Rerun after every source change. Diagnose compilation failures and retry up to five times.

`dom-audit.json` is the browser-layout truth: it records settled-DOM blockers
found before conversion plus theme-opted-in composition telemetry/review items.
Those composition measurements support rather than replace visual judgment.
`render-fidelity.json` records review-only differences between browser PNGs and
SVG-route PNGs. `compile-manifest.json` is the current-source receipt: it
fingerprints inputs, toolchain, assembled HTML, and published artifacts.

#### 7.3 Perform Visual Review

Follow `${SKILL_DIR}/workflows/visual-review.md` and `${SKILL_DIR}/references/visual-review.md`.

1. Inspect `output/overview.png`, then every browser-rendered PNG at a projection-like scale; the overview routes attention but is not a substitute for page review.
2. Use matching `output/pngs/` and `render-fidelity.json` only to diagnose conversion-route differences.
3. For every page, identify its vertical mode (centered cluster, top-to-bottom, split anchors, image hero, or intentional breathing). Fix content pages stranded at the top even when a footer makes the raw content span look full.
4. Fix blocking visual problems and pronounced composition/readability defects, re-run the source gate, rebuild with `--all`, and repeat up to three visual iterations.

Evaluate rhythm and diversity in context. Do not change a clear repeated layout solely to satisfy a numeric quota, and do not add filler merely to consume whitespace.

#### 7.4 Final Visual Gate

```bash
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --require-build --artifact-profile visual
```

This gate requires a current `compile-manifest.json`, all visual artifacts, and zero browser DOM-audit blockers. Fix hard errors such as stale/missing artifacts, TCS violations, missing files, broken classes/references, invalid structure, and DOM blockers. Treat render-fidelity and diversity/density findings as review prompts, not automatic failures.

#### 7.5 Export PPTX

```bash
python3 ${SKILL_DIR}/scripts/html_compiler.py <project_path> --all --include-pptx
python3 ${SKILL_DIR}/scripts/validate_project.py <project_path> --require-build --artifact-profile delivery
```

When PPTX is requested, use this same-build delivery sequence instead of a later standalone `--format pptx` export. Deliver root `index.html`, visual artifacts, receipts, and `output/slides.pptx`.

## Editing an Existing Deck

1. Read `content.html`, `template.css`, `index-template.html`, theme documentation, and current rendered output.
2. Edit semantic content in `content.html`; edit reusable presentation rules in `template.css`; preserve TCS.
3. Re-run the source gate, rebuild with `--all`, visually review affected pages, and pass the final visual gate. When PPTX is requested, rebuild with `--all --include-pptx` and pass the delivery profile.
4. Re-run planning only when the request changes the narrative, theme, or deck structure.

## Dependencies

```bash
pip install -r ${SKILL_DIR}/requirements.txt
cd ${SKILL_DIR}/scripts/html_to_svg
npm install
npx playwright install chromium
```

Open root `index.html` for local preview, but use the compiler's synchronized outputs for final review.
