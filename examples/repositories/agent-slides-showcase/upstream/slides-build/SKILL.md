---
name: slides-build
description: Build a complete presentation deck from a brief. Generates storytelling plan, slide operations, renders the deck, and runs QA. Requires extracted template contracts from /slides-extract. Use when the user wants to create slides, build a deck, generate a presentation, write a strategy deck, or says things like "make me a 10-slide deck on X", "create a presentation about Y", "build slides for the board meeting".
compatibility: Requires Python 3.12+ and uv.
---

# Slides Build

You are a presentation strategist and slide engineer. Your job is to translate business intent into a compelling, visually rich deck that an executive would present without changes.

Generate a complete deck from user intent + extracted template contracts.

## When to Use

- User wants to create a new presentation
- User provides a brief, topic, or content outline

## Prerequisites

`/slides-extract` must have run first. These artifacts must exist in the project directory (e.g., `output/<project>/`):

- `resolved_manifest.json` — merged template contract (primary reference)
- `base_template.pptx` — clean template
- `design-profile.json` — rendering and lint config
- `content_layout.json`, `archetypes.json`, `template_layout.json` — also generated but merged into resolved manifest

Before rendering, always run `slides preflight` to verify that the project directory, profile paths, icon pack, asset roots, and optional dependencies are all valid.

## References

| File | When to load | Content |
|---|---|---|
| `references/storytelling.md` | Always — before planning (Step 1) | Pyramid Principle, SCQA, WWWH, action titles, isomorphism, MECE |
| `references/content-density.md` | Always — before generating ops (Step 2) | Visual hierarchy, content area fill, split-panel composition, card patterns |
| `references/layout-patterns.md` | Always — before generating ops (Step 2) | Concrete ops patterns: cards, badges, KPI rows, callout boxes, timelines |
| `references/operations.md` | Always — during ops generation (Step 2) | Full operation reference with params |
| `references/common-mistakes.md` | Always — during QA (Step 5) | 25 ranked mistakes with fixes, pre-generation checklist |
| `references/chart-patterns.md` | **Only if** plan includes chart slides | Gray-first color strategy, chart type selection, chart+KPI combos, waterfall |
| `references/framework-patterns.md` | **Only if** plan includes SCQA hero, matrix, pyramid, or org chart slides | SCQA hero, 2x2 matrix, Harvey balls, pyramid, org chart |
| `references/process-patterns.md` | **Only if** plan includes process flow, timeline, or Gantt slides | Chevron flow, stage gates, Gantt bars, multi-track workstreams |

**Loading strategy:** Always load storytelling + content-density + layout-patterns + operations before generating ops. After completing the plan in Step 1, check which slide archetypes are in the plan — only then load the conditional references that match. Load common-mistakes during QA. This saves ~450 lines of context for decks that don't need charts, frameworks, or process diagrams.

## Process

### Step 1) Input intake

**Read `references/storytelling.md` before planning.** Apply WWWH, Pyramid Principle, SCQA, and isomorphism when structuring the deck.

Capture/confirm these fields:

- Audience
- Decision objective
- Core recommendation
- Scope constraints (time, geography, budget, BU)
- Target slide count

If any of the first 4 are missing, ask concise clarifying questions (max 5).

**Font size contract (lock during planning):**

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Action title | 24pt | Bold | Dark (`333333`) |
| Subheader / card title | 14-16pt | Bold | Brand (`primary_color_hex`) or `29BA74` |
| Body text | 14pt | Regular | `333333` or `575757` |
| Label / caption | 12pt | Regular | `575757` |
| Source line | 9pt | Regular | `999999` or `666666` |
| KPI number | 28-36pt | Bold | `29BA74` |

Lock these sizes before generating ops. Consistent sizes across slides are more important than perfect sizes on individual slides.

**Slide count convention:** N slides = N *content* slides. Title slide, disclaimer, and end/closing slides are always added but don't count toward the target. Example: "15 slides" = 15 content + title + disclaimer + end = 18 total.

### Step 2) Generate slides.json

Generate `slides.json` from user intent + `resolved_manifest.json`.

- Use the current agent model to generate slides-specific content on every run.
- Never hardcode topic content.
- **Before generating ops**, read `resolved_manifest.json` for each archetype's `resolved_layouts` — title method, body method, geometry, color zones, editable regions are pre-resolved.

#### Comprehension gate

After reading `resolved_manifest.json`, confirm you can answer:

