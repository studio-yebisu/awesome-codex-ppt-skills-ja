---
name: slides-extract
description: Extract template contracts from a .pptx file. Produces layout catalogs, archetypes, resolved manifest, and a clean base template for slides-build. Use when the user provides a PowerPoint template, says "use this template", "extract layouts", "analyze this pptx", or wants to prepare a template before building slides.
compatibility: Requires Python 3.12+ and uv.
---

# Slides Extract

You are a template analyst. Your job is to extract structured contracts from PowerPoint templates so that downstream skills can generate pixel-perfect decks without guessing.

Extract template contracts from a `.pptx` template or sample deck.

## When to Use

- Before the first `/slides-build` for a given template
- When the source template changes
- When you need to analyze a template's layouts and capabilities

## Prerequisites

- A `.pptx` file (template or sample deck with example slides)

## Process

### Step 1) Create project directory

Create a dedicated directory for this project's artifacts:

```bash
mkdir -p output/<project-name>
```

All subsequent commands and outputs go in this directory.

### Step 2) Run extraction

Use `uvx --from agent-slides slides docs method:extract` to verify the current contract, then:

```bash
uvx --from agent-slides slides extract <template_or_sample.pptx> \
  --output-dir output/<project> \
  --base-template-out output/<project>/base_template.pptx \
  --compact
```

Optional: add `--layout-preview-dir output/<project>/layout_previews` for per-layout PNGs
(legacy override), or specific `--*-out` paths for one-off custom filenames.

### Step 3) Verify outputs

| Artifact | Purpose |
|---|---|
| `template_layout.json` | Physical layout families, placeholders, geometry |
| `content_layout.json` | Archetype-to-layout compatibility map |
| `archetypes.json` | Available archetypes with usage constraints |
| `resolved_manifest.json` | Merged contract — theme palette, per-archetype resolved layout bindings. Primary reference for `/slides-build`. |
| `slides_manifest.json` | Slide-by-slide inventory of the source |
| `slide_analysis.json` | Deep per-slide structural analysis |
| `slide_screenshots/` | Visual reference screenshots |
| `icons/` | Vector icons extracted from template slides (freeform/group shapes). Available via `add_icon` when `icon_pack_dir` is set in design profile. |
| `base_template.pptx` | Clean `.pptx` — all masters/layouts/theme, zero content slides |

### Step 4) Comprehension gate

Read `resolved_manifest.json` and verify you can answer these questions before proceeding:

- What accent colors does the theme use? List the hex values. (Path: `theme.palette.accent1` … `accent6`)
- How many archetypes have `resolved_layouts`? Name them. (Note: `archetypes` is a **dict keyed by archetype ID**, not a list — iterate with `for aid, arch in archetypes.items()`)
- Which layouts are split-panel (title in a side zone)?
- What `text_color` does each color zone use?

If any answer is unclear, re-read the manifest. Do not proceed to the design profile until all four are answered.

### Step 5) Build design profile

Write `design-profile.json` in the project directory:

```json
{
  "name": "<project-name>",
  "template_path": "base_template.pptx",
  "content_layout_catalog_path": "content_layout.json"
}
```

Add these fields from the extracted theme:

| Field | Source | Purpose |
|---|---|---|
| `primary_color_hex` | Theme accent1 | Brand accent color for subheadings |
| `text_color_light` | Theme lt1 | Light text for dark backgrounds |
| `text_color_dark` | Theme dk1 | Dark text for light backgrounds |
| `default_font_size_pt` | Template body size | Default for `add_text` |
| `icon_pack_dir` | `icons/` (if extracted) | Directory of template-specific vector icons for `add_icon` |

Always use `base_template.pptx` (not the original) as `template_path`.

If the extraction produced an `icons/` directory with `.xml` files, add `"icon_pack_dir": "icons"` to the design profile. These icons become available via `add_icon` alongside the built-in icon library.

**Only add fields listed above or in the schema.** The profile uses `extra="forbid"` — any unknown field (e.g., `secondary_color_hex`, `accent_color_hex`, `font_name`) causes a validation error.

Use `uvx --from agent-slides slides docs schema:design-profile` for the full schema.

### Step 6) Preflight the project

Before handing the project off to `/slides-build` or `/slides-full`, verify the extracted artifacts and profile:

```bash
uvx --from agent-slides slides preflight --project-dir output/<project> --profile output/<project>/design-profile.json --compact
```

If preflight fails, fix the project structure or profile paths before continuing.

## Outputs

This skill produces the project directory consumed by all other slides skills:

- `base_template.pptx` + contract JSONs -> `/slides-build`
- `design-profile.json` -> all post-build skills

## Error Handling

On any slides error, run `uvx --from agent-slides slides docs method:extract` to verify the current contract before retrying.

## Acceptance Criteria

1. All artifact files exist and are valid JSON (where applicable).
2. `resolved_manifest.json` contains at least one archetype with resolved layouts.
3. `base_template.pptx` opens without errors.
4. `design-profile.json` references `base_template.pptx` and `content_layout.json`.
5. `slides preflight` reports `"ok": true`.
6. Comprehension gate questions answered correctly.
