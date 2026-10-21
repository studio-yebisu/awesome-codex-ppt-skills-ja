# codex-ppt-skill

`codex-ppt-skill` is a Codex skill for creating, editing, referencing, exporting, and QA-checking PowerPoint presentations.

It is designed for Chinese and English presentation workflows, with support for editable PPTX generation, template-based decks, HTML slide exports, visual asset planning, speaker notes, QA reports, and delivery manifests.

## What It Does

- Creates editable PowerPoint decks from topics, outlines, Markdown, DOCX, PDF, and PPTX sources.
- Edits existing decks while preserving core meaning, facts, and non-target slides.
- Supports single-slide edits with locked-slide comparison.
- References existing PPT files for style, structure, or both.
- Plans per-slide visual assets and requires Codex image2 / built-in imagegen for final generated raster illustrations.
- Exports PPTX, PDF, per-slide PNG previews, montage previews, QA reports, and delivery manifests.

## Install

Copy the skill folder into a Codex skill directory.

User-level install on Windows:

```powershell
Copy-Item .\codex-ppt-skill "$env:USERPROFILE\.codex\skills\codex-ppt-skill" -Recurse -Force
```

Project-level install:

```powershell
New-Item -ItemType Directory -Force .\.agents\skills | Out-Null
Copy-Item .\codex-ppt-skill .\.agents\skills\codex-ppt-skill -Recurse -Force
```

Then restart or refresh Codex so `/skills` can discover it.

## Optional Local Dependencies

Some workflows can use built-in Codex capabilities. Local fallback scripts need Python and Node packages.

Python:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Node:

```powershell
npm install
npx playwright install chromium
```

LibreOffice or Microsoft PowerPoint is recommended for PPTX to PDF/PNG export.

## Image Generation Rule

For final generated PPT illustrations, this skill expects Codex image2 through built-in `$imagegen`.

If Codex only shows an inline image and no local file is discoverable, save/download that image into:

```text
incoming_assets/imagegen_handoff/
```

The skill can then capture it into the run directory and insert it into the PPT.

## Example Prompts

```text
Use $codex-ppt-skill to make a 6-page PPT about AI-assisted lesson planning for ordinary teachers. Make it professional, clear, and lightly tech-oriented. Export PPTX, PDF, and PNG previews.
```

```text
Use $codex-ppt-skill to reference this PPT for style only. Replace the content with AI office automation and generate a new editable PPTX.
```

```text
Use $codex-ppt-skill to edit only slide 4. Make it more intuitive. Do not change any other slide.
```

## Repository Layout

```text
codex-ppt-skill/
  SKILL.md
  agents/
  references/
  scripts/
  design-system/
  assets/
  examples/
  evals/
```

Runtime outputs such as `ppt_runs/`, `outputs/`, `.venv/`, `node_modules/`, generated files, and user source documents are intentionally not included.