- Which layout will each archetype use? Name the layout for at least the first 5 archetypes. (Note: `archetypes` is a **dict keyed by archetype ID**, not a list — iterate with `for aid, arch in archetypes.items()`)
- Which layouts are split-panel? What are the editable regions?
- What is the `primary_color_hex` from the design profile?

If any answer is unclear, re-read before generating ops.

#### Conditional reference loading

After completing the plan, scan `SlidePlan.visual_hint` and `archetype_id` values to decide which additional references to load:

- **Charts** (`add_bar_chart`, `add_pie_chart`, KPI+chart combos) → load `references/chart-patterns.md`
- **Frameworks** (SCQA hero, 2x2 matrix, Harvey balls, pyramid, org chart) → load `references/framework-patterns.md`
- **Processes** (chevron flow, stage gates, Gantt, workstreams, timelines with phases) → load `references/process-patterns.md`

Skip references that don't match any planned slide. This keeps context lean for simple text+shape decks.

`slides.json` structure:

```json
{
  "plan": {
    "deck_title": "...",
    "brief": "...",
    "audience": "...",
    "objective": "...",
    "slides": [
      {
        "slide_number": 1,
        "story_role": "opening",
        "archetype_id": "title_slide",
        "action_title": "..."
      }
    ]
  },
  "ops": {
    "operations": [
      {"op": "add_slide", "layout_name": "..."},
      {"op": "set_semantic_text", "slide_index": 0, "role": "title", "text": "..."}
    ]
  }
}
```

`SlidePlan` fields: `slide_number` (required), `story_role` (required), `archetype_id` (required), `action_title` (required), plus optional `key_points`, `visual_hint`, `source_note`.

`DeckPlan` fields: `deck_title` (required), `brief` (required), `slides` (required), plus optional `audience`, `objective`, `assumptions`.

Use `uvx --from agent-slides slides docs schema:slides-document` for full schema, `uvx --from agent-slides slides docs method:render` for operation inventory.

#### Ops Generation Rules

**Read `references/content-density.md` and `references/layout-patterns.md` before writing ops.**

**Placeholder awareness:**
- Check if the layout has a `TITLE (1)` placeholder before using `set_semantic_text role=title`. Layouts like "Agenda Full Width Overview" and "End" have zero placeholders — use `add_text` with coordinates and `font_color` from `color_zones`.
- Use `set_semantic_text role=body` only when the layout has a `BODY (2)` placeholder (e.g., "Title and Text"). Otherwise use `add_text`.
- For "Title and Text" layout: use `set_semantic_text` for both `title` and `body` — inherits template formatting.

**Speaker notes (mandatory for key slides):**
- Use `add_notes` on exec summary, recommendation, and data-heavy slides.

**Visual hierarchy (mandatory for rich slides):**
- Each content slide: 3+ `add_text` ops — heading (18-22pt bold), body (15-16pt), secondary (14pt gray `575757`).
- Use `primary_color_hex` from design profile as `font_color` for subheadings/accent text.
- Use `font_color: "575757"` for captions and supporting details.

**Split-panel composition:**
- Left panel (colored): big accent text (24-36pt bold, white), callout numbers, category labels.
- Right panel: repeating header+body pairs — header 20-22pt bold, body 15pt.
- Place action title as first `add_text` on right panel at `T=0.7`.

**Callout numbers:**
- Big callout numbers (36pt bold) in colored panels with label underneath (18pt).

**Shape ops for visual structure (mandatory for rich slides):**
- `add_rounded_rectangle`: card backgrounds (place BEFORE text ops).
- `add_rectangle`: thin accent bars (height ~0.06").
- `add_oval` (equal w/h): number badges.
- `add_line_shape`: dividers, timeline connectors, separators.
- `add_rounded_rectangle` with `border_color`: insight callout boxes.
- See `references/layout-patterns.md` for patterns.

**Icons:**
- Use `add_icon` on card/column layouts. Place at `size: 0.75` on cards, `size: 0.55` as accents.
- Use `color: "FFFFFF"` on dark backgrounds, omit for theme colors on light.
- Built-in: `generic_circle`, `generic_square`. Template-extracted icons are available when `icon_pack_dir` is set in the design profile — check the extraction report for available names.

**Charts:**
- `add_bar_chart` for comparisons, `add_line_chart` for trends, `add_pie_chart`/`add_doughnut_chart` for composition.
- `add_bar_chart` orientation: `"column"` (default) or `"bar"` — never `"vertical"` or `"horizontal"`.
- Follow with styling: `set_chart_title`, `set_chart_legend`, `set_chart_data_labels`, `set_chart_series_style`.
- `set_chart_data_labels` accepts `number_format`. `set_chart_data_labels_style` does NOT — only `position`, `font_size`, `show_legend_key`, `number_format_is_linked`.
- Set `fill_color_hex` per series to match template palette.
- Series format: `[["Series Name", [v1, v2, ...]], ...]`.

**Tables:**
- `add_table` with `rows` as 2D string array. Height ~0.5-0.6in/row.
- Leave 0.5" between table bottom and footer text.

**Source lines:**
- Every data slide: `font_size: 9`, `font_color: "666666"` or `"999999"`, at `top: 6.8`.

**Body placeholder clearing (mandatory):**
- On "Title and Text" layouts using `add_text` instead of `set_semantic_text role=body`: MUST add `{"op": "set_semantic_text", "slide_index": N, "role": "body", "text": " "}`.

**Font color vs. background contrast (mandatory):**
- Never `font_color: "FFFFFF"` on light backgrounds (`F2F2F2`, `FFFFFF`).
- Check `color_zones[].bg_color` before choosing colors.

**Structural slides (mandatory):**
- Include `disclaimer` slide (second-to-last). Layout already has legal text — just `add_slide`.
- `end_slide` (last) — minimal: deck title and brief line.
- Agenda layouts with fixed labels — don't duplicate via `add_text`.

**Document properties:**
- `set_core_properties` with `title`, `author`, `subject`.

### Step 3) Preflight (required)

Run a project preflight before any render attempt:

```bash
uvx --from agent-slides slides preflight --project-dir . --profile design-profile.json --compact
```

If preflight reports missing artifacts, broken profile paths, or dependency issues, fix those before continuing.

### Step 4) Dry-run (required)

```bash
uvx --from agent-slides slides render --slides-json @slides.json --profile design-profile.json --dry-run --compact
```

### Step 5) Render

```bash
uvx --from agent-slides slides render --slides-json @slides.json --profile design-profile.json --output output.pptx --compact
```

### Step 6) QA gate (required)

**Read `references/common-mistakes.md` and review the pre-generation checklist.**

```bash
uvx --from agent-slides slides qa output.pptx --profile design-profile.json \
  --slides-json @slides.json --out qa.json --compact
```

Review the output against the 25 ranked common mistakes. Note both issues found AND positive findings (things the deck does well).

## Placeholder Rules

- **Never use `set_placeholder_text` with guessed indices.** Use `set_semantic_text` with `role` (`title`, `subtitle`, `body`) for standard placeholders.
- Only use `set_placeholder_text` with exact `idx` from `inspect` or `template_layout.json`.

## Split-Panel Layout Rules

For layouts where the title placeholder sits in a side panel (not at the top):

1. Set `set_semantic_text` title to `" "` to clear the placeholder.
2. Place the slide title as `add_text` at the top of the RIGHT panel (`T=0.7`).
3. Place left-panel content only in `editable_above` / `editable_below` areas.
4. Use `color_zones[].text_color` for `font_color` on all `add_text` ops.

Check `resolved_manifest.json` -> archetype -> `resolved_layouts` -> `title_region` to determine if a layout is split-panel.

## Anti-patterns (what NOT to do)

- Don't generate ops without reading `resolved_manifest.json` first — layout names, geometry, and color zones must come from the contract
- Don't guess placeholder indices — use `set_semantic_text` with `role` or exact `idx` from inspect
- Don't use `font_color: "FFFFFF"` on light backgrounds or `"333333"` on dark backgrounds
- Don't duplicate fixed labels on agenda or structural layouts
- Don't skip the dry-run — it catches schema/op errors before rendering
- Don't add visual elements to title, disclaimer, or end slides

## Error Handling

On any slides error, run `uvx --from agent-slides slides docs method:preflight`, `uvx --from agent-slides slides docs method:render`, or `uvx --from agent-slides slides docs schema:slides-document` to verify the current contract before retrying.

## Acceptance Criteria

1. Output PPTX exists.
2. `qa.json` reports `"ok": true`.
3. No unresolved-token or contract-critical issues.
4. `slides preflight` reports `"ok": true` before render.
5. All content slides have action titles (complete sentences).
